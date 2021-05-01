import requests

from .TwitterApiAuth import TwitterApiAuth

class UserLookup:
    AVAILABLE_FIELDS = [
        "created_at",
        "description",
        "entities",
        "id",
        "location",
        "name",
        "pinned_tweet_id",
        "profile_image_url",
        "protected",
        "public_metrics",
        "url",
        "username",
        "verified",
        "withheld",
    ]

    def __init__(
        self,
        usernames: list,
        user_fields: list = ["id", "name", "username", "profile_image_url"],
    ):
        """
        Specify the usernames that you want to lookup below
        You can enter up to 100 comma-separated values.

        User fields are adjustable, options include:
        created_at, description, entities, id, location, name,
        pinned_tweet_id, profile_image_url, protected,
        public_metrics, url, username, verified, and withheld
        """

        for user_field in user_fields:
            if user_field not in UserLookup.AVAILABLE_FIELDS:
                raise Exception(
                    f"{user_field} is not an available user field. \
                    The available user fields are {','.join(UserLookup.AVAILABLE_FIELDS)}"
                )

        self.usernames = usernames
        self.user_fields = user_fields
        self._query_strings()

    def _query_strings(self):
        self.usernames_query = "usernames=" + ",".join(self.usernames)
        self.user_fields_query = "user.fields=" + ",".join(self.user_fields)

    def create_url(self) -> str:
        url = "https://api.twitter.com/2/users/by?{}&{}".format(
            self.usernames_query, self.user_fields_query
        )
        return url

    def connect_to_endpoint(self, url: str, twitterApiAuth: TwitterApiAuth):

        headers = twitterApiAuth.get_headers()
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


# if __name__ == "__main__":
#     twitterApiAuth = TwitterApiAuth()
#     userLookup = UserLookup(usernames=["neymarjr"])
#     url = userLookup.create_url()
#     response = userLookup.connect_to_endpoint(url, twitterApiAuth)
#     print(response)