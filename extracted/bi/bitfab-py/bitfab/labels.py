from __future__ import annotations

from typing import Any, Literal, TypedDict
from urllib.parse import quote, urlencode

from typing_extensions import NotRequired

from bitfab.approval import Justification
from bitfab.experiment_id import resolve_experiment_id
from bitfab.http import HttpClient
from bitfab.traces import (
    AssertionLabelEvidence,
    parse_assertion_evidence_response,
)

LabelConfidence = Literal["VeryLow", "Low", "Medium", "High", "VeryHigh"]
LabelAction = Literal["set", "archived", "no-active-label", "skipped"]
LabelStatus = Literal["labeled", "skipped", "unlabeled"]
LabelSource = Literal["human", "agent"]


class _EvidenceUnset:
    pass


_EVIDENCE_UNSET = _EvidenceUnset()

LABELS_PATH = "/api/sdk/traces/labels"
HUMAN_LABELS_PATH = "/api/sdk/traces/labels/human"


class LabelUpdate(TypedDict):
    traceId: NotRequired[str]
    originalTraceId: NotRequired[str]
    attempt: NotRequired[int]
    assertionId: NotRequired[str]
    label: NotRequired[bool]
    annotation: NotRequired[str]
    confidence: NotRequired[LabelConfidence]
    evidence: NotRequired[Justification | None]
    skip: NotRequired[bool]
    archive: NotRequired[bool]


class LabelOutcome(TypedDict):
    key: str
    traceId: str
    action: LabelAction


class HumanLabelUpdate(TypedDict):
    traceId: str
    assertionId: str
    label: bool
    annotation: str
    confidence: NotRequired[LabelConfidence]
    evidence: NotRequired[Justification | None]


class HumanLabelOutcome(TypedDict):
    traceId: str
    assertionId: str | None
    label: bool
    action: Literal["set"]


class AssertionVerdict(TypedDict):
    assertionId: str
    assertion: str | None
    labelStatus: LabelStatus
    label: bool | None
    annotation: str | None
    evidence: Justification | None
    confidence: LabelConfidence | None
    labelSource: LabelSource
    approved: bool


class TraceLabels(TypedDict):
    traceId: str
    labelStatus: LabelStatus
    label: bool | None
    annotation: str | None
    evidence: Justification | None
    approved: bool
    passed: int
    failed: int
    assertions: list[AssertionVerdict]


class LabelsClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def save(
        self,
        label: bool,
        annotation: str,
        trace_id: str | None = None,
        original_trace_id: str | None = None,
        attempt: int | None = None,
        confidence: LabelConfidence | None = None,
        test_run_id: str | None = None,
        assertion_id: str | None = None,
        evidence: Justification | None | _EvidenceUnset = _EVIDENCE_UNSET,
        experiment_id: str | None = None,
    ) -> LabelOutcome:
        """Save one verdict. ``test_run_id`` is a deprecated alias for ``experiment_id``."""
        update: LabelUpdate = {"label": label, "annotation": annotation}
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        if confidence is not None:
            update["confidence"] = confidence
        if not isinstance(evidence, _EvidenceUnset):
            update["evidence"] = evidence
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="labels.save"
            ),
        )[0]

    def save_all(
        self,
        labels: list[LabelUpdate],
        test_run_id: str | None = None,
        experiment_id: str | None = None,
    ) -> list[LabelOutcome]:
        """Save several verdicts. ``test_run_id`` is a deprecated alias for ``experiment_id``."""
        resolved_experiment_id = resolve_experiment_id(
            experiment_id, test_run_id, where="labels.save_all"
        )
        _require_assertion_ids(labels)
        payload: dict[str, Any] = {"labels": labels}
        if resolved_experiment_id is not None:
            payload["experimentId"] = resolved_experiment_id
            payload["testRunId"] = resolved_experiment_id
        result = self._http_client.request(LABELS_PATH, payload)
        return result["labels"]

    def skip(
        self,
        trace_id: str | None = None,
        original_trace_id: str | None = None,
        attempt: int | None = None,
        test_run_id: str | None = None,
        assertion_id: str | None = None,
        experiment_id: str | None = None,
        annotation: str | None = None,
    ) -> LabelOutcome:
        """Skip one verdict. ``test_run_id`` is a deprecated alias for ``experiment_id``."""
        update: LabelUpdate = {"skip": True}
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        if annotation is not None:
            update["annotation"] = annotation
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="labels.skip"
            ),
        )[0]

    def archive(
        self,
        trace_id: str | None = None,
        original_trace_id: str | None = None,
        attempt: int | None = None,
        test_run_id: str | None = None,
        assertion_id: str | None = None,
        experiment_id: str | None = None,
    ) -> LabelOutcome:
        """Archive one verdict. ``test_run_id`` is a deprecated alias for ``experiment_id``."""
        update: LabelUpdate = {"archive": True}
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="labels.archive"
            ),
        )[0]

    def save_human(
        self,
        label: bool,
        annotation: str,
        trace_id: str,
        confidence: LabelConfidence | None = None,
        assertion_id: str | None = None,
        evidence: Justification | None | _EvidenceUnset = _EVIDENCE_UNSET,
    ) -> HumanLabelOutcome:
        update: HumanLabelUpdate = {
            "traceId": trace_id,
            "assertionId": assertion_id or "",
            "label": label,
            "annotation": annotation,
        }
        if confidence is not None:
            update["confidence"] = confidence
        if not isinstance(evidence, _EvidenceUnset):
            update["evidence"] = evidence
        return self.save_human_all([update])[0]

    def save_human_all(self, labels: list[HumanLabelUpdate]) -> list[HumanLabelOutcome]:
        _require_human_assertion_ids(labels)
        result = self._http_client.request(HUMAN_LABELS_PATH, {"labels": labels})
        return result["labels"]

    def get(self, trace_id: str) -> TraceLabels | None:
        found = self.get_all([trace_id])
        return found[0] if found else None

    def get_all(self, trace_ids: list[str]) -> list[TraceLabels]:
        if not trace_ids:
            return []
        query = urlencode({"traceIds": ",".join(trace_ids)})
        result = self._http_client.get(f"{LABELS_PATH}?{query}")
        return result["labels"]

    def generate_label_evidence(
        self, trace_id: str, assertion_id: str
    ) -> list[AssertionLabelEvidence]:
        """Generate suggested evidence from an original or replay trace."""
        encoded_trace_id = quote(trace_id, safe="")
        encoded_assertion_id = quote(assertion_id, safe="")
        result = self._http_client.get(
            f"/api/sdk/traces/{encoded_trace_id}/assertions/"
            f"{encoded_assertion_id}/evidence"
        )
        return parse_assertion_evidence_response(result, trace_id, assertion_id)


def _require_assertion_ids(labels: list[LabelUpdate]) -> None:
    unscoped = [
        entry.get("traceId") or entry.get("originalTraceId")
        for entry in labels
        if entry.get("archive") is not True and not entry.get("assertionId")
    ]
    if unscoped:
        raise ValueError(
            f"Agent verdicts must name an assertion: {', '.join(map(str, unscoped))}. "
            "Pass the assertion_id of the assertion each verdict scores to "
            "labels.save, save_all, and skip. Only archive may omit it, to clear an "
            "old whole-trace verdict."
        )


def _require_human_assertion_ids(labels: list[HumanLabelUpdate]) -> None:
    unscoped = [
        entry.get("traceId") for entry in labels if not entry.get("assertionId")
    ]
    if unscoped:
        raise ValueError(
            f"Human verdicts must name an assertion: {', '.join(map(str, unscoped))}. "
            "Pass the assertion_id of the assertion each verdict scores to "
            "labels.save_human and save_human_all."
        )


def _apply_target(
    update: LabelUpdate,
    trace_id: str | None,
    original_trace_id: str | None,
    attempt: int | None,
    assertion_id: str | None = None,
) -> None:
    if (trace_id is None) == (original_trace_id is None):
        raise ValueError(
            "Pass exactly one of trace_id or original_trace_id. "
            "Use original_trace_id for a replay verdict, with the experiment_id it ran under."
        )
    if assertion_id is not None:
        update["assertionId"] = assertion_id
    if trace_id is not None:
        update["traceId"] = trace_id
        return
    update["originalTraceId"] = original_trace_id  # type: ignore[typeddict-item]
    if attempt is not None:
        update["attempt"] = attempt
