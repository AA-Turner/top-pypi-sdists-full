import uuid

import pytest
from pydantic import ValidationError

from mistralai.workflows.protocol.v1.workflow import (
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
        # Deprecated computed field should also work
        assert ref.workflow_version_id == REGISTRATION_ID

    def test_missing_both_ids_raises(self) -> None:
        with pytest.raises(ValidationError):
            WorkflowRegistrationRef.model_validate({"workflow_id": str(WORKFLOW_ID)})


class TestWorkflowSpecsRegisterResponse:
    def _make_payload(self, *, use_old_names: bool) -> dict:
        ids_key = "workflow_version_ids" if use_old_names else "workflow_registration_ids"
        refs_key = "workflow_version_refs" if use_old_names else "workflow_registration_refs"
        return {
            ids_key: [str(REGISTRATION_ID)],
            refs_key: [{"workflow_id": str(WORKFLOW_ID), "workflow_registration_id": str(REGISTRATION_ID)}],
            "has_conflicts": False,
        }

    def test_new_field_names(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(self._make_payload(use_old_names=False))
        assert resp.workflow_registration_ids == [REGISTRATION_ID]
        assert len(resp.workflow_registration_refs) == 1
        assert resp.has_conflicts is False

    def test_old_field_names(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(self._make_payload(use_old_names=True))
        assert resp.workflow_registration_ids == [REGISTRATION_ID]
        assert len(resp.workflow_registration_refs) == 1
        assert resp.has_conflicts is False

    def test_old_field_names_without_refs(self) -> None:
        payload = {
            "workflow_version_ids": [str(REGISTRATION_ID)],
            "has_conflicts": False,
        }
        resp = WorkflowSpecsRegisterResponse.model_validate(payload)
        assert resp.workflow_registration_ids == [REGISTRATION_ID]
        assert resp.workflow_registration_refs == []

    def test_deprecated_computed_fields(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(self._make_payload(use_old_names=False))
        assert resp.workflow_version_ids == [REGISTRATION_ID]
        assert len(resp.workflow_version_refs) == 1

    def test_missing_ids_raises(self) -> None:
        with pytest.raises(ValidationError):
            WorkflowSpecsRegisterResponse.model_validate({"has_conflicts": False})

    def test_both_ids_provided_matching(self) -> None:
        resp = WorkflowSpecsRegisterResponse.model_validate(
            {
                "workflow_version_ids": [str(REGISTRATION_ID)],
                "workflow_registration_ids": [str(REGISTRATION_ID)],
                "has_conflicts": False,
            }
        )
        assert resp.workflow_registration_ids == [REGISTRATION_ID]
        assert resp.workflow_version_ids == [REGISTRATION_ID]

    def test_both_ids_provided_mismatched_raises(self) -> None:
        other_id = uuid.uuid4()
        with pytest.raises(ValidationError, match="must match"):
            WorkflowSpecsRegisterResponse.model_validate(
                {
                    "workflow_version_ids": [str(REGISTRATION_ID)],
                    "workflow_registration_ids": [str(other_id)],
                    "has_conflicts": False,
                }
            )
