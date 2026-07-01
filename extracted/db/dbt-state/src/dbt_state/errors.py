from __future__ import annotations

import abc


class BaseRunCacheError(Exception, abc.ABC):
    """Base class for all errors."""


class AdapterExtensionError(BaseRunCacheError):
    """Errors related to adapter extensions."""


class AuthenticationError(BaseRunCacheError):
    """Raised when authentication operations fail.

    By default this halts the dbt run: the user must fix their configuration
    (e.g. log in, supply valid credentials, or disambiguate the org id).
    """


class RecoverableAuthenticationError(AuthenticationError):
    """An authentication failure that should NOT block the dbt run.

    Raised when the state client cannot authenticate for a reason that is not
    the user's fault to fix: either dbt Labs has disabled their account/org, or
    the dbt platform auth service is unavailable. In these cases the state
    client fails open (disables itself) so the dbt run proceeds normally.
    """


class CertificateError(BaseRunCacheError):
    """Raised when there is an issue with SSL/TLS certificates."""


class UnsupportedClientVersionError(BaseRunCacheError):
    """Raised when the current client version is not supported."""
