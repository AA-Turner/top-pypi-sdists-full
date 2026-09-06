from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_public_settings_response_200_datatable import GetPublicSettingsResponse200Datatable
    from ..models.get_public_settings_response_200_deploy_ui import GetPublicSettingsResponse200DeployUi
    from ..models.get_public_settings_response_200_large_file_storage import (
        GetPublicSettingsResponse200LargeFileStorage,
    )


T = TypeVar("T", bound="GetPublicSettingsResponse200")


@_attrs_define
class GetPublicSettingsResponse200:
    """
    Attributes:
        workspace_id (str):
        guest_access_enabled (bool): Whether this workspace admits guest sessions. An app's own `guest` execution mode
            is inert while this is false.
        slack_name (Union[Unset, str]):
        slack_team_id (Union[Unset, str]):
        teams_team_id (Union[Unset, str]):
        teams_team_name (Union[Unset, str]):
        teams_team_guid (Union[Unset, str]):
        large_file_storage (Union[Unset, GetPublicSettingsResponse200LargeFileStorage]):
        datatable (Union[Unset, GetPublicSettingsResponse200Datatable]):
        deploy_ui (Union[Unset, GetPublicSettingsResponse200DeployUi]):
        mute_critical_alerts (Union[Unset, bool]):
    """

    workspace_id: str
    guest_access_enabled: bool
    slack_name: Union[Unset, str] = UNSET
    slack_team_id: Union[Unset, str] = UNSET
    teams_team_id: Union[Unset, str] = UNSET
    teams_team_name: Union[Unset, str] = UNSET
    teams_team_guid: Union[Unset, str] = UNSET
    large_file_storage: Union[Unset, "GetPublicSettingsResponse200LargeFileStorage"] = UNSET
    datatable: Union[Unset, "GetPublicSettingsResponse200Datatable"] = UNSET
    deploy_ui: Union[Unset, "GetPublicSettingsResponse200DeployUi"] = UNSET
    mute_critical_alerts: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        guest_access_enabled = self.guest_access_enabled
        slack_name = self.slack_name
        slack_team_id = self.slack_team_id
        teams_team_id = self.teams_team_id
        teams_team_name = self.teams_team_name
        teams_team_guid = self.teams_team_guid
        large_file_storage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.large_file_storage, Unset):
            large_file_storage = self.large_file_storage.to_dict()

        datatable: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.datatable, Unset):
            datatable = self.datatable.to_dict()

        deploy_ui: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deploy_ui, Unset):
            deploy_ui = self.deploy_ui.to_dict()

        mute_critical_alerts = self.mute_critical_alerts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "guest_access_enabled": guest_access_enabled,
            }
        )
        if slack_name is not UNSET:
            field_dict["slack_name"] = slack_name
        if slack_team_id is not UNSET:
            field_dict["slack_team_id"] = slack_team_id
        if teams_team_id is not UNSET:
            field_dict["teams_team_id"] = teams_team_id
        if teams_team_name is not UNSET:
            field_dict["teams_team_name"] = teams_team_name
        if teams_team_guid is not UNSET:
            field_dict["teams_team_guid"] = teams_team_guid
        if large_file_storage is not UNSET:
            field_dict["large_file_storage"] = large_file_storage
        if datatable is not UNSET:
            field_dict["datatable"] = datatable
        if deploy_ui is not UNSET:
            field_dict["deploy_ui"] = deploy_ui
        if mute_critical_alerts is not UNSET:
            field_dict["mute_critical_alerts"] = mute_critical_alerts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_public_settings_response_200_datatable import GetPublicSettingsResponse200Datatable
        from ..models.get_public_settings_response_200_deploy_ui import GetPublicSettingsResponse200DeployUi
        from ..models.get_public_settings_response_200_large_file_storage import (
            GetPublicSettingsResponse200LargeFileStorage,
        )

        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        guest_access_enabled = d.pop("guest_access_enabled")

        slack_name = d.pop("slack_name", UNSET)

        slack_team_id = d.pop("slack_team_id", UNSET)

        teams_team_id = d.pop("teams_team_id", UNSET)

        teams_team_name = d.pop("teams_team_name", UNSET)

        teams_team_guid = d.pop("teams_team_guid", UNSET)

        _large_file_storage = d.pop("large_file_storage", UNSET)
        large_file_storage: Union[Unset, GetPublicSettingsResponse200LargeFileStorage]
        if isinstance(_large_file_storage, Unset):
            large_file_storage = UNSET
        else:
            large_file_storage = GetPublicSettingsResponse200LargeFileStorage.from_dict(_large_file_storage)

        _datatable = d.pop("datatable", UNSET)
        datatable: Union[Unset, GetPublicSettingsResponse200Datatable]
        if isinstance(_datatable, Unset):
            datatable = UNSET
        else:
            datatable = GetPublicSettingsResponse200Datatable.from_dict(_datatable)

        _deploy_ui = d.pop("deploy_ui", UNSET)
        deploy_ui: Union[Unset, GetPublicSettingsResponse200DeployUi]
        if isinstance(_deploy_ui, Unset):
            deploy_ui = UNSET
        else:
            deploy_ui = GetPublicSettingsResponse200DeployUi.from_dict(_deploy_ui)

        mute_critical_alerts = d.pop("mute_critical_alerts", UNSET)

        get_public_settings_response_200 = cls(
            workspace_id=workspace_id,
            guest_access_enabled=guest_access_enabled,
            slack_name=slack_name,
            slack_team_id=slack_team_id,
            teams_team_id=teams_team_id,
            teams_team_name=teams_team_name,
            teams_team_guid=teams_team_guid,
            large_file_storage=large_file_storage,
            datatable=datatable,
            deploy_ui=deploy_ui,
            mute_critical_alerts=mute_critical_alerts,
        )

        get_public_settings_response_200.additional_properties = d
        return get_public_settings_response_200

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
