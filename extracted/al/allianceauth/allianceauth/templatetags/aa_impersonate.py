"""
Template tags for impersonation
"""

from django import template
from django.apps import apps
from django.template.loader import render_to_string

from allianceauth.impersonate.utils import is_impersonating

register = template.Library()


def _impersonating(context) -> bool:
    request = context.get("request")

    return bool(
        request
        and apps.is_installed("allianceauth.impersonate")
        and is_impersonating(request)
    )


@register.simple_tag(takes_context=True)
def impersonation_active(context) -> bool:
    """
    Return whether the current user is being impersonated

    Usage: ``{% impersonation_active as impersonating %}``
    Safe to use when ``allianceauth.impersonate`` is not installed.
    """

    return _impersonating(context)


@register.simple_tag(takes_context=True)
def impersonation_banner(context) -> str:
    """
    Render the "you are impersonating" banner, or nothing

    Safe to use when ``allianceauth.impersonate`` is not installed.
    """

    if not _impersonating(context):
        return ""

    return render_to_string("impersonate/banner.html", request=context["request"])
