import time
import tweepy
import os
from dotenv import load_dotenv

# Load API credentials
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate with Twitter API
try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    print("✅ Successfully authenticated with Twitter API")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)


# Exponential backoff for retrying failed API calls
def retry_with_backoff(func, max_retries=5):
    wait_time = 5  # Start with 5 seconds
    for attempt in range(max_retries):
        try:
            return func()
        except tweepy.TweepyException as e:
            if "429" in str(e):  # Rate limit hit
                print(f"⏳ Rate limit hit! Waiting {wait_time}s before retrying...")
                time.sleep(wait_time)
                wait_time *= 2  # Double wait time for next retry
            else:
                print(f"❌ API Error: {e}")
                break
    print("🚨 Max retries reached. Skipping this API call.")
    return None


# ✅ Fetch Twitter Bot Username
def get_bot_username():
    def fetch_user():
        global bot_user
        bot_user = client.get_me()
        print(f"\n✅ Bot Name: {bot_user.data.name}")
        print(f"📌 Bot Username (Handle): @{bot_user.data.username}")
        print(f"🔗 Profile URL: https://twitter.com/{bot_user.data.username}")

    retry_with_backoff(fetch_user)


# Run the function to get bot username
get_bot_username()


# ✅ Fetch Twitter Profile with Rate Limit Handling
def get_twitter_profile():
    def fetch_profile():
        user = client.get_user(username=bot_user.data.username)
        print(f"\n✅ Twitter Profile Info:")
        print(f"👤 Name: {user.data.name}")
        print(f"📌 Username (Handle): @{user.data.username}")
        print(f"🔗 Profile URL: https://twitter.com/{user.data.username}")

    retry_with_backoff(fetch_profile)


# ✅ Fetch Latest Tweets with Rate Limit Handling
def get_latest_tweets(count=5):
    def fetch_tweets():
        user = client.get_user(
            username=bot_user.data.username
        )  # Use fetched bot username
        user_id = user.data.id
        tweets = client.get_users_tweets(
            id=user_id, max_results=count, tweet_fields=["created_at"]
        )

        if not tweets.data:
            print("\n📢 No recent tweets found.")
            return

        print("\n📢 Your Latest Tweets:")
        for idx, tweet in enumerate(tweets.data, 1):
            timestamp = tweet.created_at if tweet.created_at else "Unknown Time"
            print(f"{idx}. {tweet.text} (Tweeted at: {timestamp})")

    retry_with_backoff(fetch_tweets)


# ✅ Run API Calls with Delays
get_twitter_profile()
time.sleep(15)  # Add delay before next request
get_latest_tweets()

# without rate limit logic:
# from dotenv import load_dotenv
# import tweepy
# import os
# import schedule
# import time
# import requests

# # Load API creds
# load_dotenv()

# # Fetch API credentials
# API_KEY = os.getenv("API_KEY")
# API_SECRET = os.getenv("API_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
# BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Needed for API v2

# if (
#     not API_KEY
#     or not API_SECRET
#     or not ACCESS_TOKEN
#     or not ACCESS_TOKEN_SECRET
#     or not BEARER_TOKEN
# ):
#     print("❌ Error: API credentials are missing!")
#     exit(1)


# # Authenticate with Twitter/X API v2
# client = tweepy.Client(
#     bearer_token=BEARER_TOKEN,
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_TOKEN_SECRET,
# )


# # ✅ Fetch Twitter Profile using API v2
# def get_twitter_profile():
#     try:
#         user = client.get_user(
#             username="your_username"
#         )  # Replace with your actual Twitter handle
#         if user and user.data:
#             print(f"\n✅ Twitter Profile Info:")
#             print(f"👤 Name: {user.data.name}")
#             print(f"📌 Username (Handle): @{user.data.username}")
#             print(f"🔗 Profile URL: https://twitter.com/{user.data.username}")
#         else:
#             print("❌ Error: Unable to fetch user profile.")
#     except tweepy.TweepyException as e:
#         print("❌ Error fetching profile:", e)


# # Fetch and display Twitter profile
# get_twitter_profile()


# # ✅ Fetch Latest Tweets using API v2
# def get_latest_tweets(count=2):
#     try:
#         user = client.get_user(username="your_username")  # Get user ID
#         user_id = user.data.id
#         tweets = client.get_users_tweets(id=user_id, max_results=count)

#         if not tweets.data:
#             print("\n📢 No recent tweets found.")
#             return

#         print("\n📢 Your Latest Tweets:")
#         for idx, tweet in enumerate(tweets.data, 1):
#             print(f"{idx}. {tweet.text} (Tweeted at: {tweet.created_at})")
#     except tweepy.TweepyException as e:
#         print("❌ Error fetching tweets:", e)


# # Fetch and display latest tweets
# get_latest_tweets()


# # ✅ Post a tweet using API v2
# def post_tweet(text):
#     try:
#         client.create_tweet(text=text)
#         print("✅ Success - Tweet posted!")
#     except tweepy.TweepyException as err:
#         print("❌ Error posting a tweet:", err)


# # ✅ Post an image with text using API v1.1 (Limited access)
# def post_img_tweet(img_path, text):
#     try:
#         auth = tweepy.OAuth1UserHandler(
#             API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
#         )
#         api_v1 = tweepy.API(auth)
#         api_v1.update_status_with_media(status=text, filename=img_path)
#         print("✅ Success - Image tweet posted!")
#     except tweepy.TweepyException as err:
#         print("❌ Error posting an image tweet:", err)


# # ✅ Fetch Tamil Nadu Coin (TNAD) Price & Tweet
# def fetch_tnad_price():
#     url = "https://api.coingecko.com/api/v3/simple/price?ids=tamilnadu-coin&vs_currencies=usd"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         price = data["tamilnadu-coin"]["usd"]
#         post_tweet(f"🚀 TNAD is currently trading at ${price}! #TNAD #Crypto")
#     except Exception as e:
#         print("❌ Error fetching TNAD price:", e)


# # Schedule tweets
# def scheduled_tweets():
#     post_tweet(
#         "🌍 TamilNadu Coin (TNAD) is shaping the future of decentralized finance. #TNAD #Crypto"
#     )


# schedule.every(6).hours.do(scheduled_tweets)  # Tweet every 6 hours
# schedule.every().hour.do(fetch_tnad_price)  # Fetch and tweet TNAD price every hour

# # Keep the script running
# if __name__ == "__main__":
#     while True:
#         schedule.run_pending()
#         time.sleep(60)  # Wait a minute before checking again
