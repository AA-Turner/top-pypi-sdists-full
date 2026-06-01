"""Replay sanitized real-client hook payloads through runlayer-hook.sh.

These tests complement the hand-written shell-hook unit tests with a small
contract-suite format: fixtures contain client-shaped hook input, optional
client config files, fake relay behavior, and expected hook/relay output.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

HOOK_SRC = Path(__file__).resolve().parent.parent / "hooks" / "runlayer-hook.sh"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "hook_replay"


def _fixture_cases() -> list[tuple[str, dict[str, Any]]]:
    fixture_cases: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(FIXTURE_ROOT.glob("*/*.json")):
        raw_case = json.loads(path.read_text())
        if "cases" not in raw_case:
            fixture_cases.append((f"{path.parent.name}/{path.stem}", raw_case))
            continue

        base_case = {key: value for key, value in raw_case.items() if key != "cases"}
        for named_case in raw_case["cases"]:
            name = named_case["name"]
            case = {
                **base_case,
                **{key: value for key, value in named_case.items() if key != "name"},
            }
            if "files" in base_case or "files" in named_case:
                case["files"] = {
                    **base_case.get("files", {}),
                    **named_case.get("files", {}),
                }
            if "env" in base_case or "env" in named_case:
                case["env"] = {
                    **base_case.get("env", {}),
                    **named_case.get("env", {}),
                }
            fixture_cases.append((f"{path.parent.name}/{path.stem}/{name}", case))
    return fixture_cases


def _fixture_id(fixture_case: tuple[str, dict[str, Any]]) -> str:
    return fixture_case[0]


def _write_fake_runlayer(
    bin_dir: Path,
    *,
    response: str,
    exit_code: int,
) -> None:
    bin_dir.mkdir(parents=True, exist_ok=True)
    fake = bin_dir / "runlayer"
    quoted_response = shlex.quote(response)
    fake.write_text(
        "#!/bin/bash\n"
        'if [[ "$1" == "hooks" && "$2" == "relay" ]]; then\n'
        '  target="$3"\n'
        "  _input=$(cat)\n"
        '  if [[ -n "${RUNLAYER_CAPTURE_DIR:-}" ]]; then\n'
        '    echo "$_input" | jq -c . >> "${RUNLAYER_CAPTURE_DIR}/${target}.jsonl" 2>/dev/null || echo "$_input" >> "${RUNLAYER_CAPTURE_DIR}/${target}.jsonl"\n'
        '    printf "%s\\n" "$@" >> "${RUNLAYER_CAPTURE_DIR}/argv.log"\n'
        "  fi\n"
        f"  printf '%s\\n' {quoted_response}\n"
        f"  exit {exit_code}\n"
        "fi\n"
        "exit 1\n"
    )
    fake.chmod(0o755)


def _setup_hook(home: Path, *, client: str, enforcement: bool) -> Path:
    if client == "cursor":
        hook_dir = home / ".cursor" / "hooks"
    elif client == "codex":
        hook_dir = home / ".codex" / "hooks"
    else:
        hook_dir = home / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)
    hook_copy = hook_dir / "runlayer-hook.sh"
    hook_copy.write_text(HOOK_SRC.read_text())
    hook_copy.chmod(0o755)
    (hook_dir / "runlayer-config.json").write_text(
        json.dumps({"enforcement": enforcement})
    )
    return hook_copy


def _materialize(value: Any, *, home: Path) -> Any:
    if isinstance(value, str):
        return value.replace("${HOME}", str(home))
    if isinstance(value, list):
        return [_materialize(item, home=home) for item in value]
    if isinstance(value, dict):
        return {key: _materialize(item, home=home) for key, item in value.items()}
    return value


def _write_fixture_files(home: Path, files: Mapping[str, Any]) -> None:
    for relative_path, content in files.items():
        path = home / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        materialized = _materialize(content, home=home)
        if isinstance(materialized, str):
            path.write_text(materialized)
        else:
            path.write_text(json.dumps(materialized, indent=2, sort_keys=True))


def _read_captured_payloads(capture_dir: Path) -> dict[str, list[dict[str, Any]]]:
    captured: dict[str, list[dict[str, Any]]] = {}
    for target in ("enforce", "event", "tool-pre", "tool-post"):
        path = capture_dir / f"{target}.jsonl"
        if path.exists():
            lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
            captured[target] = [json.loads(ln) for ln in lines]
    return captured


def _wait_for_targets(
    capture_dir: Path,
    target_counts: Mapping[str, int],
    *,
    timeout_seconds: float = 1.0,
) -> dict[str, list[dict[str, Any]]]:
    deadline = time.monotonic() + timeout_seconds
    captured: dict[str, list[dict[str, Any]]] = {}
    if not target_counts:
        time.sleep(timeout_seconds)
        return _read_captured_payloads(capture_dir)

    while time.monotonic() < deadline:
        captured = _read_captured_payloads(capture_dir)
        if all(
            len(captured.get(target, [])) >= count
            for target, count in target_counts.items()
        ):
            return captured
        time.sleep(0.05)
    return captured


def _assert_subset(actual: Any, expected: Any) -> None:
    if isinstance(expected, dict):
        assert isinstance(actual, dict)
        for key, value in expected.items():
            assert key in actual
            _assert_subset(actual[key], value)
        return
    if isinstance(expected, list):
        assert isinstance(actual, list)
        assert len(actual) >= len(expected)
        for actual_item, expected_item in zip(actual, expected, strict=False):
            _assert_subset(actual_item, expected_item)
        return
    assert actual == expected


@pytest.mark.parametrize("fixture_case", _fixture_cases(), ids=_fixture_id)
def test_hook_replay_fixture(
    fixture_case: tuple[str, dict[str, Any]], tmp_path: Path
) -> None:
    _, case = fixture_case
    home = tmp_path / "home"
    home.mkdir()
    capture_dir = tmp_path / "capture"
    capture_dir.mkdir()

    _write_fixture_files(home, case.get("files", {}))
    hook = _setup_hook(
        home,
        client=case["client"],
        enforcement=case.get("enforcement", True),
    )

    relay = case.get("relay", {})
    response = json.dumps(relay.get("response", {"permission": "allow"}))
    exit_code = int(relay.get("exit_code", 0))
    bin_dir = home / "bin"
    _write_fake_runlayer(
        bin_dir,
        response=response,
        exit_code=exit_code,
    )

    env = {
        **os.environ,
        "HOME": str(home),
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "RUNLAYER_CAPTURE_DIR": str(capture_dir),
    }
    env.update(case.get("env", {}))
    if case["client"] == "cursor":
        env.setdefault("CURSOR_VERSION", "1.0.0")
    else:
        env.pop("CURSOR_VERSION", None)

    input_payload = _materialize(case["input"], home=home)
    result = subprocess.run(
        ["bash", str(hook)],
        input=json.dumps(input_payload),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    expect = case["expect"]
    assert result.returncode == expect.get("returncode", 0)

    if "stdout_json" in expect:
        assert json.loads(result.stdout) == _materialize(
            expect["stdout_json"], home=home
        )
    if "stdout_json_subset" in expect:
        stdout_payload = json.loads(result.stdout)
        expected_subset = _materialize(expect["stdout_json_subset"], home=home)
        _assert_subset(stdout_payload, expected_subset)
    if expect.get("stdout_empty"):
        assert result.stdout == ""
    if "stdout_contains" in expect:
        assert expect["stdout_contains"] in result.stdout

    expected_target_counts = {
        target: 1 for target in expect.get("captured_targets", [])
    }
    for item in expect.get("captured", []):
        target = item["target"]
        count = item.get("index", 0) + 1
        expected_target_counts[target] = max(
            expected_target_counts.get(target, 0), count
        )
    captured = _wait_for_targets(capture_dir, expected_target_counts)

    for target in expect.get("captured_targets", []):
        assert target in captured
    for target in expect.get("absent_targets", []):
        assert target not in captured

    for item in expect.get("captured", []):
        target = item["target"]
        index = item.get("index", 0)
        assert target in captured
        assert len(captured[target]) > index
        expected_subset = _materialize(item.get("subset", {}), home=home)
        _assert_subset(captured[target][index], expected_subset)
