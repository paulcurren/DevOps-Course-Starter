from todo_app.data.item import Item

import requests
import os

__boardId = os.getenv('TRELLO_BOARDID')
__key = os.getenv('TRELLO_KEY')
__token = os.getenv('TRELLO_TOKEN')


def change_status(title, status):

    cards = __get_board_cards(__boardId)
    cardId = None
    for card in cards:
        if card['name'] == title:
            cardId = card['id']
    if cardId == None:
        return

    lists = __get_board_lists(__boardId)
    listId = None
    for list in lists:
        if list['name'] == status:
            listId = list['id']
    if listId == None:
        return
    
    __set_card_list(cardId, listId)

def get_statuses():
    lists = __get_board_lists(__boardId)
    for list in lists:
        yield list['name']

def get_items() -> list[Item]:

    lists = __get_board_lists(__boardId)

    for card in __get_board_cards(__boardId):
        listName = __get_list_name(lists, card['idList'])
        yield Item(card['id'], listName, card['name'])
  
def get_item(id) -> Item:
    return None

def add_item(title) -> Item:
    return None

def save_item(item) -> Item:
    return item

def __get_board_cards(boardId):
    response = requests.get(f"https://api.trello.com/1/boards/{boardId}/cards?key={__key}&token={__token}")
    return response.json()

def __set_card_list(cardId, listId):
    response = requests.put(f"https://api.trello.com/1/cards/{cardId}?key={__key}&token={__token}&idList={listId}")
    return response.json()


def __get_board_lists(boardId):
    response = requests.get(f"https://api.trello.com/1/boards/{boardId}/lists?key={__key}&token={__token}")
    return response.json()

def __get_list_name(lists, listId):
    for list in lists:
        if list['id'] == listId:
            return list['name']
    return 'unknown'