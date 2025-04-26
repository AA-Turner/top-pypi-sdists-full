from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_http_trigger_json_body_authentication_method import CreateHttpTriggerJsonBodyAuthenticationMethod
from ..models.create_http_trigger_json_body_http_method import CreateHttpTriggerJsonBodyHttpMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_http_trigger_json_body_static_asset_config import CreateHttpTriggerJsonBodyStaticAssetConfig


T = TypeVar("T", bound="CreateHttpTriggerJsonBody")


@_attrs_define
class CreateHttpTriggerJsonBody:
    """
    Attributes:
        path (str):
        script_path (str):
        route_path (str):
        is_flow (bool):
        http_method (CreateHttpTriggerJsonBodyHttpMethod):
        is_async (bool):
        authentication_method (CreateHttpTriggerJsonBodyAuthenticationMethod):
        is_static_website (bool):
        workspaced_route (Union[Unset, bool]):
        static_asset_config (Union[Unset, CreateHttpTriggerJsonBodyStaticAssetConfig]):
        authentication_resource_path (Union[Unset, str]):
        wrap_body (Union[Unset, bool]):
        raw_string (Union[Unset, bool]):
    """

    path: str
    script_path: str
    route_path: str
    is_flow: bool
    http_method: CreateHttpTriggerJsonBodyHttpMethod
    is_async: bool
    authentication_method: CreateHttpTriggerJsonBodyAuthenticationMethod
    is_static_website: bool
    workspaced_route: Union[Unset, bool] = UNSET
    static_asset_config: Union[Unset, "CreateHttpTriggerJsonBodyStaticAssetConfig"] = UNSET
    authentication_resource_path: Union[Unset, str] = UNSET
    wrap_body: Union[Unset, bool] = UNSET
    raw_string: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        route_path = self.route_path
        is_flow = self.is_flow
        http_method = self.http_method.value

        is_async = self.is_async
        authentication_method = self.authentication_method.value

        is_static_website = self.is_static_website
        workspaced_route = self.workspaced_route
        static_asset_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict()

        authentication_resource_path = self.authentication_resource_path
        wrap_body = self.wrap_body
        raw_string = self.raw_string

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "route_path": route_path,
                "is_flow": is_flow,
                "http_method": http_method,
                "is_async": is_async,
                "authentication_method": authentication_method,
                "is_static_website": is_static_website,
            }
        )
        if workspaced_route is not UNSET:
            field_dict["workspaced_route"] = workspaced_route
        if static_asset_config is not UNSET:
            field_dict["static_asset_config"] = static_asset_config
        if authentication_resource_path is not UNSET:
            field_dict["authentication_resource_path"] = authentication_resource_path
        if wrap_body is not UNSET:
            field_dict["wrap_body"] = wrap_body
        if raw_string is not UNSET:
            field_dict["raw_string"] = raw_string

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_http_trigger_json_body_static_asset_config import (
            CreateHttpTriggerJsonBodyStaticAssetConfig,
        )

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        route_path = d.pop("route_path")

        is_flow = d.pop("is_flow")

        http_method = CreateHttpTriggerJsonBodyHttpMethod(d.pop("http_method"))

        is_async = d.pop("is_async")

        authentication_method = CreateHttpTriggerJsonBodyAuthenticationMethod(d.pop("authentication_method"))

        is_static_website = d.pop("is_static_website")

        workspaced_route = d.pop("workspaced_route", UNSET)

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, CreateHttpTriggerJsonBodyStaticAssetConfig]
        if isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = CreateHttpTriggerJsonBodyStaticAssetConfig.from_dict(_static_asset_config)

        authentication_resource_path = d.pop("authentication_resource_path", UNSET)

        wrap_body = d.pop("wrap_body", UNSET)

        raw_string = d.pop("raw_string", UNSET)

        create_http_trigger_json_body = cls(
            path=path,
            script_path=script_path,
            route_path=route_path,
            is_flow=is_flow,
            http_method=http_method,
            is_async=is_async,
            authentication_method=authentication_method,
            is_static_website=is_static_website,
            workspaced_route=workspaced_route,
            static_asset_config=static_asset_config,
            authentication_resource_path=authentication_resource_path,
            wrap_body=wrap_body,
            raw_string=raw_string,
        )

        create_http_trigger_json_body.additional_properties = d
        return create_http_trigger_json_body

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
