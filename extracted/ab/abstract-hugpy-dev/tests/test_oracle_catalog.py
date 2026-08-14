"""k90 — oracle catalog: mapping-table totality over BOTH registries, catalog
composition with the provider seams stubbed (no live workers / GPU / network),
and the GET /oracle/capabilities route smoke over a bare Flask app.

Run:
  cd /srv/share/projects/hugpy/dev/abstract_hugpy_dev
  ./venv/bin/python -m pytest tests/test_oracle_catalog.py -q
"""
from __future__ import annotations

import logging
import os
import sys

logging.disable(logging.INFO)  # silence the models_config registry chatter

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from abstract_hugpy_dev.oracle import catalog  # noqa: E402
from abstract_hugpy_dev.oracle.contracts import SourceRegistry  # noqa: E402
from abstract_hugpy_dev.video_intel.studio.enums import Capability  # noqa: E402


# ---------------------------------------------------------------------------
# Mapping-table totality: every member of both vocabularies lands in exactly
# one of (mapped, EXCLUDED-with-reason). A silent gap is the failure k90 exists
# to prevent — nothing may be un-catalogued without a recorded decision.
# ---------------------------------------------------------------------------


def test_ml_tasks_map_totally():
    from abstract_hugpy_dev.flask_app.app.routes.ml_routes import ML_TASKS
    for task in ML_TASKS.values():
        mapped = task in catalog.LEGACY_TASK_CAPABILITY
        excluded = task in catalog.LEGACY_TASK_EXCLUDED
        assert mapped != excluded, (
            f"ML task {task!r} must be in exactly one of "
            f"LEGACY_TASK_CAPABILITY / LEGACY_TASK_EXCLUDED "
            f"(mapped={mapped}, excluded={excluded})")


def test_legacy_tables_are_disjoint_and_exclusions_carry_reasons():
    overlap = set(catalog.LEGACY_TASK_CAPABILITY) & set(catalog.LEGACY_TASK_EXCLUDED)
    assert not overlap, f"tasks in both tables: {sorted(overlap)}"
    for task, reason in catalog.LEGACY_TASK_EXCLUDED.items():
        assert reason.strip(), f"exclusion of {task!r} carries no reason"


def test_studio_capabilities_map_totally():
    for cap in Capability:
        mapped = cap in catalog.STUDIO_CAPABILITY_NAME
        excluded = cap in catalog.STUDIO_CAPABILITY_EXCLUDED
        assert mapped != excluded, (
            f"studio Capability {cap.value!r} must be in exactly one of "
            f"STUDIO_CAPABILITY_NAME / STUDIO_CAPABILITY_EXCLUDED")
    for cap, reason in catalog.STUDIO_CAPABILITY_EXCLUDED.items():
        assert reason.strip(), f"exclusion of {cap.value!r} carries no reason"


def test_namespaced_names_unique_across_both_registries():
    legacy_names = set(catalog.LEGACY_TASK_CAPABILITY.values())
    studio_names = set(catalog.STUDIO_CAPABILITY_NAME.values())
    assert not (legacy_names & studio_names), (
        "a capability name owned by both registries would let one view "
        f"shadow the other: {sorted(legacy_names & studio_names)}")
    for name in legacy_names | studio_names:
        assert "." in name, f"capability name {name!r} is not namespaced"
    # studio names are 1:1 (no two Capabilities collapsing into one name)
    assert len(studio_names) == len(catalog.STUDIO_CAPABILITY_NAME)


def test_every_mapped_capability_has_io_kinds():
    for name in set(catalog.LEGACY_TASK_CAPABILITY.values()):
        assert name in catalog._LEGACY_IO, f"no IO kinds declared for {name}"
    for cap in catalog.STUDIO_CAPABILITY_NAME:
        assert cap in catalog._STUDIO_IO, f"no IO kinds declared for {cap.value}"


# ---------------------------------------------------------------------------
# Legacy-side composition, providers stubbed (no live workers needed).
# ---------------------------------------------------------------------------

_ROWS = {
    "whisper-x": {"tasks": ["automatic-speech-recognition"],
                  "framework": "transformers"},
    "qwen-chat": {"tasks": ["text-generation"], "framework": "gguf"},
}


def _stub_legacy(monkeypatch, rows=_ROWS, workers=None, capable=True,
                 central=True, blocked=frozenset()):
    monkeypatch.setattr(catalog, "_legacy_registry_rows", lambda: dict(rows))
    monkeypatch.setattr(catalog, "_online_workers",
                        lambda: None if workers is None else list(workers))
    monkeypatch.setattr(catalog, "_worker_task_capable",
                        lambda w, t: bool(capable))
    monkeypatch.setattr(catalog, "_central_task_available", lambda t: central)
    monkeypatch.setattr(catalog, "_blocked_model_keys", lambda: set(blocked))


def _view(views, name):
    match = [v for v in views if v.name == name]
    assert match, f"{name} missing from {[v.name for v in views]}"
    return match[0]


def test_legacy_view_happy_path(monkeypatch):
    _stub_legacy(monkeypatch, workers=[{"id": "w1"}])
    views = catalog._legacy_views()
    asr = _view(views, "audio.transcribe")
    assert asr.source is SourceRegistry.TASKS
    assert asr.model_ids == ("whisper-x",)
    assert asr.eligibility.eligible
    assert asr.resources.frameworks == ("transformers",)


def test_legacy_view_no_model_registered(monkeypatch):
    _stub_legacy(monkeypatch, rows={}, workers=[{"id": "w1"}])
    asr = _view(catalog._legacy_views(), "audio.transcribe")
    assert not asr.eligibility.eligible
    assert any("no model registered" in r for r in asr.eligibility.reasons)


def test_legacy_view_no_online_worker_and_no_central_dep(monkeypatch):
    _stub_legacy(monkeypatch, workers=[], central=False)
    asr = _view(catalog._legacy_views(), "audio.transcribe")
    assert not asr.eligibility.eligible
    joined = " | ".join(asr.eligibility.reasons)
    assert "no online worker registered" in joined
    assert "central cannot serve" in joined


def test_legacy_view_worker_denies_but_central_serves(monkeypatch):
    # affirmative worker deny + central dep present -> still eligible, with
    # the worker gap surfaced as an ADVISORY reason (explain-before-execute).
    _stub_legacy(monkeypatch, workers=[{"id": "w1"}], capable=False, central=True)
    asr = _view(catalog._legacy_views(), "audio.transcribe")
    assert asr.eligibility.eligible
    assert any("no online worker advertises" in r
               for r in asr.eligibility.reasons)


def test_legacy_view_operator_block_is_a_named_refusal(monkeypatch):
    _stub_legacy(monkeypatch, workers=[{"id": "w1"}], blocked={"whisper-x"})
    asr = _view(catalog._legacy_views(), "audio.transcribe")
    assert not asr.eligibility.eligible
    assert asr.model_ids == ()   # blocked models are not offered
    assert any("operator-blocked" in r for r in asr.eligibility.reasons)


def test_legacy_deterministic_amenities_need_no_model_or_worker(monkeypatch):
    _stub_legacy(monkeypatch, rows={}, workers=[], central=True)
    views = catalog._legacy_views()
    for name in ("doc.extract", "web.fetch"):
        view = _view(views, name)
        assert view.eligibility.eligible, (name, view.eligibility.reasons)
        assert "deterministic" in view.resources.notes
    # and the dependency probe is still a real gate
    _stub_legacy(monkeypatch, rows={}, workers=[], central=False)
    doc = _view(catalog._legacy_views(), "doc.extract")
    assert not doc.eligibility.eligible
    assert any("dependency module not importable" in r
               for r in doc.eligibility.reasons)


# ---------------------------------------------------------------------------
# Studio-side composition against the REAL studio registry (pure dataclasses +
# find_spec — no GPU, no network, no workers). The catalog must agree with the
# studio's own servability verdict: two gates, one story.
# ---------------------------------------------------------------------------


def test_studio_views_agree_with_capability_verdict():
    from abstract_hugpy_dev.video_intel.studio.presets import capability_verdict
    views = {v.name: v for v in catalog._studio_views()}
    assert set(views) == set(catalog.STUDIO_CAPABILITY_NAME.values())
    for cap, name in catalog.STUDIO_CAPABILITY_NAME.items():
        view = views[name]
        assert view.source is SourceRegistry.STUDIO
        verdict = capability_verdict(cap)
        if not verdict.servable:
            assert not view.eligibility.eligible
            assert verdict.reason in view.eligibility.reasons
        else:
            # servable per the studio -> the catalog offers it with >=1 model
            assert view.eligibility.eligible, (name, view.eligibility.reasons)
            assert view.model_ids


def test_studio_ineligible_views_explain_themselves():
    for view in catalog._studio_views():
        if not view.eligibility.eligible:
            assert view.eligibility.reasons, f"{view.name} refuses silently"


# ---------------------------------------------------------------------------
# The unified surface.
# ---------------------------------------------------------------------------


def test_list_capabilities_unified_and_sorted(monkeypatch):
    _stub_legacy(monkeypatch, workers=[{"id": "w1"}])
    views = catalog.list_capabilities()
    names = [v.name for v in views]
    assert names == sorted(names)
    assert len(names) == len(set(names))
    sources = {v.source for v in views}
    assert sources == {SourceRegistry.STUDIO, SourceRegistry.TASKS}


def test_get_capability_and_resolve_owners(monkeypatch):
    _stub_legacy(monkeypatch, workers=[{"id": "w1"}])
    view = catalog.get_capability("audio.transcribe")
    assert view is not None and view.model_ids == ("whisper-x",)
    owners = catalog.resolve_owners("audio.transcribe")
    assert owners == (SourceRegistry.TASKS, ("whisper-x",))
    assert catalog.get_capability("no.such.capability") is None
    assert catalog.resolve_owners("no.such.capability") is None


def test_unmapped_tasks_reports_only_unknown_strings(monkeypatch):
    rows = dict(_ROWS)
    rows["weird"] = {"tasks": ["quantum-flux-sorting"], "framework": "misc"}
    monkeypatch.setattr(catalog, "_legacy_registry_rows", lambda: rows)
    assert catalog.unmapped_tasks() == ("quantum-flux-sorting",)


# ---------------------------------------------------------------------------
# Route smoke: the blueprint over a bare Flask app (the app-factory boot is
# exercised by the comms suites; here the contract is the oracle wire shape).
# ---------------------------------------------------------------------------


def _client(monkeypatch):
    from flask import Flask
    from abstract_hugpy_dev.flask_app.app.routes.oracle_routes import oracle_bp
    _stub_legacy(monkeypatch, workers=[{"id": "w1"}])
    app = Flask("oracle-catalog-test")
    app.register_blueprint(oracle_bp)
    return app.test_client()


def test_route_lists_capabilities_with_eligibility_reasons(monkeypatch):
    client = _client(monkeypatch)
    resp = client.get("/oracle/capabilities")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ok"] is True
    assert body["count"] == len(body["capabilities"]) > 0
    for entry in body["capabilities"]:
        assert "." in entry["name"]
        assert entry["source"] in ("studio", "tasks")
        elig = entry["eligibility"]
        assert isinstance(elig["eligible"], bool)
        assert isinstance(elig["reasons"], list)
        if not elig["eligible"]:
            assert elig["reasons"], f"{entry['name']} refuses without a reason"


def test_route_capability_filter(monkeypatch):
    client = _client(monkeypatch)
    resp = client.get("/oracle/capabilities?capability=audio.transcribe")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["count"] == 1
    assert body["capabilities"][0]["name"] == "audio.transcribe"
    assert body["capabilities"][0]["model_ids"] == ["whisper-x"]


def test_route_unknown_capability_404s_with_known_names(monkeypatch):
    client = _client(monkeypatch)
    resp = client.get("/oracle/capabilities?capability=no.such.capability")
    assert resp.status_code == 404
    body = resp.get_json()
    assert body["ok"] is False
    assert "audio.transcribe" in body["known"]
