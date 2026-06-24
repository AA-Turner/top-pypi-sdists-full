import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

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
            entirely.
        sandbox (bool): Publisher opted this app into sandbox isolation. When false the viewer runs the app same-origin
            with its full session.
        token (Union[Unset, None, str]): Narrowly-scoped embed token for the iframe. Absent for fully anonymous or raw
            apps, which load without a scoped token.
        expiration (Union[Unset, None, datetime.datetime]): Expiration of the embed token.
        app_path (Union[Unset, None, str]): The resolved app path; the embedder uses it to scope the app's backing
            localStorage per app.
        workspace_id (Union[Unset, None, str]): The resolved workspace; pairs with app_path so apps at the same path in
            different workspaces don't share a localStorage store.
    """

    raw_app: bool
    sandbox: bool
    token: Union[Unset, None, str] = UNSET
    expiration: Union[Unset, None, datetime.datetime] = UNSET
    app_path: Union[Unset, None, str] = UNSET
    workspace_id: Union[Unset, None, str] = UNSET
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

        get_app_embed_token_by_custom_path_response_200 = cls(
            raw_app=raw_app,
            sandbox=sandbox,
            token=token,
            expiration=expiration,
            app_path=app_path,
            workspace_id=workspace_id,
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
