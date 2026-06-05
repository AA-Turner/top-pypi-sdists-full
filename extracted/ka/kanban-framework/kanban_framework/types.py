from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Phase(str, Enum):
    PLAN = "plan"
    PLAN_REVIEW = "plan_review"
    QA_SPEC = "qa_spec"
    SPEC_REVIEW = "spec_review"
    EXECUTE = "execute"
    EVALUATE = "evaluate"
    RETROSPECTIVE = "retrospective"
    USER_DECISION = "user_decision"
    ARCHIVE = "archive"

    @classmethod
    def _missing_(cls, value):
        """Allow custom phase names (e.g. from extensions.add_phases) to work as pseudo-members.

        Returns a dynamic Phase instance so Phase("security_audit") succeeds
        instead of raising ValueError. list(Phase) still returns only built-in members.
        """
        if isinstance(value, str):
            obj = str.__new__(cls, value)
            obj._name_ = value
            obj._value_ = value
            return obj


class TaskStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class ScoreDimension(str, Enum):
    CODE_QUALITY = "code_quality"
    TEST_COMPLETENESS = "test_completeness"
    REQUIREMENT_COVERAGE = "requirement_coverage"
    DESIGN_REVIEW = "design_review"


class MatchLevel(Enum):
    EXACT = 1.0
    SYNONYM = 0.8
    FUZZY = 0.6

    def __new__(cls, weight: float):
        obj = object.__new__(cls)
        obj._value_ = weight
        obj.weight = weight
        return obj


class ControlMode(str, Enum):
    AUTO = "auto"        # 全自动 — auto-decider 处理所有决策
    SEMI = "semi"        # 半自动 — 系统默认，关键决策点询问用户
    MANUAL = "manual"    # 全手动 — 每步完成后让用户选择下一步


@dataclass
class ScoreResult:
    dimension: ScoreDimension
    score: float
    comment: str = ""


@dataclass
class AutoMode:
    """自动决策配置，控制哪些决策点使用 Agent 自动评估。"""
    auto_brainstorm: bool = False  # 需求澄清决策
    auto_iteration: bool = False   # 自迭代判断
    auto_lightweight: bool = False # 轻量模式选择
    auto_archive: bool = False     # 归档决策
    auto_worktree: bool = False    # 自动使用 worktree


@dataclass
class TaskRun:
    """单次执行记录。每次 agent spawn 创建一个 TaskRun。

    Hermes-inspired: 每次执行都是一行数据，重试历史是 primary representation，
    不是附加在 "latest state" 之上的 afterthought。
    """
    run_id: int                    # 1, 2, 3... per task
    task_id: str                   # 所属 task
    phase: str                     # plan | execute | evaluate | ...
    agent_role: str = ""           # executor | qa | code_reviewer | ...
    status: str = "active"         # active | completed | failed | blocked
    summary: str = ""              # agent 完成时写的交接摘要
    metadata: dict | None = None   # {changed_files, tests_run, decisions, errors, ...}
    error: str = ""                # 失败原因
    started_at: str = ""
    ended_at: str = ""
    duration_seconds: float = 0.0

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    phase: Phase = Phase.PLAN
    iteration: int = 1
    priority: int = 5
    worktree_path: Optional[str] = None
    mode: str = "lightweight"
    control_mode: ControlMode = ControlMode.SEMI
    custom_fsm: dict | None = None  # {"phases": [...], "evaluate_agents": [...]}
    history: list[dict] = field(default_factory=list)
    scores: dict = field(default_factory=dict)
    score_history: list[dict] = field(default_factory=list)
    auto_mode: AutoMode = field(default_factory=AutoMode)
    user_decision: Optional[dict] = None
    test_config: dict | None = None  # {framework, command, coverage, requirements}
    current_run_id: int = 0      # 当前活跃 run 的 ID，0 表示无活跃 run
    total_runs: int = 0          # 历史总 run 数
    biz_tag: Optional[str] = None  # Business context for knowledge isolation

    @property
    def phase_id(self) -> str:
        """Phase string ID, works for both built-in and custom phases."""
        return self.phase.value if isinstance(self.phase, Phase) else self.phase


@dataclass
class Report:
    role: str
    task_id: str
    iteration: int
    score: float = 0.0
    dimensions: dict = field(default_factory=dict)
    summary: str = ""
    passed: bool = False
    critical_issues: list[str] = field(default_factory=list)
    improvement_suggestions: list[str] = field(default_factory=list)


@dataclass
class NLPResult:
    success: bool
    command: str
    task_id: Optional[str] = None
    action: Optional[str] = None
    args: dict = field(default_factory=dict)


@dataclass
class KnowledgeEntry:
    """Single knowledge entry stored in .kanban/knowledge/entries/.

    Schema documentation for the dict shape used by KnowledgeManager.
    KnowledgeManager uses raw dicts for JSON I/O efficiency; this
    dataclass serves as the canonical type reference and test fixture.
    """
    id: str                       # K001, K002, ...
    domain: str                   # cli, agent, testing, infra, workflow, dashboard, git
    category: str                 # 架构, 流程, 工具, 踩坑, 优化
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    source: dict = field(default_factory=dict)  # {task_id, iteration, file, pitfall_id}
    severity: str = "medium"      # high, medium, low
    status: str = "active"        # active, stale, deprecated
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    stale_at: Optional[str] = None
    stats: dict = field(default_factory=lambda: {
        "referenced_count": 0,
        "last_referenced_at": None,
        "last_referenced_by": None,
    })


@dataclass
class DomainInfo:
    """Domain definition for knowledge categorization."""
    name: str
    label: str
    keywords: list[str] = field(default_factory=list)
    auto: bool = False  # True if auto-created from unmatched tags


@dataclass
class KnowledgeIndex:
    """In-memory representation of index.json."""
    domains: dict[str, list[str]] = field(default_factory=dict)  # domain -> [entry_ids]
    entries: dict[str, dict] = field(default_factory=dict)       # entry_id -> {title, domain, tags, severity, status}
    last_updated: str = ""
