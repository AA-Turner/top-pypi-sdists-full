"""FORCING GUARD — a provider call goes through ``send_once`` and nowhere else.

The owner's requirement for AI request snapshots: *the exact shared engine that
runs a mandate also takes the copy, so the two can never drift.* That holds only
while every model call crosses ONE step — send boundary → provider execute →
capture → restore (``matrx_ai/orchestrator/send_once.py``). Hindsight's wire
replay used to rebuild the request and call ``UnifiedAIClient().execute``
itself, skipping the send boundary: reference fences and placeholders could
reach the model unexpanded while the fidelity check still said "faithful". That
is the class this guard closes: a new direct ``.execute(`` on the provider
client makes the suite red and the message says where the call belongs.

Detection (AST, not text, so a string literal in a self-test never trips it):
in any non-test ``.py`` file under ``packages/``, ``aidream/`` or ``scripts/``
whose source names the provider client (``UnifiedAIClient`` or an import from
``matrx_ai.providers``), every call ``<receiver>.execute(...)`` whose receiver
is ``UnifiedAIClient(...)`` itself or a name / attribute containing ``client``.

Heuristic limit, stated honestly: a file that reaches a provider sub-client
without ever naming the client or the providers package is not seen. The
provider package itself (``matrx_ai/providers/``) IS the client and is exempt.

Falsifiability: ``test_guard_detects_a_planted_direct_call`` plants the exact
shape wire replay used to have and proves the scanner reports it.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCAN_ROOTS = ("packages", "aidream", "scripts")
_SKIP_PARTS = ("__pycache__", "node_modules", ".venv", "site-packages", "migrations")

SEND_ONCE = "packages/matrx-ai/matrx_ai/orchestrator/send_once.py"

#: The client itself: its dispatch hands the call to the per-wire sub-client.
EXEMPT_PREFIXES = ("packages/matrx-ai/matrx_ai/providers/",)

#: Known direct callers that are NOT yet routed through ``send_once``. Each one
#: is named with its reason and has a <=3-line entry in its node's task list
#: (common-docs/operations/tasks/...). Adding a name here is a decision, not a
#: fix: the right move is almost always to call ``send_once`` instead.
ALLOWED: dict[str, str] = {
    SEND_ONCE: "THE step — the one sanctioned provider execute.",
    "packages/matrx-ai/matrx_ai/memory/llm_adapter.py": (
        "memory observer/reflector held call (store=False); routing it through "
        "send_once changes its prompt shaping (trim, cache key, fences) — filed "
        "on the memory node, not changed blind in the snapshot-fidelity lane."
    ),
    "packages/matrx-ai/matrx_ai/orchestrator/conversation_provider.py": (
        "distillation ProviderTurn over an injected client with no ExecutionState "
        "or snapshot; routing needs the conversation runtime's own design pass — "
        "filed on the distillation node."
    ),
    "packages/matrx-ai/matrx_ai/processing/audio/stt.py": (
        "speech-to-text calls the transcription sub-client with (request, profile); "
        "not a chat turn and has no send boundary to cross — filed on the audio node."
    ),
    "scripts/check_selectable_models_live.py": (
        "operator probe: one tiny live call per selectable model to prove the wire "
        "id works; deliberately the raw client, never a product path."
    ),
}


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


def _names_the_client(text: str) -> bool:
    return "UnifiedAIClient" in text or "matrx_ai.providers" in text


def _receiver_is_client(node: ast.expr) -> bool:
    if isinstance(node, ast.Call):
        func = node.func
        name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
        return name == "UnifiedAIClient"
    if isinstance(node, ast.Name):
        return "client" in node.id.lower()
    if isinstance(node, ast.Attribute):
        return "client" in node.attr.lower()
    return False


def scan(files: list[Path], *, root: Path = REPO_ROOT) -> list[str]:
    violations: list[str] = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        if _is_test_path(rel) or rel in ALLOWED or rel.startswith(EXEMPT_PREFIXES):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not _names_the_client(text):
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "execute"
                and _receiver_is_client(node.func.value)
            ):
                violations.append(
                    f"{rel}:{node.lineno}: calls the provider client's execute directly\n"
                    f"    {ast.unparse(node)[:160]}\n"
                    f"    → route it through matrx_ai.orchestrator.send_once.send_once "
                    f"(send boundary → execute → capture → restore)"
                )
    return violations


def test_no_provider_execute_outside_send_once() -> None:
    violations = scan(_python_files())
    assert not violations, (
        "A provider call bypasses the shared send step.\n\n"
        + "\n".join(violations)
        + f"\n\nEvery model call crosses {SEND_ONCE}::send_once, so a replayed "
        "request runs exactly the code the original did."
    )


def test_guard_detects_a_planted_direct_call(tmp_path: Path) -> None:
    bad = tmp_path / "aidream" / "services" / "hindsight" / "sneaky_replay.py"
    bad.parent.mkdir(parents=True)
    bad.write_text(
        "from matrx_ai.providers import UnifiedAIClient\n"
        "async def run(request):\n"
        "    client = UnifiedAIClient()\n"
        "    await UnifiedAIClient().execute(request)\n"
        "    await client.execute(request)\n"
        "    await self._client.execute(request)\n"
        "    await db.execute('SELECT 1')\n",
        encoding="utf-8",
    )
    violations = scan([bad], root=tmp_path)
    assert len(violations) == 3, violations


def test_allowlist_names_real_files() -> None:
    for rel in ALLOWED:
        assert (REPO_ROOT / rel).is_file(), f"allowlist entry does not exist: {rel}"
