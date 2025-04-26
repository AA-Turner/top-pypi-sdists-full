import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_apps_response_200_item_execution_mode import ListAppsResponse200ItemExecutionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_apps_response_200_item_extra_perms import ListAppsResponse200ItemExtraPerms


T = TypeVar("T", bound="ListAppsResponse200Item")


@_attrs_define
class ListAppsResponse200Item:
    """
    Attributes:
        id (int):
        workspace_id (str):
        path (str):
        summary (str):
        version (int):
        extra_perms (ListAppsResponse200ItemExtraPerms):
        edited_at (datetime.datetime):
        execution_mode (ListAppsResponse200ItemExecutionMode):
        starred (Union[Unset, bool]):
        raw_app (Union[Unset, bool]):
    """

    id: int
    workspace_id: str
    path: str
    summary: str
    version: int
    extra_perms: "ListAppsResponse200ItemExtraPerms"
    edited_at: datetime.datetime
    execution_mode: ListAppsResponse200ItemExecutionMode
    starred: Union[Unset, bool] = UNSET
    raw_app: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        path = self.path
        summary = self.summary
        version = self.version
        extra_perms = self.extra_perms.to_dict()

        edited_at = self.edited_at.isoformat()

        execution_mode = self.execution_mode.value

        starred = self.starred
        raw_app = self.raw_app

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workspace_id": workspace_id,
                "path": path,
                "summary": summary,
                "version": version,
                "extra_perms": extra_perms,
                "edited_at": edited_at,
                "execution_mode": execution_mode,
            }
        )
        if starred is not UNSET:
            field_dict["starred"] = starred
        if raw_app is not UNSET:
            field_dict["raw_app"] = raw_app

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_apps_response_200_item_extra_perms import ListAppsResponse200ItemExtraPerms

        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        summary = d.pop("summary")

        version = d.pop("version")

        extra_perms = ListAppsResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        edited_at = isoparse(d.pop("edited_at"))

        execution_mode = ListAppsResponse200ItemExecutionMode(d.pop("execution_mode"))

        starred = d.pop("starred", UNSET)

        raw_app = d.pop("raw_app", UNSET)

        list_apps_response_200_item = cls(
            id=id,
            workspace_id=workspace_id,
            path=path,
            summary=summary,
            version=version,
            extra_perms=extra_perms,
            edited_at=edited_at,
            execution_mode=execution_mode,
            starred=starred,
            raw_app=raw_app,
        )

        list_apps_response_200_item.additional_properties = d
        return list_apps_response_200_item

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
