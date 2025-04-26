# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
import os
import typing

from contextlib import contextmanager, suppress
from typing import Any

import pytest

from pydantic import StrictStr

import snowflake.connector

from snowflake.connector import SnowflakeConnection
from snowflake.core import Root
from snowflake.core._rest_connection import RESTConnection
from snowflake.core.alert import AlertCollection
from snowflake.core.catalog_integration import CatalogIntegration
from snowflake.core.compute_pool import ComputePoolCollection
from snowflake.core.cortex.chat_service import CortexChatService
from snowflake.core.cortex.embed_service import CortexEmbedService
from snowflake.core.cortex.lite_agent_service import CortexAgentService
from snowflake.core.cortex.search_service import CortexSearchServiceCollection
from snowflake.core.database import (
    DatabaseCollection,
    DatabaseResource,
)
from snowflake.core.database_role import DatabaseRoleCollection
from snowflake.core.event_table import EventTableCollection
from snowflake.core.external_volume import ExternalVolumeCollection
from snowflake.core.function import FunctionCollection
from snowflake.core.grant._grants import Grants
from snowflake.core.iceberg_table import IcebergTableCollection
from snowflake.core.image_repository import ImageRepositoryCollection
from snowflake.core.network_policy import NetworkPolicyCollection
from snowflake.core.notebook import NotebookCollection
from snowflake.core.notification_integration import NotificationIntegrationCollection
from snowflake.core.pipe import PipeCollection
from snowflake.core.procedure import ProcedureCollection
from snowflake.core.role import RoleCollection
from snowflake.core.schema import (
    SchemaCollection,
    SchemaResource,
)
from snowflake.core.service import ServiceCollection
from snowflake.core.spark_connect import SparkConnectResource
from snowflake.core.stage import StageCollection
from snowflake.core.stream import StreamCollection
from snowflake.core.table import TableCollection
from snowflake.core.user import UserCollection
from snowflake.core.user_defined_function import UserDefinedFunctionCollection
from snowflake.core.view import ViewCollection
from snowflake.core.warehouse import WarehouseCollection, WarehouseResource
from tests.integ.utils import backup_role

from ..utils import ensure_snowflake_version, is_prod_version
from .fixtures.backup_objects import (  # noqa: F401 # pylint: disable=unused-import
    backup_database_schema,
    backup_warehouse_fixture,
)
from .fixtures.constants import (
    DEFAULT_IR_URL,
    TEST_DATABASE,
    TEST_IMAGE_REPO,
    TEST_IMAGE_REPO_QUALIFIED_SCHEMA,
    TEST_SCHEMA,
    TEST_WAREHOUSE,
)
from .fixtures.objects_setup import (  # noqa: F401 # pylint: disable=unused-import
    setup_basic,
    setup_credentials_fixture,
    spcs_setup_objects,
    warehouse_setup,
)
from .fixtures.pre_checks import (  # noqa: F401 # pylint: disable=unused-import
    anaconda_package_available,
    maven_snowpark_jar_available,
    qa_mode_enabled,
    shared_database_available,
    skip_for_snowflake_account,
)
from .fixtures.temp_objects import (  # noqa: F401 # pylint: disable=unused-import
    temp_cp,
    temp_customer_account_cursor,
    temp_customer_account_root,
    temp_customer_account_with_org_admin,
    temp_customer_organization,
    temp_db,
    temp_db_case_sensitive,
    temp_directory_table,
    temp_ir,
    temp_schema,
    temp_schema_case_sensitive,
    temp_service,
    temp_service_from_spec_inline,
    temp_stage,
    temp_stage_case_sensitive,
    temp_table,
    test_schema,
)
from .utils import connection_config, connection_keys


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Session

RUNNING_IN_NOTEBOOK = "RUNNING_IN_NOTEBOOK" in os.environ
RUNNING_IN_STOREDPROC = "RUNNING_IN_STOREDPROC" in os.environ

SF_ACCOUNT_CONFIG_KEY = "__sf_account__"
SF_ACCOUNT = "snowflake"


@pytest.fixture(scope="session")
def shared_compute_pool(spcs_setup_objects, connection):  # noqa: F811
    yield spcs_setup_objects.compute_pool
    # clean up services and jobs in the compute pool
    print(f"Cleaning up services and jobs in the compute pool {spcs_setup_objects.compute_pool}")
    with connection.cursor() as cur:
        cur.execute(f"alter compute pool {spcs_setup_objects.compute_pool} stop all")


@pytest.fixture(scope="session")
def instance_family(spcs_setup_objects):  # noqa: F811
    yield spcs_setup_objects.instance_family


def print_help() -> None:
    print(
        """Connection parameter must be specified in parameters.py,
    for example:
CONNECTION_PARAMETERS = {
    'account': 'testaccount',
    'user': 'user1',
    'password': 'test',
    'database': 'testdb',
    'schema': 'public',
}
"""
    )


def pytest_runtest_setup(item):
    # Skip any test marked for Notebook when running on Notebook Environment
    if RUNNING_IN_NOTEBOOK:
        notebook_marker = list(item.iter_markers(name="skip_notebook"))
        if notebook_marker:
            pytest.skip("this test is not supposed to run on Notebook Environment")
    # Skip any test marked for Storedproc when running on Storedproc Environment
    if RUNNING_IN_STOREDPROC:
        storedproc_marker = list(item.iter_markers(name="skip_storedproc"))
        if storedproc_marker:
            pytest.skip("this test is not supposed to run on Storedproc Environment")


@pytest.fixture(scope="session")
def cursor(connection):
    with suppress(Exception):
        yield connection.cursor()


@pytest.fixture(autouse=True)
def min_sf_ver(request, snowflake_version):
    if "min_sf_ver" in request.keywords and len(request.keywords["min_sf_ver"].args) > 0:
        requested_version = request.keywords["min_sf_ver"].args[0]

        ensure_snowflake_version(snowflake_version, requested_version)


@pytest.fixture(scope="session")
def snowflake_version(connection) -> str:
    with connection.cursor() as cur:
        return cur.execute("select current_version()").fetchone()[0].strip()


@pytest.fixture(scope="function", autouse=True)
def print_snowflake_version(snowflake_version):
    print(f"Running against Snowflake version: {snowflake_version}")


@pytest.fixture(scope="session")
def db_parameters() -> dict[str, str]:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        from snowflake.snowpark.context import get_active_session

        config = {}
        session = get_active_session()
        config["account"] = session.get_current_account()
        config["schema"] = TEST_SCHEMA
        config["database"] = TEST_DATABASE
        config["warehouse"] = session.get_current_warehouse()
        #  for notebook run make sure the account you are running on is already set up for SPCS
        config["should_disable_setup_for_spcs"] = "true"
        config["should_disable_setup_for_credentials"] = "true"
        return config

    config = connection_config(override_schema=TEST_SCHEMA, override_database=TEST_DATABASE)
    return config


# 2023-06-21(warsaw): WARNING!  If any of these fixtures fail, they will print
# db_parameters in the traceback, and that **will** leak the password.  pytest
# doesn't seem to have any way to suppress the password, and I've tried lots
# of things to get that to work, to no avail.


@pytest.fixture(scope="session")
def session_notebook() -> "Session":
    from snowflake.snowpark.context import get_active_session

    return get_active_session()


@pytest.fixture(scope="session")
def session_default(connection_default) -> "Session":
    from snowflake.snowpark import Session

    return Session.builder.config("connection", connection_default).create()


@pytest.fixture(scope="session")
def session(request) -> "Session":
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        return request.getfixturevalue("session_notebook")
    else:
        return request.getfixturevalue("session_default")


@pytest.fixture(scope="session")
def connection_notebook(session_notebook) -> SnowflakeConnection:
    return session_notebook.connection


@pytest.fixture(scope="session")
def connection_default(db_parameters) -> SnowflakeConnection:
    _keys = connection_keys()
    with snowflake.connector.connect(
        # This works around SNOW-998521, by forcing JSON results
        **{k: db_parameters[k] for k in _keys if k in db_parameters}
    ) as con:
        yield con


@pytest.fixture(scope="session")
def connection(request) -> SnowflakeConnection:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        return request.getfixturevalue("connection_notebook")
    else:
        return request.getfixturevalue("connection_default")


@pytest.fixture(scope="session")
def test_account(db_parameters) -> str:
    return db_parameters["account"].lower().strip()


@pytest.fixture(scope="session")
def root(request, connection) -> Root:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        notebook_session = request.getfixturevalue("session_notebook")
        return Root(notebook_session)
    return Root(connection)


@pytest.fixture(scope="session")
def database(root) -> DatabaseResource:
    return root.databases[TEST_DATABASE]


@pytest.fixture(scope="session")
def schema(schemas) -> SchemaResource:
    return schemas[TEST_SCHEMA]


@pytest.fixture(scope="session")
def warehouse(warehouses, warehouse_setup) -> WarehouseResource:  # noqa: F811
    return warehouses[TEST_WAREHOUSE]


@pytest.fixture(scope="module")
def image_repositories(schema) -> ImageRepositoryCollection:
    return schema.image_repositories


@pytest.fixture(scope="module")
def compute_pools(root) -> ComputePoolCollection:
    return root.compute_pools


@pytest.fixture(scope="session")
def external_volumes(root) -> ExternalVolumeCollection:
    return root.external_volumes


@pytest.fixture(scope="session")
def warehouses(root) -> WarehouseCollection:
    return root.warehouses


@pytest.fixture(scope="session")
def services(schema) -> ServiceCollection:
    return schema.services


@pytest.fixture(scope="session")
def functions(schema) -> FunctionCollection:
    return schema.functions


@pytest.fixture(scope="session")
def notebooks(schema) -> NotebookCollection:
    return schema.notebooks


@pytest.fixture(scope="session")
def procedures(schema) -> ProcedureCollection:
    return schema.procedures


@pytest.fixture(scope="session")
def database_roles(database) -> DatabaseRoleCollection:
    return database.database_roles


@pytest.fixture(scope="session")
def databases(root) -> DatabaseCollection:
    return root.databases


@pytest.fixture(scope="session")
def notification_integrations(root) -> NotificationIntegrationCollection:
    return root.notification_integrations


@pytest.fixture(scope="session")
def schemas(database) -> SchemaCollection:
    return database.schemas


@pytest.fixture(scope="module")
def roles(root) -> RoleCollection:
    return root.roles


@pytest.fixture(scope="module")
def users(root) -> UserCollection:
    return root.users


@pytest.fixture(scope="module")
def grants(root) -> Grants:
    return root.grants


@pytest.fixture(scope="module")
def network_policies(root) -> NetworkPolicyCollection:
    return root.network_policies


@pytest.fixture(scope="module")
def stages(schema) -> StageCollection:
    return schema.stages


@pytest.fixture(scope="module")
def streams(schema) -> StreamCollection:
    return schema.streams


@pytest.fixture(scope="module")
def pipes(schema) -> PipeCollection:
    return schema.pipes


@pytest.fixture(scope="module")
def tables(schema) -> TableCollection:
    return schema.tables


@pytest.fixture(scope="module")
def iceberg_tables(schema) -> IcebergTableCollection:
    return schema.iceberg_tables


@pytest.fixture(scope="module")
def views(schema) -> ViewCollection:
    return schema.views


@pytest.fixture(scope="session")
def cortex_search_services(schema) -> CortexSearchServiceCollection:
    return schema.cortex_search_services


@pytest.fixture(scope="session")
def cortex_chat_services(root) -> CortexChatService:
    return root.cortex_chat_services


@pytest.fixture(scope="session")
def cortex_embed_service(root) -> CortexEmbedService:
    return root.cortex_embed_service


@pytest.fixture(scope="session")
def cortex_agent_services(root) -> CortexAgentService:
    return root.cortex_agent_services


@pytest.fixture(scope="session")
def event_tables(schema) -> EventTableCollection:
    return schema.event_tables


@pytest.fixture(scope="session")
def alerts(schema) -> AlertCollection:
    return schema.alerts


@pytest.fixture(scope="session")
def catalog_integrations(root) -> CatalogIntegration:
    return root.catalog_integrations


@pytest.fixture(scope="session")
def user_defined_functions(schema) -> UserDefinedFunctionCollection:
    return schema.user_defined_functions


@pytest.fixture(scope="session")
def imagerepo(connection, spcs_setup_objects) -> str:  # noqa: F811
    # When adding an inlined image repository YAML file, don't hard code the path to the test image
    # repository.  Instead, use this fixture and f-string this value in for the `{imagrepo}` substitution.
    # This way, there's only one thing to change across the entire test suite.
    # Legacy: return 'sfengineering-ss-lprpr-test2.registry
    #    .snowflakecomputing.com/testdb_python/public/ci_image_repository'
    with connection.cursor() as cursor:
        try:
            image_repos = cursor.execute(
                f"SHOW IMAGE REPOSITORIES IN SCHEMA {TEST_IMAGE_REPO_QUALIFIED_SCHEMA};"
            ).fetchall()
            assert TEST_IMAGE_REPO in [x[1].lower() for x in image_repos]
            return DEFAULT_IR_URL
        except Exception:
            cursor.execute(
                f"CREATE IMAGE REPOSITORY IF NOT EXISTS {TEST_IMAGE_REPO_QUALIFIED_SCHEMA}.{TEST_IMAGE_REPO};"
            )
            return cursor.execute(
                f"SHOW IMAGE REPOSITORIES LIKE '{TEST_IMAGE_REPO} IN SCHEMA {TEST_IMAGE_REPO_QUALIFIED_SCHEMA}';"
            ).fetchone()[4]

@pytest.fixture(scope="session")
def rest_connection(request, connection) -> RESTConnection:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        return request.getfixturevalue("connection_notebook")
    return RESTConnection(connection.host, connection.port, connection.rest.token, protocol=connection.rest._protocol)

@pytest.fixture(scope="session")
def spark_connect_session_resource(request, connection) -> SparkConnectResource:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        notebook_session = request.getfixturevalue("session_notebook")
        return SparkConnectResource(notebook_session)
    return SparkConnectResource(connection)

@pytest.fixture(scope="session")
def spark_connect_rest_resource(request, rest_connection) -> SparkConnectResource:
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        notebook_session = request.getfixturevalue("session_notebook")
        return SparkConnectResource(notebook_session)
    return SparkConnectResource(rest_connection)

@pytest.fixture
def setup_with_connector_execution(connection):
    @contextmanager
    def _setup(sqls_to_enable: list[StrictStr], sqls_to_disable: list[StrictStr]):
        with connection.cursor() as cursor:
            for sql in sqls_to_enable:
                cursor.execute(sql)

            try:
                yield
            finally:
                for sql in sqls_to_disable:
                    cursor.execute(sql)

    return _setup


@pytest.fixture(autouse=True)
# TODO: SNOW-1545034 make sure the role used here not hurt account
def use_accountadmin(connection, request):
    if "use_accountadmin" not in request.keywords:
        yield
        return

    with connection.cursor() as cursor, backup_role(cursor):
        try:
            cursor.execute("USE ROLE ACCOUNTADMIN")
        except Exception:
            pytest.xfail("Switch to role AccountAdmin failed")

        with suppress(Exception):
            yield


@pytest.fixture(scope="session")
def sf_cursor(connection, sf_connection_parameters, test_account, snowflake_version):
    sf_conn = None
    try:
        # We can only run this if the test is against a non-prod version (i.e., only run if dev/reg)
        if is_prod_version(snowflake_version) or sf_connection_parameters is None:
            yield None
        else:
            # return the cursor if we're already using the right account
            if test_account == SF_ACCOUNT:
                sf_conn = connection
            else:
                _keys = connection_keys()

                # switch to the snowflake account if connection config is available
                sf_conn = snowflake.connector.connect(
                    **{k: sf_connection_parameters[k] for k in _keys if k in sf_connection_parameters}
                )

            yield sf_conn.cursor()
    except snowflake.connector.Error:
        # We couldn't connect, yield None
        yield None
    finally:
        if sf_conn and test_account != SF_ACCOUNT:
            sf_conn.close()


@pytest.fixture(scope="session")
def sf_connection_parameters():
    # This does not work in notebooks
    if RUNNING_IN_NOTEBOOK or RUNNING_IN_STOREDPROC:
        yield None
    else:
        sf_connection_parameters = connection_config(connection_name="sf_account", error_if_not_exists=False)
        if sf_connection_parameters is None:
            yield None
        else:
            # Validate config; if the config isn't available, yield None
            if (
                "account" in sf_connection_parameters
                and sf_connection_parameters["account"].lower() == SF_ACCOUNT
                and "user" in sf_connection_parameters
                and "password" in sf_connection_parameters
            ):
                yield sf_connection_parameters
            else:
                yield None


@pytest.fixture(scope="session")
def require_sf(request, sf_cursor):
    if sf_cursor is None:
        pytest.skip("Skipping test because Snowflake account is required.")


@pytest.fixture
def set_internal_params(test_account, sf_cursor, require_sf):
    @contextmanager
    def _set_internal_params(parameters: dict[str, Any]):
        prefix = f"alter account {test_account}"

        # Warning: this will always unset the parameter to the default value,
        # only use this if that is ok.
        try:
            for k, v in parameters.items():
                sf_cursor.execute(f"{prefix} set {k} = {v};")
            yield
        finally:
            for k in parameters.keys():
                sf_cursor.execute(f"{prefix} unset {k};")

    return _set_internal_params


@pytest.fixture
def set_params(cursor):
    # Warning: this will always unset the parameters
    # to the default values without saving their previous settings;
    # only use this if that is ok.
    @contextmanager
    def _set_params(parameters: dict[str, Any], scope, target=""):
        prefix = f"alter {scope} {target}"

        try:
            for k, v in parameters.items():
                cursor.execute(f"{prefix} set {k} = {v};")
            yield
        finally:
            for k in parameters.keys():
                cursor.execute(f"{prefix} unset {k};")

    return _set_params


@pytest.fixture(autouse=True)
def internal_only(request, snowflake_version):
    if "internal_only" in request.keywords and is_prod_version(snowflake_version):
        pytest.skip("Test is skipped because it can only run in non-prod environments.")


@pytest.fixture(autouse=True)
def verify_test_environment_pollution(cursor):
    # Get the function name
    _before_database = cursor.execute("SELECT CURRENT_DATABASE()").fetchone()[0]
    _before_schema = cursor.execute("SELECT CURRENT_SCHEMA()").fetchone()[0]
    _before_warehouse = cursor.execute("SELECT CURRENT_WAREHOUSE()").fetchone()[0]
    _before_role = cursor.execute("SELECT CURRENT_ROLE()").fetchone()[0]

    # Yield nothing
    try:
        yield
    finally:
        _after_database = cursor.execute("SELECT CURRENT_DATABASE()").fetchone()[0]
        _after_schema = cursor.execute("SELECT CURRENT_SCHEMA()").fetchone()[0]
        _after_warehouse = cursor.execute("SELECT CURRENT_WAREHOUSE()").fetchone()[0]
        _after_role = cursor.execute("SELECT CURRENT_ROLE()").fetchone()[0]
        assert _before_database == _after_database
        assert _before_schema == _after_schema
        assert _before_warehouse == _after_warehouse
        assert _before_role == _after_role
