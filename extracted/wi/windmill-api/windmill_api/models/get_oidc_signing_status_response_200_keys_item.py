from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_oidc_signing_status_response_200_keys_item_source import GetOidcSigningStatusResponse200KeysItemSource
from ..models.get_oidc_signing_status_response_200_keys_item_state import GetOidcSigningStatusResponse200KeysItemState
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetOidcSigningStatusResponse200KeysItem")


@_attrs_define
class GetOidcSigningStatusResponse200KeysItem:
    """
    Attributes:
        alg (str):
        state (GetOidcSigningStatusResponse200KeysItemState):
        source (GetOidcSigningStatusResponse200KeysItemSource):
        kid (Union[Unset, str]):
    """

    alg: str
    state: GetOidcSigningStatusResponse200KeysItemState
    source: GetOidcSigningStatusResponse200KeysItemSource
    kid: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        alg = self.alg
        state = self.state.value

        source = self.source.value

        kid = self.kid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alg": alg,
                "state": state,
                "source": source,
            }
        )
        if kid is not UNSET:
            field_dict["kid"] = kid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        alg = d.pop("alg")

        state = GetOidcSigningStatusResponse200KeysItemState(d.pop("state"))

        source = GetOidcSigningStatusResponse200KeysItemSource(d.pop("source"))

        kid = d.pop("kid", UNSET)

        get_oidc_signing_status_response_200_keys_item = cls(
            alg=alg,
            state=state,
            source=source,
            kid=kid,
        )

        get_oidc_signing_status_response_200_keys_item.additional_properties = d
        return get_oidc_signing_status_response_200_keys_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
