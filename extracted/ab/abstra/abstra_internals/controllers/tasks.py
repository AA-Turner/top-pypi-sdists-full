from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple

from abstra_internals.interface.sdk import user_exceptions
from abstra_internals.repositories.factory import Repositories
from abstra_internals.repositories.tasks import TaskDTO
from abstra_internals.utils.datetime import from_utc_iso_string


@dataclass
class DataRequestFilter:
    stage: Optional[List[str]]
    status: Optional[List[str]]
    start_date: Optional[str]
    end_date: Optional[str]

    @staticmethod
    def from_dict(data: dict) -> "DataRequestFilter":
        return DataRequestFilter(
            stage=data.get("stage", None),
            status=data.get("status", None),
            start_date=data.get("startDate", None),
            end_date=data.get("endDate", None),
        )

    def to_dict(self) -> dict:
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)


@dataclass
class DataRequest:
    filter: DataRequestFilter
    limit: int
    offset: int

    @staticmethod
    def from_dict(data: dict) -> "DataRequest":
        return DataRequest(
            filter=DataRequestFilter.from_dict(data.get("filter", {})),
            limit=data.get("limit", 10),
            offset=data.get("offset", 0),
        )

    def to_dict(self) -> dict:
        return dict((k, v) for k, v in self.__dict__.items() if v is not None)


class ListTasksItem(TaskDTO):
    target_stage_title: str
    target_stage_type: str
    source_stage_title: Optional[str]
    source_stage_type: Optional[str]


class TasksController:
    def __init__(
        self,
        repositories: Repositories,
    ) -> None:
        self.repos = repositories

    def get_stage(self, stage_id: str):
        project = self.repos.project.load(include_disabled_stages=True)
        stage = project.get_stage(stage_id)

        if not stage:
            raise Exception(f"Stage {stage_id} not found")

        return {
            "title": stage.title,
            "type_name": "tasklet" if stage.type_name == "script" else stage.type_name,
        }

    def get_nullable_stage(self, stage_id: Optional[str]):
        if not stage_id:
            return {
                "title": None,
                "type_name": None,
            }
        return self.get_stage(stage_id)

    def _list_all_tasks(
        self, req: Optional[DataRequest] = None
    ) -> Tuple[List[ListTasksItem], int]:
        """
        Private helper for `list_tasks`. Returns enriched tasks plus the
        unpaginated total, filtered by stage, status, and date range from `req`.
        """
        project = self.repos.project.load(include_disabled_stages=True)
        valid_stage_ids = {stage.id for stage in project.workflow_stages}

        items = []
        for task in self.repos.tasks.get_all_tasks():
            # Skip tasks with deleted target stages
            if task.target_stage_id not in valid_stage_ids:
                continue
            if (
                req
                and req.filter.stage
                and task.target_stage_id not in req.filter.stage
            ):
                continue
            if req and req.filter.status and task.status not in req.filter.status:
                continue
            if req and (
                req.filter.start_date
                and from_utc_iso_string(task.created.at)
                < from_utc_iso_string(req.filter.start_date)
            ):
                continue
            if req and (
                req.filter.end_date
                and from_utc_iso_string(task.created.at)
                > from_utc_iso_string(req.filter.end_date)
            ):
                continue

            target_stage = self.get_stage(task.target_stage_id)
            source_stage = self.get_nullable_stage(task.created.by_stage_id)

            items.append(
                ListTasksItem(
                    **task.dump(),
                    target_stage_type=target_stage["type_name"],
                    target_stage_title=target_stage["title"],
                    source_stage_type=source_stage["type_name"],
                    source_stage_title=source_stage["title"],
                )
            )

        if not req:
            return items, len(items)

        return items[req.offset : req.offset + req.limit], len(items)

    def _list_tasks_sent_to_stage(self, stage_id) -> List[ListTasksItem]:
        """
        Private helper for `list_tasks(direction='sent_to')`. Returns tasks
        targeted to the given stage, sorted newest-first, enriched with
        source/target stage info. Raises if `stage_id` is unknown.
        """
        target_stage = self.get_stage(stage_id)
        tasks = self.repos.tasks.get_stage_tasks(stage_id)

        tasks.sort(
            key=lambda task: from_utc_iso_string(task.created.at),
            reverse=True,
        )

        if not target_stage["title"]:
            raise Exception(f"Stage {stage_id} not found")

        return [
            ListTasksItem(
                **task.dump(),
                target_stage_title=target_stage["title"],
                target_stage_type=target_stage["type_name"],
                source_stage_title=self.get_nullable_stage(task.created.by_stage_id)[
                    "title"
                ],
                source_stage_type=self.get_nullable_stage(task.created.by_stage_id)[
                    "type_name"
                ],
            )
            for task in tasks
        ]

    def _list_tasks_sent_by_stage(self, stage_id) -> List[ListTasksItem]:
        """
        Private helper for `list_tasks(direction='sent_by')`. Returns tasks
        whose originating execution belongs to the given stage, sorted
        newest-first, enriched with source/target stage info.
        """
        all_tasks, _ = self._list_all_tasks()
        tasks_with_executions = [
            (task, self.repos.execution.get(task.created.by_execution_id))
            for task in all_tasks
            if task.created.by_execution_id is not None
        ]

        tasks_with_executions.sort(
            key=lambda task: from_utc_iso_string(task[0].created.at),
            reverse=True,
        )

        return [
            ListTasksItem(
                **task.dump(),
                target_stage_title=task.target_stage_title,
                target_stage_type=task.target_stage_title,
                source_stage_title=self.get_nullable_stage(task.created.by_stage_id)[
                    "title"
                ],
                source_stage_type=self.get_nullable_stage(task.created.by_stage_id)[
                    "type_name"
                ],
            )
            for task, execution in tasks_with_executions
            if execution and execution.stage_id == stage_id
        ]

    def update_task_status(self, task_id: str, status: str) -> None:
        """
        Update the status of an existing task.

        This method allows manual control over task lifecycle by changing task status.
        It's useful for task management, workflow control, and handling exceptional cases.

        Args:
            task_id (str): Unique identifier of the task to update.
            status (str): New status for the task. Valid values:
                - 'completed': Mark task as completed without execution
                - 'pending': Reset task to pending status for re-execution

        Raises:
            TaskInvalidStatus: If an invalid status value is provided.

        Example:
            ```python
            controller = TasksController(repositories)

            # Mark a task as completed (skip execution)
            try:
                controller.update_task_status("task-123", "completed")
                print("Task marked as completed")
            except Exception as e:
                print(f"Failed to update task: {e}")

            # Reset a task to pending status
            controller.update_task_status("task-456", "pending")
            print("Task reset to pending - will be re-executed")

            # Invalid status will raise an exception
            try:
                controller.update_task_status("task-789", "invalid_status")
            except TaskInvalidStatus as e:
                print(f"Invalid status: {e}")
            ```

        Note:
            - Completed tasks will not trigger stage execution
            - Pending tasks will be picked up by the execution engine
            - Status changes are immediate and cannot be undone
            - Use with caution as it affects workflow execution flow
            - 'locked' status is managed internally and cannot be set manually

        Copywritings:
            Update the status of a task
            Updating the status of a task...
        """
        if status == "completed":
            self.repos.tasks.complete_task(task_id, None, None)
        elif status == "pending":
            self.repos.tasks.set_task_to_pending(task_id)
        else:
            raise user_exceptions.TaskInvalidStatus(status)

    def create_task(
        self,
        name: str,
        stage_id: str,
        payload: dict,
        source_stage_id: Optional[str] = None,
        execution_id: Optional[str] = None,
    ) -> TaskDTO:
        """
        Create a new task to be executed by a specific stage.

        This method creates a task that will trigger the execution of the target stage
        with the provided payload data. Tasks are the primary mechanism for workflow
        progression and data passing between stages.

        IMPORTANT - Difference from send_task():
        - This method (create_task) sends a task DIRECTLY to a specific stage_id,
          bypassing transition-based routing.
        - In contrast, the SDK's send_task(task_type, payload) routes tasks through
          transitions based on task_type matching.
        - Use this when you need to send a task to a specific stage regardless of
          the workflow's transition configuration.

        Args:
            name (str): Type/name of the task (e.g., 'user_registration', 'data_processing').
                This becomes task.type and can be used for filtering/identification.
            stage_id (str): Unique identifier of the target stage that will execute this task.
                The task goes directly to this stage (no transition routing).
            payload (dict): Data to be passed to the target stage when it executes.
                This data will be available to the stage during execution via task.payload.
            source_stage_id (Optional[str], optional): ID of the stage that is creating
                this task. Used for workflow tracking and debugging.
            execution_id (Optional[str], optional): ID of the execution context that
                is creating this task. Used for tracking task relationships.

        Returns:
            TaskDTO: The created task object containing all task metadata including
                assigned ID, creation timestamp, and status.

        Example:
            ```python
            controller = TasksController(repositories)

            # Create a simple task directly to a stage
            task = controller.create_task(
                name="user_signup",
                stage_id="welcome-form",
                payload={"user_email": "user@example.com", "signup_date": "2024-01-15"}
            )
            print(f"Created task {task.id} with status {task.status}")

            # Create task with source tracking
            task_with_source = controller.create_task(
                name="process_order",
                stage_id="order-processor",
                payload={"order_id": 12345, "items": ["item1", "item2"]},
                source_stage_id="order-form",
                execution_id="exec-789"
            )
            ```

        Note:
            - Tasks are created in 'pending' status and will be picked up for execution
            - The payload must be JSON-serializable
            - Target stage must exist or task creation may fail
            - This bypasses transition routing - task goes directly to stage_id
            - For transition-based routing in stage code, use send_task(task_type, payload)

        Copywritings:
            Create a new task for a stage
            Creating a new task for a stage...
        """
        task = self.repos.tasks.send_task(
            name, payload, stage_id, source_stage_id, execution_id
        )
        return task

    def clear_tasks(self) -> None:
        """
        Clear all tasks in this workflow

        This method is useful to clear all tasks from every stage.

        Copywritings:
            Clear all tasks in this workflow
            Clearing all tasks in this workflow...
        """

        self.repos.tasks.clear()

    def list_tasks(
        self,
        stage_ids: Optional[List[str]] = None,
        direction: Optional[Literal["sent_to", "sent_by"]] = None,
        status: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict:
        """
        List tasks in the workflow, with optional filtering.

        By default returns the first `limit` tasks across the whole workflow.
        Use `stage_ids` together with `direction` to narrow to tasks related to a
        specific stage:
          - direction='sent_to': tasks targeted to the stage (waiting for it).
          - direction='sent_by': tasks created by the stage during its executions.
        When `direction` is provided, `stage_ids` must contain exactly one stage.
        Without `direction`, multi-stage filtering and date-range filtering apply.

        Args:
            stage_ids: Optional list of stage IDs to filter by. When `direction`
                is set, must contain exactly one stage ID.
            direction: When combined with a single `stage_ids` entry, picks the
                relationship — 'sent_to' (incoming) or 'sent_by' (outgoing).
                Ignored when `stage_ids` is None.
            status: Optional list of statuses to include
                (e.g. ['pending', 'locked', 'completed']).
            start_date: Optional ISO date string for earliest creation date.
            end_date: Optional ISO date string for latest creation date.
            limit: Page size when paginated. Defaults to 10.
            offset: Pagination offset. Defaults to 0.

        Returns:
            dict: {'tasks': list of ListTasksItem, 'total': int}. For the
                'sent_to' / 'sent_by' modes `total` equals the length of the
                returned list (no pagination is applied).

        Copywritings:
            List tasks
            Listing tasks...
        """
        if direction is not None:
            if stage_ids is None or len(stage_ids) != 1:
                raise ValueError("direction requires exactly one stage in `stage_ids`")
            stage_id = stage_ids[0]
            if direction == "sent_to":
                items = self._list_tasks_sent_to_stage(stage_id)
            elif direction == "sent_by":
                items = self._list_tasks_sent_by_stage(stage_id)
            else:
                raise ValueError(
                    f"Unknown direction: {direction!r}. Must be 'sent_to' or 'sent_by'."
                )
            return {"tasks": items, "total": len(items)}

        req = DataRequest(
            filter=DataRequestFilter(
                stage=stage_ids,
                status=status,
                start_date=start_date,
                end_date=end_date,
            ),
            limit=limit,
            offset=offset,
        )
        items, total = self._list_all_tasks(req)
        return {"tasks": items, "total": total}
