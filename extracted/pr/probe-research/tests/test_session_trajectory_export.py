"""`probe session export` and the SDK under it: a captured session's ATIF
trajectory, reassembled from every page the API serves.
"""

from __future__ import annotations

import json

from typer.testing import CliRunner

from probe.cli.main import app as cli_app

SID = "643ce138-4801-4409-b69c-ca30ab7605bc"


def _trajectory(steps: int) -> dict:
    return {
        "schema_version": "ATIF-v1.8",
        "session_id": SID,
        "agent": {"name": "codex", "version": "0.99.0"},
        "steps": [
            {"step_id": i, "source": "user", "message": f"turn {i}"} for i in range(1, steps + 1)
        ],
        "final_metrics": {"total_steps": steps},
    }


def test_export_joins_every_page_in_order(client, app) -> None:
    # 4,500 steps: three pages at the SDK's 2,000-step page size.
    app.session_trajectories[(SID, "codex")] = _trajectory(4500)
    document = client.export_session_trajectory(SID, source="codex")
    assert [s["step_id"] for s in document["steps"]] == list(range(1, 4501))
    assert document["agent"] == {"name": "codex", "version": "0.99.0"}
    assert document["final_metrics"] == {"total_steps": 4500}
    pages = [r for r in app.requests if r.url.path.endswith("/trajectory")]
    assert [int(r.url.params["step_from"]) for r in pages] == [1, 2001, 4001]
    assert all(r.url.params["source"] == "codex" for r in pages)


def test_export_writes_the_document_to_a_file(client, app, tmp_path, monkeypatch) -> None:
    import importlib

    cli = importlib.import_module("probe.cli.main")

    app.session_trajectories[(SID, "claude_code")] = _trajectory(3)
    monkeypatch.setattr(cli, "_client", lambda **_: client)
    out = tmp_path / "session.atif.json"
    result = CliRunner().invoke(cli_app, ["session", "export", SID, "--out", str(out)])
    assert result.exit_code == 0, result.output
    assert "3 steps" in result.output
    assert json.loads(out.read_text())["steps"][2]["message"] == "turn 3"


def _cli(client, monkeypatch):
    import importlib

    cli = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(cli, "_client", lambda **_: client)
    return CliRunner()


def test_export_without_source_asks_each_captured_agent(client, app, monkeypatch) -> None:
    app.session_trajectories[(SID, "codex")] = _trajectory(2)
    result = _cli(client, monkeypatch).invoke(cli_app, ["session", "export", SID])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["agent"]["name"] == "codex"
    tried = [r.url.params["source"] for r in app.requests if r.url.path.endswith("/trajectory")]
    assert tried[:2] == ["claude_code", "codex"]


def test_export_stops_at_the_agent_whose_session_has_no_trajectory_yet(
    client, app, monkeypatch
) -> None:
    app.session_trajectories[(SID, "claude_code")] = "not_built"
    app.session_trajectories[(SID, "codex")] = _trajectory(2)
    result = _cli(client, monkeypatch).invoke(cli_app, ["session", "export", SID])
    assert result.exit_code != 0
    assert "no trajectory yet" in str(result.exception)
    tried = [r.url.params["source"] for r in app.requests if r.url.path.endswith("/trajectory")]
    assert tried == ["claude_code"]


def test_export_names_every_agent_it_tried_when_none_has_the_session(
    client, app, monkeypatch
) -> None:
    result = _cli(client, monkeypatch).invoke(cli_app, ["session", "export", SID])
    assert result.exit_code != 0
    assert "any known agent" in str(result.exception) and "codex" in str(result.exception)


def test_export_refuses_pages_that_do_not_add_up(client, app) -> None:
    import pytest

    from probe import errors

    app.session_trajectories[(SID, "codex")] = _trajectory(2500)
    real = client.session_trajectory

    def rewritten_between_pages(*args, **kwargs):
        page = real(*args, **kwargs)
        if kwargs.get("step_from", 1) > 1:
            page = {**page, "total_steps": page["total_steps"] + 1}
        return page

    client.session_trajectory = rewritten_between_pages
    with pytest.raises(errors.ServerError):
        client.export_session_trajectory(SID, source="codex")
