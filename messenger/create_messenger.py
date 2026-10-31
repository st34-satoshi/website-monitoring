from messenger.messenger import Messenger


def create_messenger(name):
    if name == "slack":
        from messenger.slack import SlackMessenger
        return SlackMessenger()
    if name == "discord":
        from messenger.discord import DiscordMessenger
        return DiscordMessenger()
    if name == "logger":
        return Messenger()
    raise ValueError("Unknown messenger")
