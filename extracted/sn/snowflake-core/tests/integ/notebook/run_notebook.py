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
    execute_notebook,
    setup_account_for_notebook,
    upload_given_files_to_stage,
)


TEST_DATABASE_NAME = "DATABASE_PYTHON_TESTING_NOTEBOOK"
TEST_SCHEMA = "GH_JOB_{}".format(str(uuid.uuid4()).replace("-", "_"))
STAGE_NAME = "STAGE_PYTHON_TEST_NOTEBOOK"

all_notebook_files = [
    {
        "notebook_name": "python_test_notebook",
        "notebook_file_name": "python_test_notebook.ipynb",
        "have_output_file": True,
        "is_integration_test": True,
    },
    {
        "notebook_name": "doc_notebook_1",
        "notebook_file_name": "doc_notebook_1.ipynb",
        "have_output_file": False,
    },
]


def run():
    execution_output = None
    config = connection_config()
    should_fail_job = False

    # copy the snowpy package to the tests/integ/notebook folder
    snowflake_core_source_folder = "./src"
    snowflake_core_test_folder = "./tests"
    snowflake_core_pyproject_file_path = "./pyproject.toml"
    notebook_directory_path = "tests/integ/notebook"
    snowflake_core_zip_filename = "snowflake_core.zip"
    notebook_env_file_name = "environment.yml"
    notebook_execution_output_file_name = "execution_output.txt"
    snowflake_core_zip_filepath = f"{notebook_directory_path}/{snowflake_core_zip_filename}"

    # create the zip file
    create_zip_from_paths(
        [snowflake_core_source_folder, snowflake_core_test_folder, snowflake_core_pyproject_file_path],
        snowflake_core_zip_filepath,
    )

    _keys = connection_keys()

    with snowflake.connector.connect(
        # This works around SNOW-998521, by forcing JSON results
        **{k: config[k] for k in _keys if k in config}
    ) as connection:
        cursor = connection.cursor()

        # Set up account for notebook
        setup_account_for_notebook(cursor, config)

        with backup_database_and_schema(cursor), backup_warehouse(cursor), backup_role(cursor):
            try:
                create_and_use_new_database_and_schema(cursor, TEST_DATABASE_NAME, TEST_SCHEMA)
                warehouse_name = config["warehouse"]

                # create the stage and put the notebook files in the stage
                cursor.execute(f"CREATE STAGE {STAGE_NAME}")
                for notebook_file in all_notebook_files:
                    stage_url = f"{STAGE_NAME}/{notebook_file['notebook_name']}"
                    files_to_upload = [
                        f"{notebook_directory_path}/{notebook_file['notebook_file_name']}",
                        f"{notebook_directory_path}/{notebook_env_file_name}",
                    ]
                    upload_given_files_to_stage(cursor, stage_url, files_to_upload)

                upload_given_files_to_stage(cursor, f"{STAGE_NAME}/zip", [snowflake_core_zip_filepath])

                # try to create and execute the notebook
                for notebook_file in all_notebook_files:
                    print(f"Executing notebook {notebook_file['notebook_file_name']}")
                    should_fail_job_temp = execute_notebook(
                        cursor,
                        notebook_file["notebook_name"],
                        f"{TEST_DATABASE_NAME}.{TEST_SCHEMA}.{STAGE_NAME}/{notebook_file['notebook_name']}",
                        warehouse_name,
                        notebook_file["notebook_file_name"],
                    )
                    should_fail_job = should_fail_job or should_fail_job_temp
                    # fetch the output of the notebook execution and read
                    notebook_execution_output_file_name = f"{notebook_file['notebook_name']}_output.txt"
                    if notebook_file["have_output_file"]:
                        source_path = f"{TEST_DATABASE_NAME}.{TEST_SCHEMA}.{STAGE_NAME}/{notebook_file['notebook_name']}/{notebook_execution_output_file_name}"  # noqa: E501
                        target_directory = f"{notebook_directory_path}"
                        # download the output file
                        try:
                            cursor.execute(f"GET @{source_path} file://{target_directory}")
                        except Exception as e:
                            print(
                                f"Error downloading the notebook {notebook_file['notebook_file_name']}:\n {e.with_traceback(None)}"  # noqa: E501
                            )
                            should_fail_job = True
                            continue
                        # read the output file
                        try:
                            output_file_name = f"{target_directory}/{notebook_execution_output_file_name}"
                            with open(f"{output_file_name}") as f:
                                execution_output = f.read()
                                print(f"Notebook {notebook_file['notebook_name']} Output::::::STARTS")
                                print(execution_output)
                                print(f"Notebook {notebook_file['notebook_name']} Output::::::ENDS")
                        except Exception as e:
                            print(
                                f"Error reading the notebook {notebook_file['notebook_file_name']}:\n {e.with_traceback(None)}"  # noqa: E501
                            )
                            should_fail_job = True
                            continue
                        if notebook_file["is_integration_test"]:
                            if not (execution_output.find("All tests passed") != -1):
                                print("Some Integration test are failing")
                                should_fail_job = True
            finally:
                cursor.execute(f"USE DATABASE {TEST_DATABASE_NAME}")
                cursor.execute(f"USE SCHEMA {TEST_SCHEMA}")
                cursor.execute("DROP NOTEBOOK IF EXISTS python_test_notebook")
                cursor.execute(f"DROP STAGE IF EXISTS {STAGE_NAME}")
                cursor.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA}")
    if should_fail_job:
        raise Exception("Job Failed")


if __name__ == "__main__":
    run()
