import tweepy
import os

from dotenv import load_dotenv

# Load API creds
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with twitter/X API
def authenticate_twitter():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

api = authenticate_twitter()

# verify auth
try:
    api.verify_credentials()
    print("Auth success!")
except Exception as err:
    print("Error: ", err)

# func to post a text tweet
def post_tweet(text):
    try:
        api.update_status(text)
        print("Success - Tweet posted!")
    except Exception as err:
        print("Error - Posting a tweet: ", err)

# func to post an img tezxt
def post_img_tweet(img_path, text):
    try:
        api.update_status_with_media(status=text, filename=img_path)
        print("Success - Image tweet posted!")
    except Exception as err:
        print("Error - Posting an image tweet: ", err)

def fetch_tnad_price():
    