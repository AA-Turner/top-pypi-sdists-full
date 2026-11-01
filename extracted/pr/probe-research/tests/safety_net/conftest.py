"""Restructure safety net (agent side): opt-in snapshot tests, the `baseline` and `child_env` fixtures.

Runs only with PROBE_SAFETY_NET=1 (`make safety-net`); there a skip counts as a failure.
Twin: tests/safety_net/conftest.py (server side). Why and how to refresh: DESIGN.md.
"""

from __future__ import annotations

import difflib
import json
import os
import signal
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ENABLED = os.environ.get("PROBE_SAFETY_NET") == "1"
UPDATE = os.environ.get("PROBE_SAFETY_NET_UPDATE") == "1"
_SKIP = pytest.mark.skip(reason="restructure safety net: run it with `make safety-net` (PROBE_SAFETY_NET=1)")

if not ENABLED:
    # Like tests/selfhost: a plain `pytest` never collects the net; it is its own lane.
    collect_ignore_glob = ["*"]


def _ours(path: str | os.PathLike) -> bool:
    return HERE in Path(path).resolve().parents


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    # A nested conftest still sees the whole session's items: touch only ours.
    if ENABLED:
        return
    for item in items:
        if _ours(item.path):
            item.add_marker(_SKIP)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    # Opted in, a skipped net test would read green while checking nothing.
    if ENABLED and report.skipped and _ours(item.path):
        report.outcome = "failed"
        report.longrepr = f"safety net test skipped (a skip is a failure here): {report.longrepr}"


def render(data: object) -> str:
    """Stable JSON text for a baseline file."""
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


@pytest.fixture
def baseline(request: pytest.FixtureRequest):
    """`baseline(name, data)`: compare data with `<test dir>/baselines/<name>`, or rewrite it under --update.

    A name without a suffix is JSON (`render`); a `.txt` name takes a str as-is.
    """
    folder = Path(request.node.path).resolve().parent / "baselines"

    def check(name: str, data: object) -> None:
        path = folder / (name if "." in name else f"{name}.json")
        text = data if path.suffix == ".txt" else render(data)
        assert isinstance(text, str), f"{name}: a .txt baseline takes a str"
        if UPDATE:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                path.write_text(text, encoding="utf-8")
            return
        if not path.exists():
            pytest.fail(f"no baseline {path}; record one with `make safety-net-update`", pytrace=False)
        expected = path.read_text(encoding="utf-8")
        if expected != text:
            diff = "".join(
                difflib.unified_diff(
                    expected.splitlines(keepends=True), text.splitlines(keepends=True), "baseline", "now", n=2
                )
            )
            pytest.fail(f"{name} differs from {path}:\n{diff[:30000]}", pytrace=False)

    return check


#: Variables a child never inherits: a developer's or a harness's (a token, a session, a provider key).
_DROPPED = ("PROBE_", "CLAUDE", "CODEX", "KIMI", "PI_", "ANTHROPIC", "OPENAI", "XDG_")


def strays(home: str) -> list[int]:
    """Live processes started with this HOME: whatever a child left running."""
    needle = f"\0HOME={home}\0".encode()
    found = []
    for entry in os.scandir("/proc") if os.path.isdir("/proc") else ():
        if entry.name.isdigit() and int(entry.name) != os.getpid():
            try:
                with open(f"/proc/{entry.name}/environ", "rb") as handle:
                    if needle in b"\0" + handle.read() + b"\0":
                        found.append(int(entry.name))
            except OSError:
                continue
    return found


@pytest.fixture
def child_env(tmp_path):
    """HOME, XDG folders, TMPDIR and outbox under tmp_path; no API reachable; telemetry off.

    On the way out, any process still running with this HOME is killed and fails the test.
    """
    root = tmp_path / "child"
    for name in ("home", "config", "state", "cache", "tmp", "outbox", "empty-path"):
        (root / name).mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith(_DROPPED)}
    env.update(HOME=str(root / "home"), XDG_CONFIG_HOME=str(root / "config"), XDG_STATE_HOME=str(root / "state"),
               XDG_CACHE_HOME=str(root / "cache"), TMPDIR=str(root / "tmp"), PROBE_OUTBOX_DIR=str(root / "outbox"),
               PROBE_TELEMETRY="off", PROBE_BASE_URL="http://127.0.0.1:9", PATH=str(root / "empty-path"))
    yield env
    deadline = time.monotonic() + 3.0
    while (left := strays(env["HOME"])) and time.monotonic() < deadline:
        time.sleep(0.1)
    for pid in left:
        os.kill(pid, signal.SIGKILL)
    assert not left, f"a child left processes running: {left}"
