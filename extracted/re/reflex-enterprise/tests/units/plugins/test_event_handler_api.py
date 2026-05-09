"""Unit tests for the EventHandlerAPIPlugin."""

import inspect
import json
from typing import Any, Optional
from unittest.mock import Mock

import pytest
from reflex.app import App
from reflex.plugins.base import Plugin

from reflex_enterprise.app import AppEnterprise
from reflex_enterprise.plugins.event_handler_api import (
    EventHandlerAPIPlugin,
    _build_endpoint_docstring,
    _python_type_to_openapi_schema,
)


class _Custom:
    """Unrecognised type used in schema tests."""


@pytest.mark.parametrize(
    "annotation, expected",
    [
        (str, {"type": "string"}),
        (int, {"type": "integer"}),
        (float, {"type": "number"}),
        (bool, {"type": "boolean"}),
        (bytes, {"type": "string", "format": "byte"}),
        (list[str], {"type": "array", "items": {"type": "string"}}),
        (list[int], {"type": "array", "items": {"type": "integer"}}),
        (list, {}),
        (
            dict[str, int],
            {"type": "object", "additionalProperties": {"type": "integer"}},
        ),
        (
            dict[str, str],
            {"type": "object", "additionalProperties": {"type": "string"}},
        ),
        (str | None, {"type": "string", "nullable": True}),
        (Optional[int], {"type": "integer", "nullable": True}),
        (float | None, {"type": "number", "nullable": True}),
        (Any, {}),
        (inspect.Parameter.empty, {}),
        (_Custom, {}),
        (
            list[list[str]],
            {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
        ),
        (
            dict[str, list[int]],
            {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "integer"},
                },
            },
        ),
    ],
    ids=[
        "str",
        "int",
        "float",
        "bool",
        "bytes",
        "list[str]",
        "list[int]",
        "bare_list",
        "dict[str,int]",
        "dict[str,str]",
        "str|None",
        "Optional[int]",
        "float|None",
        "Any",
        "Parameter.empty",
        "unknown_type",
        "list[list[str]]",
        "dict[str,list[int]]",
    ],
)
def test_python_type_to_openapi_schema(annotation, expected):
    assert _python_type_to_openapi_schema(annotation) == expected


def _make_mock_handler(
    fn,
    state=None,
    parameters: dict[str, inspect.Parameter] | None = None,
):
    """Create a mock registered event handler wrapping a real function."""
    if parameters is None:
        sig = inspect.signature(fn)
        parameters = dict(sig.parameters)

    handler = Mock()
    handler.fn = fn
    handler.state = state
    handler.get_parameters.return_value = parameters

    reh = Mock()
    reh.handler = handler
    return reh


def test_docstring_no_params():
    def my_handler():
        pass

    doc = json.loads(_build_endpoint_docstring(_make_mock_handler(my_handler)))

    assert doc["summary"] == "my_handler"
    # A requestBody is emitted even with no params so OpenAPI linters don't
    # flag the POST as missing both a body and parameters.
    assert doc["requestBody"]["required"] is False
    schema = doc["requestBody"]["content"]["application/json"]["schema"]
    assert schema["type"] == "object"
    assert schema["properties"] == {}
    assert "required" not in schema
    assert "200" in doc["responses"]
    assert "401" in doc["responses"]


def test_docstring_description_falls_back_to_summary():
    def only_summary():
        """Just a one-liner."""

    doc = json.loads(_build_endpoint_docstring(_make_mock_handler(only_summary)))
    # Summary must mirror the docstring AND description must be non-empty,
    # so it falls back to the summary when there is no extended description.
    assert doc["summary"] == "Just a one-liner."
    assert doc["description"] == "Just a one-liner."


def test_docstring_operation_id_and_tags_when_state_provided():
    def save(self, x: int):
        """Save a value."""

    doc = json.loads(
        _build_endpoint_docstring(
            _make_mock_handler(save, state=object),
            state_class_name="TicketState",
        )
    )
    assert doc["operationId"] == "TicketState_save"
    assert doc["tags"] == ["TicketState"]


def test_docstring_no_operation_id_without_state_name():
    def save(self, x: int):
        """Save a value."""

    doc = json.loads(_build_endpoint_docstring(_make_mock_handler(save, state=object)))
    assert "operationId" not in doc
    assert "tags" not in doc


def test_docstring_summary_from_docstring():
    def greet():
        """Say hello to the user."""

    doc = json.loads(_build_endpoint_docstring(_make_mock_handler(greet)))
    assert doc["summary"] == "Say hello to the user."


def test_docstring_filters_args_section():
    def do_thing(x: int):
        """Do a thing.

        Some extra context.

        Args:
            x: The value.
        """

    doc = json.loads(_build_endpoint_docstring(_make_mock_handler(do_thing)))
    assert doc["summary"] == "Do a thing."
    assert "Args:" not in doc["description"]
    assert "Some extra context." in doc["description"]


def test_docstring_required_param():
    def set_name(self, name: str):
        """Set the name."""

    doc = json.loads(
        _build_endpoint_docstring(_make_mock_handler(set_name, state=object))
    )
    schema = doc["requestBody"]["content"]["application/json"]["schema"]

    assert doc["requestBody"]["required"] is True
    assert schema["properties"]["name"] == {"type": "string"}
    assert "name" in schema["required"]


def test_docstring_optional_param_with_default():
    def set_count(self, count: int = 10):
        """Set the count."""

    doc = json.loads(
        _build_endpoint_docstring(_make_mock_handler(set_count, state=object))
    )
    schema = doc["requestBody"]["content"]["application/json"]["schema"]

    assert doc["requestBody"]["required"] is False
    assert schema["properties"]["count"] == {"type": "integer", "default": 10}
    assert "required" not in schema


def test_docstring_mixed_required_and_optional():
    def update(self, key: str, value: str = "default"):
        """Update a key."""

    doc = json.loads(
        _build_endpoint_docstring(_make_mock_handler(update, state=object))
    )
    schema = doc["requestBody"]["content"]["application/json"]["schema"]

    assert "key" in schema["required"]
    assert "value" not in schema["required"]
    assert schema["properties"]["value"]["default"] == "default"


def test_docstring_dynamic_route_args():
    def my_handler():
        pass

    doc = json.loads(
        _build_endpoint_docstring(
            _make_mock_handler(my_handler),
            dynamic_route_args={"user_id": "string"},
        )
    )
    assert doc["parameters"] == [{"$ref": "#/components/parameters/route_user_id"}]


def test_docstring_no_dynamic_route_args():
    def my_handler():
        pass

    doc = json.loads(_build_endpoint_docstring(_make_mock_handler(my_handler)))
    assert "parameters" not in doc


def test_docstring_non_serialisable_default_excluded():
    sentinel = object()

    def handler(self, data: str = sentinel):  # type: ignore[assignment]
        pass

    doc = json.loads(
        _build_endpoint_docstring(_make_mock_handler(handler, state=object))
    )
    schema = doc["requestBody"]["content"]["application/json"]["schema"]
    assert "default" not in schema["properties"]["data"]


def test_check_requirements_accepts_app_enterprise():
    assert EventHandlerAPIPlugin()._check_requirements(Mock(spec=AppEnterprise)) is True


def test_check_requirements_rejects_plain_app():
    with pytest.raises(RuntimeError, match="AppEnterprise"):
        EventHandlerAPIPlugin()._check_requirements(Mock(spec=App))


def test_post_compile_skips_when_check_requirements_fails(mocker):
    plugin = EventHandlerAPIPlugin()
    check_requirements_mock = mocker.patch.object(
        plugin, "_check_requirements", return_value=False
    )

    mock_app = Mock(spec=AppEnterprise)
    mock_app._api = Mock()
    plugin.post_compile(app=mock_app)

    check_requirements_mock.assert_called_once_with(mock_app)
    mock_app._api.add_route.assert_not_called()


def test_post_compile_skips_when_no_api(mocker):
    plugin = EventHandlerAPIPlugin()
    mocker.patch.object(plugin, "_check_requirements", return_value=True)

    mock_app = Mock(spec=AppEnterprise)
    mock_app._api = None
    plugin.post_compile(app=mock_app)


def test_post_compile_raises_for_plain_app():
    with pytest.raises(RuntimeError, match="AppEnterprise"):
        EventHandlerAPIPlugin().post_compile(app=Mock(spec=App))


def test_import_from_plugins_package():
    from reflex_enterprise.plugins import EventHandlerAPIPlugin as Cls

    assert Cls is EventHandlerAPIPlugin


def test_import_via_rxe():
    import reflex_enterprise as rxe

    assert rxe.EventHandlerAPIPlugin is EventHandlerAPIPlugin


def test_is_plugin_subclass():
    assert issubclass(EventHandlerAPIPlugin, Plugin)
