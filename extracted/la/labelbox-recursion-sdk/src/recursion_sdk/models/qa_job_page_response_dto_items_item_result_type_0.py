from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.qa_job_page_response_dto_items_item_result_type_0_artifacts_item import QaJobPageResponseDtoItemsItemResultType0ArtifactsItem
  from ..models.qa_job_page_response_dto_items_item_result_type_0_details_type_0 import QaJobPageResponseDtoItemsItemResultType0DetailsType0
  from ..models.qa_job_page_response_dto_items_item_result_type_0_issues_item import QaJobPageResponseDtoItemsItemResultType0IssuesItem





T = TypeVar("T", bound="QaJobPageResponseDtoItemsItemResultType0")



@_attrs_define
class QaJobPageResponseDtoItemsItemResultType0:
    """ Detail payload of a completed QA job, exposed alongside the job row.

        Attributes:
            summary (None | str): Short natural-language summary copied from the QA container result.
            issues (list[QaJobPageResponseDtoItemsItemResultType0IssuesItem]): Issues reported by the QA container; empty
                when none were reported.
            details (None | QaJobPageResponseDtoItemsItemResultType0DetailsType0): Free-form structured detail payload from
                the QA container.
            artifacts (list[QaJobPageResponseDtoItemsItemResultType0ArtifactsItem]): Artifacts emitted by the QA container;
                empty when none were emitted.
     """

    summary: None | str
    issues: list[QaJobPageResponseDtoItemsItemResultType0IssuesItem]
    details: None | QaJobPageResponseDtoItemsItemResultType0DetailsType0
    artifacts: list[QaJobPageResponseDtoItemsItemResultType0ArtifactsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.qa_job_page_response_dto_items_item_result_type_0_artifacts_item import QaJobPageResponseDtoItemsItemResultType0ArtifactsItem # noqa: PLC0415
        from ..models.qa_job_page_response_dto_items_item_result_type_0_details_type_0 import QaJobPageResponseDtoItemsItemResultType0DetailsType0 # noqa: PLC0415
        from ..models.qa_job_page_response_dto_items_item_result_type_0_issues_item import QaJobPageResponseDtoItemsItemResultType0IssuesItem # noqa: PLC0415
        summary: None | str
        summary = self.summary

        issues = []
        for issues_item_data in self.issues:
            issues_item = issues_item_data.to_dict()
            issues.append(issues_item)



        details: dict[str, Any] | None
        if isinstance(self.details, QaJobPageResponseDtoItemsItemResultType0DetailsType0):
            details = self.details.to_dict()
        else:
            details = self.details

        artifacts = []
        for artifacts_item_data in self.artifacts:
            artifacts_item = artifacts_item_data.to_dict()
            artifacts.append(artifacts_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "summary": summary,
            "issues": issues,
            "details": details,
            "artifacts": artifacts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qa_job_page_response_dto_items_item_result_type_0_artifacts_item import QaJobPageResponseDtoItemsItemResultType0ArtifactsItem # noqa: PLC0415
        from ..models.qa_job_page_response_dto_items_item_result_type_0_details_type_0 import QaJobPageResponseDtoItemsItemResultType0DetailsType0 # noqa: PLC0415
        from ..models.qa_job_page_response_dto_items_item_result_type_0_issues_item import QaJobPageResponseDtoItemsItemResultType0IssuesItem # noqa: PLC0415
        d = dict(src_dict)
        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))


        issues = []
        _issues = d.pop("issues")
        for issues_item_data in (_issues):
            issues_item = QaJobPageResponseDtoItemsItemResultType0IssuesItem.from_dict(issues_item_data)



            issues.append(issues_item)


        def _parse_details(data: object) -> None | QaJobPageResponseDtoItemsItemResultType0DetailsType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                details_type_0 = QaJobPageResponseDtoItemsItemResultType0DetailsType0.from_dict(data)



                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QaJobPageResponseDtoItemsItemResultType0DetailsType0, data)

        details = _parse_details(d.pop("details"))


        artifacts = []
        _artifacts = d.pop("artifacts")
        for artifacts_item_data in (_artifacts):
            artifacts_item = QaJobPageResponseDtoItemsItemResultType0ArtifactsItem.from_dict(artifacts_item_data)



            artifacts.append(artifacts_item)


        qa_job_page_response_dto_items_item_result_type_0 = cls(
            summary=summary,
            issues=issues,
            details=details,
            artifacts=artifacts,
        )

        return qa_job_page_response_dto_items_item_result_type_0

