#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from snowflake.core.database import Database, DatabaseCollection

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_resist_multi_statement_sql_injection(databases: DatabaseCollection):
    new_db_name = random_string(3, "test_db_resist_multi_statement_sql_injection_")
    sql_injection_comment = "'comment for disguise'; select '1'"

    new_db = Database(
        name=new_db_name,
        comment=sql_injection_comment,
    )

    db = databases.create(new_db)
    try:
        db.fetch()
    finally:
        db.drop()
