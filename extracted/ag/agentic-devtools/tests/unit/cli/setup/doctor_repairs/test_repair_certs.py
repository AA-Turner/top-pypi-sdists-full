"""Tests for repair_certs — certificate repair with npm-conditionality."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.setup.commands import _SETUP_HOSTS
from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor_repairs import repair_certs


def _ca_dep(found: bool = False) -> DependencyStatus:
    return DependencyStatus(name="ca-bundle", found=found, required=True)


class TestRepairCertsNpmEnabled:
    """repair_certs with npm_enabled=True writes bundle and updates npmrc."""

    @patch("agentic_devtools.cli.setup.doctor_repairs._upsert_npmrc_cafile")
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle")
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=True)
    def test_npm_enabled_calls_upsert_npmrc(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        mock_upsert: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When npm is enabled, _upsert_npmrc_cafile is called with the unified path."""
        unified = tmp_path / "unified.pem"
        unified.touch()
        mock_ensure.return_value = str(tmp_path / "host.pem")
        mock_build.return_value = unified

        dep = _ca_dep()
        repair_certs(dep, repo_root=tmp_path)

        mock_upsert.assert_called_once_with(unified)
        assert dep.found is True
        assert dep.path == str(unified)

    @patch("agentic_devtools.cli.setup.doctor_repairs._upsert_npmrc_cafile")
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle", return_value=None)
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=True)
    def test_npm_enabled_pem_none_still_builds(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        mock_upsert: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When npm cert returns None, unified bundle is still built."""
        unified = tmp_path / "unified.pem"
        unified.touch()
        mock_build.return_value = unified

        dep = _ca_dep()
        repair_certs(dep, repo_root=tmp_path)

        # npmrc still updated even when individual cert returns None.
        mock_upsert.assert_called_once_with(unified)
        assert dep.found is True


class TestRepairCertsNpmDisabled:
    """repair_certs with npm_enabled=False writes bundle but does NOT touch npmrc."""

    @patch("agentic_devtools.cli.setup.doctor_repairs._upsert_npmrc_cafile")
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle")
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=False)
    def test_npm_disabled_does_not_call_upsert(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        mock_upsert: MagicMock,
        tmp_path: Path,
    ) -> None:
        """When npm is disabled, _upsert_npmrc_cafile is NOT called."""
        unified = tmp_path / "unified.pem"
        unified.touch()
        mock_ensure.return_value = str(tmp_path / "host.pem")
        mock_build.return_value = unified

        dep = _ca_dep()
        repair_certs(dep, repo_root=tmp_path)

        mock_upsert.assert_not_called()
        assert dep.found is True

    @patch("agentic_devtools.cli.setup.doctor_repairs._upsert_npmrc_cafile")
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.setup.doctor_repairs.time.monotonic")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle")
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=False)
    def test_npmrc_not_clobbered_when_npm_disabled(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_time: MagicMock,
        mock_build: MagicMock,
        mock_upsert: MagicMock,
        tmp_path: Path,
    ) -> None:
        """_upsert_npmrc_cafile is never called when npm is disabled."""
        n = len(_SETUP_HOSTS)
        mock_time.side_effect = [0.0] + [1.0] * n
        unified = tmp_path / "unified.pem"
        unified.touch()
        mock_ensure.return_value = str(tmp_path / "host.pem")
        mock_build.return_value = unified

        dep = _ca_dep()
        repair_certs(dep, repo_root=tmp_path)

        mock_upsert.assert_not_called()
        assert dep.found is True


class TestRepairCertsFailure:
    """repair_certs raises on build failure."""

    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle", return_value=None)
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle", return_value=None)
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=False)
    def test_raises_when_build_fails(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Raises RuntimeError when unified bundle cannot be built."""
        dep = _ca_dep()
        with pytest.raises(RuntimeError, match="Failed to build unified CA bundle"):
            repair_certs(dep, repo_root=tmp_path)

    @patch(
        "agentic_devtools.cli.setup.doctor_repairs._upsert_npmrc_cafile",
        side_effect=OSError("permission denied"),
    )
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle", return_value=None)
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=True)
    def test_upsert_npmrc_failure_is_wrapped(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        mock_upsert: MagicMock,
        tmp_path: Path,
    ) -> None:
        """npmrc update failures are wrapped in RuntimeError with repair context."""
        unified = tmp_path / "unified.pem"
        unified.touch()
        mock_build.return_value = unified

        dep = _ca_dep()
        with pytest.raises(RuntimeError, match="Failed to update ~/.agdt/npmrc with cafile="):
            repair_certs(dep, repo_root=tmp_path)


class TestRepairCertsTimeout:
    """repair_certs enforces 60s timeout via time tracking."""

    @patch("agentic_devtools.cli.setup.doctor_repairs.time.monotonic")
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle")
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=False)
    def test_timeout_raises_runtime_error(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        mock_time: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Raises RuntimeError when cert fetching exceeds 60s timeout."""
        # start=0, first loop check already over 60s.
        mock_time.side_effect = [0.0, 61.0]

        dep = _ca_dep()
        with pytest.raises(RuntimeError, match="timed out"):
            repair_certs(dep, repo_root=tmp_path)

    @patch("agentic_devtools.cli.setup.doctor_repairs.time.monotonic")
    @patch("agentic_devtools.cli.setup.commands._build_unified_ca_bundle")
    @patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle")
    @patch("agentic_devtools.cli.setup.npm_footprint.detect_npm_footprint", return_value=True)
    def test_npm_cert_skipped_when_timeout_reached(
        self,
        mock_detect: MagicMock,
        mock_ensure: MagicMock,
        mock_build: MagicMock,
        mock_time: MagicMock,
        tmp_path: Path,
    ) -> None:
        """npm registry cert fetch is skipped when timeout is reached after host fetches."""
        # Calls: start + one timeout-check per host (all within budget) + npm-check over budget.
        n = len(_SETUP_HOSTS)
        mock_time.side_effect = [0.0] + [10.0 * (i + 1) for i in range(n)] + [61.0]
        mock_ensure.return_value = "/some/pem"
        unified = tmp_path / "unified.pem"
        unified.touch()
        mock_build.return_value = unified

        dep = _ca_dep()
        repair_certs(dep, repo_root=tmp_path)

        # npm cert was skipped due to timeout.
        # ensure_ca_bundle called once per setup host only, not for npm registry.
        assert mock_ensure.call_count == n
        assert dep.found is True
