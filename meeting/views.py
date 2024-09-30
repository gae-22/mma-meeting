import os
import json
from functools import wraps
from datetime import timedelta

from flask import (
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    jsonify,
)
from flask_wtf import FlaskForm
from ldap3 import Server, Connection, ALL, SUBTREE
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from meeting import app
from meeting.models.thread import update
from meeting.models.agenda import get_agendas
from meeting.models.room import rooms
from meeting.models.password import make_passwd
from meeting.models.spread import write_agenda
from meeting.models.result import get_form_responses


class LDAPLoginForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired()])


# Set session lifetime to 1 hour
app.permanent_session_lifetime = timedelta(hours=1)

# LDAP configuration
ldap_host = os.getenv("LDAP_HOST")
ldap_user_dn = os.getenv("LDAP_USER_DN")
ldap_password = os.getenv("LDAP_BIND_USER_PASSWORD")
search_base = os.getenv("LDAP_SEARCH_BASE")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LDAPLoginForm()

    if session.get("logged_in"):
        return redirect(url_for("agenda"))

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        search_filter = f"(uid={username})"

        server = Server(ldap_host, get_info=ALL, use_ssl=False)
        conn = Connection(server, user=ldap_user_dn, password=ldap_password)

        if conn.bind():
            conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=SUBTREE,
            )
            if conn.entries:
                user_dn = f"uid={username}," + search_base
                user_conn = Connection(server, user=user_dn, password=password)
                if user_conn.bind():
                    session["logged_in"] = True
                    session["username"] = username
                    session["password"] = password
                    return redirect(url_for("agenda"))
                else:
                    flash("ユーザー認証に失敗しました。", "error")
            else:
                flash("ディレクトリにユーザーが見つかりません。", "error")
            conn.unbind()
        else:
            flash("LDAPサーバーへの接続に失敗しました。", "error")

    return render_template("meeting/login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/thread")
@login_required
def thread():
    BBS_ARRAY = update(session.get("username"), session.get("password"))
    agendas = BBS_ARRAY
    return render_template(
        "meeting/thread.html", BBS_ARRAY=BBS_ARRAY, agendas=agendas, length=len(agendas)
    )


@app.route("/agenda")
@login_required
def agenda():
    BBS_ARRAY = update(session.get("username"), session.get("password"))
    agendas = get_agendas(BBS_ARRAY)
    return render_template(
        "meeting/agenda.html", BBS_ARRAY=BBS_ARRAY, agendas=agendas, length=len(agendas)
    )


@app.route("/room")
@login_required
def room():
    ROOMS = rooms(session.get("username"), session.get("password"))
    return render_template("meeting/room.html", ROOMS=ROOMS, length=len(ROOMS))


@app.route("/result")
@login_required
def form_responses():
    values = get_form_responses()
    return render_template("meeting/result.html", responses=values)


@app.route("/admin")
@login_required
def admin():
    with open("datas/admin.json", "r", encoding="utf-8") as file:
        admins = json.load(file)
    if session.get("username") not in admins:
        abort(403)
    session["is_admin"] = True

    BBS_ARRAY = update(session.get("username"), session.get("password"))
    agendas = get_agendas(BBS_ARRAY)
    password = make_passwd()
    write_agenda(agendas, password)
    return render_template(
        "meeting/admin.html", password=password, is_result_public=is_result_public
    )


@app.route("/admin-conf", methods=["GET", "POST"])
@login_required
def admin_conf():
    form = AdminForm()
    if form.validate_on_submit():
        new_admin = form.new_admin.data
        with open("datas/admin.json", "r", encoding="utf-8") as file:
            admins = json.load(file)
        admins.append(new_admin)
        with open("datas/admin.json", "w", encoding="utf-8") as file:
            json.dump(admins, file, ensure_ascii=False, indent=4)
        flash(f"{new_admin}を管理者に追加しました。")
        return redirect(url_for("admin_conf"))

    with open("datas/admin.json", "r", encoding="utf-8") as file:
        admins = json.load(file)

    return render_template("meeting/admin_conf.html", admins=admins, form=form)


@app.route("/add-admin", methods=["POST"])
@login_required
def add_admin():
    new_admin = request.form.get("new_admin")
    if new_admin:
        with open("datas/admin.json", "r", encoding="utf-8") as file:
            admins = json.load(file)
        admins.append(new_admin)
        with open("datas/admin.json", "w", encoding="utf-8") as file:
            json.dump(admins, file, ensure_ascii=False, indent=4)
        flash(f"{new_admin}を管理者に追加しました。")
    return redirect(url_for("admin_conf"))


@app.route("/remove-admin/<admin>")
@login_required
def remove_admin(admin):
    with open("datas/admin.json", "r", encoding="utf-8") as file:
        admins = json.load(file)
    if admin in admins:
        admins.remove(admin)
        with open("datas/admin.json", "w", encoding="utf-8") as file:
            json.dump(admins, file, ensure_ascii=False, indent=4)
        flash("管理者を削除しました。")
    return redirect(url_for("admin_conf"))


is_result_public = False


@app.route("/toggle-result-visibility", methods=["POST"])
@login_required
def toggle_result_visibility():
    global is_result_public
    is_result_public = not is_result_public
    return jsonify({"is_result_public": is_result_public})


@app.route("/result")
@login_required
def result():
    if not is_result_public and not session.get("is_admin"):
        abort(403)
    responses = get_form_responses()
    return render_template("meeting/result.html", responses=responses)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("meeting/404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("meeting/403.html"), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("meeting/500.html"), 500


class AdminForm(FlaskForm):
    new_admin = StringField("新しい管理者", validators=[DataRequired()])
