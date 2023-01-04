from flask import Flask, render_template, request, redirect

from todo_app.ViewModels.HomeViewModel import HomeViewModel
from todo_app.flask_config import Config
from todo_app.Data.mongo_items import MongoItems


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    itemsStore = MongoItems()

    @app.route('/', methods=['GET'])
    def index():

        items = itemsStore.get_items()
        statuses = itemsStore.get_statuses()

        home_view_model = HomeViewModel(items, statuses)

        return render_template('index.html', view_model = home_view_model)


    @app.route('/add_item', methods=['POST'])
    def addItem():

        title = request.form.get('title')
        itemsStore.add_item(title)

        return redirect('/', 303)

    @app.route('/', methods=['POST'])
    def changeItem():

        item = request.form.get('item')
        newStatus = request.form.get('status')
        itemsStore.change_status(item, newStatus)

        return redirect('/', 303)

    return app
