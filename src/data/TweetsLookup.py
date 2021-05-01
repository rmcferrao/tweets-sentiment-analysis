import requests

from .TwitterApiAuth import TwitterApiAuth

class TweetsLookup:
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
        ids: list,
        tweet_fields: list = [
            "author_id",
            "id",
            "created_at",
            "text",
            "source",
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
        You can adjust ids to include a single Tweets.
        Or you can add to up to 100 comma-separated IDs
        """

        for tweet_field in tweet_fields:
            if tweet_field not in TweetsLookup.AVAILABLE_FIELDS:
                raise Exception(
                    f"{tweet_field} is not an available tweet field. \
                    The available user fields are {','.join(TweetsLookup.AVAILABLE_FIELDS)}"
                )

        self.tweet_fields = tweet_fields
        self.ids = ids
        self._query_strings()

    def _query_strings(self):
        self.tweet_fields_query = "tweet.fields=" + ",".join(self.tweet_fields)
        self.ids_query = "ids=" + ",".join(self.ids)

    def create_url(self) -> str:
        url = "https://api.twitter.com/2/tweets?{}&{}".format(
            self.ids_query, self.tweet_fields_query
        )
        return url

    def connect_to_endpoint(self, url: str, twitterApiAuth: TwitterApiAuth):

        headers = twitterApiAuth.get_headers()
        response = requests.request("GET", url, headers=headers)
        print(response.url)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


if __name__ == "__main__":
    # neymar id 158487331
    twitterApiAuth = TwitterApiAuth()
    tweetLookup = TweetsLookup(ids=["1278747501642657792,1255542774432063488"])
    url = tweetLookup.create_url()
    response = tweetLookup.connect_to_endpoint(url, twitterApiAuth)
    print(response)
