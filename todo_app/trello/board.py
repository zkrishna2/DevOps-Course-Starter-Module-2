import requests, os
from todo_app.trello.item import Item
from todo_app.trello.list import List

key=os.environ.get('TRELLO_KEY')
token=os.environ.get('TRELLO_TOKEN')

class Board:
    def __init__(self, name):
        self.id = self._get_board_id(name)
        self.name = name
        self.lists = self._init_list()
        self.items = self._init_item()
    
    def _get_board_id(self, board_name):
        url = f"https://api.trello.com/1/search?key={key}&token={token}&query={board_name}&modelTypes=boards&board_fields=name"
        r = requests.get(url).json()  
        return r["boards"][0]["id"]
    
    def _init_list(self):
        url = f"https://api.trello.com/1/boards/{self.id}/lists?key={key}&token={token}"
        r= requests.get(url).json()
        return [List(i["id"],i["name"]) for i in r]
    
    def _init_item(self):
        url = f"https://api.trello.com/1/boards/{self.id}/cards?key={key}&token={token}"
        r = requests.get(url).json()  
        return [Item(i["id"],i["name"],self._get_list_status(i["idList"])) for i in r]

    def _get_list_status(self, list_id):
        return next((l.status for l in self.lists if l.id == list_id), None)

    def _get_todo_list_id(self):
        return next((l.id for l in self.lists if l.name == "To Do"), None)

    def _get_done_list_id(self):
        return next((l.id for l in self.lists if l.name == "Done"), None)


    def get_items(self):
        """
        Returns:
            list: The list of saved items.
        """        
        return self.items


    def get_item(self, item_id):
        """
        Returns the saved item with the specified ID.
        Args:
            item_id: The ID of the item.
        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        return next((i for i in self.items if i.id == item_id), None)


    def add_item(self, title):
        """
        Adds a new item with the specified title.

        Args:
            title: The title of the card.

        Returns:
            Item: The saved card.
        """
        items = self.get_items()

        url = f"https://api.trello.com/1/cards/?key={key}&token={token}&name={title}&idList={self._get_todo_list_id()}"
        r = requests.post(url).json()
        item=Item(r["id"],r["name"],self._get_list_status(r["idList"]))
        
        items.append(item)
        self.items=items
        return item


    def save_item(self, item):
        """
        Updates an existing item. If no existing item matches the ID of the specified item, nothing is saved.
        Args:
            item: The item to save.
        """
        existing_items = self.get_items()
        updated_items = [item if item.id == existing_item.id else existing_item for existing_item in existing_items]

        self.items = updated_items
        return item


    def complete_item(self, item_id):
        """
        Mark an existing item as complete.

        Args:
            item_id: The id of the card.
        """
        item = self.get_item(item_id)

        if item != None:
            url = f"https://api.trello.com/1/cards/{item_id}?key={key}&token={token}&idList={self._get_done_list_id()}"
            r = requests.put(url).json()            
            item=Item(r["id"],r["name"],self._get_list_status(r["idList"]))
            self.save_item(item)

        return item        
