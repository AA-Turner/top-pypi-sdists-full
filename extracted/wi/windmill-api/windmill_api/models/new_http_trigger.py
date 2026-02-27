from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_http_trigger_authentication_method import NewHttpTriggerAuthenticationMethod
from ..models.new_http_trigger_http_method import NewHttpTriggerHttpMethod
from ..models.new_http_trigger_mode import NewHttpTriggerMode
from ..models.new_http_trigger_request_type import NewHttpTriggerRequestType
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
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when triggered
        route_path (str): The URL route path that will trigger this endpoint (e.g., 'api/myendpoint'). Must NOT start
            with a /.
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        http_method (NewHttpTriggerHttpMethod): HTTP method (get, post, put, delete, patch) that triggers this endpoint
        authentication_method (NewHttpTriggerAuthenticationMethod): How requests are authenticated - 'none' (public),
            'windmill' (Windmill token), 'api_key', 'basic_http', 'custom_script', 'signature'
        is_static_website (bool): If true, serves static files from S3/storage instead of running a script
        workspaced_route (Union[Unset, bool]): If true, the route includes the workspace ID in the path
        summary (Union[Unset, None, str]): Short summary describing the purpose of this trigger
        description (Union[Unset, None, str]): Detailed description of what this trigger does
        static_asset_config (Union[Unset, None, NewHttpTriggerStaticAssetConfig]): Configuration for serving static
            assets (s3 bucket, storage path, filename)
        authentication_resource_path (Union[Unset, None, str]): Path to the resource containing authentication
            configuration (for api_key, basic_http, custom_script, signature methods)
        is_async (Union[Unset, bool]): Deprecated, use request_type instead
        request_type (Union[Unset, NewHttpTriggerRequestType]): How the request is handled - 'sync' waits for result,
            'async' returns job ID immediately, 'sync_sse' streams results via Server-Sent Events
        wrap_body (Union[Unset, bool]): If true, wraps the request body in a 'body' parameter
        mode (Union[Unset, NewHttpTriggerMode]): job trigger mode
        raw_string (Union[Unset, bool]): If true, passes the request body as a raw string instead of parsing as JSON
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, NewHttpTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, NewHttpTriggerRetry]): Retry configuration for failed module executions
        email (Union[Unset, str]): Email of the user who triggered jobs run as. Used during deployment to preserve the
            original trigger owner.
        preserve_email (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group, preserves
            the original email value instead of overwriting it.
    """

    path: str
    script_path: str
    route_path: str
    is_flow: bool
    http_method: NewHttpTriggerHttpMethod
    authentication_method: NewHttpTriggerAuthenticationMethod
    is_static_website: bool
    workspaced_route: Union[Unset, bool] = UNSET
    summary: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    static_asset_config: Union[Unset, None, "NewHttpTriggerStaticAssetConfig"] = UNSET
    authentication_resource_path: Union[Unset, None, str] = UNSET
    is_async: Union[Unset, bool] = UNSET
    request_type: Union[Unset, NewHttpTriggerRequestType] = UNSET
    wrap_body: Union[Unset, bool] = UNSET
    mode: Union[Unset, NewHttpTriggerMode] = UNSET
    raw_string: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "NewHttpTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "NewHttpTriggerRetry"] = UNSET
    email: Union[Unset, str] = UNSET
    preserve_email: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        route_path = self.route_path
        is_flow = self.is_flow
        http_method = self.http_method.value

        authentication_method = self.authentication_method.value

        is_static_website = self.is_static_website
        workspaced_route = self.workspaced_route
        summary = self.summary
        description = self.description
        static_asset_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict() if self.static_asset_config else None

        authentication_resource_path = self.authentication_resource_path
        is_async = self.is_async
        request_type: Union[Unset, str] = UNSET
        if not isinstance(self.request_type, Unset):
            request_type = self.request_type.value

        wrap_body = self.wrap_body
        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        raw_string = self.raw_string
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        email = self.email
        preserve_email = self.preserve_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "route_path": route_path,
                "is_flow": is_flow,
                "http_method": http_method,
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
        if is_async is not UNSET:
            field_dict["is_async"] = is_async
        if request_type is not UNSET:
            field_dict["request_type"] = request_type
        if wrap_body is not UNSET:
            field_dict["wrap_body"] = wrap_body
        if mode is not UNSET:
            field_dict["mode"] = mode
        if raw_string is not UNSET:
            field_dict["raw_string"] = raw_string
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if email is not UNSET:
            field_dict["email"] = email
        if preserve_email is not UNSET:
            field_dict["preserve_email"] = preserve_email

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

        authentication_method = NewHttpTriggerAuthenticationMethod(d.pop("authentication_method"))

        is_static_website = d.pop("is_static_website")

        workspaced_route = d.pop("workspaced_route", UNSET)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, None, NewHttpTriggerStaticAssetConfig]
        if _static_asset_config is None:
            static_asset_config = None
        elif isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = NewHttpTriggerStaticAssetConfig.from_dict(_static_asset_config)

        authentication_resource_path = d.pop("authentication_resource_path", UNSET)

        is_async = d.pop("is_async", UNSET)

        _request_type = d.pop("request_type", UNSET)
        request_type: Union[Unset, NewHttpTriggerRequestType]
        if isinstance(_request_type, Unset):
            request_type = UNSET
        else:
            request_type = NewHttpTriggerRequestType(_request_type)

        wrap_body = d.pop("wrap_body", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, NewHttpTriggerMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = NewHttpTriggerMode(_mode)

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

        email = d.pop("email", UNSET)

        preserve_email = d.pop("preserve_email", UNSET)

        new_http_trigger = cls(
            path=path,
            script_path=script_path,
            route_path=route_path,
            is_flow=is_flow,
            http_method=http_method,
            authentication_method=authentication_method,
            is_static_website=is_static_website,
            workspaced_route=workspaced_route,
            summary=summary,
            description=description,
            static_asset_config=static_asset_config,
            authentication_resource_path=authentication_resource_path,
            is_async=is_async,
            request_type=request_type,
            wrap_body=wrap_body,
            mode=mode,
            raw_string=raw_string,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            email=email,
            preserve_email=preserve_email,
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
