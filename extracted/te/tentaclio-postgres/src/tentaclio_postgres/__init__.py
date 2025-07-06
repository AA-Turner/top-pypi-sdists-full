"""This package implements the tentaclio postgres client """
from tentaclio import *  # noqa

from .clients.postgres_client import PostgresClient
from .streams.postgres_handler import PostgresURLHandler


# Db registry
DB_REGISTRY.register("postgresql", PostgresClient)  # type: ignore

# postgres handler
STREAM_HANDLER_REGISTRY.register("postgresql", PostgresURLHandler())  # type: ignore
