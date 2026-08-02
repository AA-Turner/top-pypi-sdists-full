"""Pydantic models for the agent batch orchestrator."""

from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator


class OutcomeStatus(str, Enum):
    SUCCESS = "success"
    ESCALATED = "escalated"
    FAILED = "failed"
    NOT_READY = "not_ready"
    # Phase-1 output of the parallel batch: implemented, reviewed and CI-green, MR approved
    # but NOT merged (`/code-autopilot --stop-before-merge`). Terminal for /code-autopilot,
    # non-terminal for the batch — the serial merge-gate takes it to merged/escalated.
    READY_TO_MERGE = "ready_to_merge"
    # Not processed this run: a hard dependency is unmet (blocker not merged, or transitively
    # a deferred blocker). Left agent::ready for a later run. Exit-code neutral, like not_ready.
    DEFERRED = "deferred"


class Ticket(BaseModel):
    iid: int
    project_path: str
    title: str
    description: str | None = None
    labels: list[str] = Field(default_factory=list)
    web_url: str
    updated_at: datetime
    author_username: str = ""

    @field_validator("updated_at")
    @classmethod
    def _ensure_tz(cls, v: datetime) -> datetime:
        """Force tz-aware UTC if a caller passes a naive datetime (defensive)."""
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)


class TicketAssessment(BaseModel):
    success_probability: int = Field(ge=0, le=100)
    sensitive_domain_match: bool
    rationale: str


class CompletenessAssessment(BaseModel):
    """Sonnet's verdict on whether the ticket has enough spec to be picked up."""

    verdict: Literal["complete", "incomplete"]
    missing_specs: list[str] = Field(default_factory=list)
    rationale: str


class ScoredTicket(BaseModel):
    ticket: Ticket
    business_score: float
    success_probability: int
    sensitive_domain_match: bool
    final_score: float
    rationale: str | None = None
    completeness_verdict: Literal["complete", "incomplete", "skipped"] = "skipped"
    missing_specs: list[str] = Field(default_factory=list)
    completeness_rationale: str = ""


class RunConfig(BaseModel):
    projects: list[str]
    max_tickets: int = 5
    max_tokens: int = 100_000_000
    timeout_seconds: int = 7200
    per_ticket_timeout_seconds: int = 3600
    orphan_timeout_seconds: int = 7200
    dry_run: bool = False
    skip_llm_rank: bool = False
    slack_channel: str = "#tech-ci-agent-autopilot"
    slack_enabled: bool = True
    explicit_tickets: list[str] = Field(default_factory=list)
    watch_post_merge_deploy: bool = True
    deploy_watch_timeout_seconds: int = 1200
    deploy_watch_max_retries: int = 3
    min_success_probability: int = 50
    check_completeness: bool = True
    slack_channel_map: dict[str, str] = Field(default_factory=dict)
    slack_per_project: bool = False  # route each outcome to its repo's slack.tech_channel (else all to slack_channel)
    design_eligibility_threshold: int = 70  # design lane: min Haiku confidence to fast-path
    no_ci: bool = False  # disable all CI launch/verification (pre + post merge) for this run
    ci_at_end: bool = False  # batch: no per-ticket CI; one final CI check once everything is merged
    batch_branch: bool = False  # batch: merge tickets into a temp branch, CI once, then merge it to main


class Outcome(BaseModel):
    ticket_iid: int
    project_path: str
    status: OutcomeStatus
    mr_url: str | None
    mr_iid: int | None
    escalation_reason: str | None
    tokens_used: int = 0
    duration_seconds: int = 0
    cost_usd: float = 0.0
    ticket_title: str = ""
    deploy_status: str | None = None
    deploy_retries: int = 0
    deploy_job_url: str = ""
    not_ready_violations: list[str] = Field(default_factory=list)
    ticket_url: str = ""
    author_username: str = ""
    preview_url: str = ""  # design lane: GitLab Pages proto URL (empty for the code lane)
    # Batch-checkpoint bookkeeping, managed by `agent checkpoint`: `created` = first time the
    # ticket outcome was recorded, `last_updated` = last mutation (e.g. a success later demoted
    # by the deploy watch keeps `created`, bumps `last_updated`). None outside the checkpoint.
    created: str | None = None
    last_updated: str | None = None

    @property
    def is_success(self) -> bool:
        return self.status == OutcomeStatus.SUCCESS

    @property
    def is_escalated(self) -> bool:
        return self.status == OutcomeStatus.ESCALATED

    @model_validator(mode="after")
    def _check_escalation_reason(self) -> Self:
        if self.status == OutcomeStatus.ESCALATED and not self.escalation_reason:
            raise ValueError("escalation_reason is required when status is escalated")
        return self


class RunResult(BaseModel):
    run_id: str
    outcomes: list[Outcome] = Field(default_factory=list)
    dry_run_picks: list[ScoredTicket] = Field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        return sum(o.tokens_used for o in self.outcomes)

    @property
    def total_duration_seconds(self) -> int:
        return sum(o.duration_seconds for o in self.outcomes)

    @property
    def successes(self) -> int:
        return sum(1 for o in self.outcomes if o.is_success)

    @property
    def escalations(self) -> int:
        return sum(1 for o in self.outcomes if o.is_escalated)

    @property
    def not_readys(self) -> int:
        return sum(1 for o in self.outcomes if o.status == OutcomeStatus.NOT_READY)

    @property
    def deferreds(self) -> int:
        return sum(1 for o in self.outcomes if o.status == OutcomeStatus.DEFERRED)
