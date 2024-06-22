from twitter_scraper import get_userID, get_user_metrics
# We'll create a dictionary of dictionaries for the users in the "twitter_accounts" list
# For each twitter account we'll save each of their tweets and each of their tweets metrics in to another dictionary
# for each account we'll save their engagement metrics
def get_user_data(twitter_accounts):
  user_data_dict={}

  for account in twitter_accounts:
  #initializing dict to save data for current account in this iteration
    user_data={}

  #getting uid for later use
    userID=get_userID(account)

  #if user still exists
    if userID:
      user_data["userID"]=userID
      #getting tweets, follower count and engagement metrics
      user_metrics=get_user_metrics(userID)
      user_data.update(user_metrics)
      user_data_dict[account] = user_data
    else:
      print(f"User \"{account}\" doesn't exist in twitter anymore or can't be accesed currently. :( ")
  return user_data_dict
