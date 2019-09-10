import keyring
import twython

def startTwython():
    twi = twython.Twython(
        keyring.get_password("twitter", "api_key"),
        keyring.get_password("twitter", "api_secret_key"),
        keyring.get_password("twitter", "access_token"),
        keyring.get_password("twitter", "access_token_secret")
    )
    return twi

if __name__ == "__main__":
    twi = startTwython()
    twitterUser = twi.lookup_user(screen_name="potus44")
    userTweets = twi.get_user_timeline(screen_name="potus44", count=10)
    print("User "+ twitterUser[0]["name"] + " has " + str(twitterUser[0]["friends_count"]) + " friends and " + str(twitterUser[0]["followers_count"]) + " followers.")