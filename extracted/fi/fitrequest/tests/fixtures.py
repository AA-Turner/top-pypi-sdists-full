import inspect
import os
from collections.abc import Callable
from functools import cached_property
from pathlib import Path
from typing import Any, Literal

import httpx
import pytest
from pydantic import BaseModel, Field

from fitrequest.auth import Auth
from fitrequest.fit_config import FitConfig
from fitrequest.fit_var import FitVar, ValidFitVar
from fitrequest.method_config import MethodConfig, RequestVerb
from fitrequest.method_config_family import FamilyTemplates, MethodConfigFamily
from fitrequest.method_decorator import ValidMethodDecorator, environment_decorators
from fitrequest.method_models import environment_models
from fitrequest.session import Session


class Params(BaseModel):
    page: int | None = None
    limit: int | None = None
    sort: Literal['name', 'date'] = 'name'
    order: Literal['asc', 'desc'] = 'asc'
    lang: Literal['en', 'fr', 'es'] = 'en'


class Item(BaseModel):
    item_id: int
    item_name: str


class ItemDetails(BaseModel):
    detail_id: int
    detail: str
    item_id: int
    item_name: str


class Config(FitConfig):
    client_name: str = 'client'
    version: str = '0.0.1'
    base_url: ValidFitVar = FitVar(env_name='CLIENT_BASE_URL')


class ConfigWithExtraAttributes(FitConfig):
    client_name: str = 'client'
    version: str = '0.0.1'
    base_url: ValidFitVar = FitVar(env_name='CLIENT_BASE_URL')
    cowsay: str = 'moooh'


class ConfigWithCustomHeaders(FitConfig):
    client_name: str = 'client_with_custom_headers'
    base_url: ValidFitVar = FitVar(env_name='CLIENT_BASE_URL')


class ClientWithCustomHeaders(ConfigWithCustomHeaders().fit_class):
    @cached_property
    def session(self) -> Session:
        return Session(
            client_name=self.client_name, version=self.version, auth=self.auth, headers={'SOME_FIELD': 'SOME_VALUE'}
        )


class ConfigWithAutoVersion(FitConfig):
    # use same name as current package
    client_name: str = 'fitrequest'
    base_url: ValidFitVar = FitVar(env_name='CLIENT_BASE_URL')


class ConfigWithDocstringTemplate(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'client_with_default_docstring'
    method_docstring: str = 'Template of docstring used in every method.'
    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(name='get_items', endpoint='/items/'),
            MethodConfig(name='get_item', endpoint='/items/{item_id}/'),
            MethodConfig(
                name='get_dosctring_set',
                endpoint='/with-docstring',
                docstring='Template is ignored if set.',
            ),
            MethodConfig(name='async_get_items', endpoint='/items/', async_method=True),
            MethodConfig(name='async_get_item', endpoint='/items/{item_id}/', async_method=True),
            MethodConfig(
                name='async_get_dosctring_set',
                endpoint='/with-docstring',
                docstring='Template is ignored if set.',
                async_method=True,
            ),
        ]
    )


class ConfigWithDocstringTemplateAndVariables(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'client_with_default_docstring_and_variables'
    method_docstring: str = 'Calling endpoint: {endpoint}\nDocs URL anchor: {docs_url_anchor}'
    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_items',
                endpoint='/items/',
                docstring_vars={'docs_url_anchor': '/items/items_list'},
            ),
            MethodConfig(
                name='get_item',
                endpoint='/items/{item_id}/',
                docstring='Template is ignored if set.',
                docstring_vars={'docs_url_anchor': '/items/item_read'},
            ),
            MethodConfig(
                name='get_with_no_docstring_variable_but_dosctring_set',
                endpoint='/no-doctsring-variable/with-docstring',
                docstring='Its own docstring.',
            ),
            MethodConfig(
                name='async_get_items',
                endpoint='/items/',
                docstring_vars={'docs_url_anchor': '/items/items_list'},
                async_method=True,
            ),
            MethodConfig(
                name='async_get_item',
                endpoint='/items/{item_id}/',
                docstring='Template is ignored if set.',
                docstring_vars={'docs_url_anchor': '/items/item_read'},
                async_method=True,
            ),
            MethodConfig(
                name='async_get_with_no_docstring_variable_but_dosctring_set',
                endpoint='/no-doctsring-variable/with-docstring',
                docstring='Its own docstring.',
                async_method=True,
            ),
        ]
    )


class ConfigWithMethods(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'client_with_methods'
    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_default_args',
                endpoint='/default-args/',
            ),
            MethodConfig(
                name='get_docstring',
                endpoint='/docstring/',
                docstring='Here is a description of the method.',
            ),
            MethodConfig(
                name='get_doc_none_if_empty',
                endpoint='/docstring/empty',
                docstring='',
            ),
            MethodConfig(
                name='get_items',
                endpoint='/items/',
            ),
            MethodConfig(
                name='get_item',
                endpoint='/items/{item_id}',
            ),
            MethodConfig(
                name='async_get_item',
                async_method=True,
                endpoint='/items/{item_id}',
            ),
            MethodConfig(
                name='save_item',
                endpoint='/items/{item_id}',
                save_method=True,
            ),
            MethodConfig(
                name='get_no_raise_on_status',
                endpoint='/raise-on-status/false',
                raise_for_status=False,
            ),
            MethodConfig(
                name='get_raise_for_status',
                endpoint='/raise-on-status/true',
                raise_for_status=True,
            ),
            MethodConfig(
                name='get_value_in_json_path',
                endpoint='/json-path/',
                json_path='data|[*].data',
            ),
            MethodConfig(
                name='get_with_save_method',
                save_method=True,
                endpoint='/save-method/',
            ),
            MethodConfig(
                name='get_without_save_method',
                save_method=False,
                endpoint='/no-save-method/',
            ),
            MethodConfig(
                name='get_with_multiple_params',
                save_method=False,
                endpoint='/{country_id}/{team_id}/{user_id}',
            ),
            MethodConfig(
                name='async_get_with_multiple_params',
                save_method=False,
                async_method=True,
                endpoint='/{country_id}/{team_id}/{user_id}',
            ),
        ]
    )


class ConfigWithAsyncMethods(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'client_with_methods'
    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='async_get_default_args',
                endpoint='/default-args/',
                async_method=True,
            ),
            MethodConfig(
                name='async_get_docstring',
                endpoint='/docstring/',
                docstring='Here is a description of the method.',
                async_method=True,
            ),
            MethodConfig(
                name='async_get_doc_none_if_empty',
                endpoint='/docstring/empty',
                docstring='',
                async_method=True,
            ),
            MethodConfig(name='async_get_items', endpoint='/items/', async_method=True),
            MethodConfig(name='async_get_item', endpoint='/items/{item_id}', async_method=True),
            MethodConfig(
                name='async_save_item',
                endpoint='/items/{item_id}',
                save_method=True,
                async_method=True,
            ),
            MethodConfig(
                name='async_get_no_raise_on_status',
                endpoint='/raise-on-status/false',
                raise_for_status=False,
                async_method=True,
            ),
            MethodConfig(
                name='async_get_raise_for_status',
                endpoint='/raise-on-status/true',
                raise_for_status=True,
                async_method=True,
            ),
            MethodConfig(
                name='async_get_value_in_json_path',
                endpoint='/json-path/',
                json_path='data|[*].data',
                async_method=True,
            ),
            MethodConfig(
                name='async_get_with_save_method',
                save_method=True,
                endpoint='/save-method/',
                async_method=True,
            ),
            MethodConfig(
                name='async_get_without_save_method',
                save_method=False,
                endpoint='/no-save-method/',
                async_method=True,
            ),
        ]
    )


class ConfigWithURL(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_url'
    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='url_test',
                endpoint='awesome_endpoint/{awesome_id}/{another_awesome_id}',
            )
        ]
    )


class ConfigWithBasicCredentials(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_basic_credentials'
    auth: Auth = Auth(
        username='CUSTOM_USERNAME_KEY',
        password='CUSTOM_PASSWORD_KEY',
    )


class ConfigWithCustomCredsFromEnv(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_custom_creds_from_env'
    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='url_test',
                endpoint='awesome_endpoint/{awesome_id}/{another_awesome_id}',
            )
        ]
    )
    auth: Auth = Auth(username=FitVar(env_name='TOTO_USERNAME'), password=FitVar(env_name='TOTO_PASSWORD'))


class ConfigWithCustomParamsToken(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'client_with_custom_params_token'
    auth: Auth = Auth(params_token='CUSTOM_PARAMS_TOKEN')

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_items',
                endpoint='/items/',
                docstring_vars={'docs_url_anchor': '/items/items_list'},
            )
        ]
    )


class ConfigWithCustomParamsTokenFromAWS(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_custom_params_token_from_aws'
    auth: Auth = Auth(
        params_token=FitVar(
            aws_path='/dont_look_here/params_token',
        )
    )


class ConfigWithCustomHeaderToken(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner.fr'
    client_name: str = 'client_with_custom_header_token'
    auth: Auth = Auth(header_token='CUSTOM_HEADER_TOKEN')

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_items',
                endpoint='/items/',
                docstring_vars={'docs_url_anchor': '/items/items_list'},
            )
        ]
    )


class ConfigWithCustomHeaderTokenFromAWS(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_custom_header_token_from_aws'
    auth: Auth = Auth(
        header_token=FitVar(
            aws_path='/dont_look_here/header_token',
        )
    )


class ConfigWithCustomAuth(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_custom_header_token_from_aws'
    auth: Auth = Auth(custom=httpx.DigestAuth(username='lucien', password='awesome_password'))


class ConfigWithFamily(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_family'

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(name='get_index', endpoint='/'),
            MethodConfig(name='get_version', endpoint='/version/'),
            MethodConfigFamily(
                base_name='item',
                endpoint='/items/{item_id}',
                add_verbs=[RequestVerb.get, RequestVerb.post],
                add_async_method=True,
            ),
            MethodConfigFamily(base_name='items', endpoint='/items/', add_async_method=True, add_save_method=True),
        ]
    )


class ConfigWithFamilyCustomTemplate(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_family'

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(name='get_index', endpoint='/'),
            MethodConfig(name='get_version', endpoint='/version/'),
            MethodConfigFamily(
                base_name='item',
                endpoint='/items/{item_id}',
                add_save_method=True,
                name_templates=FamilyTemplates(save='save_{base_name}'),
            ),
            MethodConfigFamily(base_name='items', endpoint='/items/', add_async_method=True, add_save_method=True),
        ]
    )


class ConfigWithFamilyCustomDefaultTemplate(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_family'
    family_name_templates: FamilyTemplates | None = FamilyTemplates(save='save_{base_name}')

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(name='get_index', endpoint='/'),
            MethodConfig(name='get_version', endpoint='/version/'),
            MethodConfigFamily(
                base_name='item',
                endpoint='/items/{item_id}',
                add_save_method=True,
            ),
            MethodConfigFamily(base_name='items', endpoint='/items/', add_async_method=True, add_save_method=True),
        ]
    )


def simple_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        return 'simple_decorator', func(*args, **kwargs)

    async def async_wrapper(*args, **kwargs) -> Any:
        return 'simple_decorator', await func(*args, **kwargs)

    return async_wrapper if inspect.iscoroutinefunction(func) else wrapper


def decorator_with_params(return_value: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            return return_value, func(*args, **kwargs)

        async def async_wrapper(*args, **kwargs) -> Any:
            return return_value, await func(*args, **kwargs)

        return async_wrapper if inspect.iscoroutinefunction(func) else wrapper

    return decorator


# Register decorators in order to declare decorators by name instead of giving the callable object.
environment_decorators.update(
    {
        'simple_decorator': simple_decorator,
        'decorator_with_params': decorator_with_params,
    }
)

# Register models in order to declare models by name instead of giving the callable object.
environment_models.update(
    {
        'Params': Params,
        'Item': Item,
        'ItemDetails': ItemDetails,
    }
)


class ConfigWithDecorators(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_decorators'

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_index',
                endpoint='/',
                decorators=[simple_decorator],
            ),
            MethodConfig(
                name='get_version',
                endpoint='/version/',
                decorators=[decorator_with_params(return_value='decorator_with_params')],
            ),
            MethodConfigFamily(
                base_name='item',
                endpoint='/items/{item_id}',
                add_verbs=[RequestVerb.get, RequestVerb.post],
                add_async_method=True,
                decorators=[simple_decorator, decorator_with_params(return_value='decorator_with_params')],
            ),
            MethodConfigFamily(
                base_name='items',
                endpoint='/items/',
                add_async_method=True,
                add_save_method=True,
                decorators=[decorator_with_params(return_value='decorator_with_params'), simple_decorator],
            ),
        ]
    )


class ConfigWithDefaultDecorators(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_default_decorators'
    method_decorators: list[ValidMethodDecorator] = Field(
        default_factory=lambda: [decorator_with_params(return_value='decorator_with_params'), simple_decorator]
    )

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_index',
                endpoint='/',
                decorators=[simple_decorator],
            ),
            MethodConfig(
                name='get_version',
                endpoint='/version/',
                decorators=[decorator_with_params(return_value='decorator_with_params')],
            ),
            MethodConfigFamily(
                base_name='item',
                endpoint='/items/{item_id}',
                add_verbs=[RequestVerb.get, RequestVerb.post],
                add_async_method=True,
                decorators=[simple_decorator, decorator_with_params(return_value='decorator_with_params')],
            ),
            MethodConfigFamily(
                base_name='items',
                endpoint='/items/',
                add_async_method=True,
                add_save_method=True,
            ),
        ]
    )


class ConfigWithDefaultDecoratorsString(FitConfig):
    base_url: ValidFitVar = 'https://test.skillcorner'
    client_name: str = 'client_with_default_decorators'
    method_decorators: list[ValidMethodDecorator] = Field(
        default_factory=lambda: ["decorator_with_params(return_value='decorator_with_params')", 'simple_decorator']
    )

    method_config_list: list[MethodConfig | MethodConfigFamily] = Field(
        default_factory=lambda: [
            MethodConfig(
                name='get_index',
                endpoint='/',
                decorators=['simple_decorator'],
            ),
            MethodConfig(
                name='get_version',
                endpoint='/version/',
                decorators=["decorator_with_params(return_value='decorator_with_params')"],
            ),
            MethodConfigFamily(
                base_name='item',
                endpoint='/items/{item_id}',
                add_verbs=[RequestVerb.get, RequestVerb.post],
                add_async_method=True,
                decorators=['simple_decorator', "decorator_with_params(return_value='decorator_with_params')"],
            ),
            MethodConfigFamily(
                base_name='items',
                endpoint='/items/',
                add_async_method=True,
                add_save_method=True,
            ),
        ]
    )


class ConfigSimple(FitConfig):
    client_name: str = 'client'
    version: str = '0.0.1'
    base_url: ValidFitVar = 'https://skillcorner.test.com/api'


@pytest.fixture
def set_env_credentials():
    os.environ['TOTO_USERNAME'] = 'skcr'
    os.environ['TOTO_PASSWORD'] = 'goal'
    yield
    os.environ.pop('TOTO_USERNAME')
    os.environ.pop('TOTO_PASSWORD')


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def config_simple():
    return ConfigSimple()


@pytest.fixture
def config_with_extra_attributes():
    return ConfigWithExtraAttributes()


@pytest.fixture
def client_with_custom_headers():
    return ClientWithCustomHeaders()


@pytest.fixture
def config_with_auto_version():
    return ConfigWithAutoVersion()


@pytest.fixture
def config_with_default_docstring():
    return ConfigWithDocstringTemplate()


@pytest.fixture
def config_with_default_docstring_and_variables():
    return ConfigWithDocstringTemplateAndVariables()


@pytest.fixture
def config_with_methods():
    return ConfigWithMethods()


@pytest.fixture
def config_with_async_methods():
    return ConfigWithAsyncMethods()


@pytest.fixture
def config_with_url():
    return ConfigWithURL()


@pytest.fixture
def config_with_basic_credentials():
    return ConfigWithBasicCredentials()


@pytest.fixture
def config_with_custom_creds_from_env():
    return ConfigWithCustomCredsFromEnv()


@pytest.fixture
def config_with_custom_params_token():
    return ConfigWithCustomParamsToken()


@pytest.fixture
def config_with_custom_params_token_from_aws():
    return ConfigWithCustomParamsTokenFromAWS()


@pytest.fixture
def config_with_custom_header_token():
    return ConfigWithCustomHeaderToken()


@pytest.fixture
def config_with_custom_header_token_from_aws():
    return ConfigWithCustomHeaderTokenFromAWS()


@pytest.fixture
def config_with_custom_auth():
    return ConfigWithCustomAuth()


@pytest.fixture
def config_with_family():
    return ConfigWithFamily()


@pytest.fixture
def config_with_family_custom_template():
    return ConfigWithFamilyCustomTemplate()


@pytest.fixture
def config_with_family_custom_default_template():
    return ConfigWithFamilyCustomDefaultTemplate()


client_with_decorators = ConfigWithDecorators().fit_class()
client_with_default_decorators = ConfigWithDefaultDecorators().fit_class()
client_with_default_decorators_string = ConfigWithDefaultDecoratorsString().fit_class()

yaml_path = Path(__file__).parent / 'config_with_default_decorators.yaml'
json_path = Path(__file__).parent / 'config_with_default_decorators.json'
client_with_default_decorators_from_yaml = FitConfig.from_yaml(yaml_path)()
client_with_default_decorators_from_json = FitConfig.from_json(json_path)()

yaml_path = Path(__file__).parent / 'config_complex.yaml'
json_path = Path(__file__).parent / 'config_complex.json'
client_complex_from_yaml = FitConfig.from_yaml(yaml_path)()
client_complex_from_json = FitConfig.from_json(json_path)()
