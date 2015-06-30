from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import json
import random
import datetime
from config import *

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

PEOPLE_TO_NOT_FUCK = ['1676625860', '1280057341']

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,read_stream,publish_actions'}
)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return redirect(url_for('home'))
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@app.route('/friends')
def get_friends():
    friends = facebook.get('/me/friends')
    return json.dumps(friends.data)


@app.route('/fuckem/<id_to_fuck>')
def fuck_em(id_to_fuck):

    if id_to_fuck in PEOPLE_TO_NOT_FUCK:
        return 'no'
    # TODO: Make Better
    base = datetime.date(2009, 1, 1)
    date_list = [base + datetime.timedelta(days=180*x) for x in range(0, 14)]
    date_list = [date.strftime('%s') for date in date_list]
    random.shuffle(date_list)
    posts = facebook.get('/%s/posts?until=%s' % (str(id_to_fuck), date_list[0]))
    date_list.pop(0)
    count = 0
    while len(posts.data['data']) == 0:
        posts = facebook.get('/%s/posts?until=%s' % (str(id_to_fuck), date_list[count]))
        print posts.data
        count += 1
    post = random.choice(posts.data['data'])
    post_id = post['id']
    post = facebook.post('/%s/likes' % post_id)
    return post_id


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
