from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.regrade_failed_graders_response_dto_regrades_item import RegradeFailedGradersResponseDtoRegradesItem
  from ..models.regrade_failed_graders_response_dto_skipped_item import RegradeFailedGradersResponseDtoSkippedItem





T = TypeVar("T", bound="RegradeFailedGradersResponseDto")



@_attrs_define
class RegradeFailedGradersResponseDto:
    """ Result of re-grading every failed-grader run in a single run (batch).

        Example:
            {'jobV2Id': '7f6e5d4c-3b2a-4190-8d6e-9c0b1a2d3e4f', 'appliedGraderRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'regrades': [{'problemRunId': 'f3c1a2b4-5d6e-4f70-8192-a3b4c5d6e7f8',
                'regradeJobV2Id': 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'}], 'skipped': []}

        Attributes:
            job_v2_id (UUID): The run (batch root job id) that was targeted, whether supplied or resolved as the most recent
                batch.
            applied_grader_run_config_version_id (None | UUID): The grader run-config version applied to every re-grade, or
                null when each run re-resolved its existing grader binding.
            regrades (list[RegradeFailedGradersResponseDtoRegradesItem]): The runs for which a re-grade was enqueued, one
                entry each.
            skipped (list[RegradeFailedGradersResponseDtoSkippedItem]): Runs that qualified for re-grade but were not
                enqueued, with a reason each.
     """

    job_v2_id: UUID
    applied_grader_run_config_version_id: None | UUID
    regrades: list[RegradeFailedGradersResponseDtoRegradesItem]
    skipped: list[RegradeFailedGradersResponseDtoSkippedItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.regrade_failed_graders_response_dto_regrades_item import RegradeFailedGradersResponseDtoRegradesItem # noqa: PLC0415
        from ..models.regrade_failed_graders_response_dto_skipped_item import RegradeFailedGradersResponseDtoSkippedItem # noqa: PLC0415
        job_v2_id = str(self.job_v2_id)

        applied_grader_run_config_version_id: None | str
        if isinstance(self.applied_grader_run_config_version_id, UUID):
            applied_grader_run_config_version_id = str(self.applied_grader_run_config_version_id)
        else:
            applied_grader_run_config_version_id = self.applied_grader_run_config_version_id

        regrades = []
        for regrades_item_data in self.regrades:
            regrades_item = regrades_item_data.to_dict()
            regrades.append(regrades_item)



        skipped = []
        for skipped_item_data in self.skipped:
            skipped_item = skipped_item_data.to_dict()
            skipped.append(skipped_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "jobV2Id": job_v2_id,
            "appliedGraderRunConfigVersionId": applied_grader_run_config_version_id,
            "regrades": regrades,
            "skipped": skipped,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.regrade_failed_graders_response_dto_regrades_item import RegradeFailedGradersResponseDtoRegradesItem # noqa: PLC0415
        from ..models.regrade_failed_graders_response_dto_skipped_item import RegradeFailedGradersResponseDtoSkippedItem # noqa: PLC0415
        d = dict(src_dict)
        job_v2_id = UUID(d.pop("jobV2Id"))




        def _parse_applied_grader_run_config_version_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applied_grader_run_config_version_id_type_0 = UUID(data)



                return applied_grader_run_config_version_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        applied_grader_run_config_version_id = _parse_applied_grader_run_config_version_id(d.pop("appliedGraderRunConfigVersionId"))


        regrades = []
        _regrades = d.pop("regrades")
        for regrades_item_data in (_regrades):
            regrades_item = RegradeFailedGradersResponseDtoRegradesItem.from_dict(regrades_item_data)



            regrades.append(regrades_item)


        skipped = []
        _skipped = d.pop("skipped")
        for skipped_item_data in (_skipped):
            skipped_item = RegradeFailedGradersResponseDtoSkippedItem.from_dict(skipped_item_data)



            skipped.append(skipped_item)


        regrade_failed_graders_response_dto = cls(
            job_v2_id=job_v2_id,
            applied_grader_run_config_version_id=applied_grader_run_config_version_id,
            regrades=regrades,
            skipped=skipped,
        )

        return regrade_failed_graders_response_dto

