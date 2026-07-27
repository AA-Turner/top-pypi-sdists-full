"""SAGE Self-Modification System (Items 3001-3050).

Enables SAGE to modify its own code safely and systematically.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Any


@dataclass
class CodeModification:
    """A proposed code modification."""

    file_path: str
    original_code: str
    modified_code: str
    modification_type: str  # "insert", "replace", "delete", "refactor"
    line_start: int
    line_end: int
    description: str
    is_safe: bool = True
    requires_tests: bool = True


class SelfModificationSystem:
    """
    P0 Items 3001-3050: Enables SAGE to modify its own code.
    """

    # Patterns that indicate self-modification is safe
    SAFE_MODIFICATION_PATTERNS: ClassVar[list[str]] = [
        r"def\s+\w+",
        r"class\s+\w+",
        r"#.*TODO|FIXME|BUG",
        r"pass\s*$",
        r"raise\s+NotImplementedError",
    ]

    # Patterns that indicate dangerous modifications
    DANGEROUS_PATTERNS: ClassVar[list[str]] = [
        r"os\.system",
        r"subprocess\.call",
        r"eval\s*\(",
        r"exec\s*\(",
        r"__import__",
        r"open\s*\(.+['\"]w['\"]",
        r"shutil\.rmtree",
    ]

    def __init__(self, sage_root: str):
        self.sage_root = Path(sage_root)
        self._modifications: list[CodeModification] = []

    def analyze_own_code(self, file_path: str) -> dict:
        """Analyze SAGE's own code for improvement opportunities."""
        import ast

        path = self.sage_root / file_path

        if not path.exists():
            raise FileNotFoundError(f"SAGE file not found: {path}")

        code = path.read_text(encoding="utf-8", errors="replace")

        analysis: dict[str, Any] = {
            "file": file_path,
            "lines": len(code.split("\n")),
            "functions": [],
            "classes": [],
            "todos": [],
            "issues": [],
        }

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "args": len(node.args.args),
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "methods": len(
                                [n for n in node.body if isinstance(n, ast.FunctionDef)]
                            ),
                        }
                    )
        except SyntaxError as e:
            analysis["issues"].append(f"Syntax error: {e}")

        for i, line in enumerate(code.split("\n"), 1):
            if any(marker in line for marker in ["TODO", "FIXME", "BUG"]):
                analysis["todos"].append({"line": i, "content": line.strip()})

        return analysis

    def propose_modification(
        self,
        file_path: str,
        original: str,
        modified: str,
        description: str,
    ) -> CodeModification:
        """Propose a modification to SAGE's code."""
        is_safe = True
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, modified) and not re.search(pattern, original):
                is_safe = False
                break

        modification = CodeModification(
            file_path=file_path,
            original_code=original,
            modified_code=modified,
            modification_type="replace",
            line_start=0,
            line_end=0,
            description=description,
            is_safe=is_safe,
        )

        self._modifications.append(modification)
        return modification

    def apply_modification(self, modification: CodeModification) -> bool:
        """Apply a code modification to SAGE's own code."""
        if not modification.is_safe:
            raise ValueError("Cannot apply unsafe modification")

        path = self.sage_root / modification.file_path

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        current_code = path.read_text(encoding="utf-8", errors="replace")
        new_code = current_code.replace(modification.original_code, modification.modified_code)

        if new_code == current_code:
            # Fallback to line-based replacement if exact match fails
            lines = current_code.split("\n")
            orig_lines = modification.original_code.split("\n")
            mod_lines = modification.modified_code.split("\n")

            for i in range(len(lines) - len(orig_lines) + 1):
                if lines[i : i + len(orig_lines)] == orig_lines:
                    lines = lines[:i] + mod_lines + lines[i + len(orig_lines) :]
                    new_code = "\n".join(lines)
                    break

        path.write_text(new_code)
        return True
