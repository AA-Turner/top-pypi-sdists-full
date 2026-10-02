from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_environment_settings_dto_disabled_built_in_synthesizer_keys_item import UpdateEnvironmentSettingsDtoDisabledBuiltInSynthesizerKeysItem
from ..models.update_environment_settings_dto_qa_gate_override_allowed_stages_item import UpdateEnvironmentSettingsDtoQaGateOverrideAllowedStagesItem
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.update_environment_settings_dto_guided_tour_type_0 import UpdateEnvironmentSettingsDtoGuidedTourType0
  from ..models.update_environment_settings_dto_run_field_config import UpdateEnvironmentSettingsDtoRunFieldConfig





T = TypeVar("T", bound="UpdateEnvironmentSettingsDto")



@_attrs_define
class UpdateEnvironmentSettingsDto:
    """ Patch-style update body for environment settings. Omitting a field leaves the existing value untouched; null
    explicitly clears the override where allowed.

        Example:
            {'requireLockBeforeNewVersion': True, 'problemEditorInstructions': 'Describe the visual defect to detect and
                attach a representative reference image.', 'qaGateOverrideAllowedStages': ['locking', 'running'],
                'disabledBuiltInSynthesizerKeys': ['generate-tools'], 'solverRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad'}

        Attributes:
            max_import_file_size_bytes (int | None | Unset): Per-file size cap (bytes) for imported problem files. Null
                clears the override (use platform default); omit to leave unchanged. Example: 10485760.
            max_upload_file_size_bytes (int | None | Unset): Per-file size cap (bytes) for direct uploads. Null clears the
                override (use platform default); omit to leave unchanged. Example: 10485760.
            max_version_aggregate_file_size_bytes (int | None | Unset): Aggregate size cap (bytes) across all files attached
                to one problem version. Null clears the override (use platform default); omit to leave unchanged. Example:
                104857600.
            run_field_config (UpdateEnvironmentSettingsDtoRunFieldConfig | Unset): Full replacement of the attempt-count
                default for the Run problem modal. Omit to leave unchanged.
            require_lock_before_new_version (bool | Unset): When true, users must lock the current version before creating a
                new one. Omit to leave unchanged.
            problem_editor_instructions (None | str | Unset): Markdown guidance surfaced to problem editors within the
                environment. Send null to clear, or omit to leave unchanged.
            rubric_issue_template (None | str | Unset): Markdown template for new rubric issues. Send null to clear; omit to
                leave unchanged.
            global_issue_template (None | str | Unset): Markdown template for new global (non-rubric-attached) issues. Send
                null to clear; omit to leave unchanged.
            qa_gate_override_allowed_stages (list[UpdateEnvironmentSettingsDtoQaGateOverrideAllowedStagesItem] | Unset): QA-
                gate stages on which a user may override the gate verdict. Send the full set (not a delta); omit to leave
                unchanged.
            disabled_built_in_synthesizer_keys (list[UpdateEnvironmentSettingsDtoDisabledBuiltInSynthesizerKeysItem] |
                Unset): Built-in synthesizer keys to disable for this environment. Send the full set (not a delta); omit to
                leave unchanged.
            guided_tour (None | Unset | UpdateEnvironmentSettingsDtoGuidedTourType0): Authored guided-tour flow. Send null
                to clear (panel hides); omit to leave unchanged.
            preview_filename (None | str | Unset): Filename of the preview asset shown on problem cards. Send null to clear;
                omit to leave unchanged.
            solver_run_config_version_id (None | Unset | UUID): Locked run-config version to bind as the env-level solver
                default. Send null to clear the binding; omit to leave unchanged. Must reference a locked version reachable from
                this environment.
            grader_run_config_version_id (None | Unset | UUID): Locked run-config version to bind as the env-level grader
                default. Send null to clear the binding; omit to leave unchanged. Must reference a locked version reachable from
                this environment.
            programmatic_grader_run_config_version_id (None | Unset | UUID): Locked run-config version that drives all
                programmatic grading in this environment, overriding the platform-wide programmatic grader default. Send null to
                clear (falls back to the platform default); omit to leave unchanged. Must reference a locked version reachable
                from this environment.
            qa_run_config_version_id (None | Unset | UUID): Locked run-config version to bind as the env-level QA default.
                Send null to clear the binding; omit to leave unchanged. Must reference a locked version reachable from this
                environment.
            synthesizer_run_config_version_id (None | Unset | UUID): Locked run-config version to bind as the env-level
                synthesizer default. Send null to clear the binding; omit to leave unchanged. Must reference a locked version
                reachable from this environment.
     """

    max_import_file_size_bytes: int | None | Unset = UNSET
    max_upload_file_size_bytes: int | None | Unset = UNSET
    max_version_aggregate_file_size_bytes: int | None | Unset = UNSET
    run_field_config: UpdateEnvironmentSettingsDtoRunFieldConfig | Unset = UNSET
    require_lock_before_new_version: bool | Unset = UNSET
    problem_editor_instructions: None | str | Unset = UNSET
    rubric_issue_template: None | str | Unset = UNSET
    global_issue_template: None | str | Unset = UNSET
    qa_gate_override_allowed_stages: list[UpdateEnvironmentSettingsDtoQaGateOverrideAllowedStagesItem] | Unset = UNSET
    disabled_built_in_synthesizer_keys: list[UpdateEnvironmentSettingsDtoDisabledBuiltInSynthesizerKeysItem] | Unset = UNSET
    guided_tour: None | Unset | UpdateEnvironmentSettingsDtoGuidedTourType0 = UNSET
    preview_filename: None | str | Unset = UNSET
    solver_run_config_version_id: None | Unset | UUID = UNSET
    grader_run_config_version_id: None | Unset | UUID = UNSET
    programmatic_grader_run_config_version_id: None | Unset | UUID = UNSET
    qa_run_config_version_id: None | Unset | UUID = UNSET
    synthesizer_run_config_version_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_environment_settings_dto_guided_tour_type_0 import UpdateEnvironmentSettingsDtoGuidedTourType0 # noqa: PLC0415
        from ..models.update_environment_settings_dto_run_field_config import UpdateEnvironmentSettingsDtoRunFieldConfig # noqa: PLC0415
        max_import_file_size_bytes: int | None | Unset
        if isinstance(self.max_import_file_size_bytes, Unset):
            max_import_file_size_bytes = UNSET
        else:
            max_import_file_size_bytes = self.max_import_file_size_bytes

        max_upload_file_size_bytes: int | None | Unset
        if isinstance(self.max_upload_file_size_bytes, Unset):
            max_upload_file_size_bytes = UNSET
        else:
            max_upload_file_size_bytes = self.max_upload_file_size_bytes

        max_version_aggregate_file_size_bytes: int | None | Unset
        if isinstance(self.max_version_aggregate_file_size_bytes, Unset):
            max_version_aggregate_file_size_bytes = UNSET
        else:
            max_version_aggregate_file_size_bytes = self.max_version_aggregate_file_size_bytes

        run_field_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.run_field_config, Unset):
            run_field_config = self.run_field_config.to_dict()

        require_lock_before_new_version = self.require_lock_before_new_version

        problem_editor_instructions: None | str | Unset
        if isinstance(self.problem_editor_instructions, Unset):
            problem_editor_instructions = UNSET
        else:
            problem_editor_instructions = self.problem_editor_instructions

        rubric_issue_template: None | str | Unset
        if isinstance(self.rubric_issue_template, Unset):
            rubric_issue_template = UNSET
        else:
            rubric_issue_template = self.rubric_issue_template

        global_issue_template: None | str | Unset
        if isinstance(self.global_issue_template, Unset):
            global_issue_template = UNSET
        else:
            global_issue_template = self.global_issue_template

        qa_gate_override_allowed_stages: list[str] | Unset = UNSET
        if not isinstance(self.qa_gate_override_allowed_stages, Unset):
            qa_gate_override_allowed_stages = []
            for qa_gate_override_allowed_stages_item_data in self.qa_gate_override_allowed_stages:
                qa_gate_override_allowed_stages_item = qa_gate_override_allowed_stages_item_data.value
                qa_gate_override_allowed_stages.append(qa_gate_override_allowed_stages_item)



        disabled_built_in_synthesizer_keys: list[str] | Unset = UNSET
        if not isinstance(self.disabled_built_in_synthesizer_keys, Unset):
            disabled_built_in_synthesizer_keys = []
            for disabled_built_in_synthesizer_keys_item_data in self.disabled_built_in_synthesizer_keys:
                disabled_built_in_synthesizer_keys_item = disabled_built_in_synthesizer_keys_item_data.value
                disabled_built_in_synthesizer_keys.append(disabled_built_in_synthesizer_keys_item)



        guided_tour: dict[str, Any] | None | Unset
        if isinstance(self.guided_tour, Unset):
            guided_tour = UNSET
        elif isinstance(self.guided_tour, UpdateEnvironmentSettingsDtoGuidedTourType0):
            guided_tour = self.guided_tour.to_dict()
        else:
            guided_tour = self.guided_tour

        preview_filename: None | str | Unset
        if isinstance(self.preview_filename, Unset):
            preview_filename = UNSET
        else:
            preview_filename = self.preview_filename

        solver_run_config_version_id: None | str | Unset
        if isinstance(self.solver_run_config_version_id, Unset):
            solver_run_config_version_id = UNSET
        elif isinstance(self.solver_run_config_version_id, UUID):
            solver_run_config_version_id = str(self.solver_run_config_version_id)
        else:
            solver_run_config_version_id = self.solver_run_config_version_id

        grader_run_config_version_id: None | str | Unset
        if isinstance(self.grader_run_config_version_id, Unset):
            grader_run_config_version_id = UNSET
        elif isinstance(self.grader_run_config_version_id, UUID):
            grader_run_config_version_id = str(self.grader_run_config_version_id)
        else:
            grader_run_config_version_id = self.grader_run_config_version_id

        programmatic_grader_run_config_version_id: None | str | Unset
        if isinstance(self.programmatic_grader_run_config_version_id, Unset):
            programmatic_grader_run_config_version_id = UNSET
        elif isinstance(self.programmatic_grader_run_config_version_id, UUID):
            programmatic_grader_run_config_version_id = str(self.programmatic_grader_run_config_version_id)
        else:
            programmatic_grader_run_config_version_id = self.programmatic_grader_run_config_version_id

        qa_run_config_version_id: None | str | Unset
        if isinstance(self.qa_run_config_version_id, Unset):
            qa_run_config_version_id = UNSET
        elif isinstance(self.qa_run_config_version_id, UUID):
            qa_run_config_version_id = str(self.qa_run_config_version_id)
        else:
            qa_run_config_version_id = self.qa_run_config_version_id

        synthesizer_run_config_version_id: None | str | Unset
        if isinstance(self.synthesizer_run_config_version_id, Unset):
            synthesizer_run_config_version_id = UNSET
        elif isinstance(self.synthesizer_run_config_version_id, UUID):
            synthesizer_run_config_version_id = str(self.synthesizer_run_config_version_id)
        else:
            synthesizer_run_config_version_id = self.synthesizer_run_config_version_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if max_import_file_size_bytes is not UNSET:
            field_dict["maxImportFileSizeBytes"] = max_import_file_size_bytes
        if max_upload_file_size_bytes is not UNSET:
            field_dict["maxUploadFileSizeBytes"] = max_upload_file_size_bytes
        if max_version_aggregate_file_size_bytes is not UNSET:
            field_dict["maxVersionAggregateFileSizeBytes"] = max_version_aggregate_file_size_bytes
        if run_field_config is not UNSET:
            field_dict["runFieldConfig"] = run_field_config
        if require_lock_before_new_version is not UNSET:
            field_dict["requireLockBeforeNewVersion"] = require_lock_before_new_version
        if problem_editor_instructions is not UNSET:
            field_dict["problemEditorInstructions"] = problem_editor_instructions
        if rubric_issue_template is not UNSET:
            field_dict["rubricIssueTemplate"] = rubric_issue_template
        if global_issue_template is not UNSET:
            field_dict["globalIssueTemplate"] = global_issue_template
        if qa_gate_override_allowed_stages is not UNSET:
            field_dict["qaGateOverrideAllowedStages"] = qa_gate_override_allowed_stages
        if disabled_built_in_synthesizer_keys is not UNSET:
            field_dict["disabledBuiltInSynthesizerKeys"] = disabled_built_in_synthesizer_keys
        if guided_tour is not UNSET:
            field_dict["guidedTour"] = guided_tour
        if preview_filename is not UNSET:
            field_dict["previewFilename"] = preview_filename
        if solver_run_config_version_id is not UNSET:
            field_dict["solverRunConfigVersionId"] = solver_run_config_version_id
        if grader_run_config_version_id is not UNSET:
            field_dict["graderRunConfigVersionId"] = grader_run_config_version_id
        if programmatic_grader_run_config_version_id is not UNSET:
            field_dict["programmaticGraderRunConfigVersionId"] = programmatic_grader_run_config_version_id
        if qa_run_config_version_id is not UNSET:
            field_dict["qaRunConfigVersionId"] = qa_run_config_version_id
        if synthesizer_run_config_version_id is not UNSET:
            field_dict["synthesizerRunConfigVersionId"] = synthesizer_run_config_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_environment_settings_dto_guided_tour_type_0 import UpdateEnvironmentSettingsDtoGuidedTourType0 # noqa: PLC0415
        from ..models.update_environment_settings_dto_run_field_config import UpdateEnvironmentSettingsDtoRunFieldConfig # noqa: PLC0415
        d = dict(src_dict)
        def _parse_max_import_file_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_import_file_size_bytes = _parse_max_import_file_size_bytes(d.pop("maxImportFileSizeBytes", UNSET))


        def _parse_max_upload_file_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_upload_file_size_bytes = _parse_max_upload_file_size_bytes(d.pop("maxUploadFileSizeBytes", UNSET))


        def _parse_max_version_aggregate_file_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_version_aggregate_file_size_bytes = _parse_max_version_aggregate_file_size_bytes(d.pop("maxVersionAggregateFileSizeBytes", UNSET))


        _run_field_config = d.pop("runFieldConfig", UNSET)
        run_field_config: UpdateEnvironmentSettingsDtoRunFieldConfig | Unset
        if isinstance(_run_field_config,  Unset):
            run_field_config = UNSET
        else:
            run_field_config = UpdateEnvironmentSettingsDtoRunFieldConfig.from_dict(_run_field_config)




        require_lock_before_new_version = d.pop("requireLockBeforeNewVersion", UNSET)

        def _parse_problem_editor_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        problem_editor_instructions = _parse_problem_editor_instructions(d.pop("problemEditorInstructions", UNSET))


        def _parse_rubric_issue_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rubric_issue_template = _parse_rubric_issue_template(d.pop("rubricIssueTemplate", UNSET))


        def _parse_global_issue_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        global_issue_template = _parse_global_issue_template(d.pop("globalIssueTemplate", UNSET))


        _qa_gate_override_allowed_stages = d.pop("qaGateOverrideAllowedStages", UNSET)
        qa_gate_override_allowed_stages: list[UpdateEnvironmentSettingsDtoQaGateOverrideAllowedStagesItem] | Unset = UNSET
        if _qa_gate_override_allowed_stages is not UNSET:
            qa_gate_override_allowed_stages = []
            for qa_gate_override_allowed_stages_item_data in _qa_gate_override_allowed_stages:
                qa_gate_override_allowed_stages_item = UpdateEnvironmentSettingsDtoQaGateOverrideAllowedStagesItem(qa_gate_override_allowed_stages_item_data)



                qa_gate_override_allowed_stages.append(qa_gate_override_allowed_stages_item)


        _disabled_built_in_synthesizer_keys = d.pop("disabledBuiltInSynthesizerKeys", UNSET)
        disabled_built_in_synthesizer_keys: list[UpdateEnvironmentSettingsDtoDisabledBuiltInSynthesizerKeysItem] | Unset = UNSET
        if _disabled_built_in_synthesizer_keys is not UNSET:
            disabled_built_in_synthesizer_keys = []
            for disabled_built_in_synthesizer_keys_item_data in _disabled_built_in_synthesizer_keys:
                disabled_built_in_synthesizer_keys_item = UpdateEnvironmentSettingsDtoDisabledBuiltInSynthesizerKeysItem(disabled_built_in_synthesizer_keys_item_data)



                disabled_built_in_synthesizer_keys.append(disabled_built_in_synthesizer_keys_item)


        def _parse_guided_tour(data: object) -> None | Unset | UpdateEnvironmentSettingsDtoGuidedTourType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                guided_tour_type_0 = UpdateEnvironmentSettingsDtoGuidedTourType0.from_dict(data)



                return guided_tour_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateEnvironmentSettingsDtoGuidedTourType0, data)

        guided_tour = _parse_guided_tour(d.pop("guidedTour", UNSET))


        def _parse_preview_filename(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preview_filename = _parse_preview_filename(d.pop("previewFilename", UNSET))


        def _parse_solver_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                solver_run_config_version_id_type_0 = UUID(data)



                return solver_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        solver_run_config_version_id = _parse_solver_run_config_version_id(d.pop("solverRunConfigVersionId", UNSET))


        def _parse_grader_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grader_run_config_version_id_type_0 = UUID(data)



                return grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        grader_run_config_version_id = _parse_grader_run_config_version_id(d.pop("graderRunConfigVersionId", UNSET))


        def _parse_programmatic_grader_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                programmatic_grader_run_config_version_id_type_0 = UUID(data)



                return programmatic_grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        programmatic_grader_run_config_version_id = _parse_programmatic_grader_run_config_version_id(d.pop("programmaticGraderRunConfigVersionId", UNSET))


        def _parse_qa_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                qa_run_config_version_id_type_0 = UUID(data)



                return qa_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        qa_run_config_version_id = _parse_qa_run_config_version_id(d.pop("qaRunConfigVersionId", UNSET))


        def _parse_synthesizer_run_config_version_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                synthesizer_run_config_version_id_type_0 = UUID(data)



                return synthesizer_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        synthesizer_run_config_version_id = _parse_synthesizer_run_config_version_id(d.pop("synthesizerRunConfigVersionId", UNSET))


        update_environment_settings_dto = cls(
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
        )


        update_environment_settings_dto.additional_properties = d
        return update_environment_settings_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
