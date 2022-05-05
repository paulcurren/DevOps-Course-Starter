from flask import Flask, render_template, request, redirect

from todo_app.src.ViewModels.HomeViewModel import HomeViewModel
from todo_app.flask_config import Config
from todo_app.src.Data.trello_items import TrelloItems


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    trelloItems = TrelloItems()

    @app.route('/', methods=['GET'])
    def index():

        home_view_model = HomeViewModel(list(trelloItems.get_items()), list(trelloItems.get_statuses()))

        return render_template('index.html', view_model = home_view_model)


    @app.route('/add_item', methods=['POST'])
    def addItem():

        title = request.form.get('title')
        trelloItems.add_item(title)

        return redirect('/', 303)

    @app.route('/', methods=['POST'])
    def changeItem():

        item = request.form.get('item')
        newStatus = request.form.get('status')
        trelloItems.change_status(item, newStatus)

        return redirect('/', 303)

    return app
