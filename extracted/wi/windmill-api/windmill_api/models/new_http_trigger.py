from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_http_trigger_authentication_method import NewHttpTriggerAuthenticationMethod
from ..models.new_http_trigger_http_method import NewHttpTriggerHttpMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_http_trigger_error_handler_args import NewHttpTriggerErrorHandlerArgs
    from ..models.new_http_trigger_retry import NewHttpTriggerRetry
    from ..models.new_http_trigger_static_asset_config import NewHttpTriggerStaticAssetConfig


T = TypeVar("T", bound="NewHttpTrigger")


@_attrs_define
class NewHttpTrigger:
    """
    Attributes:
        path (str):
        script_path (str):
        route_path (str):
        is_flow (bool):
        http_method (NewHttpTriggerHttpMethod):
        is_async (bool):
        authentication_method (NewHttpTriggerAuthenticationMethod):
        is_static_website (bool):
        workspaced_route (Union[Unset, bool]):
        summary (Union[Unset, str]):
        description (Union[Unset, str]):
        static_asset_config (Union[Unset, NewHttpTriggerStaticAssetConfig]):
        authentication_resource_path (Union[Unset, str]):
        wrap_body (Union[Unset, bool]):
        raw_string (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, NewHttpTriggerErrorHandlerArgs]):
        retry (Union[Unset, NewHttpTriggerRetry]):
    """

    path: str
    script_path: str
    route_path: str
    is_flow: bool
    http_method: NewHttpTriggerHttpMethod
    is_async: bool
    authentication_method: NewHttpTriggerAuthenticationMethod
    is_static_website: bool
    workspaced_route: Union[Unset, bool] = UNSET
    summary: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    static_asset_config: Union[Unset, "NewHttpTriggerStaticAssetConfig"] = UNSET
    authentication_resource_path: Union[Unset, str] = UNSET
    wrap_body: Union[Unset, bool] = UNSET
    raw_string: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "NewHttpTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "NewHttpTriggerRetry"] = UNSET
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
        summary = self.summary
        description = self.description
        static_asset_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict()

        authentication_resource_path = self.authentication_resource_path
        wrap_body = self.wrap_body
        raw_string = self.raw_string
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

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
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if static_asset_config is not UNSET:
            field_dict["static_asset_config"] = static_asset_config
        if authentication_resource_path is not UNSET:
            field_dict["authentication_resource_path"] = authentication_resource_path
        if wrap_body is not UNSET:
            field_dict["wrap_body"] = wrap_body
        if raw_string is not UNSET:
            field_dict["raw_string"] = raw_string
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_http_trigger_error_handler_args import NewHttpTriggerErrorHandlerArgs
        from ..models.new_http_trigger_retry import NewHttpTriggerRetry
        from ..models.new_http_trigger_static_asset_config import NewHttpTriggerStaticAssetConfig

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        route_path = d.pop("route_path")

        is_flow = d.pop("is_flow")

        http_method = NewHttpTriggerHttpMethod(d.pop("http_method"))

        is_async = d.pop("is_async")

        authentication_method = NewHttpTriggerAuthenticationMethod(d.pop("authentication_method"))

        is_static_website = d.pop("is_static_website")

        workspaced_route = d.pop("workspaced_route", UNSET)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, NewHttpTriggerStaticAssetConfig]
        if isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = NewHttpTriggerStaticAssetConfig.from_dict(_static_asset_config)

        authentication_resource_path = d.pop("authentication_resource_path", UNSET)

        wrap_body = d.pop("wrap_body", UNSET)

        raw_string = d.pop("raw_string", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, NewHttpTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = NewHttpTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, NewHttpTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = NewHttpTriggerRetry.from_dict(_retry)

        new_http_trigger = cls(
            path=path,
            script_path=script_path,
            route_path=route_path,
            is_flow=is_flow,
            http_method=http_method,
            is_async=is_async,
            authentication_method=authentication_method,
            is_static_website=is_static_website,
            workspaced_route=workspaced_route,
            summary=summary,
            description=description,
            static_asset_config=static_asset_config,
            authentication_resource_path=authentication_resource_path,
            wrap_body=wrap_body,
            raw_string=raw_string,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        new_http_trigger.additional_properties = d
        return new_http_trigger

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
