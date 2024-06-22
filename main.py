from reddit_scraper import scrape_subreddits, extract_twitter_handels
from twitter_scraper import get_user_data
from scoring import calculate_hate_speech, calculate_engagement, calculate_user_influence, calculate_final_score

user_scores={}
hate_speech_score=0
engagement_score=0
network_score=0
influence_score=0

# Step 1
# Get names of potentialy harmful twitter users from harmful subreddits
target_tags = ['harm','death','violence','racism','supremacy','Controversial', 'hatespeech']
n=500
content=scrape_subreddits(target_tags,n)
twitter_accounts=extract_twitter_handels(content)

# step 2
# Fetch data from twitter using official api on each user and save in a dictionary
# This data includes tweets, likes, reposts, followers and followings, realtion to know offenders
user_data_dict=get_user_data(twitter_accounts)

# Step 3
# Score each user based on their data
for user, user_data in user_data_dict.items():
  tweets=user_data['tweets']
  if tweets:
       #the line on the bottom returns dict
    hate_speech_score=calculate_hate_speech(user_data['tweets'])

  if user_data['liked_tweets']:
    engagement_score= calculate_engagement(user_data['liked_tweets'])

  #if user_data['network_ids']:
   # network_score= calculate_network(user['network_ids'])
  network_score=0

    #This function calculate how influtential the user is by using his retweet, like, reply and view count, follower count
  influence_score=calculate_user_influence(user_data)

  final_score=calculate_final_score(hate_speech_score,engagement_score, network_score, influence_score)
  print(user, final_score)
  user_scores[user]=round(final_score,2)

# Step 4
# Get top 10 users with heighest score
sorted_user_scores = dict(sorted(user_scores.items(), key=lambda item: item[1], reverse=True))
top_10_users = dict(list(sorted_user_scores.items())[:10])
