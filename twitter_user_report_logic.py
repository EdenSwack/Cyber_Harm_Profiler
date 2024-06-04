import praw
import json

# Import API credentials from config.py
from config import (
    reddit_client_id, reddit_client_secret, reddit_user_agent, reddit_username,
    twitter_api_key, twitter_api_host
)







# Find subreddits that could be potentially harmfull
  # Lets define subjects we deem as harmful
target_tags = ['harm','death','violence','racism','supremacy','Controversial', 'hatespeech']

harmful_subreddits = []

for tag in target_tags:
  for subreddit in reddit.subreddits.search('flair_name:"' + tag + '"', limit=None):
      harmful_subreddits.append(subreddit)


