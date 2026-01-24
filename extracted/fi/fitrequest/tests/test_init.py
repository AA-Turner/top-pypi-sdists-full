import os
from importlib.metadata import version

import pytest
from fixtures import Config, config, config_with_auto_version, config_with_url
from pydantic_core import ValidationError

from fitrequest.errors import UnexpectedNoneBaseURLError
from fitrequest.method_config import MethodConfig


def test_client_name(config_with_url):
    assert config_with_url.client_name == 'client_with_url'


def test_config_without_base_url(config):
    with pytest.raises(UnexpectedNoneBaseURLError):
        assert config.fit_class().session.request(MethodConfig(name='test', endpoint='/'))


@pytest.mark.asyncio
async def test_async_config_without_base_url(config):
    with pytest.raises(UnexpectedNoneBaseURLError):
        assert await config.fit_class().session.async_request(MethodConfig(name='test', endpoint='/'))


def test_base_url(config_with_url):
    assert str(config_with_url.base_url) == 'https://test.skillcorner'


def test_base_url_set_as_environment_variable(config):
    os.environ['CLIENT_BASE_URL'] = 'https://downloadmoreram.com/'
    assert str(config.base_url) == 'https://downloadmoreram.com/'
    os.environ.pop('CLIENT_BASE_URL')


def test_client_version(config, config_with_url, config_with_auto_version):
    assert config.version == '0.0.1'
    assert config_with_url.version == '{version}'
    assert config_with_auto_version.version == version('fitrequest')


def test_forbidden_extra_attributes():
    with pytest.raises(ValidationError):
        Config(cowsay='moooh')
