"""Minimal workflow agent sample 1: drafting a reply (read_only).

Contract (registered by an administrator; excerpt)::

    {"runtime_protocol": "mp-workflow/1", "effect_mode": "read_only",
     "parameters_schema": {"type": "object", "additionalProperties": false,
                           "properties": {"product_code": {"type": "string"}, "language": {"type": "string", "enum": ["ja", "en"]}},
                           "required": ["product_code", "language"]},
     "env_bindings": {"PRODUCT_CODE": "product_code", "REPLY_LANGUAGE": "language"},
     "files": [{"name": "instructions", "path": "instructions.md", "format": "markdown", "editable": true, "required": true},
               {"name": "settings", "path": "settings/agent.yaml", "format": "yaml", "from_parameters": true}],
     "outputs": [{"name": "reply", "path": "reply.md", "format": "markdown", "required": true}]}

The image's start command::

    python -c "from agenticstar_platform.workflow import run; run('workflow_reply_agent:run')"

The runner stages the inputs in `/workspace/input` and copies them to `/workspace/work`. The agent only reads the work
directory and writes its declared outputs to `/workspace/output`. External reads are audited with
`context.audit.tool_invoked(..., effect_kind="read")`.
"""
from __future__ import annotations


async def create_reply(*, product_code: str, instructions: str, language: str) -> str:
    # Your processing (LLM calls etc.). A deterministic dummy here
    heading = "回答案" if language == "ja" else "Draft reply"
    return f"# {heading}: {product_code}\n\n{instructions.strip()}\n"


async def run(context) -> None:
    inv = await context.audit.tool_invoked("read_instructions", effect_kind="read", target="instructions.md")
    instructions = (context.work_dir / "instructions.md").read_text(encoding="utf-8")
    await context.audit.tool_effect(inv, status="ok", count=1)

    reply = await create_reply(product_code=context.parameters["product_code"], instructions=instructions,
                               language=context.parameters.get("language", "ja"))
    (context.output_dir / "reply.md").write_text(reply, encoding="utf-8")
