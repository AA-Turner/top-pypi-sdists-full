"""SaaS github-documents-cloud ingestion source.

Reuses the OSS ``GitHubDocumentsSource`` import logic wholesale and only swaps
in GitHub App connection auth (with a personal-access-token fallback). The
GitHub App path obtains short-lived installation tokens from the DataHub backend
via GraphQL, so the executor never handles the App signing key.
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional

from pydantic import SecretStr

from acryl_datahub_cloud.github_documents_cloud.config import (
    GitHubDocumentsCloudSourceConfig,
)
from acryl_datahub_cloud.github_documents_cloud.graphql_auth import (
    GraphQLInstallationTokenProvider,
)
from acryl_datahub_cloud.github_documents_cloud.report import (
    GitHubDocumentsCloudSourceReport,
)
from acryl_datahub_cloud.github_documents_cloud.sync_back.engine import SyncBackEngine
from acryl_datahub_cloud.github_documents_cloud.sync_back.github_writer import (
    GitHubWriteClient,
)
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    SupportStatus,
    capability,
    config_class,
    platform_name,
    support_status,
)
from datahub.ingestion.api.global_context import get_graph_context
from datahub.ingestion.api.source import (
    CapabilityReport,
    SourceCapability,
    TestConnectionReport,
)
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.ingestion.graph.client import DataHubGraph
from datahub.ingestion.source.github_documents.github_api import (
    GitHubApiClient,
    GitHubTokenProvider,
    StaticTokenProvider,
    make_repo_source_id,
    normalize_document_id,
)
from datahub.ingestion.source.github_documents.github_documents_source import (
    GitHubDocumentsSource,
)

logger = logging.getLogger(__name__)


def build_token_provider(
    config: GitHubDocumentsCloudSourceConfig,
    graph: Optional[DataHubGraph],
) -> GitHubTokenProvider:
    """Select the GitHub token provider based on the resolved auth method."""
    if config.has_app_auth:
        if graph is None:
            raise ValueError(
                "A DataHub connection is required to mint GitHub App installation "
                "tokens. Run this source via an ingestion executor or configure "
                "'datahub_api', or set 'github_token' to use a personal access token."
            )
        return GraphQLInstallationTokenProvider(graph)
    assert config.github_token is not None
    return StaticTokenProvider(config.github_token.get_secret_value())


@platform_name("GitHub")
@config_class(GitHubDocumentsCloudSourceConfig)
@support_status(SupportStatus.INCUBATING)
@capability(SourceCapability.TEST_CONNECTION, "Enabled by default")
class GitHubDocumentsCloudSource(GitHubDocumentsSource):
    """Ingest GitHub markdown/text documents using a tenant-wide GitHub App.

    Behaves identically to the OSS ``github-documents`` source but authenticates
    through the GitHub App connection installed for the tenant
    (``__system_github-0``), falling back to a personal access token when no App
    connection is configured.
    """

    config: GitHubDocumentsCloudSourceConfig
    report: GitHubDocumentsCloudSourceReport

    def __init__(
        self, config: GitHubDocumentsCloudSourceConfig, ctx: PipelineContext
    ) -> None:
        # OSS GitHubDocumentsSource.__init__ always constructs a PAT-backed client.
        # For GitHub App auth github_token is absent, so pass a throwaway token only
        # for base construction, then replace the client immediately afterward.
        init_config = config
        if config.has_app_auth:
            init_config = config.model_copy(
                update={"github_token": SecretStr("__cloud_app_auth_placeholder__")}
            )
        super().__init__(init_config, ctx)
        self.config = config
        self.client = GitHubApiClient(build_token_provider(config, ctx.graph))
        # Swap in the cloud report (adds sync-back metrics) and re-point the
        # stale-removal handler the base constructor wired to the OSS report.
        cloud_report = GitHubDocumentsCloudSourceReport()
        self.report = cloud_report
        self.stale_entity_removal_handler.report = cloud_report

    @classmethod
    def create(
        cls, config_dict: dict, ctx: PipelineContext
    ) -> "GitHubDocumentsCloudSource":
        config = GitHubDocumentsCloudSourceConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def _create_token_provider(self) -> GitHubTokenProvider:
        return build_token_provider(self.config, self.ctx.graph)

    def get_workunits_internal(self) -> Iterable[MetadataWorkUnit]:
        yield from super().get_workunits_internal()
        if self.config.sync_back.enabled:
            yield from self._run_sync_back()

    def _run_sync_back(self) -> Iterable[MetadataWorkUnit]:
        self.report.sync_back_enabled = True
        if self.ctx.graph is None:
            self.report.failure(
                title="GitHub sync-back skipped",
                message=(
                    "Sync-back requires a DataHub connection to read document "
                    "edits. Run this source via an ingestion executor or configure "
                    "'datahub_api'."
                ),
            )
            return

        try:
            engine = SyncBackEngine(
                graph=self.ctx.graph,
                writer=GitHubWriteClient(self._create_token_provider()),
                repo=self.config.repository,
                config=self.config.sync_back,
                target_branch=self.config.sync_back.target_branch or self.config.branch,
                base_directory=self.config.path_prefix.strip("/"),
                root_document_urn=self._sync_back_root_urn(),
                on_conflict=self._report_sync_back_conflict,
            )
            result = engine.run()
        except Exception as exc:
            self.report.failure(
                title="GitHub sync-back failed",
                message=(
                    "Could not write DataHub document edits back to GitHub. Verify "
                    "the GitHub credentials grant write access to the repository "
                    "and that the target branch exists."
                ),
                context=f"repository={self.config.repository}",
                exc=exc,
            )
            return

        self.report.sync_back_files_committed = result.files_committed
        self.report.sync_back_files_deleted = result.files_deleted
        self.report.sync_back_new_files = result.new_files
        self.report.sync_back_conflicts_skipped = result.conflicts_skipped
        self.report.sync_back_concurrent_edits_resolved = (
            result.concurrent_edits_resolved
        )
        self.report.sync_back_deletions_skipped = result.deletions_skipped
        self.report.sync_back_pull_request_url = result.pull_request_url
        for mcp in result.mcps:
            yield mcp.as_workunit()

    def _report_sync_back_conflict(self, document_urn: str, github_path: str) -> None:
        self.report.warning(
            title="Skipped sync-back due to conflict",
            message=(
                "A document changed in both DataHub and GitHub since the last "
                "import and sync_back.conflict_policy is 'skip', so it was not "
                "written back. Change the conflict policy or re-import to reconcile."
            ),
            context=f"{github_path} ({document_urn})",
        )

    def _sync_back_root_urn(self) -> Optional[str]:
        """Document URN whose subtree is scanned for new documents to sync back."""
        if self.config.parent_document_urn:
            return self.config.parent_document_urn
        if self.config.create_repo_root_document:
            source_id = make_repo_source_id(self.config.repository)
            return f"urn:li:document:{normalize_document_id(source_id)}"
        return None

    @classmethod
    def test_connection(cls, config_dict: dict) -> TestConnectionReport:
        try:
            config = GitHubDocumentsCloudSourceConfig.parse_obj(config_dict)
        except Exception as exc:
            return TestConnectionReport(
                internal_failure=True,
                internal_failure_reason=f"Failed to parse config: {exc}",
            )

        try:
            token_provider = build_token_provider(config, get_graph_context())
            client = GitHubApiClient(token_provider)
            client.list_matching_files(
                config.repository,
                config.branch,
                config.path_prefix.strip("/"),
                config.file_extensions[:1] or [".md"],
            )
            return TestConnectionReport(
                basic_connectivity=CapabilityReport(capable=True)
            )
        except Exception as exc:
            return TestConnectionReport(
                basic_connectivity=CapabilityReport(
                    capable=False, failure_reason=str(exc)
                ),
                internal_failure=True,
                internal_failure_reason=(
                    f"Failed to connect to GitHub repository: {exc}. "
                    "Verify the GitHub App connection (or github_token), "
                    "repository, branch, and network access."
                ),
            )
