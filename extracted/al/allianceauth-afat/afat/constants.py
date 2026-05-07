"""
Constants used in this module
"""

# Standard Library
import re
from enum import Enum

# Django
from django.utils.text import slugify

# Alliance Auth AFAT
from afat import __title__

APP_BASE_URL = slugify(value=__title__, allow_unicode=True)

INTERNAL_URL_PREFIX = "-"


class RegexPattern(Enum):
    """
    Pre-compiled regex patterns
    """

    FLEET_COMPOSITION = re.compile(
        pattern=r"(?im)^([a-zA-Z0-9 -_]{3,37})[\t](.*)[\t](.*)[\t](.*)[\t](.*)[\t]([0-5] - [0-5] - [0-5])([\t](.*))?$"
    )
