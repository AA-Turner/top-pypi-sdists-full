import re
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.config import error_messages

NAME_VALIDATION_REGEX = re.compile(r"\A[a-zA-Z0-9\-_\/]+\Z")


class LabelKind:
    PROJECT = "projects"
    DATASET = "datasets"

    @classmethod
    def validate(cls, kind):
        return kind in {cls.PROJECT, cls.DATASET}


class LabelColor:
    BLUE = 'Blue'
    GREEN = 'Green'
    LIGHT_GREEN = 'Light green'
    LIGHT_BLUE = 'Light blue'
    YELLOW = 'Yellow'
    RED = 'Red'
    PURPLE = 'Purple'
    LIGHTGREY = 'Light grey'
    GREY = 'Grey'

    ALL_COLORS = {BLUE, GREEN, LIGHT_GREEN, LIGHT_BLUE, YELLOW, RED, PURPLE, LIGHTGREY, GREY}

    @classmethod
    def validate(cls, color_name):
        return color_name in cls.ALL_COLORS


def validate_labels_params(name, kind, color_name=None):
    if not name or not isinstance(name, str) or not re.match(NAME_VALIDATION_REGEX, name):
        raise CnvrgArgumentsError(error_messages.LABEL_BAD_NAME)

    if not LabelKind.validate(kind):
        raise CnvrgArgumentsError(error_messages.LABEL_BAD_KIND)

    if color_name and not LabelColor.validate(color_name):
        raise CnvrgArgumentsError(error_messages.LABEL_BAD_COLOR)
