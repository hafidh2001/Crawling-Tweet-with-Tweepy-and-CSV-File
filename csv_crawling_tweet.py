# CRAWLING DATA TWITTER
# NAMA  : HAFIDH AHMAD FAUZAN
# NIM   : 19051397027
# PRODI : D4 MI 2019 A



####### IMPORT LIBRARY PYTHON #######
import tweepy
import sys
import csv

import os
import warnings
os.system("CLS")
warnings.filterwarnings('ignore')



####### DEVELOPER NAME #######
print("\n" + 100 * "=")
print("CRAWLING DATA TWITTER".center(100))
print("developed by".center(100))
print("\n")
print("HAFIDH AHMAD FAUZAN  |  TAUFIK NURRAHMAN  |  FACHREZA NORRAHMA".center(100))
print("    19051397027      |    19051397019     |     19051397036   ".center(100))
print("=" * 100 + "\n")



####### MAKE VARIABEL TOKEN #######
# MAKE CLASS AND FUNCTION TO HIDDEN DECLARE API AND TOKEN TWITTER
class Twitter:
    def __init__(self):
        self.api_key = ""
        self.api_key_secret = ""
        self.access_token = ""
        self.access_token_secret = ""

# MAKE RETURN FUNCTION TO RETURNS AN OBJECT OF CLASS TWITTER
def twitter_auth():
    return Twitter()

# DECLARE VARIABEL TO CALL FUNCTION
call_twitter_auth = twitter_auth()



####### AUTHENTICATE TWITTER #######
auth = tweepy.OAuthHandler(call_twitter_auth.api_key, call_twitter_auth.api_key_secret)
auth.set_access_token(call_twitter_auth.access_token, call_twitter_auth.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# CHECK CONNECTION TWITTER
print("Check Connection :")
try:
    api.verify_credentials()
    print("Autentikasi twitter berhasil dihubungkan")
except:
    print("Autentikasi twitter gagal")



####### CRAWLING TWITTER DATA #######
# ATTACHMENT CRAWLING
tweetsPerQuery = 100
maxTweets = 1000
sinceId = None
maxId = -1
tweetCount = 0

print("\n")
search_key = (input(r"Search Key      : "))
name_file = (input(r"File Names .CSV : "))
file_csv = (name_file + ".csv")

# CODE
print("\n" + 100 * "=")
print(f"START DOWNLOAD '{search_key}' TWEETS WITH MAX-COUNT : {maxTweets}".center(100))
print("=" * 100 + "\n")

# use library csv with encode utf-8
with open(file_csv, 'a+', newline='', encoding='utf-8') as csv_file:
    while tweetCount < maxTweets:
        try:
            if (maxId <= 0):
                if (not sinceId):
                    newTweets = api.search_tweets(q=search_key, lang="id", count=tweetsPerQuery, result_type="recent")
                else:
                    newTweets = api.search_tweets(q=search_key, lang="id", count=tweetsPerQuery, result_type="recent", since_id=sinceId)
            else:
                if(not sinceId):
                    newTweets = api.search_tweets(q=search_key, lang="id", count=tweetsPerQuery, result_type="recent", max_id=str(maxId - 1))
                else:
                    newTweets = api.search_tweets(q=search_key, lang="id", count=tweetsPerQuery, result_type="recent", max_id=str(maxId - 1), since_id=sinceId)

            if not newTweets:
                print("\n" + f"No more Tweets found with query = '{search_key}'")
                break

            # make header of file.csv
            fieldNames = ["IdTweet", "IdUser", "UserName", "ScreenName", "Location", "TweetAt", "UploadTweet", "OriginalTweet"]
            write_csv = csv.DictWriter(csv_file, fieldnames=fieldNames, delimiter=",")
            write_csv.writeheader()

            # insert value in dictionary
            for tweet in newTweets:
                dictTweet = {
                    "IdTweet": tweet.id,
                    "IdUser": tweet.user.id,
                    "UserName": tweet.user.name,
                    "ScreenName": tweet.user.screen_name,
                    "Location": tweet.user.location,
                    "TweetAt": tweet.created_at,
                    "UploadTweet": tweet.source,
                    "OriginalTweet": tweet.text
                }

                # looping record value
                write_csv.writerow(dictTweet)

            # descriotion crawl data
            tweetCount += len(newTweets)
            sys.stdout.write("\r")
            sys.stdout.write(f"Total downloaded Tweets : {tweetCount}")
            sys.stdout.flush()
            maxId = newTweets[-1].id

        except tweepy.TweepyException as error:
            print("Error code : " + str(error))
            break

print("\n\n" + 100 * "=")
print(f"CRAWLING DATA FINISH".center(100))
print(f"{tweetCount} STORED TWEETS WITH FILE NAMES : '{file_csv}'".center(100))
print("=" * 100 + "\n")
