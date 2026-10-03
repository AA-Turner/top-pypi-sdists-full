"""Python models for the shared Raindrop eval wire contract."""

from __future__ import annotations

from typing import Any, Callable, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    StrictBool,
    StrictInt,
    StrictFloat,
    StrictStr,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel

Output = Literal["boolean", "score", "number"]


class Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        allow_inf_nan=False,
    )

    def wire(self) -> dict[str, Any]:
        data = self.model_dump(mode="json", by_alias=True)
        for name, field in type(self).model_fields.items():
            if field.exclude:
                continue
            key = field.serialization_alias or field.alias or name
            value = getattr(self, name)
            if value is None and not field.is_required():
                data.pop(key, None)
            elif isinstance(value, Model):
                data[key] = value.wire()
            elif isinstance(value, list):
                data[key] = [
                    entry.wire() if isinstance(entry, Model) else encoded
                    for entry, encoded in zip(value, data[key])
                ]
        return data


class BooleanThreshold(Model):
    equals: StrictBool


class NumericThreshold(Model):
    gte: StrictFloat | None = None
    lte: StrictFloat | None = None

    @model_validator(mode="after")
    def check_bounds(self) -> NumericThreshold:
        if self.gte is None and self.lte is None:
            raise ValueError("A numeric threshold needs gte or lte")
        if self.gte is not None and self.lte is not None and self.gte > self.lte:
            raise ValueError("Lower threshold cannot exceed upper threshold")
        return self


Threshold = BooleanThreshold | NumericThreshold


class Expectation(Model):
    @field_validator("description", "reference", mode="before")
    @classmethod
    def trim_text(cls, value: Any) -> Any:
        return value.strip() if isinstance(value, str) else value

    description: str = Field(min_length=1, max_length=10000)
    basis: Literal["human", "policy", "code", "inferred"] | None = None
    reference: str | None = Field(default=None, min_length=1, max_length=2000)


class VerdictModel(Model):
    @field_validator("note", mode="before", check_fields=False)
    @classmethod
    def trim_note(cls, value: Any) -> Any:
        return value.strip() if isinstance(value, str) else value


class BooleanVerdict(VerdictModel):
    passed: StrictBool = Field(alias="pass")
    note: str | None = Field(default=None, min_length=1, max_length=600)


class ScoreVerdict(VerdictModel):
    score: StrictInt = Field(ge=1, le=5)

    @field_validator("score", mode="before")
    @classmethod
    def integral_number(cls, value: Any) -> Any:
        return int(value) if isinstance(value, float) and value.is_integer() else value

    note: str | None = Field(default=None, min_length=1, max_length=600)


class NumberVerdict(VerdictModel):
    value: StrictFloat
    note: str | None = Field(default=None, min_length=1, max_length=600)


Verdict = BooleanVerdict | ScoreVerdict | NumberVerdict


def parse_verdict(output: Output, value: Any) -> dict[str, Any]:
    cls = {"boolean": BooleanVerdict, "score": ScoreVerdict, "number": NumberVerdict}[
        output
    ]
    if isinstance(value, cls):
        return value.wire()
    return cls.model_validate(value).wire()


class ReplayRow(Model):
    id: StrictStr = Field(min_length=1, max_length=512)
    name: StrictStr
    input: StrictStr | None
    output: JsonValue = None
    properties: dict[str, StrictStr] = Field(default_factory=dict)

    def wire(self) -> dict[str, Any]:
        result = super().wire()
        result["output"] = self.output
        return result

    @field_validator("id")
    @classmethod
    def clean_id(cls, value: str) -> str:
        if value != value.strip():
            raise ValueError("Row id cannot have surrounding whitespace")
        return value


class CaptureReference(Model):
    id: str = Field(pattern=r"^[a-f0-9]{64}$")
    source_event_id: str = Field(min_length=1, max_length=512)
    source_event_timestamp: str | None = None


class DatasetRow(ReplayRow):
    properties: dict[str, StrictStr]

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value: Any) -> Any:
        return value.strip() if isinstance(value, str) else value

    name: StrictStr = Field(min_length=1, max_length=200)
    reference_trace: dict[str, JsonValue] | None = None
    reference_capture: CaptureReference | None = None
    expectation: Expectation | None = None
    expected_verdict: dict[str, JsonValue] | None = None
    reference_trace_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")

    @field_validator("reference_trace", mode="before")
    @classmethod
    def normalized_snapshot(cls, value: Any) -> Any:
        if value is None:
            return None
        from .trace_tools import normalize_reference_snapshot

        return normalize_reference_snapshot(value)

    @field_validator("expected_verdict")
    @classmethod
    def label(cls, value: Any) -> Any:
        if value is not None:
            if set(value) not in ({"pass"}, {"score"}, {"value"}):
                raise ValueError("Reference verdict must have exactly one graded value")
            parse_verdict(
                "boolean"
                if "pass" in value
                else "score"
                if "score" in value
                else "number",
                value,
            )
        return value


class DatasetIdentity(Model):
    id: UUID
    slug: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str = Field(min_length=1, max_length=100)
    current_version_id: UUID | None


class DatasetVersion(Model):
    id: UUID
    dataset_id: UUID
    parent_version_id: UUID | None
    fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    created_at: str


class DatasetManifest(Model):
    dataset: DatasetIdentity
    version: DatasetVersion
    rows: list[DatasetRow] = Field(alias="cases")

    @model_validator(mode="after")
    def consistent(self) -> DatasetManifest:
        if self.dataset.id != self.version.dataset_id:
            raise ValueError("Dataset and version identities do not match")
        if len({row.id for row in self.rows}) != len(self.rows):
            raise ValueError("Duplicate dataset row ids")
        return self

    @classmethod
    def from_wire(cls, value: dict[str, Any]) -> DatasetManifest:
        value = dict(value)
        value["rows"] = value.pop("cases")
        return cls.model_validate(value)


class EvalDataset(Model):
    id: str
    name: str
    version: str
    rows: list[ReplayRow]
    remote: dict[str, str] | None = None


class ProgramIdentity(Model):
    eval_id: UUID
    program_version: StrictInt = Field(gt=0)


class EvalProgram(Model):
    kind: Literal["program"] = "program"
    slug: str = Field(max_length=64, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str = Field(min_length=1, max_length=120)
    output: Output
    scope: Literal["batch"] = "batch"
    execution_mode: Literal["deterministic", "judge"]
    source: str = Field(min_length=1)
    description: str | None = Field(default=None, max_length=2000)
    intent: str = Field(min_length=1, max_length=10000)
    rules: list[str] = Field(default_factory=list, max_length=12)
    expected: ProgramIdentity | None = None


class LocalEvaluatorContext(Model):
    trace: dict[str, Any]
    reference: dict[str, Any] | None = None
    row: ReplayRow
    result: Any


class LocalEvaluator(Model):
    slug: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    name: str = Field(min_length=1, max_length=120)
    output: Output
    scope: Literal["row"] = "row"
    requires_reference: bool = False
    judge: Callable[[LocalEvaluatorContext], Any] = Field(exclude=True)


class ManifestEvaluator(Model):
    @model_validator(mode="before")
    @classmethod
    def normalize(cls, value: Any) -> Any:
        if isinstance(value, dict):
            value = dict(value)
            if "threshold" in value and value["threshold"] is None:
                raise ValueError("Optional threshold must be omitted, not null")
            if isinstance(value.get("evaluator"), str):
                value["evaluator"] = value["evaluator"].strip()
        return value

    evaluator: str = Field(min_length=1)
    threshold: Threshold | None = None


class EvalSuiteManifest(Model):
    @field_validator("concurrency", mode="before")
    @classmethod
    def integral_concurrency(cls, value: Any) -> Any:
        return int(value) if isinstance(value, float) and value.is_integer() else value

    @model_validator(mode="before")
    @classmethod
    def reject_json_nulls(cls, value: Any) -> Any:
        if isinstance(value, dict) and any(entry is None for entry in value.values()):
            raise ValueError("Optional manifest settings must be omitted, not null")
        return value

    name: str = Field(min_length=1)
    dataset: str = Field(min_length=1)
    dataset_version_id: UUID | None = None
    evaluators: list[ManifestEvaluator] = Field(min_length=1)
    concurrency: StrictInt | None = Field(default=None, gt=0)
    trace_wait_ms: StrictFloat | None = Field(default=None, ge=0)
    eval_wait_ms: StrictFloat | None = Field(default=None, ge=0)
    eval_poll_interval_ms: StrictFloat | None = Field(default=None, gt=0)

    @field_validator("name", "dataset")
    @classmethod
    def trimmed(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Cannot be empty")
        return value


class Evaluator(Model):
    evaluator: Any
    threshold: Threshold | None = None

    @model_validator(mode="after")
    def check(self) -> Evaluator:
        value = self.evaluator
        if isinstance(value, str):
            self.evaluator = value.strip()
            if not self.evaluator:
                raise ValueError("Evaluator reference cannot be empty")
        elif (
            not isinstance(value, (LocalEvaluator, EvalProgram))
            and getattr(value, "kind", None) != "portable"
        ):
            raise ValueError("Expected a saved evaluator slug or defined evaluator")
        else:
            validate_threshold(value.output, self.threshold)
        return self


class EvalSuite(Model):
    @field_validator("concurrency", mode="before")
    @classmethod
    def integral_concurrency(cls, value: Any) -> Any:
        return int(value) if isinstance(value, float) and value.is_integer() else value

    name: str = Field(min_length=1)
    dataset: str | EvalDataset
    dataset_version_id: UUID | None = None
    evaluators: list[Evaluator] = Field(min_length=1)
    concurrency: StrictInt = Field(default=4, gt=0)
    trace_wait_ms: StrictFloat = Field(default=60000, ge=0)
    eval_wait_ms: StrictFloat = Field(default=600000, ge=0)
    eval_poll_interval_ms: StrictFloat = Field(default=2000, gt=0)
    run: Callable[[ReplayRow], Any] | None = Field(default=None, exclude=True)
    agent: Any = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def valid(self) -> EvalSuite:
        if (self.run is None) == (self.agent is None):
            raise ValueError("Bind exactly one local run callback or agent")
        names = [evaluator_name(entry) for entry in self.evaluators]
        if len(set(names)) != len(names):
            raise ValueError("Suite evaluators must be unique")
        if isinstance(self.dataset, str):
            self.dataset = self.dataset.strip()
            if not self.dataset:
                raise ValueError("Dataset reference cannot be empty")
        elif self.dataset_version_id:
            raise ValueError("A dataset version pin requires a published dataset")
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Suite name cannot be empty")
        return self


class Destination(Model):
    kind: Literal["raindrop"] = "raindrop"
    query_url: str | None = None
    replay_ingest_url: str | None = None


class Selection(Model):
    dataset: DatasetManifest
    row_ids: list[str] = Field(min_length=1)


class Counts(Model):
    total: StrictInt = Field(ge=0)
    pending: StrictInt = Field(ge=0)
    done: StrictInt = Field(ge=0)
    missing: StrictInt = Field(ge=0)


class VerdictAssessment(Model):
    state: Literal["passed", "failed", "measurement", "errored", "ungraded"]
    evaluator: str
    verdict: dict[str, Any]


class RowResult(ReplayRow):
    attempt: StrictInt = Field(default=0, ge=0)
    status: Literal["pending", "done", "missing"]
    trace_id: str | None = None
    error: str | None = None
    verdicts: list[VerdictAssessment] = Field(default_factory=list)


class SuiteResult(Model):
    run_id: str
    name: str
    status: Literal["queued", "running", "complete", "failed"]
    counts: Counts
    traces_expire_at: str | None = None
    traces_expired: bool
    evaluators: list[dict[str, Any]]
    rows: list[RowResult]

    @property
    def passed(self) -> bool:
        latest = {row.id: row for row in sorted(self.rows, key=lambda row: row.attempt)}
        return (
            self.status == "complete"
            and self.counts.pending == 0
            and self.counts.missing == 0
            and self.counts.done == self.counts.total
            and len(latest) == self.counts.total
            and all(e.get("status") == "completed" for e in self.evaluators)
            and all(
                r.status == "done"
                and len(r.verdicts) == len(self.evaluators)
                and all(v.state in ("passed", "measurement") for v in r.verdicts)
                for r in latest.values()
            )
        )


def evaluator_name(entry: Evaluator) -> str:
    return entry.evaluator if isinstance(entry.evaluator, str) else entry.evaluator.slug


def validate_threshold(output: Output, threshold: Threshold | None) -> None:
    if threshold is None:
        return
    if output == "boolean":
        if not isinstance(threshold, BooleanThreshold):
            raise ValueError("Boolean evaluators require a boolean threshold")
    else:
        if not isinstance(threshold, NumericThreshold):
            raise ValueError("Numeric evaluators require a numeric threshold")
        if output == "score" and any(
            v is not None and not 1 <= v <= 5 for v in (threshold.gte, threshold.lte)
        ):
            raise ValueError("Score thresholds must be from 1 to 5")


def assess_verdict(
    entry: Evaluator, verdict: dict[str, Any], output: Output
) -> VerdictAssessment:
    name = evaluator_name(entry)
    if verdict["evaluator"] != name:
        raise ValueError("Verdict evaluator does not match")
    state = verdict["state"]
    if state in ("errored", "ungraded"):
        return VerdictAssessment(state=state, evaluator=name, verdict=verdict)
    payload = {
        k: verdict[k] for k in ("pass", "score", "value", "note") if k in verdict
    }
    parse_verdict(output, payload)
    validate_threshold(output, entry.threshold)
    if output == "boolean":
        expected = (
            entry.threshold.equals
            if isinstance(entry.threshold, BooleanThreshold)
            else True
        )
        state = "passed" if payload["pass"] == expected else "failed"
    elif entry.threshold is None:
        state = "measurement"
    else:
        value = payload["score" if output == "score" else "value"]
        threshold = entry.threshold
        state = (
            "passed"
            if (threshold.gte is None or value >= threshold.gte)
            and (threshold.lte is None or value <= threshold.lte)
            else "failed"
        )
    return VerdictAssessment(state=state, evaluator=name, verdict=verdict)
