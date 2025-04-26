# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import os
import shutil
import tempfile
import typing

from contextlib import contextmanager

import snowflake.connector

from ..utils import is_prod_version, random_string


if typing.TYPE_CHECKING:
    from snowflake.snowpark import Row, Session


def random_object_name() -> str:
    return random_string(8, prefix="test_object_")


def get_task_history(session: "Session", name: str) -> list["Row"]:
    query = (
        f"select * from table(information_schema.task_history("
        f"scheduled_time_range_start=>dateadd('hour',-1,current_timestamp()),"
        f"result_limit => 10,task_name=>'{name}'))"
    )
    return session.sql(query).collect()


def string_skip_space_and_cases(s):
    return s.replace(" ", "").upper()


def array_equal_comparison(arr1, arr2):
    if not arr1 and not arr2:
        return True
    if not arr1 or not arr2:
        return False

    return [string_skip_space_and_cases(i) for i in arr1] == [string_skip_space_and_cases(i) for i in arr2]


def connection_config(override_schema=None, override_database=None, connection_name=None, error_if_not_exists=True):
    config = {}
    try:
        from ..parameters import CONNECTION_PARAMETERS
    except ImportError:
        CONNECTION_PARAMETERS = None
        from snowflake.connector.config_manager import CONFIG_MANAGER

    if CONNECTION_PARAMETERS is None:
        if connection_name is None:
            connection_key = CONFIG_MANAGER["default_connection_name"]
        else:
            connection_key = connection_name

        # 2023-06-23(warsaw): By default, we read out of the [connections.snowflake] section in the config.toml file,
        # but by setting the environment variable SNOWFLAKE_DEFAULT_CONNECTION_NAME you can read out of a different
        # section. For example SNOWFLAKE_DEFAULT_CONNECTION_NAME='test' reads out of [connections.test]
        if connection_key not in CONFIG_MANAGER["connections"]:
            if error_if_not_exists:
                raise KeyError("Connection config is missing.")
            else:
                return None

        config = CONFIG_MANAGER["connections"][connection_key]
    else:
        config = CONNECTION_PARAMETERS

    if override_schema:
        config["schema"] = override_schema
    if override_database:
        config["database"] = override_database
    return config


def should_disable_setup_for_spcs(config):
    return config.get("should_disable_setup_for_spcs", "") == "true"


def should_disable_setup_for_credentials(config):
    return config.get("should_disable_setup_for_credentials", "") == "true"


def get_snowflake_version(cursor):
    return cursor.execute("SELECT CURRENT_VERSION()").fetchone()[0].strip()


def connection_keys():
    return [
        "user",
        "password",
        "host",
        "port",
        "database",
        "schema",
        "account",
        "protocol",
        "role",
        "warehouse",
        "private_key_file",
        "private_key_file_pwd"
    ]


@contextmanager
def backup_role(cursor):
    _current_role = cursor.execute("SELECT /* use_role */ CURRENT_ROLE()").fetchone()[0]
    try:
        yield
    finally:
        if _current_role is not None:
            cursor.execute(f"USE ROLE /* use_role::reset */ {_current_role}").fetchone()


@contextmanager
def backup_database_and_schema(cursor):
    _current_database = cursor.execute("SELECT CURRENT_DATABASE()").fetchone()[0]
    _current_schema = cursor.execute("SELECT CURRENT_SCHEMA()").fetchone()[0]
    try:
        yield
    finally:
        if _current_database is not None:
            cursor.execute(f"USE DATABASE /* use_database::reset */ {_current_database}").fetchone()
        if _current_schema is not None:
            cursor.execute(f"USE SCHEMA /* use_schema::reset */ {_current_schema}").fetchone()


@contextmanager
def backup_warehouse(cursor):
    _current_warehouse = cursor.execute("SELECT CURRENT_WAREHOUSE()").fetchone()[0]
    try:
        yield _current_warehouse
    finally:
        if _current_warehouse is not None:
            cursor.execute(f"USE WAREHOUSE /* use_warehouse::reset */ {_current_warehouse}").fetchone()


def create_zip_from_paths(paths, output_filename):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            for path in paths:
                if os.path.isdir(path):
                    folder_name = os.path.basename(path)
                    temp_folder = os.path.join(temp_dir, folder_name)
                    shutil.copytree(path, temp_folder)
                elif os.path.isfile(path):
                    shutil.copy(path, temp_dir)
                else:
                    print(f"Warning: '{path}' is not a valid file or directory. Skipping.")

            shutil.make_archive(os.path.splitext(output_filename)[0], "zip", root_dir=temp_dir)
    except Exception as e:
        raise Exception(f"Error creating the snowflake core zip file:\n {e.with_traceback(None)}") from e


def create_and_use_new_database_and_schema(cursor, new_database_name, new_schema_name):
    # Database
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS /* setup_basic */ " f"{new_database_name} DATA_RETENTION_TIME_IN_DAYS=1",
    )
    cursor.execute(f"USE DATABASE {new_database_name}")

    # Schema
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {new_schema_name}")
    cursor.execute(f"USE SCHEMA {new_schema_name}")


def upload_given_files_to_stage(cursor, stage_url, files):
    try:
        for file in files:
            cursor.execute(f"PUT file://{file} @{stage_url} AUTO_COMPRESS=FALSE OVERWRITE=TRUE")
    except Exception as e:
        raise Exception(f"Error uploading files to the stage:\n {e.with_traceback(None)}") from e


def execute_notebook(cursor, notebook_name, stage_full_path, warehouse_name, notebook_file_name) -> bool:
    try:
        cursor.execute(
            f"CREATE OR REPLACE NOTEBOOK {notebook_name} "
            f"FROM '@{stage_full_path}' "
            f"MAIN_FILE = '{notebook_file_name}' QUERY_WAREHOUSE = {warehouse_name}"
        )
        cursor.execute(f"ALTER NOTEBOOK {notebook_name} ADD LIVE VERSION FROM LAST")
        cursor.execute(f"EXECUTE NOTEBOOK {notebook_name}()")
        return False
    except Exception as e:
        print(f"Error creating and executing the notebook file {notebook_file_name}:\n {e.with_traceback(None)}")
        return True


def setup_spcs(
    target_account_name=None,
    executing_account_cursor=None,
    instance_families_to_create=None,
):
    if instance_families_to_create is None:
        instance_families_to_create = ["FAKE"]
    if target_account_name is not None:
        prefix = f"alter account {target_account_name} "
    else:
        prefix = "alter account "
    executing_account_cursor.execute(f"{prefix} set snowservices_external_image_registry_allowlist = '*';").fetchone()
    executing_account_cursor.execute(f"{prefix} set enable_snowservices=true;").fetchone()
    executing_account_cursor.execute(f"{prefix} set enable_snowservices_user_facing_features=true;").fetchone()
    with backup_role(executing_account_cursor):
        executing_account_cursor.execute("use role sysadmin").fetchone()
        for instance in instance_families_to_create:
            executing_account_cursor.execute(
                f"call system$snowservices_create_instance_type('{instance}');"
            ).fetchone()[0]


def setup_credentials(cursor):
    add_cred_to_pool_cmd = {
        "AWS": f"""
            select system$creds_add_credentials_to_pool('COMMON_AWS_INTEGRATION',
            'AWS',
            '[{{"AWS_KEY_ID": "{os.environ["AWS_ACCESS_KEY_ID"]}",
                "AWS_SECRET_KEY": "{os.environ["AWS_SECRET_ACCESS_KEY"]}",
                "CREDENTIAL_NAME": "aws-creds",
                "CREDENTIAL_TYPE": "AWS_IAM_USER"}}]',
            '{{"PROVIDER_SPECIFIC_NAME":"AWS-specific data"}}')
        """,
        "AZURE": f"""
            select system$creds_add_credentials_to_pool('COMMON_AZURE_INTEGRATION',
            'AZURE',
            '[{{"AZURE_CLIENT_ID": "{os.environ["AZURE_AD_APP_CLIENT_ID"]}",
                "AZURE_CLIENT_SECRET": "{os.environ["AZURE_AD_APP_CLIENT_SECRET"]}",
                "CREDENTIAL_NAME": "azure-creds",
                "AZURE_TENANT_ID": "{os.environ["AZURE_AD_APP_TENANT_ID"]}",
                "CREDENTIAL_TYPE": "AZURE_APP"}}]',
            '{{"PROVIDER_SPECIFIC_NAME":"AZURE-specific data"}}')
        """,
        "GOOGLE": f"""
            select system$creds_add_credentials_to_pool('COMMON_GOOGLE_INTEGRATION',
            'GOOGLE',
            '[{{"GCS_SERVICE_ACCOUNT_KEY_BASE64": "{os.environ["SITE_GCS_SERVICE_ACCOUNT_KEY_BASE64"]}",
                "CREDENTIAL_NAME": "gcp-creds",
                "CREDENTIAL_TYPE": "GCP_SERVICE_ACCOUNT"}}]',
            '{{"PROVIDER_SPECIFIC_NAME":"GOOGLE-specific data"}}')
        """,
    }
    cursor.execute(add_cred_to_pool_cmd["AWS"])
    cursor.execute(add_cred_to_pool_cmd["AZURE"])
    cursor.execute(add_cred_to_pool_cmd["GOOGLE"])


def setup_account_for_notebook(cursor, config):
    # if it's a prod account there shouldn't be requirement to do this setup
    if is_prod_version(get_snowflake_version(cursor)):
        return

    sf_connection_parameters = connection_config(connection_name="sf_account", error_if_not_exists=False)

    if config["account"] != "snowflake" and sf_connection_parameters is None:
        raise Exception("Account is not snowflake or prod and sf_account connection parameters are not provided")

    if config["account"] == "snowflake":
        setup_spcs(
            executing_account_cursor=cursor,
            instance_families_to_create=["CPU_X64_XS", "FAKE"],
        )
        cursor.execute("ALTER ACCOUNT SET FEATURE_NOTEBOOKS_NON_INTERACTIVE_EXECUTION = 'ENABLED';")
        setup_credentials(cursor)
    else:
        _keys = connection_keys()
        with snowflake.connector.connect(
            **{k: sf_connection_parameters[k] for k in _keys if k in sf_connection_parameters}
        ) as sf_conn:
            target_account_name = config["account"]
            setup_spcs(
                executing_account_cursor=sf_conn.cursor(),
                target_account_name=target_account_name,
                instance_families_to_create=["CPU_X64_XS", "FAKE"],
            )
            sf_conn.cursor().execute(
                f"ALTER ACCOUNT {target_account_name} SET FEATURE_NOTEBOOKS_NON_INTERACTIVE_EXECUTION = 'ENABLED';"
            )
            setup_credentials(sf_conn.cursor())
