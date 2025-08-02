from collections.abc import Iterator
from contextlib import suppress
from io import BytesIO
from textwrap import dedent

import pytest

import snowflake.connector

from snowflake.core import Root
from snowflake.core.compute_pool import ComputePool
from snowflake.core.database import Database, DatabaseCollection, DatabaseResource
from snowflake.core.exceptions import NotFoundError
from snowflake.core.image_repository import ImageRepository
from snowflake.core.schema import Schema, SchemaResource
from snowflake.core.service import Service, ServiceResource, ServiceSpecInlineText, ServiceSpecStageFile
from snowflake.core.stage import Stage, StageDirectoryTable, StageEncryption, StageResource
from snowflake.core.table import Table, TableColumn, TableResource

from ..utils import backup_role, random_string
from .constants import TEST_SCHEMA


@pytest.fixture(scope="session", autouse=True)
def test_schema() -> str:
    """Set up and tear down the test schema. This is automatically called per test session."""
    return TEST_SCHEMA


@pytest.fixture
def temp_ir(image_repositories) -> Iterator[ImageRepository]:
    ir_name = random_string(5, "test_ir_")
    test_ir = ImageRepository(
        name=ir_name
        # TODO: comment is not supported by image repositories?
        # comment="created by temp_ir",
    )
    image_repositories.create(test_ir)
    try:
        yield test_ir
    finally:
        image_repositories[test_ir.name].drop()


@pytest.fixture
def temp_cp(compute_pools, instance_family) -> Iterator[ComputePool]:
    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=1,
        auto_resume=False,
        comment="created by temp_cp",
    )
    compute_pools.create(test_cp, initially_suspended=True)
    try:
        yield test_cp
    finally:
        compute_pools[test_cp.name].drop()


@pytest.fixture
def temp_service(root, services, session, imagerepo, shared_compute_pool) -> Iterator[ServiceResource]:
    stage_name = random_string(5, "test_stage_")
    s_name = random_string(5, "test_service_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    spec = f"@{stage_name}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(
                f"""
                spec:
                  containers:
                  - name: hello-world
                    image: {imagerepo}/hello-world:latest
                  endpoints:
                  - name: default
                    port: 8080
                 """
            ).encode()
        ),
        spec,
    )
    test_s = Service(
        name=s_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service",
    )
    s = services.create(test_s)

    try:
        yield s
    finally:
        s.drop()


@pytest.fixture
def temp_service_from_spec_inline(root, services, session, imagerepo, shared_compute_pool) -> Iterator[ServiceResource]:
    s_name = random_string(5, "test_service_")
    inline_spec = dedent(
        f"""
        spec:
          containers:
          - name: hello-world
            image: {imagerepo}/hello-world:latest
         """
    )
    test_s = Service(
        name=s_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecInlineText(spec_text=inline_spec),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service_from_spec_inline",
    )
    s = services.create(test_s)
    try:
        yield test_s
    finally:
        s.drop()


@pytest.fixture
def temp_db(databases: DatabaseCollection, backup_database_schema) -> Iterator[DatabaseResource]:
    del backup_database_schema
    # create temp database
    db_name = random_string(5, "test_database_")
    test_db = Database(name=db_name, comment="created by temp_db")
    db = databases.create(test_db)
    try:
        yield db
    finally:
        db.drop()


@pytest.fixture
def temp_db_case_sensitive(databases: DatabaseCollection, backup_database_schema) -> Iterator[DatabaseResource]:
    del backup_database_schema
    # create temp database
    db_name = random_string(5, "test_database_case_sensitive_")
    db_name_case_sensitive = '"' + db_name + '"'
    test_db = Database(name=db_name_case_sensitive, comment="created by temp_case_sensitive_db")
    db = databases.create(test_db)
    try:
        yield db
    finally:
        db.drop()


@pytest.fixture
def temp_schema(schemas, backup_database_schema) -> SchemaResource:
    del backup_database_schema
    schema_name = random_string(5, "test_schema_")
    test_schema = Schema(name=schema_name, comment="created by temp_schema")
    sc = schemas.create(test_schema)
    try:
        yield sc
    finally:
        sc.drop()


@pytest.fixture
def temp_schema_case_sensitive(schemas, backup_database_schema) -> Iterator[SchemaResource]:
    del backup_database_schema
    schema_name = random_string(5, "test_schema_case_sensitive_")
    schema_name_case_sensitive = '"' + schema_name + '"'
    test_schema = Schema(name=schema_name_case_sensitive, comment="created by temp_schema_case_sensitive")
    sc = schemas.create(test_schema)
    try:
        yield sc
    finally:
        sc.drop()


@pytest.fixture(scope="session")
def temp_customer_organization(require_sf, sf_cursor) -> str:
    org_name = random_string(5, "testorg")
    with backup_role(sf_cursor):
        sf_cursor.execute("use role accountadmin;")
        sf_cursor.execute(
            f"CREATE ORGANIZATION {org_name} SALESFORCE_ID='new_salesforce_id' "
            "REGION_GROUPS=PUBLIC ORGANIZATION_TYPE='customer';"
        )
        try:
            yield org_name
        finally:
            sf_cursor.execute(f"DROP ORGANIZATION {org_name};")


@pytest.fixture(scope="session")
def temp_customer_account_with_org_admin(require_sf, temp_customer_organization, sf_cursor) -> str:
    with backup_role(sf_cursor):
        sf_cursor.execute("use role accountadmin;")
        sf_cursor.execute("alter session set QA_MODE=true;")
        account_name = random_string(5, "test_orgadmin_account_")
        blank_account_name = random_string(5, "test_blank_account_")
        sf_cursor.execute(f"CREATE ACCOUNT {blank_account_name} server_type=standard type=blank;")
        sf_cursor.execute(
            f"CREATE ACCOUNT {account_name} admin_name=admin admin_password='TestPassword1' "
            f"type=customer must_change_password=false organization={temp_customer_organization};"
        )
        sf_cursor.execute(f"call system$add_org_admin_to_account('{account_name.upper()}');")
        sf_cursor.execute(f"call system$it('GRANT_ORGADMIN_TO_ACCOUNTADMIN', '{account_name.upper()}');")
        sf_cursor.execute("alter session unset QA_MODE;")
        try:
            yield account_name
        finally:
            sf_cursor.execute(f"DROP ACCOUNT {account_name.upper()};")


@pytest.fixture(scope="session")
def temp_customer_account_root(temp_customer_account_with_org_admin) -> Root:
    with snowflake.connector.connect(
        **{
            "account": f"{temp_customer_account_with_org_admin}",
            "user": "admin",
            "password": "TestPassword1",
            "protocol": "http",
            "port": 8082,
            "host": f"{temp_customer_account_with_org_admin}.reg.local",
        }
    ) as connection:
        yield Root(connection)


@pytest.fixture(scope="session")
def temp_customer_account_cursor(temp_customer_account_root):
    return temp_customer_account_root._connection.cursor()


@pytest.fixture
def temp_stage(stages) -> Iterator[StageResource]:
    stage_name = random_string(5, "test_stage_")
    test_stage = Stage(name=stage_name, comment="created by temp_stage")
    st = stages.create(test_stage)
    try:
        yield st
    finally:
        st.drop()


@pytest.fixture
def temp_stage_case_sensitive(stages) -> Iterator[StageResource]:
    stage_name = random_string(5, "test_stage_case_sensitive_")
    stage_name_case_sensitive = '"' + stage_name + '"'
    test_stage = Stage(name=stage_name_case_sensitive, comment="created by temp_stage")
    st = stages.create(test_stage)
    try:
        yield st
    finally:
        st.drop()


@pytest.fixture
def temp_table(tables) -> Iterator[TableResource]:
    table_name = random_string(5, "test_table_case_insensitive_")
    columns = [TableColumn(name="col1", datatype="int"), TableColumn(name="col2", datatype="string")]
    test_table = Table(name=table_name, columns=columns)
    test_table_handle = tables.create(test_table)
    try:
        yield test_table_handle
    finally:
        with suppress(NotFoundError):
            test_table_handle.drop()


@pytest.fixture
def temp_directory_table(stages) -> Iterator[StageResource]:
    new_stage = Stage(
        name=random_string(5, "test_directory_table_"),
        encryption=StageEncryption(type="SNOWFLAKE_SSE"),
        directory_table=StageDirectoryTable(enable=True),
    )
    st = stages.create(new_stage)

    try:
        yield st
    finally:
        st.drop()
