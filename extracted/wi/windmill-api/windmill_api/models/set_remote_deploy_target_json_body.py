from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.set_remote_deploy_target_json_body_target import SetRemoteDeployTargetJsonBodyTarget


T = TypeVar("T", bound="SetRemoteDeployTargetJsonBody")


@_attrs_define
class SetRemoteDeployTargetJsonBody:
    """
    Attributes:
        target (Union[Unset, SetRemoteDeployTargetJsonBodyTarget]):
    """

    target: Union[Unset, "SetRemoteDeployTargetJsonBodyTarget"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        target: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.set_remote_deploy_target_json_body_target import SetRemoteDeployTargetJsonBodyTarget

        d = src_dict.copy()
        _target = d.pop("target", UNSET)
        target: Union[Unset, SetRemoteDeployTargetJsonBodyTarget]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = SetRemoteDeployTargetJsonBodyTarget.from_dict(_target)

        set_remote_deploy_target_json_body = cls(
            target=target,
        )

        set_remote_deploy_target_json_body.additional_properties = d
        return set_remote_deploy_target_json_body

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
