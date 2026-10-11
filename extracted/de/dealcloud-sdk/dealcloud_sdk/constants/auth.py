"""Authentication constants.

Scope is passed to the DealCloud OAuth2 token endpoint as a space-separated string.
Any scope value(s) are accepted; the SDK does not restrict or validate scope names.
Common documented scopes (https://api.docs.dealcloud.com/docs/token) include:
data, user_management, publish, ri_import, backup.
"""

DEFAULT_SCOPE = ("data", "user_management")  # default when scope not specified
AvailableScopeTypes = tuple[str, ...]  # any tuple of scope strings


