from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_taiga_submission_body_dto_job_config_overrides import CreateTaigaSubmissionBodyDtoJobConfigOverrides





T = TypeVar("T", bound="CreateTaigaSubmissionBodyDto")



@_attrs_define
class CreateTaigaSubmissionBodyDto:
    """ Request body for createTaigaSubmission. Recursion environmentId comes from the path; the Taiga-side env id travels
    in the body; problemIds resolve to their latest versions server-side.

        Attributes:
            taiga_env_id (str): Taiga-side environment id, pasted by the user into the Send-to-Taiga dialog. Restricted to
                /^[a-zA-Z0-9_-]{1,255}$/ to prevent URL path injection (the value is interpolated into authenticated Taiga
                URLs). Server does NOT round-trip to Taiga to verify the id exists; a syntactically-valid-but-unknown id
                surfaces as a Taiga 4xx in the submit-job child.
            problem_ids (list[UUID]): Recursion problem ids selected for submission; each is resolved to its latest active
                problem version server-side.
            job_config_overrides (CreateTaigaSubmissionBodyDtoJobConfigOverrides | Unset): Per-submission overrides for
                Taiga job-level controls. Omitted fields fall back to the environment integration defaults.
            taiga_image_url (str | Unset): Per-submission override for the Taiga container image URL (must reference a ready
                row in the org catalog). Omitted falls back to environment_taiga_integrations.taiga_image_url. If neither is
                set, the submission is rejected with a clear "pick an image" error.
            import_problem_run_results (bool | Unset): Per-submission override for whether Taiga problem-runs are imported
                back into Recursion as problem_run rows. When omitted, falls back to the environment-level default.
     """

    taiga_env_id: str
    problem_ids: list[UUID]
    job_config_overrides: CreateTaigaSubmissionBodyDtoJobConfigOverrides | Unset = UNSET
    taiga_image_url: str | Unset = UNSET
    import_problem_run_results: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_taiga_submission_body_dto_job_config_overrides import CreateTaigaSubmissionBodyDtoJobConfigOverrides # noqa: PLC0415
        taiga_env_id = self.taiga_env_id

        problem_ids = []
        for problem_ids_item_data in self.problem_ids:
            problem_ids_item = str(problem_ids_item_data)
            problem_ids.append(problem_ids_item)



        job_config_overrides: dict[str, Any] | Unset = UNSET
        if not isinstance(self.job_config_overrides, Unset):
            job_config_overrides = self.job_config_overrides.to_dict()

        taiga_image_url = self.taiga_image_url

        import_problem_run_results = self.import_problem_run_results


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "taigaEnvId": taiga_env_id,
            "problemIds": problem_ids,
        })
        if job_config_overrides is not UNSET:
            field_dict["jobConfigOverrides"] = job_config_overrides
        if taiga_image_url is not UNSET:
            field_dict["taigaImageUrl"] = taiga_image_url
        if import_problem_run_results is not UNSET:
            field_dict["importProblemRunResults"] = import_problem_run_results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_taiga_submission_body_dto_job_config_overrides import CreateTaigaSubmissionBodyDtoJobConfigOverrides # noqa: PLC0415
        d = dict(src_dict)
        taiga_env_id = d.pop("taigaEnvId")

        problem_ids = []
        _problem_ids = d.pop("problemIds")
        for problem_ids_item_data in (_problem_ids):
            problem_ids_item = UUID(problem_ids_item_data)



            problem_ids.append(problem_ids_item)


        _job_config_overrides = d.pop("jobConfigOverrides", UNSET)
        job_config_overrides: CreateTaigaSubmissionBodyDtoJobConfigOverrides | Unset
        if isinstance(_job_config_overrides,  Unset):
            job_config_overrides = UNSET
        else:
            job_config_overrides = CreateTaigaSubmissionBodyDtoJobConfigOverrides.from_dict(_job_config_overrides)




        taiga_image_url = d.pop("taigaImageUrl", UNSET)

        import_problem_run_results = d.pop("importProblemRunResults", UNSET)

        create_taiga_submission_body_dto = cls(
            taiga_env_id=taiga_env_id,
            problem_ids=problem_ids,
            job_config_overrides=job_config_overrides,
            taiga_image_url=taiga_image_url,
            import_problem_run_results=import_problem_run_results,
        )


        create_taiga_submission_body_dto.additional_properties = d
        return create_taiga_submission_body_dto

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
