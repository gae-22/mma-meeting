import datetime, random, string
from meeting.models.spread import write_password

password_past = ""


def reload_time() -> bool:
    mtg_from_time = datetime.time(17, 00, 00)
    mtg_to_time = datetime.time(17, 20, 00)
    mtg_wkdy = 0

    now_time = datetime.datetime.now().time()
    now_wkdy = datetime.datetime.now().weekday()

    return (
        True
        if mtg_from_time < now_time < mtg_to_time and now_wkdy == mtg_wkdy
        else False
    )


def choose_random() -> str:
    global password_past
    pass_path = "./datas/password.txt"

    with open(pass_path, "r") as f:
        lines = f.read().splitlines()

    while True:
        password = random.choice(lines)
        if password != password_past:
            break
    lines.remove(password)
    write_password(password)
    return password


def randomname(n):
    global password_past
    password = ""

    password = choose_random()

    if password == 1:
        randlst = [
            random.choice(string.ascii_lowercase + string.digits) for i in range(n)
        ]
        password_past = password = "".join(randlst)
    return password
