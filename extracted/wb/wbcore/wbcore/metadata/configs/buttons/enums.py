from enum import Enum


class Button(Enum):
    # Buttons
    REFRESH = "refresh"
    NEW = "new"
    DELETE = "delete"

    # Buttons and Create Buttons
    SAVE = "save"
    SAVE_AND_CLOSE = "save_and_close"
    SAVE_AND_NEW = "save_and_new"

    # Create Buttons
    RESET = "reset"

    # Custom Buttons
    DROPDOWN = "dropdown"
    HYPERLINK = "hyperlink"
    WIDGET = "widget"
    ACTION = "action"

    @classmethod
    def buttons(cls):
        return [
            cls.REFRESH.value,
            cls.NEW.value,
            cls.DELETE.value,
            cls.SAVE.value,
            cls.SAVE_AND_CLOSE.value,
            cls.SAVE_AND_NEW.value,
        ]

    @classmethod
    def create_buttons(cls):
        return [
            cls.SAVE.value,
            cls.SAVE_AND_CLOSE.value,
            cls.SAVE_AND_NEW.value,
            cls.RESET.value,
        ]

    @classmethod
    def custom_buttons(cls):
        return [
            cls.DROPDOWN.value,
            cls.HYPERLINK.value,
            cls.WIDGET.value,
            cls.ACTION.value,
        ]


class ButtonDefaultColor(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    INHERIT = "inherit"  # 'inherit' means that the button will take the color of a surrounding button group


class ButtonType(Enum):
    DROPDOWN = "dropdown"
    HYPERLINK = "hyperlink"
    WIDGET = "widget"
    ACTION = "action"


class HyperlinkTarget(Enum):
    BLANK = "_blank"
    SELF = "_self"
    PARENT = "_parent"
    TOP = "_top"
