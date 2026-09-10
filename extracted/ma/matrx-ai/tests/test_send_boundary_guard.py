"""FORCING GUARD — nothing may shape a prompt outside the send boundary.

Prompt caching is worth 5-10x on input cost across a tool loop, and it dies the
moment something rewrites the cached prefix between rounds. That is exactly
what happened when the executor's in-loop trim called
``trim_messages_context`` with no ``cache_state`` while the resolver called the
same function WITH one: an in-loop trim could rebuild the whole cached prefix
every iteration to reclaim a few thousand tokens.

Fixing that one call site fixes the instance. THIS test fixes the class: every
mutation seam between the ConversationResolver and the provider call is allowed
in exactly one module — ``matrx_ai/config/send_boundary.py`` — plus the module
that DEFINES the seam. A future agent who opens a new hole makes the suite red
and reads, in the failure message, where the work actually belongs.

Falsifiability: ``test_guard_detects_a_planted_violation`` plants a known-bad
file and proves the scanner reports it. A guard that cannot fail is not a
guard.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Repo root: .../aidream, holding both packages/ and aidream/.
REPO_ROOT = Path(__file__).resolve().parents[3]
SCAN_ROOTS = ("packages", "aidream")

CONTROLLER = "packages/matrx-ai/matrx_ai/config/send_boundary.py"

_SKIP_PARTS = ("__pycache__", "node_modules", ".venv", "site-packages", "migrations")


@dataclass(frozen=True)
class Seam:
    """One mutation seam and the complete list of files allowed to touch it."""

    name: str
    pattern: str
    allowed: tuple[str, ...]
    # Restrict the scan to these path prefixes (empty = every scanned file).
    scope: tuple[str, ...] = ()
    remedy: str = ""


SEAMS: tuple[Seam, ...] = (
    Seam(
        name="context trim",
        pattern=r"\btrim_messages_context\s*\(",
        allowed=(
            # The definition itself.
            "packages/matrx-ai/matrx_ai/config/context_trim.py",
            CONTROLLER,
        ),
        remedy=(
            "trim_messages_context has ONE caller: send_boundary._gated_trim, which "
            "applies the prompt-cache gate. Call prepare_for_send() instead."
        ),
    ),
    Seam(
        name="reference-fence staging",
        pattern=r"\bget_reference_fence_stager\s*\(",
        allowed=("packages/matrx-ai/matrx_ai/_ext.py", CONTROLLER),
        remedy="Fence staging is a send-boundary step — add it to prepare_for_send().",
    ),
    Seam(
        name="clone-at-send wire config",
        pattern=r"\bbuild_wire_config\s*\(",
        allowed=("packages/matrx-ai/matrx_ai/config/picklist_runtime.py", CONTROLLER),
        remedy="build_wire_config is invoked once, by send_boundary._build_wire.",
    ),
    Seam(
        name="prompt-cache routing key",
        pattern=r"\bprovider_prompt_cache_key\s*\(",
        allowed=("packages/matrx-ai/matrx_ai/providers/cache_guard.py", CONTROLLER),
        remedy="The cache key is derived once, by send_boundary._set_prompt_cache_key.",
    ),
    Seam(
        name="prompt_cache_key assignment",
        pattern=r"\.prompt_cache_key\s*=(?!=)",
        allowed=(CONTROLLER,),
        remedy="Only the send boundary stamps prompt_cache_key onto a config.",
    ),
    Seam(
        name="system-prompt date pin",
        pattern=r"\.date_anchor\s*=(?!=)|\b_pin_system_date\s*\(",
        allowed=(CONTROLLER,),
        remedy=(
            "The system prefix is pinned once, by send_boundary._pin_system_date, so it "
            "stays byte-stable across rounds."
        ),
    ),
    Seam(
        name="wire message-list replacement",
        pattern=r"\.config\.messages\s*=(?!=)|\bconfig\.messages\s*=(?!=)",
        allowed=(CONTROLLER,),
        scope=(
            "packages/matrx-ai/matrx_ai/orchestrator/",
            "packages/matrx-ai/matrx_ai/agents/",
            "packages/matrx-ai/matrx_ai/providers/",
        ),
        remedy=(
            "Replacing a live config's message list at send time rebuilds the cached "
            "prefix. Shape the prompt inside prepare_for_send()."
        ),
    ),
)


def _is_test_path(rel: str) -> bool:
    return "/tests/" in rel or rel.startswith("tests/") or Path(rel).name.startswith("test_")


def _python_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        base = REPO_ROOT / root
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            if any(part in _SKIP_PARTS for part in path.parts):
                continue
            files.append(path)
    return files


def scan(files: list[Path], *, root: Path = REPO_ROOT) -> list[str]:
    """Return a violation line for every disallowed touch of a seam."""
    violations: list[str] = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        if _is_test_path(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for seam in SEAMS:
            if seam.scope and not any(rel.startswith(prefix) for prefix in seam.scope):
                continue
            if rel in seam.allowed:
                continue
            regex = re.compile(seam.pattern)
            for lineno, line in enumerate(text.splitlines(), start=1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if regex.search(line):
                    violations.append(
                        f"{rel}:{lineno}: touches the {seam.name} seam outside "
                        f"{CONTROLLER}\n    {stripped}\n    → {seam.remedy}"
                    )
    return violations


def test_no_prompt_shaping_outside_the_send_boundary() -> None:
    violations = scan(_python_files())
    assert not violations, (
        "Prompt-shaping mutation found outside the send boundary.\n\n"
        + "\n".join(violations)
        + "\n\nEvery mutation of the wire-facing message list, system prompt, or wire "
        "config between the ConversationResolver and the provider call belongs in "
        f"{CONTROLLER}::prepare_for_send — the one place the prompt-cache gate, the "
        "trim audit, and this guard all already apply."
    )


def test_guard_detects_a_planted_violation(tmp_path: Path) -> None:
    """Falsifiability: the scan MUST fail on a known-bad file."""
    bad = tmp_path / "packages" / "matrx-ai" / "matrx_ai" / "orchestrator" / "sneaky.py"
    bad.parent.mkdir(parents=True)
    bad.write_text(
        "from matrx_ai.config.context_trim import trim_messages_context\n"
        "def send(cfg):\n"
        "    trim_messages_context(cfg.messages)\n"
        "    cfg.config.messages = []\n",
        encoding="utf-8",
    )
    violations = scan([bad], root=tmp_path)
    assert len(violations) == 2, violations
    assert any("context trim" in v for v in violations)
    assert any("wire message-list replacement" in v for v in violations)


def test_controller_is_the_only_trim_caller_and_is_itself_scanned() -> None:
    """The allowlist must name files that actually exist — a typo'd path would
    silently allow everything."""
    for seam in SEAMS:
        for rel in seam.allowed:
            assert (REPO_ROOT / rel).is_file(), f"allowlist entry does not exist: {rel}"
    assert (REPO_ROOT / CONTROLLER).is_file()
