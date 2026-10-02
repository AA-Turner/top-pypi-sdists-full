"""顧客 Agent の entrypoint に渡す `context`（marketplace-3.0 03 §2）。

read-only の相関、parameters、input/work/output_dir、operation_key、監査（tool.invoked / tool.effect / tool.denied）、
取消 / 期限の確認、permitted skip の宣言を提供する。gate を決定するメソッドや任意 DB 接続は提供しない。
実体は子プロセス側にあり、監査と取消確認は親 runner へ IPC で委譲する。

IPC は stdin / stdout ではなく **専用の fd**（親が pass_fds で渡す。要求 = fd `ASTER_WORKFLOW_IPC_OUT`、応答 = `ASTER_WORKFLOW_IPC_IN`）
を使い、1 行 1 JSON object、各要求に `id` を付けて応答を対応付ける。Agent コードや配下プロセスの stdout / stderr は制御チャネルに
混ざらない。
"""
from __future__ import annotations

import asyncio
import itertools
import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional

from .envelope import PRE_ACTION_SKIP_REASONS, SKIP_REASONS
from .errors import AuditNotPersisted, WorkflowError

MUTATING_EFFECT_KINDS = ("write", "create", "update", "delete", "send", "mutate")
READ_EFFECT_KINDS = ("read", "list", "query", "fetch")
MAX_LINE = 256 * 1024


class _Ipc:
    """子 → 親: 1 行 JSON（`id` 付き）を書き、親の応答（同じ `id`）を待つ。応答は 1 本の reader task が受け取り id で配る。
    要求の途中で cancel されても他の要求が古い応答を取り違えない（id 不一致の応答は捨てる）。"""

    def __init__(self, in_fd: int, out_fd: int):
        self._in = os.fdopen(in_fd, "rb", buffering=0)
        self._out = os.fdopen(out_fd, "wb", buffering=0)
        self._ids = itertools.count(1)
        self._pending: dict[int, asyncio.Future] = {}
        self._reader: Optional[asyncio.Task] = None
        self._write_lock = threading.Lock()  # frame 単位の直列化は thread 側で保証（asyncio cancel で途中解放されない）
        # 親の応答に stop_reason があれば呼ぶ（取り消された要求の応答でも。WorkflowContext が停止を固定する）
        self.on_stop: Optional[Callable[[], None]] = None

    def _ensure_reader(self) -> None:
        if self._reader is None:
            self._reader = asyncio.create_task(self._read_loop())

    async def _read_loop(self) -> None:
        loop = asyncio.get_running_loop()
        buf = b""
        while True:
            chunk = await loop.run_in_executor(None, self._in.read, 65536)
            if not chunk:
                for fut in self._pending.values():
                    if not fut.done():
                        fut.set_exception(WorkflowError("runner closed the control channel"))
                return
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                try:
                    msg = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(msg, dict):
                    continue
                if msg.get("stop_reason") and self.on_stop is not None:
                    self.on_stop()   # 待ち手がいない (取り消された) 要求の応答でも、親が知っている停止は捨てない
                fut = self._pending.pop(int(msg.get("id") or 0), None)
                if fut is not None and not fut.done():
                    fut.set_result(msg)

    def _write_frame(self, line: bytes) -> None:
        """1 frame を **thread lock の中で最後まで** 書く。呼出し側の asyncio task が cancel されても書きかけの frame に
        別 frame が割り込まない（PIPE_BUF を超える frame でも壊れない）。"""
        with self._write_lock:
            view = memoryview(line)
            while view:
                n = self._out.write(view)
                view = view[n or 0:]

    async def call(self, op: str, **payload: Any) -> dict[str, Any]:
        self._ensure_reader()
        rid = next(self._ids)
        line = json.dumps({"id": rid, "op": op, **payload}, ensure_ascii=False).encode("utf-8") + b"\n"
        if len(line) > MAX_LINE:
            raise WorkflowError("control message too large")
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._pending[rid] = fut
        try:
            try:
                await asyncio.get_running_loop().run_in_executor(None, self._write_frame, line)
            except (OSError, ValueError) as e:   # BrokenPipeError / 閉じた pipe: 親が制御 channel を閉じた
                raise WorkflowError("runner closed the control channel") from e
            return await fut
        finally:
            self._pending.pop(rid, None)


class AuditApi:
    """監査の送信窓口。`tool_invoked` は **保存 ack を待ってから** 戻る（ack が無ければ AuditNotPersisted = その操作へ進めない）。"""

    def __init__(self, ipc: _Ipc):
        self._ipc = ipc

    async def _send(self, event_type: str, *, decision: str = "ok", reason: Optional[str] = None,
                    metadata: Optional[dict[str, Any]] = None) -> str:
        eid = f"{event_type.replace('.', '-')}-{uuid.uuid4()}"
        meta = {k: v for k, v in (metadata or {}).items() if isinstance(v, (str, int, float, bool))}
        reply = await self._ipc.call("audit", event={"event_id": eid, "event_type": event_type, "decision": decision,
                                                     "reason": reason, "metadata": meta,
                                                     "occurred_at": datetime.now(timezone.utc).isoformat()})
        if not reply.get("accepted"):
            raise AuditNotPersisted(f"{event_type} could not be persisted: {reply.get('error') or 'unknown'}")
        return eid

    async def tool_invoked(self, tool: str, *, effect_kind: str, action_ref: Optional[str] = None,
                           target: Optional[str] = None, **extra: Any) -> str:
        """外部 read / write の **前** に呼ぶ。戻り値は event_id（action_ref 未指定時の effect の対応キー）。
        ack 無し（保存失敗 / 取消 / 期限後）では外部 write を開始してはならない（03 §3）。"""
        if effect_kind not in MUTATING_EFFECT_KINDS and effect_kind not in READ_EFFECT_KINDS:
            raise ValueError(f"unknown effect_kind {effect_kind}")
        meta = {"tool": tool, "effect_kind": effect_kind, **extra}
        if action_ref:
            meta["action_ref"] = action_ref
        if target:
            meta["target"] = target
        return await self._send("tool.invoked", metadata=meta)

    async def tool_effect(self, invoked_event_id: str, *, status: str = "ok", count: Optional[int] = None,
                          action_ref: Optional[str] = None, **extra: Any) -> str:
        """外部操作の結果を **呼出し（tool_invoked の戻り値）に** 対応付ける。status: ok / failed / unknown
        （結果不明は unknown = 効果不明として hold）。action_ref は外部の冪等キーで、集計の対応付けには使わない。"""
        meta = {"invoked_event_id": invoked_event_id, "action_ref": action_ref or invoked_event_id, "status": status, **extra}
        if count is not None:
            meta["count"] = int(count)
        return await self._send("tool.effect", decision="ok" if status in ("ok", "success") else "error", metadata=meta)

    async def tool_denied(self, tool: str, *, reason: str, reason_code: str = "tool_denied", effect_kind: str = "write",
                          **extra: Any) -> str:
        return await self._send("tool.denied", decision="denied", reason=reason,
                                metadata={"tool": tool, "effect_kind": effect_kind, "reason_code": reason_code, **extra})


# 期限の分からない token（PAT / 上流が期限を返さなかった）も、この間隔で取り直す（期限切れの値を返し続けない）
UNKNOWN_EXPIRY_REFRESH_SECONDS = 600.0


def _consume_result(task: "asyncio.Task[Any]") -> None:
    """呼び出し元が取り消された後に終わった task の例外を回収する（未回収の警告を出さない）。"""
    if not task.cancelled():
        task.exception()


def _token_expired(expires_at: Any) -> bool:
    """期限を過ぎたか。期限なし / 読めない値は過ぎたと言えない（読めない値は取り直しの判定 _token_expiring 側で扱う）。"""
    if expires_at in (None, ""):
        return False
    try:
        dt = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
    except ValueError:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt <= datetime.now(timezone.utc)


def _token_fresh(token: Mapping[str, Any], fetched_at: float, min_ttl: float) -> bool:
    """手元の token をそのまま返してよいか。期限が分からない token は取得から UNKNOWN_EXPIRY_REFRESH_SECONDS まで。"""
    if token.get("expires_at") in (None, ""):
        return time.monotonic() - fetched_at < UNKNOWN_EXPIRY_REFRESH_SECONDS
    return not _token_expiring(token.get("expires_at"), min_ttl)


def _token_expiring(expires_at: Any, min_ttl: float) -> bool:
    """期限まで min_ttl 秒を切ったか。期限なし (None) は切れない。読めない値は切れたとみなす (取り直す)。"""
    if expires_at in (None, ""):
        return False
    try:
        dt = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
    except ValueError:
        return True
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (dt - datetime.now(timezone.utc)).total_seconds() < min_ttl


class WorkflowContext:
    """Agent entrypoint が受け取る read-only の実行文脈。"""

    def __init__(self, spec: dict[str, Any], ipc: _Ipc):
        self._spec = spec
        self._ipc = ipc
        self.execution_id: str = spec["execution_id"]
        self.project_id: str = spec["project_id"]
        self.run_id: str = spec["run_id"]
        self.agent_id: str = spec["agent_id"]
        self.marketplace_agent_id: str = spec["marketplace_agent_id"]
        self.root_execution_id: str = spec["root_execution_id"]
        self.entry_ref: str = spec["entry_ref"]
        self.operation_key: str = spec["operation_key"]
        self.attempt: int = int(spec["attempt"])
        self.effect_mode: str = spec["effect_mode"]
        self.parameters: Mapping[str, Any] = MappingProxyType(dict(spec.get("parameters") or {}))
        self.connections: Mapping[str, str] = MappingProxyType(dict(spec.get("connections") or {}))
        self.input_dir = Path(spec["input_dir"])
        self.work_dir = Path(spec["work_dir"])
        self.output_dir = Path(spec["output_dir"])
        self.manifest: Mapping[str, Any] = MappingProxyType(dict(spec.get("manifest") or {}))
        self.deadlines: Mapping[str, Optional[str]] = MappingProxyType(dict(spec.get("deadlines") or {}))
        self.audit = AuditApi(ipc)
        self._last_check = 0.0
        self._stopped = False
        self._tokens: dict[str, tuple[dict[str, Any], float]] = {}   # slot -> (token, 取得時刻 monotonic)
        self._token_lock = asyncio.Lock()   # connection_token を直列にする（await の間に手元の値が捨てられても返さない）
        self._bg_tasks: set[asyncio.Task[Any]] = set()   # 呼び出し元が取り消された後も走る task への参照
        ipc.on_stop = self._latch_stop   # 親の応答に載った停止は、どの op の応答でも固定する
        self._token_refusals: dict[str, int] = {}   # slot -> 取り直しを断られた回数（渡す直前に変わっていたら渡さない）

    def _latch_stop(self) -> None:
        self._stopped = True

    def deadline_remaining(self) -> Optional[float]:
        """Agent の実行期限（runner が回収猶予を差し引いた値）までの秒数（None = 不明）。"""
        raw = self._spec.get("agent_deadline") or self.deadlines.get("execution")
        if not raw:
            return None
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except ValueError:
            return None
        return (dt - datetime.now(timezone.utc)).total_seconds()

    async def is_cancel_requested(self, *, max_age: float = 5.0) -> bool:
        """取消 / 期限を親に確認する。取消後は新しい tool 呼出しを始めない。"""
        if self._stopped:
            return True
        now = time.monotonic()
        if now - self._last_check < max_age:
            return False
        # 確認と停止の固定は shield した task で最後まで行う（呼び出し元が取り消されても、届いた停止を捨てない）。
        # 返すのは再開した時点の停止（並行する確認が先に停止を固定していれば、それも返す）
        await asyncio.shield(self._run_in_background(self._check_control(now)))
        return self._stopped

    def _run_in_background(self, coro: Any) -> "asyncio.Task[Any]":
        task = asyncio.ensure_future(coro)
        self._bg_tasks.add(task)
        task.add_done_callback(self._bg_task_done)
        return task

    def _bg_task_done(self, task: "asyncio.Task[Any]") -> None:
        self._bg_tasks.discard(task)
        _consume_result(task)

    async def _check_control(self, now: float) -> None:
        reply = await self._ipc.call("check")
        self._last_check = now
        # 一度立った停止は戻さない（並行する呼び出しの古い確認結果で消さない）
        self._stopped = self._stopped or bool(reply.get("stop_reason"))

    async def connection_token(self, slot: str, *, min_ttl: float = 300.0) -> Mapping[str, Any]:
        """接続 slot の access token（{access_token, token_type, expires_at}）。

        起動時に env で渡る token は 1 時間程度で切れうる。長い実行で外部 API を呼ぶ前はこちらを使う。期限まで
        `min_ttl` 秒を切るまでは前回の値を返し、切ったら runner 経由で front から取り直す（期限の分からない token は
        `UNKNOWN_EXPIRY_REFRESH_SECONDS` ごとに取り直す）。取消 / 期限後・起動時に束ねていない slot は WorkflowError。"""
        slot = str(slot)
        # ロックを持つ処理は shield した task で最後まで行う: 呼び出し元が取り消されても、取り直しの結果（手元の値の
        # 破棄 / 停止の固定）を反映してからロックを離す（IPC は取り消された要求の応答を捨てる）
        waiter: list[asyncio.Future[Any]] = []
        outer = asyncio.shield(self._run_in_background(self._connection_token_serial(slot, min_ttl, waiter)))
        waiter.append(outer)   # task の最初の step より前に入る（ensure_future は次の周回で走る）
        refusals = await outer
        # 最後の await の後、渡す直前に同期で確かめる（task の完了から再開までの間の停止 / 期限 / 取り直しも含む）
        return self._hand_out(slot, refusals)

    async def _connection_token_serial(self, slot: str, min_ttl: float, waiter: list) -> int:
        """手元の値を確かめるか取り直して手元に置き、その時点の拒否回数を返す（渡すのは呼び出し元の _hand_out）。"""
        async with self._token_lock:
            if waiter and waiter[0].cancelled():
                # ロック待ちの間に呼び出し元が取り消された（取消は shield の外側の future に同期で届く）: 取り直さない
                raise asyncio.CancelledError()
            if self._stopped:
                raise WorkflowError("execution is cancelled or past its deadline; no connection token")
            entry = self._tokens.get(slot)
            if entry is not None and _token_fresh(*entry, min_ttl):
                # 手元の値を返す時も、取消の後は渡さない（runner に rate-limit 付きで問い合わせる）
                if await self.is_cancel_requested():
                    raise WorkflowError("execution is cancelled or past its deadline; no connection token")
                if _token_fresh(*entry, min_ttl):   # 確認を待つ間に期限まで min_ttl を切っていれば取り直す
                    return self._token_refusals.get(slot, 0)
            # 取り直しの結果（断られた時の破棄も）は、呼び出し元が取り消されても shield した task が必ず反映する
            reply = await self._ipc.call("connection_token", slot=slot)
            if not reply.get("ok"):
                # runner が停止を知っていれば以後は渡さない
                if reply.get("stop_reason"):
                    self._stopped = True
                self._refuse(slot)
                raise WorkflowError(f"connection token unavailable for {slot!r}: {reply.get('error') or 'unknown'}")
            token = {"access_token": reply["access_token"], "token_type": reply.get("token_type") or "Bearer",
                     "expires_at": reply.get("expires_at")}
            if _token_expired(token["expires_at"]):
                # runner が取消を確かめる間に期限を過ぎた（取り直した結果が使えない）: 断られた時と同じく前の値も渡さない
                self._refuse(slot)
                raise WorkflowError(f"connection token for {slot!r} expired before it could be handed out")
            self._tokens[slot] = (token, time.monotonic())
            return self._token_refusals.get(slot, 0)

    def _refuse(self, slot: str) -> None:
        """取り直しが使える値を返さなかった: 手元の値を捨て、並行して渡しかけている呼び出しにも渡させない。"""
        self._tokens.pop(slot, None)
        self._token_refusals[slot] = self._token_refusals.get(slot, 0) + 1

    def _hand_out(self, slot: str, refusals: int) -> Mapping[str, Any]:
        """渡す直前（最後の await の後）に同期で確かめて、手元の最新の値を渡す: 停止 / Agent の期限、その間に後の呼び出しが
        取り直しを断られていないか（断られた値は渡さない。後の呼び出しが取り直しに成功していれば新しい方を渡す）、
        token 自体の期限。"""
        remaining = self.deadline_remaining()
        if self._stopped or (remaining is not None and remaining <= 0):
            raise WorkflowError("execution is cancelled or past its deadline; no connection token")
        entry = self._tokens.get(slot)
        if entry is None or self._token_refusals.get(slot, 0) != refusals:
            raise WorkflowError(f"connection token for {slot!r} was refused while being handed out")
        token = entry[0]
        if _token_expired(token.get("expires_at")):
            raise WorkflowError(f"connection token for {slot!r} has expired")
        return MappingProxyType(dict(token))

    async def ensure_can_act(self) -> None:
        """外部操作の前に呼ぶ: 取消 / 期限後なら WorkflowError。"""
        if await self.is_cancel_requested(max_age=0.0):
            raise WorkflowError("execution is cancelled or past its deadline; no new tool calls")

    async def skip(self, reason: str) -> None:
        """認定された「対象なし」理由で工程を skip する（00 §7: no_target / not_applicable / nothing_to_do）。
        front はこの 3 理由だけ次工程へ進める。"""
        if reason not in SKIP_REASONS:
            raise ValueError(f"skip reason must be one of {SKIP_REASONS}")
        reply = await self._ipc.call("skip", reason=reason)
        if not reply.get("ok"):
            raise WorkflowError(f"skip not recorded: {reply.get('error') or 'unknown'}")

    async def policy_unavailable(self) -> None:
        """外部行為の **前** に policy / 認可を照合できなかった（`skipped/policy_unavailable`）。front は budget 内で再照合し、
        上限で人待ちにする。行為を始めてから呼ばない（始めた後の不明は tool_effect(status="unknown")）。"""
        reply = await self._ipc.call("skip", reason=PRE_ACTION_SKIP_REASONS[0])
        if not reply.get("ok"):
            raise WorkflowError(f"skip not recorded: {reply.get('error') or 'unknown'}")

    async def log(self, message: str) -> None:
        await self._ipc.call("log", message=str(message)[:2000])
