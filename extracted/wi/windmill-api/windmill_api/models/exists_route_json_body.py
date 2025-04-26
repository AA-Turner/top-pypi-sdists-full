from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.exists_route_json_body_http_method import ExistsRouteJsonBodyHttpMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExistsRouteJsonBody")


@_attrs_define
class ExistsRouteJsonBody:
    """
    Attributes:
        route_path (str):
        http_method (ExistsRouteJsonBodyHttpMethod):
        trigger_path (Union[Unset, str]):
        workspaced_route (Union[Unset, bool]):
    """

    route_path: str
    http_method: ExistsRouteJsonBodyHttpMethod
    trigger_path: Union[Unset, str] = UNSET
    workspaced_route: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        route_path = self.route_path
        http_method = self.http_method.value

        trigger_path = self.trigger_path
        workspaced_route = self.workspaced_route

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_path": route_path,
                "http_method": http_method,
            }
        )
        if trigger_path is not UNSET:
            field_dict["trigger_path"] = trigger_path
        if workspaced_route is not UNSET:
            field_dict["workspaced_route"] = workspaced_route

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        route_path = d.pop("route_path")

        http_method = ExistsRouteJsonBodyHttpMethod(d.pop("http_method"))

        trigger_path = d.pop("trigger_path", UNSET)

        workspaced_route = d.pop("workspaced_route", UNSET)

        exists_route_json_body = cls(
            route_path=route_path,
            http_method=http_method,
            trigger_path=trigger_path,
            workspaced_route=workspaced_route,
        )

        exists_route_json_body.additional_properties = d
        return exists_route_json_body

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
