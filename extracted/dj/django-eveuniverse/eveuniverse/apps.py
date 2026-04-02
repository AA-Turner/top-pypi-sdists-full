from django.apps import AppConfig

from . import __version__


class EveuniverseConfig(AppConfig):
    name = "eveuniverse"
    label = "eveuniverse"
    verbose_name = f"Eve Universe v{__version__}"
    default_auto_field = "django.db.models.AutoField"
