import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_tokens_of_flow_response_200_item_risks_item import ListTokensOfFlowResponse200ItemRisksItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListTokensOfFlowResponse200Item")


@_attrs_define
class ListTokensOfFlowResponse200Item:
    """
    Attributes:
        token_prefix (str):
        created_at (datetime.datetime):
        last_used_at (datetime.datetime):
        read_only (bool):
        risks (List[ListTokensOfFlowResponse200ItemRisksItem]): what a token review flags on this token; empty for a
            token the server manages on its own
        label (Union[Unset, str]):
        expiration (Union[Unset, datetime.datetime]):
        scopes (Union[Unset, List[str]]):
        email (Union[Unset, str]):
        workspace_id (Union[Unset, str]):
        allowed_ips (Union[Unset, List[str]]): IPs or CIDRs the token may be used from; absent when it may be used from
            anywhere.
        admin (Union[Unset, bool]): The token carries workspace admin rights: it was minted with them and its owner is
            an
            admin of the workspace it is bound to (any workspace when unbound). Set by /users/tokens/list.
        super_admin (Union[Unset, bool]): The token carries superadmin rights: it was minted with them (a session always
            is) and
            its owner is a superadmin. Set by /users/tokens/list.
    """

    token_prefix: str
    created_at: datetime.datetime
    last_used_at: datetime.datetime
    read_only: bool
    risks: List[ListTokensOfFlowResponse200ItemRisksItem]
    label: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.datetime] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    email: Union[Unset, str] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    allowed_ips: Union[Unset, List[str]] = UNSET
    admin: Union[Unset, bool] = UNSET
    super_admin: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token_prefix = self.token_prefix
        created_at = self.created_at.isoformat()

        last_used_at = self.last_used_at.isoformat()

        read_only = self.read_only
        risks = []
        for risks_item_data in self.risks:
            risks_item = risks_item_data.value

            risks.append(risks_item)

        label = self.label
        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        email = self.email
        workspace_id = self.workspace_id
        allowed_ips: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        admin = self.admin
        super_admin = self.super_admin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token_prefix": token_prefix,
                "created_at": created_at,
                "last_used_at": last_used_at,
                "read_only": read_only,
                "risks": risks,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if email is not UNSET:
            field_dict["email"] = email
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips
        if admin is not UNSET:
            field_dict["admin"] = admin
        if super_admin is not UNSET:
            field_dict["super_admin"] = super_admin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token_prefix = d.pop("token_prefix")

        created_at = isoparse(d.pop("created_at"))

        last_used_at = isoparse(d.pop("last_used_at"))

        read_only = d.pop("read_only")

        risks = []
        _risks = d.pop("risks")
        for risks_item_data in _risks:
            risks_item = ListTokensOfFlowResponse200ItemRisksItem(risks_item_data)

            risks.append(risks_item)

        label = d.pop("label", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.datetime]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        email = d.pop("email", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        allowed_ips = cast(List[str], d.pop("allowed_ips", UNSET))

        admin = d.pop("admin", UNSET)

        super_admin = d.pop("super_admin", UNSET)

        list_tokens_of_flow_response_200_item = cls(
            token_prefix=token_prefix,
            created_at=created_at,
            last_used_at=last_used_at,
            read_only=read_only,
            risks=risks,
            label=label,
            expiration=expiration,
            scopes=scopes,
            email=email,
            workspace_id=workspace_id,
            allowed_ips=allowed_ips,
            admin=admin,
            super_admin=super_admin,
        )

        list_tokens_of_flow_response_200_item.additional_properties = d
        return list_tokens_of_flow_response_200_item

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
