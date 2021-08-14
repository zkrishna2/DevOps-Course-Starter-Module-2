import requests
import os

def get_board_id(board_name):
    url = f"https://api.trello.com/1/search?key={key}&token={token}&query={board_name}&modelTypes=boards&board_fields=name"
    r = requests.get(url).json()  
    response=r["boards"][0]["id"]
    return response

def get_list_id(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists?key={key}&token={token}"
    r = requests.get(url).json()
    list_id=[i["id"] for i in r if i["name"]==list_name]
    return list_id[0]

card_status=lambda list_id:"Completed" if list_id==done_id else "Pending"

key=os.environ.get('TRELLO_KEY')
token=os.environ.get('TRELLO_TOKEN')
board_id=get_board_id(os.environ.get('TRELLO_BOARD_NAME'))
todo_id=get_list_id(board_id, "To Do")
done_id=get_list_id(board_id, "Done")


def get_items():
    """
    Fetches all items from Trello.

    Returns:
        list: The list of all cards.
    """
    url = f"https://api.trello.com/1/boards/{board_id}/cards?key={key}&token={token}"
    r = requests.get(url).json()  
    response=[{"id":i["id"],"status":card_status(i["idList"]),"title":i["name"]} for i in r]
    return response


def get_item(id):
    """
    Fetches the item with the specified ID.

    Args:
        id: The ID of the card.

    Returns:
        item: The card, or None if no card match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == id), None)


def add_item(title):
    """
    Adds a new item with the specified title.

    Args:
        title: The title of the card.

    Returns:
        item: The saved card.
    """
    url = f"https://api.trello.com/1/cards/?key={key}&token={token}&name={title}&idList={todo_id}"
    i = requests.post(url).json()
    response={"id":i["id"],"status":card_status(i["idList"]),"title":i["name"]}
    return response


def complete_item(id):
    """
    Mark an existing item as complete.

    Args:
        id: The id of the card.
    """
    item = get_item(id)

    if item != None:
        url = f"https://api.trello.com/1/cards/{id}?key={key}&token={token}&idList={done_id}"
        i = requests.put(url).json()
        item={"id":i["id"],"status":card_status(i["idList"]),"title":i["name"]}
    
    return item
