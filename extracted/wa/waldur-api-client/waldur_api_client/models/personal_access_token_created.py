import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.allowed_scope_output import AllowedScopeOutput


T = TypeVar("T", bound="PersonalAccessTokenCreated")


@_attrs_define
class PersonalAccessTokenCreated:
    """
    Attributes:
        uuid (UUID):
        name (str):
        token (str): Plaintext token — shown only once.
        scopes (list[str]):
        allowed_scopes (list['AllowedScopeOutput']):
        allowed_networks (list[str]):
        expires_at (datetime.datetime):
        created (datetime.datetime):
    """

    uuid: UUID
    name: str
    token: str
    scopes: list[str]
    allowed_scopes: list["AllowedScopeOutput"]
    allowed_networks: list[str]
    expires_at: datetime.datetime
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        token = self.token

        scopes = self.scopes

        allowed_scopes = []
        for allowed_scopes_item_data in self.allowed_scopes:
            allowed_scopes_item = allowed_scopes_item_data.to_dict()
            allowed_scopes.append(allowed_scopes_item)

        allowed_networks = self.allowed_networks

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
                "allowed_scopes": allowed_scopes,
                "allowed_networks": allowed_networks,
                "expires_at": expires_at,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowed_scope_output import AllowedScopeOutput

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        token = d.pop("token")

        scopes = cast(list[str], d.pop("scopes"))

        allowed_scopes = []
        _allowed_scopes = d.pop("allowed_scopes")
        for allowed_scopes_item_data in _allowed_scopes:
            allowed_scopes_item = AllowedScopeOutput.from_dict(allowed_scopes_item_data)

            allowed_scopes.append(allowed_scopes_item)

        allowed_networks = cast(list[str], d.pop("allowed_networks"))

        expires_at = isoparse(d.pop("expires_at"))

        created = isoparse(d.pop("created"))

        personal_access_token_created = cls(
            uuid=uuid,
            name=name,
            token=token,
            scopes=scopes,
            allowed_scopes=allowed_scopes,
            allowed_networks=allowed_networks,
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
