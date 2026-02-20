from pathlib import Path
from typing import Any, Dict, List, Optional

from abstra_internals.controllers.sdk.sdk_tasks import TasksSDKController
from abstra_internals.entities.agents.memory_manager import MemoryManager
from abstra_internals.entities.agents.tools.browser_handler import (
    CheckCheckboxHandler,
    ClickHandler,
    CloseTabHandler,
    ExtractTextHandler,
    HoverHandler,
    InspectNetworkLogsHandler,
    ListDownloadsHandler,
    MakeRequestHandler,
    MoveDownloadHandler,
    NavigateHandler,
    NewTabHandler,
    PressKeyHandler,
    RunJavascriptHandler,
    SaveFactHandler,
    ScreenshotHandler,
    SelectOptionHandler,
    SwitchTabHandler,
    TypeTextHandler,
    WaitForDownloadHandler,
    WaitHandler,
)
from abstra_internals.entities.agents.tools.browser_session import BrowserSession
from abstra_internals.entities.agents.tools.connections_handler import (
    ExecuteConnectionActionHandler,
    GetConnectionActionDetailsHandler,
)
from abstra_internals.entities.agents.tools.dispatcher import (
    FinishHandler,
    ToolHandler,
)
from abstra_internals.entities.agents.tools.files_handler import (
    CreatePublicLinkHandler,
    FilesListHandler,
    FilesReadHandler,
    FilesWriteHandler,
    SourceCodeListHandler,
    SourceCodeReadHandler,
)
from abstra_internals.entities.agents.tools.send_task_handler import SendTaskHandler
from abstra_internals.entities.agents.tools.tables_handler import (
    TablesDeleteHandler,
    TablesInsertHandler,
    TablesSelectHandler,
    TablesUpdateHandler,
)
from abstra_internals.repositories.connectors import ConnectorsRepository
from abstra_internals.repositories.project.project import (
    AgentPermission,
    AgentStage,
    WorkflowTransition,
)
from abstra_internals.repositories.tables import TablesRepository

_TABLES_ACTION_MAP = {
    "select": TablesSelectHandler,
    "insert": TablesInsertHandler,
    "update": TablesUpdateHandler,
    "delete": TablesDeleteHandler,
}


def _make_tables_handler(
    perm: AgentPermission,
    tables_repo: TablesRepository,
) -> Optional[ToolHandler]:
    if not perm.table_name:
        return None
    handler_cls = _TABLES_ACTION_MAP.get(perm.action)
    if handler_cls is None:
        return None
    return handler_cls(table_name=perm.table_name, tables_repo=tables_repo)


def _collect_connection_permissions(
    permissions: List[AgentPermission],
) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for perm in permissions:
        if perm.type == "connections" and perm.connection_name:
            result.setdefault(perm.connection_name, []).append(perm.action)
    return result


_JSON_SCHEMA_TYPES = {
    "object",
    "array",
    "string",
    "number",
    "integer",
    "boolean",
    "null",
}


def _normalize_task_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    if schema.get("type") in _JSON_SCHEMA_TYPES:
        return {"default": schema}
    return schema


def _make_send_task_handler(
    transition: WorkflowTransition,
    task_sdk: TasksSDKController,
    target_task_schemas: Dict[str, Dict[str, Any]],
) -> Optional[SendTaskHandler]:
    task_type = transition.task_type
    if not task_type or not task_type.strip():
        task_type = "default"
    full_schema = target_task_schemas.get(transition.target_id)
    payload_schema: Optional[Dict[str, Any]] = None
    if isinstance(full_schema, dict):
        normalized = _normalize_task_schema(full_schema)
        payload_schema = normalized.get(task_type) or normalized.get("default")
    return SendTaskHandler(
        task_type=task_type,
        task_sdk=task_sdk,
        task_schema=payload_schema,
    )


def _make_browser_handlers(
    session: BrowserSession,
    memory_manager: Optional[MemoryManager] = None,
) -> List[ToolHandler]:
    handlers: List[ToolHandler] = [
        NavigateHandler(session),
        ClickHandler(session),
        TypeTextHandler(session),
        PressKeyHandler(session),
        SelectOptionHandler(session),
        HoverHandler(session),
        CheckCheckboxHandler(session),
        ExtractTextHandler(session),
        ScreenshotHandler(session),
        WaitHandler(session),
        RunJavascriptHandler(session),
        ListDownloadsHandler(session),
        MoveDownloadHandler(session),
        WaitForDownloadHandler(session),
        NewTabHandler(session),
        SwitchTabHandler(session),
        CloseTabHandler(session),
        MakeRequestHandler(session),
        InspectNetworkLogsHandler(session),
    ]
    if memory_manager is not None:
        handlers.append(SaveFactHandler(memory_manager))
    return handlers


def build_tool_handlers(
    stage: AgentStage,
    tables_repo: TablesRepository,
    connectors_repo: ConnectorsRepository,
    task_sdk: TasksSDKController,
    working_dir: Path,
    target_task_schemas: Optional[Dict[str, Dict[str, Any]]] = None,
    browser_session: Optional[BrowserSession] = None,
    memory_manager: Optional[MemoryManager] = None,
) -> List[ToolHandler]:
    handlers: List[ToolHandler] = []
    schemas = target_task_schemas or {}

    source_code_glob = ""
    has_source_code = False
    has_publish = False

    for perm in stage.permissions:
        if perm.type == "tables":
            handler: Optional[ToolHandler] = _make_tables_handler(perm, tables_repo)
            if handler is not None:
                handlers.append(handler)
        elif perm.type == "source_code":
            has_source_code = True
            glob_condition = perm.condition
            if isinstance(glob_condition, str) and glob_condition:
                source_code_glob = glob_condition
        elif perm.type == "files" and perm.action == "publish":
            has_publish = True

    connection_perms = _collect_connection_permissions(stage.permissions)
    if connection_perms:
        try:
            existing = connectors_repo.list_connections()
            existing_names = {c.name for c in existing}
            connection_perms = {
                k: v for k, v in connection_perms.items() if k in existing_names
            }
        except Exception:
            pass
    if connection_perms:
        handlers.append(
            GetConnectionActionDetailsHandler(connection_perms, connectors_repo)
        )
        handlers.append(
            ExecuteConnectionActionHandler(connection_perms, connectors_repo)
        )

    handlers.append(FilesListHandler(working_dir))
    handlers.append(FilesReadHandler(working_dir))
    handlers.append(FilesWriteHandler(working_dir))

    if has_source_code:
        handlers.append(SourceCodeReadHandler(source_code_glob))
        handlers.append(SourceCodeListHandler(source_code_glob))

    if has_publish:
        handlers.append(CreatePublicLinkHandler(source_code_glob))

    for transition in stage.workflow_transitions:
        send_handler = _make_send_task_handler(transition, task_sdk, schemas)
        if send_handler is not None:
            handlers.append(send_handler)

    if browser_session is not None:
        handlers.extend(_make_browser_handlers(browser_session, memory_manager))

    handlers.append(FinishHandler())

    return handlers
