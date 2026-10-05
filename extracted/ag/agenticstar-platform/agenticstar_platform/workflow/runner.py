"""`mp-workflow/1` runner（marketplace-3.0 03 §2〜§4）。

親プロセス（ここ）が 前処理 → Agent entrypoint を子プロセスで実行 → 回収 → terminal を担う:
1. executor 注入の env（ASTER_RUNTIME_PROTOCOL / ASTER_RUNTIME_BASE_URL / ASTER_RUNTIME_TOKEN / EXECUTION_ID）を検証。汎用 DB
   設定へ fallback しない
2. runtime context を取得し、execution / protocol / 期限を照合。入力 artifact を限定 API から取得して digest / size / 形式を検証
3. `/workspace/input` に展開（read-only）、`/workspace/work` へコピー、from_parameters の設定ファイルを生成。回収用の root fd を
   Agent 起動 **前** に開いて固定する
4. `context.manifest` 監査を **ack まで** 保存し（= server 側の起動 fence。accepted のときだけ所有者）、起動 fence（state の
   started）を永続化してから子プロセスを起動。子の tool.invoked も ack 後にしか進めない（ack の前後で取消 / 期限を再確認）
5. 子終了 / 停止後にプロセスグループ全体を止め（生存確認まで）、宣言 output を root fd 経由で回収して artifact API へ保存
6. tally と終了原因から envelope（version 2）を組み、completion payload を state に永続化してから同じ completion_id で保存
   （ack 喪失は再送、409 terminal は再実行しない）

再起動（runner が completion 保存前に落ちた）: started fence があれば Agent を **再実行せず**、保存済み payload の再送か、
回収できるものだけで `failed/runner_restarted`（効果不明 = had_mutating_success null）として終端する。
期限: executor は実行 deadline で `timeout` 終端 + 回収するので、runner は **回収余裕を差し引いた agent_deadline** で Agent を止め、
残りで回収 / 保存する。

停止: SIGTERM（Pod 停止）は asyncio の signal handler で **停止要求を記録するだけ**。watchdog が停止理由 `stopped` に変換し、
取消 / 期限と同じ協調停止経路（子プロセス群の停止 → 回収 → `failed/runner_stopped` の completion。効果不明）で終端する。

終了コード（00 §7「非0終了と効果不明の扱い」）: 0 = terminal 保存済み（または既に terminal）、2 = terminal を保存できなかった
（所有権を取れなかった / 保存 API が失敗した）、3 = 設定不正（Agent は呼ばれていない）。それ以外の障害（signal、ワークスペース
破損、想定外の例外）は例外のまま非0 で終わってよい: **SDK はプロセスの終了コードを保証しない**。terminal 未保存の非0 終了は
executor が `failed/agent_exit_nonzero`（効果不明）で終端し、front は人の確認（hold）へ回す。exit 0 で terminal 未保存なら
回収猶予後に `failed/completion_missing`（同じく hold）。
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import sys
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

import httpx

from .canonical import digest_json
from .envelope import PRE_ACTION_SKIP_REASONS, SKIP_REASONS, EffectTally, build_envelope, decide_outcome
from .errors import (
    AuditNotPersisted,
    ExecutionTerminal,
    InputIntegrityError,
    OutputCollectionError,
    RuntimeApiError,
    WorkflowConfigError,
    WorkflowError,
)
from .files import (
    WorkspaceRoot,
    collect_outputs,
    copy_input_to_work,
    relative_path,
    render_from_parameters,
    safe_join,
    write_input,
)
from .runtime_client import RuntimeClient

logger = logging.getLogger(__name__)

PROTOCOL = "mp-workflow/1"
ENV_PROTOCOL = "ASTER_RUNTIME_PROTOCOL"
ENV_BASE_URL = "ASTER_RUNTIME_BASE_URL"
ENV_TOKEN = "ASTER_RUNTIME_TOKEN"
ENV_EXECUTION_ID = "EXECUTION_ID"
REQUIRED_ENV = (ENV_PROTOCOL, ENV_BASE_URL, ENV_TOKEN, ENV_EXECUTION_ID)
DEFAULT_WORKSPACE = "/workspace"
STATE_FILE = ".aster_workflow_state.json"
CANCEL_POLL_SECONDS = 5.0
CHILD_GRACE_SECONDS = 10.0
MAX_CONTROL_LINE = 256 * 1024
COLLECTION_MARGIN_MAX = 120.0
COLLECTION_MARGIN_MIN = 30.0          # 停止（SIGTERM 猶予 + SIGKILL 猶予）+ 回収 + 保存の最小余裕
DEFAULT_EXECUTION_TIMEOUT = 900       # context に期限がまだ無い間のローカル上限（00 §6 既定）。server の期限が来たら短い方
DEFAULT_COLLECTION_GRACE = 300
_UUID_RE_HEX = "0123456789abcdef-"
# front は取消 / run の終端 / 期限の後の live な読み取り（入力 artifact / 接続 token）を 409 で拒否する。その code → 停止理由
_LIVE_REJECT_STOP_REASONS = {"cancelled": "cancel", "run_closed": "cancel", "deadline_exceeded": "deadline"}


@dataclass
class WorkflowResult:
    execution_id: str
    outcome: Optional[str]
    outcome_reason_code: Optional[str]
    had_mutating_success: Optional[bool]
    completion_saved: bool
    already_terminal: bool
    exit_code: int
    artifacts: list[dict[str, Any]] = field(default_factory=list)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_ts(raw: Any) -> Optional[datetime]:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None


def _exit_code(saved: bool, already: bool) -> int:
    """0 = terminal 保存済み（または既に terminal）、2 = 保存できなかった。executor はどちらも効果不明として
    hold に収束させる（exit 0 + 未保存 = 回収猶予後 completion_missing、非0 = agent_exit_nonzero）。"""
    return 0 if (saved or already) else 2


GATE_DECISIONS = ("proceed", "send_back")
GATE_DECISION_KEYS = ("gate_id", "decision", "decided_by", "note", "decided_at")


def _gate_decision(ctx: Mapping[str, Any]) -> Optional[dict[str, Any]]:
    """確認の決定を受けた起動なら、その決定（frontのcontextの`gate_decision`）。形が合わなければ渡さない。"""
    gd = ctx.get("gate_decision")
    if not isinstance(gd, dict) or gd.get("decision") not in GATE_DECISIONS or not isinstance(gd.get("gate_id"), str):
        return None
    return {key: gd[key] if isinstance(gd.get(key), str) else None for key in GATE_DECISION_KEYS}


def validate_env(env: Mapping[str, str]) -> dict[str, str]:
    missing = [k for k in REQUIRED_ENV if not env.get(k)]
    if missing:
        raise WorkflowConfigError("missing runtime env: " + ", ".join(missing)
                                  + " (injected by the marketplace executor; no fallback to generic settings)")
    if env[ENV_PROTOCOL] != PROTOCOL:
        raise WorkflowConfigError(f"unsupported runtime protocol {env[ENV_PROTOCOL]!r}; expected {PROTOCOL}")
    eid = env[ENV_EXECUTION_ID].strip().lower()
    if len(eid) != 36 or any(c not in _UUID_RE_HEX for c in eid):
        raise WorkflowConfigError("EXECUTION_ID must be a UUID")
    base = env[ENV_BASE_URL].strip()
    if not (base.startswith("http://") or base.startswith("https://")):
        raise WorkflowConfigError("ASTER_RUNTIME_BASE_URL must be an http(s) URL")
    return {ENV_PROTOCOL: PROTOCOL, ENV_BASE_URL: base, ENV_TOKEN: env[ENV_TOKEN], ENV_EXECUTION_ID: eid}


class _State:
    """再送 / 再起動用に永続化する状態（completion_id、artifact_id、起動 fence、completion payload、tally journal）。workspace 直下。"""

    def __init__(self, path: Path):
        self._path = path
        self.data: dict[str, Any] = {}
        if path.exists():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                self.data = {}

    def get_id(self, key: str) -> str:
        val = self.data.get(key)
        if not val:
            val = str(uuid.uuid4())
            self.data[key] = val
            self.save()
        return val

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def save(self) -> None:
        tmp = self._path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii=False))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, self._path)


class WorkflowRunner:
    def __init__(self, *, entrypoint: str, env: Mapping[str, str], workspace: Optional[str] = None,
                 transport: Optional[httpx.AsyncBaseTransport] = None, python: Optional[str] = None,
                 cancel_poll_seconds: float = CANCEL_POLL_SECONDS, child_grace_seconds: float = CHILD_GRACE_SECONDS,
                 stop_on_sigterm: bool = False):
        self._entrypoint = entrypoint
        self._env = validate_env(env)
        self._workspace = Path(workspace or env.get("ASTER_WORKSPACE") or DEFAULT_WORKSPACE)
        self._transport = transport
        self._python = python or sys.executable
        self._cancel_poll = cancel_poll_seconds
        self._grace = child_grace_seconds
        self._stop_on_sigterm = stop_on_sigterm   # プロセス全体の副作用なので、プロセスを所有する呼び出し（run()）だけが有効にする
        self.execution_id = self._env[ENV_EXECUTION_ID]
        self._client: Optional[RuntimeClient] = None
        self._ctx: dict[str, Any] = {}
        self._tally = EffectTally()
        self._stop_reason: Optional[str] = None
        self._stop_requested = False      # SIGTERM を受理した（watchdog が停止理由 `stopped` に変換する）
        self._last_context_check = 0.0
        self._agent_deadline: Optional[datetime] = None
        self._execution_deadline: Optional[datetime] = None
        self._collection_deadline: Optional[datetime] = None
        self._execution_explicit = False    # server が確定した期限か（False = 契約上限からの暫定値）
        self._collection_explicit = False
        self._state: Optional[_State] = None
        self._cleanup_uncertain = False   # 再起動後、前の Agent プロセスの停止を確認できなかった（回収しない）

    # ------------------------------------------------------------------
    def _seconds_left(self) -> Optional[float]:
        if self._collection_deadline is None:
            return None
        return (self._collection_deadline - _utc_now()).total_seconds()

    @staticmethod
    def _owns(state: _State) -> bool:
        """このプロセス（または同じ workspace の前回）が所有権（server 側の起動 fence）を証明しているか。"""
        return bool(state.data.get("fence_owner"))

    def request_stop(self) -> None:
        """停止要求を記録する（SIGTERM handler / 呼び出し側から）。停止そのものは協調停止経路が行う。"""
        if not self._stop_requested:
            self._stop_requested = True
            logger.warning("[%s] stop requested; finishing the terminal steps", self.execution_id)

    async def run(self) -> WorkflowResult:
        self._client = RuntimeClient(self._env[ENV_BASE_URL], self.execution_id, self._env[ENV_TOKEN],
                                     transport=self._transport, deadline=self._seconds_left)
        loop = asyncio.get_running_loop()
        installed = False
        if self._stop_on_sigterm:
            try:
                loop.add_signal_handler(signal.SIGTERM, self.request_stop)
                installed = True
            except (NotImplementedError, RuntimeError, ValueError):
                logger.warning("[%s] SIGTERM handler could not be installed; the default disposition stays", self.execution_id)
        try:
            return await self._run()
        finally:
            if installed:
                loop.remove_signal_handler(signal.SIGTERM)
            try:
                await self._client.aclose()
            except Exception as e:   # noqa: BLE001 - transport の後片付けの失敗で保存済み completion の結果を壊さない
                logger.warning("[%s] runtime client could not be closed: %s: %s", self.execution_id, type(e).__name__, e)

    async def _run(self) -> WorkflowResult:
        eid = self.execution_id
        state = _State(self._workspace / STATE_FILE)
        self._state = state
        self._tally = EffectTally.from_dict(state.data.get("tally"))  # journal（再起動でも観測を 0 に戻さない）
        try:
            ctx = await self._client.get_context()
        except ExecutionTerminal:
            logger.info("[%s] execution already terminal before start; nothing to do", eid)
            return WorkflowResult(eid, None, None, None, False, True, 0)
        self._verify_context(ctx)
        self._ctx = ctx
        self._set_deadlines(ctx)

        # 再起動: 起動 fence があるなら Agent を再実行しない（外部 write を繰り返さない）
        if state.data.get("started"):
            return await self._recover(state, ctx)
        input_dir, work_dir, output_dir = self._prepare_dirs()

        # **所有権を先に確定する**: 入力の staging / 取消判定より前に server 側の起動 fence を取る。所有を証明できない限り
        # completion は一切送らない（他 instance が所有する execution を横から terminal にしない。ここで諦めた実行は
        # executor の照合 failed/pod_lost / failed/completion_missing に収束する）。停止要求が **所有権を取る前** に来ていたら
        # fence を取らずに退く（Agent も効果も無いので再実行してよい）
        self._check_deadline_now()
        if self._stop_reason == "stopped" and not self._owns(state):
            logger.warning("[%s] stop requested before ownership was proven; not starting", eid)
            return WorkflowResult(eid, None, None, None, False, False, 2)

        manifest = self._manifest(ctx)
        try:
            owner = await self._persist_manifest(state, manifest)
        except AuditNotPersisted as e:
            logger.error("[%s] manifest audit not persisted: %s", eid, e)
            self._tally.persist_failures += 1
            await self._journal_tally()
            if not self._owns(state):
                # 所有権を証明できていない: completion を送らない（所有者かもしれない他 instance の実行を横から終端しない）
                return WorkflowResult(eid, None, None, None, False, False, 2)
            # 証明済み（前回の manifest 保存後に落ちた再起動）: Agent は起動していないので、監査が欠けたことを載せた
            # failed/audit_persist_failed（persist_failures > 0 が最優先。効果不明）で front に hold させる
            return await self._finish(state, ctx, {}, agent_error=None)
        if not owner:
            # 別の runner instance（例: emptyDir を失った入れ替わり Pod）が既にこの execution を所有している
            logger.warning("[%s] execution is owned by another runner instance; not starting and not completing", eid)
            return WorkflowResult(eid, None, None, None, False, False, 2)

        agent_error: Optional[str] = None
        roots: dict[str, WorkspaceRoot] = {}
        try:   # cancel（Pod 停止）が staging / Agent 実行中に飛んでも、開いた回収 root の fd を漏らさない
            if ctx.get("cancel_requested_at"):
                self._stop_reason = "cancel"
            else:
                try:
                    await self._stage_inputs(ctx, input_dir, work_dir)
                    roots = self._open_roots(input_dir, work_dir, output_dir)
                    await self._refresh_control(force=True)  # 起動直前に取消 / 期限を再確認
                except InputIntegrityError as e:
                    logger.error("[%s] input rejected: %s", eid, e)
                    agent_error = "input_integrity"
                except AuditNotPersisted as e:
                    logger.error("[%s] audit not persisted before start: %s", eid, e)
                    self._tally.persist_failures += 1
                except OutputCollectionError as e:
                    logger.error("[%s] workspace preparation rejected: %s", eid, e)
                    agent_error = "input_integrity"
                except ExecutionTerminal:
                    logger.info("[%s] execution became terminal while staging inputs", eid)
                    self._stop_reason = "terminal"
                except RuntimeApiError as e:
                    # 取り込み中に取消 / run の終端 / 期限が来た: Agent は起動していないので停止理由にして終端へ進む。
                    # それ以外の API エラー（不達・5xx の再送切れ等）は従来どおり例外のまま
                    if not self._stop_on_live_reject(e):
                        raise
                    logger.info("[%s] input fetch refused (%s); not starting the agent", eid, e.code)
                else:
                    if not self._stop_reason:
                        # 起動 fence（再起動時に Agent を再実行しない）を durable に書いてから、期限を再確認して起動。
                        # 書けなければ例外のまま（Agent は起動していない = 効果なし。非0 終了は executor が hold にする）
                        await asyncio.get_running_loop().run_in_executor(None, state.set, "started", _utc_now().isoformat())
                        self._check_deadline_now()
                    if not self._stop_reason and agent_error is None:
                        agent_error = await self._run_agent(ctx, manifest, input_dir, work_dir, output_dir)
            return await self._finish(state, ctx, roots, agent_error=agent_error)
        finally:
            for r in roots.values():
                r.close()

    # ------------------------------------------------------------------
    async def _finish(self, state: _State, ctx: dict[str, Any], roots: dict[str, WorkspaceRoot], *,
                      agent_error: Optional[str], restarted: bool = False) -> WorkflowResult:
        """回収 → artifact 保存 → envelope → completion（payload を永続化してから送る）。"""
        eid = self.execution_id
        contract = ctx.get("contract") or {}
        collected: list = []
        required_missing: list[str] = []
        collection_error: Optional[str] = None
        if self._tally.persist_failures == 0 and agent_error != "input_integrity" and roots and not self._cleanup_uncertain:
            try:
                collected = collect_outputs(output_root=roots["output"], work_root=roots["work"], input_root=roots.get("input"),
                                            outputs=list(contract.get("outputs") or []), files=list(contract.get("files") or []))
                required_missing = self._required_missing(contract, collected)
            except OutputCollectionError as e:
                logger.error("[%s] output collection rejected: %s", eid, e)
                collection_error = type(e).__name__
                collected = []
        artifacts: list[dict[str, Any]] = []
        upload_failed = False
        if collected and not required_missing:
            try:
                artifacts = await self._upload(state, collected)
            except ExecutionTerminal:
                return WorkflowResult(eid, None, None, None, False, True, 0)
            except (RuntimeApiError, WorkflowError) as e:
                logger.error("[%s] artifact save failed: %s", eid, e)
                upload_failed = True

        outcome, reason, had = decide_outcome(
            tally=self._tally, agent_error=agent_error, stop_reason=self._stop_reason,
            outputs_collected=len(artifacts), required_missing=required_missing,
            effect_mode=str(contract.get("effect_mode") or "read_only"), collection_failed=collection_error is not None,
            effects_uncertain=bool(restarted or self._cleanup_uncertain))
        if restarted:
            # Agent の結果を観測できていない = 実行環境の異常。効果は不明（had = None）なので front は自動 retry せず人へ回す
            outcome, reason = "failed", "runner_restarted"
        if upload_failed and outcome in ("completed", "skipped"):
            outcome, reason = "failed", "artifact_save_failed"  # 保存が一部失敗したら次工程へ進む outcome を出さない
        if self._cleanup_uncertain and not restarted and outcome != "stopped" \
                and reason not in ("audit_persist_failed", "runner_stopped"):
            # 前の Agent プロセスを止め切れていない（まだ外部 write を出しうる）。front は理由 `cleanup_uncertain` を効果不明として
            # hold する（had = True を観測済みでも自動 retry させない）。既に hold に収束する終端（再起動 / 取消 / runner 停止 /
            # 監査保存失敗）の理由は上書きしない。観測済みの成功（had = True）は envelope にそのまま残す
            outcome, reason = "failed", "cleanup_uncertain"
        error_class = collection_error or (agent_error if agent_error not in (None, "input_integrity") else None)
        if agent_error == "input_integrity":
            outcome, reason, error_class = "failed", "input_integrity", "InputIntegrityError"
        runner_state = {"stop_reason": self._stop_reason, "agent_error": agent_error, "restarted": restarted,
                        "cleanup_uncertain": self._cleanup_uncertain}
        envelope = build_envelope(outcome=outcome, reason=reason, had_mutating_success=had, tally=self._tally,
                                  error_class=error_class, runner=runner_state)
        saved, already = await self._complete(state, envelope, [a["artifact_id"] for a in artifacts])
        return WorkflowResult(eid, outcome, reason, had, saved, already, _exit_code(saved, already), artifacts)

    async def _recover(self, state: _State, ctx: dict[str, Any]) -> WorkflowResult:
        """runner 再起動後: 保存済み completion payload があれば **同じ内容を** 再送（新しい envelope を作らない = front の記録と
        戻り値が食い違わない）、無ければ Agent を再実行せず効果不明で終端。前の Agent プロセスグループが同じ PID namespace に
        残っていれば（container 再起動でない再起動）回収前に止める。"""
        eid = self.execution_id
        payload = state.data.get("completion")
        if isinstance(payload, dict) and payload.get("envelope"):
            env = payload["envelope"]
            logger.warning("[%s] runner restarted after building the completion; resending it (outcome=%s)", eid, env.get("outcome"))
            saved, already = await self._complete(state, env, list(payload.get("output_artifact_ids") or []))
            return WorkflowResult(eid, env.get("outcome"), env.get("outcome_reason_code"), env.get("had_mutating_success"),
                                  saved, already, _exit_code(saved, already))
        logger.warning("[%s] runner restarted before completion; the agent will not be re-executed", eid)
        await self._stop_previous_group(state)
        roots = {} if self._cleanup_uncertain else self._open_roots(*self._prepare_dirs())  # 止め切れていないなら回収しない
        try:
            return await self._finish(state, ctx, roots, agent_error=None, restarted=True)
        finally:
            for r in roots.values():
                r.close()

    async def _stop_previous_group(self, state: _State) -> None:
        """state に記録した前回の Agent プロセスグループ（pgid + リーダーの起動時刻）が生きていれば止める。
        リーダー（pid == pgid）が生きていて起動時刻が一致するときだけ所有とみなしてグループ全員を止める。リーダーが居ない /
        起動時刻が違う（PID 再利用）場合は所有を立証できないので kill せず、同じ session の生存プロセスが残っていれば
        cleanup_uncertain（回収しない）。"""
        prev = state.data.get("agent_process")
        if not isinstance(prev, dict):
            return
        pgid, start = prev.get("pgid"), prev.get("start_ticks")
        if not isinstance(pgid, int) or pgid <= 1:
            return
        deadline = time.monotonic() + self._grace * 4
        while True:
            members = self._group_members(pgid)
            leader = next((m for m in members if m[0] == pgid), None)
            if leader is not None and leader[1] == start:
                owned = [pid for pid, _t, _s in members]   # グループ全員（停止中に fork した子も再走査で拾う）
            else:
                if any(sid == pgid for _pid, _t, sid in members):
                    logger.error("[%s] processes of uncertain ownership remain in group %s; outputs will not be collected",
                                 self.execution_id, pgid)
                    self._cleanup_uncertain = True
                return
            if not owned:
                return
            if time.monotonic() >= deadline:
                logger.error("[%s] previous agent processes could not be stopped; outputs will not be collected", self.execution_id)
                self._cleanup_uncertain = True
                return
            logger.warning("[%s] previous agent processes %s are still alive; stopping them before collection", self.execution_id, owned)
            await self._kill_pids(owned)

    async def _kill_pids(self, pids: list[int]) -> None:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            for pid in pids:
                try:
                    os.kill(pid, sig)
                except ProcessLookupError:
                    pass
            deadline = time.monotonic() + self._grace
            while any(self._pid_alive(pid) for pid in pids) and time.monotonic() < deadline:
                await asyncio.sleep(0.1)
            if not any(self._pid_alive(pid) for pid in pids):
                return

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        try:
            with open(f"/proc/{pid}/stat", "rb") as f:
                stat_line = f.read().decode("utf-8", "replace")
            return stat_line[stat_line.rindex(")") + 2:].split()[0] != "Z"
        except (OSError, ValueError, IndexError):
            return False

    # ------------------------------------------------------------------
    def _verify_context(self, ctx: dict[str, Any]) -> None:
        if str(ctx.get("execution_id") or "").lower() != self.execution_id:
            raise WorkflowConfigError("runtime context is for a different execution")
        if ctx.get("protocol") != PROTOCOL:
            raise WorkflowConfigError("runtime context protocol mismatch")
        lr = ctx.get("launch_request") or {}
        if lr.get("protocol") != PROTOCOL or str(lr.get("requested_execution_id") or "").lower() != self.execution_id:
            raise WorkflowConfigError("launch request does not bind this execution")
        if ctx.get("state") == "terminal":
            raise ExecutionTerminal("execution already terminal")

    def _set_deadlines(self, ctx: dict[str, Any]) -> None:
        """executor は実行 deadline 後も回収 deadline までコンテナを待ち、その後 timeout 終端 + 回収する。runner は後片付け
        （agent 停止 → 回収 → 保存）の余裕を **回収期限** から取った agent_deadline で Agent を止め、保存要求は回収期限を越えない。
        余裕 = min(120s, max(30s, 回収期限までの 10%))。契約上の実行窓は削らない（回収猶予が余裕より小さい契約だけ縮む）。
        server の期限が無い項目は暫定値（実行 = 契約上限（既定 900s）、回収 = 実行 + 300s）。server が確定した期限は暫定値を
        置き換え（前後どちらでも）、確定値同士は短い方（後ろへ延ばさない）。"""
        d = ctx.get("deadlines") or {}
        execution = _parse_ts(d.get("execution"))
        collection = _parse_ts(d.get("collection"))
        limits = (ctx.get("contract") or {}).get("limits") or {}
        try:
            timeout = int(limits.get("execution_timeout_seconds") or DEFAULT_EXECUTION_TIMEOUT)
        except (TypeError, ValueError):
            timeout = DEFAULT_EXECUTION_TIMEOUT
        self._execution_deadline, self._execution_explicit = self._adopt(
            self._execution_deadline, self._execution_explicit, execution, _utc_now() + timedelta(seconds=timeout))
        provisional_collection = self._execution_deadline + timedelta(seconds=DEFAULT_COLLECTION_GRACE)
        if collection is None and not self._collection_explicit:
            # 回収の暫定値は実行期限から導く値なので、実行期限が確定値で置き換わったら作り直す（古い実行期限に取り残さない）
            self._collection_deadline, self._collection_explicit = provisional_collection, False
        else:
            self._collection_deadline, self._collection_explicit = self._adopt(
                self._collection_deadline, self._collection_explicit, collection, provisional_collection)
        remaining = (self._collection_deadline - _utc_now()).total_seconds()
        margin = min(COLLECTION_MARGIN_MAX, max(COLLECTION_MARGIN_MIN, remaining * 0.1))
        self._agent_deadline = min(self._execution_deadline, self._collection_deadline - timedelta(seconds=margin))

    @staticmethod
    def _adopt(current: Optional[datetime], current_explicit: bool, explicit: Optional[datetime],
               provisional: datetime) -> tuple[datetime, bool]:
        if explicit is not None:
            if current is None or not current_explicit:
                return explicit, True          # 暫定値は確定値で置き換える（前後どちらでも）
            return min(current, explicit), True  # 確定値同士は短い方
        if current is None:
            return provisional, False
        return current, current_explicit       # 暫定値は最初の 1 回だけ（後から作り直して延ばさない）

    def _prepare_dirs(self) -> tuple[Path, Path, Path]:
        ws = self._workspace
        ws.mkdir(parents=True, exist_ok=True)
        dirs = (ws / "input", ws / "work", ws / "output")
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    @staticmethod
    def _open_roots(input_dir: Path, work_dir: Path, output_dir: Path) -> dict[str, WorkspaceRoot]:
        """3 root の directory fd を開く。1 つでも開けなければ開いた分を閉じて OutputCollectionError に正規化する（fd を漏らさない）。"""
        roots: dict[str, WorkspaceRoot] = {}
        try:
            for name, d in (("input", input_dir), ("work", work_dir), ("output", output_dir)):
                roots[name] = WorkspaceRoot(d)
        except OSError as e:
            for r in roots.values():
                r.close()
            raise OutputCollectionError(f"cannot open workspace root: {e}") from e
        return roots

    async def _stage_inputs(self, ctx: dict[str, Any], input_dir: Path, work_dir: Path) -> None:
        contract = ctx.get("contract") or {}
        files = {relative_path(str(f.get("path"))): f for f in (contract.get("files") or []) if f.get("path")}
        for entry in ctx.get("input_manifest") or []:
            rel = relative_path(str(entry["target_path"]))
            fdef = files.get(rel) or {}
            declared = str(fdef.get("format") or "")
            bound = str(entry.get("format") or "")
            if declared and bound and declared != bound:
                # manifest の artifact 形式が契約 file の形式と食い違う（text を JSON file に束縛 等）= schema 検証を迂回させない
                raise InputIntegrityError(f"input {rel} format {bound} does not match the contract file format {declared}")
            data = await self._client.download_artifact(str(entry["artifact_id"]))
            write_input(input_dir, rel, data, expected_sha256=entry.get("sha256"), expected_size=entry.get("size"),
                        fmt=declared or bound, schema=fdef.get("schema"))
        copy_input_to_work(input_dir, work_dir)
        params = ctx.get("parameters") or {}
        for f in contract.get("files") or []:
            if f.get("from_parameters"):
                target = safe_join(work_dir, relative_path(str(f["path"])))
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(render_from_parameters(str(f.get("format") or "json"), dict(params), f.get("schema")))

    def _manifest(self, ctx: dict[str, Any]) -> dict[str, Any]:
        lr = ctx.get("launch_request") or {}
        contract = ctx.get("contract") or {}
        manifest = {
            "protocol": PROTOCOL,
            "execution_id": self.execution_id,
            "root_execution_id": ctx.get("root_execution_id"),
            "entry_ref": ctx.get("entry_ref"),
            "operation_key": ctx.get("operation_key"),
            "attempt": lr.get("attempt"),
            "config_revision": ctx.get("config_revision"),
            "contract_digest": contract.get("contract_digest"),
            "image_digest": contract.get("image_digest"),
            "effect_mode": contract.get("effect_mode"),
            "parameters_digest": ctx.get("parameters_digest"),
            "input_manifest": ctx.get("input_manifest") or [],
            "deadlines": ctx.get("deadlines") or {},
        }
        gd = _gate_decision(ctx)
        if gd:
            # 理由・コメントは人が書いた本文なので、監査に残す記録には入れない
            manifest["gate_decision"] = {key: gd[key] for key in ("gate_id", "decision", "decided_by")}
        return manifest

    async def _persist_manifest(self, state: _State, manifest: dict[str, Any]) -> bool:
        """context.manifest を durable に保存してから Agent を開始する（ack 無しでは開始しない）。
        server 側の起動 fence: execution に固定の event A（`context-manifest-<eid>`）と、この runner instance に固有の
        event B（`…-<instance>`、instance id は state に永続化）を **同じ batch**（front は 1 transaction で保存）で送る。
          A accepted                                   → 所有者。state に fence_owner を残す
          A duplicate + B duplicate + state.fence_owner → Agent 未起動での再起動（所有者）
          A duplicate + それ以外                        → 所有者でない → False（state に fence_lost を残し、以後も起動しない）
        front は A が重複でも B を commit するので、B の重複は所有の証拠にならない（accepted の応答を失った真の所有者は
        安全側に倒れて起動しない = 重複実行より hold を選ぶ。executor の照合 completion_missing で収束）。"""
        if state.data.get("fence_lost"):
            return False
        instance = state.get_id("runner_instance")
        base_id = f"context-manifest-{self.execution_id}"
        events = [
            {"event_id": base_id, "event_type": "context.manifest", "decision": "ok",
             "metadata": {"digest": digest_json(manifest), "phase": "start"}, "occurred_at": _utc_now().isoformat()},
            {"event_id": f"{base_id}-{instance}", "event_type": "context.manifest", "decision": "ok",
             "metadata": {"digest": digest_json(manifest), "phase": "owner"}, "occurred_at": _utc_now().isoformat()},
        ]
        try:
            res = await self._client.post_audit(events)
        except RuntimeApiError as e:
            raise AuditNotPersisted(str(e))
        accepted, duplicates = set(res.get("accepted") or []), set(res.get("duplicates") or [])
        if base_id in accepted:
            await asyncio.get_running_loop().run_in_executor(None, state.set, "fence_owner", _utc_now().isoformat())
            return True
        if base_id in duplicates:
            if events[1]["event_id"] in duplicates and self._owns(state):
                return True
            state.set("fence_lost", _utc_now().isoformat())
            return False
        raise AuditNotPersisted("manifest event not acknowledged")

    @staticmethod
    def _required_missing(contract: dict[str, Any], collected: list) -> list[str]:
        names = {c.logical_name for c in collected}
        return [str(o.get("name")) for o in (contract.get("outputs") or []) if o.get("required") and o.get("name") not in names]

    # ------------------------------------------------------------------
    async def _run_agent(self, ctx: dict[str, Any], manifest: dict[str, Any], input_dir: Path, work_dir: Path,
                         output_dir: Path) -> Optional[str]:
        """子プロセスで entrypoint を実行し、専用 fd の制御チャネルで監査 / 取消確認 / skip に応える。
        戻り値: None（正常 return）/ error_class（例外・設定不正・停止）。"""
        lr = ctx.get("launch_request") or {}
        spec = {
            "entrypoint": self._entrypoint,
            "execution_id": self.execution_id,
            "project_id": lr.get("project_id"), "run_id": lr.get("run_id"), "agent_id": lr.get("agent_id"),
            "marketplace_agent_id": lr.get("marketplace_agent_id"), "root_execution_id": ctx.get("root_execution_id"),
            "entry_ref": ctx.get("entry_ref"), "operation_key": ctx.get("operation_key"), "attempt": lr.get("attempt") or 1,
            "effect_mode": (ctx.get("contract") or {}).get("effect_mode") or "read_only",
            "parameters": ctx.get("parameters") or {}, "connections": ctx.get("connections") or {},
            "input_dir": str(input_dir), "work_dir": str(work_dir), "output_dir": str(output_dir),
            "manifest": manifest, "deadlines": ctx.get("deadlines") or {}, "gate_decision": _gate_decision(ctx),
            "agent_deadline": self._agent_deadline.isoformat() if self._agent_deadline else None,
        }
        # 制御チャネル: 親→子（spec + 応答）、子→親（要求）。stdio は Agent の通常出力のまま。
        # pipe / spawn / 識別の保存は **まとめて** 失敗を引き受ける = fd を漏らさない / 識別を保存できなかった子を残さない
        to_child_r = to_child_w = from_child_r = from_child_w = -1
        proc = None
        reader_pipe = None
        writer_fd = None
        try:
            to_child_r, to_child_w = os.pipe()
            from_child_r, from_child_w = os.pipe()
            child_env = {k: v for k, v in os.environ.items() if k != ENV_TOKEN}  # token は子（Agent コード）へ渡さない
            child_env["PYTHONUNBUFFERED"] = "1"
            child_env["ASTER_WORKFLOW_IPC_IN"] = str(to_child_r)
            child_env["ASTER_WORKFLOW_IPC_OUT"] = str(from_child_w)
            sdk_root = str(Path(__file__).resolve().parents[2])  # 子は親と同じ SDK を import する
            child_env["PYTHONPATH"] = sdk_root + (os.pathsep + child_env["PYTHONPATH"] if child_env.get("PYTHONPATH") else "")
            proc = await asyncio.create_subprocess_exec(
                self._python, "-m", "agenticstar_platform.workflow.child",
                stdin=asyncio.subprocess.DEVNULL, stdout=None, stderr=None,
                env=child_env, cwd=str(work_dir), start_new_session=True, pass_fds=(to_child_r, from_child_w))
            os.close(to_child_r)
            to_child_r = -1
            os.close(from_child_w)
            from_child_w = -1
            if self._state is not None:  # 再起動後に残存グループを見分けて止めるための識別（pgid + 起動時刻）
                self._state.set("agent_process", {"pgid": proc.pid, "start_ticks": self._start_ticks(proc.pid)})
            loop = asyncio.get_running_loop()
            reader = asyncio.StreamReader(limit=MAX_CONTROL_LINE)
            reader_pipe = os.fdopen(from_child_r, "rb", buffering=0)
            from_child_r = -1
            await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), reader_pipe)
            writer_fd = os.fdopen(to_child_w, "wb", buffering=0)
            to_child_w = -1
        except BaseException as e:
            # OSError（pipe / spawn / 識別の保存）だけでなく cancel 等でも、掴んだ fd と起動途中の子を片付ける
            for f in (reader_pipe, writer_fd):
                if f is not None:
                    try:
                        f.close()
                    except OSError:
                        pass
            for fd in (to_child_r, to_child_w, from_child_r, from_child_w):
                if fd >= 0:
                    try:
                        os.close(fd)
                    except OSError:
                        pass
            if proc is not None:
                await self._terminate_group(proc)   # 識別を保存できなかった子は残さない（外部 write を出しうる）
            if not isinstance(e, OSError):
                raise               # cancel 等はそのまま外へ（completion は送らない = executor が hold）
            logger.error("[%s] agent could not be started: %s", self.execution_id, e)
            return "AgentSpawnFailed"

        def _send(obj: dict[str, Any]) -> None:
            writer_fd.write(json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n")

        try:
            _send(spec)
        except (BrokenPipeError, OSError):
            await self._terminate_group(proc)
            return "AgentSpawnFailed"
        watchdog = asyncio.create_task(self._watchdog(proc))
        status = "error"
        error_class: Optional[str] = "AgentExit"
        try:
            while True:
                line_task = asyncio.ensure_future(reader.readline())
                exit_task = asyncio.ensure_future(proc.wait())
                done, _ = await asyncio.wait({line_task, exit_task}, return_when=asyncio.FIRST_COMPLETED)
                if line_task in done:
                    exit_task.cancel()
                    try:
                        line = line_task.result()
                    except (ValueError, asyncio.LimitOverrunError):
                        logger.warning("[%s] oversized control line ignored", self.execution_id)
                        continue
                    if not line:
                        break
                    try:
                        msg = json.loads(line.decode("utf-8"))
                    except ValueError:
                        continue
                    if not isinstance(msg, dict) or "id" not in msg:
                        continue
                    reply = await self._answer(msg)
                    reply["id"] = msg["id"]
                    try:
                        _send(reply)
                    except (BrokenPipeError, OSError):
                        break
                    if msg.get("op") == "done":
                        status = str(msg.get("status") or "error")
                        error_class = msg.get("error_class")
                        break
                else:
                    line_task.cancel()
                    break  # 子（リーダー）が終了。残りの要求は無視
        finally:
            watchdog.cancel()
            try:
                writer_fd.close()
            except OSError:
                pass
            await self._terminate_group(proc)   # 配下プロセスまで止めてから回収へ
        if self._stop_reason in ("cancel", "deadline", "terminal", "stopped"):
            return "AgentStopped"
        if status == "ok":
            return None
        if status == "config_error":
            return error_class or "EntrypointUnavailable"
        return error_class or "AgentError"

    async def _answer(self, msg: dict[str, Any]) -> dict[str, Any]:
        """子の要求への応答。どの op の応答にも、既に確定している停止を載せる（子は次の取消確認を待たずに固定する。#2369）。
        ここで停止要求 / 期限を停止理由へ確定させない (_check_deadline_now を呼ばない): Agent が戻った直後の done を
        期限の境目で stopped / timeout に変えない (終わり方の決め方は watchdog と各 op のまま)。"""
        reply = await self._dispatch(msg)
        if self._stop_reason and not reply.get("stop_reason"):
            reply["stop_reason"] = self._stop_reason
        return reply

    async def _dispatch(self, msg: dict[str, Any]) -> dict[str, Any]:
        op = msg.get("op")
        if op == "audit":
            return await self._on_audit(msg.get("event") or {})
        if op == "check":
            await self._refresh_control(force=False)
            self._check_deadline_now()   # 待つ間に来た停止 signal / 期限も載せる
            return {"stop_reason": self._stop_reason}
        if op == "skip":
            reason = str(msg.get("reason") or "")
            if reason in SKIP_REASONS or reason in PRE_ACTION_SKIP_REASONS:
                self._tally.skip_reason = reason
                if not await self._journal_tally():
                    self._tally.persist_failures += 1   # 失敗の証拠を残す（skip を成功に化けさせない）
                    await self._journal_tally()
                    return {"ok": False, "error": "observation journal not durable"}
                return {"ok": True}
            return {"ok": False, "error": "unknown skip reason"}
        if op == "log":
            logger.info("[%s] agent: %s", self.execution_id, str(msg.get("message"))[:2000])
            return {"ok": True}
        if op == "connection_token":
            return await self._on_connection_token(str(msg.get("slot") or ""))
        if op == "done":
            return {"ok": True}
        return {"ok": False, "error": "unknown op"}

    async def _on_connection_token(self, slot: str) -> dict[str, Any]:
        """子の求めで接続 slot の access token を front から取り直す（起動時に env で渡した token は 1 時間程度で
        切れうる。executer-marketplace #55）。取消 / 期限 / 終端の後は渡さない。token 値はログに出さない。"""
        # await の後は必ず _stop_known() で停止 / 期限を確かめてから答える。停止を知っていれば、要求の中身や取得の
        # 失敗理由に関わらず停止として返す（子は以後手元の token も渡さない）
        if self._stop_known():
            return self._token_refused()
        if not slot:
            return {"ok": False, "error": "slot is required"}
        await self._refresh_control(force=False)
        if self._stop_known():
            return self._token_refused()
        try:
            body = await self._client.get_connection_token(slot)
        except ExecutionTerminal:
            self._stop_reason = self._stop_reason or "terminal"
            return self._token_refused()
        except (RuntimeApiError, WorkflowError) as e:
            if isinstance(e, RuntimeApiError):
                self._stop_on_live_reject(e)
            if self._stop_known():
                return self._token_refused()
            return {"ok": False, "error": (getattr(e, "code", "") or type(e).__name__)[:200]}
        # 取得を待つ間に取消 / 期限 / 終端になっていれば渡さない（取消 / 終端は front に取り直して確かめる。
        # IPC は直列なので試行は 2 回まで。届かなければ手元の停止 / 期限だけで判断する）
        await self._refresh_control(force=True, attempts=2)
        if self._stop_known():
            return self._token_refused()
        token = body.get("access_token")
        if not isinstance(token, str) or not token:
            return {"ok": False, "error": "no token"}
        return {"ok": True, "access_token": token, "token_type": str(body.get("token_type") or "Bearer"),
                "expires_at": body.get("expires_at")}

    def _stop_known(self) -> bool:
        """停止要求 / 期限を停止理由に反映したうえで、停止しているか。"""
        self._check_deadline_now()
        return bool(self._stop_reason)

    def _token_refused(self) -> dict[str, Any]:
        """停止後の token 要求への応答。stop_reason を載せ、子は以後手元の token も渡さない。"""
        return {"ok": False, "error": f"execution {self._stop_reason}", "stop_reason": self._stop_reason}

    async def _on_audit(self, event: dict[str, Any]) -> dict[str, Any]:
        """子の監査を front へ保存し、ack（accepted / duplicates）だけを成功として返す。
        tool.invoked は ack の前後で取消 / 期限を確認する（期限後の write を承認しない）。観測は journal が durable に
        なってから承認する（journal に失敗したら承認しない = 監査保存失敗と同じ扱い）。"""
        etype = str(event.get("event_type") or "")
        if etype == "tool.invoked":
            await self._refresh_control(force=False)
            if self._stop_reason:
                return {"accepted": False, "error": f"execution {self._stop_reason}; no new tool calls"}
        try:
            res = await self._client.post_audit([event])
        except ExecutionTerminal:
            self._stop_reason = self._stop_reason or "terminal"
            return {"accepted": False, "error": "execution terminal"}
        except (RuntimeApiError, WorkflowError) as e:
            self._tally.persist_failures += 1  # 必須監査の保存失敗 = 正常成功を出さない
            await self._journal_tally()
            return {"accepted": False, "error": str(e)[:200]}
        eid = event.get("event_id")
        ok = eid in (res.get("accepted") or []) or eid in (res.get("duplicates") or [])
        if not ok:
            self._tally.persist_failures += 1
            await self._journal_tally()
            return {"accepted": False, "error": "not acknowledged"}
        self._tally.record(etype, str(eid), dict(event.get("metadata") or {}), reason=event.get("reason"))
        if not await self._journal_tally():
            self._tally.persist_failures += 1  # 観測を durable にできない = 再起動で失う → 承認しない
            await self._journal_tally()
            return {"accepted": False, "error": "observation journal not durable"}
        if etype == "tool.invoked":
            self._check_deadline_now()  # journal の遅延の後に再確認（期限後の write を承認しない）
            if self._stop_reason:
                self._tally.invoked.pop(str(eid), None)  # 承認しない呼出しは数えない（effects_unobserved にしない）
                await self._journal_tally()
                return {"accepted": False, "error": f"execution {self._stop_reason}; no new tool calls"}
        return {"accepted": True}

    async def _journal_tally(self) -> bool:
        """ack 済み観測を state に journal する（runner 再起動後に had_mutating_success / counts を 0 に戻さない）。
        書き込み（fsync）は event loop を塞がないよう thread で行う。"""
        if self._state is None:
            return True
        try:
            await asyncio.get_running_loop().run_in_executor(None, self._state.set, "tally", self._tally.to_dict())
            return True
        except OSError as e:
            logger.error("[%s] tally journal not written: %s", self.execution_id, type(e).__name__)
            return False

    def _stop_on_live_reject(self, e: RuntimeApiError) -> bool:
        """live な読み取りの 409（取消 / run の終端 / 期限）を停止理由に写す。写したら True。"""
        stop = _LIVE_REJECT_STOP_REASONS.get(e.code) if e.status == 409 else None
        if stop is None:
            return False
        self._stop_reason = self._stop_reason or stop
        return True

    def _check_deadline_now(self) -> None:
        """停止要求（SIGTERM / 期限切れ）を **停止理由に変換する唯一の場所**。ここから既存の協調停止経路
        （watchdog → `_terminate_group` → `_finish` → completion）に入る。停止要求を先に見るのは、Pod が消える方が差し迫っているため。"""
        if self._stop_reason:
            return
        if self._stop_requested:
            self._stop_reason = "stopped"
            return
        if self._agent_deadline is not None and _utc_now() >= self._agent_deadline:
            self._stop_reason = "deadline"

    async def _refresh_control(self, *, force: bool, attempts: Optional[int] = None) -> None:
        """取消 / 期限を確認する（期限はローカル時計、取消は runtime context を rate-limit 付きで再取得）。"""
        self._check_deadline_now()
        if self._stop_reason:
            return
        now = time.monotonic()
        if not force and now - self._last_context_check < self._cancel_poll:
            return
        self._last_context_check = now
        try:
            ctx = await self._client.get_context(attempts=attempts)
        except ExecutionTerminal:
            self._stop_reason = "terminal"
            return
        except (RuntimeApiError, WorkflowError):
            return  # 不達は次回。取消は executor の reconcile でも収束する
        if ctx.get("cancel_requested_at"):
            self._stop_reason = "cancel"
        if ctx.get("deadlines"):
            self._ctx["deadlines"] = ctx["deadlines"]
            self._set_deadlines(self._ctx)   # 起動後に確定した / 短くなった期限を採用（延長はしない）
            self._check_deadline_now()

    async def _watchdog(self, proc: asyncio.subprocess.Process) -> None:
        """ローカル期限は毎 tick 判定し、取消の HTTP 確認は別 task で行う（HTTP の遅延 / 再送で子の停止が遅れない）。"""
        poll: Optional[asyncio.Task] = None
        try:
            while proc.returncode is None:
                await asyncio.sleep(min(1.0, self._cancel_poll))
                self._check_deadline_now()
                if not self._stop_reason and (poll is None or poll.done()):
                    poll = asyncio.create_task(self._refresh_control(force=False))
                if self._stop_reason:
                    await self._terminate_group(proc)
                    return
        finally:
            if poll is not None and not poll.done():
                poll.cancel()

    async def _terminate_group(self, proc: asyncio.subprocess.Process) -> None:
        """Agent とその配下（新 session = プロセスグループ）を止める: SIGTERM → 猶予 → SIGKILL。リーダーの終了とは独立に
        グループの生存を確認してから回収に進む（配下が書き続けない）。"""
        pgid = proc.pid
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        if proc.returncode is None:
            try:
                await asyncio.wait_for(proc.wait(), timeout=self._grace)
            except asyncio.TimeoutError:
                pass
        deadline = time.monotonic() + self._grace
        while self._group_alive(pgid) and time.monotonic() < deadline:
            await asyncio.sleep(0.1)
        if self._group_alive(pgid):
            try:
                os.killpg(pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            deadline = time.monotonic() + self._grace
            while self._group_alive(pgid) and time.monotonic() < deadline:
                await asyncio.sleep(0.1)
        if self._group_alive(pgid):
            logger.error("[%s] agent process group %s survived SIGKILL; outputs will not be collected", self.execution_id, pgid)
            self._cleanup_uncertain = True
        if proc.returncode is None:
            await proc.wait()

    @staticmethod
    def _start_ticks(pid: int) -> Optional[int]:
        """/proc/<pid>/stat の starttime（boot からの clock ticks）。PID 再利用と見分けるための識別。"""
        try:
            with open(f"/proc/{pid}/stat", "rb") as f:
                stat_line = f.read().decode("utf-8", "replace")
            return int(stat_line[stat_line.rindex(")") + 2:].split()[19])
        except (OSError, ValueError, IndexError):
            return None

    @staticmethod
    def _group_members(pgid: int) -> list[tuple[int, Optional[int], int]]:
        """(pid, start_ticks, session id) of live (non-zombie) processes in the group。/proc が無ければ空。"""
        out: list[tuple[int, Optional[int], int]] = []
        try:
            names = os.listdir("/proc")
        except OSError:
            return out
        for name in names:
            if not name.isdigit():
                continue
            try:
                with open(f"/proc/{name}/stat", "rb") as f:
                    stat_line = f.read().decode("utf-8", "replace")
                fields = stat_line[stat_line.rindex(")") + 2:].split()
                if int(fields[2]) == pgid and fields[0] != "Z":
                    out.append((int(name), int(fields[19]), int(fields[3])))
            except (OSError, ValueError, IndexError):
                continue
        return out

    @classmethod
    def _group_alive(cls, pgid: int) -> bool:
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        # リーダーが zombie（未回収）でも killpg(0) は成功する。/proc で実際の生存メンバーを数える
        if not os.path.isdir("/proc"):
            return True
        return bool(cls._group_members(pgid))

    # ------------------------------------------------------------------
    async def _upload(self, state: _State, collected: list) -> list[dict[str, Any]]:
        out = []
        for c in collected:
            artifact_id = state.get_id(f"artifact:{c.source}:{c.path}")
            res = await self._client.upload_artifact(
                artifact_id=artifact_id, logical_name=c.logical_name, source=c.source, path=c.path, fmt=c.format,
                sha256=c.sha256, content=c.content, filename=Path(c.path).name)
            stored_digest = str(res.get("sha256") or c.sha256).lower()
            if stored_digest != c.sha256:
                raise WorkflowError(f"stored digest differs for {c.logical_name}")
            out.append({"artifact_id": artifact_id, "logical_name": c.logical_name, "path": c.path, "source": c.source,
                        "sha256": c.sha256, "size": c.size})
        return out

    async def _complete(self, state: _State, envelope: dict[str, Any], artifact_ids: list[str]) -> tuple[bool, bool]:
        """completion を同じ completion_id / payload で保存する。payload は送信前に永続化（再起動でも同じ内容を再送。
        既に同じ payload があるなら書き直さない）。所有権を証明していなければ送らない。
        戻り値 (saved, already_terminal)。"""
        if not self._owns(state):
            logger.error("[%s] ownership was never proven; refusing to send completion", self.execution_id)
            return False, False
        completion_id = state.get_id("completion_id")
        payload = {"envelope": envelope, "output_artifact_ids": list(artifact_ids)}
        if state.data.get("completion") != payload:
            state.set("completion", payload)
        try:
            res = await self._client.post_completion(completion_id=completion_id, envelope=envelope,
                                                     output_artifact_ids=artifact_ids)
        except ExecutionTerminal:
            logger.warning("[%s] completion rejected: execution already terminal (kept the existing result)", self.execution_id)
            return False, True
        except (RuntimeApiError, WorkflowError) as e:
            logger.error("[%s] completion could not be saved: %s", self.execution_id, e)
            return False, False
        logger.info("[%s] completion saved (existing=%s)", self.execution_id, bool(res.get("existing")))
        return True, False


async def arun(entrypoint: str, *, env: Optional[Mapping[str, str]] = None, workspace: Optional[str] = None,
               transport: Optional[httpx.AsyncBaseTransport] = None, **kwargs: Any) -> WorkflowResult:
    runner = WorkflowRunner(entrypoint=entrypoint, env=env or os.environ, workspace=workspace, transport=transport, **kwargs)
    return await runner.run()


def run(entrypoint: str, *, env: Optional[Mapping[str, str]] = None, workspace: Optional[str] = None,
        exit_process: bool = True) -> WorkflowResult:
    """顧客 image の起動 command から呼ぶ入口: `python -c "from agenticstar_platform.workflow import run; run('my_agent.main:run')"`。
    設定不正は Agent を呼ばずに終了コード 3、terminal を保存できなければ 2。SIGTERM（Pod 停止）は協調停止
    （`failed/runner_stopped` の completion）に変換する。それ以外の障害は例外のまま非0 で終わる
    （executor が効果不明 = `failed/agent_exit_nonzero` として hold に収束させる。SDK は終了コードを保証しない）。"""
    env_map = env if env is not None else os.environ
    try:
        result = asyncio.run(arun(entrypoint, env=env_map, workspace=workspace, stop_on_sigterm=exit_process))
    except WorkflowConfigError as e:
        logger.error("workflow config error: %s", e)
        if exit_process:
            sys.exit(3)
        raise
    if exit_process:
        sys.exit(result.exit_code)
    return result
