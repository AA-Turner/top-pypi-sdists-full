"""Provenance: which model made an attempt (`Generation` pieces of a `ModelRef`) and who graded it (`Scorer`)."""

from __future__ import annotations

import re
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field, model_validator

from ...compat import StrEnum

SHA256 = re.compile(r"^[0-9a-f]{64}$")
#: Multi-policy runs keep one version line per policy (Miles `trainer_model_id`).
DEFAULT_POLICY_ID = "policy"


def normalize_sha256(value: str) -> str:
    """Lowercase hex, 64 characters."""
    lowered = value.lower()
    if not SHA256.match(lowered):
        raise ValueError("sha256 must be 64 hex characters")
    return lowered


#: A content digest, normalized to lowercase hex (the validator travels with the type into projections).
Sha256 = Annotated[str, AfterValidator(normalize_sha256)]


class ModelRefKind(StrEnum):
    POLICY = "policy"  # this run's weights at a version
    RUN = "run"  # another Probe run's weights (a teacher, the sampling run behind RFT-SFT)
    CHECKPOINT = "checkpoint"  # a stored checkpoint
    EXTERNAL = "external"  # an outside or API model


class PolicyRef(BaseModel):
    """This run's policy at a weight version. The epoch is the sample's own."""

    kind: Literal["policy"] = "policy"
    version: int = Field(ge=0)
    policy_id: str = Field(default=DEFAULT_POLICY_ID, min_length=1, max_length=128)


class RunRef(BaseModel):
    """Another run's weights, named by its weight version or by its step (exactly one)."""

    kind: Literal["run"] = "run"
    run_id: UUID
    version: int | None = Field(default=None, ge=0)
    step: int | None = Field(default=None, ge=0)
    policy_id: str = Field(default=DEFAULT_POLICY_ID, min_length=1, max_length=128)

    @model_validator(mode="after")
    def _one_coordinate(self) -> RunRef:
        if (self.version is None) == (self.step is None):
            raise ValueError("a run ref names exactly one of version or step")
        return self


class CheckpointRef(BaseModel):
    """A checkpoint by artifact id, or by uri (+ sha256 when the producer can hash it)."""

    kind: Literal["checkpoint"] = "checkpoint"
    artifact_id: UUID | None = None
    uri: str | None = Field(default=None, max_length=2048)
    sha256: Sha256 | None = None
    step: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def _named(self) -> CheckpointRef:
        if self.artifact_id is None and not self.uri:
            raise ValueError("a checkpoint ref names an artifact_id or a uri")
        return self


class ExternalRef(BaseModel):
    """A model Probe holds no weights for: a hub model, an API model."""

    kind: Literal["external"] = "external"
    name: str = Field(min_length=1, max_length=512)
    revision: str | None = Field(default=None, max_length=256)
    provider: str | None = Field(default=None, max_length=128)


#: One of the four, told apart by `kind`.
ModelRef = Annotated[PolicyRef | RunRef | CheckpointRef | ExternalRef, Field(discriminator="kind")]


class GenerationPhase(StrEnum):
    PREFILL = "prefill"  # the KV cache built under these weights
    DECODE = "decode"  # tokens sampled under these weights


class Generation(BaseModel):
    """One piece of the response and the model that made it. No token range = somewhere in this attempt."""

    model: ModelRef
    phase: GenerationPhase = GenerationPhase.DECODE
    first_token: int | None = Field(default=None, ge=0)
    last_token: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def _ordered(self) -> Generation:
        if self.first_token is not None and self.last_token is not None and self.first_token > self.last_token:
            raise ValueError("first_token is after last_token")
        return self


class ScorerKind(StrEnum):
    VERIFIER = "verifier"  # a program: a test suite, Harbor's verifier, a regex grader
    REWARD_MODEL = "reward_model"
    TEACHER = "teacher"  # distillation: the teacher's logprobs grade the student
    JUDGE = "judge"  # an LLM judge (a RewardKit judge)


class Scorer(BaseModel):
    """Who graded an attempt. `name` is the key regrades replace by (Harbor: the verifier's import path)."""

    name: str = Field(min_length=1, max_length=256)
    kind: ScorerKind
    model: ModelRef | None = None
    #: The scorer's own version or config digest (Harbor: its kwargs digest).
    version: str | None = Field(default=None, max_length=256)
