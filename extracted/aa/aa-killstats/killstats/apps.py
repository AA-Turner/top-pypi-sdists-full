"""App Configuration"""

# Django
from django.apps import AppConfig

# AA Killstats
from killstats import __version__


class KillstatsrConfig(AppConfig):
    """App Config"""

    default_auto_field = "django.db.models.AutoField"
    name = "killstats"
    label = "killstats"
    verbose_name = f"Killstats v{__version__}"

    def ready(self) -> None:
        # AA Killstats
        # pylint: disable=import-outside-toplevel
        import killstats.signals  # pylint: disable=unused-import
