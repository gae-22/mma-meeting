import re
from typing import List


def get_agendas(BBS_ARRAY: List[List[str]]) -> List[str]:
    length = len(BBS_ARRAY)
    agendas = []
    for i in range(0, length):
        element = BBS_ARRAY[length - i - 1][0]
        if re.match(r"\s*--", element):
            agendas = BBS_ARRAY[length - i - 2 : length]
            break
    return agendas
