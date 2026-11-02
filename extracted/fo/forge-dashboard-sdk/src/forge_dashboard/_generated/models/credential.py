from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="Credential")



@_attrs_define
class Credential:
    """ A registered passkey's own metadata — never the
    credential itself, which never leaves the authenticator that
    created it; WebAuthn's whole design is that the server only ever
    sees a public key and signed assertions, not a secret to lose.

        Attributes:
            id (str): This passkey's own credential ID (base64url), distinct from the account's user ID.
            label (str): The passkey's name, given at registration and changeable with `PATCH
                /api/v1/auth/credentials/{id}`. Empty when it was never named; clients then fall back to `createdAt`.
            created_at (datetime.datetime):
     """

    id: str
    label: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        label = self.label

        created_at = self.created_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "label": label,
            "createdAt": created_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        label = d.pop("label")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        credential = cls(
            id=id,
            label=label,
            created_at=created_at,
        )


        credential.additional_properties = d
        return credential

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
