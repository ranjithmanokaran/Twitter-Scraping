import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
from io import BytesIO


def scrape_tweets(start_date, end_date, keyword, tweet_limit):
    # Define search query
    search_query = f'{keyword} since:{start_date} until:{end_date}'

    # Define empty list to store scraped tweets
    tweets_list = []

    # Use snscrape library to scrape tweets matching search query
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        if i >= tweet_limit:
            break
        # Get tweet properties
        date = tweet.date
        id = tweet.id
        url = tweet.url
        content = tweet.rawContent
        user = tweet.user.username
        reply_count = tweet.replyCount
        retweet_count = tweet.retweetCount
        language = tweet.lang
        source = tweet.sourceLabel
        like_count = tweet.likeCount

        # Append tweet properties to list
        tweets_list.append({'date': date.strftime("%Y-%m-%d"), 'id': id, 'url': url, 'content': content, 'user': user,
                            'reply_count': reply_count, 'retweet_count': retweet_count, 'language': language,
                            'source': source, 'like_count': like_count, 'keyword': keyword})

    # Convert list of tweets to Pandas DataFrame
    tweets_df = pd.DataFrame(tweets_list)

    return tweets_df


def download_csv(df):
    csv = df.to_csv(index=False)
    b = BytesIO()
    b.write(csv.encode())
    b.seek(0)
    return b


# Connect to MongoDB database
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['twitter_db']
tweets_collection = db['tweets']

# Set page title
st.set_page_config(page_title='Twitter Scraper')

# Set page header
st.header('Twitter Scraper')

# Get user input for keyword or hashtag to search
keyword = st.text_input('Enter a keyword or hashtag to search')

# Get user input for start and end dates
start_date = st.date_input('Start Date')
end_date = st.date_input('End Date')

# Get user input for tweet limit
tweet_limit = st.number_input('Tweet Limit', min_value=1, max_value=1000)

# Check if user has entered all required inputs
if keyword and start_date and end_date and tweet_limit:
    if start_date < end_date:
        # Scrape tweets and create DataFrame
        tweets_df = scrape_tweets(start_date.strftime(
            '%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), keyword, tweet_limit)

        # Display DataFrame
        st.dataframe(tweets_df)

        tweets_dict = tweets_df.to_dict('records')
        scraped_data = {
            "Scraped Word": keyword,
            "Scraped Date": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            "Scraped Data": tweets_dict
        }
        tweets_df['income'] = len(tweets_df)
        if tweets_df.empty == False:
            if st.button('Upload to MongoDB'):
                tweets_collection.insert_one(scraped_data)
                st.success('Tweets uploaded to MongoDB')

            if st.button('Download'):
                csv_file = download_csv(tweets_df)
                st.download_button(
                    label="Download CSV",
                    data=csv_file,
                    file_name=f"{keyword}_tweets.csv",
                    mime="text/csv"
                )
                st.download_button(
                    label="Download JSON",
                    data=tweets_df.to_json(orient='records'),
                    file_name=f"{keyword}_tweets.json",
                    mime="application/json"
                )
    elif start_date == end_date:
        st.warning('Start date and end date cannot be same')
    else:
        st.warning('Start date cannot be greater than end date')

else:
    st.warning('Fill all the inputs to search for tweets')
