import pandas as pd
import datetime
import os



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
    print(tweet)


