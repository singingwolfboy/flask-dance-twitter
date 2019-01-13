import os
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["TWITTER_OAUTH_API_KEY"] = os.environ.get("TWITTER_OAUTH_API_KEY")
app.config["TWITTER_OAUTH_API_SECRET"] = os.environ.get("TWITTER_OAUTH_API_SECRET")
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])

if __name__ == "__main__":
    app.run()
