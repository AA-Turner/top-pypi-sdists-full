from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.runtime_state_enum import RuntimeStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedServiceProviderAccountRequest")


@_attrs_define
class PatchedServiceProviderAccountRequest:
    """
    Attributes:
        username (Union[None, Unset, str]):
        runtime_state (Union[Unset, RuntimeStateEnum]):
        service_provider_comment (Union[Unset, str]): Additional comment for pending states like validation or account
            linking
        service_provider_comment_url (Union[Unset, str]): URL link for additional information or actions related to
            service provider comment
    """

    username: Union[None, Unset, str] = UNSET
    runtime_state: Union[Unset, RuntimeStateEnum] = UNSET
    service_provider_comment: Union[Unset, str] = UNSET
    service_provider_comment_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        runtime_state: Union[Unset, str] = UNSET
        if not isinstance(self.runtime_state, Unset):
            runtime_state = self.runtime_state.value

        service_provider_comment = self.service_provider_comment

        service_provider_comment_url = self.service_provider_comment_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if service_provider_comment is not UNSET:
            field_dict["service_provider_comment"] = service_provider_comment
        if service_provider_comment_url is not UNSET:
            field_dict["service_provider_comment_url"] = service_provider_comment_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        _runtime_state = d.pop("runtime_state", UNSET)
        runtime_state: Union[Unset, RuntimeStateEnum]
        if isinstance(_runtime_state, Unset):
            runtime_state = UNSET
        else:
            runtime_state = RuntimeStateEnum(_runtime_state)

        service_provider_comment = d.pop("service_provider_comment", UNSET)

        service_provider_comment_url = d.pop("service_provider_comment_url", UNSET)

        patched_service_provider_account_request = cls(
            username=username,
            runtime_state=runtime_state,
            service_provider_comment=service_provider_comment,
            service_provider_comment_url=service_provider_comment_url,
        )

        patched_service_provider_account_request.additional_properties = d
        return patched_service_provider_account_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
