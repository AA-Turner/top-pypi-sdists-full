"""
agenticstar_platform.audit — 行為監査 (action audit) 台帳モジュール。

エージェント実行系の「行為」イベント (承認/却下、ツール認可、ポリシー違反、キルスイッチ、
A2A 呼び出し等) を append-only 台帳へ記録する純インフラ。課金台帳 (metering) とは
書き込み保証で区別される (approval.* = audit-before-act 同期 / その他 = at-least-once + spill)。

設計正本: agenticai リポジトリ docs/action_audit_design_2026-08-10.md

- 本文非保存: 生値は `canonical_digest()` で SHA-256 化して payload_digest へ。
- DB は `execute_query(query, params) -> {success,data,error}` を持つもの (SDK の DataAccess 等) を渡す。

公開 API:
    ActionAudit                agent_action_audit (行為イベント台帳) の writer
    GatewayActionAudit         llm_gateway_action_audit (LLM Gateway ポリシー判定) writer
    GuardrailAlertWriter       guardrail_alerts (Admin トリアージ・非権威) producer writer
    GuardrailAlertAggregates   guardrail_alert_daily_aggregates (SelfHarm 等の非連結集計)
    ActionAuditWriteError      record_sync 失敗 (audit-before-act 違反 → 行為を中断)
    canonical_digest           任意 payload の SHA-256 digest (本文非保存の片方向化)
    KNOWN_EVENT_TYPES          既知の event_type と意味 (情報提供。強制しない)
    ACTOR_KINDS                actor_kind の閉語彙 (agent / human / system / human_external / unknown)
    reference_keys(**refs)     metadata に入れる相関キー (project_id / run_id / step_id / item_id / tool_call_id / root_execution_id)
    ACTION_AUDIT_DDL 他        ensure_schema() が使う DDL (migration を持たない環境向け)
    SPILL_MARKER               spill ログ行の検索キー
"""
from .action_audit import (
    ACTION_AUDIT_DDL,
    ACTION_AUDIT_INDEXES,
    ACTION_AUDIT_UPGRADE_DDL,
    ACTOR_KINDS,
    KNOWN_EVENT_TYPES,
    SPILL_MARKER,
    ActionAudit,
    ActionAuditWriteError,
    GatewayActionAudit,
    actor_kind_from_type,
    canonical_digest,
    reference_keys,
)
from .guardrail_alerts import (
    GuardrailAlertAggregates,
    GuardrailAlertWriter,
)

__all__ = [
    "ACTOR_KINDS",
    "KNOWN_EVENT_TYPES",
    "ACTION_AUDIT_DDL",
    "ACTION_AUDIT_UPGRADE_DDL",
    "ACTION_AUDIT_INDEXES",
    "actor_kind_from_type",
    "reference_keys",
    "ActionAudit",
    "GatewayActionAudit",
    "GuardrailAlertWriter",
    "GuardrailAlertAggregates",
    "ActionAuditWriteError",
    "canonical_digest",
    "SPILL_MARKER",
]
