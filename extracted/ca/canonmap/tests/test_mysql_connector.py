import os

from dotenv import load_dotenv
import pytest

from canonmap import MySQLConnectorConfig, MySQLConnectionMethod, MySQLConnector

load_dotenv(override=True)

# -- Helpers (use env vars or a .env file for test credentials) --
MYSQL_USER = os.getenv("DB_USER", "root")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
# MYSQL_DB = os.getenv("DB_NAME", "test_db")
MYSQL_HOST = os.getenv("DB_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("DB_PORT", "3306"))

@pytest.fixture
def mysql_config():
    return MySQLConnectorConfig(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        # database=MYSQL_DB,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        connection_method=MySQLConnectionMethod.TCP,  # or AUTO for auto-detect
        autocommit=True,
    )

@pytest.fixture
def connector(mysql_config):
    connector = MySQLConnector(mysql_config)
    connector.connect()
    yield connector
    connector.close()

def test_connect_and_is_alive(connector):
    assert connector.is_alive(), "Connection should be alive after connect()"

# def test_run_query_select(connector):
#     # Prepare a dummy table and insert a row
#     connector.run_query("CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY AUTO_INCREMENT, value VARCHAR(100))")
#     connector.run_query("INSERT INTO test_table (value) VALUES ('foo')")
#     rows = connector.run_query("SELECT * FROM test_table WHERE value = %s", ("foo",))
#     assert rows, "Should return at least one row"
#     assert rows[0]["value"] == "foo"

# def test_run_query_commit_and_rollback(connector):
#     connector.run_query("CREATE TABLE IF NOT EXISTS test_table2 (id INT PRIMARY KEY AUTO_INCREMENT, v INT)")
#     # Insert and check autocommit
#     connector.run_query("INSERT INTO test_table2 (v) VALUES (42)")
#     rows = connector.run_query("SELECT v FROM test_table2 WHERE v = %s", (42,))
#     assert rows and rows[0]["v"] == 42

def test_close(connector):
    connector.close()
    assert not connector.is_alive(), "Should not be alive after close()"

def test_bad_credentials():
    bad_config = MySQLConnectorConfig(
        user="baduser",
        password="badpass",
        # database=MYSQL_DB,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        connection_method=MySQLConnectionMethod.TCP,
    )
    with pytest.raises(Exception):
        connector = MySQLConnector(bad_config)
        connector.connect()