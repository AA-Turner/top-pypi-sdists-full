import importlib

import tinybird_cdk.errors
from tinybird_cdk.connector import SQLConnector

__version__ = "0.17.27"


def connector_for(name) -> SQLConnector:
    try:
        mod_name = f'tinybird_cdk.connectors.{name}'
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        if e.name == mod_name:
            raise tinybird_cdk.errors.UnknownConnectorError(name)
        raise e
    return mod.Connector()
