from pydantic import BaseModel
from temporalio.exceptions import ActivityError, ApplicationError

from mistralai.workflows import activity, workflow
from mistralai.workflows.core.execution.local_activity import run_activities_locally
from mistralai.workflows.core.task import task
from mistralai.workflows.models import EncryptedStrField

SECRET = "s3cret-content"
PUBLIC = "public-envelope"


class TaskState(BaseModel):
    public: str
    secret: EncryptedStrField


async def _run_content_task(task_type: str) -> None:
    async with task(task_type, state=TaskState(public=PUBLIC, secret=EncryptedStrField(data=SECRET))) as t:
        # Prefixes, not suffixes: the JSON patch must carry the full values (suffixes become append ops).
        await t.set_state(TaskState(public=f"updated-{PUBLIC}", secret=EncryptedStrField(data=f"updated-{SECRET}")))


@activity(name="full_encryption_with_task")
async def with_task(text: str) -> str:
    await _run_content_task("activity_content_task")
    return f"{text}-result"


@workflow.define(name="full-encryption-task")
class TaskWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        # Workflow-side tasks publish their events through local activities.
        await _run_content_task("workflow_content_task")
        return await with_task(SECRET)


@activity(name="full_encryption_fail", retry_policy_max_attempts=1)
async def fail(text: str) -> None:
    raise ValueError(f"{SECRET} {text}")


class FailureInput(BaseModel):
    run_locally: bool
    catch: bool


@workflow.define(name="full-encryption-failure")
class FailureWorkflow:
    @workflow.entrypoint
    async def run(self, params: FailureInput) -> str:
        if params.run_locally:
            with run_activities_locally():
                return await self._fail(params.catch)
        return await self._fail(params.catch)

    async def _fail(self, catch: bool) -> str:
        try:
            await fail("from-activity")
        except (ActivityError, ApplicationError) as e:
            if not catch:
                raise
            return str(e.cause) if isinstance(e, ActivityError) else str(e)
        return "unreachable"


@workflow.define(name="full-encryption-workflow-failure")
class WorkflowFailureWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        raise ApplicationError(f"{SECRET} from-workflow", type="ContentError", non_retryable=True)


@workflow.define(name="full-encryption-task-failure")
class TaskFailureWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        async with task("failing_task", state={"step": "running"}):
            raise ApplicationError(f"{SECRET} from-task", type="ContentError", non_retryable=True)
