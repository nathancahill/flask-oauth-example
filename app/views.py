from flask import redirect, url_for, request
from flask.ext.login import login_user, logout_user, login_required, current_user

from app import app, db, twitter, login_manager
from models import Account

@twitter.tokengetter
def get_twitter_token():
    if current_user.is_authenticated():
        return (current_user.token, current_user.secret)
    else:
        return None


@login_manager.user_loader
def load_user(userid):
    return Account.query.filter_by(id=userid).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('index'))


@app.route('/login')
def login():
    if current_user.is_authenticated():
        return redirect(url_for('settings'))
    return twitter.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or url_for('settings')))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('settings')
    if resp is None:
        return redirect(next_url)

    account = Account.query.filter_by(username = resp['screen_name']).first()
    if account is None:
        account = Account(resp['screen_name'], resp['oauth_token'], resp['oauth_token_secret'])

        db.session.add(account)
        db.session.commit()

    login_user(account)

    return redirect(next_url)


@app.route('/')
def index():
    return 'Flask-OAuth Login Example'


@app.route('/settings')
@login_required
def settings():
    return 'Logged in!'
