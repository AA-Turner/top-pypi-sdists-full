"""k91 — POST /oracle/route: the intent-inference table, route resolution over
the k90 catalog (providers stubbed — no GPU/network/workers), execution through
a monkeypatched dispatch seam, the mandatory deterministic Scorecard, and the
gap/deferred wire shapes.

Run:
  cd /srv/share/projects/hugpy/dev/abstract_hugpy_dev
  ./venv/bin/python -m pytest tests/test_oracle_route.py -q
"""
from __future__ import annotations

import hashlib
import logging
import os
import sys

logging.disable(logging.INFO)  # silence the models_config registry chatter

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import pytest  # noqa: E402

from abstract_hugpy_dev.oracle import catalog, router, runtime, scorecard  # noqa: E402
from abstract_hugpy_dev.oracle.contracts import (  # noqa: E402
    ArtifactKind,
    FailureClass,
    GoalSpec,
    InputKind,
    InputRef,
    RepairCode,
)


def _goal(prompt="hello", inputs=(), capability=None):
    return GoalSpec(objective=prompt, raw_prompt=prompt,
                    inputs=tuple(inputs), capability=capability)


def _ref(kind, ref="x"):
    return InputRef(kind=InputKind(kind), ref=ref)


_ROWS = {
    "whisper-x":  {"tasks": ["automatic-speech-recognition"],
                   "framework": "transformers"},
    "qwen-chat":  {"tasks": ["text-generation"], "framework": "gguf"},
    "qwen-vl":    {"tasks": ["image-text-to-text"], "framework": "gguf"},
    "sdxl":       {"tasks": ["text-to-image"], "framework": "transformers"},
    "vit-cls":    {"tasks": ["image-classification"], "framework": "transformers"},
}


def _stub_catalog(monkeypatch, rows=_ROWS, workers=({"id": "w1"},), capable=True,
                  central=True, blocked=frozenset()):
    monkeypatch.setattr(catalog, "_legacy_registry_rows", lambda: dict(rows))
    monkeypatch.setattr(catalog, "_online_workers",
                        lambda: None if workers is None else list(workers))
    monkeypatch.setattr(catalog, "_worker_task_capable", lambda w, t: bool(capable))
    monkeypatch.setattr(catalog, "_central_task_available", lambda t: central)
    monkeypatch.setattr(catalog, "_blocked_model_keys", lambda: set(blocked))


# ---------------------------------------------------------------------------
# The mapping table: every executable capability's task maps back through
# LEGACY_TASK_CAPABILITY — the router and the catalog can never disagree.
# ---------------------------------------------------------------------------


def test_capability_task_table_is_inverse_consistent():
    for cap, task in router.CAPABILITY_TASK.items():
        assert catalog.LEGACY_TASK_CAPABILITY.get(task) == cap
    # and every legacy capability is dispatchable
    assert set(router.CAPABILITY_TASK) == set(
        catalog.LEGACY_TASK_CAPABILITY.values())


# ---------------------------------------------------------------------------
# Intent inference — the deterministic table.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("prompt,inputs,expected", [
    ("what is in this picture?", [_ref("image")], "image.understand"),
    ("describe the scene", [_ref("image")], "image.understand"),
    ("make it a watercolor painting", [_ref("image")], "image.transform"),
    ("restyle this photo as pixel art", [_ref("image")], "image.transform"),
    # transform verb BUT question-like -> understand wins
    ("what would make it a watercolor?", [_ref("image")], "image.understand"),
    ("get the words out", [_ref("audio")], "audio.transcribe"),
    ("transcribe", [_ref("video")], "audio.transcribe"),
    ("what does this page say", [_ref("url", "https://x.test")], "web.fetch"),
    ("summarize this report for me", [], "text.summarize"),
    ("tl;dr the following", [], "text.summarize"),
    ("hello there", [], "text.chat"),
])
def test_inference_table(prompt, inputs, expected):
    cap, why = router.infer_capability(_goal(prompt, inputs))
    assert cap == expected, why
    assert why  # the reason is recorded, never blank


def test_explicit_capability_wins_over_inference(monkeypatch):
    _stub_catalog(monkeypatch)
    goal = _goal("summarize this please", capability="text.chat")
    route = router.resolve_route(goal)
    assert route.capability == "text.chat"
    assert route.inferred is False
    assert route.inference_reason == "explicit capability in request"


# ---------------------------------------------------------------------------
# resolve_route — model choice + branches.
# ---------------------------------------------------------------------------


def test_resolve_route_only_eligible_model(monkeypatch):
    _stub_catalog(monkeypatch)
    route = router.resolve_route(_goal("hi", [_ref("audio", "/tmp/a.wav")]))
    assert route.execution == "execute"
    assert route.capability == "audio.transcribe"
    assert route.task == "automatic-speech-recognition"
    assert route.model_id == "whisper-x"
    assert route.model_rationale == "only-eligible"
    assert route.inferred is True


def test_resolve_route_requested_model_wins(monkeypatch):
    _stub_catalog(monkeypatch)
    route = router.resolve_route(_goal("hi"), requested_model="qwen-chat")
    assert route.model_id == "qwen-chat"
    assert route.model_rationale == "requested"


def test_resolve_route_requested_model_outside_capability_refuses(monkeypatch):
    _stub_catalog(monkeypatch)
    with pytest.raises(router.RouteRefusal):
        router.resolve_route(_goal("hi"), requested_model="whisper-x")


def test_resolve_route_default_when_multiple_models(monkeypatch):
    rows = dict(_ROWS, **{"qwen-chat-2": {"tasks": ["text-generation"],
                                          "framework": "gguf"}})
    _stub_catalog(monkeypatch, rows=rows)
    monkeypatch.setattr(router, "_task_default_model", lambda t: "qwen-chat-2")
    route = router.resolve_route(_goal("hi"))
    assert route.model_id == "qwen-chat-2"
    assert route.model_rationale == "default"


def test_resolve_route_unknown_capability_is_gap_not_keyerror(monkeypatch):
    _stub_catalog(monkeypatch)
    route = router.resolve_route(_goal("hi", capability="quantum.flux"))
    assert route.execution == "gap"
    assert any("unknown capability" in r for r in route.reasons)


def test_resolve_route_ineligible_echoes_catalog_reasons(monkeypatch):
    _stub_catalog(monkeypatch, workers=(), central=False)
    route = router.resolve_route(_goal("hi", capability="audio.transcribe"))
    assert route.execution == "gap"
    joined = " | ".join(route.reasons)
    assert "no online worker registered" in joined
    assert "central cannot serve" in joined


def test_resolve_route_video_is_deferred_with_menu(monkeypatch):
    _stub_catalog(monkeypatch)
    monkeypatch.setattr(router, "_studio_menu", lambda: "t2v (clip-t2v-480p)")
    route = router.resolve_route(_goal("hi", capability="video.generate.t2v"))
    assert route.execution == "deferred"
    assert route.alternatives == "t2v (clip-t2v-480p)"
    assert route.reasons  # the studio verdict/advisory rides along


def test_resolve_route_deterministic_amenity(monkeypatch):
    _stub_catalog(monkeypatch, rows={})
    route = router.resolve_route(_goal("hi", capability="doc.extract"))
    assert route.execution == "execute"
    assert route.model_id is None
    assert route.model_rationale == "deterministic-local"
    assert route.placement == "local"


# ---------------------------------------------------------------------------
# runtime.execute_route — dispatch monkeypatched, no GPU/network.
# ---------------------------------------------------------------------------


class _Result:
    def __init__(self, **payload):
        self._payload = payload

    def model_dump(self):
        return dict(self._payload)


def _exec_route(monkeypatch, capability="text.chat", **goal_kw):
    _stub_catalog(monkeypatch)
    goal = _goal(goal_kw.pop("prompt", "hello"), goal_kw.pop("inputs", ()),
                 capability=capability)
    return goal, router.resolve_route(goal)


def _patch_dispatch(monkeypatch, fn):
    monkeypatch.setattr(runtime, "_dispatch", fn)
    monkeypatch.setattr(runtime, "_normalized_kwargs",
                        lambda task, body: dict(body, task=task))


def test_execute_route_happy_path(monkeypatch):
    goal, route = _exec_route(monkeypatch)
    seen = {}

    def fake_dispatch(kwargs):
        seen.update(kwargs)
        return _Result(ok=True, text="the answer", model_key="qwen-chat")

    _patch_dispatch(monkeypatch, fake_dispatch)
    artifacts, receipt = runtime.execute_route(goal, route)

    assert seen["task"] == "text-generation"
    assert seen["model_key"] == "qwen-chat"
    assert seen["prompt"] == "hello"

    assert len(artifacts) == 1
    art = artifacts[0]
    assert art["kind"] == "text" and art["text"] == "the answer"
    assert art["sha256"] == hashlib.sha256(b"the answer").hexdigest()

    assert receipt.capability == "text.chat"
    assert receipt.model_id == "qwen-chat"
    assert receipt.failure is None
    assert receipt.retries == 0
    assert receipt.duration_s >= 0
    assert receipt.started_at and receipt.ended_at
    assert receipt.request_dict()["task"] == "text-generation"
    assert [a.uri for a in receipt.artifacts] == [art["uri"]]


def test_execute_route_retries_once_on_worker_unavailable(monkeypatch):
    goal, route = _exec_route(monkeypatch)
    calls = {"n": 0}

    def flaky(kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise ConnectionError("connection refused")
        return _Result(ok=True, text="second try")

    _patch_dispatch(monkeypatch, flaky)
    artifacts, receipt = runtime.execute_route(goal, route)
    assert calls["n"] == 2
    assert receipt.retries == 1
    assert receipt.failure is None
    assert artifacts[0]["text"] == "second try"
    assert any("retried once" in w for w in receipt.warnings)


def test_execute_route_worker_unavailable_after_retry(monkeypatch):
    goal, route = _exec_route(monkeypatch)

    def dead(kwargs):
        raise ConnectionError("worker unreachable")

    _patch_dispatch(monkeypatch, dead)
    artifacts, receipt = runtime.execute_route(goal, route)
    assert artifacts == []
    assert receipt.retries == 1
    assert receipt.failure is FailureClass.WORKER_UNAVAILABLE
    assert receipt.log_excerpt


def test_execute_route_timeout_is_not_retried(monkeypatch):
    goal, route = _exec_route(monkeypatch)
    calls = {"n": 0}

    def slow(kwargs):
        calls["n"] += 1
        raise TimeoutError("request timed out after 300s")

    _patch_dispatch(monkeypatch, slow)
    _, receipt = runtime.execute_route(goal, route)
    assert calls["n"] == 1
    assert receipt.retries == 0
    assert receipt.failure is FailureClass.TIMEOUT


def test_execute_route_runner_not_ok_is_runner_error(monkeypatch):
    goal, route = _exec_route(monkeypatch)
    _patch_dispatch(monkeypatch,
                    lambda kwargs: _Result(ok=False, error="model exploded"))
    artifacts, receipt = runtime.execute_route(goal, route)
    assert receipt.failure is FailureClass.RUNNER_ERROR
    assert "model exploded" in " ".join(receipt.log_excerpt)


def test_build_request_body_shapes(monkeypatch):
    _stub_catalog(monkeypatch)
    # image.understand: file + prompt
    goal = _goal("what is this?", [_ref("image", "/tmp/x.png")],
                 capability="image.understand")
    body = runtime.build_request_body(goal, router.resolve_route(goal))
    assert body["file"] == "/tmp/x.png" and body["prompt"] == "what is this?"
    # similarity needs two texts
    goal = _goal("compare", [_ref("text", "a")], capability="text.similarity")
    route = router.RouteDecision(capability="text.similarity",
                                 execution="execute", task="sentence-similarity")
    with pytest.raises(runtime.GoalShapeError):
        runtime.build_request_body(goal, route)
    # missing image input is a typed shape error, pre-dispatch
    goal = _goal("classify", capability="image.classify")
    route = router.RouteDecision(capability="image.classify",
                                 execution="execute", task="image-classification")
    with pytest.raises(runtime.GoalShapeError):
        runtime.build_request_body(goal, route)


# ---------------------------------------------------------------------------
# Scorecard — deterministic technical checks.
# ---------------------------------------------------------------------------


def _executed(monkeypatch, dispatch):
    goal, route = _exec_route(monkeypatch)
    _patch_dispatch(monkeypatch, dispatch)
    artifacts, receipt = runtime.execute_route(goal, route)
    return goal, route, artifacts, receipt


def test_scorecard_happy_path(monkeypatch):
    goal, route, arts, receipt = _executed(
        monkeypatch, lambda k: _Result(ok=True, text="fine"))
    card = scorecard.build_technical_scorecard(goal, route, arts, receipt)
    assert card.hard_pass is True
    assert card.repair_code is None
    assert card.judge_results == ()          # k92 seam: present and empty
    assert "judge_results" in card.to_dict()
    assert {c.name for c in card.checks} == {"execution", "empty_output",
                                             "format", "decode"}


def test_scorecard_empty_artifact_fails_empty_output(monkeypatch):
    goal, route, arts, receipt = _executed(
        monkeypatch, lambda k: _Result(ok=True, text="   "))
    assert len(arts) == 1                     # the blank artifact IS produced
    card = scorecard.build_technical_scorecard(goal, route, arts, receipt)
    assert card.hard_pass is False
    assert card.repair_code is RepairCode.EMPTY_OUTPUT
    failing = {c.name for c in card.checks if not c.passed}
    assert failing == {"empty_output"}


def test_scorecard_worker_unavailable_from_receipt(monkeypatch):
    def dead(kwargs):
        raise ConnectionError("no route to host")
    goal, route, arts, receipt = _executed(monkeypatch, dead)
    card = scorecard.build_technical_scorecard(goal, route, arts, receipt)
    assert card.hard_pass is False
    assert card.repair_code is RepairCode.WORKER_UNAVAILABLE
    execution = [c for c in card.checks if c.name == "execution"][0]
    assert execution.value == "worker_unavailable"


def test_scorecard_format_mismatch():
    route = router.RouteDecision(
        capability="text.chat", execution="execute", task="text-generation",
        produces=(ArtifactKind.TEXT,))
    receipt = _receipt_for(route)
    arts = [{"kind": "json", "uri": "inline:json/x", "sha256": "0" * 64,
             "data": {"x": 1}}]
    card = scorecard.build_technical_scorecard(
        _goal("hi"), route, arts, receipt)
    assert card.hard_pass is False
    assert card.repair_code is RepairCode.FORMAT_MISMATCH


def test_scorecard_missing_file_is_decode_failed(tmp_path):
    route = router.RouteDecision(
        capability="image.generate", execution="execute", task="text-to-image",
        produces=(ArtifactKind.IMAGE,))
    receipt = _receipt_for(route)
    # one real (undecodable) file and the check must name it
    bad = tmp_path / "img.png"
    bad.write_bytes(b"not a png at all")
    arts = [{"kind": "image", "uri": str(bad), "sha256": "0" * 64}]
    card = scorecard.build_technical_scorecard(_goal("hi"), route, arts, receipt)
    try:
        import PIL  # noqa: F401
        assert card.repair_code is RepairCode.DECODE_FAILED
        assert card.hard_pass is False
    except ImportError:
        # PIL absent: degradation is named, size-only check passes
        decode = [c for c in card.checks if c.name == "decode"][0]
        assert "PIL unavailable" in decode.detail


def _receipt_for(route):
    from abstract_hugpy_dev.oracle.contracts import ExecutionReceipt
    return ExecutionReceipt(
        request=ExecutionReceipt.normalize_request({"task": route.task}),
        capability=route.capability, model_id="m", worker=None,
        started_at="2026-08-05T00:00:00+00:00",
        ended_at="2026-08-05T00:00:01+00:00", duration_s=1.0)


def test_gap_and_deferred_scorecards_are_typed():
    gap = router.RouteDecision(capability="audio.transcribe", execution="gap",
                               reasons=("no model registered",))
    card = scorecard.build_gap_scorecard(gap)
    assert card.hard_pass is False
    assert card.repair_code is RepairCode.CAPABILITY_GAP
    assert "no model registered" in card.checks[0].detail

    deferred = router.RouteDecision(capability="video.generate.t2v",
                                    execution="deferred", model_id="wan-t2v")
    card = scorecard.build_deferred_scorecard(deferred)
    assert card.hard_pass is False
    assert card.repair_code is None
    assert card.judge_results == ()


# ---------------------------------------------------------------------------
# The route, over a bare Flask app.
# ---------------------------------------------------------------------------


def _client(monkeypatch, dispatch=None):
    from flask import Flask
    from abstract_hugpy_dev.flask_app.app.routes.oracle_routes import oracle_bp
    _stub_catalog(monkeypatch)
    if dispatch is not None:
        _patch_dispatch(monkeypatch, dispatch)
    app = Flask("oracle-route-test")
    app.register_blueprint(oracle_bp)
    return app.test_client()


def test_route_executes_and_carries_all_five_parts(monkeypatch):
    client = _client(monkeypatch,
                     dispatch=lambda k: _Result(ok=True, text="routed!"))
    resp = client.post("/oracle/route", json={"prompt": "hello oracle"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ok"] is True
    for part in ("goal", "route", "artifacts", "receipt", "scorecard"):
        assert part in body, part
    assert body["route"]["capability"] == "text.chat"
    assert body["route"]["model_rationale"] == "only-eligible"
    assert body["artifacts"][0]["text"] == "routed!"
    assert body["scorecard"]["hard_pass"] is True
    assert body["scorecard"]["judge_results"] == []   # k92 seam on the wire
    assert body["receipt"]["capability"] == "text.chat"


def test_route_video_deferred_shape(monkeypatch):
    monkeypatch.setattr(router, "_studio_menu", lambda: "menu-here")
    client = _client(monkeypatch)
    resp = client.post("/oracle/route",
                       json={"prompt": "make a clip",
                             "capability": "video.generate.t2v"})
    assert resp.status_code == 202
    body = resp.get_json()
    assert body["execution"] == "deferred"
    assert body["routed"] == "video.generate.t2v"
    assert body["reason"]
    assert "binding" in body and "alternatives" in body
    assert body["scorecard"]["hard_pass"] is False


def test_route_capability_gap_shape(monkeypatch):
    client = _client(monkeypatch)
    resp = client.post("/oracle/route",
                       json={"prompt": "x", "capability": "no.such.capability"})
    assert resp.status_code == 422
    body = resp.get_json()
    assert body["ok"] is False
    assert body["scorecard"]["repair_code"] == "capability_gap"
    assert body["route"]["execution"] == "gap"


def test_route_unmapped_task_string_is_gap_not_keyerror(monkeypatch):
    client = _client(monkeypatch)
    for task in ("text-to-video", "quantum-flux-sorting"):
        resp = client.post("/oracle/route",
                           json={"prompt": "x", "capability": task})
        assert resp.status_code == 422, task
        body = resp.get_json()
        assert body["scorecard"]["repair_code"] == "capability_gap"


def test_route_legacy_task_string_folds_to_capability(monkeypatch):
    client = _client(monkeypatch,
                     dispatch=lambda k: _Result(ok=True, text="hi"))
    resp = client.post("/oracle/route",
                       json={"prompt": "x", "capability": "text-generation"})
    assert resp.status_code == 200
    assert resp.get_json()["route"]["capability"] == "text.chat"


def test_route_requested_model_mismatch_is_400(monkeypatch):
    client = _client(monkeypatch)
    resp = client.post("/oracle/route",
                       json={"prompt": "x", "model_id": "whisper-x"})
    assert resp.status_code == 400
    assert "does not serve" in resp.get_json()["error"]


def test_route_needs_prompt_or_capability(monkeypatch):
    client = _client(monkeypatch)
    resp = client.post("/oracle/route", json={})
    assert resp.status_code == 400
    resp = client.post("/oracle/route", json={"inputs": []})
    assert resp.status_code == 400


def test_route_bad_input_kind_is_400(monkeypatch):
    client = _client(monkeypatch)
    resp = client.post("/oracle/route",
                       json={"prompt": "x",
                             "inputs": [{"kind": "hologram", "uri": "y"}]})
    assert resp.status_code == 400
    assert "kind" in resp.get_json()["error"]


def test_route_missing_required_input_is_400(monkeypatch):
    client = _client(monkeypatch, dispatch=lambda k: _Result(ok=True, text="t"))
    resp = client.post("/oracle/route",
                       json={"prompt": "classify",
                             "capability": "image.classify"})
    assert resp.status_code == 400
    assert "image" in resp.get_json()["error"]
