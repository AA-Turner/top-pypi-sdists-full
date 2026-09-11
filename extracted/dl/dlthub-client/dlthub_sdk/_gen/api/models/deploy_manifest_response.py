from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.script_response import ScriptResponse
    from ..models.updated_script import UpdatedScript


T = TypeVar("T", bound="DeployManifestResponse")


@_attrs_define
class DeployManifestResponse:
    """
    Attributes:
        added (list[ScriptResponse]): Newly created scripts.
        archived (list[ScriptResponse]): Scripts archived (orphaned from manifest).
        unchanged (list[ScriptResponse]): Scripts with no changes.
        updated (list[UpdatedScript]): Updated scripts with their previous versions.
        warnings (list[str]): Validation warnings.
        deployment_module (None | str | Unset): The deployment module used for this deploy.
    """

    added: list[ScriptResponse]
    archived: list[ScriptResponse]
    unchanged: list[ScriptResponse]
    updated: list[UpdatedScript]
    warnings: list[str]
    deployment_module: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        added = []
        for added_item_data in self.added:
            added_item = added_item_data.to_dict()
            added.append(added_item)

        archived = []
        for archived_item_data in self.archived:
            archived_item = archived_item_data.to_dict()
            archived.append(archived_item)

        unchanged = []
        for unchanged_item_data in self.unchanged:
            unchanged_item = unchanged_item_data.to_dict()
            unchanged.append(unchanged_item)

        updated = []
        for updated_item_data in self.updated:
            updated_item = updated_item_data.to_dict()
            updated.append(updated_item)

        warnings = self.warnings

        deployment_module: None | str | Unset
        if isinstance(self.deployment_module, Unset):
            deployment_module = UNSET
        else:
            deployment_module = self.deployment_module

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "added": added,
                "archived": archived,
                "unchanged": unchanged,
                "updated": updated,
                "warnings": warnings,
            }
        )
        if deployment_module is not UNSET:
            field_dict["deployment_module"] = deployment_module

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.script_response import ScriptResponse
        from ..models.updated_script import UpdatedScript

        d = dict(src_dict)
        added = []
        _added = d.pop("added")
        for added_item_data in _added:
            added_item = ScriptResponse.from_dict(added_item_data)

            added.append(added_item)

        archived = []
        _archived = d.pop("archived")
        for archived_item_data in _archived:
            archived_item = ScriptResponse.from_dict(archived_item_data)

            archived.append(archived_item)

        unchanged = []
        _unchanged = d.pop("unchanged")
        for unchanged_item_data in _unchanged:
            unchanged_item = ScriptResponse.from_dict(unchanged_item_data)

            unchanged.append(unchanged_item)

        updated = []
        _updated = d.pop("updated")
        for updated_item_data in _updated:
            updated_item = UpdatedScript.from_dict(updated_item_data)

            updated.append(updated_item)

        warnings = cast(list[str], d.pop("warnings"))

        def _parse_deployment_module(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        deployment_module = _parse_deployment_module(d.pop("deployment_module", UNSET))

        deploy_manifest_response = cls(
            added=added,
            archived=archived,
            unchanged=unchanged,
            updated=updated,
            warnings=warnings,
            deployment_module=deployment_module,
        )

        deploy_manifest_response.additional_properties = d
        return deploy_manifest_response

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
