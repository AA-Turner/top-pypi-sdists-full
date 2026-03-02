import logging
import os

from teradataml import create_context, get_context, configure
from typing_extensions import deprecated

logger = logging.getLogger(__name__)

SENSITIVE_ENV_VARS = [
    "VMO_CONN_PASSWORD",
    "VMO_CONN_USERNAME",
    "VMO_CONN_ENCRYPTION_TOKEN",
    "AOA_CONN_PASSWORD",
    "AOA_CONN_USERNAME",
    "AOA_CONN_ENCRYPTION_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
]


@deprecated(
    "aoa_create_context is deprecated, please use tmo_create_context instead.",
    category=DeprecationWarning,
)
def aoa_create_context(database: str = None):
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
        AOA_CONN_LOG_MECH
        AOA_CONN_DATABASE
        AOA_VAL_INSTALL_DB
        AOA_BYOM_INSTALL_DB

    :param database: default database override
    :return: None
    """
    return tmo_create_context(database)


def tmo_create_context(database: str = None):
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
        VMO_CONN_LOG_MECH
        VMO_CONN_DATABASE
        VMO_VAL_INSTALL_DB
        VMO_BYOM_INSTALL_DB

    :param database: default database override
    :return: None
    """
    _rename_env_variables()

    try:
        if get_context() is None:
            if not database:
                database = os.getenv("VMO_CONN_DATABASE")

            host = os.environ["VMO_CONN_HOST"]
            logmech = os.getenv("VMO_CONN_LOG_MECH", "TDNEGO")
            username = os.environ["VMO_CONN_USERNAME"]
            password = os.environ["VMO_CONN_PASSWORD"]

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


def execute_sql_in_context(context, statement, parameters=None):
    from teradataml.common.exceptions import TeradataMlException
    from teradataml.common.messages import Messages
    from teradataml.common.messagecodes import MessageCodes

    if context is not None:
        tdsql_con = context.raw_connection().driver_connection
        cursor = tdsql_con.cursor()
        return cursor.execute(statement, parameters)
    else:
        raise TeradataMlException(
            Messages.get_message(MessageCodes.INVALID_CONTEXT_CONNECTION),
            MessageCodes.INVALID_CONTEXT_CONNECTION,
        )


def execute_sql(statement, parameters=None):
    return execute_sql_in_context(get_context(), statement, parameters)


def _sanitize_env_variables():
    """
    Sanitize the environment variables to remove any sensitive information.
    """
    for key in os.environ:
        if key in SENSITIVE_ENV_VARS:
            del os.environ[key]


def _rename_env_variables():
    """
    Rename the environment variables from AOA to VMO.
    """
    for key in os.environ:
        if key.startswith("AOA_"):
            new_key = key.replace("AOA_", "VMO_")
            os.environ[new_key] = os.environ[key]
