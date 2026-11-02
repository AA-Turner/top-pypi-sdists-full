from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreateSshKeyRequest")


@_attrs_define
class CreateSshKeyRequest:
    """
    Attributes:
        display_name (str):
        public_key (str):
    """

    display_name: str
    public_key: str

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        public_key = self.public_key

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "display_name": display_name,
                "public_key": public_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_name = d.pop("display_name")

        public_key = d.pop("public_key")

        create_ssh_key_request = cls(
            display_name=display_name,
            public_key=public_key,
        )

        return create_ssh_key_request
