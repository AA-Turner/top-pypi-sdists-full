from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.lb_algorithm_enum import LbAlgorithmEnum
from ..models.load_balancer_protocol_enum import LoadBalancerProtocolEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePool")


@_attrs_define
class CreatePool:
    """
    Attributes:
        url (str):
        uuid (UUID):
        load_balancer (str): Load balancer this pool belongs to
        name (str):
        protocol (LoadBalancerProtocolEnum):
        project (str):
        service_settings (str):
        lb_algorithm (Union[Unset, LbAlgorithmEnum]):  Default: LbAlgorithmEnum.SOURCE_IP_PORT.
    """

    url: str
    uuid: UUID
    load_balancer: str
    name: str
    protocol: LoadBalancerProtocolEnum
    project: str
    service_settings: str
    lb_algorithm: Union[Unset, LbAlgorithmEnum] = LbAlgorithmEnum.SOURCE_IP_PORT
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        load_balancer = self.load_balancer

        name = self.name

        protocol = self.protocol.value

        project = self.project

        service_settings = self.service_settings

        lb_algorithm: Union[Unset, str] = UNSET
        if not isinstance(self.lb_algorithm, Unset):
            lb_algorithm = self.lb_algorithm.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "load_balancer": load_balancer,
                "name": name,
                "protocol": protocol,
                "project": project,
                "service_settings": service_settings,
            }
        )
        if lb_algorithm is not UNSET:
            field_dict["lb_algorithm"] = lb_algorithm

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        load_balancer = d.pop("load_balancer")

        name = d.pop("name")

        protocol = LoadBalancerProtocolEnum(d.pop("protocol"))

        project = d.pop("project")

        service_settings = d.pop("service_settings")

        _lb_algorithm = d.pop("lb_algorithm", UNSET)
        lb_algorithm: Union[Unset, LbAlgorithmEnum]
        if isinstance(_lb_algorithm, Unset):
            lb_algorithm = UNSET
        else:
            lb_algorithm = LbAlgorithmEnum(_lb_algorithm)

        create_pool = cls(
            url=url,
            uuid=uuid,
            load_balancer=load_balancer,
            name=name,
            protocol=protocol,
            project=project,
            service_settings=service_settings,
            lb_algorithm=lb_algorithm,
        )

        create_pool.additional_properties = d
        return create_pool

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
