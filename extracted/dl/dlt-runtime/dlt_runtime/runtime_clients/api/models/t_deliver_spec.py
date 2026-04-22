from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TDeliverSpec")


@_attrs_define
class TDeliverSpec:
    """
    Attributes:
        deadline (Union[Unset, str]):
        pipeline_name (Union[Unset, str]):
        source_ref (Union[Unset, str]):
    """

    deadline: Union[Unset, str] = UNSET
    pipeline_name: Union[Unset, str] = UNSET
    source_ref: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deadline = self.deadline

        pipeline_name = self.pipeline_name

        source_ref = self.source_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deadline is not UNSET:
            field_dict["deadline"] = deadline
        if pipeline_name is not UNSET:
            field_dict["pipeline_name"] = pipeline_name
        if source_ref is not UNSET:
            field_dict["source_ref"] = source_ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deadline = d.pop("deadline", UNSET)

        pipeline_name = d.pop("pipeline_name", UNSET)

        source_ref = d.pop("source_ref", UNSET)

        t_deliver_spec = cls(
            deadline=deadline,
            pipeline_name=pipeline_name,
            source_ref=source_ref,
        )

        t_deliver_spec.additional_properties = d
        return t_deliver_spec

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
