from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execute_action_response_metadata import ExecuteActionResponseMetadata


T = TypeVar("T", bound="ExecuteActionResponse")


@_attrs_define
class ExecuteActionResponse:
    """
    Attributes:
        action (str):
        message (Union[Unset, str]):
        redirect_url (Union[Unset, str]):
        metadata (Union[Unset, ExecuteActionResponseMetadata]):
    """

    action: str
    message: Union[Unset, str] = UNSET
    redirect_url: Union[Unset, str] = UNSET
    metadata: Union[Unset, "ExecuteActionResponseMetadata"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        message = self.message

        redirect_url = self.redirect_url

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if redirect_url is not UNSET:
            field_dict["redirect_url"] = redirect_url
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.execute_action_response_metadata import ExecuteActionResponseMetadata

        d = dict(src_dict)
        action = d.pop("action")

        message = d.pop("message", UNSET)

        redirect_url = d.pop("redirect_url", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ExecuteActionResponseMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ExecuteActionResponseMetadata.from_dict(_metadata)

        execute_action_response = cls(
            action=action,
            message=message,
            redirect_url=redirect_url,
            metadata=metadata,
        )

        execute_action_response.additional_properties = d
        return execute_action_response

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
