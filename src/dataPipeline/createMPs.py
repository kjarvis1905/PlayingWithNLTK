import numpy
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import config

def makeSoup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return BeautifulSoup(r.data)

def getMPHTTPList(soup):
    card_details = soup.find_all("a", class_="people-list__person")
    mp_details = [{"name": x.find("h2", class_="people-list__person__name").getText(),
    "constituency": x.find("span", class_="people-list__person__constituency").getText(),
    "party": x.find("span", class_="people-list__person__party").getText()} for x in card_details]
    return mp_details

def getMPsAsDict():
    soup = makeSoup(config.mps_list_url)
    mps = getMPHTTPList(soup)
    return mps

if __name__ == "__main__":
    url = config.mps_list_url
    print("Using url: {}".format(url))
    print("Parsing websit data...")
    #mps_list = getMPHTTPList(soup)
    print("Data parsed! Found {} records, showing top..".format(len(mps_list)))
    print(mps_list[0])