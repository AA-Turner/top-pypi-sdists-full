from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_o_auth_connect_response_200_extra_params import GetOAuthConnectResponse200ExtraParams


T = TypeVar("T", bound="GetOAuthConnectResponse200")


@_attrs_define
class GetOAuthConnectResponse200:
    """
    Attributes:
        extra_params (Union[Unset, GetOAuthConnectResponse200ExtraParams]):
        scopes (Union[Unset, List[str]]):
    """

    extra_params: Union[Unset, "GetOAuthConnectResponse200ExtraParams"] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        extra_params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_params, Unset):
            extra_params = self.extra_params.to_dict()

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extra_params is not UNSET:
            field_dict["extra_params"] = extra_params
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_o_auth_connect_response_200_extra_params import GetOAuthConnectResponse200ExtraParams

        d = src_dict.copy()
        _extra_params = d.pop("extra_params", UNSET)
        extra_params: Union[Unset, GetOAuthConnectResponse200ExtraParams]
        if isinstance(_extra_params, Unset):
            extra_params = UNSET
        else:
            extra_params = GetOAuthConnectResponse200ExtraParams.from_dict(_extra_params)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        get_o_auth_connect_response_200 = cls(
            extra_params=extra_params,
            scopes=scopes,
        )

        get_o_auth_connect_response_200.additional_properties = d
        return get_o_auth_connect_response_200

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
