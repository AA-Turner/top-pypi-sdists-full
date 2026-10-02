"""front runtime 保存 API（`/api/mp/runtime/v1/executions/{execution_id}` 配下、marketplace-3.0 00 §5 / 04 §3）の HTTP client。

- 認証は executor が発行した execution 限定 JWT（Bearer）。SDK は署名鍵を持たない
- 到達性 / 5xx（500 含む: front は永続化の予期しない失敗を 500 にする）/ timeout は **期限内で** 有界に再送し、4xx は契約違反として
  即座に返す（409 terminal は「既に終端」= 再実行しない）。再送は同じ event / artifact / completion の ID と payload
- body / token / env 値をログに出さない
"""
from __future__ import annotations

import asyncio
import logging
import random
import re
import time
from typing import Any, Callable, Optional
from urllib.parse import quote

import httpx

from .errors import ExecutionTerminal, RuntimeApiError, WorkflowError

logger = logging.getLogger(__name__)

RETRY_STATUSES = (500, 502, 503, 504)
COMPLETION_RESERVE_SECONDS = 10.0   # context / artifact の要求が回収期限ぎりぎりまで予算を使い切らないための取り置き
AUDIT_RESERVE_SECONDS = 3.0         # 最後の tool.effect 等の監査は期限近くでも 1 回は試みる（completion の分だけ残す）
CONNECTION_SLOT_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,63}")   # front の接続 slot と同じ形（fullmatch で使う）


class RuntimeClient:
    def __init__(self, base_url: str, execution_id: str, token: str, *, timeout: float = 30.0,
                 transport: Optional[httpx.AsyncBaseTransport] = None, max_attempts: int = 6,
                 deadline: Optional[Callable[[], Optional[float]]] = None):
        """deadline: 残り秒数を返す callable（None = 無期限）。再送はこの残り時間を超えない。"""
        self._base = base_url.rstrip("/") + "/" + execution_id
        self._client = httpx.AsyncClient(timeout=timeout, transport=transport,
                                         headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
        self._max_attempts = max_attempts
        self._deadline = deadline
        self._timeout = float(timeout)
        self.execution_id = execution_id

    async def aclose(self) -> None:
        await self._client.aclose()

    # ----- low level -----
    async def _request(self, method: str, path: str, *, json_body: Any = None, files: Any = None, data: Any = None,
                       attempts: Optional[int] = None, reserve: float = 0.0) -> httpx.Response:
        """reserve: 残り予算から取り置く秒数（completion 以外は completion の分を残す）。要求全体（接続 + 本文の読み書き）を
        残り予算の絶対 timeout で包む（httpx の timeout は操作単位なので、それだけでは期限を越えうる）。"""
        url = self._base + path
        last: Optional[Exception] = None
        n = attempts or self._max_attempts
        for attempt in range(n):
            remaining = self._deadline() if self._deadline else None
            if remaining is not None:
                remaining -= reserve
            if remaining is not None and remaining <= 0:
                # 回収期限を過ぎた要求は出さない（front も deadline_exceeded で拒否する）。再送で期限を跨がない
                if last is None:
                    last = RuntimeApiError(0, "deadline_exceeded", "collection deadline passed before the request")
                break
            timeout = self._timeout if remaining is None else max(0.05, min(self._timeout, remaining))
            try:
                resp = await asyncio.wait_for(
                    self._client.request(method, url, json=json_body, files=files, data=data, timeout=timeout),
                    timeout=None if remaining is None else remaining)
            except asyncio.TimeoutError as e:
                last = httpx.TimeoutException("absolute deadline") if not isinstance(e, httpx.TimeoutException) else e
            except httpx.RequestError as e:   # 到達性 / timeout / 本文の decode 失敗（DecodingError は TransportError ではない）
                last = e
            else:
                if resp.status_code in RETRY_STATUSES:
                    last = RuntimeApiError(resp.status_code, _code(resp), "retryable")
                else:
                    return resp
            if attempt < n - 1:
                delay = min(30.0, 0.5 * (2 ** attempt)) * (0.5 + random.random())
                remaining = self._deadline() if self._deadline else None
                if remaining is not None and remaining - reserve <= delay:
                    break  # 期限（取り置き分を除く）を越えてまで再送 / backoff しない
                await asyncio.sleep(delay)
        if isinstance(last, RuntimeApiError):
            raise last
        raise RuntimeApiError(0, "unreachable", type(last).__name__ if last else "unknown")

    @staticmethod
    def _body(resp: httpx.Response) -> dict[str, Any]:
        """2xx 応答の本文。JSON でない（proxy / ingress が本文を差し替えた等）なら契約外として API エラーにする。
        ValueError をそのまま外へ出すと、呼び出し側（runner）の RuntimeApiError / WorkflowError の処理を素通りする。"""
        try:
            body = resp.json()
        except ValueError:
            raise RuntimeApiError(resp.status_code, "invalid_response", "response body is not JSON") from None
        return body if isinstance(body, dict) else {}

    @staticmethod
    def _raise_for(resp: httpx.Response) -> None:
        """**2xx だけを成功とする**。3xx（ingress / SSO が login へ 302 する等）を成功にすると、body が
        JSON でない応答を「front が保存した」と誤認して completion 無しで終わる（front は redirect を返さない）。"""
        if 200 <= resp.status_code < 300:
            return
        code = _code(resp)
        if resp.status_code == 409 and code == "terminal":
            raise ExecutionTerminal("execution is already terminal")
        raise RuntimeApiError(resp.status_code, code or ("unexpected_redirect" if resp.status_code < 400 else ""),
                              _message(resp))

    # ----- API -----
    async def get_context(self, *, attempts: Optional[int] = None) -> dict[str, Any]:
        resp = await self._request("GET", "/context", attempts=attempts, reserve=COMPLETION_RESERVE_SECONDS)
        self._raise_for(resp)
        return self._body(resp)

    async def get_connection_token(self, slot: str) -> dict[str, Any]:
        """起動時に束ねた接続 slot の access token を取り直す（{access_token, token_type, expires_at}）。
        起動時に env で渡る token は 1 時間程度で切れうるので、長い実行ではこちらで取り直す。token はログに出さない。
        試行は 2 回まで（runner の IPC は直列なので、取得を待つ間 Agent の監査 / 取消確認が止まる。失敗は Agent に返す）。"""
        if not isinstance(slot, str) or not CONNECTION_SLOT_RE.fullmatch(slot):
            # front と同じ形だけ送る（"." / ".." は quote しても残り URL の正規化で別の API パスに届く。
            # 符号化できない文字は quote が例外を出して runner の IPC ループから抜ける）
            raise WorkflowError(f"invalid connection slot {slot!r}")
        resp = await self._request("GET", f"/connections/{quote(slot, safe='')}/token", attempts=2,
                                   reserve=COMPLETION_RESERVE_SECONDS)
        self._raise_for(resp)
        return self._body(resp)

    async def download_artifact(self, artifact_id: str) -> bytes:
        resp = await self._request("GET", f"/artifacts/{artifact_id}/content", reserve=COMPLETION_RESERVE_SECONDS)
        self._raise_for(resp)
        return resp.content

    async def post_audit(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        """{accepted: [...], duplicates: [...]}。重複（同じ event_id）は保存済み扱い。"""
        resp = await self._request("POST", "/audit", json_body={"events": events}, reserve=AUDIT_RESERVE_SECONDS)
        self._raise_for(resp)
        return self._body(resp)

    async def upload_artifact(self, *, artifact_id: str, logical_name: str, source: str, path: str, fmt: str,
                              sha256: str, content: bytes, filename: str) -> dict[str, Any]:
        resp = await self._request(
            "POST", "/artifacts",
            data={"artifact_id": artifact_id, "logical_name": logical_name, "source": source, "path": path,
                  "format": fmt, "sha256": sha256},
            files={"file": (filename, content, "application/octet-stream")}, reserve=COMPLETION_RESERVE_SECONDS)
        self._raise_for(resp)
        return self._body(resp)

    async def post_completion(self, *, completion_id: str, envelope: dict[str, Any],
                              output_artifact_ids: list[str]) -> dict[str, Any]:
        resp = await self._request("POST", "/completion", json_body={
            "completion_id": completion_id, "completion_envelope": envelope, "output_artifact_ids": output_artifact_ids})
        self._raise_for(resp)
        try:
            return self._body(resp)
        except RuntimeApiError:
            # ここに来るのは _raise_for を通った 2xx だけ = front は保存済み。本文が読めなくても保存の事実は変わらない
            # （失敗にすると runner は保存済みの terminal に別の envelope を送り直そうとする）
            logger.warning("completion accepted (%s) but the response body is not JSON", resp.status_code)
            return {}


def _code(resp: httpx.Response) -> str:
    try:
        body = resp.json()
        return str(body.get("code") or "") if isinstance(body, dict) else ""
    except ValueError:
        return ""


def _message(resp: httpx.Response) -> str:
    try:
        body = resp.json()
        return str(body.get("message") or "")[:200] if isinstance(body, dict) else ""
    except ValueError:
        return ""


def monotonic() -> float:
    return time.monotonic()
