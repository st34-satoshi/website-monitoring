import requests
import logging

logger = logging.getLogger('MonitorLog').getChild("sub")


def monitor(access_info):
    url = access_info['url']
    logger.info(f'start url = {url}')
    response = requests.get(url)
    logger.info(f'finish url = {url}')
    t = response.text
    expect_body_include = access_info["expect_body_includes"]
    if expect_body_include not in t:
        return False
    return True