from flask import Flask, render_template, request

from todo_app.flask_config import Config
#from todo_app.data.session_items import add_item, get_items

from todo_app.data.trello_items import add_item, get_items, get_statuses, change_status


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET'])
def index():

    statuses = get_statuses()
    allItems = get_items()

    return render_template('index.html', statuses = list(statuses), items = list(allItems))


@app.route('/add_item', methods=['POST'])
def addItem():
    title = request.form.get('title')
    add_item(title)
    statuses = get_statuses()
    allItems = get_items()
    return render_template('index.html', statuses = list(statuses), items = list(allItems))

@app.route('/', methods=['POST'])
def changeItem():
    item = request.form.get('item')
    newStatus = request.form.get('status')

    change_status(item, newStatus)

    statuses = get_statuses()
    allItems = get_items()
    return render_template('index.html', statuses = list(statuses), items = list(allItems))

