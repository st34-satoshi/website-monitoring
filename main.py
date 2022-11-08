from monitor_website import monitor
from monitor_sites import MONITOR_SITES
from messenger.create_messenger import create_messenger
import argparse
import logging

logger = logging.getLogger('MonitorLog')


file_handler = logging.FileHandler(filename="./log/monitor.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s", "%Y-%m-%dT%H:%M:%S"))

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


parser = argparse.ArgumentParser(description='website monitoring')
parser.add_argument('--messenger', default='logger')
parser.add_argument('--send_all_success', default='False')
args = parser.parse_args()

def main():
    messenger = create_messenger(args.messenger)
    all_ok = True
    for info in MONITOR_SITES:
        result, message = monitor(info)
        if not result:
            messenger.send_error(message)
            all_ok = False
    if all_ok and args.send_all_success == 'True':
        messenger.send_message('all ok!')


if __name__ == '__main__':
    main()