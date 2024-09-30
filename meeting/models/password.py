import random

password_past = ""


def make_passwd() -> str:
    global password_past
    password = ""

    password = str(random.randint(1000, 9999))

    return password
