import praw
import prawcore
import re
import tempfile
from config import client_id, client_secret, user_agent, username


def scrape_subreddits(target_tags, n):
    reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    check_for_async=False)
    
    harmful_subreddits = []
    for tag in target_tags:
        for subreddit in reddit.subreddits.search('flair_name:"' + tag + '"', limit=None):
            harmful_subreddits.append(subreddit)

    subreddits_saved = 0
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as post_text:
        file_path = post_text.name
        for subreddit_v in harmful_subreddits:
            subreddit = reddit.subreddit(subreddit_v.display_name)
            try:
                for submission in subreddit.top(limit=n):
                    post_text.write(submission.selftext)
                    subreddits_saved += 1
            except (prawcore.exceptions.Forbidden, prawcore.exceptions.NotFound, prawcore.exceptions.RequestException) as e:
                print(f"Error accessing subreddit '{submission.title}': {e}")
    with open(file_path, 'r') as file:
    content = file.read()

    return content

def extract_twitter_handles(content):
    with open(file_path, 'r') as file:
        content = file.read()

    twitter_accounts = re.findall(r'@\w+', content)
    twitter_accounts = list(set(twitter_accounts))
    twitter_accounts = [account[1:] for account in twitter_accounts]

    return twitter_accounts
