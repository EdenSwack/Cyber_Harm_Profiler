import requests
from config import twitter_api_key, twitter_api_host

# General, all purpose call handler for general calling of api calls and handeling responses
def call_api(user, method):
  headers = {
      "X-RapidAPI-Key": twitter_api_key,
      "X-RapidAPI-Host": twitter_api_host
    }
  try:
    response = requests.get(method, headers=headers, params=user)
    response.raise_for_status()  # Raise exception for 4xx or 5xx errors
    return response.json()
  except:
    return None


#Function that takes the user name we scraped form before and provides a twitter user id needed for api calls
def get_userID(user_name):
    url = 'https://twitter135.p.rapidapi.com/v2/UserByScreenName/'
    user_param = {"username": user_name}

        #adding this exception in cases where user is no longer in twitter/his id can be accessed by api currently
    try:
        response = call_api(user_param, url)
        if response:
            if 'rest_id' in response.get('data', {}).get('user', {}).get('result', {}):
                userID = response['data']['user']['result']['rest_id']
                return userID
            else:
                print("Error: 'rest_id' not found in response")
                return None
        else:
            return None
    except Exception as e:
        print("Error during API call:", e)
        return None


#Function that recieves a json file of all users tweets an extract ids needed for api calls
# This code cells containes functions that handle tweets and their metrics
import json

def get_user_tweets(userID):
  url = "https://twitter135.p.rapidapi.com/v2/UserTweetsAndReplies/"
  user_param={"id": userID}
  tweets_replies_json=call_api(user_param,url)
  if tweets_replies_json:
    tweet_ids=extract_tweet_ids(tweets_replies_json)
    return tweet_ids
  return None

def extract_tweet_ids(json_data):
    tweet_ids = []

    def traverse(obj):
        if isinstance(obj, dict):
            if obj.get('__typename') == 'Tweet' and obj.get('legacy', {}).get('conversation_id_str') == obj.get('rest_id'):
                tweet_ids.append(obj.get('rest_id'))
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(json_data)
    return tweet_ids


#Function to get metrics for each tweet such as text, reply count, favorite count (likes), views and retweets
# Then saves all this info into a dictionary for that tweet and returns it
def get_tweet_metrics(tweet_id):
  tweet_metrics={}
  url= "https://twitter135.p.rapidapi.com/v2/TweetDetail/"
  param={"id":tweet_id }

# Exception handeling for when tweets have missing data
# For example not all tweets have replies, likes or views
# Exception handeling will make sure the function will continue gathering data even when one metric is missing
  try:
      tweet_json_raw = call_api(param, url)
      tweet_json_metrics = tweet_json_raw['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']

      tweet_metrics["id"] = tweet_id
      try:
        tweet_metrics["text"] = tweet_json_metrics['legacy']['full_text']
      except:
        tweet_metrics["text"] = ''
      try:
        tweet_metrics["reply_count"] = int(tweet_json_metrics['legacy']['reply_count'])
      except KeyError:
        tweet_metrics["reply_count"]=0

      try:
        tweet_metrics["favorite_count"] = int(tweet_json_metrics['legacy']['favorite_count'])
      except KeyError:
        tweet_metrics["favorite_count"] =0

      try:
        tweet_metrics["view_count"] = int(tweet_json_metrics['views']['count'])
      except KeyError:
        tweet_metrics["view_count"]=0

      try:
        tweet_metrics["retweet_count"] = int(tweet_json_metrics['legacy']['retweet_count'])
      except KeyError:
        tweet_metrics["retweet_count"] =0

  except KeyError as e:
      print(f"KeyError while fetching metrics for tweet ID {tweet_id}: {e}")
  except Exception as e:
      print(f"Unexpected error while fetching metrics for tweet ID {tweet_id}: {e}")

  return tweet_metrics


# Function to get number of followers

def count_followers(userID):
  url = "https://twitter135.p.rapidapi.com/v1.1/Users/"
  user_param={"ids": userID}
  response=call_api(user_param,url)
  if response:
    if 'followers_count' in response[0]:
      return response[0]['followers_count']
    else:
      print("No follower count found")
  else:
      print("Error: No response received from the API")
  return None

def get_user_likes(userID):

  params={"id":userID}
  url = "https://twitter135.p.rapidapi.com/v2/Likes/"
  likes_json_raw=call_api(params,url)
  tweet_ids=extract_tweet_ids(likes_json_raw)
  return tweet_ids

# This function returnes a dictionary containing ids of the input usef followers and users he follows
# This function is to discover connections with known offenders

def get_network_ids(userID):
  network_ids={}
  params={"id":userID}

  followers_url = "https://twitter135.p.rapidapi.com/v1.1/FollowersIds/"
  following_url="https://twitter135.p.rapidapi.com/v1.1/FollowingIds/"

  followers_ids=call_api(params,followers_url)
  following_ids=call_api(params,following_url)
  try:
    network_ids["followers_ids"]=followers_ids['ids']
  except:
    network_ids["followers_ids"]=[]
  try:
    network_ids["following_ids"]=following_ids['ids']
  except:
    network_ids["following_ids"]=[]

  return network_ids


# Comprehensive function that recevies a user id and returns data such as:
  # Dictionary containin all that user tweets and the tweets metrics explained before
  # Total reply count of all that users tweets
  # Total favorite count (likes) "" "" "" ""
  # Total view count "" "" ""
  # Total retweet count " "
  # List of Tweet id's of the the tweets the user liked
  # Number of followers
  # IDs of followers and following users

def get_user_metrics(userID):
  # initalizing neccesary data sturtures
  user_metrics={}
  tweets=[]
  reply_count=0
  favorite_count=0
  view_count=0
  retweet_count=0

  #  Getting tweet data
      #1- extract tweet ids for given user
  tweet_ids=get_user_tweets(userID)
  if tweet_ids:
    for id in tweet_ids:
      tweet_metrics=get_tweet_metrics(id)
       #2- get tweet text by id
      try:
        tweets.append(tweet_metrics["text"])
      except: pass
      #3- get reply count for tweet
      try:
        reply_count+=tweet_metrics["reply_count"]
      except: pass
      #4- get favorite count for each tweet
      try:
        favorite_count+=tweet_metrics["favorite_count"]
      except: pass
      #5- get favorite count for each tweet
      try:
        view_count+=tweet_metrics["view_count"]
      except: pass
      #6- get tweet retweet count
      try:
        retweet_count+=tweet_metrics["retweet_count"]
      except: pass

# Saving all info into the users dictionary
  user_metrics["followers_count"]=count_followers(userID)
  user_metrics["liked_tweets"]=get_user_likes(userID)
  user_metrics["network_ids"]=get_network_ids(userID)
  user_metrics["tweets"]=tweets
  user_metrics["reply_count"]=reply_count
  user_metrics["favorite_count"]=favorite_count
  user_metrics["view_count"]=view_count
  user_metrics["retweet_count"]=retweet_count

  return user_metrics
