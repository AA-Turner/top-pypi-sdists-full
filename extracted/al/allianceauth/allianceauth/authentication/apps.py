from django.apps import AppConfig
from django.core.checks import Tags, register
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    name = "allianceauth.authentication"
    label = "authentication"
    verbose_name = _("Authentication")

    def ready(self) -> None:
        from allianceauth.authentication import signals  # noqa: F401
        from allianceauth.authentication import checks
        from allianceauth.authentication.task_statistics import (
            signals as celery_signals,
        )

        register(Tags.security)(checks.check_login_scopes_setting)
        celery_signals.reset_counters()
