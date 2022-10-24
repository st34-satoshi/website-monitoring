from monitor_website import monitor
from monitor_sites import MONITOR_SITES


def main():
    for info in MONITOR_SITES:
        result = monitor(info)
        if not result:
            print('error')


if __name__ == '__main__':
    main()