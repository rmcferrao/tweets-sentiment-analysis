import os

class TwitterApiAuth:

    def __init__(self):
        BEARER_TOKEN = TwitterApiAuth.auth()
        self.headers = TwitterApiAuth.create_headers(BEARER_TOKEN)
        
    def auth():
        if not os.environ.get("BEARER_TOKEN"):
            raise Exception(
                "BEARER_TOKEN token is not available as an Enviornment variable, \
                try to export it running `pyenviron.py` file available in root folder"
            )
        return os.environ.get("BEARER_TOKEN")

    def create_headers(bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def get_headers(self):
        return self.headers