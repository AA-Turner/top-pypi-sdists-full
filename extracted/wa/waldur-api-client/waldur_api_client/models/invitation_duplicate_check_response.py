from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.invitation_duplicate import InvitationDuplicate


T = TypeVar("T", bound="InvitationDuplicateCheckResponse")


@_attrs_define
class InvitationDuplicateCheckResponse:
    """
    Attributes:
        duplicates (list['InvitationDuplicate']):
    """

    duplicates: list["InvitationDuplicate"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duplicates = []
        for duplicates_item_data in self.duplicates:
            duplicates_item = duplicates_item_data.to_dict()
            duplicates.append(duplicates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "duplicates": duplicates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invitation_duplicate import InvitationDuplicate

        d = dict(src_dict)
        duplicates = []
        _duplicates = d.pop("duplicates")
        for duplicates_item_data in _duplicates:
            duplicates_item = InvitationDuplicate.from_dict(duplicates_item_data)

            duplicates.append(duplicates_item)

        invitation_duplicate_check_response = cls(
            duplicates=duplicates,
        )

        invitation_duplicate_check_response.additional_properties = d
        return invitation_duplicate_check_response

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
