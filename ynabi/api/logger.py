from pushover import Client

from .credentials import pushover_user_key, pushover_api_token

client = Client(pushover_user_key, api_token=pushover_api_token)


def log(title, msg, pushover=False):
    s = f"{title}: {msg}"
    print(s)
    if pushover:
        client.send_message(s, title="ynabi")
