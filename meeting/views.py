from flask import render_template
from meeting import app
from meeting.models.thread import update
from meeting.models.agenda import get_agendas
from meeting.models.room import rooms
from meeting.models.password import randomname
from meeting.models.spread import write_agenda


@app.route("/")
def index():
    return render_template("meeting/index.html")


@app.route("/thread")
def thread():
    BBS_ARRAY = update()
    return render_template(
        "meeting/thread.html", BBS_ARRAY=BBS_ARRAY, length=len(BBS_ARRAY)
    )


@app.route("/agenda")
def agenda():
    BBS_ARRAY = update()
    agendas = get_agendas()
    return render_template(
        "meeting/agenda.html", BBS_ARRAY=BBS_ARRAY, agendas=agendas, length=len(agendas)
    )


@app.route("/form")
def form():
    password = randomname(6)
    write_agenda(password)
    return render_template("meeting/form.html", password=password)


@app.route("/room")
def room():
    ROOMS = rooms()
    return render_template("meeting/room.html", ROOMS=ROOMS, length=len(ROOMS))
