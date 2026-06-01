from __future__ import annotations
import json
from dataclasses import asdict

from kanban_framework.types import (
    Phase, TaskStatus, ScoreDimension,
    ScoreResult, Task, Report, NLPResult, MatchLevel,
    KnowledgeEntry, DomainInfo, KnowledgeIndex,
)


class TestPhase:
    def test_all_phases_defined(self):
        assert Phase.PLAN.value == "plan"
        assert Phase.EXECUTE.value == "execute"
        assert Phase.EVALUATE.value == "evaluate"
        assert Phase.USER_DECISION.value == "user_decision"
        assert Phase.ARCHIVE.value == "archive"

    def test_phase_from_string(self):
        assert Phase("plan") == Phase.PLAN
        assert Phase("execute") == Phase.EXECUTE


class TestTaskStatus:
    def test_all_statuses_defined(self):
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.ERROR.value == "error"
        assert TaskStatus.ARCHIVED.value == "archived"


class TestTask:
    def test_default_values(self):
        task = Task(id="TASK-001", title="Test", description="Desc")
        assert task.status == TaskStatus.PENDING
        assert task.phase == Phase.PLAN
        assert task.iteration == 1
        assert task.worktree_path is None
        assert task.history == []

    def test_to_json_serializable(self):
        task = Task(id="TASK-001", title="Test", description="Desc")
        d = asdict(task)
        d["status"] = task.status.value
        d["phase"] = task.phase.value
        d["worktree_path"] = None
        result = json.dumps(d)
        assert "TASK-001" in result

    def test_to_json_with_worktree_path(self):
        task = Task(id="TASK-002", title="Test", description="Desc",
                    worktree_path="/tmp/test")
        d = asdict(task)
        d["status"] = task.status.value
        d["phase"] = task.phase.value
        result = json.dumps(d)
        assert "/tmp/test" in result


class TestScoreResult:
    def test_create_score(self):
        s = ScoreResult(
            dimension=ScoreDimension.CODE_QUALITY,
            score=8.5,
            comment="Good"
        )
        assert s.score == 8.5
        assert s.dimension == ScoreDimension.CODE_QUALITY


class TestNLPResult:
    def test_success_result(self):
        r = NLPResult(success=True, command="create", task_id=None)
        assert r.success is True
        assert r.command == "create"

    def test_failed_result(self):
        r = NLPResult(success=False, command="unknown")
        assert r.success is False


class TestReport:
    def test_report_creation(self):
        r = Report(
            role="qa",
            task_id="TASK-001",
            iteration=1,
            score=7.0,
            dimensions={"test_completeness": {"score": 7.0, "findings": [], "issues": []}},
            summary="All good",
            passed=False,
        )
        assert r.role == "qa"
        assert r.score == 7.0
        assert "test_completeness" in r.dimensions


class TestKnowledgeEntry:
    def test_default_values(self):
        entry = KnowledgeEntry(id="K001", domain="cli", category="架构",
                               title="Test", content="Test content")
        assert entry.id == "K001"
        assert entry.domain == "cli"
        assert entry.category == "架构"
        assert entry.title == "Test"
        assert entry.content == "Test content"
        assert entry.tags == []
        assert entry.source == {}
        assert entry.severity == "medium"
        assert entry.status == "active"
        assert entry.created_at is None
        assert entry.updated_at is None
        assert entry.stale_at is None
        assert entry.stats == {
            "referenced_count": 0,
            "last_referenced_at": None,
            "last_referenced_by": None,
        }

    def test_factory_isolation_tags(self):
        e1 = KnowledgeEntry(id="K001", domain="cli", category="架构",
                            title="T1", content="C1", tags=["tag1"])
        e2 = KnowledgeEntry(id="K002", domain="agent", category="流程",
                            title="T2", content="C2", tags=["tag2"])
        e1.tags.append("extra")
        assert "extra" in e1.tags
        assert "extra" not in e2.tags
        assert e2.tags == ["tag2"]

    def test_factory_isolation_stats(self):
        e1 = KnowledgeEntry(id="K001", domain="cli", category="架构",
                            title="T1", content="C1")
        e2 = KnowledgeEntry(id="K002", domain="agent", category="流程",
                            title="T2", content="C2")
        e1.stats["referenced_count"] = 5
        assert e1.stats["referenced_count"] == 5
        assert e2.stats["referenced_count"] == 0

    def test_json_roundtrip(self):
        entry = KnowledgeEntry(
            id="K001", domain="cli", category="架构",
            title="Test Title", content="Some content",
            tags=["python", "cli"],
            source={"task_id": "TASK-001", "iteration": 1},
            severity="high",
            status="active",
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-02T00:00:00Z",
            stale_at=None,
        )
        d = asdict(entry)
        result = json.dumps(d)
        assert "K001" in result
        assert "Test Title" in result
        assert "python" in result
        assert "cli" in result
        assert "TASK-001" in result


class TestDomainInfo:
    def test_default_values(self):
        di = DomainInfo(name="cli", label="CLI")
        assert di.name == "cli"
        assert di.label == "CLI"
        assert di.keywords == []
        assert di.auto is False

    def test_with_keywords(self):
        di = DomainInfo(name="testing", label="Testing",
                        keywords=["pytest", "unittest"], auto=True)
        assert di.keywords == ["pytest", "unittest"]
        assert di.auto is True

    def test_factory_isolation_keywords(self):
        d1 = DomainInfo(name="a", label="A", keywords=["k1"])
        d2 = DomainInfo(name="b", label="B", keywords=["k2"])
        d1.keywords.append("k3")
        assert "k3" in d1.keywords
        assert "k3" not in d2.keywords
        assert d2.keywords == ["k2"]

    def test_json_roundtrip(self):
        di = DomainInfo(name="infra", label="Infrastructure",
                        keywords=["docker", "kubernetes"], auto=False)
        d = asdict(di)
        result = json.dumps(d)
        assert "infra" in result
        assert "Infrastructure" in result
        assert "docker" in result


class TestKnowledgeIndex:
    def test_default_values(self):
        ki = KnowledgeIndex()
        assert ki.domains == {}
        assert ki.entries == {}
        assert ki.last_updated == ""

    def test_factory_isolation_domains(self):
        k1 = KnowledgeIndex()
        k2 = KnowledgeIndex()
        k1.domains["cli"] = ["K001", "K002"]
        assert k1.domains["cli"] == ["K001", "K002"]
        assert k2.domains == {}

    def test_factory_isolation_entries(self):
        k1 = KnowledgeIndex()
        k2 = KnowledgeIndex()
        k1.entries["K001"] = {"title": "Test", "domain": "cli"}
        assert k1.entries["K001"]["title"] == "Test"
        assert k2.entries == {}

    def test_json_roundtrip(self):
        ki = KnowledgeIndex(
            domains={"cli": ["K001"], "agent": ["K002"]},
            entries={
                "K001": {"title": "Test", "domain": "cli"},
                "K002": {"title": "Test2", "domain": "agent"},
            },
            last_updated="2026-01-01T00:00:00Z",
        )
        d = asdict(ki)
        result = json.dumps(d)
        assert "cli" in result
        assert "K001" in result
        assert "2026-01-01" in result
        # Verify round-trip preserves structure
        parsed = json.loads(result)
        assert parsed["domains"]["cli"] == ["K001"]
        assert parsed["entries"]["K001"]["title"] == "Test"


class TestMatchLevel:
    def test_match_level_weights(self):
        assert MatchLevel.EXACT.weight == 1.0
        assert MatchLevel.SYNONYM.weight == 0.8
        assert MatchLevel.FUZZY.weight == 0.6
