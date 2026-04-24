#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
import json
import logging
import uuid
from datetime import datetime, timedelta

import pytest

from streamsets.sdk import ControlHub, aster_api
from streamsets.sdk.utils import Version, get_decoded_jwt, get_random_string

from .utils import (
    IdPManager, create_organization, execute_install_script_for_docker, fetch_aster_auth_token,
    fetch_aster_token_for_org, fetch_sch_url_and_api_credentials, get_org_id_from_aster_client, get_test_instance,
    wait_for_registered_engines,
)

# fmt: on

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Hook that defines custom command line options to be passed to pytest."""
    parser.addoption('--sch-credential-id', help='SCH component ID')
    parser.addoption('--sch-token', help='SCH auth token')
    parser.addoption('--sys-admin-email', help='SysAdmin Email')
    parser.addoption('--sys-admin-password', help='SysAdmin Password')
    parser.addoption('--org-admin-email', help='Org Admin Email')
    parser.addoption('--org-admin-password', help='Org Admin Password')
    parser.addoption('--firebase-api-key', help='Firebase API Key')
    # Since we do not run tests against production, do expect aster_url
    parser.addoption('--aster-url', help='ASTER URL', required=True)
    parser.addoption('--sdc-version', help='StreamSets Data Collector Version')
    parser.addoption('--snowflake-username', help='Username for snowflake user')
    parser.addoption('--snowflake-password', help='Password for snowflake user')
    parser.addoption(
        '--snowflake-database', help='Name of the Snowflake Database to be used in the tests', default='STREAMSETS_DB'
    )
    parser.addoption(
        '--snowflake-schema', help='Schema of the Snowflake Database to be used in the tests', default='HSS'
    )
    parser.addoption(
        '--snowflake-url',
        help='URL of the Snowflake Database to be used in the tests',
        default='https://streamsets.snowflakecomputing.com',
    )
    parser.addoption('--snowflake-warehouse', help='Snowflake warehouse to be used in the tests', default='DEMO_WH')
    parser.addoption('--transformer-version', help='StreamSets Transformer Version')
    parser.addoption(
        '--transformer-scala-version', help='Scala version to use in the transformer deployment', default='2.12'
    )
    parser.addoption(
        '--keep-engine-instances', help='Retain engines started by the test run after test is run', action='store_true'
    )

    # Arguments for AWS environment
    parser.addoption('--instance-profile', help='Instance Profile')
    parser.addoption('--aws-key-id', help='Key Id')
    parser.addoption('--aws-access-key', help='Secret access key')
    parser.addoption('--environment-region', help='Environment Region')
    parser.addoption('--vpc-id', help='VPC id')
    parser.addoption('--aws-tags', help='AWS tags')
    parser.addoption('--aws-subnet-ids', help='Subnet Ids')
    parser.addoption('--aws-security-group-id', help='Security Group Id')


@pytest.fixture(scope='session')
def args(request):
    """A session-level ``args`` fixture for test functions.
    We provide an object with command line arguments as attributes. This is done to be consistent
    with the behavior of argparse.
    """
    # pytest's Config class stores a dictionary of argparse argument name => dest. Go through this
    # dictionary and return back an args object whose attributes map dest to its option value.
    pytest_args = {arg: request.config.getoption(arg) for arg in request.config._opt2dest.values()}
    yield type('args', (object,), pytest_args)


@pytest.fixture(scope="session")
def resources_label():
    return get_random_string()


@pytest.fixture(scope="session")
def test_environment(sch):
    """A sample environment."""
    environment_builder = sch.get_environment_builder(environment_type='SELF')
    environment = environment_builder.build(
        environment_name='Test Environment for SDK {}'.format(get_random_string()),
        environment_tags=['test-sdk-tag-{}'.format(get_random_string(length=12))],
        allow_nightly_engine_builds=False,
    )
    sch.add_environment(environment)
    sch.activate_environment(environment)

    try:
        yield environment
    finally:
        sch.delete_environment(environment)
        sch.api_client.wait_for_environment_status(environment.id, 'DELETED')


@pytest.fixture(scope="session")
def test_aws_environment(sch, args):
    """A sample EC2 environment."""

    if not all(
        [
            args.aws_key_id,
            args.aws_access_key,
            args.environment_region,
            args.vpc_id,
            args.aws_subnet_ids,
            args.aws_security_group_id,
        ]
    ):
        pytest.skip("Did not provide all the necessary arguments to start an AWS environment")

    environment_builder = sch.get_environment_builder(environment_type='AWS')
    environment = environment_builder.build(
        environment_name='Test Environment for SDK {}'.format(get_random_string()),
        environment_tags=['test-aws-sdk-tag-{}'.format(get_random_string(length=12))],
        allow_nightly_engine_builds=False,
    )

    environment.credential_type = 'Access Keys'
    environment.access_key_id = args.aws_key_id
    environment.secret_access_key = args.aws_access_key
    environment.default_instance_profile = args.instance_profile if args.instance_profile else None
    environment.region = args.environment_region
    environment.vpc_id = args.vpc_id
    environment.aws_tags = json.loads(args.aws_tags) if args.aws_tags else {}
    try:
        environment.subnet_ids = json.loads(args.aws_subnet_ids)
    except ValueError:
        environment.subnet_ids = args.aws_subnet_ids.strip('][').split(', ')
    environment.security_group_id = args.aws_security_group_id

    sch.add_environment(environment)
    sch.activate_environment(environment)

    try:
        yield environment
    finally:
        sch.delete_environment(environment)
        sch.api_client.wait_for_environment_status(environment.id, 'DELETED')


@pytest.fixture(scope="session")
def sdc_snowflake_library(args):
    if not args.sdc_version:
        pytest.skip('--sdc-version needed for this fixture')

    if Version(args.sdc_version) < Version('5.3.0'):
        snowflake_library_name = 'snowflake:1.9.0'
    else:
        snowflake_library_name = 'sdc-snowflake'

    yield snowflake_library_name


@pytest.fixture(scope="session")
def sdc_deployment(args, test_environment, sch, sdc_snowflake_library):
    """Create a session-scoped fixture for an SDC deployment."""

    builder = sch.get_deployment_builder(deployment_type='SELF')

    # A deployment for SDC with DOCKER as install type.
    engine_type = 'DC'
    install_type = 'DOCKER'
    deployment = builder.build(
        deployment_name='SDK Test Deployment SDC_Docker {}'.format(get_random_string()),
        deployment_tags=['test-sdk-sdc-dep-tag-{}'.format(get_random_string(length=12))],
        engine_type=engine_type,
        engine_version=args.sdc_version,
        environment=test_environment,
    )

    deployment.install_type = install_type
    deployment.engine_configuration.engine_labels = ['test-sdc']

    logger.debug('Running with sdc version: {}, using library {}'.format(args.sdc_version, sdc_snowflake_library))

    sch.add_deployment(deployment)
    deployment.engine_configuration.stage_libs.extend(['jdbc', 'aws', sdc_snowflake_library])
    sch.update_deployment(deployment)

    # Start deployment and install 1 SDC
    sch.start_deployment(deployment)
    assert deployment.json_state == 'ENABLED'

    try:
        # Self-managed deployments don't accept engine instances - start 1 SDC
        execute_install_script_for_docker(sch, deployment)
        wait_for_registered_engines(sch, deployment.id)
        yield deployment
    finally:
        sch.delete_deployment(deployment)


@pytest.fixture(scope="session")
def snowflake_config(args):
    """Create a dictionary containing the relevant snowflake test configuration"""
    snowflake_config = {
        'connectionString': args.snowflake_url,
        'db': args.snowflake_database,
        'schema': args.snowflake_schema,
        'warehouse': args.snowflake_warehouse,
    }
    yield snowflake_config


@pytest.fixture(scope="session")
def transformer_deployment(sch, test_environment, args):
    """Create a session-scoped fixture for a Transformer."""

    if not args.transformer_version:
        pytest.skip('--transformer-version needed for fixture but not provided')
        yield None

    builder = sch.get_deployment_builder(deployment_type='SELF')

    # A deployment for Transformer with DOCKER as install type.
    engine_type = 'TF'
    install_type = 'DOCKER'
    deployment = builder.build(
        deployment_name='SDK Test Deployment Transformer_Docker {}'.format(get_random_string()),
        deployment_type='SELF',
        deployment_tags=['test-sdk-transformer-dep-tag-{}'.format(get_random_string(length=12))],
        engine_type=engine_type,
        engine_version=args.transformer_version,
        scala_binary_version=args.transformer_scala_version,
        environment=test_environment,
    )
    deployment.install_type = install_type

    # engine_labels
    deployment.engine_configuration.engine_labels = ['test-transformer']

    sch.add_deployment(deployment)

    # Start deployment and install 1 Transformer
    sch.start_deployment(deployment)
    assert deployment.json_state == 'ENABLED'

    try:
        execute_install_script_for_docker(sch, deployment)
        wait_for_registered_engines(sch, deployment.id)
        yield deployment
    finally:
        sch.delete_deployment(deployment)


@pytest.fixture(scope='session')
def sch_authoring_sdc(sdc_deployment):
    """Create a session-scoped fixture to track the authoring SDC.

    Args:
        sdc_deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

    Returns:
        An instance of (:py:class:`streamsets.sdk.sch_models.DataCollector`).
    """
    if sdc_deployment:
        yield sdc_deployment.registered_engines[0]
    else:
        yield None


@pytest.fixture(scope='session')
def sch_authoring_sdc_id(sch_authoring_sdc):
    """Create a session-scoped fixture to track the authoring SDC ID.

    Args:
        sch_authoring_sdc (:py:class:`streamsets.sdk.sch_models.Engine`): Engine object.

    Returns:
        A :obj:`str` instance of the ID of the authoring SDC.
    """
    if sch_authoring_sdc:
        yield sch_authoring_sdc.id
    else:
        yield None


@pytest.fixture(scope='session')
def sch_authoring_transformer(transformer_deployment):
    """Create a session-scoped fixture to track the authoring Transformer.

    Args:
        transformer_deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

    Returns:
        An instance of (:py:class:`streamsets.sdk.sch_models.Transformer`).
    """
    if transformer_deployment:
        yield transformer_deployment.registered_engines[0]
    else:
        yield None


@pytest.fixture(scope='session')
def sch_authoring_transformer_id(sch_authoring_transformer):
    """Create a session-scoped fixture to track the authoring Transformer ID.

    Args:
        sch_authoring_transformer (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

    Returns:
        A :obj:`str` instance of the ID of the authoring Transformer.
    """
    if sch_authoring_transformer:
        yield sch_authoring_transformer.id
    else:
        yield None


@pytest.fixture(scope='session')
def sch_engine_sdc_label(sdc_deployment):
    """Create a fixture to return the SDC engine labels.
    If tests use these, jobs in those tests will be run using these labels.

    Args:
        sdc_deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

    Returns:
        (:obj:`list`): List of SDC labels
    """
    if sdc_deployment:
        yield sdc_deployment.engine_configuration.engine_labels
    else:
        yield None


@pytest.fixture(scope='session')
def sch_engine_transformer_label(transformer_deployment):
    """Create a fixture to return Transformer engine labels.
    If tests use these, jobs in those tests will be run using these labels.

    Args:
        transformer_deployment (:py:class:`streamsets.sdk.sch_models.Deployment`): Deployment object.

    Returns:
        (:obj:`list`): List of Transformer labels
    """
    if transformer_deployment:
        yield transformer_deployment.engine_configuration.engine_labels
    else:
        yield None


@pytest.fixture(scope="session")
def metering_report(sch):
    """Pulls the last 7 days of metering data from the SCH organization.

    Args:
        sch (:py:class:`streamsets.sdk.ControlHub`): Control Hub object.

    Returns:
        An instance of (:py:class:`streamsets.sdk.sch_models.MeteringReport`).
    """
    return sch.metering_and_usage[datetime.now() - timedelta(7) :]


@pytest.fixture(scope="module")
def test_user(sch):
    """Create a sample user for testing."""
    user_email = f'stftestsdc+sdk-{get_random_string()}@streamsets.com'
    user_builder = sch.get_user_builder()
    user = user_builder.build(email_address=user_email)
    sch.invite_user(user)

    try:
        yield user
    finally:
        try:
            if sch.users.get(email_address=user_email):
                sch.delete_user(user, deactivate=True)
                with pytest.raises(ValueError):
                    sch.users.get(email_address=user_email)
        except ValueError:
            logger.warning('Unable to find and delete user %s.', user_email)


@pytest.fixture(scope="module")
def test_group(sch):
    """Create a sample group to use for membership."""
    group_display_name = f'test-group-{get_random_string()}'
    group_builder = sch.get_group_builder()
    group = group_builder.build(display_name=group_display_name)
    sch.add_group(group)

    try:
        yield group
    finally:
        try:
            if sch.groups.get(id=group.id):
                sch.delete_group(group)
                assert group not in sch.groups
        except ValueError:
            logger.warning('Unable to find and delete group %s.', group.id)


@pytest.fixture(scope="module")
def invalid_jdbc_test_connection(sch, sch_authoring_sdc):
    """Create a test connection."""
    if Version(sch_authoring_sdc.version) < Version('3.22.0'):
        raise Exception("Connection testing requires an Engine version of 3.22.0 or higher")

    connection_builder = sch.get_connection_builder()
    conn = connection_builder.build(
        title=f'mysql-conn-{str(uuid.uuid4())}',
        connection_type='STREAMSETS_JDBC',
        authoring_engine=sch_authoring_sdc,
    )
    conn.connection_definition.configuration['connectionString'] = 'jdbc://fake-server:1234'
    conn.connection_definition.configuration['useCredentials'] = True
    conn.connection_definition.configuration['username'] = 'root'
    conn.connection_definition.configuration['password'] = 'root'
    sch.add_connection(conn)
    try:
        yield conn
    finally:
        sch.delete_connection(conn)


@pytest.fixture(scope="module")
def invalid_jdbc_engineless_test_connection(sch):
    """Create a test connection."""

    connection_builder = sch.get_connection_builder()
    conn = connection_builder.build(
        title=f'mysql-conn-{str(uuid.uuid4())}',
        connection_type='STREAMSETS_JDBC',
    )
    conn.connection_definition.configuration['connectionString'] = 'jdbc://fake-server:1234'
    conn.connection_definition.configuration['useCredentials'] = True
    conn.connection_definition.configuration['username'] = 'root'
    conn.connection_definition.configuration['password'] = 'root'
    sch.add_connection(conn)
    try:
        yield conn
    finally:
        sch.delete_connection(conn)


@pytest.fixture(scope="module")
def invalid_aws_test_connection(sch, sch_authoring_sdc):
    """Create a test connection."""
    if Version(sch_authoring_sdc.version) < Version('3.22.0'):
        pytest.skip("Connection testing requires an Engine version of 3.22.0 or higher")

    connection_builder = sch.get_connection_builder()
    conn = connection_builder.build(
        title=f'aws-s3-conn-{str(uuid.uuid4())}',
        connection_type='STREAMSETS_AWS_S3',
        authoring_engine=sch_authoring_sdc,
    )
    conn.connection_definition.configuration['awsConfig.credentialMode'] = 'WITH_CREDENTIALS'
    conn.connection_definition.configuration['awsConfig.awsAccessKeyId'] = 123
    conn.connection_definition.configuration['awsConfig.awsSecretAccessKey'] = 456
    sch.add_connection(conn)
    try:
        yield conn
    finally:
        sch.delete_connection(conn)


@pytest.fixture(scope="module")
def invalid_aws_engineless_test_connection(sch):
    """Create a test connection."""
    connection_builder = sch.get_connection_builder()
    conn = connection_builder.build(
        title=f'aws-s3-conn-{str(uuid.uuid4())}',
        connection_type='STREAMSETS_AWS_S3',
    )
    conn.connection_definition.configuration['awsConfig.credentialMode'] = 'WITH_CREDENTIALS'
    conn.connection_definition.configuration['awsConfig.awsAccessKeyId'] = 123
    conn.connection_definition.configuration['awsConfig.awsSecretAccessKey'] = 456
    sch.add_connection(conn)
    try:
        yield conn
    finally:
        sch.delete_connection(conn)


@pytest.fixture(scope="module")
def invalid_snowflake_test_connection(args, sch, sch_authoring_sdc):
    if Version(args.sdc_version) < Version('5.3.0'):
        pytest.skip('Test is only run with data collector version >= 5.3.0')

    connection_builder = sch.get_connection_builder()
    conn = connection_builder.build(
        title=f'aws-s3-conn-{str(uuid.uuid4())}',
        connection_type='STREAMSETS_SNOWFLAKE',
        authoring_engine=sch_authoring_sdc,
    )
    conn.connection_definition.configuration['organization'] = 'fakeOrg'
    conn.connection_definition.configuration['account'] = 'fakeAccount'
    conn.connection_definition.configuration['user'] = 'root'
    conn.connection_definition.configuration['password'] = 'root'
    sch.add_connection(conn)
    try:
        yield conn
    finally:
        sch.delete_connection(conn)


@pytest.fixture(scope="module")
def invalid_snowflake_engineless_test_connection(args, sch):
    connection_builder = sch.get_connection_builder()
    conn = connection_builder.build(
        title=f'aws-s3-conn-{str(uuid.uuid4())}',
        connection_type='STREAMSETS_SNOWFLAKE',
    )
    conn.connection_definition.configuration['organization'] = 'fakeOrg'
    conn.connection_definition.configuration['account'] = 'fakeAccount'
    conn.connection_definition.configuration['user'] = 'root'
    conn.connection_definition.configuration['password'] = 'root'
    sch.add_connection(conn)
    try:
        yield conn
    finally:
        sch.delete_connection(conn)


@pytest.fixture(scope='session')
def aster_api_client(args):
    """Fixture that returns the Aster api_client instance."""
    if args.sys_admin_email and args.sys_admin_password:

        aster_authentication_token = fetch_aster_auth_token(
            args.aster_url, args.sys_admin_email, args.sys_admin_password, None, args.firebase_api_key
        )
        aster_api_client = aster_api.ApiClient(
            server_url=args.aster_url, authentication_token=aster_authentication_token
        )
        aster_api_client.login()
        return aster_api_client

    elif args.sch_token and args.sch_credential_id:
        aster_api_client = aster_api.ApiClient(
            server_url=args.aster_url, sch_auth_token=args.sch_token, sch_credential_id=args.sch_credential_id
        )
        aster_api_client.login()
        return aster_api_client

    else:
        pytest.skip('ASTER or SCH credentials not provided, pass at least one of them to run tests')


@pytest.fixture(scope="session")
def is_testing_run_as_sys_admin(aster_api_client):
    """Determine whether testing is being run as a SysAdmin.

    Args:
        aster_api_client (:py:obj:`streamsets.sdk.aster_api.ApiClient`): Aster client of the user running testing

    Returns:
        A :py:obj:`bool` that is ``True`` if the user running the tests is a SysAdmin, ``False`` otherwise.
    """
    # assume we are not a sys-admin by default
    is_sys_admin = False

    # if we are logged in as a sys-admin we will have the authentication token set, else we are using sch creds
    if aster_api_client._authentication_token:
        jwt_claims = get_decoded_jwt(aster_api_client._authentication_token)
        if 'sys-admin' in jwt_claims['t_s_roles']:
            is_sys_admin = True

    yield is_sys_admin


@pytest.fixture(scope="session")
def test_instance(aster_api_client, is_testing_run_as_sys_admin):
    """SCH instance in which tests are going to be run.

    Args:
        aster_api_client (:py:class:`streamsets.sdk.aster_api.ApiClient`): Aster Client of the user running the tests.
        is_testing_run_as_sys_admin (:py:obj:`bool`): If the user running the tests is a Sys-Admin.

    Returns:
        The test instance in which the test will be run if running the tests as a Sys-Admin, else None.
    """

    if is_testing_run_as_sys_admin:
        yield get_test_instance(aster_api_client)
    else:
        yield None


@pytest.fixture(scope="session")
def organization(aster_api_client, is_testing_run_as_sys_admin, test_instance, args):
    """
    Returns the organization that is going to be used to run the tests.
        -   If the tests are run as Sys-Admin it will create a new organization.
        -   If the tests are run as Org-Admin it will return the organization.
    Args:
        aster_api_client (:py:obj:`streamsets.sdk.aster_api.ApiClient`): The Aster API client.
        is_testing_run_as_sys_admin (:py:obj:`bool`): Whether tests are run as a Sys-Admin
        test_instance (:py:obj:`dict`): The instance in which the tests are running.

    Returns:
        A :py:obj:`dict` representing organization that is going to be used to run the tests.
    """
    if is_testing_run_as_sys_admin:
        email = args.org_admin_email
        org_name = f'SDK run at {datetime.now()}'
        org_admin_email, org = create_organization(aster_api_client, org_name, email, instance=test_instance)
        org["org_admin_email"] = org_admin_email

        yield org

        aster_api_client.delete_admin_organizations([org['id']])

    else:
        # get the org id of the user
        org_id = get_org_id_from_aster_client(aster_api_client)

        yield aster_api_client.get_org(org_id).response.json()


@pytest.fixture(scope="session")
def org_admin_aster_client(organization, aster_api_client, is_testing_run_as_sys_admin, args):
    """
    Returns an Aster API client for an org admin who belongs to the organization that is used to run the tests.
    Args:
        organization (:obj:`dict`): The organization used to run the tests.
        aster_api_client (:py:obj:`streamsets.sdk.aster_api.ApiClient`): The Aster API client.
        is_testing_run_as_sys_admin (:py:obj:`bool`): If testing is being run as a Sys-Admin.

    Returns:
        An instance of (:py:obj:`streamsets.sdk.aster_api.ApiClient`): The Aster API client for an org admin who belongs
        to the organization that is used to run the tests.
    """
    if is_testing_run_as_sys_admin:
        email = organization['org_admin_email']
        password = args.org_admin_password
        oidc_token = IdPManager.login(username=email, password=password, firebase_api_key=args.firebase_api_key)
        aster_token = fetch_aster_token_for_org(aster_api_client._base_url, oidc_token, organization['id'])
        org_admin_aster_client = aster_api.ApiClient(
            server_url=aster_api_client._base_url, authentication_token=aster_token
        )
        org_admin_aster_client.login()

        yield org_admin_aster_client

    else:
        yield aster_api_client


@pytest.fixture(scope="session")
def sch(args, org_admin_aster_client):
    """
    Returns a SCH client for an org admin who belongs to the organization that is used to run the tests.
    Args:
        args (:py:class:`argparse.Namespace`): The arguments used to run the tests.
        org_admin_aster_client (:py:obj:`streamsets.sdk.aster_api.ApiClient`): The  Aster API client for an org admin
        who belongs to the organization that is used to run the tests.
    Returns:
        An instance of (:py:class:`streamsets.sdk.sch.ControlHub`) The SCH client for an org admin who belongs to the
        organization that is used to run the tests.
    """
    if args.sch_credential_id and args.sch_token:
        init_data = [args.sch_credential_id, args.sch_token]
    else:
        init_data = fetch_sch_url_and_api_credentials(
            org_admin_aster_client._base_url, org_admin_aster_client._authentication_token
        )

    yield ControlHub(*init_data, aster_url=org_admin_aster_client._base_url)


@pytest.fixture(scope="session")
def is_snowflake_logged_in(args, sch: ControlHub) -> None:
    """Logs into snowflake else skips."""

    username = args.snowflake_username
    password = args.snowflake_password

    if not username or not password:
        pytest.skip("pass --snowflake-username and --snowflake-password to run snowflake tests.")

    sch.update_snowflake_user_credentials(username=username, snowflake_login_type='PASSWORD', password=password)
