import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTokenJsonBody")


@_attrs_define
class CreateTokenJsonBody:
    """
    Attributes:
        label (Union[Unset, str]):
        expiration (Union[Unset, datetime.datetime]):
        scopes (Union[Unset, List[str]]):
        workspace_id (Union[Unset, str]): Bind the token to this workspace: it is then refused on every other workspace
            and
            on instance-level endpoints. Omit for a token that reaches every workspace.
        read_only (Union[Unset, bool]): If true, the token is restricted to read-only HTTP methods
            (GET/HEAD/OPTIONS). Mutating endpoints and job-run actions are
            rejected with 403, regardless of the scopes attached.
        super_admin (Union[Unset, bool]): Carry the owner's superadmin rights: admin in every workspace, including ones
            they are not a member of, and the superadmin endpoints. Defaults to false, and
            is ignored when the owner or the calling token does not hold them.
        admin (Union[Unset, bool]): Carry the owner's workspace admin rights in the workspaces the token reaches.
            Defaults to false: the token then acts as a regular member. Ignored when the
            calling token does not hold them.
        allowed_ips (Union[Unset, List[str]]): IPs or CIDRs (IPv4 or IPv6) the token may be used from; omit to allow
            any.
            A request from elsewhere is refused as unauthenticated. A token that is itself
            restricted can only create tokens within its own networks, and creates one
            restricted to them when this is omitted.
    """

    label: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.datetime] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    super_admin: Union[Unset, bool] = UNSET
    admin: Union[Unset, bool] = UNSET
    allowed_ips: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        workspace_id = self.workspace_id
        read_only = self.read_only
        super_admin = self.super_admin
        admin = self.admin
        allowed_ips: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if read_only is not UNSET:
            field_dict["read_only"] = read_only
        if super_admin is not UNSET:
            field_dict["super_admin"] = super_admin
        if admin is not UNSET:
            field_dict["admin"] = admin
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.datetime]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        workspace_id = d.pop("workspace_id", UNSET)

        read_only = d.pop("read_only", UNSET)

        super_admin = d.pop("super_admin", UNSET)

        admin = d.pop("admin", UNSET)

        allowed_ips = cast(List[str], d.pop("allowed_ips", UNSET))

        create_token_json_body = cls(
            label=label,
            expiration=expiration,
            scopes=scopes,
            workspace_id=workspace_id,
            read_only=read_only,
            super_admin=super_admin,
            admin=admin,
            allowed_ips=allowed_ips,
        )

        create_token_json_body.additional_properties = d
        return create_token_json_body

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
