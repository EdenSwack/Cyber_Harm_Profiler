import praw
import prawcore
import re
import tempfile

def scrape_subreddits(reddit, target_tags, n):
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

    return file_path

def extract_twitter_handles(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    twitter_accounts = re.findall(r'@\w+', content)
    twitter_accounts = list(set(twitter_accounts))
    twitter_accounts = [account[1:] for account in twitter_accounts]

    return twitter_accounts
