from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_workspace_role_overrides_json_body_additional_property import (
        UpdateWorkspaceRoleOverridesJsonBodyAdditionalProperty,
    )


T = TypeVar("T", bound="UpdateWorkspaceRoleOverridesJsonBody")


@_attrs_define
class UpdateWorkspaceRoleOverridesJsonBody:
    """A workspace's overrides keyed by role name; a name the instance does not define adds a workspace-only role (EE)."""

    additional_properties: Dict[str, "UpdateWorkspaceRoleOverridesJsonBodyAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_workspace_role_overrides_json_body_additional_property import (
            UpdateWorkspaceRoleOverridesJsonBodyAdditionalProperty,
        )

        d = src_dict.copy()
        update_workspace_role_overrides_json_body = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = UpdateWorkspaceRoleOverridesJsonBodyAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        update_workspace_role_overrides_json_body.additional_properties = additional_properties
        return update_workspace_role_overrides_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "UpdateWorkspaceRoleOverridesJsonBodyAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "UpdateWorkspaceRoleOverridesJsonBodyAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
