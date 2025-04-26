#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#



from snowflake.core.database import DatabaseCollection


def test_collection_and_references(fake_root):
    db_collection = DatabaseCollection(fake_root)
    my_db_ref = db_collection["my_db"]
    my_schema_ref = my_db_ref.schemas["my_schema"]
    my_task_ref = my_schema_ref.tasks["my_task"]

    assert my_task_ref.name == "my_task"
    assert my_task_ref.schema.name == "my_schema"
    assert my_task_ref.database.name == "my_db"
    assert my_task_ref.schema is my_schema_ref
    assert my_task_ref.database is my_db_ref
    assert my_task_ref.collection is my_schema_ref.tasks
