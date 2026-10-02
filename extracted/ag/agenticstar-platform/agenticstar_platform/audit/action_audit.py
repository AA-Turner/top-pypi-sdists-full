"""
行為監査 (action audit) 台帳 writer。

純インフラ: エージェント実行系の「行為」イベント (承認/却下、ツール認可、ポリシー違反、
キルスイッチ、A2A 呼び出し等) を append-only 台帳へ記録する。エージェントロジック非依存 ─
どのコンポーネント (自作 agent、platform のサービス) からも同じ形で使える。

設計正本: agenticai リポジトリ docs/action_audit_design_2026-08-10.md

課金台帳 (metering) との違い = 書き込み保証:
  - ``record()``      … at-least-once。bounded retry 後も失敗したら **spill マーカー付き
                        構造化ログ** に全文を退避 (Loki から手動 reconcile 可能) し、決して送出しない。
  - ``record_sync()`` … audit-before-act。書けなければ ``ActionAuditWriteError`` を送出する。
                        承認イベント (approval.*) は「監査に書けない承認は成立しない」を
                        不変条件とするため、必ずこちらを使う。
  - ``record_nowait()`` … record() を fire-and-forget task 化 (strong ref 保持)。
                        ツール認可のようなホットパスでレイテンシを加えないために使う。

本文非保存: プロンプト/ツール引数/出力の生値は台帳に入れない。``canonical_digest()`` で
SHA-256 digest 化して ``payload_digest`` に渡すこと。

DB は duck-typed: ``execute_query(query, params) -> {"success", "data", "error"}`` を持つもの
(`agenticstar_platform.db.DataAccess` / `PostgreSQLManager`、および同契約の実装) をそのまま渡せる。
戻り値 dict の ``success=False`` も失敗として扱う (例外を投げない DB 実装対策)。

使用例::

    from agenticstar_platform.audit import ActionAudit

    audit = ActionAudit(db=data_access, source="worker", system_version=image_tag)
    await audit.ensure_schema()                     # 台帳が無ければ作成 (冪等)
    audit.record_nowait(                            # ツール認可 (ホットパス)
        event_type="tool.access", actor_type="agent", decision="deny",
        resource="bash", action="execute", reason="blocked_path",
        conversation_id=cid, execution_id=eid,
    )
    await audit.record_sync(                        # 承認 (audit-before-act)
        event_type="approval.granted", actor_type="human", actor_ref=approver_id,
        decision="granted", resource=tool_name, conversation_id=cid,
    )
    await audit.aclose()                            # 終了時: pending task を待つ
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# spill 行の検索キー (Loki: {app=...} |= "action_audit_spill")
SPILL_MARKER = "action_audit_spill"


class ActionAuditWriteError(Exception):
    """record_sync() が台帳へ書けなかった (audit-before-act 違反となるため呼び出し元は行為を中断する)。"""


def canonical_digest(payload: Any) -> str | None:
    """任意 payload の SHA-256 digest (canonical JSON)。生値を台帳へ入れないための片方向化。

    None はそのまま None (digest 対象なし)。非 JSON 型は str() へ degrade。
    """
    if payload is None:
        return None
    try:
        canon = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        canon = str(payload)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _row_hash(fields: dict) -> str:
    """行内容の SHA-256 (canonical JSON、None 除外)。occurred_at/id は DB 採番のため対象外。
    日次アンカー (改ざん検知) は DB 側で id, occurred_at, row_hash を連結して行うため、
    ここは「クライアントが送った内容」の完全性のみを固定する。

    正規化仕様 (ROW_HASH_SPEC.md、front / admin の Node 実装と同じ値を出す contract test 用):
      1. 対象 = row_hash 以外の全列 (source, event_type, actor_type, actor_ref, on_behalf_of_ref,
         resource, action, decision, reason, policy_id, policy_version, execution_id,
         conversation_id, message_id, request_id, payload_digest, metadata, system_version,
         actor_kind, project_id, root_execution_id, source_event_id)
      2. 値が None (JSON null) のキーは除外。空文字・空 dict は残す
      3. JSON: キーを再帰的に昇順ソート、区切りは "," と ":" (空白なし)、ensure_ascii=False
         (非 ASCII はそのまま UTF-8)、非 JSON 型は str() に落とす。metadata の数値は
         _normalize_numbers で安全整数以外を文字列化済み
      4. UTF-8 バイト列の SHA-256、小文字 hex 64 桁
    """
    canon = json.dumps({k: v for k, v in fields.items() if v is not None},
                       sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# スキーマ (設計書 §4.1 / §5.1。既存環境では ensure_schema 不要)
# ---------------------------------------------------------------------------
# ensure_schema() が作る表 (migration を持たない環境向け。1.0.0a2 で 3.0 の 4 列と index を含む形に更新)。
# migration 管理の環境 (ASTER 本体) では表は partition 化されているため、この DDL は使わず migration が正。
ACTION_AUDIT_DDL = """
CREATE TABLE IF NOT EXISTS agent_action_audit (
    id                bigint       GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    occurred_at       timestamptz  NOT NULL DEFAULT now(),
    source            text         NOT NULL,
    event_type        text         NOT NULL,
    actor_type        text         NOT NULL,
    actor_ref         text,
    on_behalf_of_ref  text,
    resource          text,
    action            text,
    decision          text         NOT NULL,
    reason            text,
    policy_id         text,
    policy_version    text,
    execution_id      text,
    conversation_id   text,
    message_id        text,
    request_id        text,
    payload_digest    text,
    metadata          jsonb        NOT NULL DEFAULT '{}'::jsonb,
    system_version    text,
    row_hash          text         NOT NULL,
    actor_kind        varchar(24),
    project_id        uuid,
    root_execution_id text,
    source_event_id   varchar(160)
)
"""
#: 既存の表に 3.0 の列が無いとき (旧 SDK が作った表) に足す。ADD COLUMN IF NOT EXISTS は冪等
ACTION_AUDIT_UPGRADE_DDL = (
    "ALTER TABLE agent_action_audit"
    " ADD COLUMN IF NOT EXISTS actor_kind varchar(24),"
    " ADD COLUMN IF NOT EXISTS project_id uuid,"
    " ADD COLUMN IF NOT EXISTS root_execution_id text,"
    " ADD COLUMN IF NOT EXISTS source_event_id varchar(160)"
)
ACTION_AUDIT_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_action_audit_conv_ts  ON agent_action_audit (conversation_id, occurred_at)",
    "CREATE INDEX IF NOT EXISTS idx_action_audit_exec     ON agent_action_audit (execution_id)",
    "CREATE INDEX IF NOT EXISTS idx_action_audit_type_ts  ON agent_action_audit (event_type, occurred_at)",
    "CREATE INDEX IF NOT EXISTS idx_action_audit_actor_ts ON agent_action_audit (actor_ref, occurred_at) WHERE actor_ref IS NOT NULL",
    # 3.0: 外部イベントの重複除去 (partition 化していない表なので partial UNIQUE が作れる)、project / root の索引
    "CREATE UNIQUE INDEX IF NOT EXISTS ux_agent_action_audit_source_event"
    " ON agent_action_audit (source_event_id) WHERE source_event_id IS NOT NULL",
    "CREATE INDEX IF NOT EXISTS ix_agent_action_audit_project_id"
    " ON agent_action_audit (project_id) WHERE project_id IS NOT NULL",
    "CREATE INDEX IF NOT EXISTS ix_agent_action_audit_root_exec"
    " ON agent_action_audit (root_execution_id, occurred_at, id)",
)

GATEWAY_ACTION_AUDIT_DDL = """
CREATE TABLE IF NOT EXISTS llm_gateway_action_audit (
    id                  bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    occurred_at         timestamptz NOT NULL DEFAULT now(),
    virtual_key_id      text,
    virtual_key_hash    text,
    request_id          text,
    external_request_id text,
    api_flavor          text,
    event_type          text NOT NULL,
    decision            text NOT NULL,
    reason              text,
    model_name          text,
    resolved_model      text,
    detail_digest       text,
    metadata            jsonb NOT NULL DEFAULT '{}'::jsonb,
    system_version      text,
    row_hash            text NOT NULL
)
"""

GATEWAY_ACTION_AUDIT_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_gw_action_vkey_ts ON llm_gateway_action_audit (virtual_key_id, occurred_at)",
    "CREATE INDEX IF NOT EXISTS idx_gw_action_type_ts ON llm_gateway_action_audit (event_type, occurred_at)",
)

# append-only 強制。非 owner ロールでは失敗しうるため ensure_schema では best-effort 適用
_REVOKE_TEMPLATE = "REVOKE UPDATE, DELETE ON {table} FROM PUBLIC"

# 3.0 (R-B2 / R-B4 / R-B6): actor_kind / project_id / root_execution_id / source_event_id を追加
# (dbmigration 01 A-8。expand 段は nullable)。旧 DDL の環境では 3.0 列の UndefinedColumn を検出して
# 下の _ACTION_INSERT_SQL_LEGACY に自動で落ちる (新 SDK × 旧 DB でも監査を失わない)
_ACTION_INSERT_SQL = (
    "INSERT INTO agent_action_audit "
    "(source, event_type, actor_type, actor_ref, on_behalf_of_ref, resource, action, "
    " decision, reason, policy_id, policy_version, execution_id, conversation_id, "
    " message_id, request_id, payload_digest, metadata, system_version, row_hash, "
    " actor_kind, project_id, root_execution_id, source_event_id) "
    "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17::jsonb,$18,$19,"
    "$20,$21::uuid,$22,$23)"
)
_ACTION_INSERT_SQL_LEGACY = (
    "INSERT INTO agent_action_audit "
    "(source, event_type, actor_type, actor_ref, on_behalf_of_ref, resource, action, "
    " decision, reason, policy_id, policy_version, execution_id, conversation_id, "
    " message_id, request_id, payload_digest, metadata, system_version, row_hash) "
    "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17::jsonb,$18,$19)"
)
_NEW_30_COLUMNS = ("actor_kind", "project_id", "root_execution_id", "source_event_id")
_MISSING_COLUMN_RE = re.compile(r'column "([A-Za-z_]+)"(?: of relation "agent_action_audit")? does not exist')

#: 既知の event_type の語彙 (情報提供。writer は強制しない。読み手 = 可視化側が同じ名前で集計する)。
#: 値は「誰が / どの段階で書くか」の短い説明
KNOWN_EVENT_TYPES: dict[str, str] = {
    # tool の統制 (interceptor / 認可)
    "tool.access": "tool call denied or allowed by policy (decision = allow | deny, reason = policy reason code)",
    "tool.invoked": "a mutating tool call started (paired with tool.effect by tool_call_id in metadata)",
    "tool.effect": "a mutating tool call finished (decision = ok | failed | error | unknown; resource ids in metadata)",
    # 判断・入力の来歴
    "context.manifest": "the inputs the agent saw before its first decision (digests, not bodies)",
    "plan.revised": "the agent's plan / replan / final decision (digests and references; the body itself is not stored here)",
    "data.access": "data read or written (store, op, ref, digest, ids; never the content)",
    # 人との接点
    "hitl.requested": "the agent asked for a human (action = question | confirmation | choice | gate)",
    "approval.granted": "a human granted an approval (actor_ref required; write before acting)",
    "approval.denied": "a human denied an approval (actor_ref required)",
    "gate.resolved": "a workflow gate was resolved: a human decision, or a system outcome such as expiry (written by the workflow host)",
    # 完了
    "completion.stale": "a late or obsolete completion attempt was rejected (the execution was already terminal or superseded)",
    # 配信・実行時
    "delivery.unconfirmed": "a terminal notification was sent but not acknowledged",
    "delivery.failed": "a terminal notification could not be delivered",
    "delivery.acked": "a terminal notification was acknowledged (written by the receiver)",
    "runtime.checkpoint.saved": "a run checkpoint was persisted",
    "runtime.tool.timeout": "a tool call hit its timeout",
    "runtime.llm.retry": "an LLM call was retried",
    "kill_switch.triggered": "the run was stopped by the kill switch",
    "run_checkpoint.resumed": "the run resumed from a checkpoint",
}

#: actor_kind の閉語彙。agent = 自律エージェント (actor_ref = agent の識別子)、human = 人 (actor_ref = user id)、
#: system = 基盤の自動処理 (固定の actor_ref)、human_external = 外部システム上の人 (ext:<connector>:<id>)、
#: unknown = 対応付けできない機械 actor
ACTOR_KINDS = ("agent", "human", "system", "human_external", "unknown")
_ACTOR_TYPE_TO_KIND = {
    "agent": "agent", "assistant": "agent", "worker": "agent",
    "human": "human", "user": "human", "approver": "human",
    "system": "system", "scheduler": "system", "policy": "system",
}
#: actor (人 / system の識別子) が必須の event_type 接頭辞 (決定の主体が必ず要るイベント)
_ACTOR_REQUIRED_PREFIXES = (
    "approval.", "gate.resolved", "content.deleted", "forensic.", "policy.changed",
    "item.quarantine_released", "workitem.",
)
_SOURCE_EVENT_ID_RE = re.compile(r"^[A-Za-z0-9_.:@+\-]{1,160}$")
_UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def actor_kind_from_type(actor_type: str | None) -> str:
    """互換期間の写像: 既存 writer が渡す actor_type から actor_kind を決める (未知は unknown)。"""
    return _ACTOR_TYPE_TO_KIND.get((actor_type or "").strip().lower(), "unknown")


def reference_keys(**refs: str | None) -> dict:
    """metadata に入れる参照キー (project_id / run_id / step_id / item_id / tool_call_id /
    root_execution_id 等)。None は落とし、値は文字列化する。5 つの問いの view はこれを結合キーに使う。
    """
    return {k: str(v) for k, v in refs.items() if v not in (None, "")}

_GATEWAY_INSERT_SQL = (
    "INSERT INTO llm_gateway_action_audit "
    "(virtual_key_id, virtual_key_hash, request_id, external_request_id, api_flavor, "
    " event_type, decision, reason, model_name, resolved_model, detail_digest, "
    " metadata, system_version, row_hash) "
    "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12::jsonb,$13,$14)"
)

# 台帳書き込みの bounded retry (audit.py=gateway 課金監査と同水準)。spill があるので過剰に粘らない
_MAX_ATTEMPTS = 3
_BACKOFF_BASE = 0.5
# record_sync は呼び出し元 (承認 UI) を待たせるため短い retry のみ
_SYNC_MAX_ATTEMPTS = 2
_SYNC_BACKOFF = 0.25
# FAF backlog 上限。DB 障害 × 高頻度イベント (例: 大量の auth 失敗) で Task が無制限に溜まり
# メモリ/接続プールを枯渇させないため。超過分は即 spill (ブロックしない)
_MAX_PENDING = 512

# ── 本文非保存の構造的ガード (フィールド上限) ───────────────────────────────
# 台帳と spill ログには自由文・本文が長期滞留するため、フィールド単位で上限を強制する。
# reason は分類コード相当の短文のみ、payload_digest は SHA-256 hex のみ、metadata は容量上限。
_MAX_REASON_CHARS = 300
_MAX_METADATA_BYTES = 2048
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


_SAFE_INT = 2 ** 53


def _normalize_numbers(value: Any) -> Any:
    """row_hash の言語間等価 (ROW_HASH_SPEC.md §数値): JSON 数値として残すのは |n| < 2^53 の整数だけ。
    float / 巨大整数 / NaN / Inf は文字列化して保存する (Python の json.dumps と JS の
    JSON.stringify で表記が食い違う 1.0 / 1e-07 / 2^53 超を入力側で排除する)。bool はそのまま。"""
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, int):
        return value if abs(value) < _SAFE_INT else str(value)
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, dict):
        return {str(k): _normalize_numbers(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_numbers(v) for v in value]
    return value


def _sanitize_fields(reason: str | None, payload_digest: str | None,
                     metadata: dict | None) -> tuple:
    """行に入る自由度の高いフィールドを構造的に制限する (本文/PII 混入ガード)。

    - reason: 300 字で截断 (分類コード/短い理由のみを想定)
    - payload_digest: SHA-256 hex (64桁) 以外は破棄 (生値の誤代入防止)
    - metadata: canonical JSON が 2KB 超なら本体を破棄し digest + サイズのみ保存
    """
    if reason is not None:
        reason = str(reason)[:_MAX_REASON_CHARS]
    if payload_digest is not None and not _HEX64_RE.match(str(payload_digest)):
        payload_digest = None
    if not isinstance(metadata, dict):
        # 型契約: metadata は dict のみ (list 等は wrap して混入形を統一する)
        metadata = {} if not metadata else {"value": str(metadata)[:_MAX_REASON_CHARS]}
    # top-level key を文字列化 (mixed-type key が sort_keys で TypeError になるのを防ぐ。
    # ネスト内の mixed key は下の except で unserializable 扱い)
    try:
        metadata = {str(k): _normalize_numbers(v) for k, v in metadata.items()}
        canon = json.dumps(metadata, sort_keys=True, ensure_ascii=False, default=str)
    except (TypeError, ValueError, RecursionError):
        # sort_keys の mixed-type key TypeError、循環参照の RecursionError 含む。
        # 壊れた入力は保存しない (metadata だけ代替値にして監査行自体は残す)
        metadata = {"unserializable": True}
        canon = json.dumps(metadata)
    raw = canon.encode("utf-8")
    if len(raw) > _MAX_METADATA_BYTES:
        metadata = {"truncated": True, "size_bytes": len(raw),
                    "digest": hashlib.sha256(raw).hexdigest()}
    else:
        # canonical JSON 経由の deep-copy: 呼び出し元 dict への aliasing を断ち
        # (後からの mutation で params と spill/row_hash が乖離しない)、
        # 非文字列 key も文字列化されて _row_hash の sort_keys で安全になる
        metadata = json.loads(canon)
    return reason, payload_digest, metadata


class _BaseActionAudit:
    """テーブル別サブクラス共通の書き込み機構 (retry / spill / FAF task 管理)。"""

    _INSERT_SQL: str = ""
    _TABLE: str = ""

    def __init__(self, db: Any, *, system_version: str | None = None):
        self._db = db
        self._system_version = system_version
        self._pending: set[asyncio.Task] = set()
        # Task → (row, marker)。開始前 cancel (coroutine 未実行) の無音消失を防ぐため、
        # done callback 側で「_record_prepared が一度も走らなかった行」を spill する
        self._task_rows: dict[asyncio.Task, tuple[dict, dict]] = {}
        # drain 開始後の新規受付は Task を作らず即 spill (drain が終わらない事態を防ぐ)
        self._closing = False

    # --- サブクラスが実装 ---------------------------------------------------
    def _build_row(self, **fields) -> dict:  # pragma: no cover - abstract
        raise NotImplementedError

    def _params(self, row: dict) -> tuple:  # pragma: no cover - abstract
        raise NotImplementedError

    # --- 書き込み -----------------------------------------------------------
    async def _insert_once(self, params: tuple) -> None:
        result = await self._db.execute_query(self._INSERT_SQL, params)
        # 例外を投げず {"success": False} を返す DB 実装 (DataAccess 系) も失敗として扱う
        if isinstance(result, dict) and result.get("success") is False:
            raise ActionAuditWriteError(str(result.get("error") or "insert failed"))

    async def _exec_checked(self, query: str) -> None:
        """DDL 等の実行。例外 / {"success": False} の両失敗形を送出に正規化する。"""
        result = await self._db.execute_query(query, ())
        if isinstance(result, dict) and result.get("success") is False:
            raise ActionAuditWriteError(str(result.get("error") or "query failed"))

    def _spill(self, row: dict, why: str) -> None:
        """最終手段: サニタイズ済み行を構造化ログへ全文退避 (Loki から手動 reconcile 可能)。

        row は _build_row で _sanitize_fields を通過済み = 本文/PII は構造的に含まれない。
        """
        logger.error("%s %s (%s) row=%s", SPILL_MARKER, self._TABLE, why,
                     json.dumps(row, ensure_ascii=False, default=str))

    async def _record_prepared(self, row: dict, params: tuple,
                               marker: dict | None = None) -> bool:
        """retry 付き書き込み本体。最終失敗/cancel は spill へ退避 (Cancelled 以外は送出しない)。"""
        if marker is not None:
            # coroutine が実行開始した印。開始前 cancel は _on_task_done 側で spill する。
            # (CancelledError は await 点でのみ届くため、この行から try までに消失窓は無い)
            marker["started"] = True
        for attempt in range(1, _MAX_ATTEMPTS + 1):
            try:
                await self._insert_once(params)
                return True
            except asyncio.CancelledError:
                # shutdown drain の timeout 等。無音で消さず spill してから伝播する
                self._spill(row, "cancelled")
                raise
            except Exception as e:
                if attempt >= _MAX_ATTEMPTS:
                    self._spill(row, f"insert failed after {attempt} attempts: {type(e).__name__}")
                    return False
                try:
                    await asyncio.sleep(_BACKOFF_BASE * (2 ** (attempt - 1)))
                except asyncio.CancelledError:
                    self._spill(row, "cancelled")
                    raise
        return False  # 論理上到達しない

    async def record(self, **fields) -> bool:
        """記録 (プロセス生存中は at-least-once: retry → 失敗時 spill 退避)。

        プロセス即死 (SIGKILL 等) では失われうる best-effort である点に注意。
        戻り値: DB へ書けたら True (spill 退避のみなら False)。決して送出しない
        (ただしバリデーション ValueError は呼び出し元のバグとして同期送出)。
        """
        try:
            row = self._build_row(**fields)
        except ValueError:
            raise  # バリデーション (approval.* の actor_ref 必須等) は呼び出し元のバグ = 隠さない
        except Exception as e:  # 想定外の組み立て失敗も監査欠落として可視化
            logger.error("%s %s build failed: %s: %s", SPILL_MARKER, self._TABLE,
                         type(e).__name__, e)
            return False
        return await self._record_prepared(row, self._params(row))

    async def record_sync(self, **fields) -> None:
        """audit-before-act 記録。書けなければ ActionAuditWriteError (呼び出し元は行為を中断)。"""
        row = self._build_row(**fields)
        params = self._params(row)
        last: Exception | None = None
        for attempt in range(1, _SYNC_MAX_ATTEMPTS + 1):
            try:
                await self._insert_once(params)
                return
            except Exception as e:
                last = e
                if attempt < _SYNC_MAX_ATTEMPTS:
                    await asyncio.sleep(_SYNC_BACKOFF)
        raise ActionAuditWriteError(
            f"{self._TABLE} sync write failed: {type(last).__name__}: {last}") from last

    def record_nowait(self, **fields) -> asyncio.Task | None:
        """record() を fire-and-forget 化 (strong ref 保持、GC 消失防止)。

        - バリデーション ValueError (approval.* の actor_ref 欠落等) は**同期**送出する
          (呼び出し元のバグを Task 内へ埋没させない)。
        - running loop 無し / backlog 上限超過はブロックせず即 spill して None。
        """
        try:
            row = self._build_row(**fields)
        except ValueError:
            raise
        except Exception as e:
            logger.error("%s %s build failed: %s: %s", SPILL_MARKER, self._TABLE,
                         type(e).__name__, e)
            return None
        params = self._params(row)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            self._spill(row, "no running loop")
            return None
        if self._closing:
            self._spill(row, "writer closing")
            return None
        if len(self._pending) >= _MAX_PENDING:
            # DB 障害中の高頻度イベントで Task を無制限に積まない (メモリ/接続枯渇ガード)
            self._spill(row, f"pending backlog >= {_MAX_PENDING}")
            return None
        marker: dict = {"started": False}
        task = loop.create_task(self._record_prepared(row, params, marker))
        self._pending.add(task)
        self._task_rows[task] = (row, marker)
        task.add_done_callback(self._on_task_done)
        return task

    def _on_task_done(self, task: asyncio.Task) -> None:
        self._pending.discard(task)
        entry = self._task_rows.pop(task, None)
        if task.cancelled():
            # coroutine が一度も実行されずに cancel された行は spill されていない → ここで退避
            if entry is not None and not entry[1].get("started"):
                self._spill(entry[0], "cancelled before start")
            return  # 実行開始後の cancel は _record_prepared が spill 済み
        exc = task.exception()  # 必ず回収 ("Task exception was never retrieved" 警告防止)
        if exc is not None:  # _record_prepared は送出しない設計 = ここに来たら実装バグ
            logger.error("action audit task unexpected error: %s: %s",
                         type(exc).__name__, exc)

    async def aclose(self, timeout: float = 10.0) -> None:
        """終了時に pending の FAF 書き込みを drain する (worker cleanup / shutdown hook 用)。

        timeout 超過分は cancel され、各 Task が自身の行を spill してから終了する
        (_record_prepared の CancelledError ハンドリング。開始前 cancel は
        _on_task_done が spill) = 無音欠落しない。呼出以降の新規 record_nowait は
        Task を作らず即 spill (drain が収束しない事態を防ぐ)。
        """
        self._closing = True
        if not self._pending:
            return
        pending = list(self._pending)
        try:
            await asyncio.wait_for(asyncio.gather(*pending, return_exceptions=True), timeout)
        except TimeoutError:
            logger.warning("%s %s aclose timeout: %d writes cancelled and spilled",
                           SPILL_MARKER, self._TABLE, len(pending))


class ActionAudit(_BaseActionAudit):
    """`agent_action_audit` 台帳の writer (append-only の行為イベント台帳)。

    Args:
        db: `execute_query(query, params) -> {success, data, error}` を持つ DB ハンドル (SDK の DataAccess 等)。
        source: この writer を使うコンポーネントの名前 (任意の短い文字列。行の `source` 列に入る。
            例: 自作 agent の名前、サービス名)。同じ台帳を複数のコンポーネントが書くとき、
            どこから来た行かを見分けるためのラベル。
        system_version: 書き手のバージョン (image tag 等)。省略可。
        agent_ref: agent が主体の行 (`actor_kind='agent'`) に `actor_ref` が無いときに自動で入れる識別子
            (agent_id 等)。省略時は `agent:<source>`。

    行の主体 (誰がやったか) は `actor_kind` (閉語彙 `ACTOR_KINDS`) と `actor_ref` で表す。人 / system の決定
    イベント (`approval.*` / `gate.resolved` / `content.deleted` / `forensic.*` / `policy.changed` /
    `item.quarantine_released` / `workitem.*`) は `actor_ref` が必須 (無ければ ValueError)。
    それ以外の行は conversation_id 等の相関 ID で間接的に結び付くため省略できる。
    `event_type` は自由文字列だが、既知の語彙は `KNOWN_EVENT_TYPES` を参照 (強制はしない)。
    """

    _INSERT_SQL = _ACTION_INSERT_SQL
    _TABLE = "agent_action_audit"

    def __init__(self, db: Any, *, source: str, system_version: str | None = None,
                 agent_ref: str | None = None):
        if not source or not str(source).strip():
            raise ValueError("source is required: the name of the component writing the ledger "
                             "(e.g. your agent's or service's name)")
        super().__init__(db, system_version=system_version)
        self._source = str(source).strip()
        # agent が主体の行 (actor_kind='agent') に自動付与する actor_ref (nullable にしない)
        self._agent_ref = agent_ref or f"agent:{self._source}"
        self._legacy_insert = False  # 旧 DDL (3.0 列なし) を検出したら True に固定

    async def ensure_schema(self) -> None:
        """台帳/索引が無ければ作成 (冪等)。旧 SDK が作った表には後から追加された列を足す。

        **表の owner ロールで、環境の初期化時に 1 回呼ぶ** (CREATE / ALTER / CREATE INDEX は owner 権限が要る。
        IF NOT EXISTS でも権限検査は省かれない)。実行時の writer は INSERT 権限だけでよく、ensure_schema を
        呼ぶ必要はない。migration 管理の環境 (partition 表など) では呼ばない (migration が正)。
        既に `source_event_id` の重複行があると UNIQUE index は作れない (先に重複を解消する)。
        REVOKE は非 owner で失敗しうるため best-effort。

        NOTE: REVOKE FROM PUBLIC は owner/直接 grant 保持ロールの UPDATE/DELETE を防げない。
        本番の append-only 強制は insert-only ロールの分離で行う (writer に UPDATE / DELETE を与えない)。
        """
        await self._exec_checked(ACTION_AUDIT_DDL)
        await self._exec_checked(ACTION_AUDIT_UPGRADE_DDL)  # 旧 SDK が作った表に新しい列を足す (冪等)
        # 列が揃ったので、同じインスタンスが旧 INSERT (列なし) に落ちていた場合も新 INSERT に戻す
        self._legacy_insert = False
        for ddl in ACTION_AUDIT_INDEXES:
            await self._exec_checked(ddl)
        try:
            await self._exec_checked(_REVOKE_TEMPLATE.format(table=self._TABLE))
        except Exception as e:
            logger.info("revoke skipped on %s (non-owner?): %s", self._TABLE, e)

    def _build_row(self, *, event_type: str, actor_type: str, decision: str,
                   actor_ref: str | None = None, on_behalf_of_ref: str | None = None,
                   resource: str | None = None, action: str | None = None,
                   reason: str | None = None, policy_id: str | None = None,
                   policy_version: str | None = None, execution_id: str | None = None,
                   conversation_id: str | None = None, message_id: str | None = None,
                   request_id: str | None = None, payload_digest: str | None = None,
                   metadata: dict | None = None,
                   actor_kind: str | None = None, project_id: str | None = None,
                   root_execution_id: str | None = None,
                   source_event_id: str | None = None) -> dict:
        """3.0 の追加列 (actor_kind / project_id / root_execution_id / source_event_id) は省略可。
        既存 writer の呼び出し形 (actor_type のみ) はそのまま通り、actor_kind は actor_type から写像する。
        """
        if not event_type or not actor_type or not decision:
            raise ValueError("event_type / actor_type / decision are required")
        kind = (actor_kind or "").strip().lower() or actor_kind_from_type(actor_type)
        if kind not in ACTOR_KINDS:
            raise ValueError(f"actor_kind must be one of {ACTOR_KINDS}: {actor_kind!r}")
        if event_type.startswith(_ACTOR_REQUIRED_PREFIXES) and not actor_ref:
            # 「誰が決めたか」は証跡の本体 (設計書 §6 / instructions/00 §4 の ✓ 行)。欠落は呼び出し元のバグ
            raise ValueError(f"actor_ref is mandatory for {event_type}")
        if not actor_ref and kind == "agent":
            actor_ref = self._agent_ref  # worker 発は agent_id を自動付与 (nullable ではない)
        if source_event_id is not None:
            source_event_id = str(source_event_id).strip()
            if not _SOURCE_EVENT_ID_RE.match(source_event_id):
                raise ValueError("source_event_id must match ^[A-Za-z0-9_.:@+-]{1,160}$")
        if project_id is not None:
            project_id = str(project_id).strip() or None
            if project_id is not None:
                if not _UUID_RE.match(project_id):
                    raise ValueError("project_id must be a UUID string")
                project_id = project_id.lower()  # PG の uuid 表記に合わせて hash 前に正規化
        if root_execution_id is not None:
            root_execution_id = str(root_execution_id).strip()[:255] or None
        reason, payload_digest, metadata = _sanitize_fields(reason, payload_digest, metadata)
        row = {
            "source": self._source, "event_type": event_type, "actor_type": actor_type,
            "actor_ref": actor_ref, "on_behalf_of_ref": on_behalf_of_ref,
            "resource": resource, "action": action, "decision": decision, "reason": reason,
            "policy_id": policy_id, "policy_version": policy_version,
            "execution_id": execution_id, "conversation_id": conversation_id,
            "message_id": message_id, "request_id": request_id,
            "payload_digest": payload_digest, "metadata": metadata or {},
            "system_version": self._system_version,
            "actor_kind": kind, "project_id": project_id,
            "root_execution_id": root_execution_id, "source_event_id": source_event_id,
        }
        row["row_hash"] = _row_hash(row)
        return row

    def _params(self, row: dict) -> tuple:
        base = (
            row["source"], row["event_type"], row["actor_type"], row["actor_ref"],
            row["on_behalf_of_ref"], row["resource"], row["action"], row["decision"],
            row["reason"], row["policy_id"], row["policy_version"], row["execution_id"],
            row["conversation_id"], row["message_id"], row["request_id"],
            row["payload_digest"],
            json.dumps(row["metadata"], ensure_ascii=False, default=str),
            row["system_version"], row["row_hash"],
        )
        return base + (row.get("actor_kind"), row.get("project_id"),
                       row.get("root_execution_id"), row.get("source_event_id"))

    @staticmethod
    def _legacy_params(params: tuple) -> tuple:
        """23 パラメータ → 19 列の legacy INSERT 用。row_hash は**実際に保存する 18 列**から再計算する
        (新列込みの hash をそのまま保存すると、保存内容と hash が一致しない行になる)。"""
        cols = ("source", "event_type", "actor_type", "actor_ref", "on_behalf_of_ref", "resource",
                "action", "decision", "reason", "policy_id", "policy_version", "execution_id",
                "conversation_id", "message_id", "request_id", "payload_digest", "metadata",
                "system_version")
        fields = dict(zip(cols, params[:18], strict=True))
        fields["metadata"] = json.loads(fields["metadata"]) if isinstance(fields["metadata"], str) else fields["metadata"]
        return params[:18] + (_row_hash(fields),)

    @staticmethod
    def _is_missing_30_column(err: Exception) -> bool:
        """3.0 列の不存在だけを legacy 降格の条件にする (他の does not exist では降格しない)。
        asyncpg: UndefinedColumnError (sqlstate 42703) + `column "<name>"`。
        DataAccess: {"success": False, "error": 'column "<name>" ... does not exist'}。"""
        cause = err.__cause__ if isinstance(err, ActionAuditWriteError) else err
        sqlstate = getattr(cause, "sqlstate", None)
        m = _MISSING_COLUMN_RE.search(str(err))
        if m is None:
            return False
        if sqlstate is not None and sqlstate != "42703":
            return False
        return m.group(1) in _NEW_30_COLUMNS

    async def _insert_once(self, params: tuple) -> None:
        """3.0 列付き INSERT。旧 DDL (列なし) の環境では 3.0 列の UndefinedColumn を 1 回だけ検出して
        legacy INSERT に固定する (新 SDK を先に出しても監査行を失わない。DDL 適用後の再起動で戻る)。
        """
        if self._legacy_insert:
            await self._db_insert(_ACTION_INSERT_SQL_LEGACY, self._legacy_params(params))
            return
        try:
            await self._db_insert(self._INSERT_SQL, params)
        except ActionAuditWriteError as e:
            if self._is_missing_30_column(e):
                logger.warning("agent_action_audit: 3.0 columns missing (migration pending) — "
                               "falling back to legacy INSERT for this process")
                self._legacy_insert = True
                await self._db_insert(_ACTION_INSERT_SQL_LEGACY, self._legacy_params(params))
                return
            raise

    async def _db_insert(self, sql: str, params: tuple) -> None:
        try:
            result = await self._db.execute_query(sql, params)
        except Exception as e:  # asyncpg 例外等も文言判定できるよう ActionAuditWriteError に正規化
            raise ActionAuditWriteError(f"{type(e).__name__}: {e}") from e
        if isinstance(result, dict) and result.get("success") is False:
            raise ActionAuditWriteError(str(result.get("error") or "insert failed"))


class GatewayActionAudit(_BaseActionAudit):
    """`llm_gateway_action_audit` (LLM Gateway ポリシー判定) の writer。

    識別は virtual key で統一 (生キーは渡さないこと。llm_gateway_audit と同方針)。
    承認概念がないため record()/record_nowait() のみ想定 (record_sync も使用可)。
    """

    _INSERT_SQL = _GATEWAY_INSERT_SQL
    _TABLE = "llm_gateway_action_audit"

    async def ensure_schema(self) -> None:
        await self._exec_checked(GATEWAY_ACTION_AUDIT_DDL)
        for ddl in GATEWAY_ACTION_AUDIT_INDEXES:
            await self._exec_checked(ddl)
        try:
            await self._exec_checked(_REVOKE_TEMPLATE.format(table=self._TABLE))
        except Exception as e:
            logger.info("revoke skipped on %s (non-owner?): %s", self._TABLE, e)

    def _build_row(self, *, event_type: str, decision: str,
                   virtual_key_id: str | None = None, virtual_key_hash: str | None = None,
                   request_id: str | None = None, external_request_id: str | None = None,
                   api_flavor: str | None = None, reason: str | None = None,
                   model_name: str | None = None, resolved_model: str | None = None,
                   detail_digest: str | None = None,
                   metadata: dict | None = None) -> dict:
        if not event_type or not decision:
            raise ValueError("event_type / decision are required")
        reason, detail_digest, metadata = _sanitize_fields(reason, detail_digest, metadata)
        row = {
            "virtual_key_id": virtual_key_id, "virtual_key_hash": virtual_key_hash,
            "request_id": request_id, "external_request_id": external_request_id,
            "api_flavor": api_flavor, "event_type": event_type, "decision": decision,
            "reason": reason, "model_name": model_name, "resolved_model": resolved_model,
            "detail_digest": detail_digest, "metadata": metadata or {},
            "system_version": self._system_version,
        }
        row["row_hash"] = _row_hash(row)
        return row

    def _params(self, row: dict) -> tuple:
        return (
            row["virtual_key_id"], row["virtual_key_hash"], row["request_id"],
            row["external_request_id"], row["api_flavor"], row["event_type"],
            row["decision"], row["reason"], row["model_name"], row["resolved_model"],
            row["detail_digest"],
            json.dumps(row["metadata"], ensure_ascii=False, default=str),
            row["system_version"], row["row_hash"],
        )
