# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Integration tests for the introspect CLI command."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from omnibase_infra.cli.infra_test.cli import cli
from omnibase_infra.enums.generated.enum_platform_topic import EnumPlatformTopic


@pytest.mark.integration
class TestIntrospectCLI:
    """Integration tests for the introspect subcommand."""

    def test_introspect_emits_to_canonical_topic(self) -> None:
        """introspect publishes to the canonical EVT_NODE_INTROSPECTION_V1 topic."""
        runner = CliRunner()
        captured_args: list[list[str]] = []

        def fake_run(args: list[str], **kwargs: object) -> MagicMock:
            captured_args.append(args)
            result = MagicMock()
            result.returncode = 0
            result.stderr = ""
            return result

        with patch(
            "omnibase_infra.cli.infra_test.introspect.subprocess.run",
            side_effect=fake_run,
        ):
            result = runner.invoke(
                cli,
                ["introspect", "--broker", "localhost:19092"],
                catch_exceptions=False,
            )

        assert result.exit_code == 0, result.output
        assert len(captured_args) == 1
        rpk_args = captured_args[0]
        expected_topic = EnumPlatformTopic.EVT_NODE_INTROSPECTION_V1.value
        assert expected_topic in rpk_args, (
            f"Expected topic {expected_topic!r} in rpk args {rpk_args}"
        )

    def test_introspect_topic_flag_overrides_default(self) -> None:
        """--topic flag overrides the default topic but still invokes rpk."""
        runner = CliRunner()
        captured_args: list[list[str]] = []

        def fake_run(args: list[str], **kwargs: object) -> MagicMock:
            captured_args.append(args)
            result = MagicMock()
            result.returncode = 0
            result.stderr = ""
            return result

        custom_topic = "onex.evt.platform.node-introspection.v2"
        with patch(
            "omnibase_infra.cli.infra_test.introspect.subprocess.run",
            side_effect=fake_run,
        ):
            result = runner.invoke(
                cli,
                ["introspect", "--broker", "localhost:19092", "--topic", custom_topic],
                catch_exceptions=False,
            )

        assert result.exit_code == 0, result.output
        assert custom_topic in captured_args[0]

    def test_introspect_rpk_failure_exits_nonzero(self) -> None:
        """When rpk returns non-zero, the CLI exits with code 1."""
        runner = CliRunner()

        def fake_run(args: list[str], **kwargs: object) -> MagicMock:
            result = MagicMock()
            result.returncode = 1
            result.stderr = "connection refused"
            return result

        with patch(
            "omnibase_infra.cli.infra_test.introspect.subprocess.run",
            side_effect=fake_run,
        ):
            result = runner.invoke(
                cli,
                ["introspect", "--broker", "localhost:19092"],
            )

        assert result.exit_code == 1
