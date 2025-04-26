import uuid

import snowflake.connector

from ..utils import (
    backup_database_and_schema,
    backup_role,
    backup_warehouse,
    connection_config,
    connection_keys,
    create_and_use_new_database_and_schema,
    create_zip_from_paths,
    upload_given_files_to_stage,
)


TEST_DATABASE_NAME = "DATABASE_PYTHON_TESTING_STOREDPROC"
TEST_SCHEMA = "GH_JOB_{}".format(str(uuid.uuid4()).replace("-", "_"))
STAGE_NAME = "STAGE_PYTHON_TEST_STOREDPROC"


storedproc_create_sql = """
CREATE OR REPLACE PROCEDURE testing_storedproc()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python', 'asn1crypto','atpublic','certifi','cffi','charset-normalizer','cryptography','docker-py','filelock','idna','packaging','platformdirs','pycparser','pydantic','pyjwt','pyopenssl','pytest','pytest-cov','python-dateutil','urllib3','tomlkit','sortedcontainers')
HANDLER = 'run_integration_test'
execute as caller
AS
$$
def run_integration_test(session):
    import sys
    import traceback

    output_file_path = "/tmp/execution_output.txt"
    snowlfake_core_zip_file_name = "snowflake_core.zip"
    stage_name = "STAGE_PYTHON_TEST_STOREDPROC"

    with open(output_file_path, "w") as f:
        sys.stdout = f
        sys.stderr = f
        try:
            import zipfile
            import os
            import pytest
            import pytest_cov

            os.environ["RUNNING_IN_STOREDPROC"] = "True"
            os.environ["PYTHONUNBUFFERED"] = "1"
            should_enable_logging = (os.environ.get("ENABLE_DEBUG_LOGGING_IN_SNOWPY") == "True")

            def clear_modules(prefix):
                for module_name in list(sys.modules.keys()):
                    if module_name.startswith(prefix):
                        del sys.modules[module_name]

            clear_modules("snowflake.core")

            get_status = session.file.get(f"@{stage_name}/zip/{snowlfake_core_zip_file_name}", "/tmp/zip")
            if len(get_status) != 1:
                raise Exception("not able to load the snowflake_core")

            with zipfile.ZipFile(f"/tmp/zip/{snowlfake_core_zip_file_name}", "r") as zip_ref:
                zip_ref.extractall("/tmp/expanded/snowflake_core")
            sys.path.insert(0, "/tmp/expanded/snowflake_core/src")
            print("Successfully completed the set up for executing the integration test in storedproc")
            try:
                if should_enable_logging:
                    import logging
                    import pathlib
                    import snowflake.core
                    snowflake.core.simple_file_logging(
                        path=pathlib.Path("execution_output.txt"),
                        level=logging.DEBUG,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    )
                exit_code = pytest.main(
                    ["/tmp/expanded/snowflake_core/tests/integ", "-W", "ignore", "-r", "a", "--no-cov", "-v", "-m", "not flaky"]
                )
                if exit_code != 0:
                    print("Some tests failed")
                else:
                    print("All tests passed")
                print("Successfully executed integration test in storedproc")
            except Exception as e:
                traceback.print_exc(file=f)
                print("Failed to execute integration test in storedproc")
        except Exception as e:
            traceback.print_exc(file=f)
            print("Failed to complete the set up for executing the integration test in storedproc")

    put_result = session.file.put(output_file_path, f"@{stage_name}", auto_compress=False)
$$;

"""  # noqa: E501


def run():
    execution_output = None
    config = connection_config()

    # copy the snowpy package to the tests/integ/storedproc folder
    snowflake_core_source_folder = "./src"
    snowflake_core_test_folder = "./tests"
    snowflake_core_pyproject_file_path = "./pyproject.toml"
    storedproc_directory_path = "tests/integ/storedproc"
    snowflake_core_zip_filename = "snowflake_core.zip"
    storedproc_execution_output_file_name = "execution_output.txt"
    snowflake_core_zip_filepath = f"{storedproc_directory_path}/{snowflake_core_zip_filename}"

    # create the zip file
    create_zip_from_paths(
        [snowflake_core_source_folder, snowflake_core_test_folder, snowflake_core_pyproject_file_path],
        snowflake_core_zip_filepath,
    )

    _keys = connection_keys()

    with snowflake.connector.connect(**{k: config[k] for k in _keys if k in config}) as connection:
        cursor = connection.cursor()
        with backup_database_and_schema(cursor), backup_warehouse(cursor), backup_role(cursor):
            try:
                create_and_use_new_database_and_schema(cursor, TEST_DATABASE_NAME, TEST_SCHEMA)

                # create the stage and put the files in the stage
                cursor.execute(f"CREATE STAGE {STAGE_NAME}")
                upload_given_files_to_stage(cursor, f"{STAGE_NAME}/zip", [snowflake_core_zip_filepath])

                # try to create and execute the storedproc
                try:
                    cursor.execute(storedproc_create_sql)
                    cursor.execute("call testing_storedproc()")
                except Exception as e:
                    print(f"Error creating and executing the storedproc: {e.with_traceback(None)}")

                # fetch the output of the storedproc execution
                try:
                    # need to specify full Stage name if tests mess up the current database and schema
                    cursor.execute(
                        f"GET @{TEST_DATABASE_NAME}.{TEST_SCHEMA}.{STAGE_NAME}/{storedproc_execution_output_file_name} file://{storedproc_directory_path}/"
                    )
                    storedproc_execution_output_file_path = (
                        f"{storedproc_directory_path}/{storedproc_execution_output_file_name}"
                    )
                    with open(f"{storedproc_execution_output_file_path}") as f:
                        execution_output = f.read()
                except Exception as e:
                    raise Exception(f"Error reading the storedproc output: {e.with_traceback(None)}") from e

                # read the execution output
                print("Storedproc Output::::::STARTS")
                print(execution_output)
                if not (execution_output.find("All tests passed") != -1):
                    raise Exception("Some Integration test are failing")
                print("Storedproc Output::::::ENDS")
            finally:
                cursor.execute(f"USE DATABASE {TEST_DATABASE_NAME}")
                cursor.execute(f"USE SCHEMA {TEST_SCHEMA}")
                cursor.execute("DROP PROCEDURE IF EXISTS testing_storedproc()")
                cursor.execute(f"DROP STAGE  IF EXISTS {STAGE_NAME}")
                cursor.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA}")


if __name__ == "__main__":
    run()
