# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contrast.agent.policy import patch_manager
from contrast.patches.databases import dbapi2
from contrast.utils.patch_utils import (
    register_module_patcher,
    unregister_module_patcher,
)

PYMYSQL = "pymysql"
VENDOR = "MySQL"


def instrument_pymysql(pymysql):
    dbapi2.instrument_adapter(
        pymysql, VENDOR, dbapi2.Dbapi2Patcher, extra_cursors=[pymysql.cursors.Cursor]
    )


def register_patches():
    register_module_patcher(instrument_pymysql, PYMYSQL)


def reverse_patches():
    unregister_module_patcher(PYMYSQL)
    if pymysql := sys.modules.get(PYMYSQL):
        patch_manager.reverse_patches_by_owner(pymysql)
        patch_manager.reverse_patches_by_owner(pymysql.connections.Connection)
        patch_manager.reverse_patches_by_owner(pymysql.cursors.Cursor)
