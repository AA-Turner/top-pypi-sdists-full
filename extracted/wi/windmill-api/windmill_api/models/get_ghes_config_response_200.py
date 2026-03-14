from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetGhesConfigResponse200")


@_attrs_define
class GetGhesConfigResponse200:
    """
    Attributes:
        base_url (str):
        app_slug (str):
        client_id (str):
    """

    base_url: str
    app_slug: str
    client_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base_url = self.base_url
        app_slug = self.app_slug
        client_id = self.client_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_url": base_url,
                "app_slug": app_slug,
                "client_id": client_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_url = d.pop("base_url")

        app_slug = d.pop("app_slug")

        client_id = d.pop("client_id")

        get_ghes_config_response_200 = cls(
            base_url=base_url,
            app_slug=app_slug,
            client_id=client_id,
        )

        get_ghes_config_response_200.additional_properties = d
        return get_ghes_config_response_200

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
