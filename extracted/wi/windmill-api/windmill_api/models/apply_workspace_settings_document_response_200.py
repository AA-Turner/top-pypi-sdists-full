from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_workspace_settings_document_response_200_changes_item import (
        ApplyWorkspaceSettingsDocumentResponse200ChangesItem,
    )


T = TypeVar("T", bound="ApplyWorkspaceSettingsDocumentResponse200")


@_attrs_define
class ApplyWorkspaceSettingsDocumentResponse200:
    """
    Attributes:
        changes (List['ApplyWorkspaceSettingsDocumentResponse200ChangesItem']):
        applied (bool):
        warnings (Union[Unset, List[str]]):
    """

    changes: List["ApplyWorkspaceSettingsDocumentResponse200ChangesItem"]
    applied: bool
    warnings: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        changes = []
        for changes_item_data in self.changes:
            changes_item = changes_item_data.to_dict()

            changes.append(changes_item)

        applied = self.applied
        warnings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "changes": changes,
                "applied": applied,
            }
        )
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.apply_workspace_settings_document_response_200_changes_item import (
            ApplyWorkspaceSettingsDocumentResponse200ChangesItem,
        )

        d = src_dict.copy()
        changes = []
        _changes = d.pop("changes")
        for changes_item_data in _changes:
            changes_item = ApplyWorkspaceSettingsDocumentResponse200ChangesItem.from_dict(changes_item_data)

            changes.append(changes_item)

        applied = d.pop("applied")

        warnings = cast(List[str], d.pop("warnings", UNSET))

        apply_workspace_settings_document_response_200 = cls(
            changes=changes,
            applied=applied,
            warnings=warnings,
        )

        apply_workspace_settings_document_response_200.additional_properties = d
        return apply_workspace_settings_document_response_200

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
