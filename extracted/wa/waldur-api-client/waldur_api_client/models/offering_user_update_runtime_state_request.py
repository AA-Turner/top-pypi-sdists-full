from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.runtime_state_enum import RuntimeStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingUserUpdateRuntimeStateRequest")


@_attrs_define
class OfferingUserUpdateRuntimeStateRequest:
    """
    Attributes:
        runtime_state (RuntimeStateEnum):
        service_provider_comment (Union[Unset, str]): Optional comment explaining the runtime state change.
        service_provider_comment_url (Union[Unset, str]): Optional URL with additional information for the user.
    """

    runtime_state: RuntimeStateEnum
    service_provider_comment: Union[Unset, str] = UNSET
    service_provider_comment_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        runtime_state = self.runtime_state.value

        service_provider_comment = self.service_provider_comment

        service_provider_comment_url = self.service_provider_comment_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "runtime_state": runtime_state,
            }
        )
        if service_provider_comment is not UNSET:
            field_dict["service_provider_comment"] = service_provider_comment
        if service_provider_comment_url is not UNSET:
            field_dict["service_provider_comment_url"] = service_provider_comment_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        runtime_state = RuntimeStateEnum(d.pop("runtime_state"))

        service_provider_comment = d.pop("service_provider_comment", UNSET)

        service_provider_comment_url = d.pop("service_provider_comment_url", UNSET)

        offering_user_update_runtime_state_request = cls(
            runtime_state=runtime_state,
            service_provider_comment=service_provider_comment,
            service_provider_comment_url=service_provider_comment_url,
        )

        offering_user_update_runtime_state_request.additional_properties = d
        return offering_user_update_runtime_state_request

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
