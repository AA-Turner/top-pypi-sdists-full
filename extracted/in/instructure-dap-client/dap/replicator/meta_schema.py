import datetime
from dataclasses import dataclass
from typing import Annotated, Optional

from pysqlsync.model.key_types import Identity, PrimaryKey
from strong_typing.auxiliary import MaxLength


@dataclass
class table_sync:
    """
    Table for storing meta-information about tables managed by the client library.

    :param source_namespace: The namespace of the source table exposed by DAP API (e.g. `canvas`).
    :param source_table: The name of the source table exposed by DAP API (e.g. `accounts`).
    :param timestamp: The timestamp of the source table that can be used by the client library in incremental queries
        during subsequent `syncdb` command executions.
    :param schema_version: The latest schema version of the source table at the time point when it was last initialized
        or synchronized with the DAP API.
    :param target_schema: The name of the target schema in the local database if applicable (e.g. in case of
        a PostgreSQL database the tables can be grouped into schemas).
    :param target_table: The name of the target table in the local database. In might differ from the name of the source
        table. For example in case of a MySQL database, the tables cannot be grouped in schemas. In this case,
        the implementor can use a prefix that reflects the namespace of the source table. For example, the qualified
        name `canvas.accounts` would become `canvas__accounts`.
    :param schema_description: The latest schema descriptor of the source table at the time point when it was
        initialized or last synchronized.
    :param schema_description_format: The format of the schema descriptor (e.g. `json`).
    """

    id: PrimaryKey[Identity[int]]
    source_namespace: Annotated[str, MaxLength(64)]
    source_table: Annotated[str, MaxLength(64)]
    timestamp: datetime.datetime
    schema_version: int
    target_schema: Annotated[Optional[str], MaxLength(64)]
    target_table: Annotated[str, MaxLength(64)]
    schema_description_format: Annotated[str, MaxLength(64)]
    schema_description: str


@dataclass
class database_version:
    """
    Table for storing meta-information about the database schema version.

    :param version: The version of the database schema.
    """
    version: PrimaryKey[Identity[int]]
