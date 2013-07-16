from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.oauth import OAuth
from flask.ext.login import LoginManager

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, \
    TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url = 'http://api.twitter.com/1/',
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url = 'https://api.twitter.com/oauth/access_token',
    authorize_url = 'https://api.twitter.com/oauth/authenticate',
    consumer_key = TWITTER_CONSUMER_KEY,
    consumer_secret = TWITTER_CONSUMER_SECRET
)

login_manager = LoginManager()
login_manager.init_app(app)

from app import views
