from monitor_website import monitor
from monitor_sites import MONITOR_SITES
from messenger.create_messenger import create_messenger
import logging

logger = logging.getLogger('MonitorLog')


file_handler = logging.FileHandler(filename="./log/monitor.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s", "%Y-%m-%dT%H:%M:%S"))

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def main():
    messenger = create_messenger("")
    for info in MONITOR_SITES:
        result, message = monitor(info)
        if not result:
            messenger.send_error(message)


if __name__ == '__main__':
    main()