#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import logging

import pytest

from snowflake.core.database import Database
from snowflake.core.schema import Schema
from tests.utils import is_prod_version, random_string


@pytest.mark.min_sf_ver("99.99.99")
def test_should_never_run_in_prod(snowflake_version):
    # This might still run in dev (where the version contains non-numerals,
    # so check if it has non-numerals). If it does not, then this should never
    # run.
    if is_prod_version(snowflake_version):
        pytest.fail("This test should not have run in a production version.")


@pytest.mark.min_sf_ver("1.0.0")
def test_should_always_run():
    pass


@pytest.mark.internal_only
@pytest.mark.usefixtures("backup_database_schema")
def test_large_results(databases, set_params):
    # Create a new db because it would only have 2 schemas initially: information_schema and public,
    # which does not trigger large results in the first iteration
    new_db = Database(name=random_string(3, "test_database_$12create_"), kind="TRANSIENT")
    database = databases.create(new_db)
    try:
        # This is fetched without large results
        schema_list1 = sorted(list(map(lambda sch: sch.name, database.schemas.iter())))

        with set_params(parameters={"RESULT_FIRST_CHUNK_MAX_SIZE": 1}, scope="session"):
            # This will be fetched with large results because we force the first chunk size to be small.
            schema_list2 = sorted(list(map(lambda sch: sch.name, database.schemas.iter())))
            assert schema_list1 == schema_list2
    finally:
        database.drop()


@pytest.mark.usefixtures("backup_database_schema")
def test_url_embedding_into_url(schemas, caplog):
    """Test whether URL part embedding works before logging.

    SNOW-1620036

    In the past we logged the URL we were reaching out to before all the paths
    were inserted. Leading to log lines like: "performing a HTTP POST call to
    /api/v2/databases/{database}/schemas". In this test we verify this does not
    happen anymore.
    """
    # We use schema because it's one of the top level objects that have db above
    new_schema = Schema(random_string(5, "test_url_embedding_into_url_"))
    with caplog.at_level(logging.INFO, logger="snowflake.core.schema._generated.api_client"):
        s = schemas.create(new_schema)
    assert "{database}" not in caplog.text
    assert (
        "performing a HTTP POST call to /api/v2/databases/"
        f"{schemas.database.name}/schemas\n"
    ) in caplog.text
    caplog.clear()
    with caplog.at_level(logging.INFO, logger="snowflake.core.schema._generated.api_client"):
        s.drop()
    assert "{database}" not in caplog.text
    assert (
        "performing a HTTP DELETE call to /api/v2/databases/"
        f"{schemas.database.name}/schemas/{new_schema.name}\n"
    ) in caplog.text


# Since our CI and tests are very unlikely to be a version that is not supported,
# this test should always pass -- we would never set the configuration to make it not work
# with the most recent version.

# TODO(SNOW-1704760): This test is commented out for now because the configuration file has not yet
# been updated in S3, so this test would fail. Once it has been updated, this test should be uncommented.
#
# def test_client_info_integration(root):
#     assert root.client_info.client_version == __version__
#
#     # Assert that ClientInfo parsed the information correctly.
#     assert root.client_info.minimum_supported_version is not None
#     assert root.client_info.end_of_support_version is not None
#     assert root.client_info.recommended_version is not None
#
#     # All minimum and recommended versions should be less than or equal to the current version
#     assert check_version_lte(root.client_info.minimum_supported_version, __version__)
#     assert check_version_lte(root.client_info.end_of_support_version, __version__)
#     assert check_version_lte(root.client_info.recommended_version, __version__)
