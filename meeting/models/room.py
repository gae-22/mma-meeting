from typing import List

from meeting.models.scrape import scrape


def rooms(username: str, password: str) -> List[List[str]]:
    WHITEBOARD_URL = "https://wiki.mma.club.uec.ac.jp/WhiteBoard"
    soup = scrape(WHITEBOARD_URL, username, password)
    tbody = soup.find("tbody")
    mat = []
    trs = tbody.find_all("tr")
    for tr in trs:
        r = []
        for td in tr.find_all("td"):
            r.append(td.text)
        mat.append(r)

    return mat
