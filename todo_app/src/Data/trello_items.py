from tokenize import String
from typing import Iterator
from todo_app.src.Data.item import Item

import requests
import os


class TrelloItems:
    def __init__(self):
        self._boardId = os.getenv('TRELLO_BOARDID')
        self._key = os.getenv('TRELLO_KEY')
        self._token = os.getenv('TRELLO_TOKEN')
        self._default_list = 'To Do'

    def change_status(self, title, status):

        cards = self.__get_board_cards(self._boardId)
        cardId = None
        for card in cards:
            if card['name'] == title:
                cardId = card['id']
        if cardId == None:
            return

        lists = self.__get_board_lists(self._boardId)
        listId = None
        for list in lists:
            if list['name'] == status:
                listId = list['id']
        if listId == None:
            return
        
        self.__set_card_list(cardId, listId)


    def get_statuses(self) -> Iterator[str]:
        lists = self.__get_board_lists(self._boardId)
        for list in lists:
            yield list['name']


    def get_items(self) -> Iterator[Item]:
        lists = self.__get_board_lists(self._boardId)
        for card in self.__get_board_cards(self._boardId):
            listName = self.__get_list_name(lists, card['idList'])
            yield Item(card['id'], listName, card['name'])
    

    def add_item(self, title):
        lists = self.__get_board_lists(self._boardId)
        listId = None
        for list in lists:
            if list['name'] == self._default_list:
                self.__add_card(list['id'], title)        


    def __add_card(self, listId, name):
        payload = {'key': self._key, 'token': self._token, 'name': name, 'idList': listId}
        response = requests.post(f"https://api.trello.com/1/cards", params=payload)
        return response.json()

    def __get_board_cards(self, boardId):
        payload = {'key': self._key, 'token': self._token}
        response = requests.get(f"https://api.trello.com/1/boards/{boardId}/cards", params=payload)
        return response.json()

    def __set_card_list(self, cardId, listId):
        payload = {'key': self._key, 'token': self._token, 'idList': listId}
        response = requests.put(f"https://api.trello.com/1/cards/{cardId}", params=payload)
        return response.json()


    def __get_board_lists(self, boardId):
        payload = {'key': self._key, 'token': self._token}
        response = requests.get(f"https://api.trello.com/1/boards/{boardId}/lists", params=payload)
        return response.json()

    def __get_list_name(self, lists, listId):
        for list in lists:
            if list['id'] == listId:
                return list['name']
        return 'unknown'