import pytest
from django.conf import settings

from wbcore.configs.decorators import register_config
from wbcore.configs.registry import ConfigRegistry
from wbcore.configs.views import ConfigAPIView


def test_registry(config_registry: ConfigRegistry, api_request):
    configs = config_registry.get_config_dict(api_request)
    assert configs.keys()


def test_release_note_config(config_registry: ConfigRegistry, api_request):
    release_notes = config_registry.get_config_dict(api_request)["release_notes"]
    assert release_notes["endpoint"]
    assert release_notes["unread_release_notes"]


def test_menu_config(config_registry: ConfigRegistry, api_request):
    menu = config_registry.get_config_dict(api_request)["menu"]
    assert menu


def test_share_config(config_registry: ConfigRegistry, api_request):
    share = config_registry.get_config_dict(api_request)["share"]
    assert share


def test_menu_calendar_config(config_registry: ConfigRegistry, api_request):
    menu_calendar = config_registry.get_config_dict(api_request)["menu_calendar"]
    assert menu_calendar


@pytest.mark.parametrize("text, version", [("Foo bar", "Foo")])
def test_beta_button_config(config_registry: ConfigRegistry, text, version, api_request):
    settings.BETA_BUTTON_VERSION = version
    settings.BETA_BUTTON_TEXT = text
    beta_calendar = config_registry.get_config_dict(api_request)["beta_button"]
    assert beta_calendar["url"] == f"{settings.CDN_BASE_ENDPOINT_URL}/{version}/main.js"
    assert beta_calendar["text"] == text


def test_config_registry_decorator():
    def some_callable():
        pass

    assert not hasattr(some_callable, "_is_config")
    some_callable = register_config(some_callable)
    assert some_callable._is_config


def test_config_view(rf):
    request = rf.get("/")
    view = ConfigAPIView.as_view()
    response = view(request)

    assert response.status_code == 200
