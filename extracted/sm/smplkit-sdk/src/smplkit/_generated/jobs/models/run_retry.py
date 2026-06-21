from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from uuid import UUID


T = TypeVar("T", bound="RunRetry")


@_attrs_define
class RunRetry:
    """Where a `RETRY` run sits in its retry chain.

    Attributes:
        of (UUID): The id of the chain's original run — the first attempt that failed and started the chain.
        attempt (int): Which retry this run is: `1` for the first retry, `2` for the second, and so on.
    """

    of: UUID
    attempt: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        of = str(self.of)

        attempt = self.attempt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "of": of,
                "attempt": attempt,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        of = UUID(d.pop("of"))

        attempt = d.pop("attempt")

        run_retry = cls(
            of=of,
            attempt=attempt,
        )

        run_retry.additional_properties = d
        return run_retry

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
