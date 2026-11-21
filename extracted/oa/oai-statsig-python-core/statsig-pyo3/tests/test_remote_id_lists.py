"""Remote ID-list membership through the Python binding."""

import base64
import hashlib
import json
from contextlib import contextmanager
from threading import Event
from time import monotonic, sleep

import pytest
from shared_id_lists_http_server import _specs as id_list_specs
from shared_id_lists_http_server import changeset
from statsig_python_core import (
    BulkEvaluationOptions,
    Statsig,
    StatsigOptions,
    StatsigUser,
)
from test_observability_client import MockObservabilityClient
from werkzeug import Response


@contextmanager
def _membership_sdk(
    httpserver,
    *,
    names=("members",),
    id_type="userID",
    lookup=lambda _body: False,
    local_lists=True,
    enabled=True,
    remote_lists=("members",),
    **options,
):
    specs = id_list_specs(names)
    for condition in specs["condition_map"].values():
        condition["idType"] = id_type
    httpserver.expect_request("/v2/download_config_specs").respond_with_json(specs)
    data = changeset(["local-member"]).encode()
    row = {
        "url": httpserver.url_for("/file"),
        "size": len(data),
        "fileID": "initial",
        "creationTime": 1,
    }
    manifest = {name: {"name": name, **row} for name in names} if local_lists else {}
    httpserver.expect_request("/v1/get_id_lists").respond_with_json(manifest)
    httpserver.expect_request("/file").respond_with_data(
        data,
        status=206,
        headers={"Content-Range": f"bytes 0-{len(data) - 1}/{len(data)}"},
    )
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    # SFP and the SDK must agree on the file cursor to cache an answer.
    cursor = (
        b"statsig-id-list-v1"
        + row["creationTime"].to_bytes(8, "big")
        + row["size"].to_bytes(8, "big")
        + row["fileID"].encode()
    )
    revision = base64.b64encode(hashlib.sha256(cursor).digest()).decode()
    calls = []

    def membership(request):
        body = request.get_json()
        calls.append(body)
        answer = {"is_member": lookup(body), "revision": revision}
        return Response(json.dumps(answer), mimetype="application/json")

    httpserver.expect_request(
        "/v1/id_list_membership", method="POST"
    ).respond_with_handler(membership)
    # Scope the process environment to construction so checks also verify the startup snapshot.
    with pytest.MonkeyPatch.context() as env:
        if enabled:
            env.setenv("STATSIG_RUST_REMOTE_ID_LISTS_ENABLED", "1")
        else:
            env.delenv("STATSIG_RUST_REMOTE_ID_LISTS_ENABLED", raising=False)
        env.setenv(
            "STATSIG_RUST_REMOTE_ID_LIST_ALLOWLIST",
            json.dumps(dict.fromkeys(remote_lists, id_type)),
        )
        sdk = Statsig(
            "secret-local-membership",
            StatsigOptions(
                specs_url=httpserver.url_for("/v2/download_config_specs"),
                id_lists_url=httpserver.url_for("/v1/get_id_lists"),
                log_event_url=httpserver.url_for("/v1/log_event"),
                enable_id_lists=True,
                fallback_to_statsig_api=False,
                output_log_level="none",
                **options,
            ),
        )
    try:
        assert sdk.initialize().wait(5)
        yield sdk, calls
    finally:
        assert sdk.shutdown().wait(10)


@pytest.mark.parametrize("enabled", [False, True], ids=["opted-out", "opted-in"])
def test_only_enrolled_server_checks_use_sfp(httpserver, enabled):
    with _membership_sdk(
        httpserver, names=("members", "local-only"), enabled=enabled
    ) as (sdk, calls):
        user = StatsigUser("local-member")
        response = json.loads(sdk.get_client_initialize_response(user, hash="none"))
        assert response["feature_gates"]["membership"]["value"]
        assert sdk.check_gate(user, "local-only")
        assert not calls

        assert sdk.check_gate(user, "membership")
        assert len(calls) == int(enabled)


def test_config_wait_releases_gil_and_keeps_the_local_decision(httpserver):
    user = StatsigUser("remote-only")
    observer = MockObservabilityClient()

    def lookup(_request):
        with pytest.raises(RuntimeError, match="borrow"):
            user.user_id = "replacement"
        return True

    with _membership_sdk(
        httpserver, lookup=lookup, local_lists=False, observability_client=observer
    ) as (sdk, calls):
        assert not sdk.get_dynamic_config(user, "membership").value["member"]
        # This outcome requires the Python handler to answer during the SDK wait.
        deadline = monotonic() + 5
        while not any(
            name == "statsig.sdk.id_list_membership_lookup"
            and tags.get("result") == "ready_local_missing"
            for _, name, _, tags in observer.metrics
        ):
            assert monotonic() < deadline, "expected an SFP answer during the config wait"
            sleep(0.01)
        assert [call["id"] for call in calls] == ["remote-only"]


def test_direct_and_typed_evaluations_share_the_users_first_lookup(httpserver):
    with _membership_sdk(httpserver, id_type="stableID") as (sdk, calls):
        user = StatsigUser("account", custom_ids={"stableid": "local-member"})
        for _ in range(2):
            assert sdk.check_gate(user, "membership")
        assert sdk.get_dynamic_config(user, "membership").value["member"]
        assert len(calls) == 1

        user.custom_ids = {"stableid": "second"}
        assert not sdk.check_gate(user, "membership")
        assert calls == [
            {"list_id": "members", "id_type": "stableID", "id": "local-member"},
            {"list_id": "members", "id_type": "stableID", "id": "second"},
        ]

        # A typed context can clone a fresh user before its first direct check.
        other = StatsigUser("another-account", custom_ids={"stableid": "local-member"})
        context = sdk._INTERNAL_typed_config_context(other, "membership")
        assert sdk.check_gate(other, "membership")
        assert context.get_evaluation()["value"]["member"]
        assert len(calls) == 3


def test_bulk_call_has_one_wait_budget_across_cold_gates(httpserver):
    gates = [f"bulk_{i}" for i in range(10)]
    release = Event()

    def slow_lookup(_request):
        release.wait(5)
        return False

    with _membership_sdk(
        httpserver,
        names=gates,
        lookup=slow_lookup,
        remote_lists=gates,
    ) as (sdk, calls):
        options = BulkEvaluationOptions(
            feature_gate_filter=gates,
            dynamic_config_filter=[],
            experiment_filter=[],
            layer_filter=[],
        )
        try:
            start = monotonic()
            result = sdk.bulk_evaluate(StatsigUser("local-member"), options)
            elapsed = monotonic() - start
        finally:
            release.set()
        assert calls
        assert set(result["feature_gates"]) == set(gates)
        assert all(gate["value"] for gate in result["feature_gates"].values())
        # One 100 ms budget with scheduling headroom. Ten waits would take 1 s.
        assert elapsed < 0.65
