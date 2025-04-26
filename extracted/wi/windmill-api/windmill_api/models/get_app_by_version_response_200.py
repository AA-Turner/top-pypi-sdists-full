import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_app_by_version_response_200_execution_mode import GetAppByVersionResponse200ExecutionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_app_by_version_response_200_extra_perms import GetAppByVersionResponse200ExtraPerms
    from ..models.get_app_by_version_response_200_policy import GetAppByVersionResponse200Policy
    from ..models.get_app_by_version_response_200_value import GetAppByVersionResponse200Value


T = TypeVar("T", bound="GetAppByVersionResponse200")


@_attrs_define
class GetAppByVersionResponse200:
    """
    Attributes:
        id (int):
        workspace_id (str):
        path (str):
        summary (str):
        versions (List[int]):
        created_by (str):
        created_at (datetime.datetime):
        value (GetAppByVersionResponse200Value):
        policy (GetAppByVersionResponse200Policy):
        execution_mode (GetAppByVersionResponse200ExecutionMode):
        extra_perms (GetAppByVersionResponse200ExtraPerms):
        custom_path (Union[Unset, str]):
    """

    id: int
    workspace_id: str
    path: str
    summary: str
    versions: List[int]
    created_by: str
    created_at: datetime.datetime
    value: "GetAppByVersionResponse200Value"
    policy: "GetAppByVersionResponse200Policy"
    execution_mode: GetAppByVersionResponse200ExecutionMode
    extra_perms: "GetAppByVersionResponse200ExtraPerms"
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
        from ..models.get_app_by_version_response_200_extra_perms import GetAppByVersionResponse200ExtraPerms
        from ..models.get_app_by_version_response_200_policy import GetAppByVersionResponse200Policy
        from ..models.get_app_by_version_response_200_value import GetAppByVersionResponse200Value

        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        summary = d.pop("summary")

        versions = cast(List[int], d.pop("versions"))

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        value = GetAppByVersionResponse200Value.from_dict(d.pop("value"))

        policy = GetAppByVersionResponse200Policy.from_dict(d.pop("policy"))

        execution_mode = GetAppByVersionResponse200ExecutionMode(d.pop("execution_mode"))

        extra_perms = GetAppByVersionResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        custom_path = d.pop("custom_path", UNSET)

        get_app_by_version_response_200 = cls(
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

        get_app_by_version_response_200.additional_properties = d
        return get_app_by_version_response_200

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
