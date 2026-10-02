from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.environment_with_counts_page_dto_items_item_disabled_built_in_synthesizer_keys_item import EnvironmentWithCountsPageDtoItemsItemDisabledBuiltInSynthesizerKeysItem
from ..models.environment_with_counts_page_dto_items_item_qa_gate_override_allowed_stages_item import EnvironmentWithCountsPageDtoItemsItemQaGateOverrideAllowedStagesItem
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0 import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0
  from ..models.environment_with_counts_page_dto_items_item_run_field_config import EnvironmentWithCountsPageDtoItemsItemRunFieldConfig





T = TypeVar("T", bound="EnvironmentWithCountsPageDtoItemsItem")



@_attrs_define
class EnvironmentWithCountsPageDtoItemsItem:
    """ An environment with denormalized rollup counts for problem and problem-run totals. Used by list endpoints to avoid
    N+1 fetches.

        Attributes:
            id (UUID): Stable environment identifier (UUID).
            external_id (None | str): Customer-provided external identifier. Null when the environment was created without
                an external id (e.g. via the in-app 'new environment' flow with no source-of-truth system).
            organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
            name (str): Human-readable display name of the environment.
            template_problem_id (None | UUID): Problem used as the template seed for new problems in this environment. Null
                when no template has been configured.
            max_import_file_size_bytes (int | None): Per-file size cap (bytes) applied to imported problem files. Null falls
                back to the platform default. Example: 10485760.
            max_upload_file_size_bytes (int | None): Per-file size cap (bytes) applied to direct uploads. Null falls back to
                the platform default. Example: 10485760.
            max_version_aggregate_file_size_bytes (int | None): Aggregate size cap (bytes) across all files attached to one
                problem version. Null falls back to the platform default. Example: 104857600.
            run_field_config (EnvironmentWithCountsPageDtoItemsItemRunFieldConfig): Default attempt count for the Run
                problem modal. Image and model policy is governed by run-config bindings and curated menus.
            require_lock_before_new_version (bool): When true, users must lock the current version before creating a new
                one. Prevents config loss from unlocked-version copies.
            problem_editor_instructions (None | str): Markdown guidance surfaced to problem editors within the environment.
                Null suppresses it.
            rubric_issue_template (None | str): Markdown template used to pre-populate the body of new rubric issues. Null
                leaves the body empty; per-rubric overrides take precedence when set.
            global_issue_template (None | str): Markdown template used to pre-populate the body of new global (non-rubric-
                attached) issues. Null leaves the body empty; per-version overrides take precedence when set.
            qa_gate_override_allowed_stages (list[EnvironmentWithCountsPageDtoItemsItemQaGateOverrideAllowedStagesItem]):
                QA-gate stages on which a user may override the gate verdict in this environment. Empty array disables overrides
                on all stages.
            disabled_built_in_synthesizer_keys
                (list[EnvironmentWithCountsPageDtoItemsItemDisabledBuiltInSynthesizerKeysItem]): Built-in synthesizer keys
                disabled for this environment. Disabled entries are hidden from run pickers and rejected on submission, but
                remain visible in the Configurations list for re-enablement.
            guided_tour (EnvironmentWithCountsPageDtoItemsItemGuidedTourType0 | None): Authored guided-tour flow shown in
                the in-editor right-rail checklist. Null hides the panel.
            preview_filename (None | str): Filename of the preview asset shown on problem cards. Null hides the preview.
            solver_run_config_version_id (None | UUID): Locked run-config version bound as the env-level solver default.
                Resolved at job submission after per-version overrides; null means no env-level binding.
            grader_run_config_version_id (None | UUID): Locked run-config version bound as the env-level grader default.
                Resolved at job submission after per-version overrides; null means no env-level binding.
            programmatic_grader_run_config_version_id (None | UUID): Locked run-config version that drives all programmatic
                grading in this environment, overriding the platform-wide programmatic grader default. Separate from the grader
                binding, which governs agentic and rubric grading only; null falls back to the platform default.
            qa_run_config_version_id (None | UUID): Locked run-config version bound as the env-level QA default. Resolved at
                job submission after per-version overrides; null means no env-level binding.
            synthesizer_run_config_version_id (None | UUID): Locked run-config version bound as the env-level synthesizer
                default. Resolved at job submission after per-version overrides; null means no env-level binding.
            created_at (datetime.datetime): Timestamp when the environment was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the environment was last updated (ISO-8601, UTC).
            problem_count (int): Total number of problems in this environment. Example: 42.
            problem_run_count (int): Total number of problem runs submitted across all problems in this environment.
                Example: 128.
     """

    id: UUID
    external_id: None | str
    organization_id: UUID
    name: str
    template_problem_id: None | UUID
    max_import_file_size_bytes: int | None
    max_upload_file_size_bytes: int | None
    max_version_aggregate_file_size_bytes: int | None
    run_field_config: EnvironmentWithCountsPageDtoItemsItemRunFieldConfig
    require_lock_before_new_version: bool
    problem_editor_instructions: None | str
    rubric_issue_template: None | str
    global_issue_template: None | str
    qa_gate_override_allowed_stages: list[EnvironmentWithCountsPageDtoItemsItemQaGateOverrideAllowedStagesItem]
    disabled_built_in_synthesizer_keys: list[EnvironmentWithCountsPageDtoItemsItemDisabledBuiltInSynthesizerKeysItem]
    guided_tour: EnvironmentWithCountsPageDtoItemsItemGuidedTourType0 | None
    preview_filename: None | str
    solver_run_config_version_id: None | UUID
    grader_run_config_version_id: None | UUID
    programmatic_grader_run_config_version_id: None | UUID
    qa_run_config_version_id: None | UUID
    synthesizer_run_config_version_id: None | UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    problem_count: int
    problem_run_count: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0 import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0 # noqa: PLC0415
        from ..models.environment_with_counts_page_dto_items_item_run_field_config import EnvironmentWithCountsPageDtoItemsItemRunFieldConfig # noqa: PLC0415
        id = str(self.id)

        external_id: None | str
        external_id = self.external_id

        organization_id = str(self.organization_id)

        name = self.name

        template_problem_id: None | str
        if isinstance(self.template_problem_id, UUID):
            template_problem_id = str(self.template_problem_id)
        else:
            template_problem_id = self.template_problem_id

        max_import_file_size_bytes: int | None
        max_import_file_size_bytes = self.max_import_file_size_bytes

        max_upload_file_size_bytes: int | None
        max_upload_file_size_bytes = self.max_upload_file_size_bytes

        max_version_aggregate_file_size_bytes: int | None
        max_version_aggregate_file_size_bytes = self.max_version_aggregate_file_size_bytes

        run_field_config = self.run_field_config.to_dict()

        require_lock_before_new_version = self.require_lock_before_new_version

        problem_editor_instructions: None | str
        problem_editor_instructions = self.problem_editor_instructions

        rubric_issue_template: None | str
        rubric_issue_template = self.rubric_issue_template

        global_issue_template: None | str
        global_issue_template = self.global_issue_template

        qa_gate_override_allowed_stages = []
        for qa_gate_override_allowed_stages_item_data in self.qa_gate_override_allowed_stages:
            qa_gate_override_allowed_stages_item = qa_gate_override_allowed_stages_item_data.value
            qa_gate_override_allowed_stages.append(qa_gate_override_allowed_stages_item)



        disabled_built_in_synthesizer_keys = []
        for disabled_built_in_synthesizer_keys_item_data in self.disabled_built_in_synthesizer_keys:
            disabled_built_in_synthesizer_keys_item = disabled_built_in_synthesizer_keys_item_data.value
            disabled_built_in_synthesizer_keys.append(disabled_built_in_synthesizer_keys_item)



        guided_tour: dict[str, Any] | None
        if isinstance(self.guided_tour, EnvironmentWithCountsPageDtoItemsItemGuidedTourType0):
            guided_tour = self.guided_tour.to_dict()
        else:
            guided_tour = self.guided_tour

        preview_filename: None | str
        preview_filename = self.preview_filename

        solver_run_config_version_id: None | str
        if isinstance(self.solver_run_config_version_id, UUID):
            solver_run_config_version_id = str(self.solver_run_config_version_id)
        else:
            solver_run_config_version_id = self.solver_run_config_version_id

        grader_run_config_version_id: None | str
        if isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        programmatic_grader_run_config_version_id: None | str
        if isinstance(self.programmatic_grader_run_config_version_id, UUID):
            programmatic_grader_run_config_version_id = str(self.programmatic_grader_run_config_version_id)
        else:
            programmatic_grader_run_config_version_id = self.programmatic_grader_run_config_version_id

        qa_run_config_version_id: None | str
        if isinstance(self.qa_run_config_version_id, UUID):
            qa_run_config_version_id = str(self.qa_run_config_version_id)
        else:
            qa_run_config_version_id = self.qa_run_config_version_id

        synthesizer_run_config_version_id: None | str
        if isinstance(self.synthesizer_run_config_version_id, UUID):
            synthesizer_run_config_version_id = str(self.synthesizer_run_config_version_id)
        else:
            synthesizer_run_config_version_id = self.synthesizer_run_config_version_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        problem_count = self.problem_count

        problem_run_count = self.problem_run_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "externalId": external_id,
            "organizationId": organization_id,
            "name": name,
            "templateProblemId": template_problem_id,
            "maxImportFileSizeBytes": max_import_file_size_bytes,
            "maxUploadFileSizeBytes": max_upload_file_size_bytes,
            "maxVersionAggregateFileSizeBytes": max_version_aggregate_file_size_bytes,
            "runFieldConfig": run_field_config,
            "requireLockBeforeNewVersion": require_lock_before_new_version,
            "problemEditorInstructions": problem_editor_instructions,
            "rubricIssueTemplate": rubric_issue_template,
            "globalIssueTemplate": global_issue_template,
            "qaGateOverrideAllowedStages": qa_gate_override_allowed_stages,
            "disabledBuiltInSynthesizerKeys": disabled_built_in_synthesizer_keys,
            "guidedTour": guided_tour,
            "previewFilename": preview_filename,
            "solverRunConfigVersionId": solver_run_config_version_id,
            "graderRunConfigVersionId": grader_run_config_version_id,
            "programmaticGraderRunConfigVersionId": programmatic_grader_run_config_version_id,
            "qaRunConfigVersionId": qa_run_config_version_id,
            "synthesizerRunConfigVersionId": synthesizer_run_config_version_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "problemCount": problem_count,
            "problemRunCount": problem_run_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0 import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0 # noqa: PLC0415
        from ..models.environment_with_counts_page_dto_items_item_run_field_config import EnvironmentWithCountsPageDtoItemsItemRunFieldConfig # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("externalId"))


        organization_id = UUID(d.pop("organizationId"))




        name = d.pop("name")

        def _parse_template_problem_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                template_problem_id_type_0 = UUID(data)



                return template_problem_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        template_problem_id = _parse_template_problem_id(d.pop("templateProblemId"))


        def _parse_max_import_file_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_import_file_size_bytes = _parse_max_import_file_size_bytes(d.pop("maxImportFileSizeBytes"))


        def _parse_max_upload_file_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_upload_file_size_bytes = _parse_max_upload_file_size_bytes(d.pop("maxUploadFileSizeBytes"))


        def _parse_max_version_aggregate_file_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_version_aggregate_file_size_bytes = _parse_max_version_aggregate_file_size_bytes(d.pop("maxVersionAggregateFileSizeBytes"))


        run_field_config = EnvironmentWithCountsPageDtoItemsItemRunFieldConfig.from_dict(d.pop("runFieldConfig"))




        require_lock_before_new_version = d.pop("requireLockBeforeNewVersion")

        def _parse_problem_editor_instructions(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        problem_editor_instructions = _parse_problem_editor_instructions(d.pop("problemEditorInstructions"))


        def _parse_rubric_issue_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rubric_issue_template = _parse_rubric_issue_template(d.pop("rubricIssueTemplate"))


        def _parse_global_issue_template(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        global_issue_template = _parse_global_issue_template(d.pop("globalIssueTemplate"))


        qa_gate_override_allowed_stages = []
        _qa_gate_override_allowed_stages = d.pop("qaGateOverrideAllowedStages")
        for qa_gate_override_allowed_stages_item_data in (_qa_gate_override_allowed_stages):
            qa_gate_override_allowed_stages_item = EnvironmentWithCountsPageDtoItemsItemQaGateOverrideAllowedStagesItem(qa_gate_override_allowed_stages_item_data)



            qa_gate_override_allowed_stages.append(qa_gate_override_allowed_stages_item)


        disabled_built_in_synthesizer_keys = []
        _disabled_built_in_synthesizer_keys = d.pop("disabledBuiltInSynthesizerKeys")
        for disabled_built_in_synthesizer_keys_item_data in (_disabled_built_in_synthesizer_keys):
            disabled_built_in_synthesizer_keys_item = EnvironmentWithCountsPageDtoItemsItemDisabledBuiltInSynthesizerKeysItem(disabled_built_in_synthesizer_keys_item_data)



            disabled_built_in_synthesizer_keys.append(disabled_built_in_synthesizer_keys_item)


        def _parse_guided_tour(data: object) -> EnvironmentWithCountsPageDtoItemsItemGuidedTourType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                guided_tour_type_0 = EnvironmentWithCountsPageDtoItemsItemGuidedTourType0.from_dict(data)



                return guided_tour_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EnvironmentWithCountsPageDtoItemsItemGuidedTourType0 | None, data)

        guided_tour = _parse_guided_tour(d.pop("guidedTour"))


        def _parse_preview_filename(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        preview_filename = _parse_preview_filename(d.pop("previewFilename"))


        def _parse_solver_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                solver_run_config_version_id_type_0 = UUID(data)



                return solver_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        solver_run_config_version_id = _parse_solver_run_config_version_id(d.pop("solverRunConfigVersionId"))


        def _parse_grader_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grader_run_config_version_id_type_0 = UUID(data)



                return grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        grader_run_config_version_id = _parse_grader_run_config_version_id(d.pop("graderRunConfigVersionId"))


        def _parse_programmatic_grader_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                programmatic_grader_run_config_version_id_type_0 = UUID(data)



                return programmatic_grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        programmatic_grader_run_config_version_id = _parse_programmatic_grader_run_config_version_id(d.pop("programmaticGraderRunConfigVersionId"))


        def _parse_qa_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qa_run_config_version_id_type_0 = UUID(data)



                return qa_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        qa_run_config_version_id = _parse_qa_run_config_version_id(d.pop("qaRunConfigVersionId"))


        def _parse_synthesizer_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synthesizer_run_config_version_id_type_0 = UUID(data)



                return synthesizer_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        synthesizer_run_config_version_id = _parse_synthesizer_run_config_version_id(d.pop("synthesizerRunConfigVersionId"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        problem_count = d.pop("problemCount")

        problem_run_count = d.pop("problemRunCount")

        environment_with_counts_page_dto_items_item = cls(
            id=id,
            external_id=external_id,
            organization_id=organization_id,
            name=name,
            template_problem_id=template_problem_id,
            max_import_file_size_bytes=max_import_file_size_bytes,
            max_upload_file_size_bytes=max_upload_file_size_bytes,
            max_version_aggregate_file_size_bytes=max_version_aggregate_file_size_bytes,
            run_field_config=run_field_config,
            require_lock_before_new_version=require_lock_before_new_version,
            problem_editor_instructions=problem_editor_instructions,
            rubric_issue_template=rubric_issue_template,
            global_issue_template=global_issue_template,
            qa_gate_override_allowed_stages=qa_gate_override_allowed_stages,
            disabled_built_in_synthesizer_keys=disabled_built_in_synthesizer_keys,
            guided_tour=guided_tour,
            preview_filename=preview_filename,
            solver_run_config_version_id=solver_run_config_version_id,
            grader_run_config_version_id=grader_run_config_version_id,
            programmatic_grader_run_config_version_id=programmatic_grader_run_config_version_id,
            qa_run_config_version_id=qa_run_config_version_id,
            synthesizer_run_config_version_id=synthesizer_run_config_version_id,
            created_at=created_at,
            updated_at=updated_at,
            problem_count=problem_count,
            problem_run_count=problem_run_count,
        )

        return environment_with_counts_page_dto_items_item

