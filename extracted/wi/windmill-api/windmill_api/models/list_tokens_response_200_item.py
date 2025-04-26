import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListTokensResponse200Item")


@_attrs_define
class ListTokensResponse200Item:
    """
    Attributes:
        token_prefix (str):
        created_at (datetime.datetime):
        last_used_at (datetime.datetime):
        label (Union[Unset, str]):
        expiration (Union[Unset, datetime.datetime]):
        scopes (Union[Unset, List[str]]):
        email (Union[Unset, str]):
    """

    token_prefix: str
    created_at: datetime.datetime
    last_used_at: datetime.datetime
    label: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.datetime] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    email: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token_prefix = self.token_prefix
        created_at = self.created_at.isoformat()

        last_used_at = self.last_used_at.isoformat()

        label = self.label
        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token_prefix": token_prefix,
                "created_at": created_at,
                "last_used_at": last_used_at,
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token_prefix = d.pop("token_prefix")

        created_at = isoparse(d.pop("created_at"))

        last_used_at = isoparse(d.pop("last_used_at"))

        label = d.pop("label", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.datetime]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        email = d.pop("email", UNSET)

        list_tokens_response_200_item = cls(
            token_prefix=token_prefix,
            created_at=created_at,
            last_used_at=last_used_at,
            label=label,
            expiration=expiration,
            scopes=scopes,
            email=email,
        )

        list_tokens_response_200_item.additional_properties = d
        return list_tokens_response_200_item

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
