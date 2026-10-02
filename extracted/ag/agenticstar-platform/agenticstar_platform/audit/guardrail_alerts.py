"""Guardrail Alerts writer (molt#1415 prop-20260801-005 Phase1-A / autonomous #2084).

`guardrail_alerts`（Admin トリアージ用の非権威的運用ビュー）と
`guardrail_alert_daily_aggregates`（SelfHarm 等の非連結集計）の**公開** writer。
配送保証は行為監査と同じ「bounded FAF + 可観測な欠損」（retry → spill marker 退避 →
shutdown drain。transactional outbox ではない）。権威は行為監査台帳側にある。

PO 決定 (molt#1415 note 1176109) を構造的に強制する:
- **alert 行に利用者 ID 列を持たない**（スキーマに列自体が無い。人物特定は UI/API 不可）
- **SelfHarm を alert 行に載せない**: 表記ゆれ（大小文字・空白・`_`・`-`）を正規化した上で
  detection_types / moderation_categories の**キー・値・ネスト**を走査し、該当があれば
  ValueError（producer バグの同期検出）。SelfHarm-only 検知は行を作らず
  `GuardrailAlertAggregates` の日次集計のみへ（相関 ID なし）
- **行の policy_outcome は 'blocked' のみ**: `allowed_with_safety_response`（SelfHarm
  素通し）は行を作らせず ValueError → 集計 (category=SelfHarm) へ誘導。カテゴリ文字列の
  省略による防波堤回避を outcome レベルで塞ぐ
- 冪等: `event_key` UNIQUE + `ON CONFLICT (event_key) DO NOTHING`（カラム指定）。
  replay は同一行を上書きせず、Admin が変更した lifecycle 状態も巻き戻さない
- 権限分離: ensure_schema が PUBLIC から UPDATE/DELETE を REVOKE（best-effort）。
  Admin BFF role への lifecycle 列 column-level GRANT / producer role の権限は
  デプロイ側 migration の契約。**producer 権限は行と集計で異なる**:
  guardrail_alerts = INSERT のみ / guardrail_alert_daily_aggregates = UPSERT のため
  INSERT + UPDATE(count) + SELECT(count) が必要（ON CONFLICT DO UPDATE が既存 count を
  参照するため SELECT も必須。INSERT-only 契約は行テーブル側だけに適用する）
- moderation_categories / 集計 severity は**カテゴリ別の実測値**（producer は
  ContentModerationResult.categories / categories_analysis の実測 severity を渡す。
  threshold を severity として代用しないこと）

集計テーブルの注意: at-least-once 配送のため retry で**二重加算があり得る近似値**。
トレンド監視・サマリーカード用であり、課金・規制報告・自動制御に使わないこと。
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from typing import Any, Optional

from .action_audit import _BaseActionAudit, _REVOKE_TEMPLATE, logger

SOURCE_SURFACES = ("agent_executor", "llm_gateway", "agent_worker")
# policy_category: regex / LLM semantic 層の「どの制御境界・攻撃方式に該当したか」の
# 閉語彙（molt#1415 詳細化）。**攻撃方式のみ**を表す — 人・話題・内容の分類
# （医療/精神状態等）や自由文・rule 名・ファイル名を値にしてはならない（倫理不変条件）。
# 語彙追加は SDK / DB CHECK (dbmigration) / admin UI の三点同時変更。
POLICY_CATEGORIES = (
    "prompt_injection",
    "system_prompt_extraction",
    "implementation_access",
    "credential_request",
    "file_system_access",
    "security_bypass",
    "custom_policy",
    "unclassified",
)
# 行に許可する outcome は blocked のみ（allowed_with_safety_response = SelfHarm 素通しは
# PO 決定により行を作らない。集計 category=SelfHarm が唯一の記録先）
ROW_POLICY_OUTCOMES = ("blocked",)
# event_key の decision_point（入力 block と出力 block を別イベントとして分離する）
DECISION_POINTS = ("input", "output")
# Azure FourSeverityLevels（content カテゴリの有効値）。0 は集計の jailbreak 専用
# sentinel（"not_applicable"。Safe=0 の検知はそもそも集計対象にしない）
CONTENT_SEVERITIES = (2, 4, 6)
CONTENT_CATEGORIES = ("Hate", "Sexual", "SelfHarm", "Violence")
SHIELD_CATEGORIES = ("jailbreak_attack",)
AGGREGATE_CATEGORIES = CONTENT_CATEGORIES + SHIELD_CATEGORIES

_FORBIDDEN_NORMALIZED = ("selfharm",)
_NORM_RE = re.compile(r"[\s_\-]+")


def _normalize(label: Any) -> str:
    return _NORM_RE.sub("", str(label).casefold())


def _contains_forbidden(value: Any) -> bool:
    """キー・値・ネスト（list/dict）を再帰走査し SelfHarm 表記ゆれを検出する。"""
    if value is None:
        return False
    if isinstance(value, dict):
        return any(_contains_forbidden(k) or _contains_forbidden(v)
                   for k, v in value.items())
    if isinstance(value, (list, tuple, set)):
        return any(_contains_forbidden(v) for v in value)
    return _normalize(value) in _FORBIDDEN_NORMALIZED


GUARDRAIL_ALERTS_DDL = """
CREATE TABLE IF NOT EXISTS guardrail_alerts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_key varchar(255) UNIQUE NOT NULL,
    schema_version smallint NOT NULL DEFAULT 1,
    detected_at timestamptz NOT NULL DEFAULT now(),
    source_surface varchar(32) NOT NULL
        CHECK (source_surface IN ('agent_executor', 'llm_gateway', 'agent_worker')),
    provider varchar(64) NOT NULL DEFAULT 'azure_content_safety',
    conversation_id varchar(64),
    message_id varchar(64),
    request_id varchar(128),
    tenant_id varchar(64),
    -- PO 決定 (molt#1415): 利用者の識別子列は存在しない（人物特定は UI/API 不可）
    detection_types jsonb NOT NULL DEFAULT '[]'::jsonb,
    prompt_shield_origin jsonb,
    moderation_categories jsonb,
    moderation_threshold smallint,
    -- Phase 1 は blocked のみ（SelfHarm 素通しは集計側。Phase 2 で緩和する場合は migration）
    policy_outcome varchar(40) NOT NULL CHECK (policy_outcome IN ('blocked')),
    response_template_code varchar(64),
    policy_source varchar(64) NOT NULL,
    -- regex / LLM semantic 層の攻撃方式分類（閉語彙）。NULL = その検知種別に分類が
    -- 存在しない（CS/Prompt Shield 行）または旧 producer 由来の「未取得」
    policy_category varchar(40)
        CHECK (policy_category IS NULL OR policy_category IN (
            'prompt_injection', 'system_prompt_extraction', 'implementation_access',
            'credential_request', 'file_system_access', 'security_bypass',
            'custom_policy', 'unclassified')),
    content_sha256 char(64),
    -- Phase 1 固定: 本文抜粋なし（prop-20260716-004 の本文非保持契約）
    content_available boolean NOT NULL DEFAULT false CHECK (content_available IS FALSE),
    status varchar(20) NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'escalated', 'closed', 'false_positive')),
    assignee_user_id varchar(64),
    resolution_code varchar(40),
    resolution_note_redacted varchar(1000),
    resolved_at timestamptz,
    resolved_by varchar(64),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
)
"""

GUARDRAIL_ALERTS_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_guardrail_alerts_status_detected "
    "ON guardrail_alerts (status, detected_at DESC)",
    "CREATE INDEX IF NOT EXISTS idx_guardrail_alerts_surface_detected "
    "ON guardrail_alerts (source_surface, detected_at DESC)",
)

GUARDRAIL_ALERT_AGGREGATES_DDL = """
CREATE TABLE IF NOT EXISTS guardrail_alert_daily_aggregates (
    day date NOT NULL,
    source_surface varchar(32) NOT NULL,
    category varchar(32) NOT NULL,
    severity smallint NOT NULL DEFAULT 0,
    count bigint NOT NULL DEFAULT 0,
    PRIMARY KEY (day, source_surface, category, severity)
)
"""

_ALERT_INSERT_SQL = (
    "INSERT INTO guardrail_alerts (event_key, schema_version, detected_at, source_surface, "
    "provider, conversation_id, message_id, request_id, tenant_id, detection_types, "
    "prompt_shield_origin, moderation_categories, moderation_threshold, policy_outcome, "
    "response_template_code, policy_source, policy_category, content_sha256, content_available) "
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb, $11::jsonb, $12::jsonb, "
    "$13, $14, $15, $16, $17, $18, $19) "
    "ON CONFLICT (event_key) DO NOTHING"
)

_AGGREGATE_UPSERT_SQL = (
    "INSERT INTO guardrail_alert_daily_aggregates (day, source_surface, category, severity, count) "
    "VALUES ($1, $2, $3, $4, 1) "
    "ON CONFLICT (day, source_surface, category, severity) "
    "DO UPDATE SET count = guardrail_alert_daily_aggregates.count + 1"
)


class GuardrailAlertWriter(_BaseActionAudit):
    """`guardrail_alerts` の公開 producer writer（INSERT のみ / 冪等 / FAF）。

    record_nowait(...) を応答パス外で呼ぶ。書けない場合は spill marker
    (`action_audit_spill guardrail_alerts`) へ退避され応答を壊さない。

    event_key = ``v2:{surface}:{correlation_kind}:{correlation}:{decision_point}:{outcome}``
    - correlation は request_id > message_id > conversation_id の優先で採用し、
      **どの種別を使ったかを correlation_kind として key に含める**（種別間衝突防止）
    - decision_point（input/output）で同一リクエスト内の別段 block を分離する
    - 同 key の重複 = 同一 incident の replay とみなし DO NOTHING（情報欠落ではない）
    """

    _INSERT_SQL = _ALERT_INSERT_SQL
    _TABLE = "guardrail_alerts"

    async def ensure_schema(self) -> None:
        await self._exec_checked(GUARDRAIL_ALERTS_DDL)
        for ddl in GUARDRAIL_ALERTS_INDEXES:
            await self._exec_checked(ddl)
        await self._exec_checked(GUARDRAIL_ALERT_AGGREGATES_DDL)
        # 権限分離の既定値: PUBLIC から UPDATE/DELETE を剥奪（既存 writer と同じ best-effort。
        # Admin BFF role への lifecycle 列 GRANT はデプロイ側 migration が明示的に行う）
        for table in (self._TABLE, "guardrail_alert_daily_aggregates"):
            try:
                await self._exec_checked(_REVOKE_TEMPLATE.format(table=table))
            except Exception as e:
                logger.info("revoke skipped on %s (non-owner?): %s", table, e)

    def _build_row(self, *, source_surface: str, policy_outcome: str, policy_source: str,
                   decision_point: str = "input",
                   request_id: Optional[str] = None, conversation_id: Optional[str] = None,
                   message_id: Optional[str] = None, tenant_id: Optional[str] = None,
                   detection_types: Optional[list] = None,
                   prompt_shield_origin: Optional[dict] = None,
                   moderation_categories: Optional[dict] = None,
                   moderation_threshold: Optional[int] = None,
                   response_template_code: Optional[str] = None,
                   provider: str = "azure_content_safety",
                   content_sha256: Optional[str] = None,
                   policy_category: Optional[str] = None,
                   detected_at: Optional[datetime] = None) -> dict:
        if source_surface not in SOURCE_SURFACES:
            raise ValueError(f"invalid source_surface: {source_surface}")
        if policy_outcome not in ROW_POLICY_OUTCOMES:
            # allowed_with_safety_response (SelfHarm 素通し) は行を作らない PO 決定。
            # 集計 (GuardrailAlertAggregates, category=SelfHarm) を使うこと
            raise ValueError(
                f"policy_outcome '{policy_outcome}' is not allowed on rows "
                "(rows are blocked-only; SelfHarm passthrough is aggregate-only)")
        if decision_point not in DECISION_POINTS:
            raise ValueError(f"invalid decision_point: {decision_point}")
        if not policy_source:
            raise ValueError("policy_source is required")
        # policy_category は閉語彙のみ（自由文・rule 名・自作ラベルの流入を同期検出。
        # 倫理不変条件: 攻撃方式の語彙以外を行に載せない）
        if policy_category is not None and policy_category not in POLICY_CATEGORIES:
            raise ValueError(
                f"invalid policy_category: {policy_category!r} "
                f"(closed vocabulary: {POLICY_CATEGORIES})")
        # PO 決定の防波堤: SelfHarm（表記ゆれ・ネスト・値を含む）を相関 ID 付き行に
        # 載せる producer はバグとして同期検出
        if (_contains_forbidden(detection_types) or _contains_forbidden(moderation_categories)
                or _contains_forbidden(prompt_shield_origin) or _contains_forbidden(policy_category)):
            raise ValueError(
                "SelfHarm must not appear on guardrail_alerts rows "
                "(SelfHarm is recorded in the aggregates only)")
        if request_id:
            kind, correlation = "request", request_id
        elif message_id:
            kind, correlation = "message", message_id
        elif conversation_id:
            kind, correlation = "conversation", conversation_id
        else:
            raise ValueError("at least one correlation id is required for event_key")
        if detected_at is None:
            detected_at = datetime.now(timezone.utc)
        elif detected_at.tzinfo is None:
            raise ValueError("detected_at must be timezone-aware")
        return {
            "event_key": (f"v2:{source_surface}:{kind}:{correlation}:"
                          f"{decision_point}:{policy_outcome}"),
            "schema_version": 1,
            "detected_at": detected_at,
            "source_surface": source_surface,
            "provider": provider,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "request_id": request_id,
            "tenant_id": tenant_id,
            "detection_types": json.dumps(list(detection_types or [])),
            "prompt_shield_origin": json.dumps(prompt_shield_origin) if prompt_shield_origin else None,
            "moderation_categories": json.dumps(moderation_categories) if moderation_categories else None,
            "moderation_threshold": moderation_threshold,
            "policy_outcome": policy_outcome,
            "response_template_code": response_template_code,
            "policy_source": policy_source,
            "policy_category": policy_category,
            "content_sha256": content_sha256,
            "content_available": False,
        }

    def _params(self, row: dict) -> tuple:
        return (row["event_key"], row["schema_version"], row["detected_at"],
                row["source_surface"], row["provider"], row["conversation_id"],
                row["message_id"], row["request_id"], row["tenant_id"],
                row["detection_types"], row["prompt_shield_origin"],
                row["moderation_categories"], row["moderation_threshold"],
                row["policy_outcome"], row["response_template_code"], row["policy_source"],
                row["policy_category"], row["content_sha256"], row["content_available"])


class GuardrailAlertAggregates(_BaseActionAudit):
    """`guardrail_alert_daily_aggregates` の公開 writer（UPSERT increment / FAF）。

    SelfHarm-only 検知（素通し含む）の**唯一の**記録先。相関 ID を一切受け取らない
    （引数に存在しない = 非連結が構造的に保証される）。

    severity 規則: content カテゴリ (Hate/Sexual/SelfHarm/Violence) は Azure
    FourSeverityLevels の検知値 (2/4/6)。jailbreak_attack は boolean 判定のため
    severity=0 固定（"not_applicable" の sentinel。Safe=0 の検知は集計対象外なので
    衝突しない）。値は at-least-once 由来の二重加算があり得る近似値。
    """

    _INSERT_SQL = _AGGREGATE_UPSERT_SQL
    _TABLE = "guardrail_alert_daily_aggregates"

    async def ensure_schema(self) -> None:
        await self._exec_checked(GUARDRAIL_ALERT_AGGREGATES_DDL)

    def _build_row(self, *, source_surface: str, category: str, severity: int = 0,
                   day: Optional[date] = None) -> dict:
        if source_surface not in SOURCE_SURFACES:
            raise ValueError(f"invalid source_surface: {source_surface}")
        if category in CONTENT_CATEGORIES:
            if severity not in CONTENT_SEVERITIES:
                raise ValueError(
                    f"content category '{category}' requires severity in {CONTENT_SEVERITIES}")
        elif category in SHIELD_CATEGORIES:
            if severity != 0:
                raise ValueError(f"shield category '{category}' requires severity=0 (n/a)")
        else:
            raise ValueError(f"invalid category: {category}")
        if day is None:
            day = datetime.now(timezone.utc).date()
        return {
            "day": day,
            "source_surface": source_surface,
            "category": category,
            "severity": severity,
        }

    def _params(self, row: dict) -> tuple:
        return (row["day"], row["source_surface"], row["category"], row["severity"])
