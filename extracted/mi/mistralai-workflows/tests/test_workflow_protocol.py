import uuid

import pytest
from pydantic import ValidationError

from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit, set_rate_limit
from mistralai.workflows.models import WorkflowSpecWithTaskQueue
from mistralai.workflows.protocol.v1.workflow import (
    WorkerHeartbeatRequest,
    WorkflowRegistrationRef,
    WorkflowSpecsRegisterRequest,
    WorkflowSpecsRegisterResponse,
)

WORKFLOW_ID = uuid.uuid4()
REGISTRATION_ID = uuid.uuid4()


def test_workflow_specs_register_request_rejects_empty_definitions() -> None:
    with pytest.raises(ValidationError):
        WorkflowSpecsRegisterRequest(
            definitions=[],
            deployment_name="test-deployment",
            worker_name="test-worker",
        )


def test_deployment_name_rejects_non_string_input() -> None:
    with pytest.raises(ValidationError):
        WorkflowSpecsRegisterRequest(
            definitions=[
                WorkflowSpecWithTaskQueue(
                    name="test",
                    description="",
                    input_schema={},
                    output_schema={},
                    task_queue="default",
                )
            ],
            deployment_name=123,
            worker_name="test-worker",
        )


def test_deployment_name_rejects_invalid_string() -> None:
    with pytest.raises(ValidationError):
        WorkflowSpecsRegisterRequest(
            definitions=[
                WorkflowSpecWithTaskQueue(
                    name="test",
                    description="",
                    input_schema={},
                    output_schema={},
                    task_queue="default",
                )
            ],
            deployment_name="bad name!",
            worker_name="test-worker",
        )


class TestReservedDeploymentNameSuffixes:
    HEX = "0123456789abcdef0123456789abcdef"

    @pytest.mark.parametrize(
        "name",
        [
            f"dep-rate-limited-{HEX}",
            f"dep-sticky-worker-session-{HEX}",
            f"dep-sticky-worker-session-{HEX}-rate-limited-{HEX}",
            f"dep-rate-limited-{HEX.upper()}",
        ],
    )
    def test_rejects_derived_task_queue_endings(self, name: str) -> None:
        with pytest.raises(ValidationError, match="reserved"):
            WorkerHeartbeatRequest(deployment_name=name, worker_name="test-worker")

    @pytest.mark.parametrize(
        "name",
        [
            "dep-rate-limited",
            "dep-sticky-worker-session",
            f"rate-limited-{HEX}",
            f"dep-rate-limited-{HEX}-v2",
            f"dep-rate-limited-{HEX[:31]}",
            f"dep_rate_limited_{HEX}",
        ],
    )
    def test_accepts_names_without_a_reserved_ending(self, name: str) -> None:
        request = WorkerHeartbeatRequest(deployment_name=name, worker_name="test-worker")

        assert request.deployment_name == name

    def test_rejects_the_rate_limited_queue_name_workers_derive(self) -> None:
        def some_activity() -> None: ...

        rate_limit = set_rate_limit(some_activity, RateLimit(time_window_in_sec=1, max_execution=1))

        with pytest.raises(ValidationError, match="reserved"):
            WorkerHeartbeatRequest(deployment_name=f"dep-{rate_limit.task_queue_suffix}", worker_name="test-worker")


def test_task_queue_is_optional_on_registered_specs() -> None:
    spec = WorkflowSpecWithTaskQueue(name="test", input_schema={})

    request = WorkflowSpecsRegisterRequest(definitions=[spec], deployment_name="dep-1", worker_name="test-worker")

    assert request.model_dump(mode="json")["definitions"][0]["task_queue"] is None


def test_task_queue_is_deprecated_and_not_required_in_the_register_schema() -> None:
    schema = WorkflowSpecWithTaskQueue.model_json_schema()

    assert "task_queue" not in schema["required"]
    assert schema["properties"]["task_queue"]["deprecated"] is True


def test_task_queue_round_trips_on_registered_specs() -> None:
    spec = WorkflowSpecWithTaskQueue(name="test", input_schema={}, task_queue="dep-1")

    request = WorkflowSpecsRegisterRequest(definitions=[spec], deployment_name="dep-1", worker_name="test-worker")

    assert request.model_dump(mode="json")["definitions"][0]["task_queue"] == "dep-1"


class TestWorkflowRegistrationRef:
    def test_new_field_name(self) -> None:
        ref = WorkflowRegistrationRef.model_validate(
            {"workflow_id": str(WORKFLOW_ID), "workflow_registration_id": str(REGISTRATION_ID)}
        )
        assert ref.workflow_id == WORKFLOW_ID
        assert ref.workflow_registration_id == REGISTRATION_ID

    def test_old_field_name(self) -> None:
        ref = WorkflowRegistrationRef.model_validate(
            {"workflow_id": str(WORKFLOW_ID), "workflow_version_id": str(REGISTRATION_ID)}
        )
        assert ref.workflow_id == WORKFLOW_ID
        assert ref.workflow_registration_id == REGISTRATION_ID
        assert ref.workflow_version_id == REGISTRATION_ID

    def test_missing_both_ids_raises(self) -> None:
        with pytest.raises(ValidationError):
            WorkflowRegistrationRef.model_validate({"workflow_id": str(WORKFLOW_ID)})

    def test_deprecated_field_included_in_serialization_for_backward_compat(self) -> None:
        ref = WorkflowRegistrationRef.model_validate(
            {"workflow_id": str(WORKFLOW_ID), "workflow_registration_id": str(REGISTRATION_ID)}
        )
        data = ref.model_dump(mode="json")
        assert data["workflow_version_id"] == str(REGISTRATION_ID)


class TestWorkflowSpecsRegisterResponse:
    def test_new_field_names(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(
            {
                "workflow_registration_ids": [str(REGISTRATION_ID)],
                "workflow_registration_refs": [
                    {"workflow_id": str(WORKFLOW_ID), "workflow_registration_id": str(REGISTRATION_ID)}
                ],
                "has_conflicts": False,
            }
        )
        assert resp.workflow_registration_ids == [REGISTRATION_ID]
        assert len(resp.workflow_registration_refs) == 1
        assert resp.has_conflicts is False

    def test_defaults_to_empty(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate({"has_conflicts": False})
        assert resp.workflow_registration_ids == []
        assert resp.workflow_registration_refs == []

    def test_deprecated_fields_excluded_from_serialization(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(
            {
                "workflow_registration_ids": [str(REGISTRATION_ID)],
                "workflow_registration_refs": [
                    {"workflow_id": str(WORKFLOW_ID), "workflow_registration_id": str(REGISTRATION_ID)}
                ],
                "has_conflicts": False,
            }
        )
        data = resp.model_dump(mode="json")
        assert "workflow_version_ids" not in data
        assert "workflow_version_refs" not in data

    def test_extra_fields_from_old_server_ignored(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(
            {
                "workflow_registration_ids": [str(REGISTRATION_ID)],
                "workflow_version_ids": [str(REGISTRATION_ID)],
                "has_conflicts": False,
            }
        )
        assert resp.workflow_registration_ids == [REGISTRATION_ID]


class TestWorkerHeartbeatRequest:
    HB_FIELDS = {"deployment_name": "test-deploy", "worker_name": "test-worker"}

    def test_new_field_name(self) -> None:
        ref = WorkflowRegistrationRef(workflow_id=WORKFLOW_ID, workflow_registration_id=REGISTRATION_ID)
        req = WorkerHeartbeatRequest(workflow_registration_refs=[ref], **self.HB_FIELDS)
        assert req.workflow_registration_refs == [ref]

    def test_deprecated_field_coerced(self) -> None:
        ref = WorkflowRegistrationRef(workflow_id=WORKFLOW_ID, workflow_registration_id=REGISTRATION_ID)
        req = WorkerHeartbeatRequest(workflow_version_refs=[ref], **self.HB_FIELDS)
        assert req.workflow_registration_refs == [ref]

    def test_deprecated_field_excluded_from_serialization(self) -> None:
        ref = WorkflowRegistrationRef(workflow_id=WORKFLOW_ID, workflow_registration_id=REGISTRATION_ID)
        req = WorkerHeartbeatRequest(workflow_registration_refs=[ref], **self.HB_FIELDS)
        data = req.model_dump(mode="json")
        assert "workflow_version_refs" not in data

    def test_missing_deployment_name_raises(self) -> None:
        with pytest.raises(Exception):
            WorkerHeartbeatRequest(workflow_registration_refs=[])
