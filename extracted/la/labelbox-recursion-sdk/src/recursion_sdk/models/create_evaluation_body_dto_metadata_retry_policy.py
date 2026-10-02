from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateEvaluationBodyDtoMetadataRetryPolicy")



@_attrs_define
class CreateEvaluationBodyDtoMetadataRetryPolicy:
    """ Infra-retry policy override applied to every problem run in this evaluation, taking precedence over the run-config-
    level override when both are set. Omit to use the run-config value (or the platform default if neither is set).

        Attributes:
            max_infra_retries (int | Unset): Additional attempts allowed after a failure classified as infra (container
                eviction, image pull error, queue orphan) before the run terminates as failed. Omit to use the platform default
                (2).
     """

    max_infra_retries: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        max_infra_retries = self.max_infra_retries


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if max_infra_retries is not UNSET:
            field_dict["maxInfraRetries"] = max_infra_retries

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_infra_retries = d.pop("maxInfraRetries", UNSET)

        create_evaluation_body_dto_metadata_retry_policy = cls(
            max_infra_retries=max_infra_retries,
        )


        create_evaluation_body_dto_metadata_retry_policy.additional_properties = d
        return create_evaluation_body_dto_metadata_retry_policy

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
