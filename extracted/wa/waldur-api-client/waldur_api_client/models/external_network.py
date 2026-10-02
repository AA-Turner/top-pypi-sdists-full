from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.external_subnet import ExternalSubnet


T = TypeVar("T", bound="ExternalNetwork")


@_attrs_define
class ExternalNetwork:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        settings (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        is_shared (Union[Unset, bool]):
        is_default (Union[Unset, bool]):
        status (Union[Unset, str]):
        description (Union[Unset, str]):
        subnets (Union[Unset, list['ExternalSubnet']]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    settings: Union[Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    is_default: Union[Unset, bool] = UNSET
    status: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    subnets: Union[Unset, list["ExternalSubnet"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        settings = self.settings

        backend_id = self.backend_id

        is_shared = self.is_shared

        is_default = self.is_default

        status = self.status

        description = self.description

        subnets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subnets, Unset):
            subnets = []
            for subnets_item_data in self.subnets:
                subnets_item = subnets_item_data.to_dict()
                subnets.append(subnets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if settings is not UNSET:
            field_dict["settings"] = settings
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared
        if is_default is not UNSET:
            field_dict["is_default"] = is_default
        if status is not UNSET:
            field_dict["status"] = status
        if description is not UNSET:
            field_dict["description"] = description
        if subnets is not UNSET:
            field_dict["subnets"] = subnets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.external_subnet import ExternalSubnet

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        settings = d.pop("settings", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        is_shared = d.pop("is_shared", UNSET)

        is_default = d.pop("is_default", UNSET)

        status = d.pop("status", UNSET)

        description = d.pop("description", UNSET)

        subnets = []
        _subnets = d.pop("subnets", UNSET)
        for subnets_item_data in _subnets or []:
            subnets_item = ExternalSubnet.from_dict(subnets_item_data)

            subnets.append(subnets_item)

        external_network = cls(
            url=url,
            uuid=uuid,
            name=name,
            settings=settings,
            backend_id=backend_id,
            is_shared=is_shared,
            is_default=is_default,
            status=status,
            description=description,
            subnets=subnets,
        )

        external_network.additional_properties = d
        return external_network

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
