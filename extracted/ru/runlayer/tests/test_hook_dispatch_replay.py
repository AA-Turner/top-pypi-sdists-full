"""Replay client-shaped hook payloads through the Python ``run_hook`` path.

``test_hook_replay_fixtures.py`` drives the legacy bash shim. Every current
installer wires ``aiwatch hook --client <name>`` instead, so contract fixtures
for those clients live under ``tests/fixtures/hook_dispatch/<client>/`` and run
``run_hook()`` in-process with the relay boundary faked. Each case pins the
exact stdout / exit contract the client sees plus which relay targets were hit.

Fixture schema (one JSON object per file; ``cases`` expands a matrix):

    client        hook client id, as passed to ``--client``
    mode          monitor | protect | enforce            (default enforce)
    input         stdin payload, client-shaped
    env           extra hook environment
    files         home-relative (``~/``) or cwd-relative config files to seed
    relay         fake responses: {"tool-pre": {...}, "tool-post": {...},
                  "enforce": {...}}; missing targets answer allow
    expect        returncode, stdout_empty, stdout_json, stdout_json_subset,
                  stderr_contains, captured [{target, subset}], absent_targets
"""

from __future__ import annotations

import io
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook import hook_io
from runlayer_cli.hook_install.clients import (
    _ENFORCEMENT_HOOKS,
    _PIPELINE_HOOKS,
    Client as InstallClient,
)
from runlayer_cli.mdm_config import AIWatchMode

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "hook_dispatch"

# Fixture dir -> installer client whose registered events every dir must cover.
_COVERAGE_CLIENTS: dict[str, InstallClient] = {
    "devin_cli": InstallClient.DEVIN_CLI,
}

_DEFAULT_RELAY: dict[str, dict[str, Any]] = {
    "tool-pre": {"permission": "allow"},
    "tool-post": {"blocked": False},
    "enforce": {"permission": "allow", "evaluated_mode": "enforce"},
}


def _fixture_cases() -> list[tuple[str, dict[str, Any]]]:
    fixture_cases: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(FIXTURE_ROOT.glob("*/*.json")):
        raw_case = json.loads(path.read_text())
        if "cases" not in raw_case:
            fixture_cases.append((f"{path.parent.name}/{path.stem}", raw_case))
            continue
        base_case = {key: value for key, value in raw_case.items() if key != "cases"}
        for named_case in raw_case["cases"]:
            case = {**base_case}
            for key, value in named_case.items():
                if key == "name":
                    continue
                if key in ("files", "env", "input") and isinstance(
                    base_case.get(key), dict
                ):
                    case[key] = {**base_case[key], **value}
                else:
                    case[key] = value
            fixture_cases.append(
                (f"{path.parent.name}/{path.stem}/{named_case['name']}", case)
            )
    return fixture_cases


def _fixture_id(fixture_case: tuple[str, dict[str, Any]]) -> str:
    return fixture_case[0]


def _seed_files(files: Mapping[str, Any], *, home: Path, cwd: Path) -> None:
    for relative, payload in files.items():
        root = home if relative.startswith("~/") else cwd
        path = root / relative.removeprefix("~/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload if isinstance(payload, str) else json.dumps(payload))


def _is_subset(expected: Any, actual: Any) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _is_subset(value, actual[key])
            for key, value in expected.items()
        )
    if isinstance(expected, list):
        return (
            isinstance(actual, list)
            and len(expected) == len(actual)
            and all(_is_subset(e, a) for e, a in zip(expected, actual, strict=True))
        )
    return expected == actual


class _FakeRelay:
    """Stands in for every relay entrypoint dispatch imports."""

    def __init__(self, responses: Mapping[str, Any]) -> None:
        self.responses = {**_DEFAULT_RELAY, **responses}
        self.captured: list[dict[str, Any]] = []

    def _record(self, target: str, **fields: Any) -> None:
        self.captured.append({"target": target, **fields})

    def forward_event(
        self, client: str, event_name: str, payload: dict[str, Any], **_: Any
    ) -> None:
        self._record("event", client=client, event_name=event_name, payload=payload)

    def forward_stop_event(
        self, client: str, event_name: str, payload: dict[str, Any], **_: Any
    ) -> None:
        self._record("stop", client=client, event_name=event_name, payload=payload)

    def forward_tool_lifecycle(
        self,
        target: str,
        client: str,
        event_name: str,
        tool_name: str,
        payload: dict[str, Any],
        **_: Any,
    ) -> None:
        self._record(
            target,
            client=client,
            event_name=event_name,
            tool_name=tool_name,
            payload=payload,
        )

    def check_tool_lifecycle(
        self,
        target: str,
        client: str,
        event_name: str,
        tool_name: str,
        payload: dict[str, Any],
        **_: Any,
    ) -> str:
        self.forward_tool_lifecycle(target, client, event_name, tool_name, payload)
        return json.dumps(self.responses[target])

    def enforce(self, payload: str, **_: Any) -> str:
        self._record("enforce", payload=json.loads(payload))
        return json.dumps(self.responses["enforce"])

    def forward_mcp_usage_metadata(self, *args: Any, **_: Any) -> None:
        self._record("mcp-usage", args=list(args))

    def start_transcript_stream(self, *_: Any, **__: Any) -> bool:
        return True


def _run_case(
    case: dict[str, Any], *, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[int, str, str, _FakeRelay]:
    home = tmp_path / "home"
    cwd = tmp_path / "project"
    home.mkdir()
    cwd.mkdir()
    _seed_files(case.get("files", {}), home=home, cwd=cwd)

    relay = _FakeRelay(case.get("relay", {}))
    for name in (
        "forward_event",
        "forward_stop_event",
        "forward_tool_lifecycle",
        "check_tool_lifecycle",
        "enforce",
        "forward_mcp_usage_metadata",
        "start_transcript_stream",
    ):
        monkeypatch.setattr(hook_dispatch, name, getattr(relay, name))
    mode = AIWatchMode(case.get("mode", "enforce"))
    monkeypatch.setattr(hook_dispatch, "_resolve_mode", lambda: mode)
    monkeypatch.setattr(hook_dispatch, "_resolve_metadata_only", lambda: False)
    monkeypatch.setattr(hook_dispatch, "_resolve_scan_only", lambda: False)

    # Isolate from the developer's machine: no real home configs, no
    # host-process env leaking through hook_io.getenv's os.environ fallback,
    # and no flow spool writes.
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("RUNLAYER_FLOW_TRACE", "0")
    for var in ("HOOK_EVENT_NAME", "CURSOR_VERSION", "DEVIN_PROJECT_DIR", "CLAUDECODE"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.chdir(cwd)

    stdout = io.StringIO()
    stderr = io.StringIO()
    request_io = hook_io.HookIO(
        stdin_text=json.dumps(case["input"]),
        stdout=stdout,
        stderr=stderr,
        env=dict(case.get("env", {})),
        cwd=str(cwd),
        argv=["aiwatch", "hook", "--client", case["client"]],
    )
    returncode = 0
    with hook_io.scoped(request_io):
        try:
            hook_dispatch.run_hook()
        except SystemExit as exc:
            returncode = int(exc.code or 0)
    return returncode, stdout.getvalue(), stderr.getvalue(), relay


def _assert_expectations(
    expect: Mapping[str, Any],
    *,
    returncode: int,
    stdout: str,
    stderr: str,
    relay: _FakeRelay,
) -> None:
    assert returncode == expect.get("returncode", 0)
    if expect.get("stdout_empty"):
        assert stdout == ""
    if "stdout_json" in expect:
        assert json.loads(stdout) == expect["stdout_json"]
    if "stdout_json_subset" in expect:
        assert _is_subset(expect["stdout_json_subset"], json.loads(stdout)), stdout
    if "stderr_contains" in expect:
        assert expect["stderr_contains"] in stderr
    for wanted in expect.get("captured", []):
        matches = [c for c in relay.captured if c["target"] == wanted["target"]]
        assert matches, f"no relay call to {wanted['target']}: {relay.captured}"
        assert any(_is_subset(wanted.get("subset", {}), c) for c in matches), (
            wanted,
            matches,
        )
    for target in expect.get("absent_targets", []):
        assert all(c["target"] != target for c in relay.captured), relay.captured


@pytest.mark.parametrize("fixture_case", _fixture_cases(), ids=_fixture_id)
def test_hook_dispatch_fixture(
    fixture_case: tuple[str, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _, case = fixture_case
    returncode, stdout, stderr, relay = _run_case(
        case, monkeypatch=monkeypatch, tmp_path=tmp_path
    )
    _assert_expectations(
        case["expect"], returncode=returncode, stdout=stdout, stderr=stderr, relay=relay
    )


@pytest.mark.parametrize(
    ("fixture_dir", "install_client"), sorted(_COVERAGE_CLIENTS.items())
)
def test_every_registered_event_has_a_fixture(
    fixture_dir: str, install_client: InstallClient
) -> None:
    """Each event the installer wires for a client needs at least one replay."""
    covered = {
        case["input"].get("hook_event_name")
        for name, case in _fixture_cases()
        if name.startswith(f"{fixture_dir}/")
    }
    registered = set(_ENFORCEMENT_HOOKS[install_client]) | set(
        _PIPELINE_HOOKS[install_client]
    )
    assert registered <= covered, sorted(registered - covered)
