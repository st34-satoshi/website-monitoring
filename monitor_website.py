import requests


def monitor(access_info):
    url = access_info['url']
    response = requests.get(url)
    t = response.text
    expect_body_include = access_info["expect_body_includes"]
    if expect_body_include not in t:
        return False
    return True