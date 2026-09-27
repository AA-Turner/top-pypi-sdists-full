import inspect
import math

import pytest

from datastar_py import action_generator as actions
from datastar_py import attribute_generator as ds

FETCH_METHODS = [
    actions.get,
    actions.post,
    actions.put,
    actions.patch,
    actions.delete,
]


@pytest.mark.parametrize("method", FETCH_METHODS)
def test_fetch_methods_serialize_literal_urls(method) -> None:
    url = "/a'\"\\\n/$token/雪/_!EXPR!_"
    assert method(url) == f'@{method.__name__}("/a\'\\"\\\\\\n/$token/\\u96ea/_!EXPR!_")'


def test_fetch_options_serialize_with_javascript_types() -> None:
    assert actions.post(
        ds.JSExpression('"/expression"'),
        content_type="json",
        headers={
            "literal": 'quoted "text"',
            "expression": ds.JSExpression('"a" + "b"'),
        },
        open_when_hidden=False,
        payload={"nested": [True, None, ds.JSExpression("1 + 2")]},
        retry="never",
        retry_interval=0,
        retry_scaler=1.5,
        retry_max_wait=20,
        retry_max_count=0,
        request_cancellation=ds.JSExpression("controller"),
        include_signals=r"^a/\w+\n",
        exclude_signals=ds.JSExpression(r"/private/i"),
    ) == (
        '@post(("/expression"), {"contentType": "json", '
        '"headers": {"literal": "quoted \\"text\\"", "expression": ("a" + "b")}, '
        '"openWhenHidden": false, "payload": {"nested": [true, null, (1 + 2)]}, '
        '"retry": "never", "retryInterval": 0, "retryScaler": 1.5, '
        '"retryMaxWait": 20, "retryMaxCount": 0, '
        '"requestCancellation": (controller), '
        '"filterSignals": {"include": (new RegExp("^a/\\\\w+\\\\n")), '
        '"exclude": (/private/i)}})'
    )


@pytest.mark.parametrize("method", FETCH_METHODS)
def test_none_omits_options_and_expressions_can_send_null(method) -> None:
    options = {name: None for name in inspect.signature(method).parameters if name != "url"}
    assert method("/", **options) == method("/")
    assert method("/", payload=ds.JSExpression("null")) == (
        f'@{method.__name__}("/", {{"payload": (null)}})'
    )


def test_form_and_empty_options_are_preserved() -> None:
    assert actions.post("/", content_type="form", selector="#form") == (
        '@post("/", {"contentType": "form", "selector": "#form"})'
    )
    assert actions.get(
        "/", open_when_hidden=False, retry_max_count=0, headers={}, include_signals=""
    ) == (
        '@get("/", {"headers": {}, "openWhenHidden": false, "retryMaxCount": 0, '
        '"filterSignals": {"include": (new RegExp(""))}})'
    )


def test_signal_actions_serialize_data_expressions_and_filters() -> None:
    assert actions.set_all(
        {"literal": "$token", "expression": ds.JSExpression("1 + 1")},
        include="^public",
        exclude="private",
    ) == (
        '@setAll({"literal": "$token", "expression": (1 + 1)}, '
        '{"include": (new RegExp("^public")), '
        '"exclude": (new RegExp("private"))})'
    )
    assert actions.toggle_all() == "@toggleAll()"
    assert actions.peek(ds.JSExpression("{answer: 42}")) == ("@peek(() => ({answer: 42}))")


def test_fetch_signatures_expose_the_same_keyword_only_options() -> None:
    expected = inspect.signature(actions.get)
    for method in FETCH_METHODS:
        assert inspect.signature(method) == expected
        assert all(
            parameter.kind == inspect.Parameter.KEYWORD_ONLY
            for name, parameter in expected.parameters.items()
            if name != "url"
        )
        with pytest.raises(TypeError):
            method("/", not_defined_kwarg=True)


@pytest.mark.parametrize(
    ("options", "error", "message"),
    (
        ({"content_type": "xml"}, ValueError, "content_type"),
        ({"retry": "sometimes"}, ValueError, "retry"),
        ({"request_cancellation": "controller"}, ValueError, "request_cancellation"),
        ({"open_when_hidden": 0}, TypeError, "open_when_hidden"),
        ({"headers": []}, TypeError, "headers"),
        ({"headers": {1: "value"}}, TypeError, "header name"),
        ({"headers": {"X-Value": False}}, TypeError, "header values"),
        ({"include_signals": []}, TypeError, "include"),
        ({"selector": ""}, ValueError, "selector"),
        ({"selector": "#form"}, ValueError, "content_type='form'"),
        ({"content_type": "form", "payload": {}}, ValueError, "payload"),
        ({"retry_interval": True}, TypeError, "retry_interval"),
        ({"retry_max_count": -1}, ValueError, "retry_max_count"),
        ({"retry_scaler": "2"}, TypeError, "retry_scaler"),
        ({"retry_scaler": math.inf}, ValueError, "retry_scaler"),
    ),
)
def test_fetch_validation(options, error, message) -> None:
    with pytest.raises(error, match=message):
        actions.post("/", **options)


@pytest.mark.parametrize(("url", "error"), ((None, TypeError), ("", ValueError)))
def test_url_validation(url, error) -> None:
    with pytest.raises(error, match="url"):
        actions.get(url)


def test_action_wrapper_validation() -> None:
    assert not hasattr(actions, "JSRegex")
    with pytest.raises(TypeError, match="JSExpression"):
        actions.peek("$token")
