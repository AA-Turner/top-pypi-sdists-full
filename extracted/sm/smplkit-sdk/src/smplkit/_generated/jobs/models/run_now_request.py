from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="RunNowRequest")


@_attrs_define
class RunNowRequest:
    """Request body for the run-now action (`POST /jobs/{id}/actions/run`).

    A plain object (not a JSON:API envelope), matching the platform convention
    for action endpoints. The body itself is optional — omit it entirely when
    the target environment is unambiguous.

        Attributes:
            environment (None | str | Unset): The environment to run the job in. Must be one the job is **enabled** in
                (otherwise the request is rejected). Optional when the target is unambiguous: when the job is enabled in exactly
                one environment, or your credential is scoped to a single environment, that environment is used.
    """

    environment: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_environment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        run_now_request = cls(
            environment=environment,
        )

        run_now_request.additional_properties = d
        return run_now_request

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
