import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="UserConsentInfo")


@_attrs_define
class UserConsentInfo:
    """
    Attributes:
        uuid (UUID):
        version (str):
        agreement_date (datetime.datetime):
        is_revoked (bool):
    """

    uuid: UUID
    version: str
    agreement_date: datetime.datetime
    is_revoked: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        version = self.version

        agreement_date = self.agreement_date.isoformat()

        is_revoked = self.is_revoked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "version": version,
                "agreement_date": agreement_date,
                "is_revoked": is_revoked,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        version = d.pop("version")

        agreement_date = isoparse(d.pop("agreement_date"))

        is_revoked = d.pop("is_revoked")

        user_consent_info = cls(
            uuid=uuid,
            version=version,
            agreement_date=agreement_date,
            is_revoked=is_revoked,
        )

        user_consent_info.additional_properties = d
        return user_consent_info

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
