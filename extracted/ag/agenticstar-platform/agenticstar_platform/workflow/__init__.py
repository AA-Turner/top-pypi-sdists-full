"""`agenticstar_platform.workflow` — MP 3.0 `mp-workflow/1` runner（marketplace-3.0 03）。

顧客 Agent 側の入口::

    # my_agent/main.py
    async def run(context):
        instructions = (context.work_dir / "instructions.md").read_text(encoding="utf-8")
        reply = await create_reply(product_code=context.parameters["product_code"], instructions=instructions)
        (context.output_dir / "reply.md").write_text(reply, encoding="utf-8")

    # image の起動 command
    python -c "from agenticstar_platform.workflow import run; run('my_agent.main:run')"

runner（親プロセス）が executor 注入 env の検証 → runtime context / 入力取得 → `/workspace` 展開 → manifest 監査 →
Agent entrypoint を子プロセスで実行 → output 回収・artifact 保存 → completion_envelope（version 2）の保存（同じ completion_id で
再送）までを担う。旧 `run_marketplace_agent`（通常 MP chat）の契約は変えない。
"""
from .context import AuditApi, WorkflowContext
from .envelope import ENVELOPE_VERSION, OUTCOMES, EffectTally, build_envelope, decide_outcome
from .errors import (
    AuditNotPersisted,
    ExecutionTerminal,
    InputIntegrityError,
    OutputCollectionError,
    RuntimeApiError,
    WorkflowConfigError,
    WorkflowError,
)
from .runner import PROTOCOL, REQUIRED_ENV, WorkflowResult, WorkflowRunner, arun, run, validate_env

__all__ = [
    "PROTOCOL", "REQUIRED_ENV", "run", "arun", "validate_env", "WorkflowRunner", "WorkflowResult", "WorkflowContext",
    "AuditApi", "EffectTally", "build_envelope", "decide_outcome", "OUTCOMES", "ENVELOPE_VERSION",
    "WorkflowError", "WorkflowConfigError", "RuntimeApiError", "ExecutionTerminal", "AuditNotPersisted",
    "InputIntegrityError", "OutputCollectionError",
]
