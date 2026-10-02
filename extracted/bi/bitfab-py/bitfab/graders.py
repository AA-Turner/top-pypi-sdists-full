from __future__ import annotations

from typing import Literal, TypedDict
from urllib.parse import urlencode

from typing_extensions import NotRequired

from bitfab.http import HttpClient
from bitfab.labels import LabelConfidence

GRADER_LABELS_PATH = "/api/sdk/graderLabels"

GraderStatus = Literal["active", "archived"]
GraderLabelSource = Literal["human", "live_grader"]


class GraderLabel(TypedDict):
    traceId: str
    graderId: str
    graderName: str | None
    graderStatus: GraderStatus
    graderType: str
    label: bool | None
    labelReason: str | None
    failureDiagnostic: str | None
    labelConfidence: LabelConfidence | None
    source: GraderLabelSource
    evaluatedAt: str | None


class GraderLabelUpdate(TypedDict):
    graderId: str
    traceId: str
    label: bool
    reason: NotRequired[str]
    failureDiagnostic: NotRequired[str]
    confidence: NotRequired[LabelConfidence]


class GraderLabelOutcome(TypedDict):
    graderId: str
    traceId: str
    label: bool
    action: Literal["set"]


class GradersClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def get_labels(
        self,
        trace_ids: list[str] | None = None,
        grader_id: str | None = None,
        limit: int | None = None,
    ) -> list[GraderLabel]:
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
        result = self._http_client.get(f"{GRADER_LABELS_PATH}?{urlencode(params)}")
        return result["labels"]

    def save_label(
        self,
        grader_id: str,
        trace_id: str,
        label: bool,
        reason: str | None = None,
        failure_diagnostic: str | None = None,
        confidence: LabelConfidence | None = None,
    ) -> GraderLabelOutcome:
        update: GraderLabelUpdate = {
            "graderId": grader_id,
            "traceId": trace_id,
            "label": label,
        }
        if reason is not None:
            update["reason"] = reason
        if failure_diagnostic is not None:
            update["failureDiagnostic"] = failure_diagnostic
        if confidence is not None:
            update["confidence"] = confidence
        return self.save_label_all([update])[0]

    def save_label_all(
        self, labels: list[GraderLabelUpdate]
    ) -> list[GraderLabelOutcome]:
        result = self._http_client.request(GRADER_LABELS_PATH, {"labels": labels})
        return result["labels"]
