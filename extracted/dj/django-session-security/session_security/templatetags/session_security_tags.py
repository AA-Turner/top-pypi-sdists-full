from django import template
from django.conf import settings as django_settings

from session_security.settings import EXPIRE_AFTER, WARN_AFTER

register = template.Library()


@register.filter
def expire_after(request):
    return EXPIRE_AFTER


@register.filter
def warn_after(request):
    return WARN_AFTER


@register.filter
def redirect_to_logout(request):
    return getattr(django_settings, 'SESSION_SECURITY_REDIRECT_TO_LOGOUT', False)
