from pydantic import BaseModel

class KeyboardInformation(BaseModel):
    """
    The Keyboard Information object contains details and attributes related to a
    computer or device keyboard. It encompasses information that describes the
    characteristics, capabilities, and configuration of the keyboard.
    """

    # Optional:
    function_keys: int | None = None
    ime: str | None = None
    keyboard_layout: str | None = None
    keyboard_subtype: int | None = None
    keyboard_type: str | None = None
