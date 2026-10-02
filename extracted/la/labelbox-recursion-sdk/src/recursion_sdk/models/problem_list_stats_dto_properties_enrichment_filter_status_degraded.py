from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_list_stats_dto_properties_enrichment_filter_status_degraded_reason import ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedReason
from ..models.problem_list_stats_dto_properties_enrichment_filter_status_degraded_state import ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedState






T = TypeVar("T", bound="ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded")



@_attrs_define
class ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegraded:
    """ 
        Attributes:
            state (ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedState): Discriminator selecting the variant.
            reason (ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedReason): Reason code explaining why
                enrichment filtering degraded.
     """

    state: ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedState
    reason: ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedReason





    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        reason = self.reason.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "state": state,
            "reason": reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedState(d.pop("state"))




        reason = ProblemListStatsDtoPropertiesEnrichmentFilterStatusDegradedReason(d.pop("reason"))




        problem_list_stats_dto_properties_enrichment_filter_status_degraded = cls(
            state=state,
            reason=reason,
        )

        return problem_list_stats_dto_properties_enrichment_filter_status_degraded

