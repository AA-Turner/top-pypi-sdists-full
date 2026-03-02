from functools import wraps
from typing import Any, Callable

from dlt.common.typing import TFun
from dlt.common.configuration.container import Container

from dlthub.common.license.exceptions import (
    DltLicenseNotFoundException,
    DltUnknownScopeException,
    DltLicenseException,
)
from dlthub.common.license.license import (
    LicenseContext,
    get_known_features,
    ensure_scope,
    ensure_feature_scope,
)


def ensure_license_with_scope(scope: str) -> None:
    """Ensures that license with `scope` is available and validates dlthub
    public key LICENSE_PUBLIC_KEY
    """
    try:
        validated_scopes = Container()[LicenseContext].validated_scopes()
    except DltLicenseNotFoundException as license_ex:
        # add feature info to get exception message with issuance instructions
        license_ex.set_scope(scope, get_known_features()[scope][0])
        raise

    ensure_scope(validated_scopes, scope)


def is_scope_active(scope: str) -> bool:
    """Checks if a scope is currently active, if there is a missing license or an invalid license,
    returns False without raising an exception.
    """
    try:
        ensure_license_with_scope(scope)
        return True
    except DltUnknownScopeException:
        # this is a dlt developer error, raise here
        raise
    except DltLicenseException:
        return False


def require_license(scope: str) -> Callable[[TFun], TFun]:
    """Decorator that requires a valid license to execute the decorated function.

    Args:
        scope (str): The scope of the license required to execute the function.
            It is always a feature scope in form package.feature ie. `dlthub.sources.mssql`

    Returns:
        TFun: A decorator function that validates the license before executing the function.

    Raises:
        DltLicenseNotFoundException: If no license is found in environment or secrets.toml
        DltLicenseExpiredException: If the license has expired
        DltLicenseSignatureInvalidException: If the license signature is invalid
    """
    ensure_feature_scope(scope)

    def decorator(func: TFun) -> TFun:
        @wraps(func)
        def wrapper_func(*args: Any, **kwargs: Any) -> Any:
            ensure_license_with_scope(scope)
            return func(*args, **kwargs)

        return wrapper_func  # type: ignore[return-value]

    return decorator
