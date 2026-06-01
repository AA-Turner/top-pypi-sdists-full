from csrd.context._constants import APP_ID_HEADER_NAME, HIT_ID_HEADER_NAME

AUTH_HEADER_NAME = "authorization"
API_VERSION_HEADER_NAME = "x-api-version"
VERSIONING_SETTINGS_STATE_KEY = "_versioning_settings"
UNVERSIONED_DISPLAY_LABEL = "Unversioned"
UNVERSIONED = "unv"
"""Sentinel for unversioned routes in version mappings.

Use as a key in ``version_mapping`` or as the ``default_version`` argument
to indicate routes that do not belong to any numbered API version.
This is the canonical normalized form — ``normalize_version(None)``
and ``normalize_version("unversioned")`` both produce this value.
"""

HTTP_METHODS = frozenset({"get", "post", "put", "delete", "patch", "options", "head"})


__all__ = (
    "API_VERSION_HEADER_NAME",
    "APP_ID_HEADER_NAME",
    "AUTH_HEADER_NAME",
    "HIT_ID_HEADER_NAME",
    "HTTP_METHODS",
    "UNVERSIONED",
    "UNVERSIONED_DISPLAY_LABEL",
    "VERSIONING_SETTINGS_STATE_KEY",
)
