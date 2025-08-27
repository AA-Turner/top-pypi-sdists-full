# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contrast.agent.policy import patch_manager
from contrast.patches.databases import dbapi2
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    register_module_patcher,
    repatch_module,
    unregister_module_patcher,
)

VENDOR = "SQLite3"


class Sqlite3Patcher(dbapi2.Dbapi2Patcher):
    @fail_quietly("failed to get database inventory information")
    def extract_connection_attributes(self, connection, connect_args, connect_kwargs):
        # sqlite does not use a server, so no need for host/port
        database = connect_kwargs.get("database") or (
            connect_args[0] if len(connect_args) > 0 else "unknown"
        )
        # this can sometimes be a PosixPath, so we need to cast
        self.db_name = str(database)
        super().extract_connection_attributes(connection, connect_args, connect_kwargs)


def instrument_sqlite3(sqlite3):
    dbapi2.instrument_adapter(
        sqlite3,
        VENDOR,
        Sqlite3Patcher,
        extra_cursors=[
            sqlite3.Cursor,
            # sqlite3.Connection.execute* functions are non-standard convenience
            # functions that will create new cursors automatically. sqlite3.Connection
            # exposes the same execute* API as a standard cursor, however, so for
            # patching purposes we can just identify it as an extra cursor. This only
            # became necessary in newer versions of python (3.11+) where the
            # implementation of these functions was moved to C.
            sqlite3.Connection,
        ],
    )


def register_patches():
    register_module_patcher(instrument_sqlite3, "sqlite3.dbapi2")
    register_module_patcher(repatch_module, "sqlite3")


def reverse_patches():
    for sqlite in ("sqlite3", "sqlite3.dbapi2"):
        unregister_module_patcher(sqlite)
        if sqlite3 := sys.modules.get(sqlite):
            patch_manager.reverse_patches_by_owner(sqlite3)
            patch_manager.reverse_patches_by_owner(sqlite3.Cursor)
            patch_manager.reverse_patches_by_owner(sqlite3.Connection)
