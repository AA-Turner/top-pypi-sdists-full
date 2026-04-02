from django.apps import AppConfig

from . import __version__


class InactivityConfig(AppConfig):
    name = "inactivity"
    label = "inactivity"
    verbose_name = f"Inactivity v{__version__}"
