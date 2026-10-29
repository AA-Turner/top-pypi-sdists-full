"""Agent entrypoint を実行する子プロセス（`python -m agenticstar_platform.workflow.child`）。

親 runner が専用 fd（env `ASTER_WORKFLOW_IPC_IN` / `ASTER_WORKFLOW_IPC_OUT`）で spec（JSON 1 行）と制御チャネルを渡す。
stdout / stderr は Agent の通常出力（本文は制御チャネルに混ざらない）。終了コード: 0 = return、1 = 例外、3 = 設定不正。
例外は既定でクラス名だけを stderr に出す（本文 / token を Pod ログへ写さない）。`ASTER_WORKFLOW_DEBUG_TRACEBACK=1` で全文。
クラス名の後ろに、原因の連鎖（クラス名・SDK の error_code / HTTP status・通信先のホスト名だけ）を 1 行で添える
（devdocs 3.2req reviews 06: `SecurityAPIError` だけでは、egress のサイドカーの 503 か Azure の障害かが分からなかった）。
同じ原因の連鎖は done の `failure_summary` で runner に渡し、終了時の報告（envelope の `completion_report.comment`）にも載る
（3.2.1。`ASTER_WORKFLOW_DEBUG_TRACEBACK=1` でも報告に載るのは連鎖だけで、traceback は載せない）。
"""
from __future__ import annotations

import asyncio
import importlib
import json
import os
import re
import sys
import traceback

from .context import WorkflowContext, _Ipc


_MAX_CAUSES = 5
_ERROR_CODE_RE = re.compile(r"[A-Z][A-Z0-9_]{0,63}")   # SDK の error_code の語の形 (REQUEST_ERROR など)


def _safe_failure_summary(exc: BaseException) -> str:
    """例外の連鎖を、本文を含めずに 1 行にする: クラス名と、あれば SDK の error_code / HTTP status と通信先のホスト名。

    例: ``SecurityAPIError(error_code=REQUEST_ERROR) <- ProxyError(host=xxx.services.ai.azure.com)``。
    文言 (応答の本文・URL の path / query・token が入りうる) は出さない。error_code は SDK の例外のときだけ。
    要約を作る途中で例外が出ても (属性の読み取りで想定外の例外を上げる例外クラスなど)、クラス名だけを返す
    (失敗の報告 = 制御チャネルの done を止めない)。
    """
    try:
        return _failure_chain(exc)
    except Exception:  # noqa: BLE001
        return type(exc).__name__


def _failure_chain(exc: BaseException) -> str:
    parts = []
    seen = set()
    cur: BaseException | None = exc
    while cur is not None and id(cur) not in seen and len(parts) < _MAX_CAUSES:
        seen.add(id(cur))
        parts.append(_describe_exception(cur))
        cur = cur.__cause__ or (None if cur.__suppress_context__ else cur.__context__)
    return " <- ".join(parts)


def _describe_exception(exc: BaseException) -> str:
    """例外 1 件を ``クラス名(error_code=..., status=..., host=...)`` にする (出せる属性が無ければクラス名だけ)。"""
    attrs = []
    # error_code は SDK 自身の例外 (SDK が決まった語を入れる) のときだけ。Agent の例外の属性は文言と同じ扱いで出さない。
    # SDK の例外クラスを Agent が自分の値で作ることもあるので、SDK の語の形 (大文字の snake_case) に合うものだけ出す
    code = _attr(exc, "error_code") if type(exc).__module__.startswith("agenticstar_platform.") else None
    if isinstance(code, str) and _ERROR_CODE_RE.fullmatch(code):
        attrs.append(f"error_code={code}")
    status = _attr(exc, "status_code")
    if isinstance(status, int) and not isinstance(status, bool):
        attrs.append(f"status={status}")
    host = _request_host(exc)
    if isinstance(host, str) and host:
        attrs.append(f"host={host}")
    return type(exc).__name__ + (f"({', '.join(attrs)})" if attrs else "")


def _request_host(exc: BaseException):
    try:
        return exc.request.url.host  # httpx の例外 (要求が付いていないと RuntimeError)
    except Exception:  # noqa: BLE001
        return None


def _attr(obj: object, name: str):
    try:
        return getattr(obj, name, None)
    except Exception:  # noqa: BLE001 — __getattr__ が AttributeError 以外を上げる例外クラス
        return None


def _load_entrypoint(ref: str):
    if ":" not in ref:
        raise ValueError("entrypoint must be 'module.path:function'")
    mod_name, func_name = ref.split(":", 1)
    module = importlib.import_module(mod_name)
    func = getattr(module, func_name, None)
    if func is None or not callable(func):
        raise ValueError(f"entrypoint {ref} not found")
    return func


async def _main() -> int:
    try:
        in_fd = int(os.environ["ASTER_WORKFLOW_IPC_IN"])
        out_fd = int(os.environ["ASTER_WORKFLOW_IPC_OUT"])
    except (KeyError, ValueError):
        sys.stderr.write("workflow child: control channel not provided\n")
        return 3
    raw = b""
    while not raw.endswith(b"\n"):
        chunk = os.read(in_fd, 65536)
        if not chunk:
            break
        raw += chunk
    try:
        spec = json.loads(raw)
        if not isinstance(spec, dict):
            raise ValueError("spec must be an object")
    except ValueError as e:
        sys.stderr.write(f"invalid runner spec: {type(e).__name__}\n")
        return 3
    ipc = _Ipc(in_fd, out_fd)
    try:
        func = _load_entrypoint(spec["entrypoint"])
        context = WorkflowContext(spec, ipc)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"entrypoint unavailable: {type(e).__name__}\n")
        await ipc.call("done", status="config_error", error_class=type(e).__name__)
        return 3
    try:
        result = func(context)
        if asyncio.iscoroutine(result):
            await result
    except Exception as e:  # noqa: BLE001
        summary = _safe_failure_summary(e)
        if os.environ.get("ASTER_WORKFLOW_DEBUG_TRACEBACK") == "1":
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(f"agent entrypoint failed: {type(e).__name__} [{summary}]\n")
        await ipc.call("done", status="error", error_class=type(e).__name__, failure_summary=summary)
        return 1
    await ipc.call("done", status="ok")
    return 0


def main() -> None:
    sys.exit(asyncio.run(_main()))


if __name__ == "__main__":
    main()
