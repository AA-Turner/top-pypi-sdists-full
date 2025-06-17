######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.879909                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.snowflake.snowflake

from ...remote_config import init_config as init_config

SERVICE_URL: None

class OuterboundsSnowflakeConnectorException(Exception, metaclass=type):
    ...

class OuterboundsSnowflakeIntegrationSpecApiResponse(object, metaclass=type):
    def __init__(self, response):
        ...
    @property
    def account(self):
        ...
    @property
    def user(self):
        ...
    @property
    def default_role(self):
        ...
    @property
    def warehouse(self):
        ...
    @property
    def database(self):
        ...
    ...

def get_snowflake_token(user: str = '', role: str = '', integration: str = '') -> str:
    """
    Uses the Outerbounds source token to request for a snowflake compatible OIDC
    token. This token can then be used to connect to snowflake.
    user: str
        The user the token will be minted for
    role: str
        The role to which the token will be scoped to
    integration: str
        The name of the snowflake integration to use. If not set, an existing integration will be used provided that only one exists per perimeter. If integration is not set and more than one exists, then we raise an exception.
    """
    ...

def connect(user: str = '', role: str = '', integration: str = '', **kwargs):
    """
    Connect to snowflake using the token minted by Outerbounds
    user: str
        The user name used to authenticate with snowflake
    role: str
        The role to request when connect with snowflake
    integration: str
        The name of the snowflake integration to use. If not set, an existing integration will be used provided that only one exists in the current perimeter. If integration is not set and more than one exists in the current perimeter, then we raise an exception.
    kwargs: dict
        Additional arguments to pass to the python snowflake connector
    """
    ...

class Snowflake(object, metaclass=type):
    def __init__(self, user: str = '', role: str = '', integration: str = '', **kwargs):
        ...
    def __enter__(self):
        ...
    def __exit__(self, exception_type, exception_value, traceback):
        ...
    def close(self):
        ...
    ...

class SnowflakeIntegrationProvisioner(object, metaclass=type):
    def __init__(self, integration_name: str):
        ...
    def get_snowflake_integration_spec(self) -> OuterboundsSnowflakeIntegrationSpecApiResponse:
        ...
    def get_integration_name(self) -> str:
        ...
    def get_perimeter(self) -> str:
        ...
    def get_snowflake_token_url(self) -> str:
        ...
    def get_service_auth_header(self) -> str:
        ...
    ...

