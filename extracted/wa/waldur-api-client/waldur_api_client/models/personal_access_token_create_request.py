import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allowed_scope_input_request import AllowedScopeInputRequest


T = TypeVar("T", bound="PersonalAccessTokenCreateRequest")


@_attrs_define
class PersonalAccessTokenCreateRequest:
    """
    Attributes:
        name (str):
        scopes (list[str]):
        expires_at (datetime.datetime):
        allowed_scopes (Union[Unset, list['AllowedScopeInputRequest']]): Optional list of entity bindings restricting
            where this token can act. Empty list = no entity restriction.
        allowed_networks (Union[Unset, list[str]]): Optional list of CIDR networks the token may be used from. Bare
            addresses are widened to /32 or /128. Empty list = no network restriction.
    """

    name: str
    scopes: list[str]
    expires_at: datetime.datetime
    allowed_scopes: Union[Unset, list["AllowedScopeInputRequest"]] = UNSET
    allowed_networks: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        scopes = self.scopes

        expires_at = self.expires_at.isoformat()

        allowed_scopes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.allowed_scopes, Unset):
            allowed_scopes = []
            for allowed_scopes_item_data in self.allowed_scopes:
                allowed_scopes_item = allowed_scopes_item_data.to_dict()
                allowed_scopes.append(allowed_scopes_item)

        allowed_networks: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_networks, Unset):
            allowed_networks = self.allowed_networks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "scopes": scopes,
                "expires_at": expires_at,
            }
        )
        if allowed_scopes is not UNSET:
            field_dict["allowed_scopes"] = allowed_scopes
        if allowed_networks is not UNSET:
            field_dict["allowed_networks"] = allowed_networks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowed_scope_input_request import AllowedScopeInputRequest

        d = dict(src_dict)
        name = d.pop("name")

        scopes = cast(list[str], d.pop("scopes"))

        expires_at = isoparse(d.pop("expires_at"))

        allowed_scopes = []
        _allowed_scopes = d.pop("allowed_scopes", UNSET)
        for allowed_scopes_item_data in _allowed_scopes or []:
            allowed_scopes_item = AllowedScopeInputRequest.from_dict(allowed_scopes_item_data)

            allowed_scopes.append(allowed_scopes_item)

        allowed_networks = cast(list[str], d.pop("allowed_networks", UNSET))

        personal_access_token_create_request = cls(
            name=name,
            scopes=scopes,
            expires_at=expires_at,
            allowed_scopes=allowed_scopes,
            allowed_networks=allowed_networks,
        )

        personal_access_token_create_request.additional_properties = d
        return personal_access_token_create_request

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
