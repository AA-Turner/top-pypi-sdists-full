import uuid

import pytest
from pydantic import ValidationError

from mistralai.workflows.protocol.v1.workflow import (
    WorkerHeartbeatRequest,
    WorkflowRegistrationRef,
    WorkflowSpecsRegisterResponse,
)

WORKFLOW_ID = uuid.uuid4()
REGISTRATION_ID = uuid.uuid4()


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
