"""Tests for the A4 CommandRunner.context pass-through/fail-closed rules.

TRK-M1-01 draft A4: CommandRunner.run gains a keyword-only
``context: LocalExecutionContext | None = None``. SubprocessCommandRunner
accepts and ignores it. BeadsConnectorConfig/FPConnectorConfig gain a
``context`` field.

Pass-through rule: the connector calls ``runner.run(command, cwd=...)``
exactly as in 0.4.3 when ``config.context is None`` (so a pre-existing
0.4.3-signature runner — ``run(self, command, *, cwd=None)``, no
``context`` parameter — keeps working unchanged), and adds
``context=config.context`` only when it is not ``None``.

Fail-closed rule: constructing a connector with a non-None ``context`` but
no explicit ``runner`` raises ConnectorConfigError rather than silently
falling back to the default direct-subprocess runner (TRK-M1-01 draft D3 —
silent fallback to direct ``bd``/``fp`` is exactly the prohibited bypass).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

import pytest

from spec_kitty_tracker import ExternalRef
from spec_kitty_tracker.connectors.beads import BeadsConnector, BeadsConnectorConfig
from spec_kitty_tracker.connectors.cli_runner import SubprocessCommandRunner
from spec_kitty_tracker.connectors.fp import FPConnector, FPConnectorConfig
from spec_kitty_tracker.context import LocalExecutionContext
from spec_kitty_tracker.errors import ConnectorConfigError

CTX = LocalExecutionContext(actor="ivan", repository="spec-kitty-tracker")


@dataclass
class LegacySignatureRunner:
    """A 0.4.3-shaped runner: no ``context`` parameter at all.

    If a connector unconditionally passed ``context=`` to ``run``, calling
    this runner would raise ``TypeError: run() got an unexpected keyword
    argument 'context'``. Used to prove the pass-through rule preserves
    pre-existing runner compatibility when ``config.context is None``.
    """

    output: str = "{}"
    calls: list[dict[str, object]] = field(default_factory=list)

    def run(self, command: Sequence[str], *, cwd: str | None = None) -> str:
        self.calls.append({"command": list(command), "cwd": cwd})
        return self.output


@dataclass
class ContextAwareRunner:
    """A runner implementing the new signature, recording the context it saw."""

    output: str = "{}"
    calls: list[dict[str, object]] = field(default_factory=list)

    def run(
        self,
        command: Sequence[str],
        *,
        cwd: str | None = None,
        context: LocalExecutionContext | None = None,
    ) -> str:
        self.calls.append({"command": list(command), "cwd": cwd, "context": context})
        return self.output


def test_subprocess_command_runner_accepts_and_ignores_context() -> None:
    runner = SubprocessCommandRunner()
    # Real subprocess execution is out of scope here; this only pins the
    # signature accepts (and does not require) a context kwarg.
    import inspect

    sig = inspect.signature(runner.run)
    assert "context" in sig.parameters
    assert sig.parameters["context"].default is None


@pytest.mark.asyncio
async def test_beads_connector_omits_context_kwarg_when_config_context_is_none() -> None:
    runner = LegacySignatureRunner(output='{"id": "b1", "title": "t", "status": "open"}')
    connector = BeadsConnector(BeadsConnectorConfig(workspace="demo"), runner=runner)

    await connector.get_issue(ExternalRef(system="beads", workspace="demo", id="b1"))

    # No TypeError was raised despite LegacySignatureRunner.run having no
    # `context` parameter at all — proving the call shape was preserved.
    assert len(runner.calls) == 1


@pytest.mark.asyncio
async def test_beads_connector_passes_context_when_config_context_is_set() -> None:
    runner = ContextAwareRunner(output='{"id": "b1", "title": "t", "status": "open"}')
    connector = BeadsConnector(
        BeadsConnectorConfig(workspace="demo", context=CTX),
        runner=runner,
    )

    await connector.get_issue(ExternalRef(system="beads", workspace="demo", id="b1"))

    assert len(runner.calls) == 1
    assert runner.calls[0]["context"] is CTX


@pytest.mark.asyncio
async def test_fp_connector_omits_context_kwarg_when_config_context_is_none() -> None:
    runner = LegacySignatureRunner(output="FP-1 [todo] [medium] title")
    connector = FPConnector(FPConnectorConfig(workspace="demo"), runner=runner)

    await connector.get_issue(ExternalRef(system="fp", workspace="demo", id="FP-1"))

    # No TypeError was raised, proving no unexpected `context` kwarg was passed.
    assert len(runner.calls) >= 1


@pytest.mark.asyncio
async def test_fp_connector_passes_context_when_config_context_is_set() -> None:
    runner = ContextAwareRunner(output="FP-1 [todo] [medium] title")
    connector = FPConnector(FPConnectorConfig(workspace="demo", context=CTX), runner=runner)

    await connector.get_issue(ExternalRef(system="fp", workspace="demo", id="FP-1"))

    assert all(call["context"] is CTX for call in runner.calls)
    assert len(runner.calls) >= 1


def test_beads_connector_fails_closed_when_context_set_and_runner_none() -> None:
    with pytest.raises(ConnectorConfigError):
        BeadsConnector(BeadsConnectorConfig(context=CTX), runner=None)


def test_fp_connector_fails_closed_when_context_set_and_runner_none() -> None:
    with pytest.raises(ConnectorConfigError):
        FPConnector(FPConnectorConfig(context=CTX), runner=None)


def test_beads_connector_default_runner_allowed_when_context_is_none() -> None:
    # No exception: context is None, so falling back to the default
    # SubprocessCommandRunner is the pre-existing 0.4.3 behavior.
    connector = BeadsConnector(BeadsConnectorConfig(), runner=None)
    assert isinstance(connector._runner, SubprocessCommandRunner)


def test_fp_connector_default_runner_allowed_when_context_is_none() -> None:
    connector = FPConnector(FPConnectorConfig(), runner=None)
    assert isinstance(connector._runner, SubprocessCommandRunner)
