class Item:
    def __init__(self, id, status, title):
        self.id = id
        self.status = status
        self.title = title

    def __repr__(self):
        return "%s, %s, %s" % (self.id, self.status, self.title)
