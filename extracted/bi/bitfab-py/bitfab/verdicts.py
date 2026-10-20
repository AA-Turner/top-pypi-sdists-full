"""Write and read the verdicts a judge records on a trace's assertions."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, TypedDict, Union, cast
from urllib.parse import quote, urlencode

from typing_extensions import NotRequired

from bitfab.approval import Justification
from bitfab.experiment_id import resolve_experiment_id
from bitfab.http import HttpClient
from bitfab.traces import (
    AssertionVerdictEvidence,
    parse_assertion_evidence_response,
)
from bitfab.warn_once import warn_once

VerdictConfidence = Literal["VeryLow", "Low", "Medium", "High", "VeryHigh"]
VerdictAction = Literal["set", "archived", "no-active-verdict", "skipped", "abstained"]
VerdictStatus = Literal["judged", "skipped", "not-judged"]
VerdictSource = Literal["human", "agent"]
Verdict = Literal["pass", "fail", "abstained"]

LabelStatus = Literal["labeled", "skipped", "unlabeled"]


class _EvidenceUnset:
    pass


_EVIDENCE_UNSET = _EvidenceUnset()

VERDICTS_PATH = "/api/sdk/traces/verdicts"
HUMAN_VERDICTS_PATH = "/api/sdk/traces/verdicts/human"


class VerdictUpdate(TypedDict):
    """One agent verdict, skip, or archive for ``verdicts.save_all``.

    Name the trace with ``traceId``, or with ``originalTraceId`` plus ``attempt`` for a replay.
    Set ``verdict`` to record a judgement, ``skip`` to withhold one, or ``archive`` to clear one.
    ``annotation`` is required for a pass or fail and optional for an abstention.
    """

    traceId: NotRequired[str]
    originalTraceId: NotRequired[str]
    attempt: NotRequired[int]
    assertionId: NotRequired[str]
    verdict: NotRequired[Verdict]
    annotation: NotRequired[str]
    confidence: NotRequired[VerdictConfidence]
    evidence: NotRequired[Justification | None]
    skip: NotRequired[bool]
    archive: NotRequired[bool]


class LabelUpdate(TypedDict):
    """Deprecated. The old ``VerdictUpdate`` shape, with ``label`` and ``abstain`` in place of ``verdict``.

    Still accepted by ``verdicts.save_all`` for one minor and sent as ``verdict``.
    """

    traceId: NotRequired[str]
    originalTraceId: NotRequired[str]
    attempt: NotRequired[int]
    assertionId: NotRequired[str]
    label: NotRequired[bool]
    annotation: NotRequired[str]
    confidence: NotRequired[VerdictConfidence]
    evidence: NotRequired[Justification | None]
    skip: NotRequired[bool]
    abstain: NotRequired[bool]
    archive: NotRequired[bool]


class VerdictOutcome(TypedDict):
    key: str
    traceId: str
    action: VerdictAction


class HumanVerdictUpdate(TypedDict):
    """One verdict recorded as written by a person. A person never abstains, so ``verdict`` is pass or fail."""

    traceId: str
    assertionId: str
    verdict: Literal["pass", "fail"]
    annotation: str
    confidence: NotRequired[VerdictConfidence]
    evidence: NotRequired[Justification | None]


class HumanLabelUpdate(TypedDict):
    """Deprecated. The old ``HumanVerdictUpdate`` shape, with ``label`` in place of ``verdict``."""

    traceId: str
    assertionId: str
    label: bool
    annotation: str
    confidence: NotRequired[VerdictConfidence]
    evidence: NotRequired[Justification | None]


class HumanVerdictOutcome(TypedDict):
    """A saved human verdict. ``label`` is deprecated: read ``verdict``."""

    traceId: str
    assertionId: str | None
    verdict: Literal["pass", "fail"]
    action: Literal["set"]
    label: NotRequired[bool]


class AssertionVerdict(TypedDict):
    """One assertion's verdict on a trace.

    ``verdictStatus`` says whether it was judged, skipped, or not judged yet, and ``source`` who judged it.
    ``labelStatus``, ``label``, and ``labelSource`` are deprecated: read ``verdictStatus``, ``verdict``, and ``source``.
    """

    assertionId: str
    assertion: str | None
    verdict: Verdict | None
    verdictStatus: VerdictStatus
    annotation: str | None
    evidence: Justification | None
    confidence: VerdictConfidence | None
    source: VerdictSource
    approved: bool
    labelStatus: NotRequired[LabelStatus]
    label: NotRequired[bool | None]
    labelSource: NotRequired[VerdictSource]


class TraceVerdicts(TypedDict):
    """A trace's effective verdict plus one row per scored assertion.

    ``labelStatus`` and ``label`` are deprecated: read ``verdictStatus`` and ``verdict``.
    """

    traceId: str
    verdict: Verdict | None
    verdictStatus: VerdictStatus
    annotation: str | None
    evidence: Justification | None
    approved: bool
    passed: int
    failed: int
    abstained: int
    assertions: list[AssertionVerdict]
    labelStatus: NotRequired[LabelStatus]
    label: NotRequired[bool | None]


AgentVerdictInput = Union[VerdictUpdate, LabelUpdate]
HumanVerdictInput = Union[HumanVerdictUpdate, HumanLabelUpdate]


class VerdictsClient:
    """Write and read the pass, fail, and abstained verdicts on a trace's assertions."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def save(
        self,
        verdict: Verdict | None = None,
        annotation: str | None = None,
        trace_id: str | None = None,
        original_trace_id: str | None = None,
        attempt: int | None = None,
        confidence: VerdictConfidence | None = None,
        test_run_id: str | None = None,
        assertion_id: str | None = None,
        evidence: Justification | _EvidenceUnset | None = _EVIDENCE_UNSET,
        experiment_id: str | None = None,
        label: bool | None = None,
    ) -> VerdictOutcome:
        """Save one agent verdict on an assertion.

        ``verdict`` is ``"pass"``, ``"fail"``, or ``"abstained"``. ``annotation`` is required for a pass or fail.
        ``confidence`` and ``evidence`` belong to a pass or fail only, so passing either with ``"abstained"`` raises ``ValueError``.
        ``label`` is a deprecated boolean spelling of ``verdict`` and ``test_run_id`` a deprecated alias for ``experiment_id``.
        """
        resolved = _resolve_verdict(verdict, label, where="verdicts.save")
        _require_annotation(resolved, annotation, where="verdicts.save")
        _refuse_abstention_detail(
            resolved,
            confidence is not None,
            not isinstance(evidence, _EvidenceUnset),
            where="verdicts.save",
        )
        update: VerdictUpdate = {"verdict": resolved}
        if annotation is not None:
            update["annotation"] = annotation
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        if confidence is not None:
            update["confidence"] = confidence
        if not isinstance(evidence, _EvidenceUnset):
            update["evidence"] = evidence
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="verdicts.save"
            ),
        )[0]

    def save_all(
        self,
        verdicts: Sequence[AgentVerdictInput] | None = None,
        test_run_id: str | None = None,
        experiment_id: str | None = None,
        labels: Sequence[AgentVerdictInput] | None = None,
    ) -> list[VerdictOutcome]:
        """Save several agent verdicts, skips, and archives in one all-or-nothing call.

        ``labels`` is a deprecated alias for ``verdicts``, and entries still carrying ``label`` or ``abstain`` are sent as ``verdict``.
        ``test_run_id`` is a deprecated alias for ``experiment_id``.
        """
        entries = resolve_legacy_entries(verdicts, labels, where="verdicts.save_all")
        resolved_experiment_id = resolve_experiment_id(
            experiment_id, test_run_id, where="verdicts.save_all"
        )
        normalized = [_normalize_agent_entry(entry) for entry in entries]
        _require_assertion_ids(normalized)
        payload: dict[str, Any] = {"verdicts": normalized}
        if resolved_experiment_id is not None:
            payload["experimentId"] = resolved_experiment_id
            payload["testRunId"] = resolved_experiment_id
        result = self._http_client.request(VERDICTS_PATH, payload)
        return result["verdicts"]

    def skip(
        self,
        trace_id: str | None = None,
        original_trace_id: str | None = None,
        attempt: int | None = None,
        test_run_id: str | None = None,
        assertion_id: str | None = None,
        experiment_id: str | None = None,
        annotation: str | None = None,
    ) -> VerdictOutcome:
        """Withhold one verdict. ``test_run_id`` is a deprecated alias for ``experiment_id``."""
        update: VerdictUpdate = {"skip": True}
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        if annotation is not None:
            update["annotation"] = annotation
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="verdicts.skip"
            ),
        )[0]

    def abstain(
        self,
        trace_id: str | None = None,
        original_trace_id: str | None = None,
        attempt: int | None = None,
        test_run_id: str | None = None,
        assertion_id: str | None = None,
        experiment_id: str | None = None,
        annotation: str | None = None,
    ) -> VerdictOutcome:
        """Record that the evidence does not show the part of the run this assertion checks, so there was nothing to judge.

        The one-call shorthand for ``save(verdict="abstained")``. Counted as a fail in every pass rate, but stored and read back as an abstention, apart from a fail.
        ``annotation`` says what the evidence would have had to show. ``test_run_id`` is a deprecated alias for ``experiment_id``.
        """
        update: VerdictUpdate = {"verdict": "abstained"}
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        if annotation is not None:
            update["annotation"] = annotation
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="verdicts.abstain"
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
    ) -> VerdictOutcome:
        """Archive one verdict. ``test_run_id`` is a deprecated alias for ``experiment_id``."""
        update: VerdictUpdate = {"archive": True}
        _apply_target(update, trace_id, original_trace_id, attempt, assertion_id)
        return self.save_all(
            [update],
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="verdicts.archive"
            ),
        )[0]

    def save_human(
        self,
        verdict: Literal["pass", "fail"] | None = None,
        annotation: str | None = None,
        trace_id: str | None = None,
        confidence: VerdictConfidence | None = None,
        assertion_id: str | None = None,
        evidence: Justification | _EvidenceUnset | None = _EVIDENCE_UNSET,
        label: bool | None = None,
    ) -> HumanVerdictOutcome:
        """Save one verdict recorded as written by a person. ``verdict`` is ``"pass"`` or ``"fail"``.

        ``label`` is a deprecated boolean spelling of ``verdict``.
        """
        resolved = _resolve_verdict(verdict, label, where="verdicts.save_human")
        if resolved == "abstained":
            raise ValueError(
                "verdicts.save_human takes a pass or fail verdict: a person never abstains."
            )
        _require_annotation(resolved, annotation, where="verdicts.save_human")
        if trace_id is None:
            raise ValueError("verdicts.save_human needs the trace_id it judges.")
        update: HumanVerdictUpdate = {
            "traceId": trace_id,
            "assertionId": assertion_id or "",
            "verdict": resolved,
            "annotation": cast(str, annotation),
        }
        if confidence is not None:
            update["confidence"] = confidence
        if not isinstance(evidence, _EvidenceUnset):
            update["evidence"] = evidence
        return self.save_human_all([update])[0]

    def save_human_all(
        self,
        verdicts: Sequence[HumanVerdictInput] | None = None,
        labels: Sequence[HumanVerdictInput] | None = None,
    ) -> list[HumanVerdictOutcome]:
        """Save several verdicts recorded as written by a person, all or nothing.

        ``labels`` is a deprecated alias for ``verdicts``, and entries still carrying ``label`` are sent as ``verdict``.
        """
        entries = resolve_legacy_entries(
            verdicts, labels, where="verdicts.save_human_all"
        )
        normalized = [_normalize_human_entry(entry) for entry in entries]
        _require_human_assertion_ids(normalized)
        result = self._http_client.request(
            HUMAN_VERDICTS_PATH, {"verdicts": normalized}
        )
        return [with_legacy_label(outcome) for outcome in result["verdicts"]]

    def get(self, trace_id: str) -> TraceVerdicts | None:
        """Read one trace's effective verdict and its per-assertion verdicts, or ``None`` when it has none."""
        found = self.get_all([trace_id])
        return found[0] if found else None

    def get_all(self, trace_ids: list[str]) -> list[TraceVerdicts]:
        """Read several traces' verdicts in one call."""
        if not trace_ids:
            return []
        query = urlencode({"traceIds": ",".join(trace_ids)})
        result = self._http_client.get(f"{VERDICTS_PATH}?{query}")
        return result["verdicts"]

    def generate_evidence(
        self, trace_id: str, assertion_id: str
    ) -> list[AssertionVerdictEvidence]:
        """Generate suggested verdict evidence from an original or replay trace."""
        encoded_trace_id = quote(trace_id, safe="")
        encoded_assertion_id = quote(assertion_id, safe="")
        result = self._http_client.get(
            f"/api/sdk/traces/{encoded_trace_id}/assertions/"
            f"{encoded_assertion_id}/evidence"
        )
        return parse_assertion_evidence_response(result, trace_id, assertion_id)

    def generate_label_evidence(
        self, trace_id: str, assertion_id: str
    ) -> list[AssertionVerdictEvidence]:
        """Deprecated alias for ``generate_evidence``."""
        warn_once(
            "deprecated-generate-label-evidence",
            "verdicts.generate_label_evidence is deprecated; use verdicts.generate_evidence instead.",
        )
        return self.generate_evidence(trace_id, assertion_id)


def with_legacy_label(outcome: Mapping[str, Any]) -> Any:
    """Copy a pass or fail ``verdict`` onto the deprecated ``label`` boolean so code reading ``label`` keeps working."""
    row = dict(outcome)
    if "label" not in row and row.get("verdict") in ("pass", "fail"):
        row["label"] = row["verdict"] == "pass"
    return row


def resolve_legacy_label(
    verdict: Any, label: bool | None, *, where: str
) -> Verdict | None:
    """Map the deprecated ``label`` boolean, or a boolean passed where ``verdict`` goes, onto ``verdict``."""
    if isinstance(verdict, bool):
        if label is not None:
            raise ValueError(
                f"{where}: pass verdict or the deprecated label, not both."
            )
        label, verdict = verdict, None
    if label is None:
        return cast("Verdict | None", verdict)
    if verdict is not None:
        raise ValueError(f"{where}: pass verdict or the deprecated label, not both.")
    warn_once(
        f"deprecated-label-argument:{where}",
        f'{where}(label=...) is deprecated; pass verdict="pass" or verdict="fail" instead.',
    )
    return "pass" if label else "fail"


def _resolve_verdict(verdict: Any, label: bool | None, *, where: str) -> Verdict:
    resolved = resolve_legacy_label(verdict, label, where=where)
    if resolved is None:
        raise ValueError(f'{where} needs a verdict: "pass", "fail", or "abstained".')
    if resolved not in ("pass", "fail", "abstained"):
        raise ValueError(
            f'{where}: verdict must be "pass", "fail", or "abstained", not {resolved!r}.'
        )
    return resolved


def _require_annotation(verdict: Any, annotation: Any, *, where: str) -> None:
    """Refuse a pass or fail whose annotation is missing, empty, or only whitespace."""
    if verdict not in ("pass", "fail"):
        return
    if not isinstance(annotation, str) or not annotation.strip():
        raise ValueError(
            f"{where} needs an annotation saying why the assertion {verdict}ed."
        )


def _refuse_abstention_detail(
    verdict: Any, has_confidence: bool, has_evidence: bool, *, where: str
) -> None:
    """Refuse confidence or evidence on an abstention, which the server accepts only on a pass or fail."""
    if verdict != "abstained":
        return
    sent = [
        name
        for name, present in (
            ("confidence", has_confidence),
            ("evidence", has_evidence),
        )
        if present
    ]
    if sent:
        raise ValueError(
            f"{where}: {' and '.join(sent)} can only go with a pass or fail verdict, "
            'not "abstained". Drop it, or pass verdict="pass" or "fail".'
        )


def resolve_legacy_entries(
    verdicts: Sequence[Any] | None, labels: Sequence[Any] | None, *, where: str
) -> list[Any]:
    """Accept the deprecated ``labels`` batch argument in place of ``verdicts``."""
    if labels is not None:
        if verdicts is not None:
            raise ValueError(
                f"{where}: pass verdicts or the deprecated labels, not both."
            )
        warn_once(
            f"deprecated-labels-argument:{where}",
            f"{where}(labels=...) is deprecated; pass verdicts=... instead.",
        )
        return list(labels)
    return list(verdicts or [])


def legacy_entry_verdict(entry: Mapping[str, Any], *, where: str) -> dict[str, Any]:
    """Rewrite an entry's deprecated ``label`` boolean as ``verdict``, refusing an entry that carries both."""
    row = dict(entry)
    if "label" not in row:
        return row
    if "verdict" in row:
        raise ValueError(
            f"{where}: an entry carries both label and verdict. Pass only verdict."
        )
    warn_once(
        f"deprecated-label-entry:{where}",
        f'{where}: the "label" entry field is deprecated; set "verdict" to "pass" or "fail" instead.',
    )
    row["verdict"] = "pass" if row.pop("label") else "fail"
    return row


def _normalize_agent_entry(entry: Mapping[str, Any]) -> VerdictUpdate:
    row = legacy_entry_verdict(entry, where="verdicts.save_all")
    if "abstain" in row:
        abstain = row.pop("abstain")
        if abstain is True:
            if "verdict" in row:
                raise ValueError(
                    "verdicts.save_all: an entry carries both abstain and a verdict. "
                    'Pass only verdict="abstained".'
                )
            warn_once(
                "deprecated-abstain-entry",
                'verdicts.save_all: the "abstain" entry field is deprecated; set "verdict" to "abstained" instead.',
            )
            row["verdict"] = "abstained"
        elif "verdict" not in row and not _is_skip_or_archive(row):
            raise ValueError(
                "verdicts.save_all: an entry carries abstain: False and no verdict. "
                'Set "verdict" to "pass", "fail", or "abstained" instead.'
            )
    if not _is_skip_or_archive(row):
        _require_annotation(
            row.get("verdict"), row.get("annotation"), where="verdicts.save_all"
        )
        _refuse_abstention_detail(
            row.get("verdict"),
            "confidence" in row,
            "evidence" in row,
            where="verdicts.save_all",
        )
    return cast(VerdictUpdate, row)


def _is_skip_or_archive(row: Mapping[str, Any]) -> bool:
    """Whether an entry withholds or clears a verdict rather than writing one."""
    return row.get("skip") is True or row.get("archive") is True


def _normalize_human_entry(entry: Mapping[str, Any]) -> HumanVerdictUpdate:
    return cast(
        HumanVerdictUpdate, legacy_entry_verdict(entry, where="verdicts.save_human_all")
    )


def _require_assertion_ids(verdicts: Sequence[Mapping[str, Any]]) -> None:
    unscoped = [
        entry.get("traceId") or entry.get("originalTraceId")
        for entry in verdicts
        if entry.get("archive") is not True and not entry.get("assertionId")
    ]
    if unscoped:
        raise ValueError(
            f"Agent verdicts must name an assertion: {', '.join(map(str, unscoped))}. "
            "Pass the assertion_id of the assertion each verdict scores to "
            "verdicts.save, save_all, skip, and abstain. Only archive may omit it, to "
            "clear an old whole-trace verdict."
        )


def _require_human_assertion_ids(verdicts: Sequence[Mapping[str, Any]]) -> None:
    unscoped = [
        entry.get("traceId") for entry in verdicts if not entry.get("assertionId")
    ]
    if unscoped:
        raise ValueError(
            f"Human verdicts must name an assertion: {', '.join(map(str, unscoped))}. "
            "Pass the assertion_id of the assertion each verdict scores to "
            "verdicts.save_human and save_human_all."
        )


def _apply_target(
    update: VerdictUpdate,
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
