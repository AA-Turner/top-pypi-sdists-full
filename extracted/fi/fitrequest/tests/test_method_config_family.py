import pytest
from pydantic_core import ValidationError

from fitrequest.errors import HttpVerbNotProvidedError
from fitrequest.method_config import MethodConfig, RequestVerb
from fitrequest.method_config_family import MethodConfigFamily
from tests.fixtures import (
    config_with_family,
    config_with_family_custom_default_template,
    config_with_family_custom_template,
)


def test_default():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(base_name=base_name, endpoint=endpoint)
    assert family.members == [MethodConfig(name=f'get_{base_name}', endpoint=endpoint)]


def test_some_verbs():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(base_name=base_name, endpoint=endpoint, add_verbs=[RequestVerb.post, RequestVerb.put])
    assert family.members == [
        MethodConfig(name=f'post_{base_name}', endpoint=endpoint, request_verb=RequestVerb.post),
        MethodConfig(name=f'put_{base_name}', endpoint=endpoint, request_verb=RequestVerb.put),
    ]


def test_all_verbs():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(base_name=base_name, endpoint=endpoint, add_verbs=list(RequestVerb))
    assert family.members == [
        MethodConfig(name=f'delete_{base_name}', endpoint=endpoint, request_verb=RequestVerb.delete),
        MethodConfig(name=f'get_{base_name}', endpoint=endpoint, request_verb=RequestVerb.get),
        MethodConfig(name=f'patch_{base_name}', endpoint=endpoint, request_verb=RequestVerb.patch),
        MethodConfig(name=f'post_{base_name}', endpoint=endpoint, request_verb=RequestVerb.post),
        MethodConfig(name=f'put_{base_name}', endpoint=endpoint, request_verb=RequestVerb.put),
    ]


def test_no_verbs():
    base_name = 'items'
    endpoint = '/skcr/items/'
    with pytest.raises(ValidationError) as err:
        MethodConfigFamily(base_name=base_name, endpoint=endpoint, add_verbs=[])
    assert isinstance(err.value.errors()[0]['ctx']['error'], HttpVerbNotProvidedError)


def test_save_method():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(base_name=base_name, endpoint=endpoint, add_save_method=True)
    assert family.members == [
        MethodConfig(name=f'get_{base_name}', endpoint=endpoint),
        MethodConfig(name=f'get_and_save_{base_name}', endpoint=endpoint, save_method=True),
    ]


def test_async_method():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(base_name=base_name, endpoint=endpoint, add_async_method=True)
    assert family.members == [
        MethodConfig(name=f'get_{base_name}', endpoint=endpoint),
        MethodConfig(name=f'async_get_{base_name}', endpoint=endpoint, async_method=True),
    ]


def test_async_and_save_method():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(base_name=base_name, endpoint=endpoint, add_async_method=True, add_save_method=True)
    assert family.members == [
        MethodConfig(name=f'get_{base_name}', endpoint=endpoint),
        MethodConfig(name=f'async_get_{base_name}', endpoint=endpoint, async_method=True),
        MethodConfig(name=f'get_and_save_{base_name}', endpoint=endpoint, save_method=True),
        MethodConfig(name=f'async_get_and_save_{base_name}', endpoint=endpoint, save_method=True, async_method=True),
    ]


def test_async_and_save_method_all_verbs():
    base_name = 'items'
    endpoint = '/skcr/items/'
    family = MethodConfigFamily(
        base_name=base_name,
        endpoint=endpoint,
        add_verbs=list(RequestVerb),
        add_async_method=True,
        add_save_method=True,
    )
    assert family.members == [
        MethodConfig(
            name=f'delete_{base_name}',
            endpoint=endpoint,
            request_verb=RequestVerb.delete,
        ),
        MethodConfig(
            name=f'async_delete_{base_name}',
            endpoint=endpoint,
            async_method=True,
            request_verb=RequestVerb.delete,
        ),
        MethodConfig(
            name=f'delete_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            request_verb=RequestVerb.delete,
        ),
        MethodConfig(
            name=f'async_delete_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            async_method=True,
            request_verb=RequestVerb.delete,
        ),
        MethodConfig(
            name=f'get_{base_name}',
            endpoint=endpoint,
            request_verb=RequestVerb.get,
        ),
        MethodConfig(
            name=f'async_get_{base_name}',
            endpoint=endpoint,
            async_method=True,
            request_verb=RequestVerb.get,
        ),
        MethodConfig(
            name=f'get_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            request_verb=RequestVerb.get,
        ),
        MethodConfig(
            name=f'async_get_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            async_method=True,
            request_verb=RequestVerb.get,
        ),
        MethodConfig(
            name=f'patch_{base_name}',
            endpoint=endpoint,
            request_verb=RequestVerb.patch,
        ),
        MethodConfig(
            name=f'async_patch_{base_name}',
            endpoint=endpoint,
            async_method=True,
            request_verb=RequestVerb.patch,
        ),
        MethodConfig(
            name=f'patch_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            request_verb=RequestVerb.patch,
        ),
        MethodConfig(
            name=f'async_patch_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            async_method=True,
            request_verb=RequestVerb.patch,
        ),
        MethodConfig(
            name=f'post_{base_name}',
            endpoint=endpoint,
            request_verb=RequestVerb.post,
        ),
        MethodConfig(
            name=f'async_post_{base_name}',
            endpoint=endpoint,
            async_method=True,
            request_verb=RequestVerb.post,
        ),
        MethodConfig(
            name=f'post_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            request_verb=RequestVerb.post,
        ),
        MethodConfig(
            name=f'async_post_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            async_method=True,
            request_verb=RequestVerb.post,
        ),
        MethodConfig(
            name=f'put_{base_name}',
            endpoint=endpoint,
            request_verb=RequestVerb.put,
        ),
        MethodConfig(
            name=f'async_put_{base_name}',
            endpoint=endpoint,
            async_method=True,
            request_verb=RequestVerb.put,
        ),
        MethodConfig(
            name=f'put_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            request_verb=RequestVerb.put,
        ),
        MethodConfig(
            name=f'async_put_and_save_{base_name}',
            endpoint=endpoint,
            save_method=True,
            async_method=True,
            request_verb=RequestVerb.put,
        ),
    ]


def test_config_with_family(config_with_family):
    client = config_with_family.fit_class()
    assert hasattr(client, 'get_index')
    assert hasattr(client, 'get_version')
    assert hasattr(client, 'get_item')
    assert hasattr(client, 'post_item')
    assert hasattr(client, 'async_get_item')
    assert hasattr(client, 'async_post_item')
    assert hasattr(client, 'get_items')
    assert hasattr(client, 'get_and_save_items')
    assert hasattr(client, 'async_get_items')
    assert hasattr(client, 'async_get_and_save_items')


def test_config_with_family_custom_template(config_with_family_custom_template):
    client = config_with_family_custom_template.fit_class()
    assert hasattr(client, 'get_index')
    assert hasattr(client, 'get_version')
    assert hasattr(client, 'get_item')
    assert hasattr(client, 'save_item')
    assert hasattr(client, 'get_items')
    assert hasattr(client, 'get_and_save_items')
    assert hasattr(client, 'async_get_items')
    assert hasattr(client, 'async_get_and_save_items')


def test_config_with_family_custom_default_template(config_with_family_custom_default_template):
    client = config_with_family_custom_default_template.fit_class()
    assert hasattr(client, 'get_index')
    assert hasattr(client, 'get_version')
    assert hasattr(client, 'get_item')
    assert hasattr(client, 'save_item')
    assert hasattr(client, 'get_items')
    assert hasattr(client, 'save_items')
    assert hasattr(client, 'async_get_items')
    assert hasattr(client, 'async_get_and_save_items')
