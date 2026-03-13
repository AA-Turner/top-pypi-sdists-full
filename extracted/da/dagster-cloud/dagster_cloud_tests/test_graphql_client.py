import base64
import json
import platform
import re
import time
from contextlib import nullcontext
from email.utils import formatdate
from unittest import mock

import freezegun
import httpretty
import pytest
from dagster._core.events import DagsterEvent, DagsterEventType, EngineEventData
from dagster._core.events.log import EventLogEntry
from dagster._core.test_utils import environ
from dagster_cloud.storage.client import DEFAULT_RETRIES
from dagster_cloud.version import __version__
from dagster_cloud_cli.core.errors import DagsterCloudAgentServerError
from dagster_cloud_cli.core.headers.impl import (
    API_TOKEN_HEADER,
    DAGSTER_CLOUD_VERSION_HEADER,
    PYTHON_VERSION_HEADER,
)
from urllib3.connectionpool import HTTPConnectionPool
from urllib3.exceptions import ConnectTimeoutError, SSLError

from dagster_cloud_tests import gen_agent_instance


@pytest.fixture(
    params=["graphql", "http"],
)
def api_protocol(request):
    with (
        environ({"DAGSTER_CLOUD_STORE_EVENT_OVER_HTTP": "1"})
        if request.param == "http"
        else nullcontext()
    ):
        yield request.param


@pytest.fixture
def graphql_url(dagster_cloud_url, api_protocol):
    if api_protocol == "graphql":
        return dagster_cloud_url + "/graphql"
    else:
        return dagster_cloud_url + "/store_events"


@pytest.fixture
def agent_instance(agent_token, dagster_cloud_url):
    with gen_agent_instance(dagster_cloud_url, agent_token) as instance:
        yield instance


@pytest.fixture
def proxy_graphql_client(agent_instance):
    return agent_instance.graphql_client


def test_graphql_client_headers(proxy_graphql_client, agent_token):
    headers = proxy_graphql_client.headers
    assert headers[DAGSTER_CLOUD_VERSION_HEADER] == __version__
    assert headers[PYTHON_VERSION_HEADER] == platform.python_version()
    assert headers[API_TOKEN_HEADER] == agent_token


@pytest.fixture
def fake_sleeps(monkeypatch):
    sleeps = []

    def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(time, "sleep", fake_sleep)

    yield sleeps


def create_test_event_log_record(message: str, run_id):
    return


def _store_event(agent_instance):
    event_log_entry = EventLogEntry(
        error_info=None,
        user_message="hello",
        level="debug",
        run_id="fake-run-id",
        timestamp=time.time(),
        dagster_event=DagsterEvent(
            DagsterEventType.ENGINE_EVENT.value,
            "nonce",
            event_specific_data=EngineEventData.in_process(999),
        ),
    )
    agent_instance.event_log_storage.store_event(event_log_entry)


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_backoff_succeeds(agent_instance, fake_sleeps, graphql_url):
    num_callbacks = {"num": 0}
    good_result = {"data": "youdidit"}

    def my_callback(_request, _url: str, headers: dict):
        num_callbacks["num"] = num_callbacks["num"] + 1
        if num_callbacks["num"] > 3:
            return (200, headers, json.dumps(good_result))

        return (502, headers, "")

    httpretty.register_uri(httpretty.POST, graphql_url, body=my_callback)

    _store_event(agent_instance)

    assert num_callbacks["num"] == 4
    assert fake_sleeps == [1, 2, 4]


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_429(agent_instance, fake_sleeps, graphql_url):
    num_callbacks = {"num": 0}
    good_result = {"data": "youdidit"}

    def my_callback(_request, _url: str, headers: dict):
        num_callbacks["num"] = num_callbacks["num"] + 1
        if num_callbacks["num"] > 3:
            return (200, headers, json.dumps(good_result))

        headers["Retry-After"] = "10"
        return (429, headers, "")

    httpretty.register_uri(httpretty.POST, graphql_url, body=my_callback)

    _store_event(agent_instance)

    assert num_callbacks["num"] == 4
    assert fake_sleeps == [10, 10, 10]


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_429_date(agent_instance, fake_sleeps, graphql_url):
    num_callbacks = {"num": 0}
    good_result = {"data": "youdidit"}

    with freezegun.freeze_time("2023-01-01"):
        now = time.time()
        future = now + 10

        def my_callback(_request, _url: str, headers: dict):
            num_callbacks["num"] = num_callbacks["num"] + 1
            if num_callbacks["num"] > 1:
                return (200, headers, json.dumps(good_result))

            headers["Retry-After"] = formatdate(future, usegmt=True)
            return (429, headers, "")

        httpretty.register_uri(httpretty.POST, graphql_url, body=my_callback)

        _store_event(agent_instance)

        assert num_callbacks["num"] == 2
        assert fake_sleeps == [10]


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_429_bad_retry_after(agent_instance, fake_sleeps, graphql_url):
    num_callbacks = {"num": 0}
    good_result = {"data": "youdidit"}

    def my_callback(_request, _url: str, headers: dict):
        num_callbacks["num"] = num_callbacks["num"] + 1
        if num_callbacks["num"] > 3:
            return (200, headers, json.dumps(good_result))
        elif num_callbacks["num"] > 2:
            headers["Retry-After"] = "junk"
        elif num_callbacks["num"] > 1:
            headers["Retry-After"] = "-1"

        return (429, headers, "")

    httpretty.register_uri(httpretty.POST, graphql_url, body=my_callback)

    _store_event(agent_instance)

    assert num_callbacks["num"] == 4
    assert fake_sleeps == [1, 2, 4]


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_backoff_fails(agent_instance, fake_sleeps, graphql_url):
    num_callbacks = {"num": 0}

    def my_callback(_request, _url: str, headers: dict):
        num_callbacks["num"] = num_callbacks["num"] + 1
        return (502, headers, "")

    httpretty.register_uri(httpretty.POST, graphql_url, body=my_callback)

    with pytest.raises(
        DagsterCloudAgentServerError, match=re.escape("too many 502 error responses")
    ):
        _store_event(agent_instance)

    assert num_callbacks["num"] == DEFAULT_RETRIES + 1
    assert fake_sleeps == [1, 2, 4, 8, 16, 32]


@httpretty.activate(allow_net_connect=False, verbose=True)
@pytest.mark.parametrize(
    "error_cls, error_args",
    [
        (SSLError, ()),
        (ConnectTimeoutError, ()),
        (ConnectionResetError, (104, "Connection reset by peer")),
    ],
)
def test_graphql_client_connection_retry_succeeds(
    agent_instance, fake_sleeps, error_cls, error_args, graphql_url
):
    orig_make_request = HTTPConnectionPool._make_request  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]

    num_callbacks = {"num": 0}
    good_result = {"data": "youdidit"}
    httpretty.register_uri(httpretty.POST, graphql_url, status=200, body=json.dumps(good_result))

    def fake_http_request(*args, **kwargs):
        num_callbacks["num"] = num_callbacks["num"] + 1

        if num_callbacks["num"] > 5:
            return orig_make_request(*args, **kwargs)

        raise error_cls(*error_args)

    with mock.patch.object(HTTPConnectionPool, "_make_request", new=fake_http_request):
        _store_event(agent_instance)

        assert num_callbacks["num"] == 6
        assert fake_sleeps == [1, 2, 4, 8, 16]


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_connection_reset_retry_fails(agent_instance, fake_sleeps, graphql_url):
    num_callbacks = {"num": 0}
    good_result = {"data": "youdidit"}
    httpretty.register_uri(httpretty.POST, graphql_url, status=200, body=json.dumps(good_result))

    def fake_http_request(*_args, **_kwargs):
        num_callbacks["num"] = num_callbacks["num"] + 1
        raise ConnectionResetError(104, "Connection reset by peer")

    with mock.patch.object(HTTPConnectionPool, "_make_request", new=fake_http_request):
        with pytest.raises(
            DagsterCloudAgentServerError, match=re.escape("Connection reset by peer")
        ):
            _store_event(agent_instance)

        assert num_callbacks["num"] == DEFAULT_RETRIES + 1
        assert fake_sleeps == [1, 2, 4, 8, 16, 32]


@httpretty.activate(allow_net_connect=False, verbose=True)
def test_graphql_client_metrics(agent_instance, fake_sleeps, graphql_url, monkeypatch):
    metric_headers = []

    def my_callback(_request, _url: str, headers: dict):
        metric_header = _request.headers.get("Dagster-Cloud-Metric")
        if metric_header:
            metric_headers.append(json.loads(base64.b64decode(metric_header)))
        else:
            metric_headers.append(None)

        return (200, headers, json.dumps({"data": "good"}))

    httpretty.register_uri(httpretty.POST, graphql_url, body=my_callback)
    monkeypatch.setenv("DISABLE_DAGSTER_CLOUD_STORE_EVENT_SEND_METRICS", "1")
    _store_event(agent_instance)
    monkeypatch.delenv("DISABLE_DAGSTER_CLOUD_STORE_EVENT_SEND_METRICS")
    _store_event(agent_instance)
    _store_event(agent_instance)
    monkeypatch.setenv("DISABLE_DAGSTER_CLOUD_STORE_EVENT_SEND_METRICS", "1")
    _store_event(agent_instance)

    assert metric_headers[0] is None
    assert metric_headers[1] is None, (
        "First event after we start recording will not have metric of previous event"
    )
    assert metric_headers[2], "expected metric of previous event"
    assert metric_headers[2]["_name"] == "store-event"
    assert metric_headers[2]["_duration"] > 0
    assert metric_headers[2]["event_type"] == "ENGINE_EVENT"
    assert metric_headers[2]["run_id"] == "fake-run-id"
    assert metric_headers[3] is None, "No metric sent after env turned off"
