"""Oracle contracts (k90): the typed currency of route-to-best-result.

Every contract is a frozen, slotted dataclass in the studio-schemas idiom
(``video_intel/studio/schemas.py``): closed vocabularies are str-Enums (they
serialize straight to JSON), collections are tuples so instances stay hashable,
and structurally-invalid values are programmer error raised in ``__post_init__``
— never runtime data that leaks downstream.

These are the contracts k91 (``POST /oracle/route``: execute → ExecutionReceipt
+ deterministic technical Scorecard) and k92 (evaluator kernel: heterogeneous
checks, judges, repair codes) build ON — so receipts and scorecards are defined
here NOW, not when their producers land. The catalog (``catalog.py``) produces
``CapabilityView``; ``GET /oracle/capabilities`` serializes it via ``to_dict``.

Wire shape: every contract has ``to_dict()`` (JSON-safe, enums as their str
values) and a ``from_dict()`` classmethod, so round-tripping through HTTP/store
is lossless and proven in ``tests/test_oracle_contracts.py``.

No pathlib anywhere. os.path only (not that this module touches the disk).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


# ---------------------------------------------------------------------------
# Closed vocabularies
# ---------------------------------------------------------------------------


class QualityProfile(str, Enum):
    PREVIEW = "preview"
    BALANCED = "balanced"
    BEST = "best"


class InputKind(str, Enum):
    """What the operator SUPPLIED with the goal (typed input refs)."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    URL = "url"


class ArtifactKind(str, Enum):
    """What a capability accepts/produces. Superset of InputKind: execution also
    yields derived kinds (embeddings, structured JSON, extracted documents)."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    URL = "url"
    EMBEDDING = "embedding"
    JSON = "json"
    DOCUMENT = "document"


class SourceRegistry(str, Enum):
    """Which of the two existing registries owns a capability (the k90 bridge
    is READ-ONLY composition over both — see catalog.py)."""
    STUDIO = "studio"   # video_intel/studio: typed ModelConfig/Capability zoo
    TASKS = "tasks"     # imports/config/models: legacy tasks-string registry


class FailureClass(str, Enum):
    """ExecutionReceipt failure classification — WHERE an execution died, not
    what to regenerate (that is RepairCode, the evaluator's verdict)."""
    DECODE_FAILED = "decode_failed"
    EMPTY_OUTPUT = "empty_output"
    FORMAT_MISMATCH = "format_mismatch"
    TIMEOUT = "timeout"
    WORKER_UNAVAILABLE = "worker_unavailable"
    CAPABILITY_GAP = "capability_gap"
    RUNNER_ERROR = "runner_error"      # the runner raised / returned Err
    REFUSED = "refused"                # policy/license/authority gate said no
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class CheckKind(str, Enum):
    """The heterogeneous-evidence axes (action_plan: technical / identity /
    semantic / temporal / speech / sync / whole-result intent)."""
    TECHNICAL = "technical"
    IDENTITY = "identity"
    SEMANTIC = "semantic"
    TEMPORAL = "temporal"
    SPEECH = "speech"
    SYNC = "sync"
    INTENT = "intent"


class RepairCode(str, Enum):
    """A failing evaluation names WHAT to regenerate — the repair controller
    (k92) maps the code to a bounded subgraph, never a full re-run."""
    IDENTITY_DRIFT = "identity_drift"
    ACTION_MISSING = "action_missing"
    VOICE_SIMILARITY_LOW = "voice_similarity_low"
    LINE_OMITTED = "line_omitted"
    SHOT_TOO_SHORT = "shot_too_short"
    LIP_SYNC_OUT_OF_RANGE = "lip_sync_out_of_range"
    TEMPORAL_ARTIFACT = "temporal_artifact"
    INTENT_MISMATCH = "intent_mismatch"    # judge: artifact does not satisfy the goal
    SOURCE_AUTHORITY_MISSING = "source_authority_missing"
    DECODE_FAILED = "decode_failed"
    EMPTY_OUTPUT = "empty_output"
    FORMAT_MISMATCH = "format_mismatch"
    TIMEOUT = "timeout"
    WORKER_UNAVAILABLE = "worker_unavailable"
    CAPABILITY_GAP = "capability_gap"


# ---------------------------------------------------------------------------
# GoalSpec (lite)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class InputRef:
    """One supplied input, typed. ``ref`` is whatever the transport hands over
    (an upload path/handle, a URL, inline text) — the oracle resolves it at
    execution time; the contract only pins WHAT KIND of thing it is."""
    kind: InputKind
    ref: str
    label: str = ""

    def __post_init__(self) -> None:
        if not self.ref:
            raise ValueError("InputRef.ref must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "ref": self.ref, "label": self.label}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "InputRef":
        return cls(kind=InputKind(d["kind"]), ref=d["ref"],
                   label=d.get("label", ""))


@dataclass(frozen=True, slots=True)
class BudgetHints:
    """Soft budget hints — planning inputs, not enforced limits (admission and
    placement stay where they live today)."""
    max_seconds: float | None = None
    max_vram_gb: float | None = None

    def __post_init__(self) -> None:
        for name, val in (("max_seconds", self.max_seconds),
                          ("max_vram_gb", self.max_vram_gb)):
            if val is not None and val <= 0:
                raise ValueError(f"BudgetHints.{name} must be positive, got {val}")

    def to_dict(self) -> dict[str, Any]:
        return {"max_seconds": self.max_seconds, "max_vram_gb": self.max_vram_gb}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "BudgetHints":
        return cls(max_seconds=d.get("max_seconds"),
                   max_vram_gb=d.get("max_vram_gb"))


@dataclass(frozen=True, slots=True)
class GoalSpec:
    """The normalized meaning of an operator request (lite slice: no rights
    manifests, no approval gates, no clarification loop yet — those phases are
    explicitly deferred by the keeper assessment).

    ``raw_prompt`` is the operator's message VERBATIM and immutable alongside
    the normalized ``objective`` — normalization must never destroy the source.
    ``capability`` is a namespaced catalog name (``audio.transcribe``); None
    means auto (k91's intent classifier picks)."""
    objective: str
    raw_prompt: str
    inputs: tuple[InputRef, ...] = ()
    capability: str | None = None
    quality: QualityProfile = QualityProfile.BALANCED
    budget: BudgetHints = field(default_factory=BudgetHints)
    acceptance: tuple[str, ...] = ()   # free-text acceptance notes, for now

    def __post_init__(self) -> None:
        if not self.objective.strip():
            raise ValueError("GoalSpec.objective must be non-empty")
        if not self.raw_prompt.strip():
            raise ValueError("GoalSpec.raw_prompt must be non-empty (the "
                             "operator's message rides alongside, immutable)")
        if self.capability is not None and "." not in self.capability:
            raise ValueError(
                f"GoalSpec.capability must be a namespaced catalog name "
                f"(e.g. 'audio.transcribe'), got {self.capability!r}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "raw_prompt": self.raw_prompt,
            "inputs": [i.to_dict() for i in self.inputs],
            "capability": self.capability,
            "quality": self.quality.value,
            "budget": self.budget.to_dict(),
            "acceptance": list(self.acceptance),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "GoalSpec":
        return cls(
            objective=d["objective"],
            raw_prompt=d["raw_prompt"],
            inputs=tuple(InputRef.from_dict(i) for i in d.get("inputs", ())),
            capability=d.get("capability"),
            quality=QualityProfile(d.get("quality", "balanced")),
            budget=BudgetHints.from_dict(d.get("budget") or {}),
            acceptance=tuple(d.get("acceptance", ())),
        )


# ---------------------------------------------------------------------------
# CapabilityView — the unified catalog descriptor (both registries)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Eligibility:
    """Can this capability execute on the fleet RIGHT NOW, and if not, why not.
    An ineligible view with no reasons is a contract violation — the whole
    point of GET /oracle/capabilities is explaining refusals BEFORE execution
    (Phase-1 done-criterion). Reasons on an ELIGIBLE view are allowed: they are
    advisory (e.g. 'no online worker; central serves it in-process')."""
    eligible: bool
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.eligible and not self.reasons:
            raise ValueError("ineligible Eligibility must carry >=1 reason")

    def to_dict(self) -> dict[str, Any]:
        return {"eligible": self.eligible, "reasons": list(self.reasons)}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Eligibility":
        return cls(eligible=bool(d["eligible"]),
                   reasons=tuple(d.get("reasons", ())))


@dataclass(frozen=True, slots=True)
class ResourceHints:
    """Where known. The studio zoo carries real VRAM envelopes; the legacy
    tasks registry carries none — None means unknown, never fabricated."""
    min_vram_gb: float | None = None
    frameworks: tuple[str, ...] = ()
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"min_vram_gb": self.min_vram_gb,
                "frameworks": list(self.frameworks), "notes": self.notes}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "ResourceHints":
        return cls(min_vram_gb=d.get("min_vram_gb"),
                   frameworks=tuple(d.get("frameworks", ())),
                   notes=d.get("notes", ""))


@dataclass(frozen=True, slots=True)
class CapabilityView:
    """One namespaced capability as the unified catalog presents it — the
    READ-ONLY join of a registry's rows, its runner/viability gates, and the
    fleet's worker-health signals. Source of truth stays in the two registries;
    this is a view, never a third store."""
    name: str                          # namespaced: "audio.transcribe"
    source: SourceRegistry
    accepts: tuple[ArtifactKind, ...]
    produces: tuple[ArtifactKind, ...]
    model_ids: tuple[str, ...]
    eligibility: Eligibility
    resources: ResourceHints = field(default_factory=ResourceHints)

    def __post_init__(self) -> None:
        if "." not in self.name:
            raise ValueError(f"CapabilityView.name must be namespaced, got {self.name!r}")
        if not self.produces:
            raise ValueError(f"{self.name}: a capability must produce something")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "source": self.source.value,
            "accepts": [k.value for k in self.accepts],
            "produces": [k.value for k in self.produces],
            "model_ids": list(self.model_ids),
            "eligibility": self.eligibility.to_dict(),
            "resources": self.resources.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "CapabilityView":
        return cls(
            name=d["name"],
            source=SourceRegistry(d["source"]),
            accepts=tuple(ArtifactKind(k) for k in d.get("accepts", ())),
            produces=tuple(ArtifactKind(k) for k in d.get("produces", ())),
            model_ids=tuple(d.get("model_ids", ())),
            eligibility=Eligibility.from_dict(d["eligibility"]),
            resources=ResourceHints.from_dict(d.get("resources") or {}),
        )


# ---------------------------------------------------------------------------
# ExecutionReceipt
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """A produced artifact by pointer + content hash. ``sha256`` is None only
    when the artifact is not a local file we could hash (e.g. a stream)."""
    kind: ArtifactKind
    uri: str
    sha256: str | None = None

    def __post_init__(self) -> None:
        if not self.uri:
            raise ValueError("ArtifactRef.uri must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "uri": self.uri, "sha256": self.sha256}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "ArtifactRef":
        return cls(kind=ArtifactKind(d["kind"]), uri=d["uri"],
                   sha256=d.get("sha256"))


@dataclass(frozen=True, slots=True)
class ExecutionReceipt:
    """What actually ran, on what, with what result — one per routed execution
    (k91 emits one on EVERY /oracle/route response, success or not).

    ``request`` is the NORMALIZED request as sorted ``(key, json-value)`` pairs
    (tuple-of-pairs keeps the dataclass frozen/hashable, same trick as the
    studio's VramEnvelope). Build it with ``normalize_request``; read it back
    with ``request_dict``. Timestamps are ISO-8601 strings, like the studio
    ledger's ``LedgerEvent.at``."""
    request: tuple[tuple[str, str], ...]
    capability: str
    model_id: str
    worker: str | None
    started_at: str
    ended_at: str
    duration_s: float
    retries: int = 0
    failure: FailureClass | None = None
    artifacts: tuple[ArtifactRef, ...] = ()
    warnings: tuple[str, ...] = ()
    log_excerpt: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.capability:
            raise ValueError("ExecutionReceipt.capability must be non-empty")
        if self.duration_s < 0:
            raise ValueError(f"negative duration_s: {self.duration_s}")
        if self.retries < 0:
            raise ValueError(f"negative retries: {self.retries}")

    @staticmethod
    def normalize_request(req: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
        """Mapping -> canonical sorted (key, json-encoded value) pairs. Stable
        across dict ordering, so identical requests normalize identically."""
        return tuple(
            (k, json.dumps(req[k], sort_keys=True, separators=(",", ":")))
            for k in sorted(req)
        )

    def request_dict(self) -> dict[str, Any]:
        return {k: json.loads(v) for k, v in self.request}

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request_dict(),
            "capability": self.capability,
            "model_id": self.model_id,
            "worker": self.worker,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_s": self.duration_s,
            "retries": self.retries,
            "failure": self.failure.value if self.failure else None,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "warnings": list(self.warnings),
            "log_excerpt": list(self.log_excerpt),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "ExecutionReceipt":
        failure = d.get("failure")
        return cls(
            request=cls.normalize_request(d.get("request") or {}),
            capability=d["capability"],
            model_id=d["model_id"],
            worker=d.get("worker"),
            started_at=d["started_at"],
            ended_at=d["ended_at"],
            duration_s=float(d["duration_s"]),
            retries=int(d.get("retries", 0)),
            failure=FailureClass(failure) if failure else None,
            artifacts=tuple(ArtifactRef.from_dict(a) for a in d.get("artifacts", ())),
            warnings=tuple(d.get("warnings", ())),
            log_excerpt=tuple(d.get("log_excerpt", ())),
        )


# ---------------------------------------------------------------------------
# Scorecard (load-bearing per operator decision 2026-08-05)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Check:
    """One deterministic/measured check. ``value``/``threshold`` are loosely
    typed on purpose (a decode check has no numeric threshold; a similarity
    check does) — ``kind`` + ``name`` say what the numbers mean."""
    name: str
    kind: CheckKind
    value: float | str | bool | None
    threshold: float | str | None
    passed: bool
    detail: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Check.name must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "kind": self.kind.value, "value": self.value,
                "threshold": self.threshold, "passed": self.passed,
                "detail": self.detail}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Check":
        return cls(name=d["name"], kind=CheckKind(d["kind"]),
                   value=d.get("value"), threshold=d.get("threshold"),
                   passed=bool(d["passed"]), detail=d.get("detail", ""))


@dataclass(frozen=True, slots=True)
class JudgeResult:
    """One model-judge's opinion (VLM rubric, round-trip ASR compare, …).
    Kept apart from Check: judges are heterogeneous EVIDENCE, not gates —
    disagreement between them is signal, recorded on the Scorecard."""
    judge: str
    verdict: str
    score: float | None = None
    rationale: str = ""

    def __post_init__(self) -> None:
        if not self.judge:
            raise ValueError("JudgeResult.judge must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {"judge": self.judge, "verdict": self.verdict,
                "score": self.score, "rationale": self.rationale}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "JudgeResult":
        return cls(judge=d["judge"], verdict=d["verdict"],
                   score=d.get("score"), rationale=d.get("rationale", ""))


@dataclass(frozen=True, slots=True)
class Scorecard:
    """The machine-readable verdict on one artifact/execution. The generating
    model never declares its own result good — this is built from checks and
    judges OUTSIDE the generator (k91: deterministic technical checks on every
    response; k92: the full heterogeneous kernel).

    Invariants: ``confidence`` in [0, 1]; a ``repair_code`` on a hard-PASSING
    card is incoherent (a repair is a diagnosis of failure) and refused."""
    hard_pass: bool
    checks: tuple[Check, ...] = ()
    judge_results: tuple[JudgeResult, ...] = ()
    confidence: float = 1.0
    disagreements: tuple[str, ...] = ()
    diagnosis: str | None = None
    repair_code: RepairCode | None = None
    recommended_repair: str | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0, 1], got {self.confidence}")
        if self.hard_pass and self.repair_code is not None:
            raise ValueError(
                f"a hard-passing Scorecard cannot carry repair_code "
                f"{self.repair_code.value!r} — repairs diagnose failures")

    def to_dict(self) -> dict[str, Any]:
        return {
            "hard_pass": self.hard_pass,
            "checks": [c.to_dict() for c in self.checks],
            "judge_results": [j.to_dict() for j in self.judge_results],
            "confidence": self.confidence,
            "disagreements": list(self.disagreements),
            "diagnosis": self.diagnosis,
            "repair_code": self.repair_code.value if self.repair_code else None,
            "recommended_repair": self.recommended_repair,
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "Scorecard":
        code = d.get("repair_code")
        return cls(
            hard_pass=bool(d["hard_pass"]),
            checks=tuple(Check.from_dict(c) for c in d.get("checks", ())),
            judge_results=tuple(JudgeResult.from_dict(j)
                                for j in d.get("judge_results", ())),
            confidence=float(d.get("confidence", 1.0)),
            disagreements=tuple(d.get("disagreements", ())),
            diagnosis=d.get("diagnosis"),
            repair_code=RepairCode(code) if code else None,
            recommended_repair=d.get("recommended_repair"),
        )
