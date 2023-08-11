# Welcome to the KTH Exam Twitter Bot
This Twitter bot is designed to scrape and reformat calendar data on all exams at KTH and tweet what exams are taking place on each day. The bot uses Pandas and Tweepy to accomplish this.

## Features
Scrapes and reformats calendar data on all exams at KTH.
Tweets what exams are taking place on each day.
## Getting Started
To run the Twitter bot locally, you'll need to have the following software installed on your computer:

* Python 3.x
* Pandas
* Tweepy

Clone the repository and install the dependencies by running the following command in your terminal:

```
pip install -r requirements.txt
```
## Setting up Twitter API
To use the Twitter API, you'll need to create a Twitter Developer account and create a new app. Once you've done that, you'll have access to your API key and API secret key.

## Setting up Environment Variables
To store your Twitter API key and API secret key, you can use environment variables. You can use a package such as python-dotenv to manage environment variables in your code.

1. Create a .env file in the same directory as your code.
2. Add the following lines to the `.env` file, replacing `YOUR_API_KEY` and `YOUR_API_SECRET_KEY` with your actual API key and API secret key:
```
TWITTER_API_KEY=YOUR_API_KEY
TWITTER_API_SECRET_KEY=YOUR_API_SECRET_KEY
```
In your code, access the API keys using `os.environ['TWITTER_API_KEY']` and `os.environ['TWITTER_API_SECRET_KEY']`.
## Setting up the exams
Go to Canvas Schedules, Select Activity Tentamen and download as CSV. Remove the first two rows with Title and Dates. Also change **Tillfälle/kurskod** to only **kurskod**

##Running the Bot
To run the bot, execute the following command in your terminal:

```
python twitterbot.py
```
The bot will start scraping the exam data and tweeting what exams are taking place on each day.

## Note
The bot will only tweet once a day, so you'll need to run it every day to ensure that it keeps tweeting.
You can customize the frequency of tweets and the format of the tweets in the code.
The code assumes that the exam data is available in a specific format. You may need to modify the code to work with the actual exam data format other universities.
## Conclusion
With this Twitter bot, you can keep up-to-date with all exams taking place at KTH. The bot is easy to set up and customize, making it a valuable tool for students and educators alike.
