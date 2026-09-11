from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.t_timeout_spec import TTimeoutSpec


T = TypeVar("T", bound="TExecuteSpec")


@_attrs_define
class TExecuteSpec:
    """
    Attributes:
        concurrency (int | None | Unset):
        intercept_signals (bool | Unset):
        timeout (None | TTimeoutSpec | Unset):
    """

    concurrency: int | None | Unset = UNSET
    intercept_signals: bool | Unset = UNSET
    timeout: None | TTimeoutSpec | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.t_timeout_spec import TTimeoutSpec

        concurrency: int | None | Unset
        if isinstance(self.concurrency, Unset):
            concurrency = UNSET
        else:
            concurrency = self.concurrency

        intercept_signals = self.intercept_signals

        timeout: dict[str, Any] | None | Unset
        if isinstance(self.timeout, Unset):
            timeout = UNSET
        elif isinstance(self.timeout, TTimeoutSpec):
            timeout = self.timeout.to_dict()
        else:
            timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency
        if intercept_signals is not UNSET:
            field_dict["intercept_signals"] = intercept_signals
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.t_timeout_spec import TTimeoutSpec

        d = dict(src_dict)

        def _parse_concurrency(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        concurrency = _parse_concurrency(d.pop("concurrency", UNSET))

        intercept_signals = d.pop("intercept_signals", UNSET)

        def _parse_timeout(data: object) -> None | TTimeoutSpec | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                timeout_type_0 = TTimeoutSpec.from_dict(data)

                return timeout_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TTimeoutSpec | Unset, data)

        timeout = _parse_timeout(d.pop("timeout", UNSET))

        t_execute_spec = cls(
            concurrency=concurrency,
            intercept_signals=intercept_signals,
            timeout=timeout,
        )

        t_execute_spec.additional_properties = d
        return t_execute_spec

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
