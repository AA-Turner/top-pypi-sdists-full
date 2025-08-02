from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFlowDeploymentStatusResponse200")


@_attrs_define
class GetFlowDeploymentStatusResponse200:
    """
    Attributes:
        lock_error_logs (Union[Unset, str]):
    """

    lock_error_logs: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lock_error_logs = self.lock_error_logs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lock_error_logs is not UNSET:
            field_dict["lock_error_logs"] = lock_error_logs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lock_error_logs = d.pop("lock_error_logs", UNSET)

        get_flow_deployment_status_response_200 = cls(
            lock_error_logs=lock_error_logs,
        )

        get_flow_deployment_status_response_200.additional_properties = d
        return get_flow_deployment_status_response_200

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
