from django.apps import AppConfig

from . import __title__, __version__


class TaskMonitorConfig(AppConfig):
    name = "taskmonitor"
    label = "taskmonitor"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = f"{__title__} v{__version__}"

    def ready(self):
        import taskmonitor.signals  # noqa: F401
