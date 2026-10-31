import logging
import os

import requests

from messenger.messenger import Messenger, NotificationError

logger = logging.getLogger('MonitorLog').getChild("discordMessenger")


class DiscordMessenger(Messenger):
    def __init__(self):
        self._webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
        if not self._webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL is required for Discord notifications")

    def send_message(self, message):
        super().send_message(message)
        self._send(message)

    def send_error(self, error_message):
        super().send_error(error_message)
        self._send(error_message)

    def _send(self, message):
        for start in range(0, len(message), 2000):
            try:
                response = requests.post(
                    self._webhook_url,
                    params={"wait": "true"},
                    json={
                        "content": message[start:start + 2000],
                        "allowed_mentions": {"parse": []},
                    },
                    timeout=10,
                    allow_redirects=False,
                )
            except requests.RequestException:
                # Request exception messages may contain the secret webhook URL.
                raise NotificationError("Discord notification failed: network error") from None
            if not 200 <= response.status_code < 300:
                raise NotificationError(
                    f"Discord notification failed: HTTP {response.status_code}"
                )
            logger.info("Discord notification sent")
