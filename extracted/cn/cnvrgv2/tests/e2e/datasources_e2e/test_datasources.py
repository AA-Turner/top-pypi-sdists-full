from cnvrgv2.errors import CnvrgHttpError, CnvrgArgumentsError
from cnvrgv2.modules.datasource import Datasource, StorageTypes
from cnvrgv2.config import GLOBAL_CNVRG_PATH, error_messages
from pathlib import Path
import os
from dotenv import load_dotenv
import pytest
from tests.e2e.conftest import call_database
from tests.long_running_tests.datasources.conftest import datasource_test_bukcet_name, datasource_test_region
from cnvrgv2.cnvrg import Cnvrg


class TestDatasources:
    storage_type = StorageTypes.S3
    storage_bucket_name = None
    storage_endpoint = None
    storage_region = None
    storage_path = None
    storage_credentials_user_rw = None
    storage_credentials_user_ro = None
    datasource_rw = None
    datasource_ro = None
    config_env_vars = ['DATASOURCE_TEST_BUCKET_NAME', 'DATASOURCE_TEST_REGION',
                       'DATASOURCE_TEST_USER_RW_ACCESS_KEY_ID', 'DATASOURCE_TEST_USER_RW_SECRET_ACCESS_KEY',
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
        cls.storage_path = path + '/'
        cls.datasource_rw = e2e_client.datasources.create(name=class_context.generate_name(5),
                                                          storage_type=cls.storage_type,
                                                          path=path,
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
        for variable_name in cls.config_env_vars:
            if variable_name in os.environ:
                os.environ.pop(variable_name)

    @classmethod
    def clear_bucket(cls):
        cls.datasource_rw.remove_file(cls.datasource_rw.path)

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

    @staticmethod
    def cleanup(context_prefix):
        # Clean Data Sources by name, will clean all data sources where name starts with the class prefix
        # Create name with : class_context.generate_name(5)
        delete_user_command = "DELETE FROM datasources WHERE name LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    # region Create
    def test_create_private(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        count_before = e2e_client.datasources.list_count(sort="id")
        new_datasource = self.create_random_datasource(e2e_client, name, credentials=self.storage_credentials_user_ro)
        count_after = e2e_client.datasources.list_count(sort="id")

        datasource = e2e_client.datasources.get(slug=new_datasource.slug)
        assert datasource is not None
        assert datasource.slug == new_datasource.slug
        assert count_after is count_before + 1

        assert type(datasource) == Datasource
        assert datasource.name == name
        assert datasource.storage_type == self.storage_type.value
        assert datasource.bucket_name == self.storage_bucket_name
        assert datasource.path == self.storage_path
        assert datasource.endpoint == self.storage_endpoint
        assert datasource.region == self.storage_region
        assert datasource.public is False

    def test_create_public(self, class_context, e2e_client):
        # We create names with class prefix so that the cleanup will find them.
        name = class_context.generate_name(5)
        count_before = e2e_client.datasources.list_count(sort="id")
        new_datasource = self.create_random_datasource(e2e_client, name, public=True,
                                                       credentials=self.storage_credentials_user_ro)
        count_after = e2e_client.datasources.list_count(sort="id")

        datasource = e2e_client.datasources.get(slug=new_datasource.slug)
        assert datasource is not None
        assert datasource.slug == new_datasource.slug
        assert count_after is count_before + 1

        assert type(datasource) == Datasource
        assert datasource.name == name
        assert datasource.storage_type == self.storage_type.value
        assert datasource.bucket_name == self.storage_bucket_name
        assert datasource.path == self.storage_path
        assert datasource.endpoint == self.storage_endpoint
        assert datasource.region == self.storage_region
        assert datasource.public is True

    def test_create_unauthorized_for_non_admin_user(self, domain, class_context, e2e_client, e2e_data_scientist_user):
        # We create names with class prefix so that the cleanup will find them.
        name = class_context.generate_name(5)
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )
        with pytest.raises(CnvrgHttpError) as exception_info:
            client_of_non_admin_user.datasources.create(name=name,
                                                        storage_type=self.storage_type,
                                                        bucket_name=self.storage_bucket_name,
                                                        region=self.storage_region,
                                                        credentials=self.storage_credentials_user_ro)
        assert 'Unauthorized' in str(exception_info.value)

    def test_create_missing_mandatory_field(self, e2e_client):
        with pytest.raises(TypeError) as exception_info:
            e2e_client.datasources.create()
        assert "required positional argument" in str(exception_info.value)
        assert "name" in str(exception_info.value)
        assert "storage_type" in str(exception_info.value)
        assert "bucket_name" in str(exception_info.value)
        assert "credentials" in str(exception_info.value)
        assert "region" in str(exception_info.value)

    def test_create_faulty_params(self, class_context, e2e_client):
        # Faulty name (not str)
        # sdk validation error
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            self.create_random_datasource(e2e_client,
                                          name=123)
        assert "name" in str(exception_info.value)
        assert "not a valid" in str(exception_info.value)

        # Faulty name (special chars)
        # server validation error
        # with pytest.raises(CnvrgHttpError) as exception_info:
        #     e2e_client.datasources.create(storage_type=self.storage_type,
        #                                   name="test@#$%^&",
        #                                   bucket_name=self.storage_bucket_name,
        #                                   path=self.storage_path,
        #                                   region=self.storage_region,
        #                                   credentials=self.storage_credentials_user_rw)
        # assert "Invalid Input" in str(exception_info.value.args)
        # assert exception_info.value.status_code == unprocessable_entity_status_code
        # Faulty bucket name (not str)
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            e2e_client.datasources.create(storage_type=self.storage_type,
                                          name=class_context.generate_name(5),
                                          bucket_name=123,
                                          path=self.storage_path,
                                          region=self.storage_region,
                                          credentials=self.storage_credentials_user_rw)

    def test_create_fails_for_duplicate_name(self, class_context, e2e_client):
        # We create names with class prefix so that the cleanup will find them.
        name = class_context.generate_name(5)
        e2e_client.datasources.create(name=name,
                                      storage_type=self.storage_type,
                                      bucket_name=self.storage_bucket_name,
                                      region=self.storage_region,
                                      credentials=self.storage_credentials_user_rw)
        with pytest.raises(CnvrgHttpError) as exception_info:
            e2e_client.datasources.create(name=name,
                                          storage_type=self.storage_type,
                                          bucket_name=self.storage_bucket_name,
                                          path=self.storage_path,
                                          region=self.storage_region,
                                          credentials=self.storage_credentials_user_rw)
        assert "already exists" in str(exception_info.value)

    # region test validity of users

    def test_create_and_assign_not_authorized_collaborator_should_throw_error_and_not_create_datasource(self,
                                                                                                        class_context,
                                                                                                        e2e_client,
                                                                                                        e2e_user,
                                                                                                        e2e_temp_user):

        # Get count (as admin)
        count_before = e2e_client.datasources.list_count(sort="id")

        # Creating a data source with unauthorized users should throw an error with emails of unauthorized users only.
        # And not create a new data source
        with pytest.raises(CnvrgHttpError) as exception_info:
            self.create_random_datasource(e2e_client,
                                          name=class_context.generate_name(5),
                                          collaborators=['manager_role17@test.com',
                                                         'fake@user.com',
                                                         e2e_temp_user['email']],
                                          credentials=self.storage_credentials_user_rw)

        assert 'manager_role17@test.com, fake@user.com' in str(exception_info.value)
        assert e2e_user['email'] not in str(exception_info.value)

        assert e2e_client.datasources.list_count(sort="id") is count_before

    def test_create_and_assign_authorized_collaborator(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        datasource = self.create_random_datasource(e2e_client,
                                                   name=class_context.generate_name(5),
                                                   collaborators=[e2e_temp_user['email']],
                                                   credentials=self.storage_credentials_user_rw)

        # Collaborators should include the user who created the data source + users params (e2e_temp_user)
        assert len(datasource.collaborators) == 2
        assert e2e_user['email'] in datasource.collaborators
        assert e2e_temp_user['email'] in datasource.collaborators

    def test_create_no_collaborators(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        datasource = self.create_random_datasource(e2e_client,
                                                   name=class_context.generate_name(5),
                                                   credentials=self.storage_credentials_user_rw)

        # Collaborators should include the user who created the data source only.
        assert len(datasource.collaborators) == 1
        assert e2e_user['email'] in datasource.collaborators

    def test_create_and_assign_admin_as_collaborator(self, class_context, e2e_client, e2e_user):
        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        datasource = self.create_random_datasource(e2e_client,
                                                   name=class_context.generate_name(5),
                                                   collaborators=[e2e_user['email']],
                                                   credentials=self.storage_credentials_user_rw)

        # Datasource collaborators = admin + users.
        # e2e_user is the owner of the datasource. It should not be added as user too.
        # Meaning it should appear once in the list of collaborators.
        assert len(datasource.collaborators) == 1
        assert e2e_user['email'] in datasource.collaborators

    # endregion

    # region test validity of credentials
    def test_credentials_format(self, class_context, e2e_client):
        # We create names with class prefix so that the cleanup will find them.
        name = class_context.generate_name(5)

        storage_credentials = {"access_key": "aaa", "secret_access": "bbb"}
        with pytest.raises(CnvrgHttpError) as exception_info:
            e2e_client.datasources.create(name=name,
                                          storage_type=self.storage_type,
                                          region=self.storage_region,
                                          bucket_name=self.storage_bucket_name,
                                          credentials=storage_credentials,
                                          )

        assert "Credentials not valid" in str(exception_info.value)

        storage_credentials = {"access_key_id": "aaa"}
        with pytest.raises(CnvrgHttpError) as exception_info:
            e2e_client.datasources.create(name=name,
                                          storage_type=self.storage_type,
                                          region=self.storage_region,
                                          bucket_name=self.storage_bucket_name,
                                          credentials=storage_credentials)

        assert "Credentials not valid" in str(exception_info.value)

    # endregion

    # endregion

    # region Get

    def test_get(self, class_context, e2e_client):
        # We create names with class prefix so that the cleanup will find them.
        name = class_context.generate_name(5)

        datasource = self.create_random_datasource(e2e_client,
                                                   name,
                                                   credentials=self.storage_credentials_user_ro)

        datasource = e2e_client.datasources.get(slug=datasource.slug)
        assert type(datasource) == Datasource
        assert datasource.name == name
        assert datasource.storage_type == self.storage_type.value
        assert datasource.bucket_name == self.storage_bucket_name
        assert datasource.path == self.storage_path

    def test_get_faulty_slug(self, class_context, e2e_client):
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            e2e_client.datasources.get(slug=123)
        assert error_messages.DATASOURCE_GET_FAULTY_SLUG in str(exception_info.value)

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            e2e_client.datasources.get(slug=None)
        assert error_messages.DATASOURCE_GET_FAULTY_SLUG in str(exception_info.value)

    def test_get_non_existent(self, class_context, e2e_client):
        # We create names with class prefix so that the cleanup will find them.
        name = class_context.generate_name(5)

        with pytest.raises(CnvrgHttpError) as exception_info:
            e2e_client.datasources.get(slug=name)
        assert "The requested resource could not be found" in str(exception_info.value)

    def test_get_unauthorized_user(self, domain, class_context, e2e_client, e2e_data_scientist_user):
        new_datasource = self.create_random_datasource(e2e_client,
                                                       name=class_context.generate_name(5),
                                                       credentials=self.storage_credentials_user_rw)
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )
        slug = new_datasource.slug
        with pytest.raises(CnvrgHttpError):
            ds = client_of_non_admin_user.datasources.get(slug=slug)
            # without reload, it doesn't perform get
            ds.reload()

    def test_get_authorized_user(self, domain, class_context, e2e_client, e2e_data_scientist_user):
        new_datasource = self.create_random_datasource(e2e_client,
                                                       name=class_context.generate_name(5),
                                                       credentials=self.storage_credentials_user_rw,
                                                       collaborators=[e2e_data_scientist_user['email']])
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )
        slug = new_datasource.slug
        ds = client_of_non_admin_user.datasources.get(slug=slug)
        # without reload, it doesn't perform get
        ds.reload()
        assert slug == ds.slug

    def test_get_all_as_admin(self, domain, class_context, e2e_client, e2e_data_scientist_user):
        new_datasource = self.create_random_datasource(e2e_client,
                                                       name=class_context.generate_name(5),
                                                       credentials=self.storage_credentials_user_rw,
                                                       collaborators=[e2e_data_scientist_user['email']])
        client_of_non_admin_user = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
            organization=e2e_client._context.organization
        )
        slug = new_datasource.slug
        client_of_non_admin_user.datasources.get(slug=slug)
        # without reload, it doesn't perform get
        datasource = e2e_client.datasources.get(slug=new_datasource.slug)
        datasource.reload()
        assert slug == datasource.slug

    def test_get_as_admin(self, class_context, e2e_client):
        new_datasource = self.create_random_datasource(e2e_client,
                                                       name=class_context.generate_name(5),
                                                       credentials=self.storage_credentials_user_rw)
        datasource = e2e_client.datasources.get(slug=new_datasource.slug)
        datasource.reload()
        assert new_datasource.slug == datasource.slug

    # endregion

    # region List
    def test_list(self, class_context, e2e_client):
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0

        # We create names with class prefix so that the cleanup will find them.
        name_base = class_context.generate_name(5)
        for i in range(40):
            name = "{}{}".format(name_base, i)
            self.create_random_datasource(e2e_client,
                                          name,
                                          credentials=self.storage_credentials_user_rw)

        # Check descending order works
        idx = 39
        datasources = e2e_client.datasources.list()
        for datasource in datasources:
            assert datasource.name == "{}{}".format(name_base, idx)
            idx -= 1

        # Check ascending order works
        idx = 0
        datasources = e2e_client.datasources.list(sort="id")
        for datasource in datasources:
            assert datasource.name == "{}{}".format(name_base, idx)
            idx += 1

    def test_list_filter(self, class_context, e2e_client):
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0
        total = 40
        # We create names with class prefix so that the cleanup will find them.
        name_base = class_context.generate_name(5)
        for i in range(total):
            name = "{}{}".format(name_base, i)
            self.create_random_datasource(e2e_client,
                                          name,
                                          credentials=self.storage_credentials_user_rw)

        idx = total - 1  # count starts at 0
        s3_filter = {'operator': "AND",
                     'conditions': [{'key': "type", 'operator': "is", 'value': StorageTypes.S3.value}]}
        datasources = e2e_client.datasources.list(filter=s3_filter)
        assert e2e_client.datasources.list_count(sort="id", filter=s3_filter) == total
        for datasource in datasources:
            assert datasource.name == "{}{}".format(name_base, idx)
            assert datasource.storage_type == StorageTypes.S3.value
            idx -= 1

        minio_filter = {'operator': "AND",
                        'conditions': [{'key': "type", 'operator': "is", 'value': StorageTypes.MINIO.value}]}
        assert e2e_client.datasources.list_count(filter=minio_filter) == 0

        fake_filter = {'operator': "AND",
                       'conditions': [{'key': "type", 'operator': "is", 'value': "fake"}]}
        assert e2e_client.datasources.list_count(filter=fake_filter) == 0

    def test_list_assigned_to_user_only(self, class_context, e2e_client, e2e_user, e2e_temp_user, domain):
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0

        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        bucket_assigned_to_temp_user = self.create_random_datasource(e2e_client,
                                                                     name=class_context.generate_name(5),
                                                                     collaborators=[e2e_temp_user['email']],
                                                                     credentials=self.storage_credentials_user_rw)

        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        self.create_random_datasource(e2e_client,
                                      name=class_context.generate_name(5),
                                      credentials=self.storage_credentials_user_rw)

        # List as temp_user (not admin), it should only list data sources assigned to temp_user.
        temp_user_cnvrg = Cnvrg(domain=domain, email=e2e_temp_user["email"], password=e2e_temp_user["password"])

        datasources_count = temp_user_cnvrg.datasources.list_count(sort="id")
        assert datasources_count == 1
        for ds in temp_user_cnvrg.datasources.list():
            assert len(ds.collaborators) >= 2  # at least temp_user & admin (it could be assigned to more collaborators too)
            assert e2e_user['email'] in ds.collaborators
            assert e2e_temp_user['email'] in ds.collaborators
            assert ds.slug == bucket_assigned_to_temp_user.slug

    def test_list_assigned_to_user_only_count_0(self, class_context, e2e_client, e2e_user, e2e_temp_user, domain):
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0

        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        # no collaborators assigned to the data source
        self.create_random_datasource(e2e_client,
                                      name=class_context.generate_name(5),
                                      credentials=self.storage_credentials_user_rw)

        # list as temp_user
        temp_user_cnvrg = Cnvrg(domain=domain, email=e2e_temp_user["email"], password=e2e_temp_user["password"])
        datasources_count = temp_user_cnvrg.datasources.list_count(sort="id")
        assert datasources_count == 0

    def test_list_all_as_admin(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0
        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        bucket_assigned_to_temp_user = self.create_random_datasource(e2e_client,
                                                                     name=class_context.generate_name(5),
                                                                     collaborators=[e2e_temp_user['email']],
                                                                     credentials=self.storage_credentials_user_rw)

        # We create names with class prefix so that the cleanup will find them.
        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        bucket_not_assigned_to_collaborators = self.create_random_datasource(e2e_client,
                                                                             name=class_context.generate_name(5),
                                                                             credentials=self.storage_credentials_user_rw)

        # list as admin

        datasources_count = e2e_client.datasources.list_count(sort="id")
        assert datasources_count == 2
        for ds in e2e_client.datasources.list():
            assert e2e_user['email'] in ds.collaborators
            assert ds.slug in [bucket_assigned_to_temp_user.slug, bucket_not_assigned_to_collaborators.slug]

    def test_list_public(self, class_context, e2e_client, e2e_user, e2e_temp_user, domain):
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0

        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        # no collaborators assigned to the data source
        self.create_random_datasource(e2e_client,
                                      name=class_context.generate_name(5),
                                      credentials=self.storage_credentials_user_rw)

        # list as temp_user
        temp_user_cnvrg = Cnvrg(domain=domain, email=e2e_temp_user["email"], password=e2e_temp_user["password"])
        datasources_count = temp_user_cnvrg.datasources.list_count(sort="id")
        assert datasources_count == 0
        # Clean the db before testing list
        TestDatasources.cleanup(class_context.prefix)
        assert e2e_client.datasources.list_count(sort="id") == 0

        # Currently, logged in as  e2e_user.
        # e2e_user will be the admin of the data source
        # no collaborators assigned to the data source but create as public
        self.create_random_datasource(e2e_client,
                                      name=class_context.generate_name(5),
                                      public=True,
                                      credentials=self.storage_credentials_user_rw)

        # list as temp_user
        temp_user_cnvrg = Cnvrg(domain=domain, email=e2e_temp_user["email"], password=e2e_temp_user["password"])
        datasources_count = temp_user_cnvrg.datasources.list_count(sort="id")
        assert datasources_count == 1
        ds = next(temp_user_cnvrg.datasources.list())
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        assert e2e_temp_user["email"] not in ds.collaborators

    # No Minio
    # def test_list_type(self, class_context, e2e_client):
    #     # Clean the db before testing list
    #     TestDatasources.cleanup(class_context.prefix)
    #     assert e2e_client.datasources.list_count(sort="id") == 0
    #
    #     # We create names with class prefix so that the cleanup will find them.
    #     # Create 2 AWS datasources
    #     name1 = class_context.generate_name(5)
    #     datasource = e2e_client.datasources.create(name=name1,
    #                                              storage_type=StorageTypes.S3,
    #                                              bucket_name=self.storage_bucket_name,
    #                                              region=self.storage_region,
    #                                              credentials=self.storage_credentials_user_rw)
    #     name2 = class_context.generate_name(5)
    #     datasource = e2e_client.datasources.create(name=name2,
    #                                              storage_type=StorageTypes.S3,
    #                                              bucket_name=self.storage_bucket_name,
    #                                              region=self.storage_region,
    #                                              credentials=self.storage_credentials_user_rw)
    #
    #     # Create 2 Minio datasources
    #     name3 = class_context.generate_name(5)
    #     datasource = e2e_client.datasources.create(name=name3,
    #                                              storage_type=StorageTypes.MINIO,
    #                                              bucket_name=self.storage_bucket_name,
    #                                              region=self.storage_region,
    #                                              credentials=self.storage_credentials_user_rw)
    #     name4 = class_context.generate_name(5)
    #     datasource = e2e_client.datasources.create(name=name4,
    #                                              storage_type=StorageTypes.MINIO,
    #                                              bucket_name=self.storage_bucket_name,
    #                                              region=self.storage_region,
    #                                              credentials=self.storage_credentials_user_rw)
    #     aws_count = 0
    #     minio_count = 0
    #     for ds in e2e_client.datasources.list(type=StorageTypes.S3):
    #         aws_count += 1
    #     for ds in e2e_client.datasources.list(type=StorageTypes.MINIO):
    #         minio_count += 1
    #     assert aws_count == 2
    #     assert minio_count == 2
    # endregion

    # region Add Collaborator
    # region test validity of collaborators
    def test_add_collaborator(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw)
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        ds.add_collaborator(e2e_temp_user['email'])
        ds.reload()
        assert len(ds.collaborators) == 2
        assert e2e_user['email'] in ds.collaborators
        assert e2e_temp_user['email'] in ds.collaborators

    def test_add_not_authorized_collaborator(self, class_context, e2e_client, e2e_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw)
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

        with pytest.raises(CnvrgHttpError) as exception_info:
            ds.add_collaborator('fake@mail.com')

        assert 'fake@mail.com' in str(exception_info.value)
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

    def test_add_existing_collaborator(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw)
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

        ds.add_collaborator(e2e_temp_user['email'])
        ds.reload()
        assert len(ds.collaborators) == 2
        assert e2e_user['email'] in ds.collaborators
        assert e2e_temp_user['email'] in ds.collaborators

        ds.add_collaborator(e2e_temp_user['email'])

        ds.reload()
        assert len(ds.collaborators) == 2
        assert e2e_user['email'] in ds.collaborators
        assert e2e_temp_user['email'] in ds.collaborators

    def test_add_admin_as_collaborator(self, class_context, e2e_client, e2e_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw)
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

        ds.add_collaborator(e2e_user['email'])

        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

    # endregion
    # region test authorizations
    def test_add_collaborator_as_non_admin(self, domain, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw)
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        # login as non admin user
        temp_user_cnvrg = Cnvrg(domain=domain, email=e2e_temp_user["email"], password=e2e_temp_user["password"])
        with pytest.raises(CnvrgHttpError) as exception_info:
            temp_ds = temp_user_cnvrg.datasources.get(ds.slug)
            temp_ds.add_collaborator(e2e_temp_user['email'])
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        assert 'Unauthorized' in str(exception_info.value)

    # endregion
    # endregion

    # region Remove Collaborator

    def test_remove_collaborator(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw
                                           )
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        ds.add_collaborator(e2e_temp_user['email'])
        ds.reload()
        assert len(ds.collaborators) == 2
        assert e2e_user['email'] in ds.collaborators
        assert e2e_temp_user['email'] in ds.collaborators
        ds.remove_collaborator(e2e_temp_user['email'])
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

    # region test validity of collaborators

    def test_remove_user_not_in_org(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw
                                           )
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        with pytest.raises(CnvrgHttpError) as exception_info:
            ds.remove_collaborator('fake@mail.com')
        assert 'fake@mail.com' in str(exception_info.value)
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

    def test_remove_user_not_assigned_to_the_datasource(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw
                                           )
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        with pytest.raises(CnvrgHttpError) as exception_info:
            ds.remove_collaborator(e2e_temp_user['email'])
        assert e2e_temp_user['email'] in str(exception_info.value)
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

    def test_remove_admin(self, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw)
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        with pytest.raises(CnvrgHttpError) as exception_info:
            ds.remove_collaborator(e2e_user['email'])
        assert e2e_user['email'] in str(exception_info.value)
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators

    # endregion

    # region test authorizations
    def test_remove_collaborator_as_non_admin(self, domain, class_context, e2e_client, e2e_user, e2e_temp_user):
        ds = self.create_random_datasource(e2e_client,
                                           name=class_context.generate_name(5),
                                           credentials=self.storage_credentials_user_rw
                                           )
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        # login as non admin user
        temp_user_cnvrg = Cnvrg(domain=domain, email=e2e_temp_user["email"], password=e2e_temp_user["password"])
        with pytest.raises(CnvrgHttpError) as exception_info:
            temp_ds = temp_user_cnvrg.datasources.get(ds.slug)
            temp_ds.remove_collaborator(e2e_temp_user['email'])
        ds.reload()
        assert len(ds.collaborators) == 1
        assert e2e_user['email'] in ds.collaborators
        assert 'Unauthorized' in str(exception_info.value)

    # endregion

    # endregion

    def test_list_count(self, class_context, e2e_client):
        # We create names with class prefix so that the cleanup will find them.
        count_before = e2e_client.datasources.list_count()
        number_of_obj_to_create = 23
        for i in range(number_of_obj_to_create):
            self.create_random_datasource(e2e_client,
                                          name=class_context.generate_name(5),
                                          credentials=self.storage_credentials_user_rw)

        count_after = e2e_client.datasources.list_count()
        assert count_after == count_before + number_of_obj_to_create

    # region HELPERS
    def create_random_datasource(self, client, name, collaborators=None, public=None, credentials=None):
        if collaborators:
            datasource = client.datasources.create(name=name,
                                                   storage_type=self.storage_type,
                                                   bucket_name=self.storage_bucket_name,
                                                   path=self.storage_path,
                                                   endpoint=self.storage_endpoint,
                                                   region=self.storage_region,
                                                   credentials=credentials,
                                                   collaborators=collaborators,
                                                   public=public)
        else:
            datasource = client.datasources.create(name=name,
                                                   storage_type=self.storage_type,
                                                   bucket_name=self.storage_bucket_name,
                                                   path=self.storage_path,
                                                   endpoint=self.storage_endpoint,
                                                   region=self.storage_region,
                                                   credentials=credentials,
                                                   public=public)
        return datasource
    # endregion
