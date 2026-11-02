from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_oidc_signing_status_response_200_mode import GetOidcSigningStatusResponse200Mode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_oidc_signing_status_response_200_keys_item import GetOidcSigningStatusResponse200KeysItem
    from ..models.get_oidc_signing_status_response_200_signer import GetOidcSigningStatusResponse200Signer


T = TypeVar("T", bound="GetOidcSigningStatusResponse200")


@_attrs_define
class GetOidcSigningStatusResponse200:
    """
    Attributes:
        mode (GetOidcSigningStatusResponse200Mode):
        keys (List['GetOidcSigningStatusResponse200KeysItem']):
        signer (Union[Unset, GetOidcSigningStatusResponse200Signer]): set when an external signer is configured
    """

    mode: GetOidcSigningStatusResponse200Mode
    keys: List["GetOidcSigningStatusResponse200KeysItem"]
    signer: Union[Unset, "GetOidcSigningStatusResponse200Signer"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mode = self.mode.value

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()

            keys.append(keys_item)

        signer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.signer, Unset):
            signer = self.signer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "keys": keys,
            }
        )
        if signer is not UNSET:
            field_dict["signer"] = signer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_oidc_signing_status_response_200_keys_item import GetOidcSigningStatusResponse200KeysItem
        from ..models.get_oidc_signing_status_response_200_signer import GetOidcSigningStatusResponse200Signer

        d = src_dict.copy()
        mode = GetOidcSigningStatusResponse200Mode(d.pop("mode"))

        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = GetOidcSigningStatusResponse200KeysItem.from_dict(keys_item_data)

            keys.append(keys_item)

        _signer = d.pop("signer", UNSET)
        signer: Union[Unset, GetOidcSigningStatusResponse200Signer]
        if isinstance(_signer, Unset):
            signer = UNSET
        else:
            signer = GetOidcSigningStatusResponse200Signer.from_dict(_signer)

        get_oidc_signing_status_response_200 = cls(
            mode=mode,
            keys=keys,
            signer=signer,
        )

        get_oidc_signing_status_response_200.additional_properties = d
        return get_oidc_signing_status_response_200

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
