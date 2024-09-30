import os
from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["LDAP_HOST"] = os.getenv("LDAP_HOST")
app.config["LDAP_BASE_DN"] = os.getenv("LDAP_BASE_DN")
app.config["LDAP_USER_DN"] = os.getenv("LDAP_USER_DN")
app.config["LDAP_BIND_USER_DN"] = os.getenv("LDAP_BIND_USER_DN")
app.config["LDAP_BIND_USER_PASSWORD"] = os.getenv("LDAP_BIND_USER_PASSWORD")

csrf = CSRFProtect(app)
ldap_manager = LDAP3LoginManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import meeting.views
