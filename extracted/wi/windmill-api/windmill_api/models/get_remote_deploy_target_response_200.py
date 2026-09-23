from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_remote_deploy_target_response_200_connection import GetRemoteDeployTargetResponse200Connection
    from ..models.get_remote_deploy_target_response_200_target import GetRemoteDeployTargetResponse200Target


T = TypeVar("T", bound="GetRemoteDeployTargetResponse200")


@_attrs_define
class GetRemoteDeployTargetResponse200:
    """
    Attributes:
        target (Union[Unset, GetRemoteDeployTargetResponse200Target]):
        connection (Union[Unset, GetRemoteDeployTargetResponse200Connection]):
    """

    target: Union[Unset, "GetRemoteDeployTargetResponse200Target"] = UNSET
    connection: Union[Unset, "GetRemoteDeployTargetResponse200Connection"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        target: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        connection: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.connection, Unset):
            connection = self.connection.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if connection is not UNSET:
            field_dict["connection"] = connection

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_remote_deploy_target_response_200_connection import GetRemoteDeployTargetResponse200Connection
        from ..models.get_remote_deploy_target_response_200_target import GetRemoteDeployTargetResponse200Target

        d = src_dict.copy()
        _target = d.pop("target", UNSET)
        target: Union[Unset, GetRemoteDeployTargetResponse200Target]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = GetRemoteDeployTargetResponse200Target.from_dict(_target)

        _connection = d.pop("connection", UNSET)
        connection: Union[Unset, GetRemoteDeployTargetResponse200Connection]
        if isinstance(_connection, Unset):
            connection = UNSET
        else:
            connection = GetRemoteDeployTargetResponse200Connection.from_dict(_connection)

        get_remote_deploy_target_response_200 = cls(
            target=target,
            connection=connection,
        )

        get_remote_deploy_target_response_200.additional_properties = d
        return get_remote_deploy_target_response_200

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
