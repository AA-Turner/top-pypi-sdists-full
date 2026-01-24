from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AlgFunction:
    name: str
    line_start: int
    line_end: int


@dataclass
class AlgProgram:
    file_path: str
    source: str
    functions: List[AlgFunction]
    features: Dict[str, Any]


class PyTealParser:
    """Lightweight PyTeal parser for P0 rule signals.

    We rely on a mix of AST and regex/string matches for robustness and speed.
    """

    def extract_signals(self, src: str) -> Dict[str, Any]:
        """Extract feature signals from PyTeal source code (string)."""
        try:
            tree = ast.parse(src)
        except SyntaxError:
            tree = ast.parse("pass\n")

        return {
            # Admin checks
            "has_admin_sender_assert": bool(
                re.search(r"Assert\s*\(\s*Txn\.sender\(\)\s*==\s*Global\.creator_address\(\)\s*\)", src)
            ),
            # Rekey/CloseRemainder asserts
            "has_rekey_zero_assert": bool(
                re.search(r"Assert\s*\(\s*Txn\.rekey_to\(\)\s*==\s*Global\.zero_address\(\)\s*\)", src)
            ),
            "has_close_zero_assert": bool(
                re.search(
                    r"Assert\s*\(\s*Txn\.close_remainder_to\(\)\s*==\s*Global\.zero_address\(\)\s*\)", src
                )
            ),
            # State mutation ops
            "uses_global_put": "App.globalPut(" in src or "App.global_put(" in src,
            "uses_local_put": "App.localPut(" in src or "App.local_put(" in src,
            "uses_box_ops": any(k in src for k in ["App.box_put(", "App.box_replace(", "App.box_create("]),
            # Lifecycle ops
            "uses_delete": ("OnComplete.DeleteApplication" in src) or ("delete_application" in src),
            "uses_update": ("OnComplete.UpdateApplication" in src) or ("update_application" in src),
            "has_delete_application": ("OnComplete.DeleteApplication" in src) or ("delete_application" in src),
            "has_update_application": ("OnComplete.UpdateApplication" in src) or ("update_application" in src),
            # State mutations for compat
            "has_global_put": "App.globalPut(" in src or "App.global_put(" in src,
            "has_global_del": "App.globalDel(" in src or "App.global_del(" in src,
            # Args & validation
            "uses_btoi_args": bool(re.search(r"Btoi\(\s*Txn\.application_args\[", src)),
            "has_assert": "Assert(" in src,
            # Inner txn
            "uses_inner_txn": "InnerTxnBuilder" in src,
            # Fee checks
            "has_fee_bound_assert": bool(re.search(r"Assert\s*\(\s*Txn\.fee\(\)\s*<=\s*Int\(\d+\)\s*\)", src)),
        }

    def parse_file(self, file_path: str) -> AlgProgram:
        with open(file_path, "r", encoding="utf-8") as f:
            src = f.read()
        try:
            tree = ast.parse(src)
        except SyntaxError:
            # Fallback to empty AST; we still do regex checks
            tree = ast.parse("pass\n")

        functions: List[AlgFunction] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(
                    AlgFunction(
                        name=node.name,
                        line_start=getattr(node, "lineno", 1),
                        line_end=getattr(node, "end_lineno", getattr(node, "lineno", 1)),
                    )
                )

        features = self.extract_signals(src)
        return AlgProgram(file_path=file_path, source=src, functions=functions, features=features)
