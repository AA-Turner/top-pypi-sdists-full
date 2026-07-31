"""This package implements the tentaclio postgres client"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

from tentaclio import *  # noqa

from .clients.postgres_client import PostgresClient
from .streams.postgres_handler import PostgresURLHandler

try:
    __version__ = _version("tentaclio-postgres")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Db registry
DB_REGISTRY.register("postgresql", PostgresClient)  # type: ignore

# postgres handler
STREAM_HANDLER_REGISTRY.register("postgresql", PostgresURLHandler())  # type: ignore
