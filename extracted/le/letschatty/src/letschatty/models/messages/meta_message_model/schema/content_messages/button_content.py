from pydantic import BaseModel

class MetaButtonContent(BaseModel):
    """When the messages type field is set to button, this object is included in the messages object:
        payload – String. The payload for a button set up by the business that a customer clicked as part of an interactive message.
        text — String. Button text.
    """
    payload: str
    text: str