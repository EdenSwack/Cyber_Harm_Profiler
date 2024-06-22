#In this part we aim to develop a scoring algorithm based on the data we've collected for each user, and then, give each user a score.

#Genreal outline of the process for each user:

#Tweets Score
#Engagment score (tweets liked)
#Network Score
#Influence scrore based on user views and size of network
#Final score, using previous scores


def calculate_hate_speech(tweets):
  # Weight given for total number of hate words:
  x=3
  y= 2
  count_hate_words_total=0
  hate_words_frequency=0

  # Generated hate speech tokens using AI, I didnt write them myself! ;)
  hate_speech_tokens = [
    "racist", "nazi", "bigot", "homophobe", "terrorist", "kike", "nigger",
    "fag", "dyke", "tranny", "spic", "chink", "gook", "sandnigger",
    "towelhead", "wetback", "beaner", "cripple", "retard", "mongoloid",
    "coon", "jigaboo", "porchmonkey", "tarbaby", "darky", "negro",
    "sambo", "whitey", "cracker", "honky", "gook", "chink", "slant",
    "slanteye", "nip", "chink", "jap", "slit-eye", "yellow", "camel jockey",
    "raghead", "islamist", "mohammedan", "muzzie", "paki", "hajji",
    "injun", "chief", "squaw", "wigger", "hillbilly", "redneck",
    "white trash", "peckerwood", "hooknose", "kike", "hebe", "yid",
    "sheeny", "coonass", "darkie", "pickaninny"
]

  for tweet in tweets:
    count_hate_words=0
    count_words=len(tweet.split())

    for keyword in hate_speech_tokens:
           count_hate_words += len(re.findall(r'\b' + re.escape(keyword) + r'\b', tweet.lower()))

    if count_hate_words:
          # Saving this var to find the total amount of hate words in the users tweets
      count_hate_words_total+=count_hate_words
      #Calculate frequency of hate speech word in this tweet
      hate_words_frequency+=(count_words/count_hate_words)

    #Calculate average hate words per tweet by summing the total frequency of each tweet and deviding by number of tweets
  avg_hate_word_frequency=hate_words_frequency/len(tweets)
    # Save total amount of hate words tweeted by user
  total_hate_words=count_hate_words_total

  user_hates_speech_score= x*avg_hate_word_frequency + ( y* total_hate_words)

  return user_hates_speech_score

def calculate_engagement(liked_tweet_ids):
  return(calculate_hate_speech(liked_tweet_ids))

#def calculate_influence(user_data):


def calculate_final_score(hate_speech_score,enagement_score, network_score, influence_score):
  hate_speech_weight = 0.3
  engagement_weight = 0.2
  network_weight = 0.2
  influence_weight = 0.1

  final_score = ( hate_speech_score * hate_speech_weight + engagement_score * engagement_weight + network_score * network_weight) * (influence_score * influence_weight)
  return final_score


def calculate_network(network_ids):
  offender_connection=0
  connection_weight=0.3
  user_ids=network_ids['followers_ids'].append(network_ids['following_ids'])
  offenders_list=get_offenders_list()

  offender_connection_count = sum(1 for user_id in user_ids if user_id in offenders_list)

  network_score=offender_connection_count*connection_weight
  return network_score


def calculate_user_influence(user_data):
  retweet_weight = 0.3
  favorite_weight = 0.2
  reply_weight = 0.1
  view_weight = 0.2
  followers_weight = 0.2

  retweet_count=user_data['retweet_count']
  followers_count=user_data['followers_count']
  favorite_count=user_data['favorite_count']
  reply_count=user_data['reply_count']
  view_count=user_data['view_count']

  influence_score = (retweet_count * retweet_weight) + (favorite_count * favorite_weight) + (reply_count * reply_weight) + (view_count * view_weight) + (followers_count * followers_weight)

  return influence_score
