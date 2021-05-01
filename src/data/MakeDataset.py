import os
import sys
from datetime import date
import json

module_path = os.path.abspath(os.path.join("."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.data.TwitterApiAuth import TwitterApiAuth
from src.data.TweetsLookup import TweetsLookup
from src.data.UserLookup import UserLookup
from src.data.UserTweets import UserTweets
from pyenviron import export_environment_variables

export_environment_variables()
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

usernames = [
    "jairbolsonaro",
    "cirogomes",
    "lulaoficial",
    "jdoriajr",
    "lucianohuck",
    "marinasilva",
    "GuilhermeBoulos",
]

twitterApiAuth = TwitterApiAuth()
userLookup = UserLookup(usernames, ["username", "id"])
url = userLookup.create_url()
response = userLookup.connect_to_endpoint(url, twitterApiAuth)
user_userId = {user["username"]: user["id"] for user in response["data"]}
user_tweet_data = {
    userInfo["username"]: {"id": userInfo["id"], "name": userInfo["name"], "data": []}
    for userInfo in response["data"]
}

start_time = date(2021, 3, 1).strftime(DATE_FORMAT)
end_time = date(2021, 4, 1).strftime(DATE_FORMAT)

# full list of parameters at
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
params = {
    "tweet.fields": "text,author_id,created_at,public_metrics",
    "start_time": start_time,
    "end_time": end_time,
    "max_results": 100,
}

for username, userId in user_userId.items():
    userTweets = UserTweets(userId)
    url = userTweets.create_url()

    next_token = ""

    while True:
        response = userTweets.connect_to_endpoint(url, params, twitterApiAuth)
        user_tweet_data[username]["data"] = [
            *user_tweet_data[username]["data"],
            *response["data"],
        ]

        if "next_token" in response["meta"].keys():
            params.update({"pagination_token": response["meta"]["next_token"]})
        else:
            break

with open("data/presidenciaveis.json", "w") as f:
    json.dump(user_tweet_data, f)