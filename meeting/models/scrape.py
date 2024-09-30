import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


def scrape(URL: str, username: str, password: str) -> BeautifulSoup:
    session = requests.session()
    login_info = {
        "name": username,
        "password": password,
        "login": "ログイン",
    }
    res = session.post(URL, data=login_info)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup


if __name__ == "__main__":
    WHITEBOARD_URL = "https://wiki.mma.club.uec.ac.jp/WhiteBoard"
    soup = scrape(WHITEBOARD_URL, "username", "password")
    print(soup)
