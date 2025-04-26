import os
import pytest
from dataengine import engine, query

DIRNAME = os.path.dirname(os.path.realpath(__file__))

# Mock environment variables
@pytest.fixture(scope='function')
def mock_env_vars():
    env_vars = {
        'DB1_HOST': 'localhost1',
        'DB1_PORT': '5431',
        'DB1_USER': 'user1',
        'DB1_PASSWORD': 'password1',
        'DB2_HOST': 'localhost2',
        'DB2_PORT': '5432',
        'DB2_USER': 'user2',
        'DB2_PASSWORD': 'password2',
    }
    for key, value in env_vars.items():
        os.environ[key] = value
    yield
    for key in env_vars.keys():
        del os.environ[key]


def test_load_asset_config_files(mock_env_vars):
    yaml_paths = [
        './tests/sample_configs/sample_config1.yaml',
        './tests/sample_configs/sample_config2.yaml']
    db_map = engine.load_asset_config_files(yaml_paths)
    assert all(i in db_map for i in ["db1", "db2"])


def test_load_assets(mock_env_vars):
    yaml_paths = [
        './tests/sample_configs/sample_config1.yaml',
        './tests/sample_configs/sample_config2.yaml']
    db_map = engine.load_assets(
        engine.load_asset_config_files(yaml_paths))
    # Validate that the databases are loaded correctly
    assert 'db1' in db_map["databases"]
    assert 'db2' in db_map["databases"]
    # Validate that the environment variables are applied
    assert db_map["databases"]['db1'].host == 'localhost1'
    assert db_map["databases"]['db1'].port == 5431
    assert db_map["databases"]['db2'].host == 'localhost2'
    assert db_map["databases"]['db2'].port == 5432

def test_query_load_functionality():
    # Test loading of base queries from configs
    queries = engine.load_assets(engine.load_asset_config_files([
        "./tests/sample_configs/sample_queries.yaml"]))
    assert list(queries["base_queries"].keys()) == ["sample_queries.test_query_1"]


def test_engine_instance():
    """
    Test the engine.Engine class.
    """
    # Instantiate the engine with the test config files
    engine_instance = engine.Engine([
        os.path.join(DIRNAME, "sample_configs/sample_queries.yaml")
    ])
    # Test loading a query from a base query
    query_object, load_success = engine_instance.load_query(
        "sample_queries.test_query_1")
    assert isinstance(query_object, query.Query)
    assert load_success == True
    # Test loading invalid query
    query_object, load_success = engine_instance.load_query(
        "invalid_base_query_name")
    assert query_object is None
    assert load_success == False
