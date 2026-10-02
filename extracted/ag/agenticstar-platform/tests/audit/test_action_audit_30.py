"""ActionAudit の 3.0 拡張（R-B2 / R-B4 / R-B6、instructions/00 §4）。"""
import asyncio
import hashlib
import json

import pytest

from agenticstar_platform.audit import (
    ACTOR_KINDS,
    ActionAudit,
    actor_kind_from_type,
    reference_keys,
)
from agenticstar_platform.audit.action_audit import _ACTION_INSERT_SQL_LEGACY, _row_hash


class _DB:
    def __init__(self, fail_new_columns=False):
        self.calls = []
        self.fail_new_columns = fail_new_columns

    async def execute_query(self, query, params=()):
        self.calls.append((query, params))
        if self.fail_new_columns and "actor_kind" in query:
            return {"success": False, "error": 'column "actor_kind" of relation "agent_action_audit" does not exist'}
        return {"success": True}


def _audit(db=None, **kw):
    return ActionAudit(db=db or _DB(), source="worker", system_version="img-1", **kw)


def test_new_columns_and_actor_kind_mapping():
    a = _audit(agent_ref="agent:react")
    row = a._build_row(event_type="tool.effect", actor_type="agent", decision="ok", resource="gitlab",
                       project_id="0f1e2d3c-4b5a-6978-8a9b-0c1d2e3f4a5b", root_execution_id="conv-1",
                       source_event_id="webhook:evt-1", metadata=reference_keys(tool_call_id="c1", run_id=None))
    assert row["actor_kind"] == "agent" and row["actor_ref"] == "agent:react"   # 自動付与
    assert row["metadata"] == {"tool_call_id": "c1"}
    params = a._params(row)
    assert len(params) == 23 and params[19:] == ("agent", "0f1e2d3c-4b5a-6978-8a9b-0c1d2e3f4a5b", "conv-1", "webhook:evt-1")
    for t, k in (("human", "human"), ("user", "human"), ("system", "system"), ("weird", "unknown")):
        assert actor_kind_from_type(t) == k
    row = a._build_row(event_type="tool.access", actor_type="human", decision="allow", actor_ref="u1")
    assert row["actor_kind"] == "human" and row["project_id"] is None
    assert set(ACTOR_KINDS) == {"agent", "human", "system", "human_external", "unknown"}


def test_validation_rules():
    a = _audit()
    with pytest.raises(ValueError):
        a._build_row(event_type="gate.resolved", actor_type="human", decision="approved")     # actor 必須
    with pytest.raises(ValueError):
        a._build_row(event_type="policy.changed", actor_type="system", decision="ok")
    with pytest.raises(ValueError):
        a._build_row(event_type="x", actor_type="agent", decision="ok", actor_kind="robot")
    with pytest.raises(ValueError):
        a._build_row(event_type="x", actor_type="agent", decision="ok", source_event_id="bad id with spaces")
    with pytest.raises(ValueError):
        a._build_row(event_type="x", actor_type="agent", decision="ok", project_id="not-a-uuid")
    row = a._build_row(event_type="gate.resolved", actor_type="system", decision="proceeded", actor_ref="system:gate-expiry")
    assert row["actor_kind"] == "system"


def test_row_hash_backward_compatible_and_spec():
    a = _audit()
    row = a._build_row(event_type="tool.access", actor_type="agent", decision="allow", actor_ref="agent:x")
    legacy = {k: v for k, v in row.items() if k not in ("row_hash", "actor_kind", "project_id", "root_execution_id", "source_event_id")}
    assert _row_hash({**legacy, "actor_kind": "agent"}) == row["row_hash"]   # None 列は hash に影響しない
    canon = json.dumps({k: v for k, v in row.items() if k != "row_hash" and v is not None},
                       sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    assert hashlib.sha256(canon.encode("utf-8")).hexdigest() == row["row_hash"]


def test_legacy_ddl_fallback_once_recomputes_row_hash():
    db = _DB(fail_new_columns=True)
    a = _audit(db=db)
    assert asyncio.run(a.record(event_type="tool.access", actor_type="agent", decision="allow", metadata={"k": "v"})) is True
    assert "actor_kind" in db.calls[0][0] and db.calls[1][0] == _ACTION_INSERT_SQL_LEGACY
    legacy = db.calls[1][1]
    assert len(legacy) == 19
    # legacy 行の row_hash は「実際に保存する 18 列」から再計算されている (新列込み hash ではない)
    cols = ("source", "event_type", "actor_type", "actor_ref", "on_behalf_of_ref", "resource", "action", "decision",
            "reason", "policy_id", "policy_version", "execution_id", "conversation_id", "message_id", "request_id",
            "payload_digest", "metadata", "system_version")
    fields = dict(zip(cols, legacy[:18])); fields["metadata"] = json.loads(fields["metadata"])
    assert legacy[18] == _row_hash(fields) and legacy[18] != db.calls[0][1][18]
    assert asyncio.run(a.record(event_type="tool.access", actor_type="agent", decision="deny")) is True
    assert db.calls[2][0] == _ACTION_INSERT_SQL_LEGACY  # 以後は最初から legacy


def test_other_does_not_exist_errors_do_not_downgrade():
    class _DBFn:
        def __init__(self): self.calls = []
        async def execute_query(self, q, p=()):
            self.calls.append(q)
            return {"success": False, "error": "function normalize_project_id(text) does not exist"}
    db = _DBFn(); a = _audit(db=db)
    assert asyncio.run(a.record(event_type="tool.access", actor_type="agent", decision="allow")) is False  # spill
    assert all("actor_kind" in q for q in db.calls) and a._legacy_insert is False
    # asyncpg 風の例外 (sqlstate 付き) は 42703 のときだけ降格
    class _Exc(Exception):
        sqlstate = "42883"
    class _DBExc:
        def __init__(self): self.calls = []
        async def execute_query(self, q, p=()):
            self.calls.append(q); raise _Exc('column "actor_kind" of relation "agent_action_audit" does not exist')
    db = _DBExc(); a = _audit(db=db)
    asyncio.run(a.record(event_type="tool.access", actor_type="agent", decision="allow"))
    assert a._legacy_insert is False


def test_project_id_is_lowercased_and_numbers_normalized():
    a = _audit()
    row = a._build_row(event_type="x", actor_type="agent", decision="ok", project_id="0F1E2D3C-4B5A-6978-8A9B-0C1D2E3F4A5B",
                       metadata={"ratio": 1.5, "n": 3, "big": 2**60, "ok": True, "nested": {"f": 2.0, "l": [1, 1.0]}})
    assert row["project_id"] == "0f1e2d3c-4b5a-6978-8a9b-0c1d2e3f4a5b"
    assert row["metadata"] == {"ratio": "1.5", "n": 3, "big": str(2**60), "ok": True, "nested": {"f": "2.0", "l": [1, "1.0"]}}


def test_new_ddl_uses_23_params():
    db = _DB()
    a = _audit(db=db)
    asyncio.run(a.record(event_type="plan.revised", actor_type="agent", decision="plan",
                         root_execution_id="conv-1", metadata={"kind": "plan"}))
    q, p = db.calls[0]
    assert "actor_kind, project_id, root_execution_id, source_event_id" in q and len(p) == 23
    assert p[19] == "agent" and p[21] == "conv-1"


def test_circular_metadata_still_records_row():
    a = _audit()
    loop = {}
    loop["self"] = loop
    row = a._build_row(event_type="x", actor_type="agent", decision="ok", metadata=loop)
    assert row["metadata"] == {"unserializable": True}


def test_ensure_schema_ddl_contains_30_columns_and_indexes():
    from agenticstar_platform.audit import (
        ACTION_AUDIT_DDL,
        ACTION_AUDIT_INDEXES,
        ACTION_AUDIT_UPGRADE_DDL,
        KNOWN_EVENT_TYPES,
    )
    from agenticstar_platform.audit.action_audit import _NEW_30_COLUMNS

    for col in _NEW_30_COLUMNS:
        assert col in ACTION_AUDIT_DDL and col in ACTION_AUDIT_UPGRADE_DDL
    joined = " ".join(ACTION_AUDIT_INDEXES)
    assert "UNIQUE INDEX IF NOT EXISTS ux_agent_action_audit_source_event" in joined
    assert "(root_execution_id, occurred_at, id)" in joined and "(project_id) WHERE project_id IS NOT NULL" in joined
    assert "ADD COLUMN IF NOT EXISTS" in ACTION_AUDIT_UPGRADE_DDL
    # 語彙表は 3.0 のイベント名を含む (強制はしないので writer は未知の名前も通す)
    for name in ("tool.access", "tool.invoked", "tool.effect", "data.access", "context.manifest", "plan.revised",
                 "hitl.requested", "completion.stale", "delivery.unconfirmed", "runtime.tool.timeout"):
        assert name in KNOWN_EVENT_TYPES and KNOWN_EVENT_TYPES[name]
    # 用途別のイベント (検証専用) は語彙表に持たない (3.0req 指示書 23。未知の名前として書くことはできる)
    assert "verification.completed" not in KNOWN_EVENT_TYPES
    a = _audit()
    row = a._build_row(event_type="my.custom.event", actor_type="agent", decision="ok")
    assert row["event_type"] == "my.custom.event"


def test_ensure_schema_runs_create_then_upgrade_then_indexes():
    db = _DB()
    a = _audit(db=db)
    asyncio.run(a.ensure_schema())
    sqls = [q for q, _ in db.calls]
    assert sqls[0].lstrip().startswith("CREATE TABLE IF NOT EXISTS agent_action_audit")
    assert sqls[1].startswith("ALTER TABLE agent_action_audit ADD COLUMN IF NOT EXISTS actor_kind")
    assert any("ux_agent_action_audit_source_event" in q for q in sqls)


def test_source_is_a_component_label():
    with pytest.raises(ValueError) as ei:
        ActionAudit(db=_DB(), source="  ")
    assert "component" in str(ei.value) and "worker" not in str(ei.value)
    a = ActionAudit(db=_DB(), source=" my-agent ")
    row = a._build_row(event_type="tool.effect", actor_type="agent", decision="ok")
    assert row["source"] == "my-agent" and row["actor_ref"] == "agent:my-agent"


def test_ensure_schema_restores_new_insert_after_legacy_fallback():
    """旧表で旧 INSERT に落ちた同じインスタンスが、ensure_schema で列が揃った後は新 INSERT (23 params) に戻る。"""
    db = _DB(fail_new_columns=True)
    a = _audit(db=db)
    asyncio.run(a.record(event_type="tool.effect", actor_type="agent", decision="ok", source_event_id="evt-1"))
    assert a._legacy_insert is True
    db.fail_new_columns = False  # ensure_schema が列を足した後の DB
    asyncio.run(a.ensure_schema())
    assert a._legacy_insert is False
    asyncio.run(a.record(event_type="tool.effect", actor_type="agent", decision="ok", source_event_id="evt-2"))
    last_insert = [c for c in db.calls if c[0].startswith("INSERT INTO agent_action_audit")][-1]
    assert len(last_insert[1]) == 23 and last_insert[1][-1] == "evt-2"


def test_known_event_meanings_do_not_use_internal_component_names():
    from agenticstar_platform.audit import KNOWN_EVENT_TYPES

    text = " ".join(KNOWN_EVENT_TYPES.values())
    assert "the front" not in text and "cli-api" not in text and "R-" not in text
