class List:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.status = "Completed" if name=="Done" else "Pending"