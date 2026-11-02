"""Jira dry-run manifest capability."""

from __future__ import annotations

from typing import Any

from agentic_devtools.adapters.dry_run_manifest import build_dry_run_manifest
from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol


class _JiraProviderDryRunMixin(_JiraProviderMixinProtocol):
    """Collect and build Jira dry-run manifests."""

    def get_dry_run_manifest(self) -> dict[str, Any]:
        """Return the accumulated dry-run manifest."""
        return build_dry_run_manifest(
            issues=self._dry_run_issues,
            dependencies=self._dry_run_deps,
        )
