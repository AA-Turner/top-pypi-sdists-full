import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_http_triggers_response_200_item_authentication_method import (
    ListHttpTriggersResponse200ItemAuthenticationMethod,
)
from ..models.list_http_triggers_response_200_item_http_method import ListHttpTriggersResponse200ItemHttpMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_http_triggers_response_200_item_extra_perms import ListHttpTriggersResponse200ItemExtraPerms
    from ..models.list_http_triggers_response_200_item_static_asset_config import (
        ListHttpTriggersResponse200ItemStaticAssetConfig,
    )


T = TypeVar("T", bound="ListHttpTriggersResponse200Item")


@_attrs_define
class ListHttpTriggersResponse200Item:
    """
    Attributes:
        route_path (str):
        http_method (ListHttpTriggersResponse200ItemHttpMethod):
        is_async (bool):
        authentication_method (ListHttpTriggersResponse200ItemAuthenticationMethod):
        is_static_website (bool):
        workspaced_route (bool):
        wrap_body (bool):
        raw_string (bool):
        path (str):
        script_path (str):
        email (str):
        extra_perms (ListHttpTriggersResponse200ItemExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        static_asset_config (Union[Unset, ListHttpTriggersResponse200ItemStaticAssetConfig]):
        authentication_resource_path (Union[Unset, str]):
    """

    route_path: str
    http_method: ListHttpTriggersResponse200ItemHttpMethod
    is_async: bool
    authentication_method: ListHttpTriggersResponse200ItemAuthenticationMethod
    is_static_website: bool
    workspaced_route: bool
    wrap_body: bool
    raw_string: bool
    path: str
    script_path: str
    email: str
    extra_perms: "ListHttpTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    static_asset_config: Union[Unset, "ListHttpTriggersResponse200ItemStaticAssetConfig"] = UNSET
    authentication_resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        route_path = self.route_path
        http_method = self.http_method.value

        is_async = self.is_async
        authentication_method = self.authentication_method.value

        is_static_website = self.is_static_website
        workspaced_route = self.workspaced_route
        wrap_body = self.wrap_body
        raw_string = self.raw_string
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        static_asset_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict()

        authentication_resource_path = self.authentication_resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_path": route_path,
                "http_method": http_method,
                "is_async": is_async,
                "authentication_method": authentication_method,
                "is_static_website": is_static_website,
                "workspaced_route": workspaced_route,
                "wrap_body": wrap_body,
                "raw_string": raw_string,
                "path": path,
                "script_path": script_path,
                "email": email,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
            }
        )
        if static_asset_config is not UNSET:
            field_dict["static_asset_config"] = static_asset_config
        if authentication_resource_path is not UNSET:
            field_dict["authentication_resource_path"] = authentication_resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_http_triggers_response_200_item_extra_perms import ListHttpTriggersResponse200ItemExtraPerms
        from ..models.list_http_triggers_response_200_item_static_asset_config import (
            ListHttpTriggersResponse200ItemStaticAssetConfig,
        )

        d = src_dict.copy()
        route_path = d.pop("route_path")

        http_method = ListHttpTriggersResponse200ItemHttpMethod(d.pop("http_method"))

        is_async = d.pop("is_async")

        authentication_method = ListHttpTriggersResponse200ItemAuthenticationMethod(d.pop("authentication_method"))

        is_static_website = d.pop("is_static_website")

        workspaced_route = d.pop("workspaced_route")

        wrap_body = d.pop("wrap_body")

        raw_string = d.pop("raw_string")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = ListHttpTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, ListHttpTriggersResponse200ItemStaticAssetConfig]
        if isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = ListHttpTriggersResponse200ItemStaticAssetConfig.from_dict(_static_asset_config)

        authentication_resource_path = d.pop("authentication_resource_path", UNSET)

        list_http_triggers_response_200_item = cls(
            route_path=route_path,
            http_method=http_method,
            is_async=is_async,
            authentication_method=authentication_method,
            is_static_website=is_static_website,
            workspaced_route=workspaced_route,
            wrap_body=wrap_body,
            raw_string=raw_string,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            static_asset_config=static_asset_config,
            authentication_resource_path=authentication_resource_path,
        )

        list_http_triggers_response_200_item.additional_properties = d
        return list_http_triggers_response_200_item

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
