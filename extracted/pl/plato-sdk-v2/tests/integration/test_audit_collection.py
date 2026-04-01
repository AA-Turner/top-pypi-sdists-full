"""Audit log collection integration test — spins up a real Chronos VM.

Validates:
  - tracked workspace mounts get unique scoped audit rules
  - untracked workspace mounts are not audited
  - audit logs are collected into per-workspace JSONL spool files
  - scoped metadata survives collection
  - tracked workspace commit/upload flow cleans local spool files

Requires:
  PLATO_API_KEY — Plato + Chronos API access

Run with:
  pytest tests/integration/test_audit_collection.py -m integration -v
"""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

import pytest

from plato.cli.chronos.test import TestConfig, TestRunner

logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not os.environ.get("PLATO_API_KEY"), reason="PLATO_API_KEY not set"),
]

CONFIGS_DIR = Path(__file__).resolve().parent / "configs"
AUDIT_CONFIG = CONFIGS_DIR / "audit-test.json"


def _run_audit_test(config_path: Path) -> tuple[int, str]:
    """Run the audit test via TestRunner, return (exit_code, session_id)."""
    config = TestConfig.from_file(config_path)
    runner = TestRunner(
        config=config,
        config_path=config_path,
        api_key=os.environ["PLATO_API_KEY"],
        phase_filter="all",
        pytest_args=None,
        artifacts_dir=None,
        verbose=True,
    )
    exit_code = asyncio.run(runner.run())
    return exit_code, runner.session_id


class TestAuditCollection:
    """Integration tests for filesystem audit log collection on agent VMs."""

    def test_audit_log_collection(self):
        """Agent file ops generate audit events collected via ausearch."""
        exit_code, session_id = _run_audit_test(AUDIT_CONFIG)
        assert exit_code == 0, (
            f"Audit test world failed (exit {exit_code}). "
            f"Session: {session_id}. "
            "Check session logs for detailed test results."
        )
        logger.info("Audit collection test passed. Session: %s", session_id)
