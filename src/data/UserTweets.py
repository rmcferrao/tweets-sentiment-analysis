import requests
from .TwitterApiAuth import TwitterApiAuth


class UserTweets:
    AVAILABLE_FIELDS = [
        "attachments",
        "author_id",
        "context_annotations",
        "conversation_id",
        "created_at",
        "entities",
        "geo",
        "id",
        "in_reply_to_user_id",
        "lang",
        "non_public_metrics",
        "organic_metrics",
        "possibly_sensitive",
        "promoted_metrics",
        "public_metrics",
        "referenced_tweets",
        "source",
        "text",
        "withheld",
    ]

    def __init__(
        self,
        ids: int,
        tweet_fields: list = [
            "text",
            "author_id",
            "created_at",
            "public_metrics",
        ],
    ):
        """
        Tweet fields are adjustable.
        Options include:
        attachments, author_id, context_annotations,
        conversation_id, created_at, entities, geo, id,
        in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        source, text, and withheld
        """

        for tweet_field in tweet_fields:
            if tweet_field not in UserTweets.AVAILABLE_FIELDS:
                raise Exception(
                    f"{tweet_field} is not an available tweet field. \
                    The available user fields are {','.join(UserTweets.AVAILABLE_FIELDS)}"
                )

        self.ids = ids
        self.tweet_fields = tweet_fields

    def create_url(self) -> str:
        return "https://api.twitter.com/2/users/{}/tweets".format(self.ids)

    def get_params(self) -> dict:
        return {"tweet.fields": ",".join(self.tweet_fields)}

    def connect_to_endpoint(
        self, url: str, params: dict, twitterApiAuth: TwitterApiAuth
    ):
        headers = twitterApiAuth.get_headers()
        response = requests.request("GET", url, headers=headers, params=params)
        print(response.url)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


# if __name__ == "__main__":
#     # neymar id 158487331
#     twitterApiAuth = TwitterApiAuth()
#     tweetLookup = UserTweets(ids=["158487331"])
#     url = tweetLookup.create_url()
#     params = tweetLookup.get_params()

#     response = tweetLookup.connect_to_endpoint(url, params, twitterApiAuth)
#     print(response)