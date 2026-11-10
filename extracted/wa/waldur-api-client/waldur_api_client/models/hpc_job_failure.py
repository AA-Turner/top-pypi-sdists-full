from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcJobFailure")


@_attrs_define
class HpcJobFailure:
    """
    Attributes:
        exit_code (Union[None, int]):
        count (int):
        names (list[str]):
        latest_job_id (Union[None, str]):
    """

    exit_code: Union[None, int]
    count: int
    names: list[str]
    latest_job_id: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exit_code: Union[None, int]
        exit_code = self.exit_code

        count = self.count

        names = self.names

        latest_job_id: Union[None, str]
        latest_job_id = self.latest_job_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exit_code": exit_code,
                "count": count,
                "names": names,
                "latest_job_id": latest_job_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_exit_code(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        exit_code = _parse_exit_code(d.pop("exit_code"))

        count = d.pop("count")

        names = cast(list[str], d.pop("names"))

        def _parse_latest_job_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        latest_job_id = _parse_latest_job_id(d.pop("latest_job_id"))

        hpc_job_failure = cls(
            exit_code=exit_code,
            count=count,
            names=names,
            latest_job_id=latest_job_id,
        )

        hpc_job_failure.additional_properties = d
        return hpc_job_failure

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
