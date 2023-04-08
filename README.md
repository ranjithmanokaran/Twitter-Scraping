# Twitter Data Scraper and Storage
This is a Python-based project that allows users to scrape Twitter data based on a specified keyword or hashtag, date range, and maximum number of tweets to scrape. The scraped data is then stored in a MongoDB database along with the search criteria used to scrape the data.
# Getting Started
# Prerequisites
To run this project, you will need to have Python 3.7 or higher installed on your machine, as well as the following libraries:
-	streamlit
-	snscrape
-	pandas
-	pymongo <br/>

You can install these libraries by running the following command in your terminal:
```
pip install streamlit snscrape pandas pymongo
```
# Installation
To install this project, simply clone this repository onto your local machine:
```
git clone https://github.com/[username]/twitter-scraper.git
```
Then, navigate to the project directory and run the following command to start the Streamlit app:
```
streamlit run app.py
```
# Usage
Once the Streamlit app is running, you can enter a keyword or hashtag to search for, select a date range, and set the maximum number of tweets to scrape. Once you click the "Scrape Data" button, the app will scrape the Twitter data using the specified criteria and display it in a table on the page. You can then click the "Save to Database" button to save the scraped data to a MongoDB database, along with the search criteria used to scrape the data.
You can also download the scraped data as a CSV or JSON file by clicking the "Download CSV" or "Download JSON" button, respectively.

