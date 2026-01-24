from fitrequest.client import FitRequest


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
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{item_id}',
        },
        {
            'name': 'get_item_details',
            'endpoint': '/items/{item_id}/details/{detail_id}',
        },
    ]

    def __init__(self, username: str | None = None, password: str | None = None) -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.session.authenticate()


client_lazy_config_custom_init_session = RestApiClient(username='toto', password='1234')
