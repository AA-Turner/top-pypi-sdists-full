from dataclasses import dataclass
from multiprocessing import Queue
from typing import Optional

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.credentials import resolve_headers_raise
from abstra_internals.environment import (
    CLOUD_API_CLI_URL,
    CLOUD_API_PROD_HEADERS,
    CLOUD_API_PROD_URL,
    EDITOR_MODE,
    RABBITMQ_CONNECTION_URI,
    linter_sidecar_enabled,
)
from abstra_internals.repositories.ai import (
    AIRepository,
    LocalAIRepository,
    ProductionAIRepository,
)
from abstra_internals.repositories.code_markers.repository import (
    CodeMarkersRepository,
    LocalCodeMarkersRepository,
    ProductionCodeMarkersRepository,
)
from abstra_internals.repositories.connectors import ConnectorsRepository
from abstra_internals.repositories.editor_auth import (
    EditorAuthRepository,
    ProductionEditorAuthRepository,
    WebEditorAuthRepository,
)
from abstra_internals.repositories.email import EmailRepository
from abstra_internals.repositories.execution import (
    ExecutionRepository,
    LocalExecutionRepository,
    ProductionExecutionRepository,
    WebEditorExecutionRepository,
)
from abstra_internals.repositories.execution_logs import (
    ExecutionLogsRepository,
    LocalExecutionLogsRepository,
    ProductionExecutionLogsRepository,
)
from abstra_internals.repositories.infra import (
    InfraRepository,
    LocalInfraRepository,
    ProductionInfraRepository,
)
from abstra_internals.repositories.keyvalue import (
    KVRepository,
    LocalKVRepository,
    ProductionKVRepository,
)
from abstra_internals.repositories.linter.repository import (
    LinterRepository,
    LocalLinterRepository,
    ProductionLinterRepository,
)
from abstra_internals.repositories.metrics import (
    LocalMetricsRepository,
    MetricsRepository,
    ProductionMetricsRepository,
)
from abstra_internals.repositories.multiprocessing import (
    ForkServerContextRepository,
    MPContextReposity,
    SpawnContextReposity,
)
from abstra_internals.repositories.passwordless import (
    LocalPasswordlessRepository,
    PasswordlessRepository,
    ProductionPasswordlessRepository,
)
from abstra_internals.repositories.producer import (
    LocalProducerRepository,
    ProducerRepository,
    ProductionProducerRepository,
    WebEditorProducerRepository,
)
from abstra_internals.repositories.project.disabled_stages_loader import (
    ProductionDisabledStagesLoader,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
    ProductionProjectRepository,
    ProjectRepository,
)
from abstra_internals.repositories.roles import (
    LocalRolesRepository,
    ProductionRolesRepository,
    RolesRepository,
)
from abstra_internals.repositories.tables import (
    LocalTablesRepository,
    ProductionTablesRepository,
    TablesRepository,
)
from abstra_internals.repositories.tasks import (
    LocalTasksRepository,
    ProductionTasksRepository,
    TasksRepository,
)
from abstra_internals.repositories.users import (
    LocalUsersRepository,
    ProductionUsersRepository,
    UsersRepository,
)
from abstra_internals.services.api_key_status import ApiKeyStatus
from abstra_internals.utils.multiprocessing import safe_multiprocessing_queue


def _build_editor_linter_repository() -> LinterRepository:
    """Editor linting runs in a dedicated child process by default; the
    ABSTRA_LINTER_SIDECAR kill-switch falls back to the in-process fan-out.
    The sidecar spawns lazily on the first lint RPC, so building it here is
    free for processes that never lint (executors, workers, tests)."""
    if linter_sidecar_enabled():
        from abstra_internals.repositories.linter.sidecar.client import (
            SidecarLinterRepository,
        )

        return SidecarLinterRepository()
    return LocalLinterRepository()


def get_mp_context_repository() -> MPContextReposity:
    """Get the appropriate multiprocessing context repository based on environment variable."""
    import os

    mp_context = os.environ.get("ABSTRA_MP_CONTEXT", "spawn").lower()
    if mp_context == "forkserver":
        return ForkServerContextRepository()
    else:
        return SpawnContextReposity()


@dataclass
class Repositories:
    project: ProjectRepository
    execution_logs: ExecutionLogsRepository
    connectors: ConnectorsRepository
    execution: ExecutionRepository
    mp_context: MPContextReposity
    producer: ProducerRepository
    tables: TablesRepository
    email: EmailRepository
    users: UsersRepository
    roles: RolesRepository
    ai: AIRepository
    passwordless: PasswordlessRepository
    kv: KVRepository
    roles: RolesRepository
    tasks: TasksRepository
    tables: TablesRepository
    users: UsersRepository
    linter: LinterRepository
    infra: InfraRepository
    code_markers: CodeMarkersRepository
    editor_auth: EditorAuthRepository
    metrics: MetricsRepository


def build_editor_repositories(local_queue: Optional[Queue] = None):
    mp_context = get_mp_context_repository()

    if local_queue is None:
        local_queue = safe_multiprocessing_queue(mp_context.get_context())

    http_client = HTTPClient(
        base_url=CLOUD_API_CLI_URL,
        base_headers_resolver=resolve_headers_raise,
        # Only the web editor recovers from a revoked API key: its token comes
        # from the deployment, so cloud-api can hand it a live one against the
        # editor session (see ApiKeyStatus). This bundle also serves the legacy
        # web editor, hence the mode check — in a local install the same 401 means
        # "run abstra login".
        on_unauthorized=(
            ApiKeyStatus.recover_from_unauthorized if EDITOR_MODE == "web" else None
        ),
    )

    editor_auth = WebEditorAuthRepository(client=http_client)
    if EDITOR_MODE == "web":
        ApiKeyStatus.configure_repair(editor_auth.repair_api_key)

    linter = _build_editor_linter_repository()

    return Repositories(
        project=LocalProjectRepository(),
        execution=LocalExecutionRepository(),
        producer=LocalProducerRepository(local_queue=local_queue),
        connectors=ConnectorsRepository(client=http_client),
        tasks=LocalTasksRepository(),
        tables=LocalTablesRepository(client=http_client),
        email=EmailRepository(client=http_client),
        # The real implementation (not a no-op) even though the local editor
        # never renews tokens: this bundle also serves the legacy web editor
        # (EDITOR_MODE=web without RABBITMQ_CONNECTION_URI — see
        # interface/cli/editor.py), where session renewal must work. Once the
        # legacy mode is removed, this can become a no-op and the real
        # implementation moves exclusively to build_web_editor_repositories.
        editor_auth=editor_auth,
        roles=LocalRolesRepository(client=http_client),
        ai=LocalAIRepository(client=http_client),
        execution_logs=LocalExecutionLogsRepository(),
        users=LocalUsersRepository(client=http_client),
        passwordless=LocalPasswordlessRepository(),
        kv=LocalKVRepository(),
        mp_context=mp_context,
        linter=linter,
        infra=LocalInfraRepository(),
        code_markers=LocalCodeMarkersRepository(),
        metrics=LocalMetricsRepository(),
    )


def build_prod_repositories():
    if CLOUD_API_PROD_URL is None or RABBITMQ_CONNECTION_URI is None:
        raise Exception("Production urls are not set")

    disabled_stages_loader = ProductionDisabledStagesLoader()

    http_client = HTTPClient(
        base_url=CLOUD_API_PROD_URL, base_headers=CLOUD_API_PROD_HEADERS
    )

    return Repositories(
        project=ProductionProjectRepository(disabled_stages_loader),
        producer=ProductionProducerRepository(RABBITMQ_CONNECTION_URI),
        execution_logs=ProductionExecutionLogsRepository(client=http_client),
        connectors=ConnectorsRepository(client=http_client),
        execution=ProductionExecutionRepository(client=http_client),
        tables=ProductionTablesRepository(client=http_client),
        email=EmailRepository(client=http_client),
        editor_auth=ProductionEditorAuthRepository(),
        roles=ProductionRolesRepository(),
        users=ProductionUsersRepository(client=http_client),
        tasks=ProductionTasksRepository(client=http_client),
        ai=ProductionAIRepository(client=http_client),
        passwordless=ProductionPasswordlessRepository(client=http_client),
        kv=ProductionKVRepository(client=http_client),
        mp_context=get_mp_context_repository(),
        linter=ProductionLinterRepository(),
        infra=ProductionInfraRepository(client=http_client),
        code_markers=ProductionCodeMarkersRepository(),
        metrics=ProductionMetricsRepository(client=http_client),
    )


def build_web_editor_repositories(rabbitmq_connection_uri: str):
    """Build repositories for the web editor.

    ``WEB_EDITOR_DATABASE_URI`` is the single switch (invariant §6, tabela-verdade
    §12) between the file-based backend (current behavior, unchanged) and the
    PostgreSQL backend. Only ``tasks``/``execution``/``execution_logs`` differ
    between the two paths; everything else is identical. This factory does NOT run
    migrations (decision D11) — it also runs in the executor warmup, so migrating
    here would take the advisory lock on every warmup. Migrations are owned by the
    boot entrypoints (editor/worker).
    """
    from abstra_internals.environment import (
        WEB_EDITOR_DATABASE_URI,
        web_editor_uses_db,
    )
    from abstra_internals.logger import AbstraLogger

    # Never log the connection URIs (they carry passwords). Log presence only.
    AbstraLogger.info(
        "[Factory] Building web editor repositories "
        f"(rabbitmq={'SET' if rabbitmq_connection_uri else 'NOT SET'}, "
        f"db={'SET' if WEB_EDITOR_DATABASE_URI else 'NOT SET'})"
    )

    http_client = HTTPClient(
        base_url=CLOUD_API_CLI_URL,
        base_headers_resolver=resolve_headers_raise,
        on_unauthorized=ApiKeyStatus.recover_from_unauthorized,
    )

    editor_auth = WebEditorAuthRepository(client=http_client)
    # Lets the recovery reach cloud-api without the service importing a
    # repository; the client above calls it whenever a 401 turns out to be the
    # API key rather than the session token.
    ApiKeyStatus.configure_repair(editor_auth.repair_api_key)

    linter = _build_editor_linter_repository()
    mp_context_repo = get_mp_context_repository()

    # Only tasks/execution/execution_logs differ between the two backends; the
    # rest are identical. Select the backend-specific trio, then build the bundle
    # with explicit keyword args (a **dict spread would erase the per-field types
    # for the type checker).
    tasks: TasksRepository
    execution: ExecutionRepository
    execution_logs: ExecutionLogsRepository
    if web_editor_uses_db():
        # PostgreSQL backend. Lazy imports (decision D8) so the legacy path never
        # imports psycopg.
        from abstra_internals.repositories.execution import (
            PgWebEditorExecutionRepository,
        )
        from abstra_internals.repositories.execution_logs import (
            PgWebEditorExecutionLogsRepository,
        )
        from abstra_internals.repositories.tasks import PgWebEditorTasksRepository

        tasks = PgWebEditorTasksRepository()
        execution = PgWebEditorExecutionRepository(rabbitmq_connection_uri)
        execution_logs = PgWebEditorExecutionLogsRepository()
    else:
        # File-based backend (unchanged).
        tasks = LocalTasksRepository()
        execution = WebEditorExecutionRepository(rabbitmq_connection_uri)
        execution_logs = LocalExecutionLogsRepository()

    return Repositories(
        project=LocalProjectRepository(),
        execution=execution,
        producer=WebEditorProducerRepository(rabbitmq_connection_uri),
        connectors=ConnectorsRepository(client=http_client),
        tasks=tasks,
        tables=LocalTablesRepository(client=http_client),
        email=EmailRepository(client=http_client),
        editor_auth=editor_auth,
        roles=LocalRolesRepository(client=http_client),
        ai=LocalAIRepository(client=http_client),
        execution_logs=execution_logs,
        users=LocalUsersRepository(client=http_client),
        passwordless=LocalPasswordlessRepository(),
        kv=LocalKVRepository(),
        mp_context=mp_context_repo,
        linter=linter,
        infra=LocalInfraRepository(),
        code_markers=LocalCodeMarkersRepository(),
        metrics=LocalMetricsRepository(),
    )
