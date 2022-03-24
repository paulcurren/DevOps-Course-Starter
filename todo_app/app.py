from flask import Flask, render_template, request

from todo_app.flask_config import Config
from todo_app.data.session_items import add_item, get_items


app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        return render_template('index.html', items = get_items())

    if (request.method == 'POST'):
        title = request.form.get('title')
        add_item(title)
        return render_template('index.html', items = get_items())


