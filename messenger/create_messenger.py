from messenger.messenger import Messenger
from messenger.slack import SlackMessenger


def create_messenger(name):
    if name == "slack":
        return SlackMessenger()
    return Messenger()