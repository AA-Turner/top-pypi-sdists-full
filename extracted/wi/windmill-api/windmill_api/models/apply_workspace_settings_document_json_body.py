from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_workspace_settings_document_json_body_document import (
        ApplyWorkspaceSettingsDocumentJsonBodyDocument,
    )


T = TypeVar("T", bound="ApplyWorkspaceSettingsDocumentJsonBody")


@_attrs_define
class ApplyWorkspaceSettingsDocumentJsonBody:
    """
    Attributes:
        document (ApplyWorkspaceSettingsDocumentJsonBodyDocument): The settings to apply, in the layout of the document.
            A secret given as `__SENSITIVE_AND_UNCHANGED__` keeps its stored value; one prefixed with `$encrypted:` is
            decrypted with the workspace key.
        replace (Union[Unset, bool]): Clear the settings `wmill sync push` clears when settings.yaml omits them.
            Otherwise a setting the document omits is left as it is.
        dry_run (Union[Unset, bool]): Only compute the changes, without applying them.
    """

    document: "ApplyWorkspaceSettingsDocumentJsonBodyDocument"
    replace: Union[Unset, bool] = UNSET
    dry_run: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document = self.document.to_dict()

        replace = self.replace
        dry_run = self.dry_run

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document": document,
            }
        )
        if replace is not UNSET:
            field_dict["replace"] = replace
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.apply_workspace_settings_document_json_body_document import (
            ApplyWorkspaceSettingsDocumentJsonBodyDocument,
        )

        d = src_dict.copy()
        document = ApplyWorkspaceSettingsDocumentJsonBodyDocument.from_dict(d.pop("document"))

        replace = d.pop("replace", UNSET)

        dry_run = d.pop("dry_run", UNSET)

        apply_workspace_settings_document_json_body = cls(
            document=document,
            replace=replace,
            dry_run=dry_run,
        )

        apply_workspace_settings_document_json_body.additional_properties = d
        return apply_workspace_settings_document_json_body

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
