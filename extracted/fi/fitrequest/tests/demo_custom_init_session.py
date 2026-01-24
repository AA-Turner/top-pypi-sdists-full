from pathlib import Path

from pydantic import Field

from fitrequest.fit_config import FitConfig
from fitrequest.fit_var import ValidFitVar
from fitrequest.method_config import MethodConfig
from fitrequest.method_config_family import MethodConfigFamily


# Custom FitConfig
class RestApiConfig(FitConfig):
    class_name: str = 'RestApiClient'
    class_docstring: str = 'Awesome class generated with fitrequest.'

    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'rest_api'
    method_docstring: str = 'Calling endpoint: {endpoint}'

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfigFamily(
                base_name='items',
                endpoint='/items/',
                add_async_method=True,
            ),
            MethodConfig(
                name='get_item',
                endpoint='/items/{item_id}',
            ),
            MethodConfig(
                name='get_item_details',
                endpoint='/items/{item_id}/details/{detail_id}',
            ),
        ]
    )


# New class created from FitConfig
class ClassDefault(RestApiConfig().fit_class):
    def __init__(self, username: str | None = None, password: str | None = None, env: str = 'dev') -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.env = env
        self.session.authenticate()


class ClassWithSpecificArgs(RestApiConfig(base_url='https://staging.skillcorner.fr:8080').fit_class):
    def __init__(self, username: str | None = None, password: str | None = None, env: str = 'dev') -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.env = env
        self.session.authenticate()


class ClassFromJson(FitConfig.from_json(Path(__file__).parent / 'demo.json')):
    def __init__(self, username: str | None = None, password: str | None = None, env: str = 'dev') -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.env = env
        self.session.authenticate()


class ClassFromYaml(FitConfig.from_yaml(Path(__file__).parent / 'demo.yaml')):
    def __init__(self, username: str | None = None, password: str | None = None, env: str = 'dev') -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.env = env
        self.session.authenticate()


class ClassFromDict(
    FitConfig.from_dict(
        class_name='RestApiClient',
        client_name='rest_api',
        class_docstring='Awesome class generated with fitrequest.',
        base_url='https://test.skillcorner.fr',
        method_docstring='Calling endpoint: {endpoint}',
        method_config_list=[
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
        ],
    )
):
    def __init__(self, username: str | None = None, password: str | None = None, env: str = 'dev') -> None:
        self.session.update(
            auth={
                'username': {'env_name': 'API_USERNAME', 'init_value': username},
                'password': {'env_name': 'API_PASSWORD', 'init_value': password},
            },
            headers={'SOME_FIELD': 'SOME_VALUE'},
            verify=False,  # Disable SSL verification
            timeout=20,  # Set request timeout
        )
        self.env = env
        self.session.authenticate()


# Client instances from generated classes
init_custom_auth = {'username': 'toto', 'password': '1234'}
client_default_custom_init_session = ClassDefault(**init_custom_auth)
client_with_specific_args_custom_init_session = ClassWithSpecificArgs(env='staging', **init_custom_auth)
client_from_json_custom_init_session = ClassFromJson(**init_custom_auth)
client_from_yaml_custom_init_session = ClassFromYaml(**init_custom_auth)
client_from_dict_custom_init_session = ClassFromDict(**init_custom_auth)
