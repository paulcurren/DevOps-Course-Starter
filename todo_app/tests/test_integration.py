import os
import pymongo
import pytest
import mongomock
from dotenv import load_dotenv, find_dotenv

from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    os.environ['LOGIN_DISABLED'] = 'True'
    
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client
   

def get_db():
    client = pymongo.MongoClient('server.example.com')
    db = client['my_db']
    return db

@mongomock.patch(servers=(('server.example.com', 27017),))
def test_index_page(client):

    # arrange
    get_db().collection.insert_one({'name': 'Test card 1', 'status': 'To Do'})
    get_db().collection.insert_one({'name': 'Test card 2', 'status': 'Done'})

    # act
    response = client.get('/')

    # assert
    data = str(response.get_data())

    assert response.status_code == 200
    assert "Test card 1" in data
    assert "Test card 2" in data


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_add_item(client):

    # arrange

    # act
    client.post('/add_item', data=dict(title='Test card 3'))

    # assert
    document = get_db().collection.find_one()

    assert document['name'] == 'Test card 3'
    assert document['status'] == 'To Do'


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_change_status(client):

    # arrange
    result = get_db().collection.insert_one({'name': 'Test card 1', 'status': 'To Do'})

    # act
    client.post('/', data=dict(item=result.inserted_id, status='Doing'))

    # assert
    document = get_db().collection.find_one()

    assert document['status'] == 'Doing'


