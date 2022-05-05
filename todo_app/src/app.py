from flask import Flask, render_template, request, redirect

from todo_app.src.ViewModels.HomeViewModel import HomeViewModel
from todo_app.flask_config import Config
from todo_app.src.Data.trello_items import add_item, get_items, get_statuses, change_status


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET'])
def index():

    home_view_model = HomeViewModel(list(get_items()), list(get_statuses()))

    return render_template('index.html', view_model = home_view_model)


@app.route('/add_item', methods=['POST'])
def addItem():

    title = request.form.get('title')
    add_item(title)

    return redirect('/', 303)

@app.route('/', methods=['POST'])
def changeItem():

    item = request.form.get('item')
    newStatus = request.form.get('status')
    change_status(item, newStatus)

    return redirect('/', 303)

