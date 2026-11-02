"""Shared state for one CLI invocation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from labqoat.cli.auth.credential_resolver import CredentialResolver
from labqoat.cli.config.profile import Profile
from labqoat.cli.config.profile_store import ProfileStore

if TYPE_CHECKING:
    from labqoat._generated.transport import Transport
    from labqoat.assets_client import AssetsClient
    from labqoat.client import Client
    from labqoat.compute_client import ComputeClient
    from labqoat.dashboards_client import DashboardsClient
    from labqoat.datasets_client import DatasetsClient
    from labqoat.management_client import ManagementClient
    from labqoat.projects.project_selection import ProjectSelection
    from labqoat.runs_client import RunsClient


class CliContext:
    """Profile, credential, and client wiring for commands."""

    def __init__(
        self,
        profile: Profile,
        resolver: CredentialResolver | None = None,
        store: ProfileStore | None = None,
        output_mode: str = "json",
        project: str | None = None,
    ) -> None:
        """Store the active profile and collaborators; ``project`` is the explicit ``--project`` value."""
        self.profile = profile
        self._project = project
        self._selection: ProjectSelection | None = None
        self.resolver = resolver if resolver is not None else CredentialResolver()
        self.profiles = store if store is not None else ProfileStore()
        self.output_mode = output_mode

    def selection(self) -> ProjectSelection:
        """Resolve the project once per invocation: --project, LABQOAT_PROJECT, then pyproject.toml."""
        if self._selection is None:
            import click

            from labqoat.projects.project_selection import ProjectSelection

            try:
                self._selection = ProjectSelection.resolve(self._project)
            except ValueError as error:
                raise click.UsageError(str(error)) from error
        return self._selection

    def project_name(self) -> str:
        """The selected project for a command that acts on one, or a usage error saying how to select it."""
        import click

        try:
            return self.selection().required()
        except ValueError as error:
            raise click.UsageError(str(error)) from error

    def client(self, project: str | None = None) -> Client:
        """Build an authenticated SDK client without prompting, for a named project or the selected one."""
        from labqoat.client import Client
        from labqoat.compute.upload_memo import UploadMemo

        credentials = self.resolver.resolve(self.profile, prompt=False)
        client = Client(
            self.profile.base_url,
            credentials.username,
            credentials.password,
            timeout_seconds=self.profile.timeout_seconds,
            environment=self.profile.environment,
            project=project or self.selection().name,
        )
        return client.with_uploads(UploadMemo.for_service(self.profile.base_url, self.profile.environment))

    def transport(self, agent: str | None = None) -> Transport:
        """Build a shared transport for domain clients."""
        from labqoat._generated.transport import Transport

        credentials = self.resolver.resolve(self.profile, prompt=False)
        return Transport(
            base_url=self.profile.base_url,
            username=credentials.username,
            password=credentials.password,
            timeout_seconds=self.profile.timeout_seconds,
            environment=self.profile.environment,
            project=self.selection().name,
            agent=agent,
        )

    def assets(self) -> AssetsClient:
        """Build the asset client."""
        from labqoat.assets_client import AssetsClient

        return AssetsClient(self.transport())

    def datasets(self) -> DatasetsClient:
        """Build the dataset client."""
        from labqoat.datasets_client import DatasetsClient

        return DatasetsClient(self.transport())

    def dashboards(self) -> DashboardsClient:
        """Build the dashboard client."""
        from labqoat.dashboards_client import DashboardsClient

        return DashboardsClient(self.transport())

    def runs(self) -> RunsClient:
        """Build the run client."""
        from labqoat.runs_client import RunsClient

        return RunsClient(self.transport())

    def compute(self) -> ComputeClient:
        """Build the revision-checked compute policy and connected-host client."""
        from labqoat.compute_client import ComputeClient

        return ComputeClient(self.transport())

    def management(self, agent: str | None = None) -> ManagementClient:
        """Build the explicit JSON management client used by canonical commands."""
        from labqoat.management_client import ManagementClient

        return ManagementClient(self.transport(agent))

    def origin(self) -> str:
        """Return the normalized API origin for credential scoping."""
        return self.resolver.origin(self.profile.base_url)
