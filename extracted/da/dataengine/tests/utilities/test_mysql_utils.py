import pytest
from unittest.mock import patch, Mock, MagicMock
from dataengine.utilities import mysql_utils
import pymysql


@pytest.fixture
def mock_pymysql_connect():
    with patch('pymysql.connect') as mock_connect:
        yield mock_connect


def test_get_connection_successful(mock_pymysql_connect):
    # Arrange
    schema_name = 'test_schema'
    host = 'localhost'
    port = 3306
    user = 'user'
    password = 'password'
    # Act
    conn = mysql_utils.get_connection(schema_name, host, port, user, password)
    # Assert
    mock_pymysql_connect.assert_called_once_with(
        db=schema_name, host=host, port=port,
        user=user, passwd=password,
        client_flag=mysql_utils.CLIENT.MULTI_STATEMENTS)


def test_get_connection_operational_error(mock_pymysql_connect):
    # Arrange
    mock_pymysql_connect.side_effect = pymysql.OperationalError(
        "Operational Error")
    # Act
    conn = mysql_utils.get_connection(
        'test_schema', 'localhost', 3306, 'user', 'password')
    # Assert
    assert conn is None


def test_get_connection_programming_error(mock_pymysql_connect):
    # Arrange
    mock_pymysql_connect.side_effect = pymysql.ProgrammingError(
        "Programming Error")
    # Act
    conn = mysql_utils.get_connection(
        'test_schema', 'localhost', 3306, 'user', 'password')
    # Assert
    assert conn is None


def test_get_connection_general_error(mock_pymysql_connect):
    # Arrange
    mock_pymysql_connect.side_effect = Exception("General Error")
    # Act
    conn = mysql_utils.get_connection(
        'test_schema', 'localhost', 3306, 'user', 'password')
    # Assert
    assert conn is None


def test_load_from_s3_success():
    mock_conn = Mock()
    mock_cursor = MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    with patch('logging.info'):
        result = mysql_utils.load_from_s3(
            mock_conn, 'table_name', 's3_prefix')
    assert mock_conn.commit.called
    assert mock_cursor.execute.called
    assert result == True


def test_load_from_s3_mysql_error():
    mock_conn = Mock()
    mock_cursor = MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception('MySQL Error')
    with patch('logging.error'):
        result = mysql_utils.load_from_s3(
            mock_conn, 'table_name', 's3_prefix')
    assert mock_conn.rollback.called
    assert result == False


def test_load_from_s3_general_error():
    mock_conn = Mock()
    mock_cursor = MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception('General Error')
    with patch('logging.error'):
        result = mysql_utils.load_from_s3(
            mock_conn, 'table_name', 's3_prefix')
    assert mock_conn.rollback.called
    assert result == False
