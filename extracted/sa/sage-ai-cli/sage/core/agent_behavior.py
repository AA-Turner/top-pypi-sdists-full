"""
Unified agent behavior controller for SAGE.

This module integrates all the fix modules to ensure SAGE behaves correctly:
- Classifies requests properly (analysis vs implementation)
- Maintains context across turns
- Grounds all file references in reality
- Validates responses meet requirements
- Executes tools properly

This is the main entry point for the fixed SAGE behavior.
"""

from __future__ import annotations

import re
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from sage.core.context_persistence import (
    ContextPersistenceManager,
    ConversationContext,
    TaskProgress,
)
from sage.core.grounded_search import (
    FileReferenceValidator,
    GroundedSearch,
    SearchCommandExecutor,
    SearchQuery,
    SearchResponse,
)

# Import all fix modules
from sage.core.request_classifier import (
    ClassifiedRequest,
    OutputFormat,
    RequestClassifier,
    RequestType,
)
from sage.core.response_generator import (
    ResponseQualityValidator,
    ResponseValidationResult,
)
from sage.core.tool_validation import (
    ToolCall,
    ToolExecutionValidator,
    ToolExecutor,
    ToolSelectionHeuristics,
    ToolType,
)

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class AgentState:
    """Current state of the agent."""

    # Session info
    session_id: str
    turn_number: int = 0

    # Request tracking
    original_request: str | None = None
    classification: ClassifiedRequest | None = None

    # Progress tracking
    task_progress: TaskProgress | None = None
    items_generated: int = 0

    # File tracking
    verified_files: set[str] = field(default_factory=set)
    files_read: set[str] = field(default_factory=set)
    files_modified: list[str] = field(default_factory=list)

    # Search tracking
    searches_executed: list[dict[str, Any]] = field(default_factory=list)

    # Tool tracking
    tools_executed: list[ToolCall] = field(default_factory=list)

    # Validation
    last_validation: ResponseValidationResult | None = None


class AgentBehaviorController:
    """
    Main controller that enforces correct agent behavior.

    This class integrates all the fix modules and provides a unified
    interface for the SAGE agent to follow proper behavior patterns.
    """

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

        # Initialize all components
        self.classifier = RequestClassifier()
        self.context_manager = ContextPersistenceManager(base_dir)
        self.searcher = GroundedSearch(base_dir)
        self.file_validator = FileReferenceValidator(self.searcher)
        self.search_executor = SearchCommandExecutor(base_dir)
        self.tool_executor = ToolExecutor(base_dir)
        self.tool_validator = ToolExecutionValidator()
        self.response_validator = ResponseQualityValidator()
        self.tool_heuristics = ToolSelectionHeuristics()

        # Register tool handlers
        self._register_handlers()

        # Current state
        self.state: AgentState | None = None
        self.context: ConversationContext | None = None

    def _register_handlers(self) -> None:
        """Register handlers for all tool types."""
        self.tool_executor.register_handler(ToolType.WRITE, self._handle_write)
        self.tool_executor.register_handler(ToolType.RUN, self._handle_run)
        self.tool_executor.register_handler(ToolType.SEARCH, self._handle_search)

    def _handle_write(self, call: ToolCall) -> str:
        """Handle WRITE tool by writing to filesystem."""
        path = call.command.strip()
        content = call.args.get("content", "")
        
        if not content and "\n" in path:
            path, content = path.split("\n", 1)
            path = path.strip()
            
        full_path = self.base_dir / path if not Path(path).is_absolute() else Path(path)
        full_path = full_path.resolve()
        
        # Ensure directories exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        full_path.write_text(content, encoding="utf-8")
        
        if not full_path.exists():
            return f"Error: Failed to create file at {full_path}"
            
        self.record_file_modification(path)
        return f"Successfully wrote {len(content)} bytes to {full_path}"

    def _handle_run(self, call: ToolCall) -> str:
        """Handle RUN tool by executing shell command."""
        from sage.core.commands import execute_command
        # Allow shell=True for better flexibility in agent-generated scripts
        result = execute_command(call.command, cwd=self.base_dir, allow_shell=True)
        if result.success:
            return result.stdout + (f"\n[stderr]\n{result.stderr}" if result.stderr else "")
        else:
            return f"Error ({result.returncode}):\n{result.stderr}\n{result.stdout}"

    def _handle_search(self, call: ToolCall) -> str:
        """Handle SEARCH tool using the search executor."""
        response = self.search_executor.execute(call.command)
        return self.search_executor.format_results(response)

    # ═══════════════════════════════════════════════════════════════════════════
    # SESSION MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════

    def start_session(self) -> str:
        """Start a new agent session."""
        self.context = self.context_manager.create_context()
        self.state = AgentState(session_id=self.context.session_id)

        # Index files for search
        file_count = self.searcher.index_files()

        return f"Session {self.state.session_id} started. Indexed {file_count} files."

    def resume_session(self, session_id: str | None = None) -> str | None:
        """Resume an existing session."""
        if session_id:
            self.context = self.context_manager.load_context(session_id)
        else:
            self.context = self.context_manager.load_latest_context()

        if self.context is None:
            return None

        self.state = AgentState(
            session_id=self.context.session_id,
            turn_number=self.context.turn_count,
            verified_files=self.context.get_verified_paths(),
            files_modified=list(self.context.files_modified),
        )

        # Restore original request
        if self.context.original_request:
            self.state.original_request = self.context.original_request.raw_text
            # Recreate classification from stored data
            self.state.classification = ClassifiedRequest(
                original_request=self.context.original_request.raw_text,
                request_type=RequestType[
                    self.context.original_request.classification.get("request_type", "ANALYSIS")
                ],
                expected_format=OutputFormat[
                    self.context.original_request.classification.get(
                        "expected_format", "MARKDOWN_LIST"
                    )
                ],
                quantity_required=self.context.original_request.quantity_required,
                priority_ranking=self.context.original_request.priority_ranking,
                read_only=self.context.original_request.read_only,
            )

        # Restore task progress
        if self.context.task_progress:
            self.state.task_progress = self.context.task_progress
            self.state.items_generated = self.context.get_item_count()

        return f"Resumed session {self.state.session_id} at turn {self.state.turn_number}"

    def save_session(self) -> None:
        """Save current session state."""
        if self.context:
            self.context_manager.save_context(self.context)

    # ═══════════════════════════════════════════════════════════════════════════
    # REQUEST HANDLING
    # ═══════════════════════════════════════════════════════════════════════════

    def process_request(self, request: str) -> dict[str, Any]:
        """
        Process a new user request.

        This is the main entry point for handling user requests.
        It classifies the request and sets up proper tracking.
        """
        if self.state is None or self.context is None:
            self.start_session()

        # Increment turn
        self.state.turn_number += 1
        self.context.increment_turn()

        # Classify the request
        classification = self.classifier.classify(request)

        # If this is the first request, store it as the original
        if self.state.original_request is None:
            self.state.original_request = request
            self.state.classification = classification
            self.context.set_original_request(request, classification)

            # Initialize task progress for multi-item requests
            if classification.quantity_required and classification.quantity_required > 1:
                self.state.task_progress = TaskProgress(
                    total_items=classification.quantity_required
                )
                self.context.task_progress = self.state.task_progress

        # Save context
        self.save_session()

        return {
            "session_id": self.state.session_id,
            "turn": self.state.turn_number,
            "request_type": classification.request_type.name,
            "expected_format": classification.expected_format.name,
            "quantity_required": classification.quantity_required,
            "priority_ranking": classification.priority_ranking,
            "read_only": classification.read_only,
            "original_request": self.state.original_request,
            "items_generated": self.state.items_generated,
            "context_summary": self.context.get_context_summary(),
        }

    def get_context_injection(self) -> str:
        """
        Get context to inject into the system prompt.

        This ensures the agent remembers the original request and progress.
        """
        if self.context is None:
            return ""

        parts = ["# CURRENT CONTEXT (DO NOT LOSE THIS)"]
        parts.append(self.context.get_context_summary())

        if self.state and self.state.classification:
            parts.append("\n# RESPONSE REQUIREMENTS")
            if self.state.classification.read_only:
                parts.append("- READ-ONLY: Do NOT create FILE: blocks or modify code")
            if self.state.classification.quantity_required:
                parts.append(
                    f"- QUANTITY: Must produce at least {self.state.classification.quantity_required} items"
                )
            if self.state.classification.priority_ranking:
                parts.append(
                    "- RANKING: Must include priority rankings (P0/P1/P2 or CRITICAL/HIGH/MEDIUM/LOW)"
                )
            if self.state.classification.must_include_file_paths:
                parts.append("- FILE PATHS: Must reference real, verified file paths")

        return "\n".join(parts)

    # ═══════════════════════════════════════════════════════════════════════════
    # FILE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def verify_file(self, path: str) -> bool:
        """Verify a file exists before referencing it."""
        exists = self.searcher.file_exists(path)
        if exists:
            self.state.verified_files.add(path)
            self.context.verify_file(path, self.base_dir)
        return exists

    def read_file(self, path: str) -> str | None:
        """Read a file and track that it was read."""
        # First verify it exists
        if not self.verify_file(path):
            return None

        content = self.searcher.read_file(path)
        if content:
            self.state.files_read.add(path)

        return content

    def must_read_before_reference(self, path: str) -> bool:
        """Check if a file must be read before referencing."""
        return path not in self.state.files_read and path not in self.state.verified_files

    def record_file_modification(self, path: str) -> None:
        """Record that a file was modified."""
        if path not in self.state.files_modified:
            self.state.files_modified.append(path)
        self.context.record_file_modification(path)
        self.save_session()

    # ═══════════════════════════════════════════════════════════════════════════
    # SEARCH OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def execute_search(self, pattern: str, file_glob: str | None = None) -> SearchResponse:
        """Execute a search and track results."""
        query = SearchQuery(pattern=pattern, file_glob=file_glob)
        response = self.searcher.search(query)

        # Track search
        self.state.searches_executed.append(
            {
                "pattern": pattern,
                "file_glob": file_glob,
                "results_count": len(response.results),
                "files_found": list(response.get_unique_files()),
            }
        )

        # Cache results
        self.context.cache_search_results(pattern, list(response.get_unique_files()))

        # Auto-verify found files
        for file_path in response.get_unique_files():
            self.state.verified_files.add(file_path)

        self.save_session()
        return response

    def search_was_executed(self, pattern: str) -> bool:
        """Check if a search was already executed."""
        return any(s["pattern"] == pattern for s in self.state.searches_executed)

    # ═══════════════════════════════════════════════════════════════════════════
    # TOOL OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def execute_tool(
        self, tool_type: ToolType, command: str, args: dict[str, Any] | None = None
    ) -> ToolCall:
        """Execute a tool and track it."""
        call = ToolCall(tool_type=tool_type, command=command, args=args or {})
        result = self.tool_executor.execute(call)

        self.state.tools_executed.append(result)
        self.context.record_execution(
            action=f"{tool_type.name}: {command}",
            result=result.status.name,
            details={"output": result.output[:500] if result.output else None},
        )

        self.save_session()
        return result

    def suggest_tools(self, task: str) -> list[ToolCall]:
        """Get tool suggestions for a task."""
        return self.tool_heuristics.suggest_tools(task)

    def validate_tool_execution(self, response: str) -> dict[str, Any]:
        """Validate that mentioned tools were actually executed."""
        executed, unexecuted = self.tool_validator.validate_execution(
            response, self.state.tools_executed
        )

        return {
            "executed_count": len(executed),
            "unexecuted_count": len(unexecuted),
            "unexecuted_tools": [
                {"type": c.tool_type.name, "command": c.command} for c in unexecuted
            ],
            "all_executed": len(unexecuted) == 0,
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # RESPONSE VALIDATION
    # ═══════════════════════════════════════════════════════════════════════════

    def validate_response(self, response: str) -> ResponseValidationResult:
        """Validate a response against all requirements."""
        if self.state.classification is None:
            # Use a default classification
            classification = ClassifiedRequest(
                original_request="",
                request_type=RequestType.ANALYSIS,
                expected_format=OutputFormat.MARKDOWN_LIST,
            )
        else:
            classification = self.state.classification

        result = self.response_validator.validate(
            response, classification, self.state.verified_files
        )

        self.state.last_validation = result
        return result

    def check_response_before_send(self, response: str) -> dict[str, Any]:
        """
        Final check before sending response to user.

        Returns a dict with:
        - can_send: bool
        - issues: list of issues that must be fixed
        - warnings: list of warnings (can still send)
        """
        validation = self.validate_response(response)
        tool_check = self.validate_tool_execution(response)

        blocking_issues = []
        warnings = []

        # Check validation errors
        for issue in validation.issues:
            if issue.severity == "ERROR":
                blocking_issues.append(issue.message)
            elif issue.severity == "WARNING":
                warnings.append(issue.message)

        # Check unexecuted tools
        if not tool_check["all_executed"]:
            for tool in tool_check["unexecuted_tools"]:
                blocking_issues.append(
                    f"Tool mentioned but not executed: {tool['type']} {tool['command']}"
                )

        # Check quantity requirements
        if (
            self.state.classification
            and self.state.classification.quantity_required
            and validation.item_count < self.state.classification.quantity_required
        ):
            blocking_issues.append(
                f"Response has {validation.item_count} items but "
                f"{self.state.classification.quantity_required} required"
            )

        return {
            "can_send": len(blocking_issues) == 0,
            "issues": blocking_issues,
            "warnings": warnings,
            "validation_score": validation.score,
            "item_count": validation.item_count,
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # PROGRESS TRACKING
    # ═══════════════════════════════════════════════════════════════════════════

    def record_item(self, item: dict[str, Any]) -> int:
        """Record a generated item."""
        item_num = self.context.add_item(item)
        self.state.items_generated = self.context.get_item_count()

        if self.state.task_progress:
            self.state.task_progress.mark_completed(item_num)

        self.save_session()
        return item_num

    def get_progress_summary(self) -> str:
        """Get current progress summary."""
        if self.state.task_progress:
            return (
                f"Progress: {self.state.task_progress.completed_items}/"
                f"{self.state.task_progress.total_items} items "
                f"({self.state.task_progress.progress_percent:.1f}%)"
            )
        return f"Items generated: {self.state.items_generated}"

    # ═══════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════

    def get_status(self) -> dict[str, Any]:
        """Get current agent status."""
        return {
            "session_id": self.state.session_id if self.state else None,
            "turn": self.state.turn_number if self.state else 0,
            "original_request": self.state.original_request if self.state else None,
            "request_type": self.state.classification.request_type.name
            if self.state and self.state.classification
            else None,
            "items_generated": self.state.items_generated if self.state else 0,
            "files_verified": len(self.state.verified_files) if self.state else 0,
            "files_read": len(self.state.files_read) if self.state else 0,
            "files_modified": len(self.state.files_modified) if self.state else 0,
            "searches_executed": len(self.state.searches_executed) if self.state else 0,
            "tools_executed": len(self.state.tools_executed) if self.state else 0,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Convenience functions
# ═══════════════════════════════════════════════════════════════════════════════


def create_agent_controller(base_dir: Path) -> AgentBehaviorController:
    """Create a new agent behavior controller."""
    return AgentBehaviorController(base_dir)


def process_user_request(base_dir: Path, request: str) -> dict[str, Any]:
    """Process a user request with proper behavior enforcement."""
    controller = AgentBehaviorController(base_dir)
    controller.start_session()
    return controller.process_request(request)
