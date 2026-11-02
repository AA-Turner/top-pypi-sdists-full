"""Tests for strict JSON capture from existing SpecKit gate commands."""

import json

import pytest

from agentic_devtools.cli.speckit.run_phase3_gates import _invoke_json_command


def test_captures_json_and_exit_code() -> None:
    def command(argv: list[str]) -> None:
        print(json.dumps({"ok": True}))
        raise SystemExit(1)

    payload, exit_code = _invoke_json_command(command, ["--json"], "test")

    assert payload == {"ok": True}
    assert exit_code == 1


def test_treats_none_exit_code_as_success() -> None:
    def command(argv: list[str]) -> None:
        print('{"ok": true}')
        raise SystemExit()

    payload, exit_code = _invoke_json_command(command, [], "test")

    assert payload == {"ok": True}
    assert exit_code == 0


def test_rejects_non_integer_exit_code() -> None:
    def command(argv: list[str]) -> None:
        raise SystemExit("failed")

    with pytest.raises(RuntimeError, match="non-integer exit code"):
        _invoke_json_command(command, [], "test")


def test_rejects_non_object_json() -> None:
    def command(argv: list[str]) -> None:
        print("[]")

    with pytest.raises(RuntimeError, match="JSON object"):
        _invoke_json_command(command, [], "test")


def test_rejects_exit_code_two() -> None:
    def command(argv: list[str]) -> None:
        print('{"error": true}')
        raise SystemExit(2)

    with pytest.raises(RuntimeError, match="operational error"):
        _invoke_json_command(command, [], "test")


def test_wraps_unexpected_command_error() -> None:
    def command(argv: list[str]) -> None:
        raise OSError("unavailable")

    with pytest.raises(RuntimeError, match="unavailable"):
        _invoke_json_command(command, [], "test")
