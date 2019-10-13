import keyring
import twython
import numpy
import pandas as pd
import re

def startTwython():
    twi = twython.Twython(
        keyring.get_password("twitter", "api_key"),
        keyring.get_password("twitter", "api_secret_key"),
        keyring.get_password("twitter", "access_token"),
        keyring.get_password("twitter", "access_token_secret")
    )
    return twi

def getMPsHandles(twi):
    list_members = twi.get_list_members(slug="UKMPs", owner_screen_name = "tweetminster", count=1000)
    members = list_members['users']
    return members
    
def makeMPsDF(twi):
    return pd.DataFrame(getMPsHandles(twi))

def processTweet(tweetJson):
    """Takes a tweet dict and processes it for insertion into dataframe"""
    processed = {
        "tweet_id" : tweetJson["id"],
        "favorite_count" : tweetJson["favorite_count"],
        "retweet_count" : tweetJson["retweet_count"],
        "text" : tweetJson["text"]
    }
    return processed

regexExpressions = "|".join([r"@\w*", r":"])#, r"?", r"#"])
regexCleaner = re.compile(regexExpressions)
regexWhitespace = r"\s\s+"
whiteSpaceCleaner = re.compile(regexWhitespace)

def cleanTweetText(text):
    """Twitter returns a utf-8 encoded string, which is the default python string encoding as
    of version 3. UTF-8 is a variable-length encoding scheme. The number of bytes that a character,
    or code-point is encoded by is determined by the number of MSB of the leading byte. 
    The first 2^7 code points use 1 byte: 0xxxxxxx
    The next 2^11 points use 2 bytes: 110xxxxx 10xxxxxx
    And so on... Python expects strings to be formatted in utf-8
    ord(x) takes a series of bytes and returns the code-point number
    ascii(x) returns an ascii-readable string"""
    asciiStr = text.encode("ascii", errors='ignore').decode() #Result maps to same characters in utf-8
    cleaned = regexCleaner.sub("", asciiStr)
    whiteSpaceCleaned = whiteSpaceCleaner(cleaned)
    return whiteSpaceCleaned

def processMPHandle(mpJSON):
    """Takes a twitter user object and prepares it for insertion into a dataframe"""
    processed = {
        "id" : mpJSON["id"],
        "id_str" : mpJSON["id_str"],
        "name" : mpJSON["name"],
        "screen_name" : mpJSON["screen_name"],
        "friends_count" : mpJSON["friends_count"],
        "followers_count" : mpJSON["followers_count"]
    }
    return processed

def processAllTwitterHandles():
    twi = startTwython()
    mps_handles = getMPsHandles(twi)
    processedHandles = [processMPHandle(x) for x in mps_handles]
    return processedHandles


if __name__ == "__main__":
    twi = startTwython()
    print("started twython")
    mp_df = makeMPsDF(twi)
    print("Made dataframe")
    mp_df[["name", "screen_name", "followers_count"]].sort_values("followers_count", ascending=False)
