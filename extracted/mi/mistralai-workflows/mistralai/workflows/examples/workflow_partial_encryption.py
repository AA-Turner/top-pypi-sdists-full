from typing import Any

from pydantic import BaseModel, Field

import mistralai.workflows as mistralai_workflows
from mistralai.workflows.models import EncryptedStrField

with mistralai_workflows.workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)

SECRET_VALUE = "this-is-a-secret-value"


class BasePayload(BaseModel):
    """Base payload with encrypted secret field and a plain field."""

    plain_field: str = "not-secret"
    secret_key: EncryptedStrField = Field(default_factory=lambda: EncryptedStrField(data=SECRET_VALUE))


class WorkflowParam(BasePayload):
    pass


class WorkflowResult(BaseModel):
    secret_key: EncryptedStrField
    input_secret_correct: bool
    activity_input_secret_correct: bool
    activity_result_secret_correct: bool
    child_input_secret_correct: bool
    child_result_secret_correct: bool
    signal_input_secret_correct: bool
    query_input_secret_correct: bool
    update_input_secret_correct: bool


class ActivityParam(BasePayload):
    pass


class ActivityResult(BaseModel):
    secret_key: EncryptedStrField
    input_secret_key_correct: bool


class SignalParam(BasePayload):
    pass


class UpdateParam(BasePayload):
    pass


class UpdateResult(BaseModel):
    secret_key: EncryptedStrField


class QueryParam(BasePayload):
    pass


class QueryResult(BaseModel):
    secret_key: EncryptedStrField


class ChildWorkflowParam(BasePayload):
    pass


class ChildWorkflowResult(BaseModel):
    secret_key: EncryptedStrField
    input_secret_correct: bool


@mistralai_workflows.activity()
async def partial_encryption_example_activity(params: ActivityParam) -> ActivityResult:
    return ActivityResult(
        secret_key=params.secret_key,
        input_secret_key_correct=params.secret_key.data == SECRET_VALUE,
    )


@mistralai_workflows.workflow.define(
    name="workflow-partial-encryption-child",
    workflow_description="Child workflow testing partial encryption",
)
class WorkflowPartialEncryptionChild:
    @mistralai_workflows.workflow.entrypoint
    async def run(self, params: ChildWorkflowParam) -> ChildWorkflowResult:
        return ChildWorkflowResult(
            secret_key=params.secret_key,
            input_secret_correct=params.secret_key.data == SECRET_VALUE,
        )


@mistralai_workflows.workflow.define(
    name="workflow-partial-encryption",
    workflow_description="Workflow testing partial encryption with EncryptedStrField",
)
class WorkflowPartialEncryption:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._stopped = False
        self._signal_input_secret: str | None = None
        self._query_input_secret: str | None = None
        self._update_input_secret: str | None = None

    @mistralai_workflows.workflow.entrypoint
    async def run(self, params: WorkflowParam) -> WorkflowResult:
        activity_result = await partial_encryption_example_activity(
            ActivityParam(plain_field=params.plain_field, secret_key=params.secret_key)
        )

        child_result = await mistralai_workflows.workflow.execute_workflow(
            WorkflowPartialEncryptionChild,
            params=ChildWorkflowParam(plain_field=params.plain_field, secret_key=params.secret_key),
        )

        await mistralai_workflows.workflow.wait_condition(lambda: self._stopped)

        return WorkflowResult(
            secret_key=params.secret_key,
            input_secret_correct=params.secret_key.data == SECRET_VALUE,
            activity_input_secret_correct=activity_result.input_secret_key_correct,
            activity_result_secret_correct=activity_result.secret_key.data == SECRET_VALUE,
            child_input_secret_correct=child_result.input_secret_correct,
            child_result_secret_correct=child_result.secret_key.data == SECRET_VALUE,
            signal_input_secret_correct=self._signal_input_secret == SECRET_VALUE,
            query_input_secret_correct=self._query_input_secret == SECRET_VALUE,
            update_input_secret_correct=self._update_input_secret == SECRET_VALUE,
        )

    @mistralai_workflows.workflow.signal(name="stop_workflow", description="Stop the workflow")
    async def stop_workflow(self, params: SignalParam) -> None:
        self._signal_input_secret = params.secret_key.data
        self._stopped = True

    @mistralai_workflows.workflow.query(name="get_secret", description="Query with encrypted input/output")
    def get_secret(self, params: QueryParam) -> QueryResult:
        self._query_input_secret = params.secret_key.data
        return QueryResult(secret_key=params.secret_key)

    @mistralai_workflows.workflow.update(name="update_secret", description="Update with encrypted input/output")
    async def update_secret(self, params: UpdateParam) -> UpdateResult:
        self._update_input_secret = params.secret_key.data
        return UpdateResult(secret_key=params.secret_key)
