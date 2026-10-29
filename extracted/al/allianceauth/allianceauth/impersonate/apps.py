from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImpersonateConfig(AppConfig):
    name = 'allianceauth.impersonate'
    label = 'impersonate'
    verbose_name = _('Impersonate')

    def ready(self) -> None:
        from allianceauth.impersonate import signals  # noqa: F401
