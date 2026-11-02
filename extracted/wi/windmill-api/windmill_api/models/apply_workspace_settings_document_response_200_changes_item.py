from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApplyWorkspaceSettingsDocumentResponse200ChangesItem")


@_attrs_define
class ApplyWorkspaceSettingsDocumentResponse200ChangesItem:
    """
    Attributes:
        key (str):
        before (Any):
        after (Any):
    """

    key: str
    before: Any
    after: Any
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        before = self.before
        after = self.after

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "before": before,
                "after": after,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        before = d.pop("before")

        after = d.pop("after")

        apply_workspace_settings_document_response_200_changes_item = cls(
            key=key,
            before=before,
            after=after,
        )

        apply_workspace_settings_document_response_200_changes_item.additional_properties = d
        return apply_workspace_settings_document_response_200_changes_item

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
