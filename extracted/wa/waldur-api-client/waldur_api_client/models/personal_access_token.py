import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PersonalAccessToken")


@_attrs_define
class PersonalAccessToken:
    """
    Attributes:
        uuid (UUID):
        name (str):
        token_prefix (str):
        scopes (list[str]):
        expires_at (datetime.datetime):
        is_active (bool):
        last_used_at (datetime.datetime):
        last_used_ip (str): An IPv4 or IPv6 address.
        use_count (int):
        created (datetime.datetime):
    """

    uuid: UUID
    name: str
    token_prefix: str
    scopes: list[str]
    expires_at: datetime.datetime
    is_active: bool
    last_used_at: datetime.datetime
    last_used_ip: str
    use_count: int
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        token_prefix = self.token_prefix

        scopes = self.scopes

        expires_at = self.expires_at.isoformat()

        is_active = self.is_active

        last_used_at = self.last_used_at.isoformat()

        last_used_ip: str
        last_used_ip = self.last_used_ip

        use_count = self.use_count

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "token_prefix": token_prefix,
                "scopes": scopes,
                "expires_at": expires_at,
                "is_active": is_active,
                "last_used_at": last_used_at,
                "last_used_ip": last_used_ip,
                "use_count": use_count,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        token_prefix = d.pop("token_prefix")

        scopes = cast(list[str], d.pop("scopes"))

        expires_at = isoparse(d.pop("expires_at"))

        is_active = d.pop("is_active")

        last_used_at = isoparse(d.pop("last_used_at"))

        def _parse_last_used_ip(data: object) -> str:
            return cast(str, data)

        last_used_ip = _parse_last_used_ip(d.pop("last_used_ip"))

        use_count = d.pop("use_count")

        created = isoparse(d.pop("created"))

        personal_access_token = cls(
            uuid=uuid,
            name=name,
            token_prefix=token_prefix,
            scopes=scopes,
            expires_at=expires_at,
            is_active=is_active,
            last_used_at=last_used_at,
            last_used_ip=last_used_ip,
            use_count=use_count,
            created=created,
        )

        personal_access_token.additional_properties = d
        return personal_access_token

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
