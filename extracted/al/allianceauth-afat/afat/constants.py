"""
Constants used in this module
"""

# Django
from django.utils.text import slugify

# Alliance Auth AFAT
from afat import __title__

APP_BASE_URL = slugify(value=__title__, allow_unicode=True)

INTERNAL_URL_PREFIX = "-"
