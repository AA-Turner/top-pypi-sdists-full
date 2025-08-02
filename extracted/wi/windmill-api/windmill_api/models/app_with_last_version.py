import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.app_with_last_version_execution_mode import AppWithLastVersionExecutionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.app_with_last_version_extra_perms import AppWithLastVersionExtraPerms
    from ..models.app_with_last_version_policy import AppWithLastVersionPolicy
    from ..models.app_with_last_version_value import AppWithLastVersionValue


T = TypeVar("T", bound="AppWithLastVersion")


@_attrs_define
class AppWithLastVersion:
    """
    Attributes:
        id (int):
        workspace_id (str):
        path (str):
        summary (str):
        versions (List[int]):
        created_by (str):
        created_at (datetime.datetime):
        value (AppWithLastVersionValue):
        policy (AppWithLastVersionPolicy):
        execution_mode (AppWithLastVersionExecutionMode):
        extra_perms (AppWithLastVersionExtraPerms):
        custom_path (Union[Unset, str]):
    """

    id: int
    workspace_id: str
    path: str
    summary: str
    versions: List[int]
    created_by: str
    created_at: datetime.datetime
    value: "AppWithLastVersionValue"
    policy: "AppWithLastVersionPolicy"
    execution_mode: AppWithLastVersionExecutionMode
    extra_perms: "AppWithLastVersionExtraPerms"
    custom_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        path = self.path
        summary = self.summary
        versions = self.versions

        created_by = self.created_by
        created_at = self.created_at.isoformat()

        value = self.value.to_dict()

        policy = self.policy.to_dict()

        execution_mode = self.execution_mode.value

        extra_perms = self.extra_perms.to_dict()

        custom_path = self.custom_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workspace_id": workspace_id,
                "path": path,
                "summary": summary,
                "versions": versions,
                "created_by": created_by,
                "created_at": created_at,
                "value": value,
                "policy": policy,
                "execution_mode": execution_mode,
                "extra_perms": extra_perms,
            }
        )
        if custom_path is not UNSET:
            field_dict["custom_path"] = custom_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.app_with_last_version_extra_perms import AppWithLastVersionExtraPerms
        from ..models.app_with_last_version_policy import AppWithLastVersionPolicy
        from ..models.app_with_last_version_value import AppWithLastVersionValue

        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        summary = d.pop("summary")

        versions = cast(List[int], d.pop("versions"))

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        value = AppWithLastVersionValue.from_dict(d.pop("value"))

        policy = AppWithLastVersionPolicy.from_dict(d.pop("policy"))

        execution_mode = AppWithLastVersionExecutionMode(d.pop("execution_mode"))

        extra_perms = AppWithLastVersionExtraPerms.from_dict(d.pop("extra_perms"))

        custom_path = d.pop("custom_path", UNSET)

        app_with_last_version = cls(
            id=id,
            workspace_id=workspace_id,
            path=path,
            summary=summary,
            versions=versions,
            created_by=created_by,
            created_at=created_at,
            value=value,
            policy=policy,
            execution_mode=execution_mode,
            extra_perms=extra_perms,
            custom_path=custom_path,
        )

        app_with_last_version.additional_properties = d
        return app_with_last_version

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
