from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_job_object_input_entity_type_type_0 import (
    TJobObjectInputEntityTypeType0,
)

T = TypeVar("T", bound="TJobObjectInput")


@_attrs_define
class TJobObjectInput:
    """
    Attributes:
        entity_type (Literal['job-run'] | TJobObjectInputEntityTypeType0):
        input_ (str):
    """

    entity_type: Literal["job-run"] | TJobObjectInputEntityTypeType0
    input_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity_type: Literal["job-run"] | str
        if isinstance(self.entity_type, TJobObjectInputEntityTypeType0):
            entity_type = self.entity_type.value
        else:
            entity_type = self.entity_type

        input_ = self.input_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_type": entity_type,
                "input": input_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_entity_type(
            data: object,
        ) -> Literal["job-run"] | TJobObjectInputEntityTypeType0:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                entity_type_type_0 = TJobObjectInputEntityTypeType0(data)

                return entity_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            entity_type_type_1 = cast(Literal["job-run"], data)
            if entity_type_type_1 != "job-run":
                raise ValueError(
                    f"entity_type_type_1 must match const 'job-run', got '{entity_type_type_1}'"
                )
            return entity_type_type_1

        entity_type = _parse_entity_type(d.pop("entity_type"))

        input_ = d.pop("input")

        t_job_object_input = cls(
            entity_type=entity_type,
            input_=input_,
        )

        t_job_object_input.additional_properties = d
        return t_job_object_input

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
