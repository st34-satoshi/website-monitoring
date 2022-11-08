import requests
import logging

logger = logging.getLogger('MonitorLog').getChild("sub")


"""
error: return False, error message
ok: return True, None
"""
def monitor(access_info):
    url = access_info['url']
    logger.info(f'start url = {url}')
    response = requests.get(url)
    logger.info(f'finish url = {url}')
    expect_status_code = access_info["expect_status_code"]
    if response.status_code != expect_status_code:
        return False, f"url = {url}. status code = {response.status_code}"
    t = response.text
    expect_body_include = access_info["expect_body_includes"]
    if expect_body_include not in t:
        return False, f"url = {url}. expect body = {expect_body_include}"
    return True, None