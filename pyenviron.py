import os
import json


def export_environment_variables():
    with open("keys.json", "r") as f:
        keys = json.load(f)

    os.environ.update(keys)


# if __name__ == "__main__":
#     export_environment_variables()
