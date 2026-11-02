from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.ssh_host_key import SshHostKey


T = TypeVar("T", bound="SshHostKeyResponse")


@_attrs_define
class SshHostKeyResponse:
    """
    Attributes:
        data (SshHostKey):
    """

    data: SshHostKey

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ssh_host_key import SshHostKey

        d = dict(src_dict)
        data = SshHostKey.from_dict(d.pop("data"))

        ssh_host_key_response = cls(
            data=data,
        )

        return ssh_host_key_response
