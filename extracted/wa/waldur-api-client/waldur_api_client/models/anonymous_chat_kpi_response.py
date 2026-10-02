from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.anonymous_chat_kpi_response_llm_intent_distribution import (
        AnonymousChatKpiResponseLlmIntentDistribution,
    )
    from ..models.daily_volume import DailyVolume
    from ..models.severity_by_day import SeverityByDay


T = TypeVar("T", bound="AnonymousChatKpiResponse")


@_attrs_define
class AnonymousChatKpiResponse:
    """
    Attributes:
        interactions_total (int):
        sessions_total (int):
        unique_users (int): Distinct user_slug values in the window — proxy for active anonymous users.
        flagged_total (int):
        feedback_positive (int):
        feedback_negative (int):
        satisfaction_rate (float): positive / (positive + negative); null when no human feedback.
        clicks_total (int):
        click_through_rate (float): clicks / interactions; null when no interactions.
        input_tokens_total (int): Prompt tokens summed over the filtered turns. Turns recorded before per-interaction
            token capture contribute nothing, so this understates spend on historical data.
        output_tokens_total (int): Completion tokens summed over the filtered turns.
        reviewed_total (int): Threads carrying a judge verdict. Always present, unlike the review rates below — zero
            here is the signal that the nightly pass is off or stalled, so consumers can keep showing the row.
        review_input_tokens_total (int): Prompt tokens spent by the LLM judge. Tracked apart from ``input_tokens_total``
            because review runs on its own budget.
        review_output_tokens_total (int): Completion tokens spent by the LLM judge.
        avg_llm_resolution_score (Union[None, Unset, float]): Mean of llm_resolution_score across reviewed sessions
            (1-5).
        llm_intent_distribution (Union[Unset, AnonymousChatKpiResponseLlmIntentDistribution]): Counts keyed by
            llm_intent_category.
        hallucination_rate (Union[None, Unset, float]): Share of reviewed sessions flagged as hallucinating.
        review_coverage (Union[None, Unset, float]): Reviewed sessions / total reviewable sessions. Operations health
            signal — drops below ~90% if the review budget is too tight or the task is failing.
        daily_volume (Union[Unset, list['DailyVolume']]): Per-day query counts across the filter window.
        severity_by_day (Union[Unset, SeverityByDay]):
    """

    interactions_total: int
    sessions_total: int
    unique_users: int
    flagged_total: int
    feedback_positive: int
    feedback_negative: int
    satisfaction_rate: float
    clicks_total: int
    click_through_rate: float
    input_tokens_total: int
    output_tokens_total: int
    reviewed_total: int
    review_input_tokens_total: int
    review_output_tokens_total: int
    avg_llm_resolution_score: Union[None, Unset, float] = UNSET
    llm_intent_distribution: Union[Unset, "AnonymousChatKpiResponseLlmIntentDistribution"] = UNSET
    hallucination_rate: Union[None, Unset, float] = UNSET
    review_coverage: Union[None, Unset, float] = UNSET
    daily_volume: Union[Unset, list["DailyVolume"]] = UNSET
    severity_by_day: Union[Unset, "SeverityByDay"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interactions_total = self.interactions_total

        sessions_total = self.sessions_total

        unique_users = self.unique_users

        flagged_total = self.flagged_total

        feedback_positive = self.feedback_positive

        feedback_negative = self.feedback_negative

        satisfaction_rate = self.satisfaction_rate

        clicks_total = self.clicks_total

        click_through_rate = self.click_through_rate

        input_tokens_total = self.input_tokens_total

        output_tokens_total = self.output_tokens_total

        reviewed_total = self.reviewed_total

        review_input_tokens_total = self.review_input_tokens_total

        review_output_tokens_total = self.review_output_tokens_total

        avg_llm_resolution_score: Union[None, Unset, float]
        if isinstance(self.avg_llm_resolution_score, Unset):
            avg_llm_resolution_score = UNSET
        else:
            avg_llm_resolution_score = self.avg_llm_resolution_score

        llm_intent_distribution: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.llm_intent_distribution, Unset):
            llm_intent_distribution = self.llm_intent_distribution.to_dict()

        hallucination_rate: Union[None, Unset, float]
        if isinstance(self.hallucination_rate, Unset):
            hallucination_rate = UNSET
        else:
            hallucination_rate = self.hallucination_rate

        review_coverage: Union[None, Unset, float]
        if isinstance(self.review_coverage, Unset):
            review_coverage = UNSET
        else:
            review_coverage = self.review_coverage

        daily_volume: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.daily_volume, Unset):
            daily_volume = []
            for daily_volume_item_data in self.daily_volume:
                daily_volume_item = daily_volume_item_data.to_dict()
                daily_volume.append(daily_volume_item)

        severity_by_day: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.severity_by_day, Unset):
            severity_by_day = self.severity_by_day.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interactions_total": interactions_total,
                "sessions_total": sessions_total,
                "unique_users": unique_users,
                "flagged_total": flagged_total,
                "feedback_positive": feedback_positive,
                "feedback_negative": feedback_negative,
                "satisfaction_rate": satisfaction_rate,
                "clicks_total": clicks_total,
                "click_through_rate": click_through_rate,
                "input_tokens_total": input_tokens_total,
                "output_tokens_total": output_tokens_total,
                "reviewed_total": reviewed_total,
                "review_input_tokens_total": review_input_tokens_total,
                "review_output_tokens_total": review_output_tokens_total,
            }
        )
        if avg_llm_resolution_score is not UNSET:
            field_dict["avg_llm_resolution_score"] = avg_llm_resolution_score
        if llm_intent_distribution is not UNSET:
            field_dict["llm_intent_distribution"] = llm_intent_distribution
        if hallucination_rate is not UNSET:
            field_dict["hallucination_rate"] = hallucination_rate
        if review_coverage is not UNSET:
            field_dict["review_coverage"] = review_coverage
        if daily_volume is not UNSET:
            field_dict["daily_volume"] = daily_volume
        if severity_by_day is not UNSET:
            field_dict["severity_by_day"] = severity_by_day

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.anonymous_chat_kpi_response_llm_intent_distribution import (
            AnonymousChatKpiResponseLlmIntentDistribution,
        )
        from ..models.daily_volume import DailyVolume
        from ..models.severity_by_day import SeverityByDay

        d = dict(src_dict)
        interactions_total = d.pop("interactions_total")

        sessions_total = d.pop("sessions_total")

        unique_users = d.pop("unique_users")

        flagged_total = d.pop("flagged_total")

        feedback_positive = d.pop("feedback_positive")

        feedback_negative = d.pop("feedback_negative")

        satisfaction_rate = d.pop("satisfaction_rate")

        clicks_total = d.pop("clicks_total")

        click_through_rate = d.pop("click_through_rate")

        input_tokens_total = d.pop("input_tokens_total")

        output_tokens_total = d.pop("output_tokens_total")

        reviewed_total = d.pop("reviewed_total")

        review_input_tokens_total = d.pop("review_input_tokens_total")

        review_output_tokens_total = d.pop("review_output_tokens_total")

        def _parse_avg_llm_resolution_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        avg_llm_resolution_score = _parse_avg_llm_resolution_score(d.pop("avg_llm_resolution_score", UNSET))

        _llm_intent_distribution = d.pop("llm_intent_distribution", UNSET)
        llm_intent_distribution: Union[Unset, AnonymousChatKpiResponseLlmIntentDistribution]
        if isinstance(_llm_intent_distribution, Unset):
            llm_intent_distribution = UNSET
        else:
            llm_intent_distribution = AnonymousChatKpiResponseLlmIntentDistribution.from_dict(_llm_intent_distribution)

        def _parse_hallucination_rate(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        hallucination_rate = _parse_hallucination_rate(d.pop("hallucination_rate", UNSET))

        def _parse_review_coverage(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        review_coverage = _parse_review_coverage(d.pop("review_coverage", UNSET))

        daily_volume = []
        _daily_volume = d.pop("daily_volume", UNSET)
        for daily_volume_item_data in _daily_volume or []:
            daily_volume_item = DailyVolume.from_dict(daily_volume_item_data)

            daily_volume.append(daily_volume_item)

        _severity_by_day = d.pop("severity_by_day", UNSET)
        severity_by_day: Union[Unset, SeverityByDay]
        if isinstance(_severity_by_day, Unset):
            severity_by_day = UNSET
        else:
            severity_by_day = SeverityByDay.from_dict(_severity_by_day)

        anonymous_chat_kpi_response = cls(
            interactions_total=interactions_total,
            sessions_total=sessions_total,
            unique_users=unique_users,
            flagged_total=flagged_total,
            feedback_positive=feedback_positive,
            feedback_negative=feedback_negative,
            satisfaction_rate=satisfaction_rate,
            clicks_total=clicks_total,
            click_through_rate=click_through_rate,
            input_tokens_total=input_tokens_total,
            output_tokens_total=output_tokens_total,
            reviewed_total=reviewed_total,
            review_input_tokens_total=review_input_tokens_total,
            review_output_tokens_total=review_output_tokens_total,
            avg_llm_resolution_score=avg_llm_resolution_score,
            llm_intent_distribution=llm_intent_distribution,
            hallucination_rate=hallucination_rate,
            review_coverage=review_coverage,
            daily_volume=daily_volume,
            severity_by_day=severity_by_day,
        )

        anonymous_chat_kpi_response.additional_properties = d
        return anonymous_chat_kpi_response

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
