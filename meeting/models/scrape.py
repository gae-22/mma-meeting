import requests
import configparser
from bs4 import BeautifulSoup


def scrape(URL):
    config_file = "./datas/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    name = config.get("User", "name")
    password = config.get("User", "password")

    login_info = {
        "name": name,
        "password": password,
        "login": "ログイン",
        "login": "ログイン",
    }

    session = requests.session()
    res = session.post(URL, data=login_info)
    soup = BeautifulSoup(res.content, "html.parser")

    return soup
