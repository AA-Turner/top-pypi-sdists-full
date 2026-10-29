__lazy_modules__ = ["django.http"]

from typing import TYPE_CHECKING, Any

from django.conf import settings

from .views import NightModeRedirectView

if TYPE_CHECKING:
    from django.http import HttpRequest


def auth_settings(request: "HttpRequest") -> dict[str, Any]:
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'NIGHT_MODE': NightModeRedirectView.night_mode_state(request),
    }
