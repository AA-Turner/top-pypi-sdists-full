from fitrequest.client import FitRequest
from fitrequest.decorators import retry
from tests.fixtures import Item, ItemDetails, Params


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://test.skillcorner.fr'
    method_docstring = 'Calling endpoint: {endpoint}'

    method_config_list = [
        {
            'base_name': 'items',
            'endpoint': '/items/',
            'add_async_method': True,
            'response_model': Item,
            'params_model': Params,
            'json_path': ' [*].items',
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{item_id}',
            'decorators': [retry(max_retries=3, on_status='500-600')],
            'response_model': Item,
            'params_model': ['lang', 'resp_format'],
        },
        {
            'name': 'get_item_details',
            'endpoint': '/items/{item_id}/details/{detail_id}',
            'decorators': [retry(max_retries=2, on_status='507')],
            'response_model': ItemDetails,
            'params_model': ['lang', 'resp_format'],
        },
    ]


client_lazy_config_request_params = RestApiClient()
