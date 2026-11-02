from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.remote_deploy_status_connection import RemoteDeployStatusConnection
    from ..models.remote_deploy_status_target import RemoteDeployStatusTarget


T = TypeVar("T", bound="RemoteDeployStatus")


@_attrs_define
class RemoteDeployStatus:
    """
    Attributes:
        target (Union[Unset, RemoteDeployStatusTarget]):
        connection (Union[Unset, RemoteDeployStatusConnection]):
    """

    target: Union[Unset, "RemoteDeployStatusTarget"] = UNSET
    connection: Union[Unset, "RemoteDeployStatusConnection"] = UNSET
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
        from ..models.remote_deploy_status_connection import RemoteDeployStatusConnection
        from ..models.remote_deploy_status_target import RemoteDeployStatusTarget

        d = src_dict.copy()
        _target = d.pop("target", UNSET)
        target: Union[Unset, RemoteDeployStatusTarget]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = RemoteDeployStatusTarget.from_dict(_target)

        _connection = d.pop("connection", UNSET)
        connection: Union[Unset, RemoteDeployStatusConnection]
        if isinstance(_connection, Unset):
            connection = UNSET
        else:
            connection = RemoteDeployStatusConnection.from_dict(_connection)

        remote_deploy_status = cls(
            target=target,
            connection=connection,
        )

        remote_deploy_status.additional_properties = d
        return remote_deploy_status

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
