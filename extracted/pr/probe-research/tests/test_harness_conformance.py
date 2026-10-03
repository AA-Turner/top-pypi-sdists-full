"""Every harness in the registry against every table that still restates it.

Until each table is derived from the registry (H1-H3), these checks are what
keep the two from drifting: a fact changed in one place and not the other
fails here, naming both. As a table becomes derived, its check here becomes a
plain consumer test and stays.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from probe.daemon import adapters
from probe.harness import get_registry
from probe.sdk import agent_session

AGENT = Path(__file__).resolve().parents[1]
REG = get_registry()
CAPTURED = [h.id for h in REG.captured()]


def _tap_sources():
    spec = importlib.util.spec_from_file_location(
        "tap_sources_for_conformance", AGENT / "plugins/probe-research-tap/tap/sources.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve their module through sys.modules
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("harness_id", REG.ids())
def test_the_sdk_agent_table_agrees(harness_id):
    harness = REG.get(harness_id)
    spec = next(a for a in agent_session.AGENTS if a.label == harness_id)
    assert tuple(spec.detect_env) == harness.detect_env
    assert spec.session_env == harness.session_env
    assert spec.captured == harness.captured
    assert spec.version_env == harness.version_env
    assert spec.min_version == harness.min_version
    assert spec.display == harness.display


def test_the_sdk_agent_table_has_no_harness_the_registry_lacks():
    assert [a.label for a in agent_session.AGENTS] == list(REG.ids())


@pytest.mark.parametrize("harness_id", CAPTURED)
def test_the_tap_source_table_agrees(harness_id):
    harness = REG.get(harness_id)
    sources = _tap_sources()
    row = sources.get(harness_id)
    assert row.display_name == harness.label
    assert row.webhook_path == f"/ingest/v1/sessions/{harness.route}"
    assert row.sanitizer_module == f"tap.{harness.capture.sanitizer}"
    assert row.token_env == harness.capture.token_env
    assert row.plugin_dir_env == harness.capture.plugin_dir_env
    assert row.default_session_root == harness.transcripts["root"]
    assert row.session_id_strategy == harness.transcripts["session_id"]


def test_the_tap_has_exactly_the_captured_harnesses():
    assert sorted(_tap_sources().SOURCES) == sorted(CAPTURED)


@pytest.mark.parametrize("harness_id", CAPTURED)
def test_every_captured_harness_has_a_daemon_adapter(harness_id):
    assert adapters.for_source(harness_id).name == harness_id


@pytest.mark.parametrize("harness_id", CAPTURED)
def test_the_cli_capture_tables_agree(harness_id):
    from probe.cli import capabilities

    harness = REG.get(harness_id)
    assert capabilities.tap_token_env(harness_id) == harness.capture.token_env
    assert capabilities.consumes_cli_capture_token(harness_id) == harness.capture.cli_token_fallback


@pytest.mark.parametrize("harness_id", CAPTURED)
def test_the_cli_tap_dir_agrees(harness_id, monkeypatch, tmp_path):
    from probe.cli import capabilities

    harness = REG.get(harness_id)
    monkeypatch.delenv(harness.capture.plugin_dir_env, raising=False)
    monkeypatch.setattr(capabilities.Path, "home", lambda: tmp_path)
    assert capabilities.tap_plugin_dir(harness_id) == tmp_path / harness.capture.plugin_dir
    monkeypatch.setenv(harness.capture.plugin_dir_env, str(tmp_path / "override"))
    assert capabilities.tap_plugin_dir(harness_id) == tmp_path / "override"


@pytest.mark.parametrize("harness_id", [h.id for h in REG.installable()])
def test_the_wizard_labels_agree(harness_id):
    from probe.cli import setup

    assert setup.AGENT_LABELS[harness_id] == REG.get(harness_id).label


def test_the_wizard_installs_exactly_the_installable_harnesses():
    from probe.cli import setup

    assert sorted(setup.INSTALLABLE_AGENT_SOURCES) == sorted(h.id for h in REG.installable())


def test_one_capture_token_fallback_and_it_is_the_default():
    """The CLI config's capture token was minted for exactly one harness."""
    fallbacks = [h.id for h in REG.captured() if h.capture.cli_token_fallback]
    assert fallbacks == [REG.default]
