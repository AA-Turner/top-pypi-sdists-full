import logging
import os
from typing import Optional

from teradataml import create_context, get_context, configure, remove_context
from typing_extensions import deprecated

from .wrappers import execute_sql

logger = logging.getLogger(__name__)

__all__ = ["aoa_create_context", "tmo_create_context"]

SENSITIVE_ENV_VARS = [
    "VMO_CONN_PASSWORD",
    "VMO_CONN_USERNAME",
    "VMO_CONN_JWT",
    "VMO_CONN_ENCRYPTION_TOKEN",
    "AOA_CONN_PASSWORD",
    "AOA_CONN_USERNAME",
    "AOA_CONN_JWT",
    "AOA_CONN_ENCRYPTION_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
]


@deprecated(
    "aoa_create_context is deprecated, please use tmo_create_context instead.",
    category=DeprecationWarning,
)
def aoa_create_context(database: Optional[str] = None) -> None:
    """
    Creates a teradataml context if one does not already exist.
    Most users should not need to understand how we pass the environment variables etc. for dataset connections. This
    provides a way to achieve that and also allow them to work within a notebook for example where a context is already
    present.

    We create the connection based on the following environment variables which are configured automatically by ModelOps
    based on the dataset connection selected:

        AOA_CONN_HOST
        AOA_CONN_USERNAME
        AOA_CONN_PASSWORD
        AOA_CONN_JWT
        AOA_CONN_LOG_MECH
        AOA_CONN_DATABASE
        AOA_VAL_INSTALL_DB
        AOA_BYOM_INSTALL_DB

    :param database: default database override
    :return: None
    """
    return tmo_create_context(database)  # noqa


def tmo_create_context(database: Optional[str] = None, force: bool = False) -> None:
    """
    Creates a teradataml context if one does not already exist.
    Most users should not need to understand how we pass the environment variables etc. for dataset connections. This
    provides a way to achieve that and also allow them to work within a notebook for example where a context is already
    present.

    We create the connection based on the following environment variables which are configured automatically by ModelOps
    based on the dataset connection selected:

        VMO_CONN_HOST
        VMO_CONN_USERNAME
        VMO_CONN_PASSWORD
        VMO_CONN_JWT
        VMO_CONN_LOG_MECH
        VMO_CONN_DATABASE
        VMO_VAL_INSTALL_DB
        VMO_BYOM_INSTALL_DB

    :param database: default database override
    :param force: if True, forces recreation of the context even if one already exists
                  with matching parameters.  Requires fresh credentials to be present in
                  the environment; raises ValueError before touching the existing context
                  if they are missing.
    :return: None
    """
    _rename_env_variables()

    try:
        if not database:
            database = os.getenv("VMO_CONN_DATABASE")

        host = os.environ["VMO_CONN_HOST"]
        logmech = os.getenv("VMO_CONN_LOG_MECH", "TDNEGO").upper()

        if force or not _is_same_context(host, logmech, database):
            if force:
                _validate_credentials(logmech)
            if get_context() is not None:
                remove_context()
            if database:
                logger.debug(
                    f"Configuring temp database for tables/views to {database}"
                )
                configure.temp_table_database = database
                configure.temp_view_database = database

            configure.val_install_location = os.environ.get("VMO_VAL_INSTALL_DB", "VAL")
            configure.byom_install_location = os.environ.get(
                "VMO_BYOM_INSTALL_DB", "MLDB"
            )

            if logmech == "JWT":
                jwt_token = os.environ["VMO_CONN_JWT"]
                logger.debug(
                    f"Connecting to {host} on database {database} using logmech JWT"
                )
                create_context(
                    host=host,
                    database=database,
                    logmech=logmech,
                    logdata=f"token={jwt_token}",
                )
            else:
                username = os.environ["VMO_CONN_USERNAME"]
                password = os.environ["VMO_CONN_PASSWORD"]
                logger.debug(
                    f"Connecting to {host} on database {database} using logmech"
                    f" {logmech} as {username}"
                )
                create_context(
                    host=host,
                    database=database,
                    username=username,
                    password=password,
                    logmech=logmech,
                )

            from tmo import __version__

            execute_sql(f"""
            SET QUERY_BAND = 'appVersion={__version__};appName=VMO;appFunc=python;org=teradata-internal-telem;' FOR SESSION VOLATILE
            """)

        else:
            logger.info("teradataml context already exists. Skipping create_context.")
    finally:
        _sanitize_env_variables()


def _validate_credentials(logmech: str) -> None:
    """Raise ValueError if the credentials required to create a new context are absent.

    Called when force=True to ensure the existing context is never torn down
    when the subsequent create_context() call would fail with a KeyError.

    Args:
        logmech: The logon mechanism (e.g. "JWT", "TDNEGO", "LDAP").

    Raises:
        ValueError: If one or more required credential env vars are not set.
    """
    if logmech == "JWT":
        if os.environ.get("VMO_CONN_JWT") is None:
            raise ValueError(
                "force=True requires fresh credentials but VMO_CONN_JWT is not set. "
                "Provide VMO_CONN_JWT before calling tmo_create_context(force=True)."
            )
    else:
        missing = [
            v
            for v in ("VMO_CONN_USERNAME", "VMO_CONN_PASSWORD")
            if os.environ.get(v) is None
        ]
        if missing:
            raise ValueError(
                f"force=True requires fresh credentials but {' and '.join(missing)} "
                f"{'is' if len(missing) == 1 else 'are'} not set. "
                "Provide VMO_CONN_USERNAME and VMO_CONN_PASSWORD before calling "
                "tmo_create_context(force=True)."
            )


def _check_jwt_difference(existing_context, differences: list) -> None:
    """Check if JWT token differs from the existing context; appends to differences if so.
    Skips comparison if VMO_CONN_JWT is absent (sanitized after a previous connect).
    """
    provided_jwt = os.environ.get("VMO_CONN_JWT")
    if provided_jwt is None:
        return  # sanitized after previous connect — reuse existing context
    existing_logdata = existing_context.url.query.get("LOGDATA", "")
    if existing_logdata != f"token={provided_jwt}":
        differences.append("logdata: <token changed>")


def _check_username_difference(existing_context, differences: list) -> None:
    """Check if username differs from the existing context; appends to differences if so.
    Skips comparison if VMO_CONN_USERNAME is absent (sanitized after a previous connect).
    Note: password comparison is intentionally skipped — teradataml masks it as '***'.
    """
    provided_username = os.environ.get("VMO_CONN_USERNAME")
    if provided_username is None:
        return  # sanitized after previous connect — reuse existing context
    existing_username = existing_context.url.username
    if existing_username != provided_username:
        differences.append(f"username: '{existing_username}' → '{provided_username}'")


def _get_param_differences(
    existing_context, host: str, log_mech: str, database: Optional[str]
) -> list[str]:
    """Return a list of 'param: old → new' strings for each connection parameter
    that differs between the existing context and the requested values.

    Covers host, database and logmech only.  Credential differences (JWT / username)
    are handled separately by _check_jwt_difference and _check_username_difference.
    """
    existing_host = existing_context.url.host
    existing_database = (
        existing_context.url.query.get("DATABASE")
        or configure._current_database_name  # noqa
    )
    existing_log_mech = existing_context.url.query.get("LOGMECH", "TDNEGO").upper()

    differences = []
    if existing_host != host:
        differences.append(f"host: '{existing_host}' → '{host}'")
    if existing_database != database:
        differences.append(f"database: '{existing_database}' → '{database}'")
    if existing_log_mech != log_mech:
        differences.append(f"logmech: '{existing_log_mech}' → '{log_mech}'")
    return differences


def _warn_if_params_changed(
    existing_context, host: str, log_mech: str, database: Optional[str]
) -> None:
    """Emit a warning when connection parameters differ from the existing context
    but no credentials are available to act on the change.

    This helps users understand why their parameter changes were ignored and
    what they need to do (provide fresh credentials or use force=True).
    """
    changes = _get_param_differences(existing_context, host, log_mech, database)
    if changes:
        logger.warning(
            "Connection parameters changed (%s) but no credentials are available. "
            "Reusing the existing context — changes will be ignored. "
            "To reconnect with the new parameters, provide fresh credentials "
            "and call tmo_create_context() again, or use force=True.",
            ", ".join(changes),
        )


def _is_same_context(host: str, log_mech: str, database: Optional[str]) -> bool:
    """
    Checks if the existing teradataml context matches the provided connection parameters.

    Args:
        host: The host to compare against the existing context.
        log_mech: The logon mechanism to compare against the existing context.
        database: The database to compare against the existing context.

    Returns:
        True if the existing context matches all provided parameters, False otherwise.
    """
    existing_context = get_context()
    if existing_context is None:
        return False

    # If no credentials are present we cannot create a new context regardless of
    # whether params changed.  This covers two situations:
    #   1. Credentials were sanitized after a previous successful connect.
    #   2. Credentials were never provided (e.g. context was created manually).
    # In both cases the only sane action is to reuse the existing context.
    #
    # NOTE: when fresh credentials ARE present we always proceed to parameter
    # comparison so that a caller who re-sets credentials for a different
    # host/database gets a new connection, even if the context already exists.
    credentials_available = (
        os.environ.get("VMO_CONN_USERNAME") is not None
        or os.environ.get("VMO_CONN_JWT") is not None
    )
    if not credentials_available:
        # Even though we must reuse the existing context, warn if the caller
        # provided different parameters — their changes will be silently ignored
        # otherwise, which is hard to debug.
        _warn_if_params_changed(existing_context, host, log_mech, database)
        logger.debug(
            "No credentials available; reusing existing context without parameter"
            " comparison."
        )
        return True

    differences = _get_param_differences(existing_context, host, log_mech, database)
    if log_mech == "JWT":
        _check_jwt_difference(existing_context, differences)
    else:
        _check_username_difference(existing_context, differences)

    if differences:
        logger.debug(
            f"Existing context differs from requested: {', '.join(differences)}"
        )
        return False

    return True


def _sanitize_env_variables() -> None:
    """
    Sanitize the environment variables to remove any sensitive information.
    """
    for key in list(os.environ.keys()):  # noqa
        if key in SENSITIVE_ENV_VARS:
            del os.environ[key]


def _rename_env_variables() -> None:
    """
    Rename the environment variables from AOA to VMO.
    """
    for key in list(os.environ.keys()):  # noqa
        if key.startswith("AOA_"):
            new_key = key.replace("AOA_", "VMO_")
            if not os.environ.get(new_key):
                os.environ[new_key] = os.environ[key]
