from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal, TypedDict, Union, cast
from urllib.parse import urlencode

from typing_extensions import NotRequired

from bitfab.http import HttpClient
from bitfab.verdicts import (
    VerdictConfidence,
    legacy_entry_verdict,
    resolve_legacy_entries,
    resolve_legacy_label,
    with_legacy_label,
)
from bitfab.warn_once import warn_once

GRADER_VERDICTS_PATH = "/api/sdk/graderVerdicts"
GRADER_LABELS_PATH = GRADER_VERDICTS_PATH

GraderStatus = Literal["active", "archived"]
GraderVerdictSource = Literal["human", "live_grader"]


class GraderVerdict(TypedDict):
    """One grader's verdict on one trace, ``None`` while the grader has not judged it.

    ``label``, ``labelReason``, and ``labelConfidence`` are deprecated: read ``verdict``, ``reason``, and ``confidence``.
    """

    traceId: str
    graderId: str
    graderName: str | None
    graderStatus: GraderStatus
    graderType: str
    verdict: Literal["pass", "fail"] | None
    reason: str | None
    failureDiagnostic: str | None
    confidence: VerdictConfidence | None
    source: GraderVerdictSource
    evaluatedAt: str | None
    label: NotRequired[bool | None]
    labelReason: NotRequired[str | None]
    labelConfidence: NotRequired[VerdictConfidence | None]


class GraderVerdictUpdate(TypedDict):
    """One external grader's verdict on one trace. ``verdict`` is ``"pass"`` or ``"fail"``."""

    graderId: str
    traceId: str
    verdict: Literal["pass", "fail"]
    reason: NotRequired[str]
    failureDiagnostic: NotRequired[str]
    confidence: NotRequired[VerdictConfidence]


class GraderLabelUpdate(TypedDict):
    """Deprecated. The old ``GraderVerdictUpdate`` shape, with ``label`` in place of ``verdict``."""

    graderId: str
    traceId: str
    label: bool
    reason: NotRequired[str]
    failureDiagnostic: NotRequired[str]
    confidence: NotRequired[VerdictConfidence]


class GraderVerdictOutcome(TypedDict):
    """A saved external grader verdict. ``label`` is deprecated: read ``verdict``."""

    graderId: str
    traceId: str
    verdict: Literal["pass", "fail"]
    action: Literal["set"]
    label: NotRequired[bool]


GraderVerdictInput = Union[GraderVerdictUpdate, GraderLabelUpdate]

GraderLabel = GraderVerdict
GraderLabelOutcome = GraderVerdictOutcome
GraderLabelSource = GraderVerdictSource


class GradersClient:
    """Read the verdicts each grader recorded, and post verdicts for external graders."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def get_verdicts(
        self,
        trace_ids: list[str] | None = None,
        grader_id: str | None = None,
        limit: int | None = None,
    ) -> list[GraderVerdict]:
        """Read grader verdicts by traces, by grader, or both."""
        if not trace_ids and grader_id is None:
            raise ValueError(
                "Pass trace_ids, grader_id, or both: there is nothing to read otherwise."
            )
        params: dict[str, str] = {}
        if trace_ids:
            params["traceIds"] = ",".join(trace_ids)
        if grader_id is not None:
            params["graderId"] = grader_id
        if limit is not None:
            params["limit"] = str(limit)
        result = self._http_client.get(f"{GRADER_VERDICTS_PATH}?{urlencode(params)}")
        return [_with_legacy_grader_fields(row) for row in result["verdicts"]]

    def save_verdict(
        self,
        grader_id: str,
        trace_id: str,
        verdict: Literal["pass", "fail"] | None = None,
        reason: str | None = None,
        failure_diagnostic: str | None = None,
        confidence: VerdictConfidence | None = None,
        label: bool | None = None,
    ) -> GraderVerdictOutcome:
        """Post one external grader's verdict. ``verdict`` is ``"pass"`` or ``"fail"``.

        ``label`` is a deprecated boolean spelling of ``verdict``.
        """
        resolved = resolve_legacy_label(verdict, label, where="graders.save_verdict")
        if resolved not in ("pass", "fail"):
            raise ValueError(
                f'graders.save_verdict: verdict must be "pass" or "fail", not {resolved!r}.'
            )
        update: GraderVerdictUpdate = {
            "graderId": grader_id,
            "traceId": trace_id,
            "verdict": resolved,
        }
        if reason is not None:
            update["reason"] = reason
        if failure_diagnostic is not None:
            update["failureDiagnostic"] = failure_diagnostic
        if confidence is not None:
            update["confidence"] = confidence
        return self.save_verdict_all([update])[0]

    def save_verdict_all(
        self,
        verdicts: Sequence[GraderVerdictInput] | None = None,
        labels: Sequence[GraderVerdictInput] | None = None,
    ) -> list[GraderVerdictOutcome]:
        """Post up to 200 external grader verdicts, all or nothing.

        ``labels`` is a deprecated alias for ``verdicts``, and entries still carrying ``label`` are sent as ``verdict``.
        """
        entries = resolve_legacy_entries(
            verdicts, labels, where="graders.save_verdict_all"
        )
        normalized = [
            legacy_entry_verdict(entry, where="graders.save_verdict_all")
            for entry in entries
        ]
        result = self._http_client.request(
            GRADER_VERDICTS_PATH, {"verdicts": normalized}
        )
        return [with_legacy_label(outcome) for outcome in result["verdicts"]]

    def get_labels(
        self,
        trace_ids: list[str] | None = None,
        grader_id: str | None = None,
        limit: int | None = None,
    ) -> list[GraderVerdict]:
        """Deprecated alias for ``get_verdicts``."""
        warn_once(
            "deprecated-graders-get-labels",
            "graders.get_labels is deprecated; use graders.get_verdicts instead.",
        )
        return self.get_verdicts(trace_ids=trace_ids, grader_id=grader_id, limit=limit)

    def save_label(
        self,
        grader_id: str,
        trace_id: str,
        label: bool,
        reason: str | None = None,
        failure_diagnostic: str | None = None,
        confidence: VerdictConfidence | None = None,
    ) -> GraderVerdictOutcome:
        """Deprecated alias for ``save_verdict``, taking the old ``label`` boolean."""
        warn_once(
            "deprecated-graders-save-label",
            'graders.save_label is deprecated; use graders.save_verdict(verdict="pass" or "fail") instead.',
        )
        return self.save_verdict(
            grader_id,
            trace_id,
            verdict="pass" if label else "fail",
            reason=reason,
            failure_diagnostic=failure_diagnostic,
            confidence=confidence,
        )

    def save_label_all(
        self, labels: Sequence[GraderVerdictInput]
    ) -> list[GraderVerdictOutcome]:
        """Deprecated alias for ``save_verdict_all``."""
        warn_once(
            "deprecated-graders-save-label-all",
            "graders.save_label_all is deprecated; use graders.save_verdict_all instead.",
        )
        return self.save_verdict_all(labels)


def _with_legacy_grader_fields(row: dict[str, Any]) -> GraderVerdict:
    filled = dict(row)
    verdict = filled.get("verdict")
    filled.setdefault("label", None if verdict is None else verdict == "pass")
    filled.setdefault("labelReason", filled.get("reason"))
    filled.setdefault("labelConfidence", filled.get("confidence"))
    return cast(GraderVerdict, filled)
