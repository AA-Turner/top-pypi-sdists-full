import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.update_draft_response_200_status import UpdateDraftResponse200Status

T = TypeVar("T", bound="UpdateDraftResponse200")


@_attrs_define
class UpdateDraftResponse200:
    """
    Attributes:
        status (UpdateDraftResponse200Status):
        current_timestamp (datetime.datetime):
    """

    status: UpdateDraftResponse200Status
    current_timestamp: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        current_timestamp = self.current_timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "current_timestamp": current_timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = UpdateDraftResponse200Status(d.pop("status"))

        current_timestamp = isoparse(d.pop("current_timestamp"))

        update_draft_response_200 = cls(
            status=status,
            current_timestamp=current_timestamp,
        )

        update_draft_response_200.additional_properties = d
        return update_draft_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
