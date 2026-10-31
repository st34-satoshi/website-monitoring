from monitor_website import monitor
from monitor_sites import MONITOR_SITES
from messenger.create_messenger import create_messenger
from messenger.messenger import NotificationError
import argparse
import logging

logger = logging.getLogger('MonitorLog')


file_handler = logging.FileHandler(filename="./log/monitor.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s", "%Y-%m-%dT%H:%M:%S"))

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


parser = argparse.ArgumentParser(description='website monitoring')
parser.add_argument('--messenger', default='logger', choices=['logger', 'slack', 'discord'])
parser.add_argument('--send_all_success', default='False')

def main(argv=None):
    args = parser.parse_args(argv)
    try:
        messenger = create_messenger(args.messenger)
    except ValueError as error:
        parser.error(str(error))
    all_ok = True
    notification_failed = False
    for info in MONITOR_SITES:
        result, message = monitor(info)
        if not result:
            try:
                messenger.send_error(message)
            except NotificationError as error:
                logger.error("%s", error)
                notification_failed = True
            all_ok = False
    if all_ok and args.send_all_success == 'True':
        try:
            messenger.send_message('all ok!')
        except NotificationError as error:
            logger.error("%s", error)
            notification_failed = True
    return 1 if notification_failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
