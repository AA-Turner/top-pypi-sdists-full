from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.connect_callback_json_body_params import ConnectCallbackJsonBodyParams


T = TypeVar("T", bound="ConnectCallbackJsonBody")


@_attrs_define
class ConnectCallbackJsonBody:
    """
    Attributes:
        code (str):
        state (str):
        params (Union[Unset, ConnectCallbackJsonBodyParams]): The callback URL's other query params, which the
            provider's `connect_fields` may read (QuickBooks' `realmId`)
    """

    code: str
    state: str
    params: Union[Unset, "ConnectCallbackJsonBodyParams"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        state = self.state
        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "state": state,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.connect_callback_json_body_params import ConnectCallbackJsonBodyParams

        d = src_dict.copy()
        code = d.pop("code")

        state = d.pop("state")

        _params = d.pop("params", UNSET)
        params: Union[Unset, ConnectCallbackJsonBodyParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = ConnectCallbackJsonBodyParams.from_dict(_params)

        connect_callback_json_body = cls(
            code=code,
            state=state,
            params=params,
        )

        connect_callback_json_body.additional_properties = d
        return connect_callback_json_body

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
