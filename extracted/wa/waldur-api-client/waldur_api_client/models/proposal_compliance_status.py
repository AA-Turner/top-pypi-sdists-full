import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProposalComplianceStatus")


@_attrs_define
class ProposalComplianceStatus:
    """
    Attributes:
        has_checklist (bool):
        is_completed (bool):
        requires_review (bool):
        completion_percentage (int):
        reviewed_by (Union[None, str]):
        reviewed_at (Union[None, datetime.datetime]):
        error (Union[Unset, str]):
        checklist_name (Union[Unset, str]):
        unanswered_required_count (Union[Unset, int]):
    """

    has_checklist: bool
    is_completed: bool
    requires_review: bool
    completion_percentage: int
    reviewed_by: Union[None, str]
    reviewed_at: Union[None, datetime.datetime]
    error: Union[Unset, str] = UNSET
    checklist_name: Union[Unset, str] = UNSET
    unanswered_required_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_checklist = self.has_checklist

        is_completed = self.is_completed

        requires_review = self.requires_review

        completion_percentage = self.completion_percentage

        reviewed_by: Union[None, str]
        reviewed_by = self.reviewed_by

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        error = self.error

        checklist_name = self.checklist_name

        unanswered_required_count = self.unanswered_required_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_checklist": has_checklist,
                "is_completed": is_completed,
                "requires_review": requires_review,
                "completion_percentage": completion_percentage,
                "reviewed_by": reviewed_by,
                "reviewed_at": reviewed_at,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if checklist_name is not UNSET:
            field_dict["checklist_name"] = checklist_name
        if unanswered_required_count is not UNSET:
            field_dict["unanswered_required_count"] = unanswered_required_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        has_checklist = d.pop("has_checklist")

        is_completed = d.pop("is_completed")

        requires_review = d.pop("requires_review")

        completion_percentage = d.pop("completion_percentage")

        def _parse_reviewed_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by"))

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        error = d.pop("error", UNSET)

        checklist_name = d.pop("checklist_name", UNSET)

        unanswered_required_count = d.pop("unanswered_required_count", UNSET)

        proposal_compliance_status = cls(
            has_checklist=has_checklist,
            is_completed=is_completed,
            requires_review=requires_review,
            completion_percentage=completion_percentage,
            reviewed_by=reviewed_by,
            reviewed_at=reviewed_at,
            error=error,
            checklist_name=checklist_name,
            unanswered_required_count=unanswered_required_count,
        )

        proposal_compliance_status.additional_properties = d
        return proposal_compliance_status

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
