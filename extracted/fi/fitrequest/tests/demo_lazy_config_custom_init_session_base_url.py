from fitrequest.client import FitRequest


class RestApiClient(FitRequest):
    """Awesome class generated with fitrequest."""

    client_name = 'rest_api'
    base_url = 'https://staging-env.skillcorner.fr'
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
            base_url='https://test.skillcorner.fr',
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
        )
        self.session.authenticate()


client_lazy_config_custom_init_session_base_url = RestApiClient(username='toto', password='1234')
