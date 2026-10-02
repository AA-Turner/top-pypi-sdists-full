"""Mobile-web localStorage verbs over the visible CDP channel."""
import logging

import pytest

from testmu_appium import _action_web, _vars
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers.local_storage import (
    clear_local_storage,
    delete_local_storage,
    set_local_storage,
)


class _Driver:
    current_package = "com.android.chrome"


class _Channel:
    def __init__(self, error=None):
        self.calls = []
        self.error = error

    def call_function(self, function, arguments=()):
        self.calls.append((function, arguments))
        if self.error is not None:
            raise self.error


@pytest.fixture(autouse=True)
def _clear_vars():
    yield
    _vars.clear_state()


def _use(monkeypatch, channel):
    seen = []

    def visible(package):
        seen.append(package)
        return channel

    monkeypatch.setattr(_action_web, "visible_channel", visible)
    return seen


def test_set_resolves_runtime_values_as_strings_and_uses_structured_arguments(
        monkeypatch):
    channel = _Channel()
    seen = _use(monkeypatch, channel)
    _vars.set_var("token", 12345)
    items = {
        "token": "{{token}}",
        "hostile": "'; localStorage.clear(); //",
    }

    set_local_storage(_Driver(), items)

    assert seen == ["com.android.chrome"]
    assert len(channel.calls) == 1
    function, arguments = channel.calls[0]
    assert "localStorage.setItem" in function
    assert "12345" not in function
    assert "localStorage.clear(); //" not in function
    assert arguments == ({
        "token": "12345",
        "hostile": "'; localStorage.clear(); //",
    },)


def test_set_does_not_mutate_the_recorded_items(monkeypatch):
    channel = _Channel()
    _use(monkeypatch, channel)
    items = {"token": "{{token}}"}

    set_local_storage(_Driver(), items)

    assert items == {"token": "{{token}}"}


def test_delete_passes_copied_keys_as_a_structured_argument(monkeypatch):
    channel = _Channel()
    seen = _use(monkeypatch, channel)
    keys = ["token", "theme"]

    delete_local_storage(_Driver(), keys)

    assert seen == ["com.android.chrome"]
    function, arguments = channel.calls[0]
    assert "localStorage.removeItem" in function
    assert "token" not in function
    assert arguments == (["token", "theme"],)
    assert arguments[0] is not keys


def test_clear_operates_on_the_current_origin_without_arguments(monkeypatch):
    channel = _Channel()
    seen = _use(monkeypatch, channel)

    clear_local_storage(_Driver())

    assert seen == ["com.android.chrome"]
    function, arguments = channel.calls[0]
    assert "this.localStorage.clear()" in function
    assert arguments == ()


@pytest.mark.parametrize("verb,args", [
    (set_local_storage, ({"a": "b"},)),
    (delete_local_storage, (["a"],)),
    (clear_local_storage, ()),
])
def test_storage_verbs_fail_closed_without_a_visible_channel(
        monkeypatch, verb, args):
    monkeypatch.setattr(_action_web, "visible_channel", lambda package: None)

    with pytest.raises(WebSurfaceUnavailable) as exc:
        verb(_Driver(), *args)

    assert "visible debuggable mobile web surface" in str(exc.value)
    assert "com.android.chrome" in str(exc.value)


@pytest.mark.parametrize("verb,args", [
    (set_local_storage, ({"a": "b"},)),
    (delete_local_storage, (["a"],)),
    (clear_local_storage, ()),
])
def test_storage_verbs_propagate_cdp_errors(monkeypatch, verb, args):
    _use(monkeypatch, _Channel(RuntimeError("CDP failed")))

    with pytest.raises(RuntimeError, match="CDP failed"):
        verb(_Driver(), *args)


@pytest.mark.parametrize("items", [
    None,
    [],
    {},
    {"": "value"},
    {1: "value"},
])
def test_set_rejects_invalid_items_before_opening_a_channel(monkeypatch, items):
    monkeypatch.setattr(
        _action_web,
        "visible_channel",
        lambda package: pytest.fail("invalid input must not open CDP"),
    )

    with pytest.raises(ValueError):
        set_local_storage(_Driver(), items)


@pytest.mark.parametrize("keys", [
    None,
    {},
    [],
    [""],
    [1],
])
def test_delete_rejects_invalid_keys_before_opening_a_channel(monkeypatch, keys):
    monkeypatch.setattr(
        _action_web,
        "visible_channel",
        lambda package: pytest.fail("invalid input must not open CDP"),
    )

    with pytest.raises(ValueError):
        delete_local_storage(_Driver(), keys)


def test_storage_values_are_never_logged(monkeypatch, caplog):
    channel = _Channel()
    _use(monkeypatch, channel)
    caplog.set_level(logging.INFO, logger="testmu_appium")
    secret = "super-secret-storage-value"

    set_local_storage(_Driver(), {"auth": secret}, description=secret)

    assert secret not in caplog.text
    assert "set 1 item(s)" in caplog.text
