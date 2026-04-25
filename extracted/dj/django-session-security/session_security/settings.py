"""
Settings for django-session-security.

WARN_AFTER
    Time (in seconds) before the user should be warned that their session will
    expire because of inactivity. Default 540. Overridable via
    ``settings.SESSION_SECURITY_WARN_AFTER``.

EXPIRE_AFTER
    Time (in seconds) before the user should be logged out if inactive. Default
    is 600. Overridable via ``settings.SESSION_SECURITY_EXPIRE_AFTER``.

PASSIVE_URLS
    List of URLs that should be ignored by the middleware. For example the ping
    ajax request of session_security is made without user intervention, so it
    should not update the user's last activity datetime.
    Overridable via ``settings.SESSION_SECURITY_PASSIVE_URLS``.

PASSIVE_URL_NAMES
    Same as PASSIVE_URLS, but takes Django URL names instead of paths. Useful
    when path names change or contain parameterised values. NOTE: namespaces are
    not currently handled. Overridable via
    ``settings.SESSION_SECURITY_PASSIVE_URL_NAMES``.

REDIRECT_TO_LOGOUT
    When True, expired sessions redirect to the logout URL (via POST on
    Django 5.x+) instead of reloading the current page. Useful for SSO
    setups where a page reload would silently re-authenticate the user.
    Default False. Overridable via
    ``settings.SESSION_SECURITY_REDIRECT_TO_LOGOUT``.

SESSION_SECURITY_INSECURE
    Set this to True if you want the project to run without setting
    ``SESSION_EXPIRE_AT_BROWSER_CLOSE=True``. Not recommended.
"""
from django.conf import settings

__all__ = [
    'EXPIRE_AFTER',
    'WARN_AFTER',
    'PASSIVE_URLS',
    'PASSIVE_URL_NAMES',
    'REDIRECT_TO_LOGOUT',
]

# WARNING:  These values cannot be reconfigured by tests
EXPIRE_AFTER = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 600)

WARN_AFTER = getattr(settings, 'SESSION_SECURITY_WARN_AFTER', 540)

PASSIVE_URLS = getattr(settings, 'SESSION_SECURITY_PASSIVE_URLS', [])
PASSIVE_URL_NAMES = getattr(settings, 'SESSION_SECURITY_PASSIVE_URL_NAMES', [])
REDIRECT_TO_LOGOUT = getattr(settings, 'SESSION_SECURITY_REDIRECT_TO_LOGOUT', False)

expire_at_browser_close = getattr(
    settings,
    'SESSION_EXPIRE_AT_BROWSER_CLOSE',
    False
)
force_insecurity = getattr(
    settings,
    'SESSION_SECURITY_INSECURE',
    False
)

if not (expire_at_browser_close or force_insecurity):
    raise Exception(
        'Enable SESSION_EXPIRE_AT_BROWSER_CLOSE or SESSION_SECURITY_INSECURE'
    )
