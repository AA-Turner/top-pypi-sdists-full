from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.effective_route import EffectiveRoute


T = TypeVar("T", bound="EffectiveRoutesResponse")


@_attrs_define
class EffectiveRoutesResponse:
    """
    Attributes:
        snat (Union[None, bool]):
        has_external_gateway (bool):
        routes (list['EffectiveRoute']):
    """

    snat: Union[None, bool]
    has_external_gateway: bool
    routes: list["EffectiveRoute"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        snat: Union[None, bool]
        snat = self.snat

        has_external_gateway = self.has_external_gateway

        routes = []
        for routes_item_data in self.routes:
            routes_item = routes_item_data.to_dict()
            routes.append(routes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "snat": snat,
                "has_external_gateway": has_external_gateway,
                "routes": routes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.effective_route import EffectiveRoute

        d = dict(src_dict)

        def _parse_snat(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        snat = _parse_snat(d.pop("snat"))

        has_external_gateway = d.pop("has_external_gateway")

        routes = []
        _routes = d.pop("routes")
        for routes_item_data in _routes:
            routes_item = EffectiveRoute.from_dict(routes_item_data)

            routes.append(routes_item)

        effective_routes_response = cls(
            snat=snat,
            has_external_gateway=has_external_gateway,
            routes=routes,
        )

        effective_routes_response.additional_properties = d
        return effective_routes_response

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
