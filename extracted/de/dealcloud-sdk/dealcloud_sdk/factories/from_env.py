from os import getenv

from dealcloud_sdk.constants.env_var_names import (
    CLIENT_ID_ENV_NAME,
    CLIENT_SECRET_ENV_NAME,
    SITE_URL_ENV_NAME,
)
from dealcloud_sdk.models.factory_models import DealCloudFactoryArgs


def read_env_config(env_name: str) -> str:
    """
    Raises a KeyError if the environment variable is not set.
    Args:
        env_name: the name of the environment variable

    Returns:
        the value of the environment variable

    """
    env_value = getenv(env_name)
    if not env_value:
        raise KeyError(f"The environment variable {env_name} could not be found!")

    return env_value


def dc_from_environment_variables(
    site_url_env_name: str = SITE_URL_ENV_NAME,
    client_id_env_name: str = CLIENT_ID_ENV_NAME,
    client_secret_env_name: str = CLIENT_SECRET_ENV_NAME,
) -> DealCloudFactoryArgs:
    """
    Create a DealCloud object from environment variables.

    site_url_env_name (str): The environment variable name containing the site_url.
    client_id_env_name (str): The environment variable name containing the client ID.
    client_secret_env_name (str): The environment variable name containing the client secret.

    Returns:
       (DealCloudFactoryArgs): the  arguments to instantiate a DealCloud class.
    """

    site_url = read_env_config(site_url_env_name)
    client_id = read_env_config(client_id_env_name)
    client_secret = read_env_config(client_secret_env_name)

    dc = DealCloudFactoryArgs(
        site_url=site_url,
        client_id=client_id,
        client_secret=client_secret,
    )

    return dc
