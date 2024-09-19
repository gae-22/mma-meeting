import re

from meeting.models.thread import update


def get_agendas() -> list[str]:
    BBS_ARRAY = update()
    length = len(BBS_ARRAY)
    agendas = []
    for i in range(0, length):
        element = BBS_ARRAY[length - i - 1][0]
        if re.match("\s*--", element):
            agendas = BBS_ARRAY[length - i - 2 : length]
            break

    return agendas
