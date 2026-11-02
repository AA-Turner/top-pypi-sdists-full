"""Hook settings that make Claude Code, Codex and opencode run `lab agent` at the moments rules get lost."""

import json
from pathlib import Path
from typing import ClassVar

from labqoat.cli.agent.agent_rules import AgentRules
from labqoat.json_document import JsonDocument, JsonValue

PLUGIN = """// Written by `lab init`: keeps opencode on Labqoat's tools.
import type { Plugin } from "@opencode-ai/plugin"

export const Labqoat: Plugin = async ({ $ }) => ({
  "tool.execute.before": async (input, output) => {
    if (input.tool !== "bash") return
    const hook = new Response(JSON.stringify({ tool_input: { command: output.args.command } }))
    const answer = (await $`lab agent check < ${hook}`.nothrow().text()).trim()
    const decision = answer ? JSON.parse(answer).hookSpecificOutput : undefined
    if (decision?.permissionDecision === "deny") throw new Error(decision.permissionDecisionReason)
  },
  "experimental.session.compacting": async (_input, output) => {
    output.context.push(await $`lab agent brief`.nothrow().text())
  },
})
"""


class AgentHooks:
    """Merge Labqoat's hooks into each agent's project settings without touching anything else there."""

    events: ClassVar[dict[str, tuple[str | None, str]]] = {
        "SessionStart": ("startup|resume|clear|compact", "lab agent brief --event SessionStart"),
        "SubagentStart": (None, "lab agent brief --event SubagentStart"),
        "PreToolUse": ("Bash", "lab agent check"),
    }
    settings: ClassVar[dict[str, str]] = {"claude": ".claude/settings.json", "codex": ".codex/hooks.json"}

    @classmethod
    def install(cls, workspace: Path, agent: str) -> list[str]:
        """Write what ``agent`` needs in ``workspace`` and name every file that changed."""
        changed = [name for name in ("AGENTS.md", "CLAUDE.md") if cls.place(workspace / name, cls.guide(name))]
        if agent == "opencode":
            return changed + (
                ["opencode plugin"] if cls.place(workspace / ".opencode/plugins/labqoat.ts", PLUGIN) else []
            )
        path = workspace / cls.settings[agent]
        merged = cls.merged(cls.read(path))
        if merged != cls.read(path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
            changed.append(cls.settings[agent])
        return changed

    @staticmethod
    def guide(name: str) -> str:
        """AGENTS.md holds the card for Codex and opencode; CLAUDE.md imports it for Claude Code."""
        return f"{AgentRules.card}\n" if name == "AGENTS.md" else "@AGENTS.md\n"

    @staticmethod
    def place(path: Path, content: str) -> bool:
        """Create ``path`` with ``content`` unless a file is already there."""
        if path.exists():
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True

    @staticmethod
    def read(path: Path) -> dict[str, JsonValue]:
        """The settings document at ``path``, or an empty one."""
        if not path.is_file():
            return {}
        return dict(JsonDocument.expect_dict(json.loads(path.read_text(encoding="utf-8"))))

    @classmethod
    def merged(cls, document: dict[str, JsonValue]) -> dict[str, JsonValue]:
        """``document`` with each Labqoat hook added once."""
        hooks = dict(JsonDocument.expect_dict(document.get("hooks", {})))
        for event, (matcher, command) in cls.events.items():
            groups = list(JsonDocument.expect_list(hooks.get(event, [])))
            if command not in json.dumps(groups):
                group: dict[str, JsonValue] = {"hooks": [{"type": "command", "command": command, "timeout": 30}]}
                groups.append({"matcher": matcher, **group} if matcher else group)
            hooks[event] = groups
        return {**document, "hooks": hooks}
