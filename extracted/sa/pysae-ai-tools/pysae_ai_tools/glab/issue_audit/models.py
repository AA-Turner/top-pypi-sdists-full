"""Pydantic models for the audit API."""

from enum import StrEnum

from pydantic import BaseModel


class Status(StrEnum):
    OK = "ok"
    PENDING = "pending"
    PREVIEW = "preview"
    APPLYING = "applying"
    DONE = "done"
    FAILED = "failed"


class StatusResponse(BaseModel):
    status: Status


class ClientsResponse(BaseModel):
    connected: int


class FixPreviewResponse(BaseModel):
    request_id: str
    status: Status
    plan: "FixPlan"


class FixTaskState(BaseModel):
    status: Status
    plan: "FixPlan | None" = None
    output: str = ""


class ErrorResponse(BaseModel):
    error: str


class FixAllRequest(BaseModel):
    """List of issue keys to fix, format: 'project_path#iid'."""

    issues: list[str]


class FixAllResponse(BaseModel):
    request_id: str
    status: Status
    count: int


class Violation(BaseModel):
    check: str
    severity: str
    message: str
    fixable: bool = False
    method: str = ""  # detection method: a DetectionMethod value, or a rule-specific descriptor


class IssueResult(BaseModel):
    iid: int
    project_id: int
    title: str
    web_url: str
    project_path: str
    labels: list[str]
    author: str = ""
    assignees: list[str] = []
    age_days: int = 0
    violations: list[Violation]


class AuditContext(BaseModel):
    project: str | None = None
    user: str | None = None
    search: str | None = None


class PlanAction(BaseModel):
    type: str
    check: str  # which audit check this action fixes
    label: str | None = None
    remove: list[str] | None = None
    title: str | None = None
    current_title: str | None = None
    description: str | None = None
    summary: str | None = None
    needs_claude: bool = False


class IssuePlan(BaseModel):
    project_id: int
    project_path: str
    iid: int
    title: str
    web_url: str
    actions: list[PlanAction]


class FixPlan(BaseModel):
    issues: list[IssuePlan] = []


class AuditProgress(BaseModel):
    phase: str  # "preload" | "checks" | "plan"
    current: int
    total: int
    current_issue: str  # e.g. "pysae/api#123"
    detail: str  # current check or fix being executed, e.g. "labels", "title:translate"


class AggregatedTiming(BaseModel):
    count: int
    total_ms: float
    avg_ms: float
    min_ms: float
    max_ms: float


class CheckTimingItem(BaseModel):
    check: str
    issue_key: str
    duration_ms: float


class FixTimingItem(BaseModel):
    check: str
    fix_type: str
    issue_key: str
    duration_ms: float


class DiagnosticPerf(BaseModel):
    check_timings: list[CheckTimingItem]
    checks_agg: dict[str, AggregatedTiming]
    total_audit_ms: float


class PlanPerf(BaseModel):
    fix_timings: list[FixTimingItem]
    fixes_agg: dict[str, AggregatedTiming]
    total_plan_ms: float


class AuditResults(BaseModel):
    total_issues: int
    issues_with_errors: int
    total_violations: int
    fixable: int
    issues_with_fixable: int = 0
    by_check: dict[str, dict[str, int]]
    active_scopes: dict[str, bool]
    context: AuditContext
    issues: list[IssueResult]
    label_colors: dict[str, str] = {}
    known_projects: list[str] = []
    plan: FixPlan = FixPlan()
    perf: DiagnosticPerf | None = None
    plan_perf: PlanPerf | None = None


class PlanResults(BaseModel):
    plan: FixPlan
    perf: PlanPerf | None = None
