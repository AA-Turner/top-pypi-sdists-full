__lazy_modules__ = ["django.core.checks"]

from typing import TYPE_CHECKING

from django.conf import settings
from django.core.checks import Error

if TYPE_CHECKING:
    from django.core.checks import CheckMessage


def check_login_scopes_setting(*args, **kwargs) -> "list[CheckMessage]":
    errors = []
    try:
        assert settings.LOGIN_TOKEN_SCOPES
    except (AssertionError, AttributeError):
        errors.append(Error('LOGIN_TOKEN_SCOPES setting cannot be blank.',
                            hint='SSO tokens used for logging in must require scopes to be refreshable.'))
    return errors
