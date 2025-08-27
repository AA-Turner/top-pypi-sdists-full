# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Database adapter patch for psycopg2.
This module's cursor doesn't have an `executescript` method.
"""

import os
import sys
from contrast.agent.policy import patch_manager
from contrast.patches.databases import dbapi2
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    register_module_patcher,
    unregister_module_patcher,
)

PSYCOPG2 = "psycopg2"
VENDOR = "PostgreSQL"


class Psycopg2Patcher(dbapi2.Dbapi2Patcher):
    @fail_quietly("failed to get database inventory information")
    def extract_connection_attributes(self, connection, connect_args, connect_kwargs):
        """
        Record DB inventory for a Postgres connection.

        Here we make a good effort to find connection params. There are several ways
        that these can be set, in the following order of priority (using dbname as an
        example):
        - using the `connection_factory` kwarg
        - as a kwarg itself - `dbname` or the deprecated `database`
        - via the dbname parameter in the dsn string
        - with the PGDATABASE environment variable

        Newer versions of psycopg2 (v2.7, ~2017) support connection.get_dsn_parameters,
        which provides a dictionary of the parsed connection params - we're interested
        in `dbname`.

        For now, it's still possible for us to miss the dbname (i.e. an old version of
        psycopg2 using the dsn string only), but this is unlikely and it would only
        affect inventory.
        """
        dsn_params = getattr(connection, "get_dsn_parameters", dict)()
        dbname = (
            dsn_params.get("dbname")
            or connect_kwargs.get("dbname")
            or connect_kwargs.get("database")
            or os.environ.get("PGDATABASE", "unknown_database")
        )
        self.db_name = dbname
        super().extract_connection_attributes(connection, connect_args, connect_kwargs)


def instrument_psycopg2(psycopg2):
    dbapi2.instrument_adapter(
        psycopg2, VENDOR, Psycopg2Patcher, extra_cursors=[psycopg2.extensions.cursor]
    )


def register_patches():
    register_module_patcher(instrument_psycopg2, PSYCOPG2)


def reverse_patches():
    unregister_module_patcher(PSYCOPG2)
    if psycopg2 := sys.modules.get(PSYCOPG2):
        patch_manager.reverse_patches_by_owner(psycopg2)
        patch_manager.reverse_patches_by_owner(psycopg2.extensions.connection)
        patch_manager.reverse_patches_by_owner(psycopg2.extensions.cursor)
        patch_manager.reverse_patches_by_owner(psycopg2.extras.NamedTupleCursor)
