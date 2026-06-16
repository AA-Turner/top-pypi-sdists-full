import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_http_trigger_response_200_authentication_method import GetHttpTriggerResponse200AuthenticationMethod
from ..models.get_http_trigger_response_200_http_method import GetHttpTriggerResponse200HttpMethod
from ..models.get_http_trigger_response_200_request_type import GetHttpTriggerResponse200RequestType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_http_trigger_response_200_draft import GetHttpTriggerResponse200Draft
    from ..models.get_http_trigger_response_200_error_handler_args import GetHttpTriggerResponse200ErrorHandlerArgs
    from ..models.get_http_trigger_response_200_other_drafts_users_item import (
        GetHttpTriggerResponse200OtherDraftsUsersItem,
    )
    from ..models.get_http_trigger_response_200_retry import GetHttpTriggerResponse200Retry
    from ..models.get_http_trigger_response_200_static_asset_config import GetHttpTriggerResponse200StaticAssetConfig


T = TypeVar("T", bound="GetHttpTriggerResponse200")


@_attrs_define
class GetHttpTriggerResponse200:
    """
    Attributes:
        route_path (str): The URL route path that will trigger this endpoint (e.g., 'api/myendpoint'). Must NOT start
            with a /.
        http_method (GetHttpTriggerResponse200HttpMethod): HTTP method (get, post, put, delete, patch) that triggers
            this endpoint
        request_type (GetHttpTriggerResponse200RequestType): How the request is handled - 'sync' waits for result,
            'async' returns job ID immediately, 'sync_sse' streams results via Server-Sent Events
        authentication_method (GetHttpTriggerResponse200AuthenticationMethod): How requests are authenticated - 'none'
            (public), 'windmill' (Windmill token), 'api_key', 'basic_http', 'custom_script', 'signature'
        is_static_website (bool): If true, serves static files from S3/storage instead of running a script
        workspaced_route (bool): If true, the route includes the workspace ID in the path
        wrap_body (bool): If true, wraps the request body in a 'body' parameter
        raw_string (bool): If true, passes the request body as a raw string instead of parsing as JSON
        is_draft (bool):
        static_asset_config (Union[Unset, None, GetHttpTriggerResponse200StaticAssetConfig]): Configuration for serving
            static assets (s3 bucket, storage path, filename)
        authentication_resource_path (Union[Unset, None, str]): Path to the resource containing authentication
            configuration (for api_key, basic_http, custom_script, signature methods)
        summary (Union[Unset, None, str]): Short summary describing the purpose of this trigger
        description (Union[Unset, None, str]): Detailed description of what this trigger does
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, GetHttpTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, GetHttpTriggerResponse200Retry]): Retry configuration for failed module executions
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetHttpTriggerResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetHttpTriggerResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    route_path: str
    http_method: GetHttpTriggerResponse200HttpMethod
    request_type: GetHttpTriggerResponse200RequestType
    authentication_method: GetHttpTriggerResponse200AuthenticationMethod
    is_static_website: bool
    workspaced_route: bool
    wrap_body: bool
    raw_string: bool
    is_draft: bool
    static_asset_config: Union[Unset, None, "GetHttpTriggerResponse200StaticAssetConfig"] = UNSET
    authentication_resource_path: Union[Unset, None, str] = UNSET
    summary: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetHttpTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetHttpTriggerResponse200Retry"] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetHttpTriggerResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetHttpTriggerResponse200OtherDraftsUsersItem"]] = UNSET
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
        is_draft = self.is_draft
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

        draft_saved_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_saved_at, Unset):
            draft_saved_at = self.draft_saved_at.isoformat()

        no_deployed = self.no_deployed
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        other_drafts_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.other_drafts_users, Unset):
            other_drafts_users = []
            for other_drafts_users_item_data in self.other_drafts_users:
                other_drafts_users_item = other_drafts_users_item_data.to_dict()

                other_drafts_users.append(other_drafts_users_item)

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
                "is_draft": is_draft,
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
        if draft_saved_at is not UNSET:
            field_dict["draft_saved_at"] = draft_saved_at
        if no_deployed is not UNSET:
            field_dict["no_deployed"] = no_deployed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if other_drafts_users is not UNSET:
            field_dict["other_drafts_users"] = other_drafts_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_http_trigger_response_200_draft import GetHttpTriggerResponse200Draft
        from ..models.get_http_trigger_response_200_error_handler_args import GetHttpTriggerResponse200ErrorHandlerArgs
        from ..models.get_http_trigger_response_200_other_drafts_users_item import (
            GetHttpTriggerResponse200OtherDraftsUsersItem,
        )
        from ..models.get_http_trigger_response_200_retry import GetHttpTriggerResponse200Retry
        from ..models.get_http_trigger_response_200_static_asset_config import (
            GetHttpTriggerResponse200StaticAssetConfig,
        )

        d = src_dict.copy()
        route_path = d.pop("route_path")

        http_method = GetHttpTriggerResponse200HttpMethod(d.pop("http_method"))

        request_type = GetHttpTriggerResponse200RequestType(d.pop("request_type"))

        authentication_method = GetHttpTriggerResponse200AuthenticationMethod(d.pop("authentication_method"))

        is_static_website = d.pop("is_static_website")

        workspaced_route = d.pop("workspaced_route")

        wrap_body = d.pop("wrap_body")

        raw_string = d.pop("raw_string")

        is_draft = d.pop("is_draft")

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, None, GetHttpTriggerResponse200StaticAssetConfig]
        if _static_asset_config is None:
            static_asset_config = None
        elif isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = GetHttpTriggerResponse200StaticAssetConfig.from_dict(_static_asset_config)

        authentication_resource_path = d.pop("authentication_resource_path", UNSET)

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, GetHttpTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetHttpTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetHttpTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetHttpTriggerResponse200Retry.from_dict(_retry)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetHttpTriggerResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetHttpTriggerResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetHttpTriggerResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_http_trigger_response_200 = cls(
            route_path=route_path,
            http_method=http_method,
            request_type=request_type,
            authentication_method=authentication_method,
            is_static_website=is_static_website,
            workspaced_route=workspaced_route,
            wrap_body=wrap_body,
            raw_string=raw_string,
            is_draft=is_draft,
            static_asset_config=static_asset_config,
            authentication_resource_path=authentication_resource_path,
            summary=summary,
            description=description,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_http_trigger_response_200.additional_properties = d
        return get_http_trigger_response_200

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
