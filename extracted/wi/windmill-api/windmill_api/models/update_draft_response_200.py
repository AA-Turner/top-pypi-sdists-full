import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.update_draft_response_200_status import UpdateDraftResponse200Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDraftResponse200")


@_attrs_define
class UpdateDraftResponse200:
    """
    Attributes:
        status (UpdateDraftResponse200Status):
        current_timestamp (datetime.datetime):
        path (Union[Unset, str]): `saved` only, upsert or delete: where the write landed. Differs from the URL path when
            the item had moved away from it; the editor follows it there. Absent when a delete found nothing to remove and
            the caller cannot read the path it moved to.
    """

    status: UpdateDraftResponse200Status
    current_timestamp: datetime.datetime
    path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        current_timestamp = self.current_timestamp.isoformat()

        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "current_timestamp": current_timestamp,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = UpdateDraftResponse200Status(d.pop("status"))

        current_timestamp = isoparse(d.pop("current_timestamp"))

        path = d.pop("path", UNSET)

        update_draft_response_200 = cls(
            status=status,
            current_timestamp=current_timestamp,
            path=path,
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
