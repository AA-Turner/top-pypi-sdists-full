from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApplyWorkspaceSettingsDocumentJsonBodyDocument")


@_attrs_define
class ApplyWorkspaceSettingsDocumentJsonBodyDocument:
    """The settings to apply, in the layout of the document. A secret given as `__SENSITIVE_AND_UNCHANGED__` keeps its
    stored value; one prefixed with `$encrypted:` is decrypted with the workspace key.

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        apply_workspace_settings_document_json_body_document = cls()

        apply_workspace_settings_document_json_body_document.additional_properties = d
        return apply_workspace_settings_document_json_body_document

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
