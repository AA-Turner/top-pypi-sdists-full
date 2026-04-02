"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy

# Alliance Auth AFAT
from afat import __title_translated__, __version__


class AfatConfig(AppConfig):
    """
    General config
    """

    name = "afat"
    label = "afat"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
