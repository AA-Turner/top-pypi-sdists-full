from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attach_dev_workspace_json_body_dev_workspace_label import AttachDevWorkspaceJsonBodyDevWorkspaceLabel
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachDevWorkspaceJsonBody")


@_attrs_define
class AttachDevWorkspaceJsonBody:
    """
    Attributes:
        dev_workspace_id (str):
        lock_prod_deploy (Union[Unset, bool]):
        lock_prod_forking (Union[Unset, bool]):
        dev_workspace_label (Union[Unset, AttachDevWorkspaceJsonBodyDevWorkspaceLabel]): Environment label; also names
            the branch the dev workspace deploys to. Omitted defaults to 'dev'
    """

    dev_workspace_id: str
    lock_prod_deploy: Union[Unset, bool] = UNSET
    lock_prod_forking: Union[Unset, bool] = UNSET
    dev_workspace_label: Union[Unset, AttachDevWorkspaceJsonBodyDevWorkspaceLabel] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dev_workspace_id = self.dev_workspace_id
        lock_prod_deploy = self.lock_prod_deploy
        lock_prod_forking = self.lock_prod_forking
        dev_workspace_label: Union[Unset, str] = UNSET
        if not isinstance(self.dev_workspace_label, Unset):
            dev_workspace_label = self.dev_workspace_label.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dev_workspace_id": dev_workspace_id,
            }
        )
        if lock_prod_deploy is not UNSET:
            field_dict["lock_prod_deploy"] = lock_prod_deploy
        if lock_prod_forking is not UNSET:
            field_dict["lock_prod_forking"] = lock_prod_forking
        if dev_workspace_label is not UNSET:
            field_dict["dev_workspace_label"] = dev_workspace_label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dev_workspace_id = d.pop("dev_workspace_id")

        lock_prod_deploy = d.pop("lock_prod_deploy", UNSET)

        lock_prod_forking = d.pop("lock_prod_forking", UNSET)

        _dev_workspace_label = d.pop("dev_workspace_label", UNSET)
        dev_workspace_label: Union[Unset, AttachDevWorkspaceJsonBodyDevWorkspaceLabel]
        if isinstance(_dev_workspace_label, Unset):
            dev_workspace_label = UNSET
        else:
            dev_workspace_label = AttachDevWorkspaceJsonBodyDevWorkspaceLabel(_dev_workspace_label)

        attach_dev_workspace_json_body = cls(
            dev_workspace_id=dev_workspace_id,
            lock_prod_deploy=lock_prod_deploy,
            lock_prod_forking=lock_prod_forking,
            dev_workspace_label=dev_workspace_label,
        )

        attach_dev_workspace_json_body.additional_properties = d
        return attach_dev_workspace_json_body

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
