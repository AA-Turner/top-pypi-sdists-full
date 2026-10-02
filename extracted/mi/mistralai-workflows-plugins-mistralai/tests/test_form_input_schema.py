from datetime import date, datetime, timezone
from typing import Any

import pytest
from pydantic import ValidationError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows import InteractiveWorkflow, workflow
from mistralai.workflows.conversational import (
    ACCEPT_OPTION_VALUE,
    DECLINE_OPTION_VALUE,
    AcceptDeclineConfirmation,
    ConfirmationInput,
    DateField,
    DateTimeField,
    FileField,
    FileWithMetadataValue,
    FormInput,
    MultiChoice,
    NumberField,
    SingleChoice,
    TextField,
    is_accepted,
)
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.testing import (
    create_capturing_mock_events_client,
    create_test_worker_with_events,
    wait_for_pending_inputs,
)


class BasicTextForm(FormInput):
    name: str = TextField(description="Enter your name")


class TextFormWithPattern(FormInput):
    email: str = TextField(
        description="Email address",
        pattern=r"^[\w.-]+@[\w.-]+\.\w+$",
    )


class NumberFormWithBounds(FormInput):
    amount: float = NumberField(
        description="Amount in USD",
        minimum=0,
        maximum=10000,
    )


class DateTimeForm(FormInput):
    scheduled_at: datetime = DateTimeField(description="Schedule date and time")


class DateForm(FormInput):
    scheduled_at: date = DateField(description="Scheduled date")


class SingleChoiceForm(FormInput):
    priority: str = SingleChoice(
        options=[
            ("low", "Low Priority"),
            ("medium", "Medium Priority"),
            ("high", "High Priority"),
        ],
        description="Select priority level",
    )


class MultiChoiceForm(FormInput):
    tags: list[str] = MultiChoice(
        options=[
            ("frontend", "Frontend"),
            ("backend", "Backend"),
            ("infra", "Infrastructure"),
        ],
        description="Select applicable tags",
    )


class SingleFileForm(FormInput):
    document: str = FileField(description="Upload a document")


class MultiFileForm(FormInput):
    attachments: list[str] = FileField(description="Upload files", multiple=True)


class CompleteRFCForm(FormInput):
    title: str = TextField(description="RFC title", pattern=r"^RFC.*")
    summary: str = TextField(description="Brief summary")
    priority: str = SingleChoice(
        options=[
            ("low", "Low Priority"),
            ("high", "High Priority"),
        ],
        description="Priority level",
    )
    estimated_effort: float = NumberField(
        description="Effort in person-days",
        minimum=1,
        maximum=365,
    )


class FormWithInitialValues(FormInput):
    """Form with initial values for testing (UI hints only, fields remain required)."""

    name: str = TextField(description="Your name", prefilled_value="John Doe")
    email: str = TextField(description="Email", pattern=r"^[\w.-]+@[\w.-]+\.\w+$", prefilled_value="user@example.com")
    age: float = NumberField(description="Your age", prefilled_value=25.0)
    amount: float = NumberField(description="Amount", minimum=0, maximum=100, prefilled_value=50.0)
    price: float = NumberField(description="Price", exclusive_minimum=0, exclusive_maximum=1000, prefilled_value=99.99)
    priority: str = SingleChoice(
        options=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        description="Priority",
        prefilled_value="medium",
    )
    tags: list[str] = MultiChoice(
        options=[("frontend", "Frontend"), ("backend", "Backend"), ("infra", "Infra")],
        description="Tags",
        prefilled_value=["frontend"],
    )
    tags_deduped: list[str] = MultiChoice(
        options=[("frontend", "Frontend"), ("backend", "Backend"), ("infra", "Infra")],
        description="Tags with duplicates",
        prefilled_value=["frontend", "backend", "frontend"],
    )
    scheduled_at: datetime = DateTimeField(
        description="Schedule time", prefilled_value=datetime(2023, 1, 1, tzinfo=timezone.utc)
    )
    scheduled_at_str: datetime = DateTimeField(
        description="Schedule time from string", prefilled_value="2023-06-15T12:30:00Z"
    )
    scheduled_date: date = DateField(description="Schedule date", prefilled_value=date(2023, 1, 1))
    scheduled_date_str: date = DateField(description="Schedule date from string", prefilled_value="2023-06-15")


@workflow.define(name="basic_text_form_workflow")
class BasicTextFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(BasicTextForm, label="Basic Text Form")
        return {"name": form_input.name}


@workflow.define(name="text_pattern_form_workflow")
class TextPatternFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(TextFormWithPattern, label="Email Form")
        return {"email": form_input.email}


@workflow.define(name="number_form_workflow")
class NumberFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(NumberFormWithBounds, label="Amount Form")
        return {"amount": form_input.amount}


@workflow.define(name="datetime_form_workflow")
class DateTimeFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(DateTimeForm, label="Schedule Form")
        return {"scheduled_at": form_input.scheduled_at.isoformat()}


@workflow.define(name="date_form_workflow")
class DateFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(DateForm, label="Schedule date Form")
        return {"scheduled_at": form_input.scheduled_at.isoformat()}


@workflow.define(name="single_choice_form_workflow")
class SingleChoiceFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(SingleChoiceForm, label="Priority Form")
        return {"priority": form_input.priority}


@workflow.define(name="multi_choice_form_workflow")
class MultiChoiceFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(MultiChoiceForm, label="Tags Form")
        return {"tags": form_input.tags}


@workflow.define(name="single_file_form_workflow")
class SingleFileFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(SingleFileForm, label="File Upload")
        return {"document": form_input.document}


@workflow.define(name="multi_file_form_workflow")
class MultiFileFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(MultiFileForm, label="Files Upload")
        return {"attachments": form_input.attachments}


class SingleFileWithMetadataForm(FormInput):
    document: FileWithMetadataValue = FileField(description="Upload a document", include_metadata=True)


class MultiFileWithMetadataForm(FormInput):
    attachments: list[FileWithMetadataValue] = FileField(
        description="Upload files", multiple=True, include_metadata=True
    )


@workflow.define(name="single_file_with_metadata_form_workflow")
class SingleFileWithMetadataFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(SingleFileWithMetadataForm, label="File With Metadata Upload")
        return {"filename": form_input.document.filename, "url": form_input.document.url}


@workflow.define(name="multi_file_with_metadata_form_workflow")
class MultiFileWithMetadataFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(MultiFileWithMetadataForm, label="Files With Metadata Upload")
        return {"attachments": [{"filename": a.filename, "url": a.url} for a in form_input.attachments]}


@workflow.define(name="accept_decline_step_workflow")
class AcceptDeclineStepWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(
            AcceptDeclineConfirmation(accept_label="Yes", decline_label="No", description="Do you accept?")
        )
        return {"choice": form_input.choice}


@workflow.define(name="confirmation_step_workflow")
class ConfirmationStepWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(
            ConfirmationInput(
                options=[("option-a", "Option A"), ("option-b", "Option B"), ("option-c", "Option C")],
                description="Choose an option",
            )
        )
        return {"choice": form_input.choice}


@workflow.define(name="complete_rfc_form_workflow")
class CompleteRFCFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(CompleteRFCForm, label="RFC Feedback Form")
        return {
            "title": form_input.title,
            "summary": form_input.summary,
            "priority": form_input.priority,
            "estimated_effort": form_input.estimated_effort,
        }


@workflow.define(name="prefilled_values_form_workflow")
class InitialValuesFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(FormWithInitialValues, label="Initial Values Form")
        return {"name": form_input.name}


def extract_input_schema_from_events(captured_events: list[Any]) -> dict[str, Any] | None:
    for event in captured_events:
        if (
            hasattr(event, "event_type")
            and event.event_type.value == "CUSTOM_TASK_STARTED"
            and hasattr(event, "attributes")
            and event.attributes.custom_task_type == "wait_for_input"
        ):
            return event.attributes.payload.value.get("input_schema")
    return None


def extract_label_from_events(captured_events: list[Any]) -> str | None:
    for event in captured_events:
        if (
            hasattr(event, "event_type")
            and event.event_type.value == "CUSTOM_TASK_STARTED"
            and hasattr(event, "attributes")
            and event.attributes.custom_task_type == "wait_for_input"
        ):
            return event.attributes.payload.value.get("label")
    return None


@pytest.mark.asyncio
async def test_text_field_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[BasicTextFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "basic_text_form_workflow",
                id="test-text-field-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"name": "John Doe"}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    assert input_schema["type"] == "object"
    assert "properties" in input_schema

    name_schema = input_schema["properties"]["name"]
    assert name_schema["type"] == "string"
    assert name_schema["description"] == "Enter your name"


@pytest.mark.asyncio
async def test_text_field_with_pattern_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TextPatternFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "text_pattern_form_workflow",
                id="test-text-pattern-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"email": "test@example.com"}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    email_schema = input_schema["properties"]["email"]
    assert email_schema["type"] == "string"
    assert email_schema["description"] == "Email address"
    assert email_schema["pattern"] == r"^[\w.-]+@[\w.-]+\.\w+$"


@pytest.mark.asyncio
async def test_number_field_with_bounds_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[NumberFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "number_form_workflow",
                id="test-number-field-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"amount": 500.0}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    amount_schema = input_schema["properties"]["amount"]
    assert amount_schema["type"] == "number"
    assert amount_schema["description"] == "Amount in USD"
    assert amount_schema["minimum"] == 0
    assert amount_schema["maximum"] == 10000


@pytest.mark.asyncio
async def test_datetime_field_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[DateTimeFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "datetime_form_workflow",
                id="test-datetime-field-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"scheduled_at": "2025-01-15T10:30:00"}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    scheduled_schema = input_schema["properties"]["scheduled_at"]
    assert scheduled_schema["type"] == "string"
    assert scheduled_schema["format"] == "date-time"
    assert scheduled_schema["description"] == "Schedule date and time"


@pytest.mark.asyncio
async def test_date_field_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[DateFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "date_form_workflow",
                id="test-date-field-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"scheduled_at": "2025-01-15"}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    scheduled_schema = input_schema["properties"]["scheduled_at"]
    assert scheduled_schema["type"] == "string"
    assert scheduled_schema["format"] == "date"
    assert scheduled_schema["description"] == "Scheduled date"


@pytest.mark.asyncio
async def test_single_choice_field_in_event(temporal_env: WorkflowEnvironment) -> None:
    """Test that SingleChoice generates oneOf schema with const values."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SingleChoiceFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "single_choice_form_workflow",
                id="test-single-choice-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"priority": "high"}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    priority_schema = input_schema["properties"]["priority"]

    assert "oneOf" in priority_schema
    assert "type" not in priority_schema
    assert priority_schema["description"] == "Select priority level"

    one_of = priority_schema["oneOf"]
    assert len(one_of) == 3

    assert one_of[0] == {"type": "string", "const": "low", "description": "Low Priority"}
    assert one_of[1] == {"type": "string", "const": "medium", "description": "Medium Priority"}
    assert one_of[2] == {"type": "string", "const": "high", "description": "High Priority"}


@pytest.mark.asyncio
async def test_complete_rfc_form_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[CompleteRFCFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "complete_rfc_form_workflow",
                id="test-complete-form-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "title": "RFC: New Feature",
                        "summary": "A brief summary",
                        "priority": "high",
                        "estimated_effort": 10.0,
                    },
                },
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    assert input_schema["type"] == "object"
    assert input_schema["title"] == "FormInput"

    props = input_schema["properties"]

    assert props["title"]["type"] == "string"
    assert props["title"]["description"] == "RFC title"
    assert props["title"]["pattern"] == r"^RFC.*"

    assert props["summary"]["type"] == "string"
    assert props["summary"]["description"] == "Brief summary"

    assert "oneOf" in props["priority"]
    assert len(props["priority"]["oneOf"]) == 2
    assert props["priority"]["description"] == "Priority level"

    assert props["estimated_effort"]["type"] == "number"
    assert props["estimated_effort"]["minimum"] == 1
    assert props["estimated_effort"]["maximum"] == 365


@pytest.mark.asyncio
async def test_form_input_label_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[CompleteRFCFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "complete_rfc_form_workflow",
                id="test-form-label",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "title": "RFC: Test",
                        "summary": "Test",
                        "priority": "low",
                        "estimated_effort": 5.0,
                    },
                },
            )
            await handle.result()

    label = extract_label_from_events(captured_events)
    assert label == "RFC Feedback Form"


def test_text_field_pattern_validation() -> None:
    class PatternForm(FormInput):
        email: str = TextField(description="Email", pattern=r"^[\w.-]+@[\w.-]+\.\w+$")

    # Valid input should work
    valid = PatternForm(email="test@example.com")
    assert valid.email == "test@example.com"

    # Invalid input should raise ValidationError
    with pytest.raises(ValidationError):
        PatternForm(email="not-an-email")


def test_number_field_minimum_validation() -> None:
    class MinForm(FormInput):
        amount: float = NumberField(description="Amount", minimum=0)

    # Valid input at boundary
    valid = MinForm(amount=0)
    assert valid.amount == 0

    # Valid input above minimum
    valid = MinForm(amount=100)
    assert valid.amount == 100

    # Invalid input below minimum
    with pytest.raises(ValidationError):
        MinForm(amount=-1)


def test_number_field_maximum_validation() -> None:
    class MaxForm(FormInput):
        amount: float = NumberField(description="Amount", maximum=100)

    # Valid input at boundary
    valid = MaxForm(amount=100)
    assert valid.amount == 100

    # Valid input below maximum
    valid = MaxForm(amount=50)
    assert valid.amount == 50

    # Invalid input above maximum
    with pytest.raises(ValidationError):
        MaxForm(amount=101)


def test_number_field_exclusive_bounds_validation() -> None:
    class ExclusiveForm(FormInput):
        value: float = NumberField(
            description="Value",
            exclusive_minimum=0,
            exclusive_maximum=100,
        )

    valid = ExclusiveForm(value=50)
    assert valid.value == 50

    with pytest.raises(ValidationError):
        ExclusiveForm(value=0)

    with pytest.raises(ValidationError):
        ExclusiveForm(value=100)


def test_single_choice_valid_option_validation() -> None:
    class ChoiceForm(FormInput):
        priority: str = SingleChoice(
            options=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
            description="Priority",
        )

    low = ChoiceForm(priority="low")
    assert low.priority == "low"

    medium = ChoiceForm(priority="medium")
    assert medium.priority == "medium"

    high = ChoiceForm(priority="high")
    assert high.priority == "high"


def test_single_choice_invalid_option_validation() -> None:
    class ChoiceForm(FormInput):
        priority: str = SingleChoice(
            options=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
            description="Priority",
        )

    with pytest.raises(ValidationError):
        ChoiceForm(priority="invalid")


def test_single_choice_simple_strings_validation() -> None:
    class SimpleChoiceForm(FormInput):
        color: str = SingleChoice(
            options=["red", "green", "blue"],
            description="Color",
        )

    valid = SimpleChoiceForm(color="red")
    assert valid.color == "red"

    with pytest.raises(ValidationError):
        SimpleChoiceForm(color="yellow")


@pytest.mark.asyncio
async def test_multi_choice_field_in_event(temporal_env: WorkflowEnvironment) -> None:
    """Test that MultiChoice generates array schema with anyOf items."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[MultiChoiceFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "multi_choice_form_workflow",
                id="test-multi-choice-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"tags": ["frontend", "backend"]}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    tags_schema = input_schema["properties"]["tags"]

    assert tags_schema["type"] == "array"
    assert tags_schema["description"] == "Select applicable tags"

    any_of = tags_schema["items"]["anyOf"]
    assert len(any_of) == 3

    assert any_of[0] == {"type": "string", "const": "frontend", "description": "Frontend"}
    assert any_of[1] == {"type": "string", "const": "backend", "description": "Backend"}
    assert any_of[2] == {"type": "string", "const": "infra", "description": "Infrastructure"}

    assert tags_schema["minItems"] == 1
    assert tags_schema["uniqueItems"] is True


def test_multi_choice_valid_option_validation() -> None:
    class ChoiceForm(FormInput):
        tags: list[str] = MultiChoice(
            options=[("frontend", "Frontend"), ("backend", "Backend"), ("infra", "Infra")],
            description="Tags",
        )

    result = ChoiceForm(tags=["frontend", "backend"])
    assert result.tags == ["frontend", "backend"]

    single = ChoiceForm(tags=["infra"])
    assert single.tags == ["infra"]


def test_multi_choice_invalid_option_validation() -> None:
    class ChoiceForm(FormInput):
        tags: list[str] = MultiChoice(
            options=[("frontend", "Frontend"), ("backend", "Backend")],
            description="Tags",
        )

    with pytest.raises(ValidationError):
        ChoiceForm(tags=["invalid"])

    with pytest.raises(ValidationError):
        ChoiceForm(tags=["frontend", "invalid"])


def test_multi_choice_simple_strings_validation() -> None:
    class SimpleChoiceForm(FormInput):
        colors: list[str] = MultiChoice(
            options=["red", "green", "blue"],
            description="Colors",
        )

    valid = SimpleChoiceForm(colors=["red", "blue"])
    assert valid.colors == ["red", "blue"]

    with pytest.raises(ValidationError):
        SimpleChoiceForm(colors=["yellow"])


def test_multi_choice_rejects_non_list_input() -> None:
    class ChoiceForm(FormInput):
        tags: list[str] = MultiChoice(
            options=[("frontend", "Frontend"), ("backend", "Backend")],
            description="Tags",
        )

    with pytest.raises(ValidationError):
        ChoiceForm.model_validate({"tags": "frontend"})


def test_multi_choice_rejects_empty_list() -> None:
    class ChoiceForm(FormInput):
        tags: list[str] = MultiChoice(
            options=[("frontend", "Frontend"), ("backend", "Backend")],
            description="Tags",
        )

    with pytest.raises(ValidationError):
        ChoiceForm(tags=[])


def test_multi_choice_rejects_duplicate_values() -> None:
    class ChoiceForm(FormInput):
        tags: list[str] = MultiChoice(
            options=[("frontend", "Frontend"), ("backend", "Backend")],
            description="Tags",
        )

    with pytest.raises(ValidationError):
        ChoiceForm(tags=["frontend", "frontend"])


def test_multi_choice_rejects_duplicate_options() -> None:
    with pytest.raises(ValueError):
        MultiChoice(
            options=[("frontend", "Frontend"), ("frontend", "Frontend 2")],
            description="Tags",
        )

    with pytest.raises(ValueError):
        MultiChoice(
            options=["red", "red"],
            description="Colors",
        )


def test_multi_choice_all_options_selected() -> None:
    class ChoiceForm(FormInput):
        tags: list[str] = MultiChoice(
            options=[("frontend", "Frontend"), ("backend", "Backend"), ("infra", "Infra")],
            description="Tags",
        )

    result = ChoiceForm(tags=["frontend", "backend", "infra"])
    assert result.tags == ["frontend", "backend", "infra"]


@pytest.mark.asyncio
async def test_single_file_field_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SingleFileFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "single_file_form_workflow",
                id="test-single-file-field-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"document": "https://storage.example.com/file.pdf"}},
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    document_schema = input_schema["properties"]["document"]
    assert document_schema["type"] == "string"
    assert document_schema["format"] == "uri"
    assert document_schema["title"] == "File"
    assert document_schema["description"] == "Upload a document"


@pytest.mark.asyncio
async def test_multi_file_field_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[MultiFileFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "multi_file_form_workflow",
                id="test-multi-file-field-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "attachments": [
                            "https://storage.example.com/file1.pdf",
                            "https://storage.example.com/file2.pdf",
                        ],
                    },
                },
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    attachments_schema = input_schema["properties"]["attachments"]
    assert attachments_schema["type"] == "array"
    assert attachments_schema["items"] == {
        "type": "string",
        "format": "uri",
        "title": "File",
    }
    assert attachments_schema["description"] == "Upload files"


def test_file_field_single_validation() -> None:
    valid = SingleFileForm(document="https://storage.example.com/file.pdf")
    assert valid.document == "https://storage.example.com/file.pdf"


def test_file_field_multiple_validation() -> None:
    valid = MultiFileForm(
        attachments=[
            "https://storage.example.com/file1.pdf",
            "https://storage.example.com/file2.pdf",
        ]
    )
    assert valid.attachments == [
        "https://storage.example.com/file1.pdf",
        "https://storage.example.com/file2.pdf",
    ]


# ============================================================================
# ConfirmationInput and ValidateDenyConfirmation Schema Tests
# ============================================================================


@pytest.mark.asyncio
async def test_accept_decline_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[AcceptDeclineStepWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "accept_decline_step_workflow",
                id="test-accept-decline-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "choice": ACCEPT_OPTION_VALUE,
                    },
                },
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    assert input_schema["title"] == "Confirmation"

    choice_schema = input_schema["properties"]["choice"]
    assert choice_schema["oneOf"] == [
        {"const": "decline", "description": "No", "type": "string"},
        {"const": "accept", "description": "Yes", "type": "string"},
    ]
    assert choice_schema["description"] == "Do you accept?"


@pytest.mark.asyncio
async def test_confirmation_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[ConfirmationStepWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "confirmation_step_workflow",
                id="test-confirmation-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "choice": "option-a",
                    },
                },
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    assert input_schema["title"] == "Confirmation"

    choice_schema = input_schema["properties"]["choice"]
    assert choice_schema["oneOf"] == [
        {"const": "option-a", "description": "Option A", "type": "string"},
        {"const": "option-b", "description": "Option B", "type": "string"},
        {"const": "option-c", "description": "Option C", "type": "string"},
    ]
    assert choice_schema["description"] == "Choose an option"


# ============================================================================
# is_accepted helper tests
# ============================================================================


def test_is_accepted_returns_true_for_accept() -> None:
    """Test that is_accepted returns True when choice is 'accept'."""
    ConfirmationModel = AcceptDeclineConfirmation(
        description="Confirm?",
        accept_label="Yes",
        decline_label="No",
    )
    confirmation = ConfirmationModel(choice=ACCEPT_OPTION_VALUE)
    assert is_accepted(confirmation) is True


def test_is_accepted_returns_false_for_decline() -> None:
    """Test that is_accepted returns False when choice is 'decline'."""
    ConfirmationModel = AcceptDeclineConfirmation(
        description="Confirm?",
        accept_label="Yes",
        decline_label="No",
    )
    confirmation = ConfirmationModel(choice=DECLINE_OPTION_VALUE)
    assert is_accepted(confirmation) is False


# ============================================================================
# Initial Values Tests (UI hints only — fields remain required)
# ============================================================================


@pytest.mark.asyncio
async def test_form_with_prefilled_values_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    """Test that emitted workflow event schema includes initial values as 'default' hints."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[InitialValuesFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "prefilled_values_form_workflow",
                id="test-initial-values-schema",
                task_queue="test-task-queue",
            )

            await wait_for_pending_inputs(handle, expected_count=1)

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    props = input_schema["properties"]
    assert props["name"]["default"] == "John Doe"
    assert props["email"]["default"] == "user@example.com"
    assert props["age"]["default"] == 25.0
    assert props["amount"]["default"] == 50.0
    assert props["price"]["default"] == 99.99
    assert props["priority"]["default"] == "medium"
    assert props["tags"]["default"] == ["frontend"]
    assert props["tags_deduped"]["default"] == ["frontend", "backend"]
    assert props["scheduled_at"]["default"] == "2023-01-01T00:00:00+00:00"
    assert props["scheduled_at_str"]["default"] == "2023-06-15T12:30:00+00:00"
    assert props["scheduled_date"]["default"] == "2023-01-01"
    assert props["scheduled_date_str"]["default"] == "2023-06-15"

    # initial values are UI hints only — all fields remain required
    assert set(input_schema["required"]) == {
        "name",
        "email",
        "age",
        "amount",
        "price",
        "priority",
        "tags",
        "tags_deduped",
        "scheduled_at",
        "scheduled_at_str",
        "scheduled_date",
        "scheduled_date_str",
    }


class FormWithInvalidInitialValues(FormInput):
    """Form where all initial values are invalid and should be silently ignored."""

    email: str = TextField(
        description="Email",
        pattern=r"^[\w.-]+@[\w.-]+\.\w+$",
        prefilled_value="not-an-email",
    )
    below_min: float = NumberField(description="Amount", minimum=10, prefilled_value=5)
    above_max: float = NumberField(description="Amount", maximum=100, prefilled_value=200)
    at_exclusive_min: float = NumberField(description="Amount", exclusive_minimum=0, prefilled_value=0)
    at_exclusive_max: float = NumberField(description="Amount", exclusive_maximum=100, prefilled_value=100)
    priority: str = SingleChoice(
        options=[("low", "Low"), ("high", "High")],
        prefilled_value="invalid_option",
    )
    tags: list[str] = MultiChoice(
        options=[("frontend", "Frontend"), ("backend", "Backend")],
        prefilled_value=["frontend", "invalid_tag"],
    )
    dt: datetime = DateTimeField(description="DateTime", prefilled_value="not-a-datetime")
    d: date = DateField(description="Date", prefilled_value="not-a-date")


@workflow.define(name="invalid_prefilled_values_form_workflow")
class InvalidInitialValuesFormWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        form_input = await self.wait_for_input(FormWithInvalidInitialValues, label="Invalid Initial Values Form")
        return {"email": form_input.email}


@pytest.mark.asyncio
async def test_invalid_prefilled_values_ignored_in_event(temporal_env: WorkflowEnvironment) -> None:
    """Invalid initial values should be silently dropped from the emitted schema."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[InvalidInitialValuesFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "invalid_prefilled_values_form_workflow",
                id="test-invalid-initial-values-schema",
                task_queue="test-task-queue",
            )

            await wait_for_pending_inputs(handle, expected_count=1)

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    props = input_schema["properties"]
    for field_name in [
        "email",
        "below_min",
        "above_max",
        "at_exclusive_min",
        "at_exclusive_max",
        "priority",
        "tags",
        "dt",
        "d",
    ]:
        assert "default" not in props[field_name], f"Expected no default for {field_name}"


# ============================================================================
# FileWithMetadataField Schema and Validation Tests
# ============================================================================


@pytest.mark.asyncio
async def test_single_file_with_metadata_field_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SingleFileWithMetadataFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "single_file_with_metadata_form_workflow",
                id="test-single-file-with-metadata-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "document": {
                            "filename": "report.pdf",
                            "url": "https://storage.example.com/report.pdf",
                            "content_type": "application/pdf",
                        },
                    },
                },
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    document_schema = input_schema["properties"]["document"]
    assert document_schema["title"] == "FileWithMetadata"
    assert document_schema["type"] == "object"
    assert document_schema["description"] == "Upload a document"
    assert document_schema["required"] == ["filename", "url", "content_type"]
    assert document_schema["properties"]["filename"] == {"type": "string"}
    assert document_schema["properties"]["url"] == {"type": "string", "format": "uri"}
    assert document_schema["properties"]["content_type"] == {"type": "string"}


@pytest.mark.asyncio
async def test_multi_file_with_metadata_field_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[MultiFileWithMetadataFormWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "multi_file_with_metadata_form_workflow",
                id="test-multi-file-with-metadata-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "attachments": [
                            {
                                "filename": "file1.pdf",
                                "url": "https://storage.example.com/file1.pdf",
                                "content_type": "application/pdf",
                            },
                            {
                                "filename": "file2.png",
                                "url": "https://storage.example.com/file2.png",
                                "content_type": "image/png",
                            },
                        ],
                    },
                },
            )
            await handle.result()

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None

    attachments_schema = input_schema["properties"]["attachments"]
    assert attachments_schema["type"] == "array"
    assert attachments_schema["description"] == "Upload files"
    assert attachments_schema["items"] == {
        "title": "FileWithMetadata",
        "type": "object",
        "properties": {
            "filename": {"type": "string"},
            "url": {"type": "string", "format": "uri"},
            "content_type": {"type": "string"},
        },
        "required": ["filename", "url", "content_type"],
    }


# ============================================================================
# FileField type annotation mismatch validation tests
# ============================================================================


def test_file_field_rejects_multiple_without_list_annotation() -> None:
    with pytest.raises(TypeError, match="multiple=True but type annotation is not a list"):

        class BadForm(FormInput):
            document: str = FileField(description="Upload", multiple=True)


def test_file_field_rejects_list_annotation_without_multiple() -> None:
    with pytest.raises(TypeError, match="multiple=False but type annotation is a list"):

        class BadForm(FormInput):
            documents: list[str] = FileField(description="Upload")


def test_file_field_rejects_metadata_type_without_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=False but type annotation is not str"):

        class BadForm(FormInput):
            document: FileWithMetadataValue = FileField(description="Upload")


def test_file_field_rejects_str_type_with_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=True but type annotation is not FileWithMetadataValue"):

        class BadForm(FormInput):
            document: str = FileField(description="Upload", include_metadata=True)


def test_file_field_rejects_list_str_with_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=True but type annotation is not FileWithMetadataValue"):

        class BadForm(FormInput):
            documents: list[str] = FileField(description="Upload", multiple=True, include_metadata=True)


def test_file_field_rejects_list_metadata_without_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=False but type annotation is not str"):

        class BadForm(FormInput):
            documents: list[FileWithMetadataValue] = FileField(description="Upload", multiple=True)


def test_file_field_accepts_optional_annotations() -> None:
    """Optional (None union) annotations should not break the validation."""

    class ValidForm(FormInput):
        doc: str | None = FileField(description="Upload")
        docs: list[str] | None = FileField(description="Upload", multiple=True)
        meta_doc: FileWithMetadataValue | None = FileField(description="Upload", include_metadata=True)
        meta_docs: list[FileWithMetadataValue] | None = FileField(
            description="Upload", multiple=True, include_metadata=True
        )

    assert ValidForm.model_fields["doc"] is not None


def test_file_field_rejects_optional_str_with_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=True but type annotation is not FileWithMetadataValue"):

        class BadForm(FormInput):
            doc: str | None = FileField(description="Upload", include_metadata=True)


def test_file_field_rejects_optional_list_str_with_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=True but type annotation is not FileWithMetadataValue"):

        class BadForm(FormInput):
            docs: list[str] | None = FileField(description="Upload", multiple=True, include_metadata=True)


def test_file_field_rejects_optional_metadata_without_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=False but type annotation is not str"):

        class BadForm(FormInput):
            doc: FileWithMetadataValue | None = FileField(description="Upload")


def test_file_field_rejects_optional_list_metadata_without_include_metadata() -> None:
    with pytest.raises(TypeError, match="include_metadata=False but type annotation is not str"):

        class BadForm(FormInput):
            docs: list[FileWithMetadataValue] | None = FileField(description="Upload", multiple=True)


def test_file_field_rejects_optional_str_with_multiple() -> None:
    with pytest.raises(TypeError, match="multiple=True but type annotation is not a list"):

        class BadForm(FormInput):
            doc: str | None = FileField(description="Upload", multiple=True)


def test_file_field_rejects_optional_list_str_without_multiple() -> None:
    with pytest.raises(TypeError, match="multiple=False but type annotation is a list"):

        class BadForm(FormInput):
            docs: list[str] | None = FileField(description="Upload")


def test_file_field_rejects_optional_metadata_with_multiple() -> None:
    with pytest.raises(TypeError, match="multiple=True but type annotation is not a list"):

        class BadForm(FormInput):
            doc: FileWithMetadataValue | None = FileField(description="Upload", multiple=True, include_metadata=True)


def test_file_field_rejects_optional_list_metadata_without_multiple() -> None:
    with pytest.raises(TypeError, match="multiple=False but type annotation is a list"):

        class BadForm(FormInput):
            docs: list[FileWithMetadataValue] | None = FileField(description="Upload", include_metadata=True)
