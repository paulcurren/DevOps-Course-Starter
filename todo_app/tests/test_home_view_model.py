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
    