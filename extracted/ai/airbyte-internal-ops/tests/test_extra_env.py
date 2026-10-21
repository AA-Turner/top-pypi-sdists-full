"""Tests for CLI connector-container environment variable parsing."""

from __future__ import annotations

from pathlib import Path

import pytest

from airbyte_ops_mcp.cli import cloud
from airbyte_ops_mcp.regression_tests.models import (
    Command,
    ExecutionInputs,
    TargetOrControl,
)


def test_parse_extra_env_none() -> None:
    assert cloud._parse_extra_env(None) == {}


def test_parse_extra_env_multiple_pairs() -> None:
    assert cloud._parse_extra_env(["AIRBYTE_EDITION=CLOUD", "FOO=bar"]) == {
        "AIRBYTE_EDITION": "CLOUD",
        "FOO": "bar",
    }


def test_parse_extra_env_preserves_equals_in_value() -> None:
    assert cloud._parse_extra_env(["JAVA_TOOL_OPTIONS=-Dfoo=bar"]) == {
        "JAVA_TOOL_OPTIONS": "-Dfoo=bar"
    }


@pytest.mark.parametrize("item", ["MISSING", "=value"])
def test_parse_extra_env_rejects_invalid_pair(
    item: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit):
        cloud._parse_extra_env([item])

    error = f"Invalid --extra-env value (expected KEY=VALUE): {item}"
    assert error in capsys.readouterr().err


def test_run_connector_command_merges_extra_env_over_debug_log_level(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    captured_env: list[dict[str, str] | None] = []

    class StubResult:
        success = True
        exit_code = 0
        stdout_file_path = tmp_path / "stdout.txt"
        stderr_file_path = tmp_path / "stderr.txt"

        def save_artifacts(self, _output_dir: Path) -> None:
            pass

        def get_message_count_per_type(self) -> dict:
            return {}

        def get_record_count_per_stream(self) -> dict:
            return {}

    class StubRunner:
        def __init__(
            self, execution_inputs: ExecutionInputs, **_kwargs: object
        ) -> None:
            captured_env.append(execution_inputs.environment_variables)

        def run(self) -> StubResult:
            return StubResult()

    monkeypatch.setattr(cloud, "ConnectorRunner", StubRunner)
    monkeypatch.setattr(
        cloud.ComparableOutputs,
        "from_execution_result",
        classmethod(lambda _cls, _result: None),
    )

    cloud._run_connector_command(
        connector_image="airbyte/source-shopify:3.2.4",
        command=Command.SPEC,
        output_dir=tmp_path / "output",
        target_or_control=TargetOrControl.TARGET,
        enable_debug_logs=True,
        extra_env={"LOG_LEVEL": "INFO", "AIRBYTE_EDITION": "CLOUD"},
    )

    assert captured_env == [{"LOG_LEVEL": "INFO", "AIRBYTE_EDITION": "CLOUD"}]
