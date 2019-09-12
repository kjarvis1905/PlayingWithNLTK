import keyring
import twython
import numpy
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

mps_list_url = "https://beta.parliament.uk/houses/1AFu55Hs/members/current"

def makeSoup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return BeautifulSoup(r.data)

def getMPHTTPList(soup):
    soup.find_all("ul", "list--block")

def startTwython():
    twi = twython.Twython(
        keyring.get_password("twitter", "api_key"),
        keyring.get_password("twitter", "api_secret_key"),
        keyring.get_password("twitter", "access_token"),
        keyring.get_password("twitter", "access_token_secret")
    )
    return twi

def getMPsHandles(twi):
    return twi.get_list_members(slug="UKMPs", owner_screen_name = "tweetminster", count=1000)

def makeMPsDF(twi):
    return pd.DataFrame(getMPsHandles(twi))


if __name__ == "__main__":
    twi = startTwython()
    mp_df = makeMPsDF(twi)
    mp_df[["name", "screen_name", "followers_count"]].sort_values("followers_count", ascending=False).head(15)