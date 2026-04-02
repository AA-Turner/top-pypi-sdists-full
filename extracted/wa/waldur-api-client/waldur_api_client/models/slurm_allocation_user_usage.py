from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SlurmAllocationUserUsage")


@_attrs_define
class SlurmAllocationUserUsage:
    """
    Attributes:
        month (int):
        year (int):
        allocation (str):
        username (str):
        full_name (str):
        cpu_usage (Union[Unset, int]):
        ram_usage (Union[Unset, int]):
        gpu_usage (Union[Unset, int]):
        user (Union[None, Unset, str]):
    """

    month: int
    year: int
    allocation: str
    username: str
    full_name: str
    cpu_usage: Union[Unset, int] = UNSET
    ram_usage: Union[Unset, int] = UNSET
    gpu_usage: Union[Unset, int] = UNSET
    user: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month = self.month

        year = self.year

        allocation = self.allocation

        username = self.username

        full_name = self.full_name

        cpu_usage = self.cpu_usage

        ram_usage = self.ram_usage

        gpu_usage = self.gpu_usage

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        else:
            user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "month": month,
                "year": year,
                "allocation": allocation,
                "username": username,
                "full_name": full_name,
            }
        )
        if cpu_usage is not UNSET:
            field_dict["cpu_usage"] = cpu_usage
        if ram_usage is not UNSET:
            field_dict["ram_usage"] = ram_usage
        if gpu_usage is not UNSET:
            field_dict["gpu_usage"] = gpu_usage
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month = d.pop("month")

        year = d.pop("year")

        allocation = d.pop("allocation")

        username = d.pop("username")

        full_name = d.pop("full_name")

        cpu_usage = d.pop("cpu_usage", UNSET)

        ram_usage = d.pop("ram_usage", UNSET)

        gpu_usage = d.pop("gpu_usage", UNSET)

        def _parse_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user = _parse_user(d.pop("user", UNSET))

        slurm_allocation_user_usage = cls(
            month=month,
            year=year,
            allocation=allocation,
            username=username,
            full_name=full_name,
            cpu_usage=cpu_usage,
            ram_usage=ram_usage,
            gpu_usage=gpu_usage,
            user=user,
        )

        slurm_allocation_user_usage.additional_properties = d
        return slurm_allocation_user_usage

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
