import logging

logger = logging.getLogger('MonitorLog').getChild("messenger")


class Messenger:

    def send_message(self, message):
        logger.info(message)

    def send_error(self, error_message):
        logger.error(error_message)