from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_entry_point_job_type import TEntryPointJobType

T = TypeVar("T", bound="TEntryPoint")


@_attrs_define
class TEntryPoint:
    """
    Attributes:
        function (None | str):
        job_type (TEntryPointJobType):
        launcher (str):
        module (str):
    """

    function: None | str
    job_type: TEntryPointJobType
    launcher: str
    module: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        function: None | str
        function = self.function

        job_type = self.job_type.value

        launcher = self.launcher

        module = self.module

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "function": function,
                "job_type": job_type,
                "launcher": launcher,
                "module": module,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_function(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        function = _parse_function(d.pop("function"))

        job_type = TEntryPointJobType(d.pop("job_type"))

        launcher = d.pop("launcher")

        module = d.pop("module")

        t_entry_point = cls(
            function=function,
            job_type=job_type,
            launcher=launcher,
            module=module,
        )

        t_entry_point.additional_properties = d
        return t_entry_point

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
