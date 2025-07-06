from cnvrgv2.modules.datasource import StorageTypes
import pytest
from cnvrgv2.config import GLOBAL_CNVRG_PATH
from pathlib import Path
import os
from dotenv import load_dotenv
from tests.long_running_tests.datasources.conftest import datasource_test_bukcet_name, datasource_test_region


class TestDatasourcesFilesOperations:
    storage_type = StorageTypes.S3
    storage_bucket_name = None
    storage_endpoint = None
    storage_region = None
    storage_credentials_user_rw = None
    storage_credentials_user_ro = None
    datasource_rw = None
    datasource_ro = None
    datasource_rw_no_path = None
    config_env_vars = ['DATASOURCE_TEST_USER_RW_ACCESS_KEY_ID', 'DATASOURCE_TEST_USER_RW_SECRET_ACCESS_KEY',
                       'DATASOURCE_TEST_USER_RO_ACCESS_KEY_ID', 'DATASOURCE_TEST_USER_RO_SECRET_ACCESS_KEY']

    @classmethod
    def set_datasource_aws_config(cls):
        # Path to the AWS config file
        config_file = os.path.join(GLOBAL_CNVRG_PATH, '.env')

        # load from config file if running locally.
        # Env vars should exist when running through github actions
        if Path(config_file).is_file():
            load_dotenv(config_file)

        bucket_name = datasource_test_bukcet_name
        region = datasource_test_region
        user1_access_key_id = os.getenv(key='DATASOURCE_TEST_USER_RW_ACCESS_KEY_ID')
        user1_secret_access_key = os.getenv(key='DATASOURCE_TEST_USER_RW_SECRET_ACCESS_KEY')
        user2_access_key_id = os.getenv(key='DATASOURCE_TEST_USER_RO_ACCESS_KEY_ID')
        user2_secret_access_key = os.getenv(key='DATASOURCE_TEST_USER_RO_SECRET_ACCESS_KEY')

        cls.storage_bucket_name = bucket_name
        cls.storage_region = region
        cls.storage_credentials_user_rw = {
            "access_key_id": user1_access_key_id,
            "secret_access_key": user1_secret_access_key
        }
        cls.storage_credentials_user_ro = {
            "access_key_id": user2_access_key_id,
            "secret_access_key": user2_secret_access_key
        }

    @classmethod
    def create_datasources(cls, class_context, e2e_client):
        path = class_context.generate_name(5)
        cls.datasource_rw = e2e_client.datasources.create(name=class_context.generate_name(5),
                                                          storage_type=cls.storage_type,
                                                          path=path,
                                                          bucket_name=cls.storage_bucket_name,
                                                          region=cls.storage_region,
                                                          credentials=cls.storage_credentials_user_rw)
        cls.datasource_rw_no_path = e2e_client.datasources.create(name=class_context.generate_name(5),
                                                                  storage_type=cls.storage_type,
                                                                  bucket_name=cls.storage_bucket_name,
                                                                  region=cls.storage_region,
                                                                  credentials=cls.storage_credentials_user_rw)

        cls.datasource_ro = e2e_client.datasources.create(name=class_context.generate_name(5),
                                                          storage_type=cls.storage_type,
                                                          path=path,
                                                          bucket_name=cls.storage_bucket_name,
                                                          region=cls.storage_region,
                                                          credentials=cls.storage_credentials_user_ro)

    @classmethod
    def clear_env(cls):
        # Clear env varaiables
        for variable_name in cls.config_env_vars:
            if variable_name in os.environ:
                os.environ.pop(variable_name)

    @classmethod
    def clear_bucket_path(cls):
        cls.remove_files(datasource=cls.datasource_rw)

    @classmethod
    @pytest.fixture(scope='class', autouse=True)
    def setup_and_teardown_class(cls, class_context, e2e_client):
        # Setup Class - Executed once per test class
        cls.set_datasource_aws_config()
        # Skip tests if config is missing
        if any(var is None for var in [cls.storage_bucket_name, cls.storage_region,
                                       cls.storage_credentials_user_rw['access_key_id'],
                                       cls.storage_credentials_user_rw['secret_access_key'],
                                       cls.storage_credentials_user_ro['access_key_id'],
                                       cls.storage_credentials_user_ro['secret_access_key']]):
            pytest.skip("Skipping tests due to CONFIGURATION MISSING")
        cls.create_datasources(class_context, e2e_client)
        yield
        # Teardown Class - Executed once after all test methods in the class
        cls.clear_env()
        # Every test should clear up the path,
        # but we also clear path in teardown in case some tests fail before they clear up.
        cls.clear_bucket_path()

    # region Helpers
    def count_paginator(self, paginator):
        file_count = 0
        for page in paginator:
            for file_name in page:
                file_count += 1
        return file_count

    @classmethod
    def remove_files(self, datasource):
        paginator = datasource.list_objects()
        for page in paginator:
            for file_name in page:
                datasource.remove_file(file_name)
    # endregion
