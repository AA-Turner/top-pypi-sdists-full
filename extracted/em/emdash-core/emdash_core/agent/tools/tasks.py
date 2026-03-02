"""Task management tools for agent workflows."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory


# ─────────────────────────────────────────────────────────────
# Legacy Task Status (v1 - in-memory)
# ─────────────────────────────────────────────────────────────


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """A task in the todo list."""

    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
        }


class ChoiceQuestion:
    """A choice question with options."""

    def __init__(
        self,
        question: str,
        options: list[dict],
        header: str = "",
        multi_select: bool = False,
    ):
        self.question = question
        self.options = options  # List of {"label": str, "description": str}
        self.header = header or question.split()[0][:12]  # Default: first word of question
        self.multi_select = multi_select

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "header": self.header,
            "options": self.options,
            "multiSelect": self.multi_select,
        }


class TaskState:
    """Singleton state for task management."""

    _instance: Optional["TaskState"] = None

    def __init__(self):
        self.tasks: list[Task] = []
        self.completed: bool = False
        self.completion_summary: Optional[str] = None
        self.pending_question: Optional[str] = None
        self.user_response: Optional[str] = None
        self.pending_choices: Optional[list[ChoiceQuestion]] = None
        self.choice_context: Optional[str] = None
        self.choice_responses: Optional[list[str]] = None
        self._next_id: int = 1

    @classmethod
    def get_instance(cls) -> "TaskState":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance."""
        cls._instance = None

    def add_task(
        self,
        title: str,
        description: str = "",
    ) -> Task:
        """Add a new task.

        Args:
            title: Task title
            description: Detailed description
        """
        task = Task(
            id=str(self._next_id),
            title=title,
            description=description,
        )
        self._next_id += 1
        self.tasks.append(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        task = self.get_task(task_id)
        if task:
            task.status = status
            return True
        return False

    def get_all_tasks(self) -> list[dict]:
        """Get all tasks as dicts."""
        return [t.to_dict() for t in self.tasks]

    def mark_completed(self, summary: str):
        """Mark the overall task as completed."""
        self.completed = True
        self.completion_summary = summary

    def ask_question(self, question: str):
        """Set a pending question for the user."""
        self.pending_question = question
        self.user_response = None

    def set_pending_choices(
        self,
        choices: list["ChoiceQuestion"],
        context: str = "approach",
    ):
        """Set pending choice questions for the user.

        Args:
            choices: List of ChoiceQuestion objects
            context: Context type (approach, scope, requirement)
        """
        self.pending_choices = choices
        self.choice_context = context
        self.choice_responses = None

    def clear_pending_choices(self):
        """Clear pending choices after user responds."""
        self.pending_choices = None
        self.choice_context = None


class TaskManagementTool(BaseTool):
    """Base class for task management tools."""

    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    @property
    def state(self) -> TaskState:
        """Get current TaskState instance (always fresh to handle resets)."""
        return TaskState.get_instance()


class WriteTodoTool(TaskManagementTool):
    """Create a new task for tracking work."""

    name = "write_todo"
    description = """Create a new task.

With Tasks v2 (EMDASH_TASKS_V2=1), you can also specify:
- labels: List of labels for categorization (e.g., ["backend", "api"])
- depends_on: List of task IDs that must complete first

Use reset=true to clear all existing tasks first (v1 only)."""

    def execute(
        self,
        title: str,
        description: str = "",
        reset: bool = False,
        labels: list[str] = None,
        depends_on: list[str] = None,
        priority: int = 0,
        **kwargs,
    ) -> ToolResult:
        """Create a new task.

        Args:
            title: Short task title
            description: Detailed description (optional)
            reset: If true, clear all existing tasks before adding this one (v1 only)
            labels: Labels for categorization (v2 only)
            depends_on: Task IDs that must complete first (v2 only)
            priority: Task priority (higher = more important) (v2 only)

        Returns:
            ToolResult with task info
        """
        if not title or not title.strip():
            return ToolResult.error_result("Task title is required")

        # Check if Tasks v2 is enabled
        try:
            from emdash_core.tasks import is_tasks_v2_enabled, get_current_task_list, get_session_id
            from emdash_core.tasks.store import TaskStore

            if is_tasks_v2_enabled():
                return self._execute_v2(
                    title=title.strip(),
                    description=description.strip() if description else "",
                    labels=labels,
                    depends_on=depends_on,
                    priority=priority,
                )
        except ImportError:
            pass

        # Fall back to v1 (in-memory)
        return self._execute_v1(title, description, reset)

    def _execute_v1(self, title: str, description: str, reset: bool) -> ToolResult:
        """Execute using legacy in-memory TaskState."""
        # Reset all tasks if requested
        if reset:
            TaskState.reset()

        task = self.state.add_task(
            title=title.strip(),
            description=description.strip() if description else "",
        )

        return ToolResult.success_result({
            "task": task.to_dict(),
            "total_tasks": len(self.state.tasks),
            "all_tasks": self.state.get_all_tasks(),
            "was_reset": reset,
        })

    def _execute_v2(
        self,
        title: str,
        description: str,
        labels: list[str] | None,
        depends_on: list[str] | None,
        priority: int,
    ) -> ToolResult:
        """Execute using file-based TaskStore."""
        from emdash_core.tasks import get_current_task_list, get_session_id
        from emdash_core.tasks.store import TaskStore

        store = TaskStore()
        task_list_id = get_current_task_list()
        session_id = get_session_id()

        try:
            task = store.add_task(
                task_list_id=task_list_id,
                title=title,
                description=description,
                labels=labels or [],
                depends_on=depends_on or [],
                priority=priority,
                created_by=session_id,
            )

            all_tasks = store.get_all_tasks(task_list_id)

            return ToolResult.success_result({
                "task": task.to_dict(),
                "task_id": task.id,
                "labels": task.labels,
                "depends_on": task.depends_on,
                "task_list": task_list_id,
                "total_tasks": len(all_tasks),
                "message": f"Created task '{title}'" + (f" with labels {labels}" if labels else ""),
            })
        except ValueError as e:
            return ToolResult.error_result(str(e))

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "title": {
                    "type": "string",
                    "description": "Short task title",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of what needs to be done",
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels for categorization (e.g., ['backend', 'api']). Tasks v2 only.",
                },
                "depends_on": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Task IDs that must complete before this task. Tasks v2 only.",
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority (higher = more important). Tasks v2 only.",
                    "default": 0,
                },
                "reset": {
                    "type": "boolean",
                    "description": "Set to true to clear all existing tasks (v1 only)",
                    "default": False,
                },
            },
            required=["title"],
        )


class UpdateTodoListTool(TaskManagementTool):
    """Update task status."""

    name = "update_todo_list"
    description = "Update task status. Auto-creates tasks if they don't exist."

    def execute(
        self,
        task_id: str,
        status: str = None,
        title: str = "",
        description: str = "",
        **kwargs,  # Ignore unexpected params from LLM
    ) -> ToolResult:
        """Update task status.

        Args:
            task_id: Task ID to update (e.g., "1", "2")
            status: New status (pending, in_progress, completed)
            title: Optional title for auto-created tasks
            description: Optional description for auto-created tasks

        Returns:
            ToolResult with updated task list
        """
        task = self.state.get_task(task_id)

        # Auto-create task if not found
        if not task:
            new_status = TaskStatus.PENDING
            if status:
                try:
                    new_status = TaskStatus(status.lower())
                except ValueError:
                    pass

            task = Task(
                id=str(task_id),
                title=title or f"Task {task_id}",
                status=new_status,
                description=description,
            )
            self.state.tasks.append(task)
            return ToolResult.success_result({
                "task_id": task_id,
                "auto_created": True,
                "task": task.to_dict(),
                "all_tasks": self.state.get_all_tasks(),
            })

        # Update status if provided
        if status:
            try:
                task.status = TaskStatus(status.lower())
            except ValueError:
                return ToolResult.error_result(
                    f"Invalid status: {status}. Use: pending, in_progress, completed"
                )

        return ToolResult.success_result({
            "task_id": task_id,
            "task": task.to_dict(),
            "all_tasks": self.state.get_all_tasks(),
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "ID of the task to update (e.g., '1', '2')",
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "completed"],
                    "description": "New status for the task",
                },
                "title": {
                    "type": "string",
                    "description": "Task title (used if auto-creating)",
                },
                "description": {
                    "type": "string",
                    "description": "Task description (used if auto-creating)",
                },
            },
            required=["task_id"],
        )


class AskChoiceQuestionsTool(TaskManagementTool):
    """Ask the user questions with predefined choices. User can always select 'Other' for free-text."""

    name = "ask_choice_questions"
    description = """Ask the user questions when you need clarification or decisions.

USE THIS WHEN:
- You need to gather user preferences or requirements
- You need to clarify ambiguous instructions
- You found multiple valid approaches and need user preference
- The choice requires user input (not a technical decision you can make)

CONSTRAINTS:
- 1-4 questions per call
- Each question must have 2-4 options with labels and descriptions
- Only use AFTER exploring - options should be informed by what you discovered
- User can always select "Other" to provide custom text input

EXAMPLE:
```python
ask_choice_questions(
    questions=[
        {
            "question": "Which caching strategy should we use?",
            "header": "Caching",
            "options": [
                {"label": "Redis", "description": "Found in services/cache.py - distributed, fast"},
                {"label": "Local LRU", "description": "Found in utils/lru.py - simple, per-instance"}
            ],
            "multiSelect": False
        },
        {
            "question": "Which features should be included?",
            "header": "Features",
            "options": [
                {"label": "Logging", "description": "Add structured logging"},
                {"label": "Metrics", "description": "Add prometheus metrics"},
                {"label": "Tracing", "description": "Add OpenTelemetry tracing"}
            ],
            "multiSelect": True
        }
    ]
)
```"""

    def execute(
        self,
        questions: list[dict],
    ) -> ToolResult:
        """Ask the user questions with predefined choices.

        Args:
            questions: List of questions, each with:
                - question: The question text (should end with ?)
                - header: Short label for UI display (max 12 chars)
                - options: 2-4 options, each with label and description
                - multiSelect: Whether user can select multiple options (default False)

        Returns:
            ToolResult indicating questions were set
        """
        if not questions:
            return ToolResult.error_result("At least one question is required")

        if len(questions) > 4:
            return ToolResult.error_result("Maximum 4 questions allowed per call")

        # Validate and convert questions
        choice_questions = []
        for i, q in enumerate(questions):
            question_text = q.get("question", "").strip()
            if not question_text:
                return ToolResult.error_result(f"Question {i+1} missing question text")

            header = q.get("header", "").strip()
            if not header:
                # Generate header from first word of question
                header = question_text.split()[0][:12] if question_text else "Choice"
            elif len(header) > 12:
                header = header[:12]

            options = q.get("options", [])
            if len(options) < 2:
                return ToolResult.error_result(
                    f"Question {i+1} needs at least 2 options"
                )
            if len(options) > 4:
                return ToolResult.error_result(
                    f"Question {i+1} has too many options (max 4)"
                )

            multi_select = q.get("multiSelect", False)

            # Validate each option has label and description
            validated_options = []
            for j, opt in enumerate(options):
                if isinstance(opt, str):
                    # Simple string option - convert to dict
                    validated_options.append({
                        "label": opt,
                        "description": "",
                    })
                elif isinstance(opt, dict):
                    label = opt.get("label", "").strip()
                    if not label:
                        return ToolResult.error_result(
                            f"Question {i+1}, option {j+1} missing label"
                        )
                    validated_options.append({
                        "label": label,
                        "description": opt.get("description", "").strip(),
                    })
                else:
                    return ToolResult.error_result(
                        f"Question {i+1}, option {j+1} invalid format"
                    )

            choice_questions.append(ChoiceQuestion(
                question=question_text,
                header=header,
                options=validated_options,
                multi_select=multi_select,
            ))

        # Store in state
        self.state.set_pending_choices(choice_questions, "questions")

        return ToolResult.success_result({
            "questions": [q.to_dict() for q in choice_questions],
            "status": "awaiting_choices",
            "message": "Questions will be shown to user. User can select options or choose 'Other' for custom input.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "questions": {
                    "type": "array",
                    "description": "1-4 questions to ask the user",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The complete question to ask (should end with ?)",
                            },
                            "header": {
                                "type": "string",
                                "description": "Short label displayed as chip/tag (max 12 chars). E.g., 'Auth method', 'Library'",
                            },
                            "options": {
                                "type": "array",
                                "description": "2-4 available choices. User can always select 'Other' for custom input.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "label": {
                                            "type": "string",
                                            "description": "Display text for this option (1-5 words)",
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "Explanation of what this option means or what will happen if chosen",
                                        },
                                    },
                                    "required": ["label", "description"],
                                },
                                "minItems": 2,
                                "maxItems": 4,
                            },
                            "multiSelect": {
                                "type": "boolean",
                                "description": "Allow multiple selections (default false). Use when choices are not mutually exclusive.",
                                "default": False,
                            },
                        },
                        "required": ["question", "header", "options"],
                    },
                    "minItems": 1,
                    "maxItems": 4,
                },
            },
            required=["questions"],
        )


class RequestBrowserHandoffTool(TaskManagementTool):
    """Request the user to take control of a shared browser session.

    Use this when the agent encounters a situation in a Browserbase browser
    session that requires human involvement, such as:
    - CAPTCHAs or verification challenges
    - Password entry or login forms
    - Two-factor authentication (2FA/MFA)
    - Cookie consent or age verification dialogs
    - Rate limiting that requires manual waiting
    - Any interactive element the agent cannot handle
    """

    name = "request_browser_handoff"
    description = """Request the user to take control of a shared Browserbase browser session.

USE THIS WHEN you hit a blocker in the browser that requires human action:
- CAPTCHA or bot verification
- Password/login forms (never handle credentials yourself)
- Two-factor authentication (2FA, MFA, SMS codes)
- Cookie consent or age verification
- Rate limiting (429 errors) that need manual retry
- OAuth authorization flows
- Any interactive challenge you cannot automate

The user will receive the Live View URL to interact with the browser directly.
After they complete the required action, they'll signal you to resume.

EXAMPLE:
```python
request_browser_handoff(
    reason="CAPTCHA detected on login page - need human to solve it",
    session_id="abc-123",
    live_view_url="https://www.browserbase.com/sessions/abc-123"
)
```"""

    def execute(
        self,
        reason: str,
        session_id: str = "",
        live_view_url: str = "",
        **kwargs,
    ) -> ToolResult:
        """Request user to take control of browser session.

        Args:
            reason: Why the handoff is needed (shown to user)
            session_id: Browserbase session ID
            live_view_url: Live View URL for the user to access

        Returns:
            ToolResult indicating handoff was requested (pauses agent loop)
        """
        if not reason or not reason.strip():
            return ToolResult.error_result("A reason for the handoff is required")

        # Build the handoff question for the user
        handoff_message = f"🔄 **Browser Handoff Requested**\n\n{reason.strip()}"
        if live_view_url:
            handoff_message += f"\n\n**Live View URL**: {live_view_url}"
        handoff_message += "\n\nPlease take control of the browser session, complete the required action, then select an option below."

        # Use the choice questions mechanism to pause and wait for user
        choice_questions = [ChoiceQuestion(
            question=handoff_message,
            header="Handoff",
            options=[
                {"label": "Done", "description": "I've completed the required action in the browser. Resume automation."},
                {"label": "Skip", "description": "Skip this step and continue without completing it."},
                {"label": "Cancel", "description": "Cancel the browser session entirely."},
            ],
            multi_select=False,
        )]

        self.state.set_pending_choices(choice_questions, "browser_handoff")

        return ToolResult.success_result({
            "status": "awaiting_choices",
            "questions": [q.to_dict() for q in choice_questions],
            "context": "browser_handoff",
            "reason": reason.strip(),
            "session_id": session_id,
            "live_view_url": live_view_url,
            "message": "Handoff requested. Waiting for user to complete the action in the browser.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "reason": {
                    "type": "string",
                    "description": "Why the handoff is needed (e.g., 'CAPTCHA detected', 'Login required', '2FA prompt')",
                },
                "session_id": {
                    "type": "string",
                    "description": "The Browserbase session ID (from browserbase_session_create result)",
                },
                "live_view_url": {
                    "type": "string",
                    "description": "The Live View URL for the user to access the browser (from browserbase_session_create result)",
                },
            },
            required=["reason"],
        )


class AttemptCompletionTool(TaskManagementTool):
    """Signal task completion with summary."""

    name = "attempt_completion"
    description = "Signal that the task is complete. Provide a summary of what was accomplished and list files that were modified."

    def execute(
        self,
        summary: str,
        files_modified: list[str] = None,
    ) -> ToolResult:
        """Signal task completion.

        Args:
            summary: Summary of what was accomplished
            files_modified: List of files that were modified

        Returns:
            ToolResult with completion info
        """
        if not summary or not summary.strip():
            return ToolResult.error_result("Summary is required")

        self.state.mark_completed(summary.strip())

        # Count completed vs total tasks
        completed = sum(1 for t in self.state.tasks if t.status == TaskStatus.COMPLETED)
        total = len(self.state.tasks)

        return ToolResult.success_result({
            "status": "completed",
            "summary": summary,
            "files_modified": files_modified or [],
            "tasks_completed": f"{completed}/{total}" if total > 0 else "No subtasks",
            "message": "Task marked as complete. Agent loop will terminate.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "summary": {
                    "type": "string",
                    "description": "Summary of what was accomplished",
                },
                "files_modified": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths that were modified",
                },
            },
            required=["summary"],
        )


# ─────────────────────────────────────────────────────────────
# Tasks v2 Tools (file-based, cross-session)
# ─────────────────────────────────────────────────────────────


class ClaimTodoTool(TaskManagementTool):
    """Claim a todo to work on it (Tasks v2 only)."""

    name = "claim_todo"
    description = """Claim a todo before starting work on it.

A todo can only be claimed if:
- It's not already claimed by another session
- All its dependencies are completed

Example: claim_todo(todo_id="todo-abc123")
"""

    def execute(self, todo_id: str, **kwargs) -> ToolResult:
        """Claim a todo.

        Args:
            todo_id: ID of the todo to claim

        Returns:
            ToolResult with claim status
        """
        try:
            from emdash_core.tasks import is_tasks_v2_enabled, get_current_task_list, get_session_id
            from emdash_core.tasks.store import TaskStore

            if not is_tasks_v2_enabled():
                return ToolResult.error_result(
                    "Tasks v2 not enabled. Set experimental.tasks_v2: true in emdash.config.json"
                )

            store = TaskStore()
            task_list_id = get_current_task_list()
            session_id = get_session_id()

            success, message = store.claim_task(task_list_id, todo_id, session_id)

            if success:
                todo = store.get_task(task_list_id, todo_id)
                return ToolResult.success_result({
                    "todo_id": todo_id,
                    "title": todo.title,
                    "labels": todo.labels,
                    "status": "claimed",
                    "message": message,
                })
            else:
                # Include blocking info if blocked
                blocking = store.get_blocking_tasks(task_list_id, todo_id)
                return ToolResult.error_result({
                    "message": message,
                    "blocking_todos": [
                        {"id": t.id, "title": t.title, "status": t.status.value, "claimed_by": t.claimed_by}
                        for t in blocking
                    ] if blocking else [],
                })

        except ImportError:
            return ToolResult.error_result("Tasks v2 module not available")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "todo_id": {
                    "type": "string",
                    "description": "ID of the todo to claim",
                },
            },
            required=["todo_id"],
        )


class CompleteTodoTool(TaskManagementTool):
    """Mark a claimed todo as completed (Tasks v2 only)."""

    name = "complete_todo"
    description = """Mark a todo as completed. You must have claimed it first."""

    def execute(self, todo_id: str, **kwargs) -> ToolResult:
        """Complete a todo.

        Args:
            todo_id: ID of the todo to complete

        Returns:
            ToolResult with completion status
        """
        try:
            from emdash_core.tasks import is_tasks_v2_enabled, get_current_task_list, get_session_id
            from emdash_core.tasks.store import TaskStore

            if not is_tasks_v2_enabled():
                return ToolResult.error_result(
                    "Tasks v2 not enabled. Set experimental.tasks_v2: true in emdash.config.json"
                )

            store = TaskStore()
            task_list_id = get_current_task_list()
            session_id = get_session_id()

            success, message = store.complete_task(task_list_id, todo_id, session_id)

            if success:
                return ToolResult.success_result({
                    "todo_id": todo_id,
                    "status": "completed",
                    "message": message,
                })
            else:
                return ToolResult.error_result(message)

        except ImportError:
            return ToolResult.error_result("Tasks v2 module not available")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "todo_id": {
                    "type": "string",
                    "description": "ID of the todo to complete",
                },
            },
            required=["todo_id"],
        )


class GetClaimableTodosTool(TaskManagementTool):
    """Get todos that can be claimed, optionally filtered by labels (Tasks v2 only)."""

    name = "get_claimable_todos"
    description = """Get todos that are ready to be claimed.

Optionally filter by labels to find relevant work:
- get_claimable_todos(labels=["backend"])  # Only backend todos
- get_claimable_todos(labels=["frontend", "ui"])  # Frontend/UI todos
- get_claimable_todos()  # All available todos
"""

    def execute(self, labels: list[str] = None, **kwargs) -> ToolResult:
        """Get claimable todos.

        Args:
            labels: Optional labels to filter by

        Returns:
            ToolResult with list of claimable todos
        """
        try:
            from emdash_core.tasks import is_tasks_v2_enabled, get_current_task_list
            from emdash_core.tasks.store import TaskStore

            if not is_tasks_v2_enabled():
                return ToolResult.error_result(
                    "Tasks v2 not enabled. Set experimental.tasks_v2: true in emdash.config.json"
                )

            store = TaskStore()
            task_list_id = get_current_task_list()

            todos = store.get_claimable_tasks(task_list_id, labels=labels)

            return ToolResult.success_result({
                "todo_list": task_list_id,
                "count": len(todos),
                "filter_labels": labels,
                "todos": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "labels": t.labels,
                        "depends_on": t.depends_on,
                        "priority": t.priority,
                    }
                    for t in todos
                ],
            })

        except ImportError:
            return ToolResult.error_result("Tasks v2 module not available")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels to filter by (todos must have at least one matching label)",
                },
            },
            required=[],
        )


class GetTodosByLabelsTool(TaskManagementTool):
    """Get all todos matching given labels (Tasks v2 only)."""

    name = "get_todos_by_labels"
    description = """Get todos matching specific labels.

Examples:
- get_todos_by_labels(labels=["backend"])  # Todos with 'backend' label
- get_todos_by_labels(labels=["api", "auth"], match_all=True)  # Must have BOTH labels
"""

    def execute(self, labels: list[str], match_all: bool = False, **kwargs) -> ToolResult:
        """Get todos by labels.

        Args:
            labels: Labels to filter by
            match_all: If True, todo must have ALL labels. If False, ANY label matches.

        Returns:
            ToolResult with matching todos grouped by status
        """
        try:
            from emdash_core.tasks import is_tasks_v2_enabled, get_current_task_list
            from emdash_core.tasks.store import TaskStore

            if not is_tasks_v2_enabled():
                return ToolResult.error_result(
                    "Tasks v2 not enabled. Set experimental.tasks_v2: true in emdash.config.json"
                )

            store = TaskStore()
            task_list_id = get_current_task_list()

            todos = store.get_tasks_by_labels(task_list_id, labels, match_all=match_all)

            # Group by status
            by_status = {"pending": [], "in_progress": [], "completed": [], "blocked": []}
            for t in todos:
                status_key = t.status.value
                by_status.get(status_key, by_status["pending"]).append({
                    "id": t.id,
                    "title": t.title,
                    "labels": t.labels,
                    "claimed_by": t.claimed_by,
                })

            return ToolResult.success_result({
                "todo_list": task_list_id,
                "filter_labels": labels,
                "match_all": match_all,
                "total": len(todos),
                "by_status": by_status,
            })

        except ImportError:
            return ToolResult.error_result("Tasks v2 module not available")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels to filter by",
                },
                "match_all": {
                    "type": "boolean",
                    "description": "If true, todo must have ALL labels. Default: false (ANY label matches)",
                    "default": False,
                },
            },
            required=["labels"],
        )


class WaitForTodoTool(TaskManagementTool):
    """Wait for a todo to complete (Tasks v2 only)."""

    name = "wait_for_todo"
    description = """Wait for a blocking todo to complete before continuing.
This PAUSES your execution until the todo is done.

Use when you need to work on a todo that's blocked by
another todo being worked on by a different session.

Example: wait_for_todo(todo_id="todo-abc123", timeout_seconds=300)
"""

    async def execute(self, todo_id: str, timeout_seconds: float = 300, **kwargs) -> ToolResult:
        """Wait for a todo to complete.

        Args:
            todo_id: ID of the todo to wait for
            timeout_seconds: Maximum seconds to wait (default 300)

        Returns:
            ToolResult with wait status
        """
        try:
            from emdash_core.tasks import (
                is_tasks_v2_enabled,
                get_current_task_list,
                TaskWaiter,
            )
            from emdash_core.tasks.store import TaskStore
            from emdash_core.tasks.models import TaskStatus

            if not is_tasks_v2_enabled():
                return ToolResult.error_result(
                    "Tasks v2 not enabled. Set experimental.tasks_v2: true in emdash.config.json"
                )

            store = TaskStore()
            task_list_id = get_current_task_list()

            # Check if already complete
            todo = store.get_task(task_list_id, todo_id)
            if not todo:
                return ToolResult.error_result(f"Todo '{todo_id}' not found")

            if todo.status == TaskStatus.COMPLETED:
                return ToolResult.success_result({
                    "status": "already_completed",
                    "todo": {"id": todo.id, "title": todo.title},
                })

            if not todo.claimed_by:
                return ToolResult.error_result({
                    "status": "not_started",
                    "message": f"Todo '{todo.title}' is not being worked on. "
                              "Claim it yourself or wait for another agent to start.",
                })

            # Actually wait
            completed = await TaskWaiter.wait_for_task(
                task_id=todo_id,
                timeout=timeout_seconds,
            )

            if completed:
                todo = store.get_task(task_list_id, todo_id)
                return ToolResult.success_result({
                    "status": "completed",
                    "todo": {"id": todo.id, "title": todo.title},
                    "message": f"Todo '{todo.title}' is now complete!",
                })
            else:
                return ToolResult.error_result({
                    "status": "timeout",
                    "message": f"Timed out after {timeout_seconds}s waiting for '{todo.title}'",
                })

        except ImportError:
            return ToolResult.error_result("Tasks v2 module not available")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "todo_id": {
                    "type": "string",
                    "description": "ID of the todo to wait for",
                },
                "timeout_seconds": {
                    "type": "number",
                    "description": "Maximum seconds to wait (default 300)",
                    "default": 300,
                },
            },
            required=["todo_id"],
        )


class ReleaseTodoTool(TaskManagementTool):
    """Release a claimed todo back to pending (Tasks v2 only)."""

    name = "release_todo"
    description = """Release a todo you claimed back to pending status.
Use this if you can't complete a todo and want to let another agent claim it."""

    def execute(self, todo_id: str, **kwargs) -> ToolResult:
        """Release a todo.

        Args:
            todo_id: ID of the todo to release

        Returns:
            ToolResult with release status
        """
        try:
            from emdash_core.tasks import is_tasks_v2_enabled, get_current_task_list, get_session_id
            from emdash_core.tasks.store import TaskStore

            if not is_tasks_v2_enabled():
                return ToolResult.error_result(
                    "Tasks v2 not enabled. Set experimental.tasks_v2: true in emdash.config.json"
                )

            store = TaskStore()
            task_list_id = get_current_task_list()
            session_id = get_session_id()

            success, message = store.release_task(task_list_id, todo_id, session_id)

            if success:
                return ToolResult.success_result({
                    "todo_id": todo_id,
                    "status": "released",
                    "message": message,
                })
            else:
                return ToolResult.error_result(message)

        except ImportError:
            return ToolResult.error_result("Tasks v2 module not available")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "todo_id": {
                    "type": "string",
                    "description": "ID of the todo to release",
                },
            },
            required=["todo_id"],
        )
