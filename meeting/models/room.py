from meeting.models.scrape import scrape


def rooms() -> list[list[str]]:
    WHITEBOARD_URL = "https://wiki.mma.club.uec.ac.jp/WhiteBoard"
    soup = scrape(WHITEBOARD_URL)
    tbody = soup.find("tbody")
    mat = []
    trs = tbody.find_all("tr")
    for tr in trs:
        r = []
        for td in tr.find_all("td"):
            r.append(td.text)
        mat.append(r)

    return mat
