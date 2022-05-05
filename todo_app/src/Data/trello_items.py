from tokenize import String
from typing import Iterator
from todo_app.src.Data.item import Item

import requests
import os

__boardId = os.getenv('TRELLO_BOARDID')
__key = os.getenv('TRELLO_KEY')
__token = os.getenv('TRELLO_TOKEN')
__default_list = 'To Do'

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


def get_statuses() -> Iterator[str]:
    lists = __get_board_lists(__boardId)
    for list in lists:
        yield list['name']


def get_items() -> Iterator[Item]:
    lists = __get_board_lists(__boardId)
    for card in __get_board_cards(__boardId):
        listName = __get_list_name(lists, card['idList'])
        yield Item(card['id'], listName, card['name'])
  

def get_item(id) -> Item:
    return None


def add_item(title):
    lists = __get_board_lists(__boardId)
    listId = None
    for list in lists:
        if list['name'] == __default_list:
            listId = list['id']   
    __add_card(listId, title)


def save_item(item) -> Item:
    return item


def __add_card(listId, name):
    payload = {'key': __key, 'token': __token, 'name': name, 'idList': listId}
    response = requests.post(f"https://api.trello.com/1/cards", params=payload)
    return response.json()

def __get_board_cards(boardId):
    payload = {'key': __key, 'token': __token}
    response = requests.get(f"https://api.trello.com/1/boards/{boardId}/cards", params=payload)
    return response.json()

def __set_card_list(cardId, listId):
    payload = {'key': __key, 'token': __token, 'idList': listId}
    response = requests.put(f"https://api.trello.com/1/cards/{cardId}", params=payload)
    return response.json()


def __get_board_lists(boardId):
    payload = {'key': __key, 'token': __token}
    response = requests.get(f"https://api.trello.com/1/boards/{boardId}/lists", params=payload)
    return response.json()

def __get_list_name(lists, listId):
    for list in lists:
        if list['id'] == listId:
            return list['name']
    return 'unknown'