#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

from copy import deepcopy

import pytest

from streamsets.sdk import ControlHub
from streamsets.sdk.constants import SDC_EXECUTOR_TYPE
from streamsets.sdk.sch_models import Connection

from .resources.connections_data import CONNECTION_INTERNAL_JSON


class DummyEngine:
    def __init__(self, _id):
        self.id = _id
        self.engine_type = SDC_EXECUTOR_TYPE


class DummyEngines:
    def get(self, id):
        return DummyEngine(id)


class DummyControlHub(ControlHub):
    def __init__(self, *args, **kwargs):
        # purposely avoid calling super().__init__()
        # we want access to the method and not the initializing steps
        pass

    @property
    def engines(self):
        return DummyEngines()


@pytest.fixture(scope="function")
def dummy_sch():
    yield DummyControlHub()


@pytest.fixture(scope="function")
def mock_connection(dummy_sch):
    connection_internal_data = deepcopy(CONNECTION_INTERNAL_JSON)
    connection = Connection(connection=connection_internal_data, control_hub=dummy_sch)
    yield connection


@pytest.mark.parametrize("not_a_connection", [None, 'banana'])
def test_verify_connection_raises_type_error_for_invalid_connection(dummy_sch, not_a_connection):
    with pytest.raises(TypeError):
        dummy_sch.verify_connection(not_a_connection)


def test_verify_connection_raises_type_error_for_invalid_library_type(dummy_sch, mock_connection):
    with pytest.raises(TypeError):
        dummy_sch.verify_connection(connection=mock_connection, library={"this": "isn't", "a": "string"})


def test_verify_connection_raises_value_error_for_invalid_library(dummy_sch, mock_connection):
    with pytest.raises(ValueError):
        dummy_sch.verify_connection(connection=mock_connection, library='not jdbc')
