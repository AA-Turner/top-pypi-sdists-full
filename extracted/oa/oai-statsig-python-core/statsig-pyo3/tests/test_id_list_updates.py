"""ID-list file updates through the actual Python binding and Rust evaluator.

Only HTTP responses are local fixtures. The SDK's polling, range downloads,
membership storage, publication and evaluation all run normally.
"""

import base64
import hashlib
import json
from threading import Lock
from time import monotonic, sleep

import pytest
from statsig_python_core import (
    DynamicConfigEvaluationOptions,
    EvaluationCache,
    FeatureGateEvaluationOptions,
    Statsig,
    StatsigOptions,
    StatsigUser,
    StatsigUserContext,
)
from werkzeug import Response


def _member_key(user_id):
    return base64.b64encode(hashlib.sha256(user_id.encode()).digest()).decode()[:8]


def _specs():
    rule = {
        "name": "member",
        "id": "member",
        "salt": "member",
        "conditions": ["member"],
        "passPercentage": 100,
        "returnValue": True,
        "idType": "userID",
    }
    gate = {
        "type": "feature_gate",
        "entity": "feature_gate",
        "salt": "member",
        "enabled": True,
        "defaultValue": False,
        "idType": "userID",
        "version": 1,
        "rules": [rule],
    }
    config = {
        **gate,
        "type": "dynamic_config",
        "entity": "dynamic_config",
        "defaultValue": {"member": False},
        "rules": [{**rule, "returnValue": {"member": True}}],
    }
    return {
        "time": 1_800_000_100_001,
        "has_updates": True,
        "feature_gates": {"membership": gate},
        "dynamic_configs": {"membership": config},
        "layer_configs": {},
        "experiment_to_layer": {},
        "condition_map": {
            "member": {
                "type": "unit_id",
                "operator": "in_segment_list",
                "targetValue": "members",
                "idType": "userID",
            }
        },
    }


@pytest.mark.parametrize(
    "use_evaluation_cache", [False, True], ids=["uncached", "cached"]
)
def test_membership_append_remove_and_new_file_reset(httpserver, use_evaluation_cache):
    specs = _specs()
    # Real targeting hashes are eight ASCII bytes. Include fallback parser keys
    # in the same file; direct non-eight-byte membership is covered in Rust.
    initial = (
        f"+{_member_key('alice')}\n+{_member_key('steady')}\n"
        "+short\n+longer-than-eight\n+🙂\n"
    ).encode()
    files = {"first": initial}
    current = {"file_id": "first", "creation_time": 1}
    downloads = []
    lock = Lock()

    httpserver.expect_request("/v2/download_config_specs").respond_with_json(specs)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    def manifest(_request):
        with lock:
            file_id = current["file_id"]
            body = {
                "members": {
                    "name": "members",
                    "url": httpserver.url_for(f"/members/{file_id}"),
                    "size": len(files[file_id]),
                    "creationTime": current["creation_time"],
                    "fileID": file_id,
                }
            }
        return Response(json.dumps(body), mimetype="application/json")

    def download(request):
        file_id = request.path.rsplit("/", 1)[1]
        range_header = request.headers["Range"]
        assert range_header.startswith("bytes=") and range_header.endswith("-")
        start = int(range_header[len("bytes=") : -1])
        size = int(request.headers["statsig-id-list-file-size"])
        with lock:
            data = files[file_id][start:size]
            downloads.append((file_id, start, size))
        assert data
        return Response(
            data,
            status=206,
            mimetype="text/plain",
            headers={"Content-Range": f"bytes {start}-{start + len(data) - 1}/{size}"},
        )

    httpserver.expect_request("/v1/get_id_lists").respond_with_handler(manifest)
    for file_id in ("first", "replacement"):
        httpserver.expect_request(f"/members/{file_id}").respond_with_handler(download)

    sdk = Statsig(
        "secret-local-id-list-test",
        StatsigOptions(
            specs_url=httpserver.url_for("/v2/download_config_specs"),
            id_lists_url=httpserver.url_for("/v1/get_id_lists"),
            log_event_url=httpserver.url_for("/v1/log_event"),
            specs_sync_interval_ms=60_000,
            id_lists_sync_interval_ms=1000,
            enable_id_lists=True,
            fallback_to_statsig_api=False,
            output_log_level="none",
            evaluation_cache=EvaluationCache() if use_evaluation_cache else None,
        ),
    )
    context = StatsigUserContext(custom={"fixture": "id-list-updates"})
    gate_options = FeatureGateEvaluationOptions(disable_exposure_logging=True)
    config_options = DynamicConfigEvaluationOptions(disable_exposure_logging=True)

    def membership(user_id):
        user = StatsigUser(user_id)
        return (
            sdk.get_feature_gate(user, "membership", gate_options).value,
            sdk.get_feature_gate_with_context(
                context, "membership", user_id=user_id, options=gate_options
            ).value,
            sdk.get_dynamic_config(user, "membership", config_options).value["member"],
        )

    def wait_for(expected):
        deadline = monotonic() + 10
        while True:
            actual = {user_id: membership(user_id) for user_id in expected}
            if all(actual[user_id] == (value,) * 3 for user_id, value in expected.items()):
                return
            assert monotonic() < deadline, actual
            sleep(0.02)

    try:
        assert sdk.initialize().wait(10) and sdk.is_initialized()
        wait_for({"alice": True, "bob": False, "steady": True})
        old_member = sdk.get_dynamic_config(
            StatsigUser("alice"), "membership", config_options
        )
        old_nonmember = sdk.get_feature_gate(
            StatsigUser("bob"), "membership", gate_options
        )

        first_delta = f"+{_member_key('bob')}\n-{_member_key('alice')}\n".encode()
        with lock:
            files["first"] += first_delta
        wait_for({"alice": False, "bob": True, "steady": True})
        with lock:
            assert ("first", len(initial), len(initial) + len(first_delta)) in downloads

        second_delta = f"-{_member_key('bob')}\n+{_member_key('alice')}\n".encode()
        with lock:
            previous_size = len(files["first"])
            files["first"] += second_delta
        wait_for({"alice": True, "bob": False, "steady": True})
        with lock:
            assert ("first", previous_size, previous_size + len(second_delta)) in downloads

        # A new file identity must replace membership, even when its content is
        # shorter. This does not exercise same-file creation-time replay.
        replacement = f"+{_member_key('bob')}\n".encode()
        with lock:
            files["replacement"] = replacement
            current.update(file_id="replacement", creation_time=2)
        wait_for({"alice": False, "bob": True, "steady": False})
        with lock:
            assert ("replacement", 0, len(replacement)) in downloads

        # Public evaluation results are retained snapshots. User contexts own
        # targeting metadata, not old SDK snapshots, and saw every update above.
        assert old_member.value == {"member": True}
        assert old_nonmember.value is False
        assert old_member.details.lcut == specs["time"]
        assert (
            sdk.get_feature_gate(StatsigUser("bob"), "membership").details.lcut
            == specs["time"]
        )
    finally:
        assert sdk.shutdown().wait(10)
