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
        return self.__items_by_status("Doing")

    @property
    def done_items(self) -> list[Item]:
        return self.__items_by_status("Done")

    @property
    def todo_items(self) -> list[Item]:
        return self.__items_by_status("To Do")


    @property
    def statuses(self) -> list[str]:
        return self._statuses

    def __items_by_status(self, status) -> list[Item]:
        result = []
        for item in self._items:
            if (item.status == status):
                result.append(item)
        return result
    