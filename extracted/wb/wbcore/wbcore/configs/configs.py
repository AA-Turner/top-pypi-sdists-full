from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.request import Request
from rest_framework.reverse import reverse

from wbcore.configs.decorators import register_config
from wbcore.shares.config import share_action_button


@register_config
def release_note_config(request: Request) -> tuple[str, dict[str, str]]:
    return "release_notes", {
        "endpoint": reverse("wbcore:releasenote-list", request=request),
        "unread_release_notes": reverse("wbcore:releasenote-unread-count", request=request),
    }


@register_config
def menu_config(request: Request) -> tuple[str, str]:
    return "menu", reverse("wbcore:menu", request=request)


@register_config
def share_config(request: Request):
    return "share", share_action_button(request=request).serialize(request)


@register_config
def menu_calendar_config(request: Request) -> tuple[str, str | None]:
    menu_calendar = None
    if settings.FRONTEND_MENU_CALENDAR:
        menu_calendar = import_string(settings.FRONTEND_MENU_CALENDAR)(request=request)
    return "menu_calendar", menu_calendar


@register_config
def beta_button(request: Request) -> tuple[str, dict] | None:
    beta_url = settings.BETA_BUTTON_URL
    if ((beta_version := settings.BETA_BUTTON_VERSION) or beta_url) and (beta_text := settings.BETA_BUTTON_TEXT):
        if beta_version and not beta_url:
            beta_url = f"{settings.CDN_BASE_ENDPOINT_URL}/{beta_version}/main.js"
        return "beta_button", {"url": beta_url, "text": beta_text}


@register_config
def frontend_version(request: Request) -> tuple[str, str | None]:
    return "frontend_version", getattr(settings, "FRONTEND_VERSION", None)


@register_config
def user_preferences(request: Request) -> tuple[str, dict] | None:
    return "user_preferences", reverse("wbcore:user_preferences-list", request=request)
