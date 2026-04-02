from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvitationDuplicate")


@_attrs_define
class InvitationDuplicate:
    """
    Attributes:
        email (str):
        role (UUID):
        existing_invitation_uuid (Union[None, UUID, Unset]):
    """

    email: str
    role: UUID
    existing_invitation_uuid: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = str(self.role)

        existing_invitation_uuid: Union[None, Unset, str]
        if isinstance(self.existing_invitation_uuid, Unset):
            existing_invitation_uuid = UNSET
        elif isinstance(self.existing_invitation_uuid, UUID):
            existing_invitation_uuid = str(self.existing_invitation_uuid)
        else:
            existing_invitation_uuid = self.existing_invitation_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "role": role,
            }
        )
        if existing_invitation_uuid is not UNSET:
            field_dict["existing_invitation_uuid"] = existing_invitation_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        role = UUID(d.pop("role"))

        def _parse_existing_invitation_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                existing_invitation_uuid_type_0 = UUID(data)

                return existing_invitation_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        existing_invitation_uuid = _parse_existing_invitation_uuid(d.pop("existing_invitation_uuid", UNSET))

        invitation_duplicate = cls(
            email=email,
            role=role,
            existing_invitation_uuid=existing_invitation_uuid,
        )

        invitation_duplicate.additional_properties = d
        return invitation_duplicate

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
