from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_external_instance_pg_databases_response_200_additional_property_tag import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyTag,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_external_instance_pg_databases_response_200_additional_property_logs import (
        ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs,
    )


T = TypeVar("T", bound="ListExternalInstancePgDatabasesResponse200AdditionalProperty")


@_attrs_define
class ListExternalInstancePgDatabasesResponse200AdditionalProperty:
    """
    Attributes:
        logs (ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs):
        success (bool): Whether the operation completed successfully Example: True.
        error (Union[Unset, None, str]): Error message if the operation failed Example: Connection timeout.
        tag (Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyTag]):
        used_by_workspaces (Union[Unset, List[str]]): Workspaces that reference this database through a ducklake catalog
            or a datatable database of the kind being listed — 'instance' for the instance databases endpoint,
            'external_instance' for the external cluster one. Computed at request time, not persisted, and only returned to
            superadmins.
        workspace_id (Union[Unset, str]): The workspace a member created this database for as a fork copy. Only that
            workspace can import into it or point a fork at it.
    """

    logs: "ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs"
    success: bool
    error: Union[Unset, None, str] = UNSET
    tag: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyTag] = UNSET
    used_by_workspaces: Union[Unset, List[str]] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        logs = self.logs.to_dict()

        success = self.success
        error = self.error
        tag: Union[Unset, str] = UNSET
        if not isinstance(self.tag, Unset):
            tag = self.tag.value

        used_by_workspaces: Union[Unset, List[str]] = UNSET
        if not isinstance(self.used_by_workspaces, Unset):
            used_by_workspaces = self.used_by_workspaces

        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logs": logs,
                "success": success,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if tag is not UNSET:
            field_dict["tag"] = tag
        if used_by_workspaces is not UNSET:
            field_dict["used_by_workspaces"] = used_by_workspaces
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_external_instance_pg_databases_response_200_additional_property_logs import (
            ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs,
        )

        d = src_dict.copy()
        logs = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs.from_dict(d.pop("logs"))

        success = d.pop("success")

        error = d.pop("error", UNSET)

        _tag = d.pop("tag", UNSET)
        tag: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyTag]
        if isinstance(_tag, Unset):
            tag = UNSET
        else:
            tag = ListExternalInstancePgDatabasesResponse200AdditionalPropertyTag(_tag)

        used_by_workspaces = cast(List[str], d.pop("used_by_workspaces", UNSET))

        workspace_id = d.pop("workspace_id", UNSET)

        list_external_instance_pg_databases_response_200_additional_property = cls(
            logs=logs,
            success=success,
            error=error,
            tag=tag,
            used_by_workspaces=used_by_workspaces,
            workspace_id=workspace_id,
        )

        list_external_instance_pg_databases_response_200_additional_property.additional_properties = d
        return list_external_instance_pg_databases_response_200_additional_property

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
