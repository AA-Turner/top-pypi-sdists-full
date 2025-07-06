import pytest
import configparser
from tests.conftest import random_string

datasource_test_bukcet_name = 'cnvrg-datasources-bucket'
datasource_test_region = 'us-east-2'
unprocessable_entity_status_code = 422


def parse_aws_credentials(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    credentials = {}
    for section in config.sections():
        credentials[section] = {
            'aws_access_key_id': config.get(section, 'aws_access_key_id'),
            'aws_secret_access_key': config.get(section, 'aws_secret_access_key')
        }
    return credentials


@pytest.fixture(scope="function")
def e2e_datasource(request, e2e_client):
    datasource_name = random_string(5)
    datasource = e2e_client.datasources.create(datasource_name)

    request.addfinalizer(lambda: datasource.delete())

    return datasource
