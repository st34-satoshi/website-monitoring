from monitor_website import monitor
from monitor_sites import MONITOR_SITES
# from log_manager import get_logger
import logging

logger = logging.getLogger('MonitorLog')


file_handler = logging.FileHandler(filename="./log/monitor.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s", "%Y-%m-%dT%H:%M:%S"))

logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def main():
    for info in MONITOR_SITES:
        result = monitor(info)
        if not result:
            print('error')


if __name__ == '__main__':
    main()