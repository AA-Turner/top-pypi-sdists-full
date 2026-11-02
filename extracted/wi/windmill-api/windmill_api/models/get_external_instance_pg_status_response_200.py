from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_external_instance_pg_status_response_200_last_setup import (
        GetExternalInstancePgStatusResponse200LastSetup,
    )


T = TypeVar("T", bound="GetExternalInstancePgStatusResponse200")


@_attrs_define
class GetExternalInstancePgStatusResponse200:
    """
    Attributes:
        configured (bool):
        database_count (int):
        last_setup (Union[Unset, GetExternalInstancePgStatusResponse200LastSetup]):
    """

    configured: bool
    database_count: int
    last_setup: Union[Unset, "GetExternalInstancePgStatusResponse200LastSetup"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        configured = self.configured
        database_count = self.database_count
        last_setup: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_setup, Unset):
            last_setup = self.last_setup.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "configured": configured,
                "database_count": database_count,
            }
        )
        if last_setup is not UNSET:
            field_dict["last_setup"] = last_setup

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_external_instance_pg_status_response_200_last_setup import (
            GetExternalInstancePgStatusResponse200LastSetup,
        )

        d = src_dict.copy()
        configured = d.pop("configured")

        database_count = d.pop("database_count")

        _last_setup = d.pop("last_setup", UNSET)
        last_setup: Union[Unset, GetExternalInstancePgStatusResponse200LastSetup]
        if isinstance(_last_setup, Unset):
            last_setup = UNSET
        else:
            last_setup = GetExternalInstancePgStatusResponse200LastSetup.from_dict(_last_setup)

        get_external_instance_pg_status_response_200 = cls(
            configured=configured,
            database_count=database_count,
            last_setup=last_setup,
        )

        get_external_instance_pg_status_response_200.additional_properties = d
        return get_external_instance_pg_status_response_200

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
