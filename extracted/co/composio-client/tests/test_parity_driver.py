"""The shared Python parity invocation, checked against all 116 operations.

``scripts/parity_driver.py`` runs one Python lane of the live harness. The part
of it that can be wrong quietly is invocation spelling. The scenarios and both
Python clients now use the Stainless convention, so the same arguments must be
passed to the pinned and owned lanes.

The invocation is checked over the whole derived corpus rather than a sample:

* the oracle half must reproduce ``wire_corpus.oracle_call`` exactly — the same
  function the committed fixture was captured through;
* the owned half must receive that exact call without a translation table.

Those two are the same logical call, which is the whole premise of the lane.
No network, no client: a recording stand-in answers both.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
from parity_driver import (
    CapturingTransport,
    Operations,
    _request_capture,
    _snake_keys,
    _split_arguments,
    build_client,
    execute,
    oracle_chain_call,
    oracle_raw_call,
    owned_chain_call,
    owned_raw_call,
)
from wire_corpus import COVERAGE_PATH, derived_calls, oracle_call


class Recorder:
    """A stand-in client that resolves any accessor and records the leaf call."""

    def __init__(self) -> None:
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def __getattr__(self, _name: str) -> Recorder:
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append((args, kwargs))

    @property
    def only(self) -> tuple[tuple[Any, ...], dict[str, Any]]:
        assert len(self.calls) == 1, f"expected one call, recorded {len(self.calls)}"
        return self.calls[0]


@pytest.fixture(scope="module")
def operations() -> Operations:
    """Parsing the 4.5 MB spec once serves every case below."""
    return Operations()


def _ts_invocation(call: Any) -> dict[str, Any]:
    """One derived call as a scenario would spell it.

    The scenarios are written in the TypeScript Stainless convention, which is
    the Python Stainless convention too — last path parameter positional, one
    flat options object after it. So the corpus's own oracle spelling *is* the
    scenario spelling, which is why this is the right input to translate from.
    """
    positional, kwargs = oracle_call(call)
    args: list[Any] = [*positional]
    if kwargs:
        args.append(kwargs)
    return {"kind": "chain", "chain": ".".join(call.oracle_accessor), "args": args}


CORPUS = derived_calls()
CASES = [pytest.param(call, id=".".join(call.accessor)) for call in CORPUS]

#: Operation key -> the TypeScript chain a scenario names it by: the oracle's,
#: so without the `_internal` root the owned client moved `x-internal` ones under.
_LOCATIONS: dict[str, list[str]] = {
    entry["key"]: entry["location"][1:] if entry["location"][:1] == ["_internal"] else entry["location"]
    for entry in json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))["operations"]
}


# ---- the two halves reproduce the conventions they claim to ----


@pytest.mark.parametrize("call", CASES)
def test_the_oracle_half_reproduces_the_pinned_clients_own_calling_convention(
    call: Any, operations: Operations
) -> None:
    """The fixture in ``tests/fixtures/stainless_wire_oracle.json`` was captured
    through ``oracle_call``. A lane that spelled the oracle's calls differently
    would be comparing something the fixture never vouched for."""
    recorder = Recorder()

    oracle_chain_call(recorder, _ts_invocation(call), operations.for_key(call.key))

    assert recorder.only == oracle_call(call)


@pytest.mark.parametrize("call", CASES)
def test_the_owned_half_receives_the_same_stainless_invocation(call: Any, operations: Operations) -> None:
    """No owned-only body/query/path repacking remains in the live lane."""
    operation = operations.for_key(call.key)
    recorder = Recorder()

    owned_chain_call(recorder, _ts_invocation(call), operation)

    assert recorder.only == oracle_call(call)


def test_the_shared_corpus_is_the_whole_covered_surface() -> None:
    """A guard against the two parametrizations above quietly shrinking."""
    assert len(CORPUS) == 116


@pytest.mark.parametrize("lane", ["stainless", "owned"])
def test_execute_resolves_relocated_operations_on_each_lane(lane: str, operations: Operations) -> None:
    transport = CapturingTransport()
    transport._inner = httpx.MockTransport(lambda request: httpx.Response(200, json={"id": "session_1"}))  # noqa: SLF001

    with httpx.Client(base_url="https://api.test", transport=transport) as http_client:

        def get_session(*, id: str) -> httpx.Response:
            return http_client.get("/api/v3.1/cli/get-session", params={"id": id})

        cli = SimpleNamespace(get_session=get_session)
        client = {
            "stainless": SimpleNamespace(cli=cli),
            "owned": SimpleNamespace(_internal=SimpleNamespace(cli=cli)),
        }[lane]
        exchange = execute(
            lane,
            client,
            transport,
            operations,
            {"invocation": {"kind": "chain", "chain": "cli.getSession", "args": [{"id": "session_1"}]}},
        )

    assert exchange["exchangeCount"] == 1
    assert exchange["transportError"] is None
    assert exchange["request"]["method"] == "GET"
    assert exchange["request"]["path"] == "/api/v3.1/cli/get-session"
    assert exchange["request"]["query"] == "id=session_1"
    assert exchange["response"]["status"] == 200


# ---- the one operation whose body and query collide ----


def test_the_prefixed_collision_stays_flat_for_the_owned_lane(operations: Operations) -> None:
    key = "post /api/v3.1/connected_accounts/{nanoid}/refresh"
    invocation = {
        "kind": "chain",
        "chain": "connectedAccounts.refresh",
        "args": ["ca_1", {"body_redirect_url": "https://body", "query_redirect_url": "https://query"}],
    }
    recorder = Recorder()

    owned_chain_call(recorder, invocation, operations.for_key(key))

    assert recorder.only == (
        ("ca_1",),
        {"body_redirect_url": "https://body", "query_redirect_url": "https://query"},
    )


# ---- the one body whose two wire properties collide in Python ----


def test_the_oracles_numbered_collision_is_spelled_for_it(operations: Operations) -> None:
    """`trigger_instances.upsert` declares both `triggerConfig` and
    `trigger_config`, and both become `trigger_config` in Python. The oracle
    resolves that by position, so neither can be named by its wire spelling and
    a scenario written in wire names reaches the wrong one — or, as the first
    live run showed, no keyword the method accepts at all."""
    key = "post /api/v3.1/trigger_instances/{slug}/upsert"
    invocation = {
        "kind": "chain",
        "chain": "triggerInstances.upsert",
        "args": ["SLUG", {"connected_account_id": "ca_1", "trigger_config": {}}],
    }
    recorder = Recorder()

    oracle_chain_call(recorder, invocation, operations.for_key(key))

    # `body_trigger_config_1` is the one that reaches the wire as
    # `trigger_config`; `_2` is `triggerConfig`.
    assert recorder.only == (("SLUG",), {"connected_account_id": "ca_1", "body_trigger_config_1": {}})


def test_the_owned_lane_uses_the_same_numbered_collision_name(operations: Operations) -> None:
    key = "post /api/v3.1/trigger_instances/{slug}/upsert"
    invocation = {
        "kind": "chain",
        "chain": "triggerInstances.upsert",
        "args": ["SLUG", {"connected_account_id": "ca_1", "trigger_config": {}}],
    }
    recorder = Recorder()

    owned_chain_call(recorder, invocation, operations.for_key(key))

    assert recorder.only == (
        ("SLUG",),
        {"connected_account_id": "ca_1", "body_trigger_config_1": {}},
    )


# ---- the parameters that ride in headers ----


def test_a_declared_header_parameter_stays_flat_on_the_owned_lane(operations: Operations) -> None:
    key = "get /api/v3.1/org/consumer/connected_toolkits"
    invocation = {
        "kind": "chain",
        "chain": "org.consumer.listConnectedToolkits",
        "args": [{"x_user_api_key": "uk_1", "x_org_id": "org_1"}],
    }
    recorder = Recorder()

    owned_chain_call(recorder, invocation, operations.for_key(key))

    assert recorder.only == ((), {"x_user_api_key": "uk_1", "x_org_id": "org_1"})


def test_the_same_call_stays_flat_on_the_oracle_lane(operations: Operations) -> None:
    key = "get /api/v3.1/org/consumer/connected_toolkits"
    invocation = {
        "kind": "chain",
        "chain": "org.consumer.listConnectedToolkits",
        "args": [{"x_user_api_key": "uk_1", "x_org_id": "org_1"}],
    }
    recorder = Recorder()

    oracle_chain_call(recorder, invocation, operations.for_key(key))

    assert recorder.only == ((), {"x_user_api_key": "uk_1", "x_org_id": "org_1"})


def test_the_corpus_actually_carries_the_header_operations() -> None:
    """The parametrized cases above assert on ``headers`` only where the corpus
    samples one, so a corpus that stopped sampling them would keep passing while
    covering nothing. These three are the operations that declare a *required*
    header parameter; ``tools.execute``'s is optional, which is why it is not
    here. Two of them declare ``x-user-api-key``, a name that is also a
    credential scheme's header — the client suppresses its own credential beside
    it, which ``test_credential_scheme.py`` owns and this must not disturb."""
    assert {".".join(call.oracle_accessor) for call in CORPUS if call.headers} == {
        "cli.create_codact_failure",
        "org.consumer.list_connected_toolkits",
        "org.consumer.project.resolve",
    }


# ---- refusals ----


def test_a_leading_path_parameter_the_scenario_omits_is_refused(operations: Operations) -> None:
    """`files.list(mount_id, {session_id})` — drop `session_id` and the owned
    lane would have nothing to put in the first path segment. Substituting a
    blank would dispatch to a different URL and still capture cleanly."""
    key = "get /api/v3.1/tool_router/session/{session_id}/mounts/{mountID}/items"
    invocation = {"kind": "chain", "chain": "toolRouter.session.files.list", "args": ["m1", {"limit": 5}]}

    with pytest.raises(ValueError, match="needs path parameter"):
        owned_chain_call(Recorder(), invocation, operations.for_key(key))


def test_too_many_positional_arguments_are_refused(operations: Operations) -> None:
    key = "get /api/v3.1/auth_configs/{nanoid}"
    invocation = {"kind": "chain", "chain": "authConfigs.retrieve", "args": ["a", {}, {}]}

    with pytest.raises(ValueError, match="the calling convention allows one options object"):
        _split_arguments(invocation, operations.for_key(key))


def test_a_non_object_where_the_options_object_belongs_is_refused(operations: Operations) -> None:
    key = "get /api/v3.1/auth_configs/{nanoid}"
    invocation = {"kind": "chain", "chain": "authConfigs.retrieve", "args": ["a", "not-an-object"]}

    with pytest.raises(ValueError, match="expects an options object"):
        _split_arguments(invocation, operations.for_key(key))


def test_an_accessor_the_client_does_not_expose_is_refused(operations: Operations) -> None:
    """The four operations the pinned client has no typed method for must reach
    the escape hatch. Reporting the accessor as missing is how a scenario that
    forgot to is caught, rather than the lane silently running 60 of 64."""

    class Empty:
        pass

    key = "post /api/v3.1/auth_configs"
    invocation = {"kind": "chain", "chain": "authConfigs.create", "args": [{}]}

    with pytest.raises(ValueError, match="exposes no auth_configs.create"):
        oracle_chain_call(Empty(), invocation, operations.for_key(key))


def test_an_operation_outside_the_covered_surface_is_refused(operations: Operations) -> None:
    with pytest.raises(KeyError, match="no covered operation"):
        operations.for_key("get /api/v3.1/not_an_endpoint")


def test_a_chain_the_coverage_map_does_not_record_is_refused(operations: Operations) -> None:
    with pytest.raises(KeyError, match="no covered operation is reached by"):
        operations.for_chain("authConfigs.notAMethod")


# ---- the bridge between the two languages ----


@pytest.mark.parametrize("call", CASES)
def test_every_covered_operation_is_reachable_by_its_typescript_chain(
    call: Any, operations: Operations
) -> None:
    """An ``Invocation`` carries a dotted chain and nothing else, so the lane
    can only find an operation by the ``location`` ``surface-coverage.json``
    records beside the Python ``accessor``. That file is the bridge between the
    two languages, and it is the generator that writes it — this asserts it
    actually spans, rather than a table kept by hand here."""
    chain = ".".join(_LOCATIONS[call.key])

    assert operations.for_chain(chain) is operations.for_key(call.key)


# ---- the shared raw escape hatch ----


def test_the_raw_call_is_spelled_the_same_way_on_both_lanes() -> None:
    invocation = {
        "kind": "raw",
        "method": "GET",
        "path": "/api/v3.1/webhook_subscriptions",
        "query": {"limit": 5},
    }

    oracle, owned = Recorder(), Recorder()
    oracle_raw_call(oracle, invocation)
    owned_raw_call(owned, invocation)

    assert oracle.only == (
        ("/api/v3.1/webhook_subscriptions",),
        {"cast_to": object, "options": {"params": {"limit": 5}}},
    )
    assert owned.only == oracle.only


def test_a_raw_body_is_passed_through_on_both_lanes() -> None:
    invocation = {
        "kind": "raw",
        "method": "POST",
        "path": "/api/v3.1/webhook_subscriptions",
        "body": {"webhook_url": "https://sink", "enabled_events": ["composio.trigger.message"]},
    }

    oracle, owned = Recorder(), Recorder()
    oracle_raw_call(oracle, invocation)
    owned_raw_call(owned, invocation)

    assert oracle.only[1]["body"] == invocation["body"]
    assert owned.only[1]["body"] == invocation["body"]


# ---- key spelling ----


def test_nested_keys_are_respelled_all_the_way_down() -> None:
    """A nested object's keys are not keyword arguments but are still aliased,
    and both clients rename the pythonic spelling to the wire's."""
    assert _snake_keys({"authScheme": {"yourDomain": ["a"]}, "n": 1}) == {
        "auth_scheme": {"your_domain": ["a"]},
        "n": 1,
    }


# ---- capture ----


def test_the_capture_drops_generator_identity_but_keeps_the_call(mock_request: httpx.Request) -> None:
    captured = _request_capture(mock_request)

    assert captured["method"] == "POST"
    assert captured["path"] == "/api/v3.1/auth_configs"
    assert captured["query"] == "limit=5"
    assert captured["headers"]["x-api-key"] == "ak_test"
    assert "user-agent" not in captured["headers"]
    assert "x-stainless-lang" not in captured["headers"]
    assert "content-length" not in captured["headers"]
    assert captured["body"] == {"name": "n"}
    assert captured["bodyText"] is None


def test_a_method_the_inventory_does_not_model_is_refused() -> None:
    request = httpx.Request("OPTIONS", "https://api.test/api/v3.1/auth_configs")

    with pytest.raises(ValueError, match="unsupported HTTP method OPTIONS"):
        _request_capture(request)


def test_a_non_json_body_is_kept_as_text_so_the_bytes_stay_comparable() -> None:
    request = httpx.Request(
        "POST", "https://api.test/api/v3.1/files", content=b"not json", headers={"content-type": "text/plain"}
    )

    captured = _request_capture(request)

    assert captured["body"] is None
    assert captured["bodyText"] == "not json"


def test_the_transport_records_the_response_verbatim_and_still_serves_the_client() -> None:
    """The client must receive an unconsumed response; the capture must hold the
    same bytes. Reading one at the cost of the other is the failure mode."""
    transport = CapturingTransport()
    transport._inner = httpx.MockTransport(  # noqa: SLF001 - the point is to replace the network
        lambda request: httpx.Response(201, json={"id": "x"}, headers={"content-type": "application/json"})
    )

    with httpx.Client(transport=transport) as client:
        response = client.post("https://api.test/api/v3.1/auth_configs", json={"name": "n"})

    assert response.json() == {"id": "x"}
    recorded = transport.take()
    assert len(recorded) == 1
    assert recorded[0]["response"]["status"] == 201
    assert json.loads(recorded[0]["response"]["bodyText"]) == {"id": "x"}
    assert recorded[0]["transportError"] is None


def test_take_clears_what_it_returned() -> None:
    transport = CapturingTransport()
    transport._inner = httpx.MockTransport(lambda request: httpx.Response(200, json={}))  # noqa: SLF001

    with httpx.Client(transport=transport) as client:
        client.get("https://api.test/api/v3.1/toolkits")

    assert len(transport.take()) == 1
    assert transport.take() == []


@pytest.fixture
def mock_request() -> httpx.Request:
    return httpx.Request(
        "POST",
        "https://api.test/api/v3.1/auth_configs?limit=5",
        json={"name": "n"},
        headers={
            "x-api-key": "ak_test",
            "user-agent": "Composio/Python 2.0.0",
            "x-stainless-lang": "python",
            "accept": "application/json",
        },
    )


def test_the_owned_lane_constructs_through_auth() -> None:
    """Since 2.0.0-rc.18 the owned client takes ``auth``; ``ProjectAuth`` sends
    the ``x-api-key`` on every request that the oracle's ``api_key=`` does, so
    the two lanes still put the same credential on the wire."""
    client, label = build_client("owned", "ak_parity", "https://api.test", CapturingTransport())
    try:
        assert label.startswith("composio-client@")
        assert client.auth_mode == "project"
        assert client.max_retries == 0
    finally:
        client.close()
