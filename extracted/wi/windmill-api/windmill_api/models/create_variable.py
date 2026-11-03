import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateVariable")


@_attrs_define
class CreateVariable:
    """
    Attributes:
        path (str): The path to the variable
        value (str): The value of the variable. For a secret, `$external:vault://<path>#<key>` stores a reference to an
            existing secret in the instance's external HashiCorp Vault (path as `vault kv get` takes it) instead of a value;
            without `#<key>` it reads the whole secret as a JSON object of its fields. It is resolved on each read, only
            under the path prefixes a superadmin allowed for the workspace, and is returned as-is when the secret is not
            decrypted.
        is_secret (bool): Whether the variable is a secret
        description (str): The description of the variable
        account (Union[Unset, int]): Ignored. A variable is linked to an OAuth account only when `createAccount` creates
            both.
        is_oauth (Union[Unset, bool]): Whether the variable is an OAuth variable
        expires_at (Union[Unset, datetime.datetime]): When to garbage-collect the variable. Used for ephemeral secrets;
            the variable is deleted once this is reached. Not the value's expiry — see value_valid_until.
        value_valid_until (Union[Unset, datetime.datetime]): When the value stored in this variable stops working.
            Triggers the workspace's variable expiration handler ahead of it, by the handler's `notify_before_secs` (1 day
            by default); never causes the variable to be deleted.
        labels (Union[Unset, List[str]]):
        ws_specific (Union[Unset, bool]):
    """

    path: str
    value: str
    is_secret: bool
    description: str
    account: Union[Unset, int] = UNSET
    is_oauth: Union[Unset, bool] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    value_valid_until: Union[Unset, datetime.datetime] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    ws_specific: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        is_secret = self.is_secret
        description = self.description
        account = self.account
        is_oauth = self.is_oauth
        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        value_valid_until: Union[Unset, str] = UNSET
        if not isinstance(self.value_valid_until, Unset):
            value_valid_until = self.value_valid_until.isoformat()

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        ws_specific = self.ws_specific

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
                "is_secret": is_secret,
                "description": description,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if is_oauth is not UNSET:
            field_dict["is_oauth"] = is_oauth
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if value_valid_until is not UNSET:
            field_dict["value_valid_until"] = value_valid_until
        if labels is not UNSET:
            field_dict["labels"] = labels
        if ws_specific is not UNSET:
            field_dict["ws_specific"] = ws_specific

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        is_secret = d.pop("is_secret")

        description = d.pop("description")

        account = d.pop("account", UNSET)

        is_oauth = d.pop("is_oauth", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        _value_valid_until = d.pop("value_valid_until", UNSET)
        value_valid_until: Union[Unset, datetime.datetime]
        if isinstance(_value_valid_until, Unset):
            value_valid_until = UNSET
        else:
            value_valid_until = isoparse(_value_valid_until)

        labels = cast(List[str], d.pop("labels", UNSET))

        ws_specific = d.pop("ws_specific", UNSET)

        create_variable = cls(
            path=path,
            value=value,
            is_secret=is_secret,
            description=description,
            account=account,
            is_oauth=is_oauth,
            expires_at=expires_at,
            value_valid_until=value_valid_until,
            labels=labels,
            ws_specific=ws_specific,
        )

        create_variable.additional_properties = d
        return create_variable

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
