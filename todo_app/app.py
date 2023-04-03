import json
import sys
import logging
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user

from todo_app.ViewModels.HomeViewModel import HomeViewModel
from todo_app.flask_config import Config
from todo_app.Data.mongo_items import MongoItems

import requests
import os

from loggly.handlers import HTTPSHandler
from logging import Formatter


class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name     

    def get(id):
        #print('User.get', id)
        return User(id, "xx")

    def add(self):
        #print('User.add', self)
        return

def create_app():


    _client_id = os.getenv('CLIENT_ID')
    _client_secret = os.getenv('CLIENT_SECRET')
    _oauth_uri = os.getenv('OAUTH_URI')
    _home_uri = os.getenv('HOME_URI')

    app = Flask(__name__)
    app.config.from_object(Config())
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
    app.config['LOGGLY_TOKEN'] = os.getenv('LOGGLY_TOKEN')

    logFormat = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    dateFormat = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        format=logFormat, 
        datefmt=dateFormat,
        level=os.environ.get("LOG_LEVEL", "DEBUG"))


    rootLog = logging.getLogger()
    

    # reduce Flash logging
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.setLevel(logging.ERROR)

    # reduce handler logging
    urlLog = logging.getLogger('urllib3.connectionpool')
    urlLog.setLevel(logging.ERROR)

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter(fmt = logFormat, datefmt = dateFormat))
        rootLog.addHandler(handler)



    #rootLog.info('Starting with environment: %s', os.environ.items())
    rootLog.info('Starting todo app')

    itemsStore = MongoItems()

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(f'https://github.com/login/oauth/authorize?client_id={_client_id}&redirect_uri={_oauth_uri}', 303)


    @login_manager.user_loader
    def load_user(user_id):
        app.logger.debug('load_user', user_id)
        return User.get(user_id)

    login_manager.init_app(app)


    @app.route('/', methods=['GET'])
    @login_required
    def index():

        items = itemsStore.get_items()
        statuses = itemsStore.get_statuses()

        home_view_model = HomeViewModel(items, statuses)

        return render_template('index.html', view_model = home_view_model)


    @app.route('/add_item', methods=['POST'])
    @login_required
    def addItem():

        title = request.form.get('title')
        itemsStore.add_item(title)

        return redirect('/', 303)

    @app.route('/', methods=['POST'])
    @login_required
    def changeItem():

        item = request.form.get('item')
        newStatus = request.form.get('status')
        itemsStore.change_status(item, newStatus)

        return redirect('/', 303)


    @app.route('/login/callback', methods=['GET'])
    def callback():
        code = request.args.get("code")

        payload = {'client_id': _client_id, 'client_secret': _client_secret, 'code': code, 'redirect_uri': _oauth_uri}
        oauth_headers = {'Accept': 'application/json'}
        oauth_response = requests.get(f'https://github.com/login/oauth/access_token', params=payload, headers=oauth_headers)
        oauth = oauth_response.json()
        #print(oauth)

        access_token = oauth.get('access_token')
        if access_token == None:
            return render_template('noauth.html')

        user_headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get('https://api.github.com/user', headers=user_headers)

        user_info = user_response.json()
        app.logger.debug('user_info', user_info)

        user_id = user_info.get('id')
        user_name = user_info.get('name')

        if user_id == None:
            return render_template('noauth.html')

        user = User(
            id = user_id,
            name = user_name
        )

        user.add()

        login_user(user)

        return redirect('/')

    return app
