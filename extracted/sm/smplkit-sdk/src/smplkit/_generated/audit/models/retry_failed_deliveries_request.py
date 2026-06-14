from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="RetryFailedDeliveriesRequest")


@_attrs_define
class RetryFailedDeliveriesRequest:
    """Inputs to the retry-failed-deliveries action.

    Attributes:
        environment (None | str | Unset): The single environment whose failed deliveries are re-attempted. Omit it and a
            single-environment credential implies it (a multi-environment credential must name it), and a named environment
            must be one the caller may access. The action always targets exactly one environment.
    """

    environment: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        field_dict: dict[str, Any] = {}

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

        retry_failed_deliveries_request = cls(
            environment=environment,
        )

        return retry_failed_deliveries_request
