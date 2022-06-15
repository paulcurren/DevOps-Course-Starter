import os
from ssl import match_hostname
import pytest
import requests
from dotenv import load_dotenv, find_dotenv

from todo_app.src import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    # Create the new app.
    test_app = app.create_app()
    
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_board_id = os.getenv('TRELLO_BOARDID')
    fake_response_data = None

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do'
        }]
    elif url == f'https://api.trello.com/1/boards/{test_board_id}/cards':
        fake_response_data = [
            {'id': '456', 'name': 'Test card 1', 'idList': '123abc'},
            {'id': '789', 'name': 'Test card 2', 'idList': '123abc'},
        ]

    return StubResponse(fake_response_data)

def test_index_page(monkeypatch, client):
    # arrange
    monkeypatch.setattr(requests, 'get', get_lists_stub)

    # act
    response = client.get('/')

    # assert
    data = str(response.get_data())

    assert response.status_code == 200
    assert "Test card 1" in data
    assert "Test card 2" in data


    