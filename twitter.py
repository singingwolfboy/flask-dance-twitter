import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["TWITTER_OAUTH_CLIENT_ID"] = os.environ.get("TWITTER_OAUTH_CLIENT_ID")
app.config["TWITTER_OAUTH_CLIENT_SECRET"] = os.environ.get("TWITTER_OAUTH_CLIENT_SECRET")
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])
