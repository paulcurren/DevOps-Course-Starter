from todo_app.src.Data.item import Item

class HomeViewModel:

    def __init__(self, items: list[Item], statuses: list[str]):
        self._items = items
        self._statuses = statuses

    @property
    def items(self) -> list[Item]:
        return self._items
        
    @property
    def doing_items(self) -> list[Item]:
        return []

    @property
    def statuses(self) -> list[str]:
        return self._statuses
