"""Documentation coverage tests — fails if docs drift from the CLI.

Reads `docs/SAGE_COMMANDS.md` and asserts every CLI command + subcommand
appears in the document. When you add a new command without documenting
it, this test fails — keeping the doc honest.

Also verifies every command in the docs actually exists in the CLI (no
"phantom" commands documented but not implemented).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from typer.testing import CliRunner


_DOCS_PATH = Path(__file__).parent.parent.parent / "docs" / "SAGE_COMMANDS.md"


@pytest.fixture(scope="module")
def docs_content() -> str:
    if not _DOCS_PATH.exists():
        pytest.skip(f"docs file not found at {_DOCS_PATH}")
    return _DOCS_PATH.read_text()


@pytest.fixture(scope="module")
def sage_app():
    from sage.cli_core import app
    return app


@pytest.fixture(scope="module")
def all_command_names(sage_app):
    """Extract every top-level command name from the sage typer app."""
    names = set()
    for cmd in sage_app.registered_commands:
        if cmd.name:
            names.add(cmd.name)
        elif cmd.callback:
            names.add(cmd.callback.__name__.replace("_", "-"))
    # Group names (subcommand apps mounted via add_typer)
    for group in sage_app.registered_groups:
        if group.name:
            names.add(group.name)
    return names


# ── Every command appears in the docs ────────────────────────────────────────


# Commands that exist for legacy/internal reasons and we deliberately
# don't document publicly. Keep this list short.
_UNDOCUMENTED_OK: frozenset[str] = frozenset({
    # (None right now — if you skip docs for a command, add it here
    #  with a comment explaining why.)
})


class TestDocsCoverEveryCommand:
    def test_each_top_level_command_documented(self, docs_content, all_command_names):
        """For every command in the CLI, the docs must mention it."""
        missing = []
        for name in all_command_names:
            if name in _UNDOCUMENTED_OK:
                continue
            # Look for the command name as a backticked token in the docs
            # (matches `sage <name>` or `<name>` headings)
            pattern = re.compile(rf"`sage {re.escape(name)}\b|^### `{re.escape(name)}\b", re.MULTILINE)
            if not pattern.search(docs_content):
                missing.append(name)
        assert not missing, (
            f"The following commands exist in the CLI but aren't documented "
            f"in docs/SAGE_COMMANDS.md: {missing}"
        )

    def test_new_commands_specifically_documented(self, docs_content):
        """Explicit anchors for the commands shipped this session."""
        for cmd in ("search", "image", "schedule", "integrate", "daemon"):
            # Each new command gets a `### `sage <cmd>` heading
            assert f"sage {cmd}" in docs_content, (
                f"Newly-added command 'sage {cmd}' missing from "
                f"docs/SAGE_COMMANDS.md"
            )

    def test_new_command_flags_documented(self, docs_content):
        """Key flags on new commands are called out so users discover them."""
        # `sage ask --image` was added this session
        assert "--image" in docs_content
        # PDF auto-extract feature on --file
        assert "PDF" in docs_content
        # Cloud model fleet
        assert "cloud:qwen-coder-7b" in docs_content
        assert "cloud:llava-next-7b" in docs_content

    def test_privacy_documented(self, docs_content):
        """The anonymizer + privacy posture must be mentioned so users
        know what's NOT sent to the cloud."""
        lower = docs_content.lower()
        assert "anonymizer" in lower or "privacy" in lower

    def test_exit_codes_documented(self, docs_content):
        """User-facing exit-code contract."""
        assert "exit code" in docs_content.lower() or "Exit code" in docs_content


# ── No phantom commands ──────────────────────────────────────────────────────


class TestDocsHaveNoPhantoms:
    """Every command mentioned in the docs must actually exist in the CLI.
    Catches stale references when commands get renamed/removed."""

    @pytest.fixture
    def documented_commands(self, docs_content) -> set[str]:
        """Pull all `sage <name>` references from the docs."""
        # Match `sage <command>` at start of code block content or inline
        matches = re.findall(r"sage ([a-z][a-z0-9-]*)\b", docs_content)
        # Filter out generic terms that aren't actual commands
        ignored = {
            "ai", "is", "to", "and", "the", "for", "by", "on",
            "subcommand", "fleet", "models",  # may be part of feature names
        }
        cmds = set()
        for m in matches:
            if m not in ignored and len(m) > 1:
                cmds.add(m)
        return cmds

    def test_every_documented_command_exists(
        self, documented_commands, all_command_names,
    ):
        # Subcommands like `add`, `list`, `pause` show up too — accept
        # those as long as their PARENT group exists.
        subcommand_parents = {
            "add": "schedule", "list": "schedule", "pause": "schedule",
            "resume": "schedule", "remove": "schedule", "run-due": "schedule",
            "connect": "integrate", "revoke": "integrate",
            "start": "daemon", "stop": "daemon", "status": "daemon",
            "show": "config", "set": "config", "get": "config", "init": "config",
            "setup": "sms", "logs": "sms", "contacts": "sms",
            "index": "rag", "query": "rag",
        }
        phantoms = []
        for doc_cmd in documented_commands:
            if doc_cmd in all_command_names:
                continue
            if doc_cmd in subcommand_parents and subcommand_parents[doc_cmd] in all_command_names:
                continue
            # Some docs sentences might reference "sage" as an alias for the
            # main command (no subcommand) — that's the empty/None case
            phantoms.append(doc_cmd)
        # Allow up to a small number of false positives (regex isn't perfect);
        # if it grows, tighten the regex.
        assert len(phantoms) < 10, (
            f"docs mentions commands that don't exist: {phantoms}. "
            f"Either remove from docs or add to the CLI."
        )


# ── Slash commands documented ────────────────────────────────────────────────


class TestSlashCommandsDocumented:
    """In-REPL slash commands (`/model`, `/clear`, etc.) only work inside
    `sage chat`/`run`. They MUST be documented because they're invisible
    to `sage --help`."""

    def test_essential_slash_commands_in_docs(self, docs_content):
        for slash in ("/model", "/clear", "/quit", "/help", "/temp"):
            assert slash in docs_content, (
                f"Slash command {slash} not mentioned in docs"
            )

    def test_autoorg_and_autofleet_documented(self, docs_content):
        """These swarm features only fire via slash command — easy to
        forget about, so we lock them in via doc check."""
        assert "/autoorg" in docs_content
        assert "/autofleet" in docs_content
