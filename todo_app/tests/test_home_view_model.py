import pytest

from todo_app.src.Data.item import Item
from todo_app.src.ViewModels.HomeViewModel import HomeViewModel


def test_doing_items():
    # arrange
    item1 = Item(1, "Doing", "Item1")
    item2 = Item(2, "Done", "Item2")
    item3 = Item(3, "Doing", "Item3")
    
    view_model = HomeViewModel(items=[item1, item2, item3], statuses=[])

    # act
    doing_items = view_model.doing_items

    # assert
    assert len(doing_items) == 2
    assert doing_items[0].title == "Item1"
    assert doing_items[1].title == "Item3"

def test_done_items():
    # arrange
    item1 = Item(1, "Doing", "Item1")
    item2 = Item(2, "Done", "Item2")
    item3 = Item(3, "Doing", "Item3")
    
    view_model = HomeViewModel(items=[item1, item2, item3], statuses=[])

    # act
    done_items = view_model.done_items

    # assert
    assert len(done_items) == 1
    assert done_items[0].title == "Item2"

def test_todo_items():
    # arrange
    item1 = Item(1, "Doing", "Item1")
    item2 = Item(2, "Done", "Item2")
    item3 = Item(3, "Doing", "Item3")
    item3 = Item(4, "To Do", "Item4")
    
    view_model = HomeViewModel(items=[item1, item2, item3], statuses=[])

    # act
    todo_items = view_model.todo_items

    # assert
    assert len(todo_items) == 1
    assert todo_items[0].title == "Item4"
