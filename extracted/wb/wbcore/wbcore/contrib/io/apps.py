from django.apps import AppConfig
from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate
from django.utils.module_loading import autodiscover_modules


class ImportExportConfig(AppConfig):
    name = "wbcore.contrib.io"

    def ready(self):
        """
        registered source from settings
        """
        from anymail.signals import inbound

        # Implicitly connect a signal handlers decorated with @receiver.
        from wbcore.contrib.io.management import load_sources_from_settings

        from .backends.mail import handle_inbound

        # Explicitly connect a signal handler.
        inbound.connect(handle_inbound)

        def autodiscover_backends(
            app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs
        ):
            # we wrap the autodiscover into a post_migrate receiver because we expect db calls
            autodiscover_modules("import_export.backends")

        post_migrate.connect(
            autodiscover_backends,
            dispatch_uid="wbcore.io.autodiscover_backends",
        )
        post_migrate.connect(
            load_sources_from_settings,
            dispatch_uid="wbcore.contrib.io.load_sources_from_settings",
        )
