import os
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

import requests

import main
from messenger.create_messenger import create_messenger
from messenger.discord import DiscordMessenger
from messenger.messenger import Messenger, NotificationError


class DiscordTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/id/secret"})
        env.start()
        self.addCleanup(env.stop)

    @patch("messenger.discord.requests.post")
    def test_message_and_error_payloads(self, post):
        post.return_value.status_code = 200
        messenger = create_messenger("discord")
        messenger.send_message("all ok!")
        messenger.send_error("site failed @everyone")
        self.assertEqual(post.call_count, 2)
        self.assertEqual(post.call_args.kwargs["json"], {
            "content": "site failed @everyone", "allowed_mentions": {"parse": []},
        })
        self.assertEqual(post.call_args.kwargs["params"], {"wait": "true"})
        self.assertEqual(post.call_args.kwargs["timeout"], 10)
        self.assertFalse(post.call_args.kwargs["allow_redirects"])

    @patch("messenger.discord.requests.post")
    def test_long_message_is_preserved(self, post):
        post.return_value.status_code = 200
        message = "あ" * 2000 + "end"
        DiscordMessenger().send_message(message)
        chunks = [call.kwargs["json"]["content"] for call in post.call_args_list]
        self.assertEqual([len(chunk) for chunk in chunks], [2000, 3])
        self.assertEqual("".join(chunks), message)

    @patch("messenger.discord.requests.post")
    def test_http_errors(self, post):
        for status in [302, 400, 401, 404, 429, 500]:
            with self.subTest(status=status):
                post.return_value.status_code = status
                with self.assertRaisesRegex(NotificationError, f"HTTP {status}"):
                    DiscordMessenger().send_error("site failed")

    @patch("messenger.discord.requests.post")
    def test_network_errors_do_not_expose_webhook(self, post):
        for error in [requests.Timeout, requests.ConnectionError]:
            post.side_effect = error(os.environ["DISCORD_WEBHOOK_URL"])
            with self.assertRaises(NotificationError) as caught:
                DiscordMessenger().send_message("test")
            self.assertNotIn("secret", str(caught.exception))

    def test_missing_configuration(self):
        with patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": " "}):
            with self.assertRaisesRegex(ValueError, "DISCORD_WEBHOOK_URL"):
                create_messenger("discord")

    def test_modes_do_not_import_slack_credentials(self):
        # Use a fresh interpreter so an already-cached module cannot hide imports.
        result = subprocess.run([sys.executable, "-c", """
import sys
sys.modules['messenger.secret'] = None
from messenger.create_messenger import create_messenger
create_messenger('logger')
create_messenger('discord')
assert 'messenger.slack' not in sys.modules
"""], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_slack_selection_remains_available(self):
        with patch.dict(sys.modules, {"messenger.slack": Mock()}):
            create_messenger("slack")
            sys.modules["messenger.slack"].SlackMessenger.assert_called_once_with()
        self.assertIsInstance(create_messenger("logger"), Messenger)


class MonitoringTests(unittest.TestCase):
    @patch.object(main, "MONITOR_SITES", ["first", "second"])
    @patch.object(main, "monitor", return_value=(False, "site failed"))
    @patch.object(main, "create_messenger")
    def test_failed_delivery_does_not_stop_monitoring(self, factory, monitor):
        factory.return_value.send_error.side_effect = NotificationError("delivery failed")
        self.assertEqual(main.main(["--messenger", "discord"]), 1)
        self.assertEqual(monitor.call_count, 2)
        self.assertEqual(factory.return_value.send_error.call_count, 2)

    @patch.object(main, "MONITOR_SITES", ["site"])
    @patch.object(main, "monitor", return_value=(True, None))
    @patch.object(main, "create_messenger")
    def test_success_notification_is_opt_in(self, factory, monitor):
        self.assertEqual(main.main(["--messenger", "discord"]), 0)
        factory.return_value.send_message.assert_not_called()
        self.assertEqual(main.main(["--messenger", "discord", "--send_all_success", "True"]), 0)
        factory.return_value.send_message.assert_called_once_with("all ok!")
        factory.return_value.send_message.side_effect = NotificationError("delivery failed")
        self.assertEqual(main.main(["--messenger", "discord", "--send_all_success", "True"]), 1)

    @patch.object(main, "monitor")
    def test_invalid_configuration_stops_before_monitoring(self, monitor):
        with patch.dict(os.environ, {"DISCORD_WEBHOOK_URL": ""}), patch("sys.stderr"):
            for args in [["--messenger", "discord"], ["--messenger", "discrd"]]:
                with self.assertRaises(SystemExit) as caught:
                    main.main(args)
                self.assertEqual(caught.exception.code, 2)
        monitor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
