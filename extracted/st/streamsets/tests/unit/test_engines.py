# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk.sch_api import Command
from streamsets.sdk.sch_models import CollectionModelResults, Engine, Engines

from .resources.engines_data import GET_ENGINE_RESPONSE_COLLECTOR_JSON, GET_ENGINE_RESPONSE_TRANSFORMER_JSON

# fmt: on

NUM_OF_ENGINES = 5


class MockControlHub:
    def __init__(self, value):
        self.api_client = MockApiClient(value)
        self.organization = 'DUMMY ORG'


class MockApiClient:
    def __init__(self, value):
        self.value = value

    def get_engine(self, **kwargs):
        return Command(self, MockResponse(self.value))

    def get_all_registered_engines(self, **kwargs):
        return Command(self, MockResponse(self.value))


class MockResponse:
    def __init__(self, value):
        self.value = value

    def json(self):
        return self.value


@pytest.fixture(scope="function")
def get_engine_response_collector_json():
    json = deepcopy(GET_ENGINE_RESPONSE_COLLECTOR_JSON)

    return json


@pytest.fixture(scope="function")
def get_engine_response_transformer_json():
    json = deepcopy(GET_ENGINE_RESPONSE_TRANSFORMER_JSON)

    return json


@pytest.fixture(scope="function")
def get_all_registered_engines_response_collector_json(get_engine_response_collector_json):
    json = {'totalCount': 1, 'offset': 50, 'len': 50, 'data': []}
    get_engine_response_collector_json['id'] += '{}'
    for i in range(NUM_OF_ENGINES):
        get_engine_response_collector_json['id'].format(i)
        json['data'].append(get_engine_response_collector_json)

    return json


@pytest.fixture(scope="function")
def get_all_registered_engines_response_transformer_json(get_engine_response_transformer_json):
    json = {'totalCount': 1, 'offset': 50, 'len': 50, 'data': []}
    get_engine_response_transformer_json['id'] += '{}'
    for i in range(NUM_OF_ENGINES):
        get_engine_response_transformer_json['id'].format(i)
        json['data'].append(get_engine_response_transformer_json)

    return json


@pytest.mark.parametrize(
    "engine_json",
    ["get_all_registered_engines_response_collector_json", "get_all_registered_engines_response_transformer_json"],
)
def test_engines_sanity(engine_json, request):
    engine_json = request.getfixturevalue(engine_json)

    mock_control_hub = MockControlHub(engine_json)
    e = Engines(mock_control_hub)

    response = e._get_all_results_from_api()

    assert isinstance(response, CollectionModelResults)
    assert response.results == engine_json
    assert len(response.results['data']) == NUM_OF_ENGINES
    assert response.class_type == Engine
    assert response.class_kwargs['control_hub'] == mock_control_hub


@pytest.mark.parametrize(
    "engine_json",
    ["get_engine_response_collector_json", "get_engine_response_transformer_json"],
)
def test_engines_get_with_id(engine_json, request):
    engine_json = request.getfixturevalue(engine_json)
    mock_control_hub = MockControlHub(engine_json)
    e = Engines(mock_control_hub)

    response = e._get_all_results_from_api(id='123')

    assert isinstance(response, CollectionModelResults)
    assert response.results == [engine_json]
    assert response.class_type == Engine
    assert response.class_kwargs['control_hub'] == mock_control_hub


@pytest.mark.parametrize(
    "engine_json,engine_type",
    [("get_engine_response_collector_json", "COLLECTOR"), ("get_engine_response_transformer_json", "TRANSFORMER")],
)
def test_engines_get_with_id_and_type(engine_json, engine_type, request):
    engine_json = request.getfixturevalue(engine_json)
    mock_control_hub = MockControlHub(engine_json)
    e = Engines(mock_control_hub)

    response = e._get_all_results_from_api(engine_type=engine_type, id='123')

    assert isinstance(response, CollectionModelResults)
    assert response.results == [engine_json]
    assert response.class_type == Engine
    assert response.class_kwargs['control_hub'] == mock_control_hub


@pytest.mark.parametrize(
    "engine_json,engine_type",
    [("get_engine_response_collector_json", "TRANSFORMER"), ("get_engine_response_transformer_json", "COLLECTOR")],
)
def test_engines_get_with_incorrect_type(engine_json, engine_type, request):
    engine_json = request.getfixturevalue(engine_json)
    e = Engines(MockControlHub(engine_json))

    with pytest.raises(TypeError):
        e._get_all_results_from_api(engine_type=engine_type, id='123')


def test_engines_get_with_invalid_type(get_engine_response_collector_json):
    e = Engines(MockControlHub(get_engine_response_collector_json))

    with pytest.raises(ValueError):
        e._get_all_results_from_api(engine_type='DUMMY TYPE', id='123')
