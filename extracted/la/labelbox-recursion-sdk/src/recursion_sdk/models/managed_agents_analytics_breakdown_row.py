from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsAnalyticsBreakdownRow")



@_attrs_define
class ManagedAgentsAnalyticsBreakdownRow:
    """ Aggregated analytics measures for one window, group, or time bucket. Counters and sums are exact; p50_ms, p90_ms and
    p95_ms are approximate, derived from a fixed-bin histogram so they can be merged across shards, buckets, and scopes.

        Example:
            {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'criterion_count': 1, 'criterion_fail_count': 1,
                'criterion_not_applicable_count': 1, 'criterion_pass_count': 1, 'criterion_pass_rate': 1.5, 'duration_samples':
                1, 'environment_failed': 1, 'environment_ready': 1, 'environment_starts': 1, 'environment_startup_ms': 1,
                'evaluation_count': 1, 'evaluation_fail_count': 1, 'evaluation_not_applicable_count': 1,
                'evaluation_pass_count': 1, 'evaluation_pass_rate': 1.5, 'event_count': 1, 'input_tokens': 1, 'label':
                'example', 'model_calls': 1, 'model_cost_micros': 1, 'output_tokens': 1, 'p50_ms': 1.5, 'p90_ms': 1.5, 'p95_ms':
                1.5, 'session_completion_ms': 1, 'sessions': 1, 'tool_calls': 1, 'tool_completed': 1, 'tool_cost_micros': 1,
                'tool_duration_ms': 1, 'tool_failed': 1, 'tool_in_flight': 1, 'total_cost_micros': 1, 'turns': 1, 'value':
                'example'}

        Attributes:
            cache_read_tokens (int): Prompt tokens served from the provider's cache.
            cache_write_tokens (int): Prompt tokens written into the provider's cache.
            duration_samples (int): How many measurements the percentiles below were derived from. Compare with tool_calls
                or environment_starts to see the coverage.
            environment_failed (int): Environment startups that failed or were cancelled before the sandbox ran.
            environment_ready (int): Environment startups that reached a running sandbox.
            environment_starts (int): Sandbox environment startups observed, including those still in progress.
            environment_startup_ms (int): Summed time from the first provisioning transition to the first running
                transition, in milliseconds, over successful startups only.
            event_count (int): Units of work recorded: every tool call, model call, and environment startup.
            input_tokens (int): Prompt tokens billed in the window.
            model_calls (int): Distinct model inference calls. A response persisted across several events is charged once.
            model_cost_micros (int): Model spend in micro-USD (1,000,000 = 1 USD).
            output_tokens (int): Completion tokens billed in the window.
            sessions (int): For managed_agent_completion: root sessions with a first recorded successful completion in the
                window, bucketed by completion time. For other families: sessions counted once in the bucket they started in.
            tool_calls (int): Tool invocations in the window. A call is counted once, in the bucket it started in, whether
                or not it has finished.
            tool_completed (int): Tool calls whose result reported success.
            tool_cost_micros (int): Directly attributable tool spend in micro-USD, such as a metered built-in tool.
            tool_duration_ms (int): Summed measured duration of every tool call that reported one, in milliseconds. Model
                thinking time is not included.
            tool_failed (int): Tool calls whose result reported an error, plus invocations that failed before any result was
                recorded.
            tool_in_flight (int): Tool calls with no result yet. A call that never receives one stays here permanently.
            total_cost_micros (int): model_cost_micros plus tool_cost_micros.
            turns (int): Model turns, counted once each from the runtime's own turn grouping. Only the managed_agent_turn
                family records these; divided by sessions it is turns per session.
            value (str): The dimension's value for this group, and the value to pass back as a filter. Empty means the
                dimension was not recorded on the underlying work.
            criterion_count (int | Unset): Immutable criterion verdict facts in the quality family.
            criterion_fail_count (int | Unset): Quality criterion verdicts that are fail.
            criterion_not_applicable_count (int | Unset): Quality criterion verdicts that are not applicable.
            criterion_pass_count (int | Unset): Quality criterion verdicts that are pass.
            criterion_pass_rate (float | None | Unset): Passed criteria divided by passed plus failed criteria. Null when
                that denominator is zero.
            evaluation_count (int | Unset): Immutable evaluation snapshots in the quality family.
            evaluation_fail_count (int | Unset): Quality evaluations whose parent verdict is fail.
            evaluation_not_applicable_count (int | Unset): Quality evaluations whose parent verdict is not applicable.
            evaluation_pass_count (int | Unset): Quality evaluations whose parent verdict is pass.
            evaluation_pass_rate (float | None | Unset): Passed evaluations divided by passed plus failed evaluations. Null
                when that denominator is zero.
            label (str | Unset): Human-readable name for value, resolved when the request is served. Present for identifier
                dimensions (agent, agent version, environment); absent for dimensions that are already readable, and for an
                identifier whose subject has since been deleted.
            p50_ms (float | Unset): Approximate median duration in milliseconds, interpolated within a fixed histogram
                bucket. Absent when nothing in the window reported a duration.
            p90_ms (float | Unset): Approximate 90th percentile duration in milliseconds, interpolated within a fixed
                histogram bucket. Absent when nothing in the window reported a duration.
            p95_ms (float | Unset): Approximate 95th percentile duration in milliseconds, interpolated within a fixed
                histogram bucket. Absent when nothing in the window reported a duration.
            session_completion_ms (int | Unset): Sum of creation-to-first-recorded-successful-completion durations in
                milliseconds. Divide by sessions for the mean in the completion family. Earlier sessions without a recorded
                completion milestone are excluded.
     """

    cache_read_tokens: int
    cache_write_tokens: int
    duration_samples: int
    environment_failed: int
    environment_ready: int
    environment_starts: int
    environment_startup_ms: int
    event_count: int
    input_tokens: int
    model_calls: int
    model_cost_micros: int
    output_tokens: int
    sessions: int
    tool_calls: int
    tool_completed: int
    tool_cost_micros: int
    tool_duration_ms: int
    tool_failed: int
    tool_in_flight: int
    total_cost_micros: int
    turns: int
    value: str
    criterion_count: int | Unset = UNSET
    criterion_fail_count: int | Unset = UNSET
    criterion_not_applicable_count: int | Unset = UNSET
    criterion_pass_count: int | Unset = UNSET
    criterion_pass_rate: float | None | Unset = UNSET
    evaluation_count: int | Unset = UNSET
    evaluation_fail_count: int | Unset = UNSET
    evaluation_not_applicable_count: int | Unset = UNSET
    evaluation_pass_count: int | Unset = UNSET
    evaluation_pass_rate: float | None | Unset = UNSET
    label: str | Unset = UNSET
    p50_ms: float | Unset = UNSET
    p90_ms: float | Unset = UNSET
    p95_ms: float | Unset = UNSET
    session_completion_ms: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        duration_samples = self.duration_samples

        environment_failed = self.environment_failed

        environment_ready = self.environment_ready

        environment_starts = self.environment_starts

        environment_startup_ms = self.environment_startup_ms

        event_count = self.event_count

        input_tokens = self.input_tokens

        model_calls = self.model_calls

        model_cost_micros = self.model_cost_micros

        output_tokens = self.output_tokens

        sessions = self.sessions

        tool_calls = self.tool_calls

        tool_completed = self.tool_completed

        tool_cost_micros = self.tool_cost_micros

        tool_duration_ms = self.tool_duration_ms

        tool_failed = self.tool_failed

        tool_in_flight = self.tool_in_flight

        total_cost_micros = self.total_cost_micros

        turns = self.turns

        value = self.value

        criterion_count = self.criterion_count

        criterion_fail_count = self.criterion_fail_count

        criterion_not_applicable_count = self.criterion_not_applicable_count

        criterion_pass_count = self.criterion_pass_count

        criterion_pass_rate: float | None | Unset
        if isinstance(self.criterion_pass_rate, Unset):
            criterion_pass_rate = UNSET
        else:
            criterion_pass_rate = self.criterion_pass_rate

        evaluation_count = self.evaluation_count

        evaluation_fail_count = self.evaluation_fail_count

        evaluation_not_applicable_count = self.evaluation_not_applicable_count

        evaluation_pass_count = self.evaluation_pass_count

        evaluation_pass_rate: float | None | Unset
        if isinstance(self.evaluation_pass_rate, Unset):
            evaluation_pass_rate = UNSET
        else:
            evaluation_pass_rate = self.evaluation_pass_rate

        label = self.label

        p50_ms = self.p50_ms

        p90_ms = self.p90_ms

        p95_ms = self.p95_ms

        session_completion_ms = self.session_completion_ms


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cache_read_tokens": cache_read_tokens,
            "cache_write_tokens": cache_write_tokens,
            "duration_samples": duration_samples,
            "environment_failed": environment_failed,
            "environment_ready": environment_ready,
            "environment_starts": environment_starts,
            "environment_startup_ms": environment_startup_ms,
            "event_count": event_count,
            "input_tokens": input_tokens,
            "model_calls": model_calls,
            "model_cost_micros": model_cost_micros,
            "output_tokens": output_tokens,
            "sessions": sessions,
            "tool_calls": tool_calls,
            "tool_completed": tool_completed,
            "tool_cost_micros": tool_cost_micros,
            "tool_duration_ms": tool_duration_ms,
            "tool_failed": tool_failed,
            "tool_in_flight": tool_in_flight,
            "total_cost_micros": total_cost_micros,
            "turns": turns,
            "value": value,
        })
        if criterion_count is not UNSET:
            field_dict["criterion_count"] = criterion_count
        if criterion_fail_count is not UNSET:
            field_dict["criterion_fail_count"] = criterion_fail_count
        if criterion_not_applicable_count is not UNSET:
            field_dict["criterion_not_applicable_count"] = criterion_not_applicable_count
        if criterion_pass_count is not UNSET:
            field_dict["criterion_pass_count"] = criterion_pass_count
        if criterion_pass_rate is not UNSET:
            field_dict["criterion_pass_rate"] = criterion_pass_rate
        if evaluation_count is not UNSET:
            field_dict["evaluation_count"] = evaluation_count
        if evaluation_fail_count is not UNSET:
            field_dict["evaluation_fail_count"] = evaluation_fail_count
        if evaluation_not_applicable_count is not UNSET:
            field_dict["evaluation_not_applicable_count"] = evaluation_not_applicable_count
        if evaluation_pass_count is not UNSET:
            field_dict["evaluation_pass_count"] = evaluation_pass_count
        if evaluation_pass_rate is not UNSET:
            field_dict["evaluation_pass_rate"] = evaluation_pass_rate
        if label is not UNSET:
            field_dict["label"] = label
        if p50_ms is not UNSET:
            field_dict["p50_ms"] = p50_ms
        if p90_ms is not UNSET:
            field_dict["p90_ms"] = p90_ms
        if p95_ms is not UNSET:
            field_dict["p95_ms"] = p95_ms
        if session_completion_ms is not UNSET:
            field_dict["session_completion_ms"] = session_completion_ms

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_read_tokens = d.pop("cache_read_tokens")

        cache_write_tokens = d.pop("cache_write_tokens")

        duration_samples = d.pop("duration_samples")

        environment_failed = d.pop("environment_failed")

        environment_ready = d.pop("environment_ready")

        environment_starts = d.pop("environment_starts")

        environment_startup_ms = d.pop("environment_startup_ms")

        event_count = d.pop("event_count")

        input_tokens = d.pop("input_tokens")

        model_calls = d.pop("model_calls")

        model_cost_micros = d.pop("model_cost_micros")

        output_tokens = d.pop("output_tokens")

        sessions = d.pop("sessions")

        tool_calls = d.pop("tool_calls")

        tool_completed = d.pop("tool_completed")

        tool_cost_micros = d.pop("tool_cost_micros")

        tool_duration_ms = d.pop("tool_duration_ms")

        tool_failed = d.pop("tool_failed")

        tool_in_flight = d.pop("tool_in_flight")

        total_cost_micros = d.pop("total_cost_micros")

        turns = d.pop("turns")

        value = d.pop("value")

        criterion_count = d.pop("criterion_count", UNSET)

        criterion_fail_count = d.pop("criterion_fail_count", UNSET)

        criterion_not_applicable_count = d.pop("criterion_not_applicable_count", UNSET)

        criterion_pass_count = d.pop("criterion_pass_count", UNSET)

        def _parse_criterion_pass_rate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        criterion_pass_rate = _parse_criterion_pass_rate(d.pop("criterion_pass_rate", UNSET))


        evaluation_count = d.pop("evaluation_count", UNSET)

        evaluation_fail_count = d.pop("evaluation_fail_count", UNSET)

        evaluation_not_applicable_count = d.pop("evaluation_not_applicable_count", UNSET)

        evaluation_pass_count = d.pop("evaluation_pass_count", UNSET)

        def _parse_evaluation_pass_rate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        evaluation_pass_rate = _parse_evaluation_pass_rate(d.pop("evaluation_pass_rate", UNSET))


        label = d.pop("label", UNSET)

        p50_ms = d.pop("p50_ms", UNSET)

        p90_ms = d.pop("p90_ms", UNSET)

        p95_ms = d.pop("p95_ms", UNSET)

        session_completion_ms = d.pop("session_completion_ms", UNSET)

        managed_agents_analytics_breakdown_row = cls(
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            duration_samples=duration_samples,
            environment_failed=environment_failed,
            environment_ready=environment_ready,
            environment_starts=environment_starts,
            environment_startup_ms=environment_startup_ms,
            event_count=event_count,
            input_tokens=input_tokens,
            model_calls=model_calls,
            model_cost_micros=model_cost_micros,
            output_tokens=output_tokens,
            sessions=sessions,
            tool_calls=tool_calls,
            tool_completed=tool_completed,
            tool_cost_micros=tool_cost_micros,
            tool_duration_ms=tool_duration_ms,
            tool_failed=tool_failed,
            tool_in_flight=tool_in_flight,
            total_cost_micros=total_cost_micros,
            turns=turns,
            value=value,
            criterion_count=criterion_count,
            criterion_fail_count=criterion_fail_count,
            criterion_not_applicable_count=criterion_not_applicable_count,
            criterion_pass_count=criterion_pass_count,
            criterion_pass_rate=criterion_pass_rate,
            evaluation_count=evaluation_count,
            evaluation_fail_count=evaluation_fail_count,
            evaluation_not_applicable_count=evaluation_not_applicable_count,
            evaluation_pass_count=evaluation_pass_count,
            evaluation_pass_rate=evaluation_pass_rate,
            label=label,
            p50_ms=p50_ms,
            p90_ms=p90_ms,
            p95_ms=p95_ms,
            session_completion_ms=session_completion_ms,
        )


        managed_agents_analytics_breakdown_row.additional_properties = d
        return managed_agents_analytics_breakdown_row

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
