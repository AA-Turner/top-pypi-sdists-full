from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.jwks_response_keys_item import JwksResponseKeysItem


T = TypeVar("T", bound="JwksResponse")


@_attrs_define
class JwksResponse:
    """
    Attributes:
        keys (List['JwksResponseKeysItem']): Array of JSON Web Keys for JWT verification
    """

    keys: List["JwksResponseKeysItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()

            keys.append(keys_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keys": keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.jwks_response_keys_item import JwksResponseKeysItem

        d = src_dict.copy()
        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = JwksResponseKeysItem.from_dict(keys_item_data)

            keys.append(keys_item)

        jwks_response = cls(
            keys=keys,
        )

        jwks_response.additional_properties = d
        return jwks_response

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
