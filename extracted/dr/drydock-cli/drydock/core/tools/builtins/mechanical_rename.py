"""mechanical_rename — safe-rollback rename across multiple .py files.

Sidesteps Gemma 4's multi-file coordination weakness for the gauntlet's
surgery cases (P4-S1 units→quantity, P5-S1 Backend ABC adoption, P6-S1
db.attr → repo.attr) by mechanically applying the rename then verifying
with pytest. Rolls back atomically if the test suite goes red.

Approach: word-bounded regex rename across all .py files under `scope`,
plus optional string-literal rename for the `field` kind (so dict keys
like `row["units"]` get renamed alongside attribute access).

This is intentionally NOT a full AST transform. libcst isn't installed
in the drydock env and the gauntlet's actual cases are all
identifier-level renames where `\\b<name>\\b` handles correctly. If a
case needs scope-aware renames (shadowing, dynamic getattr), the model
should fall back to per-file search_replace.

Always runs pytest before declaring success; rolls back all files if
red. Returns the list of files changed + the pytest summary so the
model knows the outcome without a second tool call.
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Literal, final

from pydantic import BaseModel, Field

from drydock.core.tools.base import (
    BaseTool, BaseToolConfig, BaseToolState, InvokeContext, ToolError, ToolPermission,
)
from drydock.core.types import ToolStreamEvent
from drydock.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData

if TYPE_CHECKING:
    from drydock.core.types import ToolResultEvent


# Python keywords we refuse to rename (would create syntax errors).
_PY_KEYWORDS = frozenset({
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
})


class MechanicalRenameArgs(BaseModel):
    old_name: str = Field(
        description="Identifier to rename (function, class, or field name)."
    )
    new_name: str = Field(
        description="New identifier name."
    )
    scope: str = Field(
        default=".",
        description="Directory to walk for .py files. Default: cwd.",
    )
    kind: Literal["function", "class", "field", "auto"] = Field(
        default="auto",
        description=(
            "function = identifier rename only. "
            "class = identifier rename only. "
            "field = identifier rename PLUS string-literal rename (for dict keys/JSON). "
            "auto = identifier rename (no string-literal handling)."
        ),
    )
    run_tests: bool = Field(
        default=True,
        description="If true, run pytest after rename; rollback if red. Default True.",
    )


class MechanicalRenameResult(BaseModel):
    files_changed: list[str]
    files_unchanged: list[str]
    occurrences_replaced: int
    pytest_status: str  # "green" | "red" | "skipped" | "no-tests-dir"
    pytest_output: str  # truncated to 2KB
    rolled_back: bool


class MechanicalRenameConfig(BaseToolConfig):
    permission: ToolPermission = ToolPermission.ASK
    max_files: int = 200
    pytest_timeout_s: int = 60


@final
class MechanicalRename(
    BaseTool[MechanicalRenameArgs, MechanicalRenameResult,
             MechanicalRenameConfig, BaseToolState],
    ToolUIData[MechanicalRenameArgs, MechanicalRenameResult],
):
    description: ClassVar[str] = (
        "Mechanically rename an identifier across all .py files in scope. "
        "Word-bounded regex; safe for function/class/field renames. "
        "Runs pytest after and rolls back if the test suite goes red. "
        "Use for 'rename X to Y everywhere' / 'change schema field' style tasks."
    )

    @classmethod
    def get_status_text(cls) -> str:
        return "Renaming identifier"

    @classmethod
    def format_call_display(cls, args: MechanicalRenameArgs) -> ToolCallDisplay:
        return ToolCallDisplay(
            summary=f"rename: {args.old_name} → {args.new_name} ({args.kind})"
        )

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        r = event.result
        if isinstance(r, MechanicalRenameResult):
            if r.rolled_back:
                return ToolResultDisplay(
                    success=False,
                    message=f"rolled back ({r.pytest_status}); see output",
                )
            msg = (
                f"{r.occurrences_replaced} sites in {len(r.files_changed)} files "
                f"(pytest: {r.pytest_status})"
            )
            return ToolResultDisplay(success=True, message=msg)
        return ToolResultDisplay(success=False, message="rename failed")

    async def run(
        self, args: MechanicalRenameArgs, ctx: InvokeContext | None = None,
    ) -> AsyncGenerator[ToolStreamEvent | MechanicalRenameResult, None]:
        # Validate inputs.
        old, new = args.old_name.strip(), args.new_name.strip()
        if not old or not new:
            raise ToolError("old_name and new_name must both be non-empty")
        if old == new:
            raise ToolError("old_name and new_name are identical")
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", old):
            raise ToolError(f"old_name {old!r} is not a valid Python identifier")
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", new):
            raise ToolError(f"new_name {new!r} is not a valid Python identifier")
        if new in _PY_KEYWORDS:
            raise ToolError(f"new_name {new!r} is a Python keyword; refusing")

        scope = Path(args.scope).resolve()
        if not scope.is_dir():
            raise ToolError(f"scope {args.scope!r} is not a directory")

        # Collect .py files; bound to max_files.
        py_files: list[Path] = []
        for p in scope.rglob("*.py"):
            # Skip common heavy/irrelevant dirs.
            parts = set(p.parts)
            if parts & {".git", "__pycache__", ".venv", "venv", "node_modules", ".tox"}:
                continue
            py_files.append(p)
            if len(py_files) > self.config.max_files:
                raise ToolError(
                    f"scope contains >{self.config.max_files} .py files; "
                    f"tighten scope or raise max_files"
                )

        # Build the rename patterns.
        word_pat = re.compile(rf"\b{re.escape(old)}\b")
        string_pats: list[tuple[re.Pattern, str]] = []
        if args.kind == "field":
            # Match the old name inside quoted strings (single or double quotes).
            string_pats = [
                (re.compile(rf"(['\"])(?P<v>{re.escape(old)})(\1)"),
                 rf"\1{new}\3"),
            ]

        # Snapshot + rewrite. Track originals for rollback.
        originals: dict[Path, str] = {}
        files_changed: list[Path] = []
        total_occurrences = 0
        for fp in py_files:
            try:
                content = fp.read_text(errors="replace")
            except OSError:
                continue
            new_content, n_word = word_pat.subn(new, content)
            n_string = 0
            for pat, repl in string_pats:
                new_content, k = pat.subn(repl, new_content)
                n_string += k
            occurrences = n_word + n_string
            if occurrences > 0 and new_content != content:
                originals[fp] = content
                fp.write_text(new_content)
                files_changed.append(fp)
                total_occurrences += occurrences

        if not files_changed:
            yield MechanicalRenameResult(
                files_changed=[],
                files_unchanged=[str(p.relative_to(scope)) for p in py_files][:20],
                occurrences_replaced=0,
                pytest_status="skipped",
                pytest_output=f"no .py file in {scope} contained {old!r}",
                rolled_back=False,
            )
            return

        # Run pytest unless explicitly skipped.
        pytest_status = "skipped"
        pytest_output = "tests not run (run_tests=False)"
        rolled_back = False
        if args.run_tests:
            tests_dir = self._find_tests_dir(scope)
            if not tests_dir:
                pytest_status = "no-tests-dir"
                pytest_output = (
                    f"no tests/ dir found under {scope}; "
                    f"rename applied without verification"
                )
            else:
                try:
                    r = subprocess.run(
                        [sys.executable, "-m", "pytest", "-q",
                         "--no-header", "--tb=short", str(tests_dir)],
                        cwd=str(scope),
                        capture_output=True,
                        text=True,
                        timeout=self.config.pytest_timeout_s,
                    )
                    pytest_output = ((r.stdout or "") + (r.stderr or "")).strip()
                    pytest_status = "green" if r.returncode == 0 else "red"
                except subprocess.TimeoutExpired:
                    pytest_status = "timeout"
                    pytest_output = (
                        f"pytest timed out after {self.config.pytest_timeout_s}s "
                        f"— rename will be rolled back as a safety measure"
                    )
                except Exception as e:
                    pytest_status = "error"
                    pytest_output = f"pytest exec error: {e!r}"

                # Roll back on red OR timeout — safer to fail closed.
                if pytest_status in ("red", "timeout"):
                    for fp, original in originals.items():
                        try:
                            fp.write_text(original)
                        except OSError:
                            pass
                    rolled_back = True

        # Truncate pytest_output to 2KB.
        if len(pytest_output) > 2048:
            pytest_output = pytest_output[:2048] + "\n…[truncated]"

        result_files_changed = [str(p.relative_to(scope)) for p in files_changed]
        if rolled_back:
            result_files_changed = []  # nothing actually persisted

        yield MechanicalRenameResult(
            files_changed=result_files_changed,
            files_unchanged=[str(p.relative_to(scope)) for p in py_files
                             if p not in originals][:20],
            occurrences_replaced=total_occurrences if not rolled_back else 0,
            pytest_status=pytest_status,
            pytest_output=pytest_output,
            rolled_back=rolled_back,
        )

    def _find_tests_dir(self, scope: Path) -> Path | None:
        """Find a tests/ dir under scope that contains at least one test_*.py."""
        candidates = [scope / "tests"]
        # Also accept tests/ as a top-level peer (when scope IS the package dir).
        candidates.append(scope.parent / "tests")
        for c in candidates:
            if c.is_dir() and any(c.glob("test_*.py")):
                return c
        # Last-ditch: search 1 level deep.
        for sub in scope.iterdir() if scope.is_dir() else []:
            if sub.is_dir():
                t = sub / "tests"
                if t.is_dir() and any(t.glob("test_*.py")):
                    return t
        return None
