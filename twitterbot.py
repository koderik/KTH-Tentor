import pandas as pd
import tweepy
import datetime
import os

# api key
# Enter your API keys and tokens here
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


# Create a tweet and post it to your Twitter account

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)
# response = client.create_tweet(text='hello world')

# print(response)

# Read data from CSV file and store in dataframe
df = pd.read_csv("exams.csv")

# Keep first instance of duplicate rows based on "Startdatum" and "Grupp" columns
df = df.drop_duplicates(subset=["Startdatum", "kurskod"], keep="first")

# Keep only rows where "Aktivitet" is "Tentamen"
df = df[df["Aktivitet"] == "Tentamen"]

# Remove " Helklass" from "Grupp" column
df["kurskod"] = df["kurskod"].str.replace(" Helklass", "")

# Split rows with comma-separated "Grupp" values into multiple rows
df = (
    df.set_index(df.columns.drop("kurskod", 1).tolist())
    .kurskod.str.split(", ", expand=True)
    .stack()
    .reset_index()
    .rename(columns={0: "kurskod"})
    .loc[:, df.columns]
)
# if "FUNK" in kurskod, drop the row
df = df[~df["kurskod"].str.contains("FUNK")]

# Truncate "Grupp" values to 6 characters
df["kurskod"] = df["kurskod"].str[:6]

# Keep first instance of duplicate rows based on "Startdatum" and "Grupp" columns
df = df.drop_duplicates(subset=["Startdatum", "kurskod"], keep="first")

# Create dictionary with dates and tweets
tweets = {}

# Iterate through unique values in "Startdatum" column
for date in df["Startdatum"].unique():
    # Get rows for current date
    exams = df[df["Startdatum"] == date]

    # Build tweet with exam information for current date
    tweet = date + "\nIdag skrivs " + str(len(exams)) + " tentor!\nDagens tentor är:"
    groups = {}

    for index, row in exams.iterrows():
        try:
            group = row["kurskod"]
            start = row["Starttid"]
            end = row["Sluttid"]

            # Check if this start and end time combination is already in the dictionary
            if (start, end) in groups:
                # If it is, append the course to the list of courses for this start and end time
                groups[(start, end)].append(group)
            else:
                # If it isn't, create a new entry in the dictionary for this start and end time
                groups[(start, end)] = [group]
        except:
            print("Error")

    # Iterate through the dictionary and generate the tweets
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    # check if course SF1918 in the vals

    # Iterate through the sorted groups and generate the tweets
    for time, courses in sorted_groups:
        start, end = time
        tweet += "\n" + ", ".join(courses) + ": " + str(start) + "-" + str(end)
    # if tweet longer than 280 chars, make the last three chars "..."
    tweet += "\nLycka till!"
    tweets[date] = tweet


# if there is a tweet today, post it to Twitter
today = datetime.date.today().strftime("%Y-%m-%d")

if today in tweets:
    tweet = tweets[today]
    # Initialize the variables for the loop
    lines = tweet.split("\n")

    # Initialize the variables for the loop
    tweet_id = None
    current_tweet = ""

    # Loop through the lines
    for line in lines:
        # Check if adding the line to the current tweet would result in a tweet that is longer than 280 characters
        if len(current_tweet) + len(line) <= 280:
            # If it doesn't, add the line to the current tweet
            current_tweet += "\n" + line
        else:
            # If it does, post the current tweet as a reply to the previous tweet and start a new tweet with the line
            status = api.update_status(current_tweet, in_reply_to_status_id=tweet_id)
            tweet_id = status.id
            current_tweet = line

    # Check if there is a current tweet that hasn't been posted
    if current_tweet:
        # If there is, post it as a reply to the previous tweet
        api.update_status(current_tweet, in_reply_to_status_id=tweet_id)

    # print(tweets[today])
    # response = client.create_tweet(text=tweets[today])
