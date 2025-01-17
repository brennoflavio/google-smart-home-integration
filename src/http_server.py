from flask import Flask, request, redirect, url_for, session
import os
from google_helpers import (
    get_credentials,
    get_authorization_url,
    handle_callback,
)
from variables import load_and_assert
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from privacy_policy import privacy_policy


app = Flask(__name__)
app.secret_key = load_and_assert("SECRET_ID")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "True"

auth = HTTPBasicAuth()

users = {
    load_and_assert("APP_USER"): generate_password_hash(load_and_assert("APP_PASSWORD"))
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


def build_secure_url(route, _external=False):
    url = url_for(route, _external=_external)
    url = url.replace("http", "https", 1)
    return url


@app.route("/")
@auth.login_required
def index():
    if not get_credentials():
        return redirect(build_secure_url("authorize"))
    return "You're authorized, no action needed"


@app.route("/authorize")
def authorize():
    authorization_url, state = get_authorization_url(
        build_secure_url("oauth2callback", _external=True)
    )
    session["state"] = state
    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]
    handle_callback(
        state, build_secure_url("oauth2callback", _external=True), request.url
    )
    return redirect("/")


@app.route("/privacy")
def privacy():
    return privacy_policy


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
