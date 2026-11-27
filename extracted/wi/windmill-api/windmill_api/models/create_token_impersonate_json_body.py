import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTokenImpersonateJsonBody")


@_attrs_define
class CreateTokenImpersonateJsonBody:
    """
    Attributes:
        impersonate_email (str):
        label (Union[Unset, str]):
        expiration (Union[Unset, datetime.datetime]):
        workspace_id (Union[Unset, str]): Bind the token to this workspace; omit for a token that reaches every
            workspace.
        super_admin (Union[Unset, bool]): Carry the impersonated account's superadmin rights. Defaults to false.
        admin (Union[Unset, bool]): Carry the impersonated account's workspace admin rights. Defaults to false.
        allowed_ips (Union[Unset, List[str]]): IPs or CIDRs the token may be used from; omit to allow any.
    """

    impersonate_email: str
    label: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.datetime] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    super_admin: Union[Unset, bool] = UNSET
    admin: Union[Unset, bool] = UNSET
    allowed_ips: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        impersonate_email = self.impersonate_email
        label = self.label
        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        workspace_id = self.workspace_id
        super_admin = self.super_admin
        admin = self.admin
        allowed_ips: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "impersonate_email": impersonate_email,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
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
        impersonate_email = d.pop("impersonate_email")

        label = d.pop("label", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.datetime]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        workspace_id = d.pop("workspace_id", UNSET)

        super_admin = d.pop("super_admin", UNSET)

        admin = d.pop("admin", UNSET)

        allowed_ips = cast(List[str], d.pop("allowed_ips", UNSET))

        create_token_impersonate_json_body = cls(
            impersonate_email=impersonate_email,
            label=label,
            expiration=expiration,
            workspace_id=workspace_id,
            super_admin=super_admin,
            admin=admin,
            allowed_ips=allowed_ips,
        )

        create_token_impersonate_json_body.additional_properties = d
        return create_token_impersonate_json_body

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
