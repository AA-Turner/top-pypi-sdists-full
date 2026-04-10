import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PersonalAccessTokenCreated")


@_attrs_define
class PersonalAccessTokenCreated:
    """
    Attributes:
        uuid (UUID):
        name (str):
        token (str): Plaintext token — shown only once.
        scopes (list[str]):
        expires_at (datetime.datetime):
        created (datetime.datetime):
    """

    uuid: UUID
    name: str
    token: str
    scopes: list[str]
    expires_at: datetime.datetime
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        token = self.token

        scopes = self.scopes

        expires_at = self.expires_at.isoformat()

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "token": token,
                "scopes": scopes,
                "expires_at": expires_at,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        token = d.pop("token")

        scopes = cast(list[str], d.pop("scopes"))

        expires_at = isoparse(d.pop("expires_at"))

        created = isoparse(d.pop("created"))

        personal_access_token_created = cls(
            uuid=uuid,
            name=name,
            token=token,
            scopes=scopes,
            expires_at=expires_at,
            created=created,
        )

        personal_access_token_created.additional_properties = d
        return personal_access_token_created

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
