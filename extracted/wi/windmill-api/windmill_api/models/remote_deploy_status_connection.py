import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RemoteDeployStatusConnection")


@_attrs_define
class RemoteDeployStatusConnection:
    """
    Attributes:
        remote_email (str): identity the stored token has on the remote instance
        proxy_key (str): goes in every proxy URL, `/w/{workspace}/remote_deploy/proxy/{proxy_key}/{route}`
        connected_at (datetime.datetime):
    """

    remote_email: str
    proxy_key: str
    connected_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        remote_email = self.remote_email
        proxy_key = self.proxy_key
        connected_at = self.connected_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "remote_email": remote_email,
                "proxy_key": proxy_key,
                "connected_at": connected_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        remote_email = d.pop("remote_email")

        proxy_key = d.pop("proxy_key")

        connected_at = isoparse(d.pop("connected_at"))

        remote_deploy_status_connection = cls(
            remote_email=remote_email,
            proxy_key=proxy_key,
            connected_at=connected_at,
        )

        remote_deploy_status_connection.additional_properties = d
        return remote_deploy_status_connection

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
