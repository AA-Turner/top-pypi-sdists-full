import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAppEmbedTokenByCustomPathResponse200")


@_attrs_define
class GetAppEmbedTokenByCustomPathResponse200:
    """
    Attributes:
        raw_app (bool): Raw apps render single-iframe and skip the opaque-viewer indirection and the embed token
            entirely. A sandboxed one may still carry a token here: the viewer-scoped frontend SDK token, which is a
            different credential from the low-code embed token.
        sandbox (bool): Publisher opted this app into sandbox isolation. When false the viewer runs the app same-origin
            with its full session.
        token (Union[Unset, None, str]): Scoped token for the app. For sandboxed low-code apps this is the embed token
            handed to the opaque iframe. For a raw app it is the viewer-scoped frontend SDK token, returned only when the
            app is sandboxed, its policy declares frontend_sdk_scopes, and the request carries sdk_consent=true. Absent for
            anonymous viewers and whenever no token is needed.
        expiration (Union[Unset, None, datetime.datetime]): Expiration of the embed token.
        app_path (Union[Unset, None, str]): The resolved app path; the embedder uses it to scope the app's backing
            localStorage per app.
        workspace_id (Union[Unset, None, str]): The resolved workspace; pairs with app_path so apps at the same path in
            different workspaces don't share a localStorage store.
        sdk_scopes (Union[Unset, None, List[str]]): Sandboxed raw apps: scopes the app policy declares for the frontend
            SDK token. Null when the app is unsandboxed, however the policy reads. The viewer renders these in the
            permission prompt; token stays absent until the endpoint is re-called with sdk_consent=true.
        viewer_email (Union[Unset, None, str]): The caller's own email, returned alongside sdk_scopes so the viewer can
            key its stored "do not ask again" per person.
    """

    raw_app: bool
    sandbox: bool
    token: Union[Unset, None, str] = UNSET
    expiration: Union[Unset, None, datetime.datetime] = UNSET
    app_path: Union[Unset, None, str] = UNSET
    workspace_id: Union[Unset, None, str] = UNSET
    sdk_scopes: Union[Unset, None, List[str]] = UNSET
    viewer_email: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        raw_app = self.raw_app
        sandbox = self.sandbox
        token = self.token
        expiration: Union[Unset, None, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat() if self.expiration else None

        app_path = self.app_path
        workspace_id = self.workspace_id
        sdk_scopes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.sdk_scopes, Unset):
            if self.sdk_scopes is None:
                sdk_scopes = None
            else:
                sdk_scopes = self.sdk_scopes

        viewer_email = self.viewer_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "raw_app": raw_app,
                "sandbox": sandbox,
            }
        )
        if token is not UNSET:
            field_dict["token"] = token
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if app_path is not UNSET:
            field_dict["app_path"] = app_path
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if sdk_scopes is not UNSET:
            field_dict["sdk_scopes"] = sdk_scopes
        if viewer_email is not UNSET:
            field_dict["viewer_email"] = viewer_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        raw_app = d.pop("raw_app")

        sandbox = d.pop("sandbox")

        token = d.pop("token", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, None, datetime.datetime]
        if _expiration is None:
            expiration = None
        elif isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        app_path = d.pop("app_path", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        sdk_scopes = cast(List[str], d.pop("sdk_scopes", UNSET))

        viewer_email = d.pop("viewer_email", UNSET)

        get_app_embed_token_by_custom_path_response_200 = cls(
            raw_app=raw_app,
            sandbox=sandbox,
            token=token,
            expiration=expiration,
            app_path=app_path,
            workspace_id=workspace_id,
            sdk_scopes=sdk_scopes,
            viewer_email=viewer_email,
        )

        get_app_embed_token_by_custom_path_response_200.additional_properties = d
        return get_app_embed_token_by_custom_path_response_200

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
