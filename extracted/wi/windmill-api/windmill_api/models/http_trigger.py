import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.http_trigger_authentication_method import HttpTriggerAuthenticationMethod
from ..models.http_trigger_http_method import HttpTriggerHttpMethod
from ..models.http_trigger_mode import HttpTriggerMode
from ..models.http_trigger_request_type import HttpTriggerRequestType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_trigger_error_handler_args import HttpTriggerErrorHandlerArgs
    from ..models.http_trigger_extra_perms import HttpTriggerExtraPerms
    from ..models.http_trigger_retry import HttpTriggerRetry
    from ..models.http_trigger_static_asset_config import HttpTriggerStaticAssetConfig


T = TypeVar("T", bound="HttpTrigger")


@_attrs_define
class HttpTrigger:
    """
    Attributes:
        route_path (str): The URL route path that will trigger this endpoint (e.g., 'api/myendpoint'). Must NOT start
            with a /.
        http_method (HttpTriggerHttpMethod): HTTP method (get, post, put, delete, patch) that triggers this endpoint
        request_type (HttpTriggerRequestType): How the request is handled - 'sync' waits for result, 'async' returns job
            ID immediately, 'sync_sse' streams results via Server-Sent Events
        authentication_method (HttpTriggerAuthenticationMethod): How requests are authenticated - 'none' (public),
            'windmill' (Windmill token), 'api_key', 'basic_http', 'custom_script', 'signature'
        is_static_website (bool): If true, serves static files from S3/storage instead of running a script
        workspaced_route (bool): If true, the route includes the workspace ID in the path
        wrap_body (bool): If true, wraps the request body in a 'body' parameter
        raw_string (bool): If true, passes the request body as a raw string instead of parsing as JSON
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (HttpTriggerExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (HttpTriggerMode): job trigger mode
        static_asset_config (Union[Unset, None, HttpTriggerStaticAssetConfig]): Configuration for serving static assets
            (s3 bucket, storage path, filename)
        authentication_resource_path (Union[Unset, None, str]): Path to the resource containing authentication
            configuration (for api_key, basic_http, custom_script, signature methods)
        summary (Union[Unset, None, str]): Short summary describing the purpose of this trigger
        description (Union[Unset, None, str]): Detailed description of what this trigger does
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, HttpTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, HttpTriggerRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            trigger at the same path. Set by list endpoints when
            `include_draft_only=true` synthesizes the row from the
            draft. Frontend renders a "Draft" badge.
        is_draft (Union[Unset, bool]): True when the authed user has a per-user draft at this path
            (over a deployed row or a synthesized draft-only row).
            Frontend appends a `*` to the displayed name.
    """

    route_path: str
    http_method: HttpTriggerHttpMethod
    request_type: HttpTriggerRequestType
    authentication_method: HttpTriggerAuthenticationMethod
    is_static_website: bool
    workspaced_route: bool
    wrap_body: bool
    raw_string: bool
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "HttpTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: HttpTriggerMode
    static_asset_config: Union[Unset, None, "HttpTriggerStaticAssetConfig"] = UNSET
    authentication_resource_path: Union[Unset, None, str] = UNSET
    summary: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "HttpTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "HttpTriggerRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    is_draft: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        route_path = self.route_path
        http_method = self.http_method.value

        request_type = self.request_type.value

        authentication_method = self.authentication_method.value

        is_static_website = self.is_static_website
        workspaced_route = self.workspaced_route
        wrap_body = self.wrap_body
        raw_string = self.raw_string
        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

        static_asset_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict() if self.static_asset_config else None

        authentication_resource_path = self.authentication_resource_path
        summary = self.summary
        description = self.description
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        draft_only = self.draft_only
        is_draft = self.is_draft

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_path": route_path,
                "http_method": http_method,
                "request_type": request_type,
                "authentication_method": authentication_method,
                "is_static_website": is_static_website,
                "workspaced_route": workspaced_route,
                "wrap_body": wrap_body,
                "raw_string": raw_string,
                "path": path,
                "script_path": script_path,
                "permissioned_as": permissioned_as,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
                "mode": mode,
            }
        )
        if static_asset_config is not UNSET:
            field_dict["static_asset_config"] = static_asset_config
        if authentication_resource_path is not UNSET:
            field_dict["authentication_resource_path"] = authentication_resource_path
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if labels is not UNSET:
            field_dict["labels"] = labels
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.http_trigger_error_handler_args import HttpTriggerErrorHandlerArgs
        from ..models.http_trigger_extra_perms import HttpTriggerExtraPerms
        from ..models.http_trigger_retry import HttpTriggerRetry
        from ..models.http_trigger_static_asset_config import HttpTriggerStaticAssetConfig

        d = src_dict.copy()
        route_path = d.pop("route_path")

        http_method = HttpTriggerHttpMethod(d.pop("http_method"))

        request_type = HttpTriggerRequestType(d.pop("request_type"))

        authentication_method = HttpTriggerAuthenticationMethod(d.pop("authentication_method"))

        is_static_website = d.pop("is_static_website")

        workspaced_route = d.pop("workspaced_route")

        wrap_body = d.pop("wrap_body")

        raw_string = d.pop("raw_string")

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = HttpTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = HttpTriggerMode(d.pop("mode"))

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, None, HttpTriggerStaticAssetConfig]
        if _static_asset_config is None:
            static_asset_config = None
        elif isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = HttpTriggerStaticAssetConfig.from_dict(_static_asset_config)

        authentication_resource_path = d.pop("authentication_resource_path", UNSET)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, HttpTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = HttpTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, HttpTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = HttpTriggerRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        draft_only = d.pop("draft_only", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        http_trigger = cls(
            route_path=route_path,
            http_method=http_method,
            request_type=request_type,
            authentication_method=authentication_method,
            is_static_website=is_static_website,
            workspaced_route=workspaced_route,
            wrap_body=wrap_body,
            raw_string=raw_string,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            static_asset_config=static_asset_config,
            authentication_resource_path=authentication_resource_path,
            summary=summary,
            description=description,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            labels=labels,
            draft_only=draft_only,
            is_draft=is_draft,
        )

        http_trigger.additional_properties = d
        return http_trigger

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
