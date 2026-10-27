"""`probe repair` (plan clean-uninstall-reinstall R-T6): the install pipeline in repair mode.

It reports COMPLETE or INCOMPLETE with the reasons (exit 0 / 1), refuses while
an uninstall runs (exit 2), and `--json` gives the wizard's NDJSON events. The
CLI part runs with real uv (`reinstall_harness`); the parts that would start a
service or reach a server are stood in for.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time

import pytest
import typer

from probe._shared import installs, uninstall_barrier
from probe.cli import repair
from probe.core import events
from tests.reinstall_harness import reinstall_wheels, uv_machine  # noqa: F401 -- fixtures


@pytest.fixture
def parts(monkeypatch):
    """Every part answers from `said` (its Part); the CLI's outcome has no env."""
    said = {name: repair.Part(lines=[f"{name} ok"]) for name in ("cli", "keeper", "identity", "service")}
    integrations = {"claude_code": repair.Part(lines=["plugins ok"])}
    monkeypatch.setattr(repair, "repair_cli", lambda: (said["cli"], None))
    monkeypatch.setattr(repair, "repair_keeper", lambda out: said["keeper"])
    monkeypatch.setattr(repair, "repair_identity", lambda: said["identity"])
    monkeypatch.setattr(repair, "repair_service", lambda out: said["service"])
    monkeypatch.setattr(repair, "_agents", lambda: list(integrations))

    class Done:
        def __init__(self, part):
            self.lines, self.problems = part.lines, part.problems

    monkeypatch.setattr(repair, "repair_integrations",
                        lambda sources: {s: Done(integrations[s]) for s in sources})
    return said, integrations


def _json_run(monkeypatch) -> tuple[int, list[dict]]:
    out = io.StringIO()
    code = 0
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "stdout", out)
        try:
            repair.run(json_output=True)
        except typer.Exit as exc:
            code = exc.exit_code
    return code, [json.loads(line) for line in out.getvalue().splitlines() if line.strip()]


def test_a_complete_machine_says_so(parts, monkeypatch):
    code, lines = _json_run(monkeypatch)
    done = lines[-1]
    assert code == 0 and done["event"] == "done" and done["complete"] is True
    steps = {(s["name"], s.get("agent")) for s in done["steps"]}
    assert {(events.Step.REPAIR_CLI, None), (events.Step.KEEPER, None), (events.Step.IDENTITY, None),
            (events.Step.SERVICE, None), (events.Step.REPAIR_INTEGRATIONS, "claude_code")} <= steps


def test_an_incomplete_machine_says_why(parts, monkeypatch):
    said, _integrations = parts
    said["identity"].problems.append("PROBE_TOKEN in this environment belongs to another account: unset PROBE_TOKEN")
    code, lines = _json_run(monkeypatch)
    assert code == repair.INCOMPLETE_EXIT
    assert lines[-1]["complete"] is False
    result = next(line for line in lines if line["event"] == "result")
    device = next(row for row in result["agents"] if row["agent"] is None)
    assert device["ok"] is False and "PROBE_TOKEN" in device["message"]


def test_it_refuses_while_an_uninstall_runs(parts, monkeypatch):
    from probe.service import procid

    path = uninstall_barrier.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"v": 1, "pid": os.getpid(), "start": procid.start_time(os.getpid()),
                                "at": time.time(), "plan": "x", "phase": "stopping"}))
    code, lines = _json_run(monkeypatch)
    assert code == repair.REFUSED_EXIT
    assert any(line["event"] == "error" and "uninstall" in line["message"] for line in lines)


def test_the_cli_part_rebuilds_a_broken_env_with_real_uv(uv_machine, monkeypatch):
    """`probe repair` run by a person whose active env no longer imports."""
    from probe.cli import install_pipeline

    m = uv_machine
    assert install_pipeline.install_cli("1.0.1").ok
    broken = installs.active(m.tools)
    run = next(broken.glob("lib/python3*/site-packages/probe/core/run.py"))
    run.unlink()
    part, out = repair.repair_cli()
    assert not part.problems, part.problems
    assert out.ok and out.changed and installs.active(m.tools).parent.name == "1.0.1+g2"
    assert m.probe() == "probe 1.0.1"


def test_the_service_part_restarts_a_service_on_another_env(monkeypatch):
    """The service runs the old generation: stopped, started on the active env."""
    from pathlib import Path

    from probe.service import client

    answers = [{"service_version": "1.0.0", "env": "/v/1.0.0/probe-research"}, None,
               {"service_version": "1.0.0", "env": "/v/1.0.0+g2/probe-research"}]
    calls = []
    monkeypatch.setattr(repair, "_hello", lambda version: answers.pop(0) if answers else None)
    monkeypatch.setattr(client, "call", lambda method, *a, **kw: calls.append(method) or {"stopping": True})
    monkeypatch.setattr(client, "ensure", lambda wait=0.0: calls.append("ensure") or client.Ensured.SPAWNED)

    class Out:
        env = Path("/v/1.0.0+g2/probe-research")
        version = "1.0.0"

    part = repair.repair_service(Out())
    assert not part.problems, part.problems
    assert calls == ["service.stop", "ensure"]
    assert any("stopped the Probe service" in line for line in part.lines)
