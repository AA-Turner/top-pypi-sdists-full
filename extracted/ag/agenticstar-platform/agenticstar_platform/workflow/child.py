"""Agent entrypoint を実行する子プロセス（`python -m agenticstar_platform.workflow.child`）。

親 runner が専用 fd（env `ASTER_WORKFLOW_IPC_IN` / `ASTER_WORKFLOW_IPC_OUT`）で spec（JSON 1 行）と制御チャネルを渡す。
stdout / stderr は Agent の通常出力（本文は制御チャネルに混ざらない）。終了コード: 0 = return、1 = 例外、3 = 設定不正。
例外は既定でクラス名だけを stderr に出す（本文 / token を Pod ログへ写さない）。`ASTER_WORKFLOW_DEBUG_TRACEBACK=1` で全文。
"""
from __future__ import annotations

import asyncio
import importlib
import json
import os
import sys
import traceback

from .context import WorkflowContext, _Ipc


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
        if os.environ.get("ASTER_WORKFLOW_DEBUG_TRACEBACK") == "1":
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(f"agent entrypoint failed: {type(e).__name__}\n")
        await ipc.call("done", status="error", error_class=type(e).__name__)
        return 1
    await ipc.call("done", status="ok")
    return 0


def main() -> None:
    sys.exit(asyncio.run(_main()))


if __name__ == "__main__":
    main()
