"""
Helpers to detect impersonation.

These only read the session, so they are safe to import and call
whether or not ``allianceauth.impersonate`` is installed.
"""

from django.http import HttpRequest

# Session key maintained by django-hijack, a stack of the original users' pks
SESSION_KEY = "hijack_history"


def is_impersonating(request: HttpRequest) -> bool:
    """Return True when the current user is being impersonated by a superuser."""
    session = getattr(request, "session", None)
    if session is None:
        return False
    return bool(session.get(SESSION_KEY))


def get_impersonator_pk(request: HttpRequest) -> int | None:
    """Return the pk of the user doing the impersonating, if any."""
    if not is_impersonating(request):
        return None
    return int(request.session[SESSION_KEY][-1])
