"""Tests for the browser Studio: data assembler + localhost server.

The page itself is verified visually via headless Chrome (out of band);
these pin the Python side — the render payload's shape (demo + live modes),
that the bundled page injects data with no placeholder left, and that the
localhost server serves it.
"""

from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path

import pytest
from typer.testing import CliRunner

from efterlev.cli.main import app
from efterlev.studio import web_data
from efterlev.studio.server import build_served_html, run_studio_live, run_studio_web

runner = CliRunner()
_VALID = {
    "implemented",
    "partial",
    "not_implemented",
    "not_applicable",
    "evidence_layer_inapplicable",
}


# --- build_studio_data -------------------------------------------------


def test_data_demo_mode_without_workspace() -> None:
    d = web_data.build_studio_data(None)
    assert d["mode"] == "demo"
    assert len(d["nodes"]) == 60
    assert all(n["s"] in _VALID for n in d["nodes"])
    assert all({"k", "x", "y", "t", "s", "src"} <= set(n) for n in d["nodes"])
    assert d["edges"] and all(len(e) == 2 for e in d["edges"])
    assert 0 <= d["readiness"] <= 100
    assert sum(d["counts"].values()) == 60
    assert len(d["sources"]) == 5


def test_data_live_mode_uses_real_verdicts(monkeypatch: pytest.MonkeyPatch) -> None:
    # stub the store reader so we don't need an LLM-driven gap run
    monkeypatch.setattr(
        web_data,
        "_real_verdicts",
        lambda root, ksis: {"KSI-SVC-SNT": "implemented", "KSI-AFR-ADS": "not_implemented"},
    )
    d = web_data.build_studio_data(Path("/some/ws"))
    assert d["mode"] == "live"
    by_ksi = {n["k"]: n["s"] for n in d["nodes"]}
    assert by_ksi["KSI-SVC-SNT"] == "implemented"
    assert by_ksi["KSI-AFR-ADS"] == "not_implemented"


# --- served HTML -------------------------------------------------------


def test_served_html_injects_data() -> None:
    html = build_served_html(None)
    assert "/*STUDIO_DATA*/{}" not in html  # placeholder consumed
    assert '"nodes"' in html and '"readiness"' in html
    assert "efterlev" in html
    # the injected blob is valid JSON-bearing (sanity: balanced braces present)
    assert html.count("<canvas") == 1
    # v0.1.190: star map dropped; the hero is a theme-grouped KSI grid the
    # evidence flow streams into, with hover-to-focus tile tooltips.
    assert "tilePos" in html
    assert "focusIdx" in html


# --- localhost server --------------------------------------------------


def test_stream_payload_and_page_wiring() -> None:
    # --live flags the page to stream from /events instead of the baked sample
    html = build_served_html(None, stream=True)
    assert '"stream": true' in html
    assert "EventSource" in html
    # non-stream page must NOT flag stream
    assert '"stream": false' in build_served_html(None)


def test_sample_payload_is_real_govnotes_posture() -> None:
    # `studio --sample` serves the bundled, precomputed govnotes posture
    html = build_served_html(None, sample=True)
    assert '"mode": "sample"' in html
    assert '"stream": false' in html
    data = web_data.load_sample_studio_data()
    assert data["mode"] == "sample"
    assert len(data["nodes"]) == 60
    assert all(n["s"] in _VALID for n in data["nodes"])
    # a genuinely mixed posture (not all one verdict). Regenerated from a real
    # gap run (scripts/build_govnotes_sample.py), so it matches --live: the
    # agent reserves "implemented" for full-outcome scanner coverage, which
    # scanner-only evidence rarely meets — expect partial + gaps + procedural.
    assert data["counts"].get("partial", 0) > 0
    assert data["counts"].get("not_implemented", 0) > 0
    assert len([k for k, v in data["counts"].items() if v > 0]) >= 3
    assert sum(data["counts"].values()) == 60


def test_sample_workspace_is_bundled() -> None:
    # the IaC + workflow ship in the package so --live --sample can run them
    d = web_data.sample_dir()
    assert (d / "infra" / "main.tf").is_file()
    assert (d / "github_workflows" / "ci.yml").is_file()
    assert (d / "posture.json").is_file()


def test_live_server_streams_events_then_done() -> None:
    lines = [
        '{"kind":"evidence_found","detector_id":"d","ksis":["KSI-SVC-SNT"],"source_file":"main.tf"}',
        '{"kind":"ksi_classified","ksi":"KSI-SVC-SNT","status":"implemented"}',
        '{"kind":"agent_finished","counts":{"implemented":1}}',
    ]
    url, server = run_studio_live(
        Path("."), open_browser=False, port=0, serve=False, _prefilled=lines
    )
    try:
        page = urllib.request.urlopen(url, timeout=5).read().decode()
        assert '"stream": true' in page and "EventSource" in page
        # SSE endpoint replays the buffered events then signals completion
        stream = urllib.request.urlopen(url + "events", timeout=5).read().decode()
        assert "evidence_found" in stream
        assert "ksi_classified" in stream
        assert "data: " in stream
        assert "event: done" in stream
    finally:
        server.shutdown()


def test_reports_endpoints_list_and_serve(tmp_path: Path) -> None:
    # a workspace with generated artifacts under efterlev-out/
    rd = tmp_path / "efterlev-out" / "reports"
    (rd / "poam").mkdir(parents=True)
    (rd / "gap-20260525.html").write_text("<html><span id='ksi-KSI-SVC-SNT'>x</span></html>")
    (rd / "poam" / "poam-20260525.md").write_text("# POA&M")

    url, server = run_studio_web(tmp_path, open_browser=False, port=0, serve=False)
    try:
        import json as _json

        reports = _json.loads(urllib.request.urlopen(url + "reports", timeout=5).read())["reports"]
        labels = {r["label"] for r in reports}
        assert "Gap report" in labels and "POA&M" in labels
        gap = next(r for r in reports if r["label"] == "Gap report")
        body = urllib.request.urlopen(url + "report?f=" + gap["rel"], timeout=5).read().decode()
        assert "ksi-KSI-SVC-SNT" in body
        # path-traversal is rejected
        try:
            urllib.request.urlopen(url + "report?f=../../etc/hosts", timeout=5)
            raise AssertionError("path traversal was not blocked")
        except urllib.error.HTTPError as e:
            assert e.code in (403, 404)
        # the page wires the reports panel + click-to-open
        page = urllib.request.urlopen(url, timeout=5).read().decode()
        assert "fetchReports" in page and "/report?f=" in page
    finally:
        server.shutdown()


def test_worklist_endpoint_serves_json(tmp_path: Path) -> None:
    # Real workspace root (uninitialized) — worklist returns the stage-aware items
    # (boundary discover + init). The page guards on empty, so a populated items
    # list is the contract this endpoint must keep.
    url, server = run_studio_web(tmp_path, open_browser=False, port=0, serve=False)
    try:
        import json as _json

        data = _json.loads(urllib.request.urlopen(url + "worklist", timeout=5).read())
        assert data["stage"] == "uninitialized"
        cmds = [it["command"] for it in data["items"]]
        assert any("efterlev init" in c for c in cmds)
        # the page wires the worklist card + fetch
        page = urllib.request.urlopen(url, timeout=5).read().decode()
        assert "fetchWorklist" in page and "worklistCard" in page
    finally:
        server.shutdown()


def test_watch_mode_streams_external_event_log(tmp_path: Path) -> None:
    # Attach mode: pre-write events to a log, point Studio at it, confirm /events
    # streams them and signals done after `agent_finished` (the page's streamDone
    # trigger). This is the path the AI install prompt uses — the driver runs
    # `report run` with EFTERLEV_STUDIO_EVENT_LOG=<path> while Studio --watch
    # tails the same path.
    from efterlev.studio.server import run_studio_watch

    log = tmp_path / "events.jsonl"
    log.write_text(
        '{"kind":"evidence_found","detector_id":"d","ksis":["KSI-SVC-SNT"],"source_file":"main.tf"}\n'
        '{"kind":"ksi_classified","ksi":"KSI-SVC-SNT","status":"implemented"}\n'
        '{"kind":"agent_finished","counts":{"implemented":1}}\n'
    )
    url, server = run_studio_watch(tmp_path, log, open_browser=False, port=0, serve=False)
    try:
        page = urllib.request.urlopen(url, timeout=5).read().decode()
        assert '"stream": true' in page  # attach mode flags the page to stream
        stream = urllib.request.urlopen(url + "events", timeout=5).read().decode()
        assert "evidence_found" in stream
        assert "ksi_classified" in stream
        assert "agent_finished" in stream
        assert "event: done" in stream  # agent_finished triggers the done signal
    finally:
        server.shutdown()


def test_watch_mutually_exclusive_with_live(tmp_path: Path) -> None:
    log = tmp_path / "events.jsonl"
    log.write_text("")
    result = runner.invoke(app, ["studio", "--watch", str(log), "--live"])
    assert result.exit_code == 2
    assert "mutually exclusive" in result.output.lower()


def test_worklist_endpoint_empty_in_sample_mode() -> None:
    # No workspace root (sample mode) → empty items so the card stays hidden.
    url, server = run_studio_web(None, open_browser=False, port=0, serve=False, sample=True)
    try:
        import json as _json

        data = _json.loads(urllib.request.urlopen(url + "worklist", timeout=5).read())
        assert data["items"] == []
    finally:
        server.shutdown()


def test_server_serves_page_and_204_for_other() -> None:
    url, server = run_studio_web(None, open_browser=False, port=0, serve=False)
    try:
        body = urllib.request.urlopen(url, timeout=5).read().decode()
        assert '"nodes"' in body and "efterlev studio" in body
        # unknown path → 204
        req = urllib.request.urlopen(url + "favicon.ico", timeout=5)
        assert req.status == 204
    finally:
        server.shutdown()


# --- command -----------------------------------------------------------


def test_studio_rejects_removed_tui_flag() -> None:
    # the terminal star-map (--tui) was dropped at v0.1.190; the flag is gone
    result = runner.invoke(app, ["studio", "--tui"])
    assert result.exit_code == 2
    assert "no such option" in result.output.lower() or "tui" in result.output.lower()
