import gspread

from meeting.models.agenda import get_agendas

key_name = "./datas/meeting.json"
sheet_id = "1SLP8YSEvr7KY5J5g4SNAC4xaaRrCfoFStgmxBl1xkao"


def write_password(password):
    sheet_name = "概要"
    gc = gspread.service_account(filename=key_name)
    wks = gc.open_by_key(sheet_id).worksheet(sheet_name)
    wks.update_cell(8, 2, password)


def write_agenda(password):
    sheet_name = "質問"
    gc = gspread.service_account(filename=key_name)
    wks = gc.open_by_key(sheet_id).worksheet(sheet_name)
    last_row = len(wks.col_values(1))
    agendas = get_agendas()
    k = 3
    cnt = 0
    plus_rows = []
    for agenda in agendas:
        cnt += 1
        if cnt % 2 == 0:
            agenda = agenda[0]
            while "+" in agenda:
                idx = agenda.find("+")
                agenda = agenda[idx + 1 :]
                idx = agenda.find("\n")
                one_agenda = agenda[:idx]
                if "告知" not in one_agenda:
                    plus_rows.append(one_agenda)
                    k += 1
    for i, agenda_text in enumerate(plus_rows, start=3):
        wks.update_cell(i, 1, agenda_text)
    for j in range(3 + len(plus_rows), last_row + 1):
        wks.update_cell(j, 1, "")

    write_password(password)
