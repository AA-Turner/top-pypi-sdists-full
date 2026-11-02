from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SshHostKey")


@_attrs_define
class SshHostKey:
    """
    Attributes:
        public_key (str):
        fingerprint (str):
        known_hosts (str):
    """

    public_key: str
    fingerprint: str
    known_hosts: str

    def to_dict(self) -> dict[str, Any]:
        public_key = self.public_key

        fingerprint = self.fingerprint

        known_hosts = self.known_hosts

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "public_key": public_key,
                "fingerprint": fingerprint,
                "known_hosts": known_hosts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        public_key = d.pop("public_key")

        fingerprint = d.pop("fingerprint")

        known_hosts = d.pop("known_hosts")

        ssh_host_key = cls(
            public_key=public_key,
            fingerprint=fingerprint,
            known_hosts=known_hosts,
        )

        return ssh_host_key
