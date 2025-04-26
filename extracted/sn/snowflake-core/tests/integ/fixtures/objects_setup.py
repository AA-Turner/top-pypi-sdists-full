from contextlib import suppress

import pytest

from tests.integ.utils import (
    backup_database_and_schema,
    setup_credentials,
    setup_spcs,
    should_disable_setup_for_credentials,
    should_disable_setup_for_spcs,
)

from ...utils import is_prod_version
from .constants import TEST_COMPUTE_POOL, TEST_WAREHOUSE, SpcsSetupTuple, objects_to_setup


# Setup Warehouse
@pytest.fixture(scope="session")
def warehouse_setup(cursor):
    cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {TEST_WAREHOUSE};").fetchone()
    cursor.execute(f"USE WAREHOUSE {TEST_WAREHOUSE};").fetchone()


# Setup basic objects: database, schema
@pytest.fixture(scope="session", autouse=True)
def setup_basic(connection):
    with connection.cursor() as cursor, backup_database_and_schema(cursor):
        _temp_database = None
        _temp_schema = None

        for db_name, db in objects_to_setup.items():
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS /* setup_basic */ {db_name} {db['params']}",
            )
            _temp_database = db_name

            cursor.execute(f"USE DATABASE /* setup_basic */ {db_name}")  # just in case it already existed
            for schema_name in db["schemas"]:
                cursor.execute(
                    f"CREATE SCHEMA IF NOT EXISTS /* setup_basic */ {schema_name}",
                )
                _temp_schema = schema_name

        if _temp_database is not None:
            cursor.execute(
                f"USE DATABASE /* setup_basic */ {_temp_database}",
            )
        if _temp_schema is not None:
            cursor.execute(
                f"USE SCHEMA /* setup_basic */ {_temp_schema}",
            )

        try:
            yield
        finally:
            if _temp_database is not None:
                cursor.execute(f"DROP DATABASE /* setup_basic::reset */ {_temp_database}")


# Setup Compute pool by either create FAKE instance family or use CPU_X64_XS
@pytest.fixture(scope="session")
def spcs_setup_objects(cursor, sf_cursor, db_parameters, test_account, snowflake_version):
    # TODO: More accurate prod system detection
    is_prod_database = is_prod_version(snowflake_version)
    if not should_disable_setup_for_spcs(db_parameters) and (not is_prod_database):
        if sf_cursor is None:
            pytest.fail(
                'Either disable setup for SPCS by setting "should_disable_setup_for_spcs" to "true" in '
                "connection config for account you are running the test on or provide a connection "
                "configuration named sf_account = {account=..., database = ....}"
            )
        else:
            setup_spcs(
                executing_account_cursor=sf_cursor,
                target_account_name=test_account,
                instance_families_to_create=["CPU_X64_XS", "FAKE"],
            )
    if is_prod_database:
        instance_family = "CPU_X64_XS"
    else:
        instance_family = "FAKE"

    cursor.execute(
        f"create compute pool if not exists {TEST_COMPUTE_POOL} "
        + f"with instance_family={instance_family} "
        + "min_nodes=1 max_nodes=5 auto_resume=true auto_suspend_secs=60;"
    ).fetchone()[0]

    with suppress(Exception):
        yield SpcsSetupTuple(instance_family, TEST_COMPUTE_POOL)


@pytest.fixture()
def setup_credentials_fixture(sf_cursor, db_parameters, snowflake_version):
    # TODO: More accurate prod system detection
    is_prod_database = is_prod_version(snowflake_version)
    if not should_disable_setup_for_credentials(db_parameters) and (not is_prod_database):
        if sf_cursor is None:
            pytest.fail(
                'Either disable setup for credentials by setting "should_disable_setup_for_credentials" to "true" in '
                "connection config for account you are running the test on or provide a connection "
                "configuration named sf_account = {account=..., database = ....}"
            )
        else:
            setup_credentials(sf_cursor)
