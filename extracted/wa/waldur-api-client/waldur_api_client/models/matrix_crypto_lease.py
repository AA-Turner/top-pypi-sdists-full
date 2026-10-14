import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="MatrixCryptoLease")


@_attrs_define
class MatrixCryptoLease:
    """
    Attributes:
        lease (str):
        expires_at (datetime.datetime):
        temporary_password (Union[None, str]): For a reset only: the password to answer the homeserver's interactive
            auth with. Replaced once the new key is escrowed.
    """

    lease: str
    expires_at: datetime.datetime
    temporary_password: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lease = self.lease

        expires_at = self.expires_at.isoformat()

        temporary_password: Union[None, str]
        temporary_password = self.temporary_password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lease": lease,
                "expires_at": expires_at,
                "temporary_password": temporary_password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lease = d.pop("lease")

        expires_at = isoparse(d.pop("expires_at"))

        def _parse_temporary_password(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        temporary_password = _parse_temporary_password(d.pop("temporary_password"))

        matrix_crypto_lease = cls(
            lease=lease,
            expires_at=expires_at,
            temporary_password=temporary_password,
        )

        matrix_crypto_lease.additional_properties = d
        return matrix_crypto_lease

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
