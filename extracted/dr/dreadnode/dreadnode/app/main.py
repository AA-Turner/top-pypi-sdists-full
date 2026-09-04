from __future__ import annotations

import contextlib
import random
import typing as t
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin

import coolname
import logfire
from logfire._internal.exporters.remove_pending import RemovePendingSpansExporter
from opentelemetry import propagate
from opentelemetry.exporter.otlp.proto.http import Compression
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from dreadnode.app.api.client import ApiClient
from dreadnode.app.config import Profile, UserConfig
from dreadnode.core.exceptions import (
    DreadnodeUsageWarning,
    handle_internal_errors,
    warn_at_user_stacklevel,
)
from dreadnode.core.load import load as load_package_util
from dreadnode.core.metric import (
    Metric,
    MetricAggMode,
    MetricDict,
    MetricsLike,
)
from dreadnode.core.tls import create_platform_http_session
from dreadnode.core.types.common import (
    INHERITED,
    AnyDict,
    Inherited,
    JsonValue,
)
from dreadnode.core.util import (
    clean_str,
    valid_version,
)
from dreadnode.packaging.package import (
    BuildResult,
    Package,
    PackageInfo,
    PackageType,
    PullResult,
    PushResult,
)
from dreadnode.storage import Storage, StorageProvider
from dreadnode.tracing.exporter import CustomOTLPSpanExporter
from dreadnode.tracing.exporters import (
    LocalStorageSpanExporter,
    TraceBackend,
    TraceExportConfig,
)
from dreadnode.tracing.span import (
    Span,
    TaskContext,
    TaskSpan,
    current_task_span,
)
from dreadnode.version import VERSION

if t.TYPE_CHECKING:
    from opentelemetry.sdk.trace import SpanProcessor
    from opentelemetry.trace import Tracer

    from dreadnode.app.api.models import Organization, Project, Workspace
    from dreadnode.capabilities.capability import Capability
    from dreadnode.core.environment import TaskEnvironment
    from dreadnode.core.scorer import ScorersLike
    from dreadnode.core.task import P, R, ScoredTaskDecorator, Task, TaskDecorator
    from dreadnode.optimization import Direction, OptimizationConfig
    from dreadnode.optimization.backends import OptimizationAdapter, OptimizationBackend
    from dreadnode.tracing.constants import SpanType


@dataclass
class CapabilityPushResult:
    """Result of a single capability push operation."""

    name: str
    version: str
    status: t.Literal["pushed", "up_to_date", "built"]
    digest: str | None = None


@dataclass
class CapabilitySyncResult:
    """Result of a batch capability sync operation."""

    uploaded: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.failed) == 0


@dataclass
class EnvironmentSyncResult:
    """Result of a batch environment/task sync operation.

    Structurally identical to CapabilitySyncResult — kept separate intentionally
    so the two domains can diverge independently.
    """

    uploaded: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.failed) == 0


def _load_environment_metadata(source_dir: Path) -> tuple[str, str]:
    """Return environment name/version from task.yaml."""
    import yaml

    task_yaml_path = source_dir / "task.yaml"
    if not source_dir.is_dir() or not task_yaml_path.is_file():
        raise FileNotFoundError(f"task.yaml not found in {source_dir}")

    raw = yaml.safe_load(task_yaml_path.read_text())
    if not isinstance(raw, dict):
        raise TypeError("task.yaml must contain a YAML mapping")

    env_name = raw.get("name") or source_dir.name
    if not isinstance(env_name, str):
        raise TypeError("task.yaml name must be a string")

    env_version = raw.get("version") or "1.0.0"
    if not isinstance(env_version, str):
        raise TypeError("task.yaml version must be a string")
    if not valid_version(env_version):
        raise ValueError(f"task.yaml version must use fixed semver (X.Y.Z), got {env_version!r}")

    return env_name, env_version


@dataclass
class Dreadnode:
    """
    The core Dreadnode SDK class.

    A default instance is created and can be used directly with `dreadnode.*`.
    Otherwise, create your own instance with `Dreadnode().configure()`.
    """

    def __init__(self) -> None:
        self.server: str | None = None
        self.api_key: str | None = None
        self.cache: Path = Path.home() / ".dreadnode"
        self.storage_provider: StorageProvider | None = None
        self.trace_backend: TraceBackend | None = None

        self.organization: str | uuid.UUID | None = None
        self.workspace: str | uuid.UUID | None = None
        self.project: str | uuid.UUID | None = None

        self.otel_scope: str = "dreadnode"
        self.console: logfire.ConsoleOptions | bool = False

        self._api: ApiClient | None = None
        self._profile: Profile | None = None
        self._storage: Storage | None = None
        self._logfire: logfire.Logfire = logfire.DEFAULT_LOGFIRE_INSTANCE
        self._logfire.config.ignore_no_config = True

        self._initialized: bool = False
        self._version: str = VERSION

        self._trace_config: TraceExportConfig | None = None
        self._local_exporter: LocalStorageSpanExporter | None = None

    @property
    def api(self) -> ApiClient:
        if self._api is None:
            raise RuntimeError("No API client - configure with server and API key")
        return self._api

    @property
    def profile(self) -> Profile:
        if self._profile is None:
            raise RuntimeError("No profile - configure with server and API key")
        return self._profile

    @property
    def session(self) -> Profile:
        """Deprecated alias for :attr:`profile`."""
        import warnings

        warnings.warn(
            "Dreadnode.session is deprecated, use .profile instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.profile

    @property
    def storage(self) -> Storage:
        if self._storage is None:
            raise RuntimeError("Call configure() first")
        return self._storage

    @property
    def can_sync(self) -> bool:
        """Whether remote sync is possible (has credentials)."""
        return self._profile is not None

    def configure(
        self,
        *,
        server: str | None = None,
        api_key: str | None = None,
        organization: str | uuid.UUID | None = None,
        workspace: str | uuid.UUID | None = None,
        project: str | uuid.UUID | None = None,
        cache: Path | str | None = None,
        storage_provider: StorageProvider | None = None,
        trace_backend: TraceBackend | None = None,
        console: logfire.ConsoleOptions | bool | None = None,
        otel_scope: str = "dreadnode",
    ) -> Dreadnode:
        """Configure the Dreadnode SDK.

        Credential resolution follows profile precedence:
        explicit args > environment variables > saved profile defaults.

        Args:
            server: Platform API URL.
            api_key: API key for authentication.
            organization: Organization key/UUID override.
            workspace: Workspace key/UUID override.
            project: Project key/UUID override.
            cache: Local cache directory (default: ~/.dreadnode).
            storage_provider: Remote storage provider (s3, r2, minio). Auto-detected if not specified.
            trace_backend: Controls remote OTLP streaming.
            console: Log span information to the console.
            otel_scope: The OpenTelemetry scope name.

        Returns:
            Configured Dreadnode SDK instance.
        """
        if self._initialized:
            return self
        if cache:
            self.cache = Path(cache)
        elif self.cache == Path.home() / ".dreadnode":
            pass
        self.storage_provider = storage_provider
        self.trace_backend = trace_backend
        self.console = console if console is not None else self.console
        self.otel_scope = otel_scope

        # Resolve credentials + context: explicit args > env vars > saved profile
        from dreadnode.app.cli.args import PlatformScopeArgs
        from dreadnode.core import startup_clock

        with startup_clock.timed("configure.resolve_profile"):
            resolved = PlatformScopeArgs(
                server=server,
                api_key=api_key,
                organization=str(organization) if organization else None,
                workspace=str(workspace) if workspace else None,
                project=str(project) if project else None,
            ).resolve()

        self.server = resolved.url
        self.api_key = resolved.api_key
        self.organization = resolved.organization
        self.workspace = resolved.workspace
        self.project = resolved.project

        if self.server and self.api_key:
            self._api = ApiClient(self.server, api_key=self.api_key)

            # Auto-resolve organization if not specified
            if not self.organization:
                with startup_clock.timed("configure.list_organizations"):
                    orgs = self._api.list_user_organizations()
                if len(orgs) == 1:
                    resolved = resolved.with_overrides(organization=orgs[0].key)
                    self.organization = orgs[0].key
                elif len(orgs) > 1:
                    org_keys = ", ".join(o.key for o in orgs)
                    raise RuntimeError(
                        f"Multiple organizations available ({org_keys}). "
                        "Specify one with --organization."
                    )
                else:
                    raise RuntimeError("No organizations found for this API key.")

            try:
                with startup_clock.timed("configure.validate_scope"):
                    resolved.validate_scope(self._api)
            except Exception as exc:
                from dreadnode.app.config import _is_transient_network_error

                if not _is_transient_network_error(exc):
                    raise
                # Transient network error — proceed without validated scope
                # so `dreadnode serve` can still start in sandbox environments
                # with flaky connectivity to the platform API.
                import logging

                logging.getLogger("dreadnode").warning(
                    "validate_scope failed (%s: %s), proceeding without server validation",
                    type(exc).__name__,
                    exc,
                )
            self._profile = resolved

            # Auto-create project if it was requested but doesn't exist yet
            if self.project and self._profile.project is None:
                ws_key = self._profile.workspace
                if ws_key:
                    try:
                        with startup_clock.timed("configure.create_project"):
                            self._api.create_project(
                                str(self.organization),
                                str(ws_key),
                                name=str(self.project),
                                key=str(self.project),
                            )
                            # Re-validate to pick up the newly created project
                            resolved = resolved.with_overrides(project=str(self.project))
                            resolved.validate_scope(self._api)
                        self._profile = resolved
                    except Exception as proj_exc:
                        logging.getLogger("dreadnode").debug(
                            "Auto-create project failed: %s", proj_exc
                        )
        else:
            self._api = None
            self._profile = None

        # Register a lazy proxy provisioner so `dn/<model>` ids route through the
        # platform LiteLLM gateway from a local SDK process - the same mechanism the
        # TUI uses. It mints a short-lived, credit-metered *virtual* key on first
        # `dn/` use (no provider keys ever reach the machine). In-memory only.
        from dreadnode.generators.proxy import (
            provision_platform_proxy,
            register_proxy_provisioner,
        )

        if self._api is not None and self.organization is not None:
            _api = self._api
            _org = str(self.organization)
            register_proxy_provisioner(
                lambda: provision_platform_proxy(_api, _org, "dreadnode-sdk")
            )
        else:
            register_proxy_provisioner(None)

        self._storage = Storage(
            profile=self._profile,
            cache=self.cache,
            api=self._api,
            provider=self.storage_provider,
            default_project=self.project,
        )
        self._local_exporter = LocalStorageSpanExporter(self._storage)
        span_processors: list[SpanProcessor] = []
        span_processors.append(BatchSpanProcessor(self._local_exporter))

        if self._api is not None and self._profile is not None and self.trace_backend != "local":
            org_key = self._profile.org_key
            span_processors.append(
                BatchSpanProcessor(
                    RemovePendingSpansExporter(
                        CustomOTLPSpanExporter(
                            endpoint=urljoin(self.server, f"/api/v1/org/{org_key}/otel/traces"),
                            headers={"X-Api-Key": self.api_key},
                            timeout=30,  # 30s (default 10s causes span loss on slow networks)
                            compression=Compression.Gzip,
                            session=create_platform_http_session(),
                        ),
                    ),
                ),
            )

        console_opt: logfire.ConsoleOptions | t.Literal[False] | None
        if self.console is True:
            console_opt = logfire.ConsoleOptions()
        elif self.console is False:
            console_opt = False
        else:
            console_opt = self.console

        self._logfire = logfire.configure(
            send_to_logfire=False,
            console=console_opt,
            additional_span_processors=span_processors or None,
            scrubbing=False,
        )

        self._initialized = True
        return self

    def _get_storage_credentials(self) -> t.Any:
        """Get storage credentials from the API."""
        if self._profile is None:
            raise RuntimeError("Profile not configured")
        return self.api.get_storage_access(
            self._profile.org_key,
            self._profile.workspace_key,
        )

    def _setup_trace_infrastructure(
        self,
        *,
        root_id: str | None = None,
    ) -> str:
        """
        Set up trace infrastructure (exporters, config) without creating a span.

        This is called internally when a top-level span (agent/evaluation/study)
        needs to be created and no trace context exists yet.

        Args:
            root_id: The root ID for grouping spans. If not provided, generates one.

        Returns:
            The root_id used for this trace session.
        """
        if not self._initialized:
            self.configure()

        root_id = root_id or str(uuid.uuid4().hex)
        trace_config = TraceExportConfig(
            storage=self.storage,
            run_id=root_id,  # Still called run_id in config for file routing
        )
        self._trace_config = trace_config

        return root_id

    def get_current_run(self) -> TaskSpan[t.Any] | None:
        """Get the current task span (backwards compatibility alias)."""
        return current_task_span.get()

    def get_current_task(self) -> TaskSpan[t.Any] | None:
        """Get the current task span."""
        return current_task_span.get()

    def _resolve_trace_project(self, project: str | uuid.UUID | None = None) -> str:
        """
        Resolve the project identifier to stamp onto root spans.

        Remote analytics APIs filter traces by project UUID, not project key.
        When a configured session is available, prefer the resolved project ID.
        Fall back to an explicit UUID, then the configured key for local-only use.
        """
        if isinstance(project, uuid.UUID):
            return str(project)

        active_project_key = self._profile.project if self._profile else None
        active_project_id = self._profile.project_id if self._profile else None

        if project is None:
            if active_project_id is not None:
                return str(active_project_id)
            return str(self.project) if self.project else "default"

        if active_project_id is not None:
            if project == str(active_project_id):
                return str(active_project_id)
            if active_project_key is not None and project == active_project_key:
                return str(active_project_id)

        if self._api is not None and self._profile is not None and isinstance(project, str):
            try:
                # Use configured org/workspace if available, otherwise fall back to profile
                org_key = str(self.organization) if self.organization else self._profile.org_key
                workspace_key = (
                    str(self.workspace) if self.workspace else self._profile.workspace_key
                )
                resolved_project = self._api.get_project(
                    org_key,
                    workspace_key,
                    project,
                )
            except RuntimeError:
                pass
            else:
                return str(resolved_project.id)

        return project

    def get_tracer(self, *, is_span_tracer: bool = True) -> Tracer:
        """
        Get an OpenTelemetry Tracer instance.

        Args:
            is_span_tracer: Whether the tracer is for creating spans.

        Returns:
            An OpenTelemetry Tracer.
        """
        return self._logfire._tracer_provider.get_tracer(
            self.otel_scope,
            self._version,
            is_span_tracer=is_span_tracer,
        )

    @handle_internal_errors()
    def shutdown(self) -> None:
        """
        Shutdown any associate OpenTelemetry components and flush any pending spans.

        It is not required to call this method, as the SDK will automatically
        flush and shutdown when the process exits.

        However, if you want to ensure that all spans are flushed before
        exiting, you can call this method manually.
        """
        if not self._initialized:
            return

        self._logfire.shutdown()

    def login(
        self,
        server: str,
        api_key: str,
        organization: str | uuid.UUID,
        *,
        workspace: str | uuid.UUID | None = None,
        project: str | uuid.UUID | None = None,
        cache: Path | str | None = None,
        set_default_workspace: bool = True,
        set_default_project: bool = True,
    ) -> Organization:
        """
        Login to a Dreadnode server and save credentials to profile.

        Authenticates with the server, resolves the organization, and saves
        the profile to ~/.dreadnode/config.yaml for future use.

        Args:
            server: The Dreadnode server URL.
            api_key: The Dreadnode API key.
            organization: Organization key or ID to login to.
            workspace: Default workspace to use.
            project: Default project to use.
            cache: Local cache directory (default: ~/.dreadnode).
            set_default_workspace: Save workspace as default in profile.
            set_default_project: Save project as default in profile.

        Returns:
            The resolved Organization.

        Raises:
            RuntimeError: If authentication fails or organization not found.
        """
        cache_path = Path(cache) if cache else Path.home() / ".dreadnode"

        # Create API client and authenticate
        api = ApiClient(server, api_key=api_key)
        user = api.get_user()

        # Get organization by key/id
        org = api.get_organization(str(organization))

        # Resolve workspace - use specified or find default
        resolved_workspace: str | None = None
        if workspace:
            ws = api.get_workspace(org.key, str(workspace))
            if ws:
                resolved_workspace = ws.key
        else:
            # Auto-select default workspace if none specified
            workspaces = api.list_workspaces(org.key)
            if workspaces:
                # Prefer default workspace, otherwise use first one
                for ws in workspaces:
                    if getattr(ws, "is_default", False):
                        resolved_workspace = ws.key
                        break
                if not resolved_workspace:
                    resolved_workspace = workspaces[0].key

        # Resolve project if specified
        resolved_project: str | None = None
        if project and resolved_workspace:
            proj = api.get_project(org.key, resolved_workspace, str(project))
            if proj:
                resolved_project = proj.key
        elif resolved_workspace and set_default_project:
            resolved_project = api.get_default_project_key(org.key, resolved_workspace)

        # Use username as the user_key for storage paths
        user_key = user.username
        if not user_key:
            raise RuntimeError("User has no username set. Please set a username first.")

        # Create and save profile
        profile = Profile(
            url=server,
            user_key=user_key,
            email=user.email_address,
            username=user.username,
            api_key=api_key,
            default_organization=org.key,
            default_workspace=resolved_workspace if set_default_workspace else None,
            default_project=resolved_project if set_default_project else None,
        )

        # Save profile to user config
        user_config = UserConfig.read(cache_path / "config.yaml")
        user_config.servers[user_key] = profile
        user_config.active = user_key
        user_config.write(cache_path / "config.yaml")

        # Configure the SDK with this organization
        self.configure(
            server=server,
            api_key=api_key,
            organization=org.key,
            workspace=resolved_workspace,
            project=resolved_project,
            cache=cache_path,
        )

        return org

    def list_workspaces(self, org: str | None = None) -> list[Workspace]:
        """
        List workspaces the user has access to.

        Args:
            org: Organization key. Uses configured org if not provided.

        Returns:
            List of workspaces.
        """
        if self._api is None or self._profile is None:
            raise RuntimeError("Call configure() first")
        org = org or self._profile.org_key
        return self._api.list_workspaces(org)

    def list_projects(
        self,
        org: str | None = None,
        workspace: str | None = None,
    ) -> list[Project]:
        """
        List projects in a workspace.

        Args:
            org: Organization key. Uses configured org if not provided.
            workspace: Workspace key. Uses configured workspace if not provided.

        Returns:
            List of projects.
        """
        if self._api is None or self._profile is None:
            raise RuntimeError("Call configure() first")
        org = org or self._profile.org_key
        workspace = workspace or self._profile.workspace_key
        return self._api.list_projects(org, workspace)

    def list_agents(
        self,
        org: str | None = None,
    ) -> list[PackageInfo]:
        """
        List agents in a workspace.

        Args:
            org: Organization key. Uses configured org if not provided.

        Returns:
            List of agent PackageInfo.
        """
        if self._api is None or self._profile is None:
            raise RuntimeError("Call configure() first")
        org = org or self._profile.org_key
        return self._api.list_agents(org)  # ty: ignore[unresolved-attribute]

    def span(
        self,
        name: str,
        *,
        tags: t.Sequence[str] | None = None,
        attributes: AnyDict | None = None,
    ) -> Span:
        """
        Create a new OpenTelemety span.

        Spans are more lightweight than tasks, but still let you track
        work being performed and view it in the UI. You cannot
        log parameters, inputs, or outputs to spans.

        Example:
            ```
            with dreadnode.span("my_span") as span:
                # do some work here
                pass
            ```

        Args:
            name: The name of the span.
            tags: A list of tags to attach to the span.
            attributes: A dictionary of attributes to attach to the span.

        Returns:
            A Span object.
        """
        return Span(
            name=name,
            attributes=attributes,
            tracer=self.get_tracer(),
            tags=tags,
        )

    def task(
        self,
        func: t.Callable[P, t.Awaitable[R]] | t.Callable[P, R] | None = None,
        /,
        *,
        scorers: ScorersLike[t.Any] | None = None,
        name: str | None = None,
        label: str | None = None,
        log_inputs: t.Sequence[str] | bool | Inherited = INHERITED,
        log_output: bool | Inherited = INHERITED,
        log_execution_metrics: bool = False,
        tags: t.Sequence[str] | None = None,
        attributes: AnyDict | None = None,
        entrypoint: bool = False,
    ) -> TaskDecorator | ScoredTaskDecorator[R] | Task[P, R]:
        """Create a new task from a function. See `task()` for details."""
        from dreadnode.core.task import task as task_factory

        return task_factory(  # ty: ignore[no-matching-overload]
            func,
            tracer=self.get_tracer(),
            scorers=scorers,
            name=name,
            label=label,
            log_inputs=log_inputs,
            log_output=log_output,
            log_execution_metrics=log_execution_metrics,
            tags=tags,
            attributes=attributes,
            entrypoint=entrypoint,
        )

    def task_span(
        self,
        name: str,
        *,
        type: SpanType = "task",
        label: str | None = None,
        tags: t.Sequence[str] | None = None,
        attributes: AnyDict | None = None,
        _tracer: Tracer | None = None,
    ) -> TaskSpan[t.Any]:
        """
        Create a task span without an explicit associated function.

        This is useful for creating tasks on the fly without having to
        define a function.

        Example:
            ```
            async with dreadnode.task_span("my_task") as task:
                # do some work here
                pass
            ```
        Args:
            name: The name of the task.
            type: The type of span (task, evaluation, etc.).
            label: The label of the task - useful for filtering in the UI.
            tags: A list of tags to attach to the task span.
            attributes: A dictionary of attributes to attach to the task span.

        Returns:
            A TaskSpan object.
        """
        parent_task = current_task_span.get()
        label = clean_str(label or name)

        return TaskSpan(
            name=name,
            tracer=_tracer or self.get_tracer(),
            storage=self._storage,
            project=parent_task.project_id if parent_task else self._resolve_trace_project(),
            type=type,
            label=label,
            attributes=attributes,
            tags=tags,
        )

    def scorer(
        self,
        func: t.Callable[..., t.Any] | None = None,
        *,
        name: str | None = None,
        assert_: bool = False,
        attributes: AnyDict | None = None,
    ) -> t.Any:
        """Create a scorer decorator. See `scorer()` for details."""
        from dreadnode.core.scorer import scorer as scorer_factory

        return scorer_factory(func, name=name, assert_=assert_, attributes=attributes)

    def evaluation(
        self,
        func: t.Callable[..., t.Any] | None = None,
        /,
        *,
        dataset: t.Any | None = None,
        dataset_file: str | None = None,
        name: str | None = None,
        description: str = "",
        tags: list[str] | None = None,
        concurrency: int = 1,
        iterations: int = 1,
        max_errors: int | None = None,
        max_consecutive_errors: int = 10,
        dataset_input_mapping: list[str] | dict[str, str] | None = None,
        parameters: dict[str, list[t.Any]] | None = None,
        scorers: ScorersLike[t.Any] | None = None,
        assert_scores: list[str] | t.Literal[True] | None = None,
    ) -> t.Any:
        """Decorator to create an Evaluation from a function. See `evaluation()` for details."""
        from dreadnode.evaluations import evaluation as evaluation_factory

        return evaluation_factory(
            func,
            dataset=dataset,
            dataset_file=dataset_file,
            name=name,
            description=description,
            tags=tags,
            concurrency=concurrency,
            iterations=iterations,
            max_errors=max_errors,
            max_consecutive_errors=max_consecutive_errors,
            dataset_input_mapping=dataset_input_mapping,
            parameters=parameters,
            scorers=scorers,
            assert_scores=assert_scores,
        )

    def study(
        self,
        func: t.Callable[..., t.Any] | None = None,
        /,
        *,
        name: str | None = None,
        search_strategy: t.Any | None = None,
        dataset: t.Any | None = None,
        dataset_file: str | None = None,
        objectives: ScorersLike[t.Any] | None = None,
        directions: list[Direction] | None = None,
        constraints: ScorersLike[t.Any] | None = None,
        max_trials: int = 100,
        concurrency: int = 1,
        stop_conditions: list[t.Any] | None = None,
    ) -> t.Any:
        """Decorator to create a Study from a task factory. See `study()` for details."""
        from dreadnode.optimization import study as study_factory

        return study_factory(  # ty: ignore[call-non-callable]
            func,
            name=name,
            search_strategy=search_strategy,
            dataset=dataset,
            dataset_file=dataset_file,
            objectives=objectives,
            directions=directions,
            constraints=constraints,
            max_trials=max_trials,
            concurrency=concurrency,
            stop_conditions=stop_conditions,
        )

    def optimize_anything(
        self,
        *,
        evaluator: t.Callable[..., t.Any] | None = None,
        seed_candidate: str | dict[str, str] | None = None,
        dataset: list[t.Any] | None = None,
        trainset: list[t.Any] | None = None,
        valset: list[t.Any] | None = None,
        objective: str | None = None,
        background: str | None = None,
        name: str | None = None,
        description: str = "",
        tags: list[str] | None = None,
        config: OptimizationConfig | None = None,
        backend: str | OptimizationBackend[t.Any] = "gepa",
        adapter: OptimizationAdapter[t.Any] | None = None,
    ) -> t.Any:
        """Create an optimize_anything executor. See `optimize_anything()` for details."""
        from dreadnode.optimization import optimize_anything as optimize_anything_factory

        return optimize_anything_factory(
            evaluator=evaluator,
            seed_candidate=seed_candidate,
            dataset=dataset,
            trainset=trainset,
            valset=valset,
            objective=objective,
            background=background,
            name=name,
            description=description,
            tags=tags,
            config=config,
            backend=backend,
            adapter=adapter,
        )

    def train(
        self,
        config: str | Path | dict[str, t.Any],
        *,
        prompts: list[str] | None = None,
        reward_fn: t.Callable[[list[str], list[str]], list[float]] | None = None,
        scorers: ScorersLike[t.Any] | None = None,
    ) -> t.Any:
        """
        Train a model using a YAML configuration file.

        This is the main entry point for training LLMs with GRPO, SFT, DPO, PPO,
        or other training methods supported by the Ray training framework.

        Example YAML config (grpo.yaml):
            ```yaml
            trainer: grpo
            model_name: Qwen/Qwen2.5-1.5B-Instruct
            max_steps: 100
            num_prompts_per_step: 4
            num_generations_per_prompt: 4
            learning_rate: 1e-6
            temperature: 0.7

            # Dataset - supports dreadnode datasets, huggingface, jsonl, or inline
            dataset:
              type: dreadnode  # or huggingface, jsonl, list
              name: my-dataset  # dreadnode dataset name
              prompt_field: question

            # Reward - supports dreadnode scorers or built-in types
            reward:
              type: scorer  # Use dreadnode scorer
              # or type: correctness, length, contains
            ```

        Usage:
            ```python
            import dreadnode as dn

            # Train from YAML config
            result = dn.train("config/grpo.yaml")

            # Train with dreadnode dataset and scorers
            @dn.scorer
            def correctness(completion: str) -> float:
                return 1.0 if "answer" in completion else 0.0

            result = dn.train(
                {"trainer": "grpo", "model_name": "..."},
                prompts=dn.load("my-dataset").to_prompts("question"),
                scorers=[correctness],
            )

            # Train with custom prompts and reward function
            result = dn.train(
                "config/grpo.yaml",
                prompts=["What is 2+2?", "What is 3*4?"],
                reward_fn=my_reward_fn,
            )
            ```

        Args:
            config: Path to YAML config file, or dict with config values.
            prompts: Optional list of prompts (overrides dataset in config).
            reward_fn: Optional reward function (overrides reward/scorers).
            scorers: Optional dreadnode Scorers to use as reward (converted to reward_fn).

        Returns:
            Training result (trainer-specific).
        """
        import yaml

        from dreadnode.core.scorer import Scorer
        from dreadnode.training import (
            _build_reward_fn,
            _load_training_dataset,
            _scorers_to_reward_fn,
            train_dpo,
            train_grpo,
            train_ppo,
            train_sft,
        )

        # Load config
        if isinstance(config, (str, Path)):
            config_path = Path(config)
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")

            with config_path.open() as f:
                config_dict = yaml.safe_load(f)
        else:
            config_dict = dict(config)  # Copy to avoid mutating input

        # Determine trainer type
        trainer_type = config_dict.pop("trainer", "grpo").lower()

        # Load prompts from dataset if not provided
        if prompts is None and "dataset" in config_dict:
            prompts = _load_training_dataset(config_dict.pop("dataset"))

        if prompts is None:
            raise ValueError("Either 'prompts' argument or 'dataset' in config is required")

        # Build reward function from scorers if provided
        if scorers is not None:
            fitted_scorers = Scorer.fit_many(scorers)
            reward_fn = _scorers_to_reward_fn(fitted_scorers)

        # Build reward function from config if not provided
        if reward_fn is None and "reward" in config_dict:
            reward_fn = _build_reward_fn(config_dict.pop("reward"), prompts)

        # For SFT, reward is optional
        if reward_fn is None and trainer_type not in ("sft",):
            raise ValueError(
                "Either 'reward_fn', 'scorers', or 'reward' in config is required for "
                f"{trainer_type} training"
            )

        # Create and run trainer
        if trainer_type == "grpo":
            assert reward_fn is not None  # Validated above
            return train_grpo(config_dict, prompts, reward_fn)
        if trainer_type == "sft":
            return train_sft(config_dict, prompts)
        if trainer_type == "dpo":
            return train_dpo(config_dict, prompts)
        if trainer_type == "ppo":
            assert reward_fn is not None  # Validated above
            return train_ppo(config_dict, prompts, reward_fn)
        raise ValueError(f"Unknown trainer type: {trainer_type}")

    def run(
        self,
        name: str | None = None,
        *,
        tags: t.Sequence[str] | None = None,
        params: AnyDict | None = None,
        project: str | None = None,
        name_prefix: str | None = None,
        attributes: AnyDict | None = None,
        _tracer: Tracer | None = None,
    ) -> TaskSpan[t.Any]:
        """
        Create a new top-level task span.

        This sets up trace infrastructure and creates a task span that can
        contain agents, evaluations, studies, or other work.

        Example:
            ```
            with dreadnode.run("my_experiment"):
                # Run an agent, evaluation, or other work
                await agent.run("do something")
            ```

        Args:
            name: The name of the task. If not provided, a random name will be generated.
            tags: A list of tags to attach to the task.
            params: A dictionary of parameters to attach to the task.
            project: The project name to associate with. If not provided,
                the project passed to `configure()` will be used, or
                a default project will be used.
            attributes: Additional attributes to attach to the span.

        Returns:
            A TaskSpan object that can be used as a context manager.
        """
        name_prefix = clean_str(name_prefix or coolname.generate_slug(2), replace_with="-")
        name = name or f"{name_prefix}-{random.randint(100, 999)}"  # nosec

        # Resolve project to string
        resolved_project = self._resolve_trace_project(project)

        # Set up trace infrastructure
        task_id = self._setup_trace_infrastructure()

        return TaskSpan(
            name=name,
            tracer=_tracer or self.get_tracer(),
            storage=self.storage,
            project=resolved_project,
            task_id=task_id,
            type="task",  # Just a task, not a special "run" type
            params=params,
            attributes=attributes,
            tags=tags,
        )

    @contextlib.contextmanager
    def task_and_run(
        self,
        name: str,
        *,
        task_name: str | None = None,
        task_type: SpanType = "task",
        project: str | None = None,
        tags: t.Sequence[str] | None = None,
        params: AnyDict | None = None,
        inputs: AnyDict | None = None,
        label: str | None = None,
        _tracer: Tracer | None = None,
    ) -> t.Iterator[TaskSpan[t.Any]]:
        """
        Create a task span, setting up trace infrastructure if needed.

        If no trace context exists, this sets up exporters and creates the
        span as a top-level span. The span type (evaluation, study, agent, etc.)
        becomes the root of the trace.

        Args:
            name: Name for the task span.
            task_name: Optional separate name for the task span. If not provided, uses name.
            task_type: The type of span to create (task, evaluation, study, agent, etc.).
            project: Project for trace storage.
            tags: Tags to attach to the span.
            params: Parameters to log.
            inputs: Inputs to log.
            label: Display label for the span.
        """
        needs_infrastructure = current_task_span.get() is None

        # Set up trace infrastructure if this is a top-level span
        if needs_infrastructure:
            # Resolve project
            self._resolve_trace_project(project)
            self._setup_trace_infrastructure()

        with self.task_span(
            task_name or name,
            type=task_type,
            label=label,
            tags=tags,
            _tracer=_tracer,
        ) as task_span:
            # Log inputs and params
            self.log_inputs(**(inputs or {}))
            self.log_params(**(params or {}))
            yield task_span

    def get_task_context(self) -> TaskContext:
        """
        Capture the current task context for transfer to another host, thread, or process.

        Use `continue_task()` to continue the task anywhere else.

        Returns:
            TaskContext containing task state and trace propagation headers.

        Raises:
            RuntimeError: If called outside of an active task.
        """
        if (task := current_task_span.get()) is None:
            raise RuntimeError("get_task_context() must be called within a task")

        trace_context: dict[str, str] = {}
        propagate.inject(trace_context)

        return {
            "task_id": task.task_id,
            "task_name": task.name,
            "project": task.project_id,
            "trace_context": trace_context,
        }

    def continue_task(self, task_context: TaskContext) -> TaskSpan[t.Any]:
        """
        Continue a task from captured context on a remote host.

        Args:
            task_context: The TaskContext captured from get_task_context().

        Returns:
            A TaskSpan object that can be used as a context manager.
        """
        if not self._initialized:
            self.configure()

        return TaskSpan.from_context(
            context=task_context,
            tracer=self.get_tracer(),
            storage=self.storage,
        )

    def tag(self, *tag: str) -> None:
        """
        Add one or many tags to the current span.

        Example:
            ```
            with dreadnode.run("my_run"):
                dreadnode.tag("my_tag")
            ```

        Args:
            tag: The tag(s) to attach.
        """
        task = current_task_span.get()
        if task is None:
            warn_at_user_stacklevel(
                "tag() was called outside of a task or run.",
                category=DreadnodeUsageWarning,
            )
            return

        task.add_tags(tag)

    def load_package(
        self,
        uri: str | Path | None = None,
        type: PackageType | None = None,
    ) -> t.Any:
        """
        Load a package (dataset, model, or agent) from the server.

        Downloads and installs the package if not already installed,
        then loads it via entry points. Artifacts are fetched from
        CAS on demand.

        Args:
            uri: Package URI (e.g., "dataset://org/name", "model://org/name").
            type: Package type hint if not specified in URI.

        Returns:
            The loaded package object (Dataset, Model, or Agent).
        """
        return load_package_util(uri, type=type, storage=self.storage, profile=self._profile)  # ty: ignore[no-matching-overload]

    def task_env(
        self,
        task_ref: str,
        *,
        inputs: dict[str, t.Any] | None = None,
        secret_ids: list[str] | None = None,
        project_id: str | None = None,
        timeout_sec: int | None = None,
    ) -> TaskEnvironment:
        """Construct a ``TaskEnvironment`` bound to this profile's org/workspace.

        The environment is not provisioned until ``setup()`` (or ``async with``)
        is called. Pulls ``api_client``/``organization``/``workspace`` from the
        active profile.

        Example::

            import dreadnode as dn

            async with dn.task_env("acme/sqli@1.0.0", inputs={"host": "x"}) as env:
                await env.execute("curl -sS $web_url/login")
        """
        from dreadnode.core.environment import TaskEnvironment

        if self.organization is None or self.workspace is None:
            raise RuntimeError(
                "No active organization/workspace — call dreadnode.configure() first."
            )
        return TaskEnvironment(
            api_client=self.api,
            org=str(self.organization),
            workspace=str(self.workspace),
            task_ref=task_ref,
            project_id=project_id,
            inputs=inputs,
            secret_ids=secret_ids,
            timeout_sec=timeout_sec,
        )

    def load_dataset(
        self,
        path: str | Path,
        config: str | None = None,
        *,
        dataset_name: str | None = None,
        split: str | None = None,
        format: t.Literal["parquet", "arrow", "feather"] = "parquet",
        version: str | None = None,
        **kwargs: t.Any,
    ) -> t.Any:
        """
        Load a dataset from HuggingFace Hub or a local dataset source directory.

        Args:
            path: HuggingFace dataset path (e.g., "squad", "imdb", "glue") or a
                local directory containing dataset.yaml.
            config: Dataset configuration name (e.g., "cola" for glue dataset).
            dataset_name: Name to store the dataset as locally. Defaults to the path.
            split: Dataset split to load (e.g., "train", "test", "train[:100]").
            format: Storage format (parquet, arrow, feather).
            version: Version string for the stored dataset.
            **kwargs: Additional arguments passed to HuggingFace's load_dataset.

        Returns:
            LocalDataset instance with the loaded data.

        Example:
            >>> import dreadnode as dn
            >>> dn.configure(...)
            >>> ds = dn.load_dataset("glue", "cola", split="train[:100]")
        """
        from dreadnode.datasets.local import load_dataset as local_load_dataset

        return local_load_dataset(
            path,
            dataset_name=dataset_name,
            storage=self.storage,
            split=split,
            format=format,
            version=version,
            **({"name": config} if config else {}),
            **kwargs,
        )

    def load_model(
        self,
        path: str | Path,
        *,
        model_name: str | None = None,
        task: str | None = None,
        format: t.Literal["safetensors", "pytorch"] = "safetensors",
        version: str | None = None,
        **kwargs: t.Any,
    ) -> t.Any:
        """
        Load a model from HuggingFace Hub or a local model source directory.

        Args:
            path: HuggingFace model path (e.g., "bert-base-uncased", "gpt2") or a
                local directory containing model.yaml.
            model_name: Name to store the model as locally. Defaults to the path.
            task: Task type for the model (e.g., "classification", "generation").
            format: Storage format (safetensors or pytorch).
            version: Version string for the stored model.
            **kwargs: Additional arguments passed to from_pretrained.

        Returns:
            LocalModel instance with the loaded model.

        Example:
            >>> import dreadnode as dn
            >>> dn.configure(...)
            >>> model = dn.load_model("bert-base-uncased", task="classification")
        """
        from dreadnode.models.local import load_model as local_load_model

        return local_load_model(
            path,
            model_name=model_name,
            storage=self.storage,
            task=task,
            format=format,
            version=version,
            **kwargs,
        )

    def load_capability(
        self,
        capability: str | Path,
    ) -> Capability:
        """
        Load a capability from an explicit path or from the configured capability search paths.

        Returns a high-level ``Capability`` object that exposes the serialized capability
        manifest plus resolved agents, tools, skills, and MCP server definitions.

        Args:
            capability: Capability directory path or capability name.

        Returns:
            Capability ready to attach to an agent or server runtime.

        Raises:
            FileNotFoundError: If no capability with the requested name can be found.
        """
        from dreadnode.capabilities import Capability

        return Capability(
            capability,
            cwd=Path.cwd(),
            storage=self.storage,
        )

    def build_package(
        self,
        path: str | Path,
    ) -> BuildResult:
        """
        Build a local repository into an OCI image.

        Args:
            path: Path to a dataset, model, or environment package project.

        Returns:
            BuildResult with success status and OCI image.
        """
        return Package(path=Path(path)).build()

    def push_package(
        self,
        path: str | Path,
        *,
        skip_upload: bool = False,
    ) -> PushResult:
        """
        Build and push a local package to the Dreadnode OCI Registry.

        Handles artifact upload to CAS (for datasets/models) and OCI image
        push automatically.

        Args:
            path: Path to a dataset, model, or environment package project.
            skip_upload: Skip uploading to remote (local only).

        Returns:
            PushResult with status and details.
        """
        import warnings

        is_local_mode = self.server == "local" or self._profile is None
        if is_local_mode and not skip_upload:
            warnings.warn(
                "No remote credentials configured. Artifacts will be stored locally only. "
                "Use dn.configure() with server credentials to enable remote upload.",
                stacklevel=2,
            )
            skip_upload = True

        # Package.push() now handles the full flow: CAS upload + OCI build + OCI push
        return Package(path=Path(path)).push(storage=self.storage, skip_upload=skip_upload)

    def push_capability(
        self,
        capability: str | Path,
        *,
        name: str | None = None,
        skip_upload: bool = False,
        force: bool = False,
        publish: bool = False,
    ) -> CapabilityPushResult:
        """
        Build and push a capability directory to the OCI registry.

        Before pushing, compares the local build SHA-256 against the remote.
        If the version already exists with the same content, the push is skipped.
        If the version exists with different content, an error is raised unless
        ``force=True``.

        Args:
            capability: Capability directory path or resolvable local capability name.
            name: Optional OCI repository name override. Bare names are prefixed with
                the active organization when available.
            skip_upload: Skip uploading to remote and only validate/build locally.
            force: Push even if the version already exists with different content.
            publish: Ensure the capability is public after upload or skip.

        Returns:
            Push result with status and details.
        """
        import warnings

        from dreadnode.packaging.oci import build_capability

        loaded = self.load_capability(capability)

        resolved_name = name or loaded.name
        if "/" not in resolved_name and self._profile is not None:
            resolved_name = f"{self._profile.org_key}/{resolved_name}"
        target_org = self._profile.org_key if self._profile else ""
        target_name = loaded.name
        if "/" in resolved_name:
            target_org, target_name = resolved_name.split("/", 1)
        elif resolved_name:
            target_name = resolved_name

        is_local_mode = self.server == "local" or self._profile is None
        if is_local_mode and not skip_upload:
            warnings.warn(
                "No remote credentials configured. Capability will be built locally only. "
                "Use dn.configure() with server credentials to enable remote upload.",
                stacklevel=2,
            )
            skip_upload = True

        image = build_capability(loaded.path, name=resolved_name)

        if skip_upload:
            return CapabilityPushResult(
                name=resolved_name,
                version=loaded.version,
                status="built",
            )

        # Extract local layer SHA for comparison
        if not image.layers:
            raise ValueError("Capability OCI image has no layers")
        local_sha = image.layers[0].digest.split(":", 1)[-1]

        # Check remote state
        remote_sha = self._get_remote_capability_sha(target_org, target_name, loaded.version)

        if remote_sha and not force:
            if remote_sha == local_sha:
                if publish and self._profile:
                    self.set_capability_visibility(target_org, target_name, is_public=True)
                return CapabilityPushResult(
                    name=resolved_name,
                    version=loaded.version,
                    status="up_to_date",
                    digest=f"sha256:{local_sha}",
                )
            raise ValueError(
                f"{target_name}@{loaded.version} already exists with different content. "
                "Bump the version in capability.yaml or use --force to overwrite."
            )

        push_result = self.storage.oci_client().push(resolved_name, loaded.version, image)
        if not push_result.success:
            msg = "; ".join(push_result.errors) or "OCI push failed"
            raise RuntimeError(msg)

        if publish and self._profile:
            self.set_capability_visibility(target_org, target_name, is_public=True)

        return CapabilityPushResult(
            name=resolved_name,
            version=loaded.version,
            status="pushed",
            digest=push_result.manifest_digest,
        )

    def sync_capabilities(
        self,
        directory: str | Path,
        *,
        force: bool = False,
        publish: bool = False,
        on_progress: t.Callable[[str, str, str | None], None] | None = None,
    ) -> CapabilitySyncResult:
        """Sync capabilities from a directory to the platform.

        Discovers all capabilities (directories containing ``capability.yaml``),
        compares each against the latest remote version by SHA-256, and pushes
        only those that have changed.  Optionally publishes them to the public
        catalog.

        To push a single capability, use :meth:`push_capability` instead.

        Args:
            directory: Root directory containing capability subdirectories.
            force: Upload even when the remote SHA matches.
            publish: Ensure ``is_public=True`` after upload or skip.

        Returns:
            :class:`CapabilitySyncResult` with uploaded/skipped/failed details.
        """
        from dreadnode.packaging.oci import build_capability

        if not self.can_sync:
            raise RuntimeError(
                "No remote credentials configured. Use dn.configure() with server and API key."
            )

        root = Path(directory).resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"Capabilities directory not found: {root}")

        org = self.profile.org_key

        cap_dirs = sorted(d.parent for d in root.rglob("capability.yaml") if d.is_file())

        result = CapabilitySyncResult()
        oci_client = self.storage.oci_client()

        for cap_dir in cap_dirs:
            dir_name = cap_dir.name
            try:
                loaded = self.load_capability(cap_dir)
                cap_name = loaded.name
                resolved_name = f"{org}/{cap_name}"
                version = loaded.version

                image = build_capability(cap_dir, name=resolved_name)

                # Extract local layer SHA
                if not image.layers:
                    raise ValueError("Capability OCI image has no layers")  # noqa: TRY301 - simple validation failure inside broader capability publish flow
                local_sha = image.layers[0].digest.split(":", 1)[-1]

                # Compare with remote
                remote_sha = self._get_remote_capability_sha(org, cap_name, version)
                if not force and remote_sha and remote_sha == local_sha:
                    if publish:
                        self.set_capability_visibility(org, cap_name, is_public=True)
                    result.skipped.append(cap_name)
                    if on_progress:
                        on_progress(cap_name, "skipped", None)
                    continue

                push_result = oci_client.push(resolved_name, version, image)
                if not push_result.success:
                    msg = "; ".join(push_result.errors) or "OCI push failed"
                    result.failed.append((cap_name, msg))
                    if on_progress:
                        on_progress(cap_name, "failed", msg)
                    continue

                if publish:
                    self.set_capability_visibility(org, cap_name, is_public=True)

                result.uploaded.append(cap_name)
                if on_progress:
                    on_progress(cap_name, "uploaded", None)

            except Exception as exc:
                result.failed.append((dir_name, str(exc)))
                if on_progress:
                    on_progress(dir_name, "failed", str(exc))

        return result

    def _get_remote_capability_sha(self, org: str, name: str, version: str) -> str | None:
        """Return the artifact SHA-256 for a specific remote version, or None."""
        try:
            detail = self.api.get_capability(org, name, version)
        except RuntimeError:
            return None

        sha = detail.get("artifact_sha256")
        return str(sha) if sha else None

    def _get_remote_task_sha(self, org: str, name: str, version: str) -> str | None:
        """Return the OCI layer digest for a specific remote task version, or None."""
        try:
            detail = self.api.get_task(org, name, version)
        except RuntimeError:
            return None

        digest = detail.get("oci_digest")
        if not isinstance(digest, str) or not digest:
            return None
        return digest.split(":", 1)[-1] if ":" in digest else digest

    def _resolve_target_name_parts(self, resolved_name: str, default_name: str) -> tuple[str, str]:
        """Resolve org/name from a possibly bare resolved name."""
        target_org = self._profile.org_key if self._profile else ""
        target_name = default_name
        if "/" in resolved_name:
            target_org, target_name = resolved_name.split("/", 1)
        elif resolved_name:
            target_name = resolved_name
        return target_org, target_name

    def set_task_visibility(self, org: str, name: str, *, is_public: bool) -> None:
        """Update task visibility for all versions of a task name."""
        self.api.update_task_visibility(org, name, is_public=is_public)

    def set_capability_visibility(self, org: str, name: str, *, is_public: bool) -> None:
        """Update capability visibility for all versions of a capability name."""
        self.api.update_capability_visibility(org, name, is_public=is_public)

    def set_dataset_visibility(self, org: str, name: str, *, is_public: bool) -> None:
        """Update dataset visibility for all versions of a dataset name."""
        self.api.update_dataset_visibility(org, name, is_public=is_public)

    def set_model_visibility(self, org: str, name: str, *, is_public: bool) -> None:
        """Update model visibility for all versions of a model name."""
        self.api.update_model_visibility(org, name, is_public=is_public)

    def push_dataset(
        self,
        dataset: str | Path,
        *,
        name: str | None = None,
        skip_upload: bool = False,
        publish: bool = False,
    ) -> PushResult:
        """Build and push a dataset source directory to the OCI registry."""
        import json
        import warnings

        from dreadnode.datasets.local import LocalDataset
        from dreadnode.packaging.oci import build_manifest_image

        source_dir = Path(dataset).expanduser().resolve()
        if not source_dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {source_dir}")
        if not (source_dir / "dataset.yaml").is_file():
            raise FileNotFoundError(f"No dataset.yaml found in {source_dir}")

        loaded = self.load_dataset(source_dir)
        if not isinstance(loaded, LocalDataset):
            raise TypeError("push_dataset() requires a dataset source directory")

        resolved_name = name or loaded.name
        if "/" not in resolved_name and self._profile is not None:
            resolved_name = f"{self._profile.org_key}/{resolved_name}"

        result = PushResult(
            success=False,
            package_name=resolved_name,
            package_version=loaded.version,
            package_type="datasets",
        )

        is_local_mode = self.server == "local" or self._profile is None
        if is_local_mode and not skip_upload:
            warnings.warn(
                "No remote credentials configured. Dataset will be built locally only. "
                "Use dn.configure() with server credentials to enable remote upload.",
                stacklevel=2,
            )
            skip_upload = True

        if not skip_upload:
            blobs_to_upload = {
                self.storage.blob_path(oid): oid for oid in loaded.manifest.artifacts.values()
            }
            uploaded, skipped = self.storage.upload_blobs(blobs_to_upload)
            result.blobs_uploaded += uploaded
            result.blobs_skipped += skipped

        image = build_manifest_image(
            json.loads(loaded.manifest.model_dump_json()),
            package_type="dataset",
            name=resolved_name,
            version=loaded.version,
        )

        if skip_upload:
            result.success = True
            return result

        oci_result = self.storage.oci_client().push(resolved_name, loaded.version, image)
        if not oci_result.success:
            result.errors.extend(oci_result.errors)
            return result

        result.success = True
        result.manifest_digest = oci_result.manifest_digest
        result.blobs_uploaded += oci_result.blobs_pushed
        result.blobs_skipped += oci_result.blobs_existed

        if publish and self._profile:
            target_org, target_name = self._resolve_target_name_parts(resolved_name, loaded.name)
            self.set_dataset_visibility(target_org, target_name, is_public=True)

        return result

    def push_hf_dataset(
        self,
        hf_path: str,
        *,
        config: str | None = None,
        split: str | None = "train",
        name: str | None = None,
        version: str = "0.1.0",
        summary: str | None = None,
        user_field: str | None = None,
        assistant_field: str | None = None,
        system_prompt: str | None = None,
        format: t.Literal["parquet", "jsonl"] = "parquet",
        skip_upload: bool = False,
        publish: bool = False,
    ) -> PushResult:
        """Pull a HuggingFace dataset, package it locally, and push to the org registry.

        Default format is ``parquet`` — matches the Dreadnode dataset-manifest
        default and keeps the raw HF shape intact. When ``user_field`` AND
        ``assistant_field`` are both set, a ``messages`` column is added to
        each row in the OpenAI conversation shape Tinker SFT consumes:

        .. code-block:: json

            {"messages": [
                {"role": "system",    "content": system_prompt},
                {"role": "user",      "content": row[user_field]},
                {"role": "assistant", "content": row[assistant_field]}
            ]}

        ``system_prompt`` is optional; when omitted the system turn is not
        emitted and the conversation starts at ``user``. Passing just one of
        ``user_field`` / ``assistant_field`` raises — the SFT shape needs both.

        Args:
            hf_path: HuggingFace dataset path (e.g., ``"openai/gsm8k"``).
            config: Optional HF config name (e.g., ``"main"`` for gsm8k).
            split: HF split spec (``"train"``, ``"train[:100]"`` etc).
                Pass ``None`` to load every split and concatenate them into
                a single artifact — useful when you want the whole dataset
                as one table, not just one split.
            name: Override the registry name. Defaults to ``hf_path``.
            version: Registry version string. Defaults to ``"0.1.0"``.
            summary: Optional summary for ``dataset.yaml``.
            user_field: HF row field to map to the user message.
            assistant_field: HF row field to map to the assistant message.
            system_prompt: Optional system prompt for the messages transform.
            format: Output file format. ``"parquet"`` (default) writes a
                single ``data.parquet``; ``"jsonl"`` writes line-delimited
                JSON to ``data.jsonl``. Parquet is the platform default.
            skip_upload: Build locally without pushing (for validation).
            publish: Make the dataset publicly discoverable after push.
        """
        import json
        import tempfile

        import yaml

        from dreadnode.datasets.hf import require_datasets

        require_datasets()
        import datasets as hf_datasets

        if (user_field is None) != (assistant_field is None):
            raise ValueError(
                "user_field and assistant_field must be set together for the "
                "messages transform — either both or neither"
            )
        if system_prompt is not None and user_field is None:
            raise ValueError("system_prompt requires user_field and assistant_field")

        load_kwargs: dict[str, t.Any] = {}
        if split is not None:
            load_kwargs["split"] = split
        if config is not None:
            load_kwargs["name"] = config
        hf_ds = hf_datasets.load_dataset(hf_path, **load_kwargs)
        if isinstance(hf_ds, hf_datasets.DatasetDict):
            # ``split=None`` → HF returns a mapping of every split. Flatten by
            # concatenating each split's Dataset into a single table so the
            # downstream parquet/jsonl writer sees one shape. Splits with
            # divergent schemas raise inside ``concatenate_datasets`` — we
            # surface that error rather than guessing.
            split_datasets = list(hf_ds.values())
            if not split_datasets:
                raise ValueError(f"HuggingFace returned an empty DatasetDict for {hf_path!r}")
            hf_ds = hf_datasets.concatenate_datasets(split_datasets)

        if user_field is not None and assistant_field is not None:
            _user_field = user_field
            _assistant_field = assistant_field
            _system_prompt = system_prompt

            def _add_messages(row: dict[str, t.Any]) -> dict[str, t.Any]:
                messages: list[dict[str, str]] = []
                if _system_prompt is not None:
                    messages.append({"role": "system", "content": _system_prompt})
                messages.append({"role": "user", "content": str(row[_user_field])})
                messages.append({"role": "assistant", "content": str(row[_assistant_field])})
                return {"messages": messages}

            hf_ds = hf_ds.map(_add_messages)

        # Strip any HF namespace ("openai/gsm8k" -> "gsm8k"); a slash in the
        # resolved name would defeat the org-prefix guard in push_dataset.
        dataset_name = name or hf_path.rsplit("/", 1)[-1]
        split_label = split if split is not None else "all splits"
        dataset_summary = (
            summary or f"{hf_path} ({split_label}) pulled from HuggingFace via push_hf_dataset"
        )

        with tempfile.TemporaryDirectory(prefix="dn-hf-push-") as tmp:
            tmp_dir = Path(tmp)
            (tmp_dir / "dataset.yaml").write_text(
                yaml.safe_dump(
                    {
                        "name": dataset_name,
                        "version": version,
                        "summary": dataset_summary,
                        "format": format,
                    },
                    sort_keys=False,
                )
            )
            if format == "parquet":
                hf_ds.to_parquet(str(tmp_dir / "data.parquet"))
            else:
                with (tmp_dir / "data.jsonl").open("w", encoding="utf-8") as f:
                    for row in hf_ds:
                        f.write(json.dumps(dict(row)) + "\n")

            return self.push_dataset(
                tmp_dir,
                name=name,
                skip_upload=skip_upload,
                publish=publish,
            )

    def push_model(
        self,
        model: str | Path,
        *,
        name: str | None = None,
        skip_upload: bool = False,
        publish: bool = False,
    ) -> PushResult:
        """Build and push a model source directory to the OCI registry."""
        import json
        import warnings

        from dreadnode.models.local import LocalModel
        from dreadnode.packaging.oci import build_manifest_image

        source_dir = Path(model).expanduser().resolve()
        if not source_dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {source_dir}")
        if not (source_dir / "model.yaml").is_file():
            raise FileNotFoundError(f"No model.yaml found in {source_dir}")

        loaded = self.load_model(source_dir)
        if not isinstance(loaded, LocalModel):
            raise TypeError("push_model() requires a model source directory")

        resolved_name = name or loaded.name
        if "/" not in resolved_name and self._profile is not None:
            resolved_name = f"{self._profile.org_key}/{resolved_name}"

        result = PushResult(
            success=False,
            package_name=resolved_name,
            package_version=loaded.version,
            package_type="models",
        )

        is_local_mode = self.server == "local" or self._profile is None
        if is_local_mode and not skip_upload:
            warnings.warn(
                "No remote credentials configured. Model will be built locally only. "
                "Use dn.configure() with server credentials to enable remote upload.",
                stacklevel=2,
            )
            skip_upload = True

        if not skip_upload:
            blobs_to_upload = {
                self.storage.blob_path(oid): oid for oid in loaded.manifest.artifacts.values()
            }
            uploaded, skipped = self.storage.upload_blobs(blobs_to_upload)
            result.blobs_uploaded += uploaded
            result.blobs_skipped += skipped

        image = build_manifest_image(
            json.loads(loaded.manifest.model_dump_json()),
            package_type="model",
            name=resolved_name,
            version=loaded.version,
        )

        if skip_upload:
            result.success = True
            return result

        oci_result = self.storage.oci_client().push(resolved_name, loaded.version, image)
        if not oci_result.success:
            result.errors.extend(oci_result.errors)
            return result

        result.success = True
        result.manifest_digest = oci_result.manifest_digest
        result.blobs_uploaded += oci_result.blobs_pushed
        result.blobs_skipped += oci_result.blobs_existed

        if publish and self._profile:
            target_org, target_name = self._resolve_target_name_parts(resolved_name, loaded.name)
            self.set_model_visibility(target_org, target_name, is_public=True)

        return result

    def push_environment(
        self,
        environment: str | Path,
        *,
        name: str | None = None,
        skip_upload: bool = False,
        force: bool = False,
        publish: bool = False,
        validate: bool = True,
    ) -> PushResult:
        """Build and push an environment directory with task.yaml to the OCI registry.

        Before pushing, compares the local build SHA-256 against the remote.
        If the task already exists with the same content, the push is skipped
        unless ``force=True``.

        Args:
            environment: Task directory path containing task.yaml.
            name: Optional OCI repository name override. Bare names are prefixed
                with the active organization when available.
            skip_upload: Skip uploading to remote and only build locally.
            force: Push even if the remote SHA matches.
            publish: Ensure the task is public after upload or skip.

        Returns:
            Push result with success status and details.
        """
        import warnings

        from dreadnode.packaging.oci import build_environment
        from dreadnode.packaging.task_validation import (
            TaskValidationError,
            assert_task_directory_valid,
        )

        source_dir = Path(environment).expanduser().resolve()
        env_name, env_version = _load_environment_metadata(source_dir)

        resolved_name = name or env_name
        if "/" not in resolved_name and self._profile is not None:
            resolved_name = f"{self._profile.org_key}/{resolved_name}"
        target_org = self._profile.org_key if self._profile else ""
        target_name = env_name
        if "/" in resolved_name:
            target_org, target_name = resolved_name.split("/", 1)
        elif resolved_name:
            target_name = resolved_name

        result = PushResult(
            success=False,
            package_name=resolved_name,
            package_version=env_version,
            package_type="environments",
        )

        is_local_mode = self.server == "local" or self._profile is None
        if is_local_mode and not skip_upload:
            warnings.warn(
                "Environment will be built locally only. "
                "Use dn.configure() with server credentials to enable remote upload.",
                stacklevel=2,
            )
            skip_upload = True

        # Predict platform ingest: block on anything the SDK marks `error`,
        # since the API would reject the same archive at upload.
        if validate:
            try:
                assert_task_directory_valid(source_dir)
            except TaskValidationError as exc:
                result.errors.append(str(exc))
                return result

        image = build_environment(
            source_dir,
            name=resolved_name,
            version=env_version,
        )

        if skip_upload:
            result.success = True
            return result

        # SHA-256 comparison — skip no-op pushes
        if not force and image.layers:
            local_sha = image.layers[0].digest.split(":", 1)[-1]
            remote_sha = self._get_remote_task_sha(
                target_org,
                target_name,
                env_version,
            )
            if remote_sha and remote_sha == local_sha:
                if publish and self._profile:
                    self.set_task_visibility(target_org, target_name, is_public=True)
                result.success = True
                result.manifest_digest = f"sha256:{local_sha}"
                return result

        oci_result = self.storage.oci_client().push(resolved_name, env_version, image)
        if not oci_result.success:
            result.errors.extend(oci_result.errors)
            return result

        if publish and self._profile:
            self.set_task_visibility(target_org, target_name, is_public=True)

        result.success = True
        result.manifest_digest = oci_result.manifest_digest
        result.blobs_uploaded += oci_result.blobs_pushed
        result.blobs_skipped += oci_result.blobs_existed
        return result

    def sync_environments(
        self,
        directory: str | Path,
        *,
        force: bool = False,
        publish: bool = False,
        max_workers: int = 8,
        validate: bool = True,
        on_progress: t.Callable[[str, str, str | None], None] | None = None,
        on_status: t.Callable[[str], None] | None = None,
    ) -> EnvironmentSyncResult:
        """Sync task environments from a directory to the platform.

        Discovers all subdirectories containing ``task.yaml``, compares each
        against the exact remote version by OCI layer SHA-256, and pushes
        only those that have changed.

        Args:
            directory: Root directory containing task subdirectories.
            force: Upload even when the remote SHA matches.
            publish: Ensure ``is_public=True`` after upload or skip.
            max_workers: Maximum parallel build/upload threads.
            validate: Run local validation per task and fail any that the
                platform would reject at ingest (error-level issues).
            on_progress: Optional callback ``(name, status, error)`` for each task.

        Returns:
            :class:`EnvironmentSyncResult` with uploaded/skipped/failed details.
        """
        import concurrent.futures
        import threading

        from dreadnode.packaging.oci import build_environment

        if not self.can_sync:
            raise RuntimeError(
                "No remote credentials configured. Use dn.configure() with server and API key."
            )

        from dreadnode.packaging.task_validation import (
            assert_task_directory_valid,
            discover_task_directories,
        )

        _status = on_status or (lambda _msg: None)

        root = Path(directory).resolve()
        if not root.is_dir():
            raise FileNotFoundError(f"Task directory not found: {root}")

        org = self.profile.org_key

        _status("Discovering tasks...")
        task_dirs, conflicts = discover_task_directories(root)
        _status(f"Found {len(task_dirs)} task(s)")

        if conflicts and on_progress:
            for parent, nested in conflicts:
                on_progress(
                    nested.name,
                    "failed",
                    f"task nested inside another task ({parent.name})",
                )

        result = EnvironmentSyncResult(
            failed=[(nested.name, f"nested inside {parent.name}") for parent, nested in conflicts],
        )

        _status(f"Syncing with {max_workers} workers...")

        lock = threading.Lock()

        def _sync_one(task_dir: Path) -> None:
            dir_name = task_dir.name
            try:
                env_name, env_version = _load_environment_metadata(task_dir)
                resolved_name = f"{org}/{env_name}"

                # Predict ingest: a task the SDK marks `error` would 400 at
                # upload, so fail it locally (recorded below) and keep going.
                if validate:
                    assert_task_directory_valid(task_dir, root_dir=root)

                image = build_environment(task_dir, name=resolved_name, version=env_version)

                if not image.layers:
                    raise ValueError("Environment OCI image has no layers")  # noqa: TRY301
                local_sha = image.layers[0].digest.split(":", 1)[-1]

                remote_sha = (
                    None if force else self._get_remote_task_sha(org, env_name, env_version)
                )
                if not force and remote_sha and remote_sha == local_sha:
                    if publish:
                        self.set_task_visibility(org, env_name, is_public=True)
                    with lock:
                        result.skipped.append(env_name)
                    if on_progress:
                        on_progress(env_name, "skipped", None)
                    return

                # Each thread gets its own OCI client (own httpx.Client)
                oci_client = self.storage.oci_client()
                push_result = oci_client.push(resolved_name, env_version, image)
                if not push_result.success:
                    msg = "; ".join(push_result.errors) or "OCI push failed"
                    with lock:
                        result.failed.append((env_name, msg))
                    if on_progress:
                        on_progress(env_name, "failed", msg)
                    return

                if publish:
                    self.set_task_visibility(org, env_name, is_public=True)

                with lock:
                    result.uploaded.append(env_name)
                if on_progress:
                    on_progress(env_name, "uploaded", None)

            except Exception as exc:
                with lock:
                    result.failed.append((dir_name, str(exc)))
                if on_progress:
                    on_progress(dir_name, "failed", str(exc))

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            list(pool.map(_sync_one, task_dirs))

        return result

    def pull_package(
        self,
        packages: list[str],
        *,
        upgrade: bool = False,
    ) -> PullResult:
        """
        Download packages from the registry.

        Args:
            packages: Package names to install.
            upgrade: Upgrade if already installed.

        Returns:
            PullResult with status.
        """
        return Package.pull(*packages, upgrade=upgrade, _storage=self.storage)

    def change_workspace(self, workspace: str | uuid.UUID) -> Workspace:
        """
        Change the current workspace within the current organization.

        This re-resolves the workspace and updates the storage paths accordingly.
        The organization remains unchanged.

        Args:
            workspace: The workspace name, key, or uuid.UUID to switch to.

        Returns:
            The resolved Workspace object.

        Raises:
            RuntimeError: If not configured or workspace not found.
        """
        if self._profile is None or self._api is None:
            raise RuntimeError("Call configure() first")

        # Re-resolve profile with new workspace
        self._profile = self._profile.with_overrides(workspace=str(workspace))
        self._profile.validate_scope(self._api)
        self.workspace = workspace

        # Update storage with new workspace context
        self._storage = Storage(
            profile=self._profile, cache=self.cache, api=self._api, provider=self.storage_provider
        )

        ws_key = self._profile.workspace
        if ws_key is None:
            raise RuntimeError("Workspace not found after profile validation")

        # Fetch and return the full Workspace object for backward compatibility
        return self._api.get_workspace(self._profile.org_key, ws_key)

    def list_registry(
        self,
        project_type: PackageType,
        *,
        org: str | None = None,  # noqa: ARG002 — kept for public-API stability
    ) -> list[PackageInfo]:
        """
        List packages available in the registry.

        Currently lists packages from local storage. Remote registry support
        will be added when the API endpoint is available.

        Args:
            project_type: Type of package to list (datasets, models, tools, agents, environments).
            org: Organization to filter

        Returns:
            List of PackageInfo objects.
        """
        packages: list[PackageInfo] = []

        # List from local storage
        projects_dir = self.storage.projects_path / project_type
        if projects_dir.exists():
            for pkg_dir in projects_dir.iterdir():
                if pkg_dir.is_dir():
                    # Get latest version
                    versions = self.storage.list_versions(project_type, pkg_dir.name)
                    latest = versions[0] if versions else None

                    packages.append(
                        PackageInfo(
                            name=pkg_dir.name,
                            project_type=project_type,
                            version=latest,
                            is_local=True,
                        )
                    )

        # TODO(monoxgas): fan out to per-type endpoints (list_datasets /
        # list_models / etc.) to restore remote registry listing here. The
        # legacy aggregate /org/{org}/packages/{type} route was removed
        # server-side.

        return packages

    @handle_internal_errors()
    def push_update(self) -> None:
        """
        Push any pending run data to the server before run completion.

        This is useful for ensuring that the UI is up to date with the
        latest data. Data is automatically pushed periodically, but
        you can call this method to force a push.

        Example:
            ```
            with dreadnode.run("my_run"):
                dreadnode.log_params(...)
                dreadnode.log_metric(...)
                dreadnode.push_update()

                # do more work
        """
        if (run := current_task_span.get()) is None:
            warn_at_user_stacklevel(
                "push_update() was called outside of a run.",
                category=DreadnodeUsageWarning,
            )
            return

        run.push_update(force=True)  # ty: ignore[unresolved-attribute]

    @handle_internal_errors()
    def log_param(
        self,
        key: str,
        value: JsonValue,
    ) -> None:
        """
        Log a single parameter to the current run.

        Parameters are key-value pairs that are associated with the run
        and can be used to track configuration values, hyperparameters, or other
        metadata.

        Example:
            ```
            with dreadnode.run("my_run"):
                dreadnode.log_param("param_name", "param_value")
            ```

        Args:
            key: The name of the parameter.
            value: The value of the parameter.
        """
        self.log_params(**{key: value})

    @handle_internal_errors()
    def log_params(self, **params: JsonValue) -> None:
        """
        Log multiple parameters to the current run.

        Parameters are key-value pairs that are associated with the run
        and can be used to track configuration values, hyperparameters, or other
        metadata.

        Example:
            ```
            with dreadnode.run("my_run"):
                dreadnode.log_params(
                    param1="value1",
                    param2="value2"
                )
            ```

        Args:
            **params: The parameters to log. Each parameter is a key-value pair.
        """
        if (run := current_task_span.get()) is None:
            warn_at_user_stacklevel(
                "log_params() was called outside of a run.",
                category=DreadnodeUsageWarning,
            )
            return

        run.log_params(**params)

    @t.overload
    def log_metric(
        self,
        name: str,
        value: float | bool,
        *,
        step: int = 0,
        origin: t.Any | None = None,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        attributes: AnyDict | None = None,
    ) -> Metric:
        """
        Log a single metric to the current task or run.

        Metrics are some measurement or recorded value related to the task or run.
        They can be used to track performance, resource usage, or other quantitative data.

        Example:
            ```
            with dreadnode.run("my_run"):
                dreadnode.log_metric("metric_name", 42.0)
            ```

        Args:
            name: The name of the metric.
            value: The value of the metric.
            step: The step of the metric.
            origin: The origin of the metric - can be provided any object which was logged
                as an input or output anywhere in the run.
            timestamp: The timestamp of the metric - defaults to the current time.
            aggregation: The aggregation to use for the metric. Helpful when you want to let
                the library take care of translating your raw values into better representations.
                - direct: do not modify the value at all (default)
                - min: the lowest observed value reported for this metric
                - max: the highest observed value reported for this metric
                - avg: the average of all reported values for this metric
                - sum: the cumulative sum of all reported values for this metric
                - count: increment every time this metric is logged - disregard value
            attributes: A dictionary of additional attributes to attach to the metric.

        Returns:
            The logged metric object.
        """

    @t.overload
    def log_metric(
        self,
        name: str,
        value: Metric,
        *,
        origin: t.Any | None = None,
        aggregation: MetricAggMode | None = None,
    ) -> Metric:
        """
        Log a single metric to the current task or run.

        Metrics are some measurement or recorded value related to the task or run.
        They can be used to track performance, resource usage, or other quantitative data.

        Example:
            ```
            with dreadnode.run("my_run"):
                dreadnode.log_metric("metric_name", 42.0)
            ```

        Args:
            name: The name of the metric.
            value: The metric object.
            origin: The origin of the metric - can be provided any object which was logged
                as an input or output anywhere in the run.
            aggregation: The aggregation to use for the metric. Helpful when you want to let
                the library take care of translating your raw values into better representations.
                - min: always report the lowest ovbserved value for this metric
                - max: always report the highest observed value for this metric
                - avg: report the average of all values for this metric
                - sum: report a rolling sum of all values for this metric
                - count: report the number of times this metric has been logged

        Returns:
            The logged metric object.
        """

    @handle_internal_errors()
    def log_metric(
        self,
        name: str,
        value: float | bool | Metric,
        *,
        step: int = 0,
        origin: t.Any | None = None,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        attributes: AnyDict | None = None,
    ) -> Metric:
        """
        Log a single metric to the current task or run.

        Metrics are some measurement or recorded value related to the task or run.
        They can be used to track performance, resource usage, or other quantitative data.

        Examples:
            With a raw value:
            ```
            with dreadnode.run("my_run"):
                dreadnode.log_metric("accuracy", 0.95, step=10)
                dreadnode.log_metric("loss", 0.05, step=10, aggregation="min")
            ```

            With a Metric object:
            ```
            with dreadnode.run("my_run"):
                metric = Metric(0.95, step=10, timestamp=datetime.now(timezone.utc))
                dreadnode.log_metric("accuracy", metric)
            ```

        Args:
            name: The name of the metric.
            value: The value of the metric, either as a raw float/bool or a Metric object.
            step: The step of the metric.
            origin: The origin of the metric - can be provided any object which was logged
                as an input or output anywhere in the run.
            timestamp: The timestamp of the metric - defaults to the current time.
            aggregation: The aggregation to use for the metric. Helpful when you want to let
                the library take care of translating your raw values into better representations.
                - direct: do not modify the value at all (default)
                - min: the lowest observed value reported for this metric
                - max: the highest observed value reported for this metric
                - avg: the average of all reported values for this metric
                - sum: the cumulative sum of all reported values for this metric
                - count: increment every time this metric is logged - disregard value
            attributes: A dictionary of additional attributes to attach to the metric.

        Returns:
            The logged metric object.
        """
        metric = (
            value
            if isinstance(value, Metric)
            else Metric(
                float(value),
                step,
                timestamp or datetime.now(UTC),
                attributes or {},
            )
        )

        task = current_task_span.get()
        if task is None:
            warn_at_user_stacklevel(
                "log_metric() was called outside of a task or run.",
                category=DreadnodeUsageWarning,
            )
            return metric

        return task.log_metric(name, metric, origin=origin, aggregation=aggregation)

    @t.overload
    def log_metrics(
        self,
        metrics: dict[str, float | bool],
        *,
        step: int = 0,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        attributes: AnyDict | None = None,
        origin: t.Any | None = None,
    ) -> list[Metric]:
        """
        Log multiple metrics from a dictionary of name/value pairs.

        Examples:
            ```
            dreadnode.log_metrics(
                {
                    "accuracy": 0.95,
                    "loss": 0.05,
                    "f1_score": 0.92
                },
                step=10
            )
            ```

        Args:
            metrics: Dictionary of name/value pairs to log as metrics.
            step: Step value for all metrics.
            timestamp: Timestamp for all metrics.
            aggregation: Aggregation for all metrics.
            attributes: Attributes for all metrics.
            to: The target object to log metrics to. Can be "task-or-run" or "run".
                Defaults to "task-or-run". If "task-or-run", the metrics will be logged
                to the current task or run, whichever is the nearest ancestor.

        Returns:
            List of logged Metric objects.
        """

    @t.overload
    def log_metrics(
        self,
        metrics: list[MetricDict],
        *,
        step: int = 0,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        attributes: AnyDict | None = None,
        origin: t.Any | None = None,
    ) -> list[Metric]:
        """
        Log multiple metrics from a list of metric configurations.

        Example:
            ```
            dreadnode.log_metrics(
                [
                    {"name": "accuracy", "value": 0.95},
                    {"name": "loss", "value": 0.05, "aggregation": "min"}
                ],
                step=10
            )
            ```

        Args:
            metrics: List of metric configurations to log.
            step: Default step value for metrics if not supplied.
            timestamp: Default timestamp for metrics if not supplied.
            aggregation: Default aggregation for metrics if not supplied.
            attributes: Default attributes for metrics if not supplied.

        Returns:
            List of logged Metric objects.
        """

    @handle_internal_errors()
    def log_metrics(
        self,
        metrics: MetricsLike,
        *,
        step: int = 0,
        timestamp: datetime | None = None,
        aggregation: MetricAggMode | None = None,
        attributes: AnyDict | None = None,
        origin: t.Any | None = None,
    ) -> list[Metric]:
        """
        Log multiple metrics to the current task or run.

        Examples:
            Log metrics from a dictionary:
            ```
            dreadnode.log_metrics(
                {
                    "accuracy": 0.95,
                    "loss": 0.05,
                    "f1_score": 0.92
                },
                step=10
            )
            ```

            Log metrics from a list of MetricDicts:
            ```
            dreadnode.log_metrics(
                [
                    {"name": "accuracy", "value": 0.95},
                    {"name": "loss", "value": 0.05, "aggregation": "min"}
                ],
                step=10
            )
            ```

        Args:
            metrics: Either a dictionary of name/value pairs or a list of MetricDicts to log.
            step: Default step value for metrics if not supplied.
            timestamp: Default timestamp for metrics if not supplied.
            aggregation: Default aggregation for metrics if not supplied.
            attributes: Default attributes for metrics if not supplied.
            origin: The origin of the metrics - can be provided any object which was
                logged as an input or output anywhere in the run.

        Returns:
            List of logged Metric objects.
        """

        task = current_task_span.get()
        if task is None:
            warn_at_user_stacklevel(
                "log_metrics() was called outside of a task or run.",
                category=DreadnodeUsageWarning,
            )
            return []

        logged_metrics: list[Metric] = []

        # Dictionary of name/value pairs
        if isinstance(metrics, dict):
            logged_metrics = [
                task.log_metric(
                    name,
                    value,
                    step=step,
                    timestamp=timestamp,
                    aggregation=aggregation,
                    attributes=attributes,
                    origin=origin,
                )
                for name, value in metrics.items()
            ]

        # List of MetricDicts
        else:
            logged_metrics = [
                task.log_metric(
                    metric["name"],
                    metric["value"],
                    step=metric.get("step", step),
                    timestamp=metric.get("timestamp", timestamp),
                    aggregation=metric.get("aggregation", aggregation),
                    attributes=metric.get("attributes", attributes) or {},
                    origin=origin,
                )
                for metric in metrics
            ]

        return logged_metrics

    # @handle_internal_errors()
    def log_artifact(
        self,
        local_uri: str | Path,
        *,
        name: str | None = None,
    ) -> None:
        """
        Log a file or directory artifact to the current run.

        This stores the artifact in the workspace CAS and uploads it to remote storage.
        Artifact metadata is recorded in artifacts.jsonl for tracking.

        Examples:
            Log a single file:
            ```
            with dreadnode.run("my_run"):
                # Save a file
                with open("results.json", "w") as f:
                    json.dump(results, f)

                # Log it as an artifact
                dreadnode.log_artifact("results.json")
            ```

            Log a directory:
            ```
            with dreadnode.run("my_run"):
                # Create a directory with model files
                os.makedirs("model_output", exist_ok=True)
                save_model("model_output/model.pkl")
                save_config("model_output/config.yaml")

                # Log the entire directory as an artifact
                dreadnode.log_artifact("model_output")
            ```

        Args:
            local_uri: The local path to the file or directory to upload.
            name: Optional name for the artifact (defaults to filename).
        """
        if (run := current_task_span.get()) is None:
            warn_at_user_stacklevel(
                "log_artifact() was called outside of a run.",
                category=DreadnodeUsageWarning,
            )
            return

        # Store/upload artifact and get metadata
        artifact_metadata = run.log_artifact(local_uri=local_uri, name=name)

        # Write metadata to artifacts.jsonl
        if artifact_metadata and self._trace_config:
            if artifact_metadata.get("type") == "directory":
                # For directories, write each file's metadata
                for file_meta in artifact_metadata.get("files", []):
                    self._trace_config.write_artifact(file_meta)
            else:
                self._trace_config.write_artifact(artifact_metadata)

    @handle_internal_errors()
    def log_input(
        self,
        name: str,
        value: t.Any,
        *,
        label: str | None = None,
        attributes: AnyDict | None = None,
    ) -> None:
        """
        Log a single input to the current span.

        Inputs can be any runtime object, which are serialized, stored, and tracked
        in the Dreadnode UI.

        Args:
            name: The name of the input.
            value: The input value to log.
            label: Optional display label.
            attributes: Optional additional attributes.

        Example:
            ```
            @dreadnode.task
            async def my_task(x: int) -> int:
                dreadnode.log_input("input_name", x)
                return x * 2
            ```
        """
        task = current_task_span.get()
        if task is None:
            warn_at_user_stacklevel(
                "log_input() was called outside of a task or run.",
                category=DreadnodeUsageWarning,
            )
            return

        task.log_input(name, value, label=label, attributes=attributes)

    @handle_internal_errors()
    def log_inputs(self, **inputs: t.Any) -> None:
        """
        Log multiple inputs to the current span.

        See `log_input()` for more details.
        """
        for name, value in inputs.items():
            self.log_input(name, value)

    @handle_internal_errors()
    def log_output(
        self,
        name: str,
        value: t.Any,
        *,
        label: str | None = None,
        attributes: AnyDict | None = None,
    ) -> None:
        """
        Log a single output to the current span.

        Outputs can be any runtime object, which are serialized, stored, and tracked
        in the Dreadnode UI.

        Args:
            name: The name of the output.
            value: The value of the output.
            label: An optional label for the output, useful for filtering in the UI.
            attributes: Additional attributes to attach to the output.

        Example:
            ```
            @dreadnode.task
            async def my_task(x: int) -> int:
                result = x * 2
                dreadnode.log_output("result", result)
                return result
            ```
        """
        task = current_task_span.get()
        if task is None:
            warn_at_user_stacklevel(
                "log_output() was called outside of a task or run.",
                category=DreadnodeUsageWarning,
            )
            return

        task.log_output(name, value, label=label, attributes=attributes)

    @handle_internal_errors()
    def log_outputs(self, **outputs: t.Any) -> None:
        """
        Log multiple outputs to the current span.

        See `log_output()` for more details.
        """
        for name, value in outputs.items():
            self.log_output(name, value)

    @handle_internal_errors()
    def log_sample(
        self,
        label: str,
        input: t.Any,
        output: t.Any,
        metrics: MetricsLike | None = None,
        *,
        step: int = 0,
    ) -> None:
        """
        Convenience method to log an input/output pair with metrics as a ephemeral task.

        This is useful for logging a single sample of input and output data
        along with any metrics that were computed during the process.
        """

        with self.task_span(name=label, label=label):
            self.log_input("input", input)
            self.log_output("output", output)
            self.link_objects(output, input)
            if metrics is not None:
                self.log_metrics(metrics, step=step, origin=output)

    @handle_internal_errors()
    def log_samples(
        self,
        name: str,
        samples: list[tuple[t.Any, t.Any] | tuple[t.Any, t.Any, MetricsLike]],
    ) -> None:
        """
        Log multiple input/output samples as ephemeral tasks.

        This is useful for logging a batch of input/output pairs with metrics
        in a single run.

        Example:
            ```
            dreadnode.log_samples(
                "my_samples",
                [
                    (input1, output1, {"accuracy": 0.95}),
                    (input2, output2, {"accuracy": 0.90}),
                ]
            )
            ```

        Args:
            name: The name of the task to create for each sample.
            samples: A list of tuples containing (input, output, metrics [optional]).
        """
        for sample in samples:
            metrics: MetricsLike | None = None
            if len(sample) == 3:
                input_data, output_data, metrics = sample  # ty: ignore[invalid-assignment]
            elif len(sample) == 2:
                input_data, output_data = sample  # ty: ignore[invalid-assignment]
            else:
                raise ValueError(
                    "Each sample must be a tuple of (input, output) or (input, output, metrics)",
                )

            # Log each sample as an ephemeral task
            self.log_sample(name, input_data, output_data, metrics=metrics)

    @handle_internal_errors()
    def link_objects(
        self,
        origin: t.Any,
        link: t.Any,
        attributes: AnyDict | None = None,
    ) -> None:
        """
        Associate two runtime objects with each other.

        This is useful for linking any two objects which are related to
        each other, such as a model and its training data, or an input
        prompt and the resulting output.

        Example:
            ```
            with dreadnode.run("my_run"):
                model = SomeModel()
                data = SomeData()

                dreadnode.link_objects(model, data)
            ```

        Args:
            origin: The origin object to link from.
            link: The linked object to link to.
            attributes: Additional attributes to attach to the link.
        """
        if (run := current_task_span.get()) is None:
            warn_at_user_stacklevel(
                "link_objects() was called outside of a run.",
                category=DreadnodeUsageWarning,
            )
            return

        origin_hash = run.log_object(origin)
        link_hash = run.log_object(link)
        run.link_objects(origin_hash, link_hash, attributes=attributes)

    def serve(
        self,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        """Start the agent server.

        This starts a FastAPI server that provides REST + WebSocket endpoints
        for agent communication.

        Args:
            host: Host to bind to. Defaults to DREADNODE_RUNTIME_HOST (legacy:
                DREADNODE_SERVER_HOST) or 127.0.0.1.
            port: Port to bind to. Defaults to DREADNODE_RUNTIME_PORT (legacy:
                DREADNODE_SERVER_PORT) or 8787.

        Example:
            ```python
            import dreadnode as dn
            dn.configure()
            dn.serve(port=8787)
            ```
        """
        from dreadnode.app.server import run_server

        if not self._initialized:
            self.configure()

        run_server(self, host=host, port=port)


DEFAULT_INSTANCE = Dreadnode()
