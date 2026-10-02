"""Minimal workflow agent sample 2: a mock send (idempotent_write).

Run an external write only **after tool.invoked has been acknowledged**, and link its result with tool.effect.
For resends use operation_key plus a stable action_ref, and never call a write again just because of a network
error without checking its result. After cancellation or the deadline, do not start new writes
(`context.ensure_can_act()`).

Contract (excerpt)::

    {"runtime_protocol": "mp-workflow/1", "effect_mode": "idempotent_write",
     "outputs": [{"name": "receipt", "path": "receipt.md", "format": "markdown", "required": true}]}
"""
from __future__ import annotations


class MockInbox:
    """An idempotent destination: resends with the same action_ref collapse into one message."""

    def __init__(self):
        self.sent: dict[str, str] = {}

    async def send(self, action_ref: str, body: str) -> str:
        if action_ref not in self.sent:
            self.sent[action_ref] = body
        return f"receipt:{action_ref}"


inbox = MockInbox()


async def run(context) -> None:
    await context.ensure_can_act()  # do not start new external operations after cancellation / the deadline
    action_ref = f"send:{context.operation_key[:16]}"  # stable across resends of the same step and entry_ref
    body = (context.work_dir / "reply.md").read_text(encoding="utf-8") if (context.work_dir / "reply.md").exists() else "hello"

    invoked = await context.audit.tool_invoked("mock_send", effect_kind="send", action_ref=action_ref, target="mock://inbox")
    try:
        receipt = await inbox.send(action_ref, body)
    except Exception as e:  # noqa: BLE001 — never treat an unknown result as "not sent"
        await context.audit.tool_effect(invoked, status="unknown", action_ref=action_ref, error=type(e).__name__)
        raise
    await context.audit.tool_effect(invoked, status="ok", count=1, action_ref=action_ref)
    (context.output_dir / "receipt.md").write_text(f"# receipt\n\n{receipt}\n", encoding="utf-8")
