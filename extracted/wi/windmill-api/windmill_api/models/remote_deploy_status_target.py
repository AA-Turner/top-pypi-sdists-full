from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RemoteDeployStatusTarget")


@_attrs_define
class RemoteDeployStatusTarget:
    """
    Attributes:
        base_url (str): root URL of the remote Windmill instance, without /api
        workspace_id (str): workspace on the remote instance that deploys land in
    """

    base_url: str
    workspace_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base_url = self.base_url
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_url": base_url,
                "workspace_id": workspace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_url = d.pop("base_url")

        workspace_id = d.pop("workspace_id")

        remote_deploy_status_target = cls(
            base_url=base_url,
            workspace_id=workspace_id,
        )

        remote_deploy_status_target.additional_properties = d
        return remote_deploy_status_target

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
