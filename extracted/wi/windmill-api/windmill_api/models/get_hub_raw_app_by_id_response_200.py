from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_hub_raw_app_by_id_response_200_app import GetHubRawAppByIdResponse200App


T = TypeVar("T", bound="GetHubRawAppByIdResponse200")


@_attrs_define
class GetHubRawAppByIdResponse200:
    """
    Attributes:
        app (GetHubRawAppByIdResponse200App):
    """

    app: "GetHubRawAppByIdResponse200App"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        app = self.app.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "app": app,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_hub_raw_app_by_id_response_200_app import GetHubRawAppByIdResponse200App

        d = src_dict.copy()
        app = GetHubRawAppByIdResponse200App.from_dict(d.pop("app"))

        get_hub_raw_app_by_id_response_200 = cls(
            app=app,
        )

        get_hub_raw_app_by_id_response_200.additional_properties = d
        return get_hub_raw_app_by_id_response_200

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
