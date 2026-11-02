from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_workspace_deploy_ui_settings_json_body_deploy_ui_settings import (
        EditWorkspaceDeployUISettingsJsonBodyDeployUiSettings,
    )


T = TypeVar("T", bound="EditWorkspaceDeployUISettingsJsonBody")


@_attrs_define
class EditWorkspaceDeployUISettingsJsonBody:
    """
    Attributes:
        deploy_ui_settings (Union[Unset, EditWorkspaceDeployUISettingsJsonBodyDeployUiSettings]):
    """

    deploy_ui_settings: Union[Unset, "EditWorkspaceDeployUISettingsJsonBodyDeployUiSettings"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deploy_ui_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deploy_ui_settings, Unset):
            deploy_ui_settings = self.deploy_ui_settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deploy_ui_settings is not UNSET:
            field_dict["deploy_ui_settings"] = deploy_ui_settings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_workspace_deploy_ui_settings_json_body_deploy_ui_settings import (
            EditWorkspaceDeployUISettingsJsonBodyDeployUiSettings,
        )

        d = src_dict.copy()
        _deploy_ui_settings = d.pop("deploy_ui_settings", UNSET)
        deploy_ui_settings: Union[Unset, EditWorkspaceDeployUISettingsJsonBodyDeployUiSettings]
        if isinstance(_deploy_ui_settings, Unset):
            deploy_ui_settings = UNSET
        else:
            deploy_ui_settings = EditWorkspaceDeployUISettingsJsonBodyDeployUiSettings.from_dict(_deploy_ui_settings)

        edit_workspace_deploy_ui_settings_json_body = cls(
            deploy_ui_settings=deploy_ui_settings,
        )

        edit_workspace_deploy_ui_settings_json_body.additional_properties = d
        return edit_workspace_deploy_ui_settings_json_body

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
