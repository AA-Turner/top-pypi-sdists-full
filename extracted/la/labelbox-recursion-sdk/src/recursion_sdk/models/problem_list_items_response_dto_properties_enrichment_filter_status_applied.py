from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_applied_state import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusAppliedState






T = TypeVar("T", bound="ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied")



@_attrs_define
class ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied:
    """ 
        Attributes:
            state (ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusAppliedState): Discriminator selecting the
                variant.
     """

    state: ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusAppliedState





    def to_dict(self) -> dict[str, Any]:
        state = self.state.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "state": state,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusAppliedState(d.pop("state"))




        problem_list_items_response_dto_properties_enrichment_filter_status_applied = cls(
            state=state,
        )

        return problem_list_items_response_dto_properties_enrichment_filter_status_applied

