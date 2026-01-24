import pytest
from pydantic_core import ValidationError

from fitrequest.client import FitRequest
from fitrequest.errors import ReservedNamesError
from fitrequest.utils import reserved_fitrequest_names, reserved_httpx_names


@pytest.mark.parametrize(
    'keyword',
    [
        *reserved_fitrequest_names,
        *reserved_httpx_names,
    ],
)
def test_endpoint_forbidden_keyword(keyword):
    with pytest.raises(ReservedNamesError) as err:

        class RestApiClient(FitRequest):
            client_name = 'rest_api'
            base_url = 'https://test.skillcorner.fr'
            method_config_list = [
                {
                    'name': 'get_item',
                    'endpoint': f'/items/{{{keyword}}}',
                }
            ]

    assert err.value.bad_names == {keyword}


@pytest.mark.parametrize(
    'keyword',
    [
        *reserved_fitrequest_names,
        *reserved_httpx_names,
    ],
)
def test_params_forbidden_keyword(keyword):
    with pytest.raises(ValidationError) as err:

        class RestApiClient(FitRequest):
            client_name = 'rest_api'
            base_url = 'https://test.skillcorner.fr'
            method_config_list = [
                {
                    'name': 'get_item',
                    'endpoint': '/items/{item_id}',
                    'params_model': [keyword],
                }
            ]

    err = err.value.errors()[0]['ctx']['error']
    assert isinstance(err, ReservedNamesError)
    assert err.bad_names == {keyword}
