#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Validate that omnibase_compat has no forbidden upstream dependencies.

Run: python scripts/validate_no_upstream_deps.py
Exits 1 if any forbidden import is found.
"""

import ast
import sys
from pathlib import Path

FORBIDDEN_PREFIXES = ["omnibase_core", "omnibase_spi", "omnibase_infra"]
SRC = Path("src/omnibase_compat")

violations: list[str] = []
for py_file in SRC.rglob("*.py"):
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in FORBIDDEN_PREFIXES:
                    if alias.name.startswith(forbidden):
                        violations.append(f"{py_file}:{node.lineno}: imports {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for forbidden in FORBIDDEN_PREFIXES:
                if module.startswith(forbidden):
                    violations.append(f"{py_file}:{node.lineno}: from {module} import ...")

if violations:
    print("FAIL — forbidden upstream imports found:")
    for v in violations:
        print(f"  {v}")
    sys.exit(1)

count = sum(1 for _ in SRC.rglob("*.py"))
print(f"OK — scanned {count} files, no forbidden imports.")
