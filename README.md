# Twitter User Report

This project aims to identify potentially harmful Twitter users by scraping Reddit for Twitter handles mentioned in controversial subreddits, collecting data from the Twitter API, and calculating a score based on various metrics to rate the harmfulness of each user.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Collection](#data-collection)
- [Data Enrichment](#data-enrichment)
- [Scoring Mechanism](#scoring-mechanism)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/EdenSwacm/twitter-user-report.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up the necessary API credentials for Reddit and Twitter in the `config.py` file.
2. Run the `twitter_user_report.py` script:

   ```bash
   python twitter_user_report.py
   ```

## Project Structure

```
twitter-user-report/
├── config.py
├── data/
│   ├── raw_user_data.json
│   └── top_10_raw_user_data.json
├── twitter_scraper.py
├── reddit_scraper.py
├── scoring.py
├── main.py
├── README.md
└── requirements.txt
```

- `config.py`: Contains the API credentials for Reddit and Twitter.
- `data/`: Directory to store the raw user data and the top 10 user data.
- `twitter_scraper.py`: api calls to twitter and custom functions to handel and use the needed output from the api calls
- `reddit_scraper.py`: functions using praw to save data and relevant content from reddit
- `scoring.py`: custom scoring functions used to calculate metrics such as ingagement of inlfuence
- `main.py`: the main script which as a result create a list of the top 10 most potentially harmful twitter users
- `README.md`: This documentation file.
- `requirements.txt`: List of required Python packages.

## Data Collection

The script uses the PRAW (Python Reddit API Wrapper) library to scrape Reddit for potentially harmful subreddits based on predefined tags. It then retrieves the top `n` posts from these subreddits and extracts any mentioned Twitter user handles using regular expressions.

## Data Enrichment

For each Twitter user handle found, the script uses the Twitter API to collect various data points, such as user IDs, tweets, follower/following counts, engagement metrics (views, likes, replies, retweets), and network information (followers/following IDs).

## Scoring Mechanism

The script calculates a score for each user based on the following metrics:

1. **Tweet Score**: Calculates the total number of hate words in the user's tweets and the average hate word frequency.
2. **Engagement Score**: Calculates the tweet score for the content the user has liked.
3. **Network Score**: Checks if the user has connections with known offenders in their network.
4. **Influence Score**: Calculates the user's influence and potential based on their total views, network size, and engagement metrics (replies, likes, retweets).
5. **Final Score**: Combines the previous scores using custom weights to determine the user's overall harmfulness.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize this documentation as per your project's specific requirements, adding more detailed sections or examples as needed.
