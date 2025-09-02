
from pydantic import BaseModel

class MetaButtonReply(BaseModel):
    id: str
    title: str

class MetaListReply(BaseModel):
    id: str
    title: str
    description: str

class MetaInteractiveType(BaseModel):
    button_reply: MetaButtonReply
    list_reply: MetaListReply

class MetaInteractiveContent(BaseModel):
    """type — Object with the following properties:
            button_reply – Sent when a customer clicks a button. Object with the following properties:
                id — String. Unique ID of a button.
                title — String. Title of a button.
            list_reply — Sent when a customer selects an item from a list. Object with the following properties:
                id — String. Unique ID of the selected list item.
                title — String. Title of the selected list item.
                description — String. Description of the selected row.
    """
    type: MetaInteractiveType
