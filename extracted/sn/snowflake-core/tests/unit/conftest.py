import logging
import types

from threading import Event
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from snowflake.core._internal.snowapi_parameters import SnowApiParameter, SnowApiParameters
from snowflake.core._root import Root
from snowflake.core.database import DatabaseCollection
from snowflake.core.table._generated.models.table import Table
from snowflake.core.table._generated.models.table_column import TableColumn


@pytest.fixture
def fake_root():
    """Mock for Root.

    Usage of this central definition is necessary since the underlying
    generated Configuration class is handled as a singleton, so we treat
    the unit test root as a singleton as well.
    """
    with patch('snowflake.core._root.Root'):
        mock_instance = MagicMock()
        mock_instance._hostname = "localhost"
        mock_instance._connection = mock.MagicMock(
            _rest=mock.MagicMock(
                _protocol="http",
                _port="80",
            )
        )
        mock_instance.root_config = MagicMock()
        mock_instance.root_config.has_user_agents = MagicMock(return_value=False)
        mock_instance.root_config.get_user_agents = MagicMock(return_value="")
        mock_instance.parameters.return_value = SnowApiParameters({SnowApiParameter.MAX_THREADS: "1"})

        mock_instance._initialize_client_info = types.MethodType(Root._initialize_client_info, mock_instance)

        return mock_instance

@pytest.fixture()
def logger_level_info(caplog):
    # Default logger level to info

    with caplog.at_level(logging.INFO):
        yield


@pytest.fixture
def dbs(fake_root):
    return DatabaseCollection(fake_root)


@pytest.fixture
def db(dbs):
    return dbs["my_db"]


@pytest.fixture
def schemas(db):
    return db.schemas


@pytest.fixture
def schema(schemas):
    return schemas["my_schema"]


@pytest.fixture
def tables(schema):
    return schema.tables


@pytest.fixture
def stages(schema):
    return schema.stages


@pytest.fixture
def table(tables):
    return Table(
        name="my_table",
        columns=[
            TableColumn(name="c1", datatype="int"),
        ],
    )


@pytest.fixture()
def event():
    event = Event()
    yield event
    event.set()
