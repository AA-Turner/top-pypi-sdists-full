import pytest


@pytest.fixture()
def anaconda_package_available(cursor, warehouse, backup_warehouse_fixture):
    del backup_warehouse_fixture
    packages_required = ["snowflake-snowpark-python", "atpublic"]
    required_available = True
    cursor.execute(f"use warehouse {warehouse.name}").fetchone()
    for package in packages_required:
        packages = cursor.execute(
            f"select * from information_schema.packages where package_name = '{package}';"
        ).fetchmany(3)
        required_available &= packages is not None and len(packages) > 0

    if not required_available:
        pytest.xfail(reason="Anaconda packages not available")


@pytest.fixture()
def maven_snowpark_jar_available(cursor, warehouse, backup_warehouse_fixture):
    del backup_warehouse_fixture
    packages_required = ["com.snowflake:snowpark"]
    required_available = True
    cursor.execute(f"use warehouse {warehouse.name}").fetchone()
    for package in packages_required:
        packages = cursor.execute(
            f"select * from information_schema.packages where package_name = '{package}';"
        ).fetchmany(3)
        required_available &= packages is not None and len(packages) > 0

    if not required_available:
        pytest.xfail(reason="Maven Snowpark jar not available")


@pytest.fixture(scope="session")
def shared_database_available(cursor):
    shared_database = cursor.execute("SHOW SHARES LIKE 'SAMPLE_DATA';").fetchone()
    if shared_database is None or len(shared_database) == 0 or shared_database[2] != "SFSALESSHARED.SFC_SAMPLES_PROD3":
        pytest.xfail(reason="There's no shared database")


@pytest.fixture(scope="session")
def skip_for_snowflake_account(cursor):
    account_name = cursor.execute("SELECT CURRENT_ACCOUNT();").fetchone()
    if len(account_name) > 0 and "SNOWFLAKE" == account_name[0]:
        pytest.skip("Skip when running in Snowflake account")


@pytest.fixture
def qa_mode_enabled(cursor):
    alter_prefix = "alter session "
    try:
        cursor.execute(alter_prefix + "set QA_MODE = true").fetchone()
        yield
        cursor.execute(alter_prefix + "unset QA_MODE").fetchone()
    except Exception:
        pytest.xfail("QA Mode is not available")


@pytest.fixture(scope="session")
def my_integration_exists(cursor):
    integrations = cursor.execute("SHOW INTEGRATIONS LIKE 'my_integration';").fetchone()
    if integrations is None or len(integrations) == 0 or integrations[1] != "my_integration":
        pytest.xfail(reason="my_integration does not exist")
