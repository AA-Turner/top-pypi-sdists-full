from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.coi_status_update_status_enum import COIStatusUpdateStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="COIStatusUpdateRequest")


@_attrs_define
class COIStatusUpdateRequest:
    """
    Attributes:
        status (COIStatusUpdateStatusEnum):
        review_notes (Union[Unset, str]):
        management_plan (Union[Unset, str]): Required when status is 'waived'
    """

    status: COIStatusUpdateStatusEnum
    review_notes: Union[Unset, str] = UNSET
    management_plan: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        review_notes = self.review_notes

        management_plan = self.management_plan

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if review_notes is not UNSET:
            field_dict["review_notes"] = review_notes
        if management_plan is not UNSET:
            field_dict["management_plan"] = management_plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = COIStatusUpdateStatusEnum(d.pop("status"))

        review_notes = d.pop("review_notes", UNSET)

        management_plan = d.pop("management_plan", UNSET)

        coi_status_update_request = cls(
            status=status,
            review_notes=review_notes,
            management_plan=management_plan,
        )

        coi_status_update_request.additional_properties = d
        return coi_status_update_request

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
