from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SshKey")


@_attrs_define
class SshKey:
    """Organization-scoped personal SSH public key metadata.

    Attributes:
        id (str):
        organization_id (str):
        user_id (str):
        display_name (str):
        public_key (str):
        fingerprint (str):
        created_at (datetime.datetime):
    """

    id: str
    organization_id: str
    user_id: str
    display_name: str
    public_key: str
    fingerprint: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        organization_id = self.organization_id

        user_id = self.user_id

        display_name = self.display_name

        public_key = self.public_key

        fingerprint = self.fingerprint

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organization_id": organization_id,
                "user_id": user_id,
                "display_name": display_name,
                "public_key": public_key,
                "fingerprint": fingerprint,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        user_id = d.pop("user_id")

        display_name = d.pop("display_name")

        public_key = d.pop("public_key")

        fingerprint = d.pop("fingerprint")

        created_at = datetime.datetime.fromisoformat(
            d.pop("created_at").replace("Z", "+00:00")
        )

        ssh_key = cls(
            id=id,
            organization_id=organization_id,
            user_id=user_id,
            display_name=display_name,
            public_key=public_key,
            fingerprint=fingerprint,
            created_at=created_at,
        )

        ssh_key.additional_properties = d
        return ssh_key

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
