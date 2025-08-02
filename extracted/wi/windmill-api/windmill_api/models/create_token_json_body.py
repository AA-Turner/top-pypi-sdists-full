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
        workspace_id (Union[Unset, str]):
    """

    label: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.datetime] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    workspace_id: Union[Unset, str] = UNSET
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

        create_token_json_body = cls(
            label=label,
            expiration=expiration,
            scopes=scopes,
            workspace_id=workspace_id,
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
