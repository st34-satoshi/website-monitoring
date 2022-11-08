from messenger.messenger import Messenger
from messenger.secret import SLACK_TOKEN
import requests
import logging

logger = logging.getLogger('MonitorLog').getChild("slackMessenger")

class SlackMessenger(Messenger):

    def __init__(self) -> None:
        super().__init__()
        self._headers = {'Content-Type': 'application/json'}
        self._channel = "#random"

    def send_message(self, message):
        self.to_slack(message)

    def send_error(self, error_message):
        self.to_slack(error_message)

    def to_slack(self, message):
        params = {"token": SLACK_TOKEN, "channel": self._channel, "text": message}
        r = requests.post('https://slack.com/api/chat.postMessage',
                          headers=self._headers,
                          params=params)
        logger.info(f"slack response = {r.status_code}")
