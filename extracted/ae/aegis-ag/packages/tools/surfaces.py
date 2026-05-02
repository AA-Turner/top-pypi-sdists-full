"""Protocols and in-memory support types for built-in tools."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Callable, Protocol
from uuid import uuid4

from packages.contracts.runtime import EvidenceRetrievalResult, ExecutionResult, GoalNode, MemoryRecord
from packages.cron import CronRuntime
from packages.operator import (
    ActivityOperatorSurface,
    ProcedureOperatorDetail,
    ProcedureOperatorSurface,
    ProfileOperatorSurface,
)
from packages.skills import SkillDefinition, SkillHubEntry, SkillManifestLoadRecord
from .runtime import ToolInvocation

class MemoryManagementSurface(Protocol):
    def inspect_memories(self, session_id: str) -> tuple[MemoryRecord, ...]:
        """List active memories for a session."""

    def inspect_memory(self, session_id: str, memory_id: str) -> MemoryRecord:
        """Inspect one memory."""

    def search_memories(self, session_id: str, query: str, *, limit: int = 5) -> tuple[MemoryRecord, ...]:
        """Search memories relevant to a query."""

    def correct_memory(
        self,
        session_id: str,
        memory_id: str,
        *,
        corrected_content: str,
        reason: str = "",
    ) -> tuple[MemoryRecord | None, MemoryRecord | None, str, str | None]:
        """Correct a memory with lineage preserved."""

    def delete_memory(self, session_id: str, memory_id: str, *, reason: str) -> tuple[MemoryRecord, str | None]:
        """Delete a memory through governed flow."""

    def pin_memory(self, session_id: str, memory_id: str, *, reason: str = "") -> tuple[MemoryRecord, str]:
        """Pin a memory so governance treats it as protected."""

    def unpin_memory(self, session_id: str, memory_id: str, *, reason: str = "") -> tuple[MemoryRecord, str]:
        """Remove the pinned tag from a memory."""

    def memory_lineage(self, memory_id: str) -> str | None:
        """Inspect lineage for a memory."""

    def memory_state(self, memory_id: str) -> str | None:
        """Inspect lifecycle state for a memory."""


class RecallSearchSurface(Protocol):
    def recall(
        self,
        session_id: str,
        query: str,
        *,
        limit: int = 5,
    ) -> EvidenceRetrievalResult:
        """Retrieve scoped evidence for the current turn without mutating durable truth."""


class BrowserVisionAnalyzer(Protocol):
    def analyze_browser_screenshot(
        self,
        *,
        session_id: str,
        invocation_id: str,
        question: str,
        screenshot_path: Path,
        page_url: str = "",
        page_title: str = "",
        page_snapshot: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any] | str:
        """Analyze a browser screenshot with an optional multimodal provider."""


class BrowserToolBackend(Protocol):
    def backend_label(self) -> str:
        """Human-readable backend identifier."""

    def invoke(
        self,
        action: str,
        invocation: ToolInvocation,
        *,
        vision_analyzer: BrowserVisionAnalyzer | None = None,
    ) -> Mapping[str, Any] | ExecutionResult:
        """Run one browser action."""


class MessageDeliverySurface(Protocol):
    def send_message(
        self,
        *,
        session_id: str,
        body: str,
        target: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> Mapping[str, Any] | ExecutionResult:
        """Deliver an outbound message to a configured target."""


class ClarifySurface(Protocol):
    def request_clarification(
        self,
        *,
        session_id: str,
        question: str,
        mode: str,
        choices: tuple[str, ...] = (),
    ) -> Mapping[str, Any] | ExecutionResult:
        """Request user clarification through a surface-aware prompt."""


class SubAgentsSurface(Protocol):
    def run_sub_agent(
        self,
        *,
        session_id: str,
        task: str,
        name: str | None = None,
        skills: tuple[str, ...] = (),
    ) -> Mapping[str, Any] | ExecutionResult:
        """Run one bounded sub-agent task and return its final result."""

    def run_sub_agents(
        self,
        *,
        session_id: str,
        tasks: tuple[Mapping[str, Any], ...],
        max_concurrency: int = 3,
    ) -> Mapping[str, Any] | ExecutionResult:
        """Run a bounded pool of sub-agent tasks and return final results."""

    def start_sub_agents(
        self,
        *,
        session_id: str,
        tasks: tuple[Mapping[str, Any], ...],
        max_concurrency: int = 3,
    ) -> Mapping[str, Any] | ExecutionResult:
        """Start a bounded pool of sub-agent tasks and return a run handle immediately."""

    def inspect_sub_agent_run(
        self,
        *,
        session_id: str,
        run_id: str,
        wait_timeout_seconds: float | None = None,
    ) -> Mapping[str, Any] | ExecutionResult:
        """Inspect or wait for a previously started sub-agent run."""

    def list_sub_agent_runs(self, *, session_id: str) -> Mapping[str, Any] | ExecutionResult:
        """List sub-agent runs attached to the session."""


class ProfileManagementSurface(Protocol):
    def inspect_profile_surface(self, session_id: str) -> ProfileOperatorSurface:
        """Inspect the owner-aligned profile surface for the active session."""

    def patch_profile_surface(
        self,
        session_id: str,
        payload: Mapping[str, object],
    ) -> ProfileOperatorSurface:
        """Patch the owner-aligned profile surface for the active session."""


class ActivityManagementSurface(Protocol):
    def inspect_activity_surface(self, session_id: str) -> ActivityOperatorSurface:
        """Inspect the owner-aligned activity surface for the active session."""

    def inspect_goal(self, session_id: str, goal_id: str) -> GoalNode:
        """Inspect one durable activity item."""

    def create_goal(self, session_id: str, **kwargs: Any) -> GoalNode:
        """Create one durable activity item."""

    def update_goal(
        self,
        session_id: str,
        goal_id: str,
        *,
        title: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        reason: str | None = None,
    ) -> tuple[GoalNode, GoalNode, str]:
        """Update one durable activity item."""

    def delete_goal(self, session_id: str, goal_id: str, *, reason: str) -> tuple[GoalNode, GoalNode]:
        """Drop one durable activity item."""


class ProcedureManagementSurface(Protocol):
    def inspect_procedure_surface(
        self,
        session_id: str,
        *,
        minimum_support: int = 2,
    ) -> ProcedureOperatorSurface:
        """Inspect promoted procedures and candidates for the active session."""

    def inspect_procedure_detail(self, session_id: str, procedure_id: str) -> ProcedureOperatorDetail:
        """Inspect one promoted procedure."""

    def patch_procedure_surface(
        self,
        session_id: str,
        procedure_id: str,
        payload: Mapping[str, object],
    ) -> ProcedureOperatorDetail:
        """Patch one promoted procedure."""

    def retire_procedure_surface(self, session_id: str, procedure_id: str) -> ProcedureOperatorDetail:
        """Retire one promoted procedure."""


class SkillManagementSurface(Protocol):
    def list_skill_hub(self, *, limit: int | None = None) -> tuple[SkillHubEntry, ...]:
        """List local skill shelf entries visible on this surface."""

    def inspect_skill(self, skill_id: str, *, session_id: str | None = None) -> SkillDefinition:
        """Inspect one installed or local-hub skill package."""

    def inspect_skill_source(self, skill_id: str, *, session_id: str | None = None) -> SkillDefinition:
        """Inspect one operator-selected local or remote skill package source."""

    def set_skill_enabled(
        self,
        skill_id: str,
        enabled: bool,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillDefinition:
        """Enable or disable one installed skill."""

    def install_skill_source(
        self,
        reference: str | Path,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        requester: str | None = None,
    ) -> SkillManifestLoadRecord:
        """Install one skill package from a reference or path."""

    def create_authored_skill(
        self,
        *,
        skill_id: str,
        display_name: str,
        summary: str,
        instruction_text: str,
        category: str | None = None,
        install: bool = True,
        overwrite: bool = False,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillManifestLoadRecord:
        """Create one authored skill package."""

    def update_authored_skill(
        self,
        skill_id: str,
        *,
        display_name: str | None = None,
        summary: str | None = None,
        instruction_text: str | None = None,
        category: str | None = None,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillManifestLoadRecord:
        """Update one authored skill package."""

    def delete_skill_source(
        self,
        skill_id: str,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> tuple[str, str]:
        """Delete one installed or authored skill package."""


@dataclass(frozen=True, slots=True)
class TodoItem:
    item_id: str
    title: str
    status: str = "open"
    notes: str = ""
    goal_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class TodoStore(Protocol):
    def list_items(self, session_id: str) -> tuple[TodoItem, ...]:
        """List session-scoped todo items."""

    def inspect_item(self, session_id: str, item_id: str) -> TodoItem:
        """Inspect one todo item."""

    def upsert_item(
        self,
        session_id: str,
        *,
        item_id: str | None = None,
        title: str,
        status: str = "open",
        notes: str = "",
        goal_id: str | None = None,
    ) -> TodoItem:
        """Create or update a todo item."""

    def remove_item(self, session_id: str, item_id: str) -> TodoItem:
        """Remove one todo item."""

    def clear(self, session_id: str) -> int:
        """Clear all todo items for a session."""


@dataclass
class InMemorySessionTodoStore:
    _items: dict[str, dict[str, TodoItem]] = field(default_factory=dict)

    def list_items(self, session_id: str) -> tuple[TodoItem, ...]:
        return tuple(self._items.get(session_id, {}).values())

    def inspect_item(self, session_id: str, item_id: str) -> TodoItem:
        item = self._items.get(session_id, {}).get(item_id)
        if item is None:
            raise KeyError(item_id)
        return item

    def upsert_item(
        self,
        session_id: str,
        *,
        item_id: str | None = None,
        title: str,
        status: str = "open",
        notes: str = "",
        goal_id: str | None = None,
    ) -> TodoItem:
        now = datetime.now(timezone.utc)
        resolved_id = item_id or f"todo:{uuid4().hex[:10]}"
        current = self._items.get(session_id, {}).get(resolved_id)
        created_at = current.created_at if current is not None else now
        item = TodoItem(
            item_id=resolved_id,
            title=title,
            status=status,
            notes=notes,
            goal_id=goal_id,
            created_at=created_at,
            updated_at=now,
        )
        self._items.setdefault(session_id, {})[resolved_id] = item
        return item

    def remove_item(self, session_id: str, item_id: str) -> TodoItem:
        items = self._items.get(session_id, {})
        item = items.pop(item_id, None)
        if item is None:
            raise KeyError(item_id)
        return item

    def clear(self, session_id: str) -> int:
        removed = len(self._items.get(session_id, {}))
        self._items.pop(session_id, None)
        return removed


@dataclass
class ManagedProcess:
    process_id: str
    command: str
    cwd: Path
    process: subprocess.Popen[str]
    started_at: datetime
    stdout: str = ""
    stderr: str = ""
    finished_at: datetime | None = None

    @property
    def returncode(self) -> int | None:
        return self.process.poll()

    @property
    def running(self) -> bool:
        return self.returncode is None


@dataclass
class InMemoryProcessManager:
    _processes: dict[str, ManagedProcess] = field(default_factory=dict)

    def start(self, *, command: str, cwd: Path, env: Mapping[str, str] | None = None) -> ManagedProcess:
        process_id = f"proc:{uuid4().hex[:10]}"
        popen = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            env={**dict(env or {})} if env else None,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        managed = ManagedProcess(
            process_id=process_id,
            command=command,
            cwd=cwd,
            process=popen,
            started_at=datetime.now(timezone.utc),
        )
        self._processes[process_id] = managed
        return managed

    def list(self) -> tuple[ManagedProcess, ...]:
        return tuple(self._processes.values())

    def get(self, process_id: str) -> ManagedProcess:
        process = self._processes.get(process_id)
        if process is None:
            raise KeyError(process_id)
        return process

    def capture_if_finished(self, process_id: str) -> ManagedProcess:
        managed = self.get(process_id)
        if managed.running or managed.finished_at is not None:
            return managed
        stdout, stderr = managed.process.communicate()
        managed.stdout = stdout or ""
        managed.stderr = stderr or ""
        managed.finished_at = datetime.now(timezone.utc)
        return managed

    def wait(self, process_id: str, *, timeout_seconds: int = 20) -> ManagedProcess:
        managed = self.get(process_id)
        if managed.finished_at is None:
            try:
                stdout, stderr = managed.process.communicate(timeout=max(1, timeout_seconds))
                managed.stdout = stdout or managed.stdout
                managed.stderr = stderr or managed.stderr
                managed.finished_at = datetime.now(timezone.utc)
            except subprocess.TimeoutExpired:
                return managed
        return managed

    def write(self, process_id: str, data: str) -> ManagedProcess:
        managed = self.get(process_id)
        if not managed.running or managed.process.stdin is None:
            raise RuntimeError(f"process is not writable: {process_id}")
        managed.process.stdin.write(data)
        managed.process.stdin.flush()
        return managed

    def kill(self, process_id: str) -> ManagedProcess:
        managed = self.get(process_id)
        if managed.running:
            managed.process.kill()
        return self.capture_if_finished(process_id)


@dataclass(frozen=True, slots=True)
class BuiltinToolDependencies:
    cwd: Path
    workspace_resolver: Callable[[str | None], Path] | None = None
    cron_runtime: CronRuntime | None = None
    profile_management: ProfileManagementSurface | None = None
    activity_management: ActivityManagementSurface | None = None
    memory_management: MemoryManagementSurface | None = None
    recall_search: RecallSearchSurface | None = None
    procedure_management: ProcedureManagementSurface | None = None
    skill_management: SkillManagementSurface | None = None
    browser_backend: BrowserToolBackend | None = None
    browser_vision_analyzer: BrowserVisionAnalyzer | None = None
    message_delivery: MessageDeliverySurface | None = None
    clarify_surface: ClarifySurface | None = None
    sub_agents_surface: SubAgentsSurface | None = None
    process_manager: InMemoryProcessManager = field(default_factory=InMemoryProcessManager)
    todo_store: InMemorySessionTodoStore = field(default_factory=InMemorySessionTodoStore)
    additional_workspace_roots: tuple[Path, ...] = field(
        default_factory=lambda: (Path.home(), Path(tempfile.gettempdir()))
    )
    web_user_agent: str = "Aegis/2.0 (+https://github.com/agentic-in/aegis)"
    code_tool_allowlist: tuple[str, ...] = (
        "tool.file.read",
        "tool.file.write",
        "tool.file.patch",
        "tool.file.search",
        "tool.web.search",
        "tool.web.read",
        "tool.web.extract",
        "tool.terminal.exec",
    )

    def cwd_for_session(self, session_id: str | None) -> Path:
        if self.workspace_resolver is None:
            return self.cwd
        return self.workspace_resolver(session_id)
