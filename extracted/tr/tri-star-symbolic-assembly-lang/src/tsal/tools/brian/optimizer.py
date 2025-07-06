"""Symbolic diff, repair, and spiral resequencer engine."""

import ast
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from tsal.core.rev_eng import Rev_Eng
from tsal.core.phase_math import phase_match_enhanced
from tsal.core.optimizer_utils import (
    SymbolicSignature,
    extract_signature,
)
from tsal.core.spiral_vector import SpiralVector, phi_alignment

class SymbolicOptimizer:
    """Walks Python AST, computes signatures, and suggests repairs."""

    def __init__(
        self,
        target_signatures: Optional[Dict[str, List[float]]] = None,
        rev_eng: Optional[Rev_Eng] = None,
    ):
        self.target_signatures = target_signatures or {}
        self.rev = rev_eng or Rev_Eng(origin="SymbolicOptimizer")

    def analyze(self, code: str) -> List[Tuple[SymbolicSignature, Dict]]:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            self.rev.log_event("ANTISPIRAL", file="<buffer>")
            raise
        results = []
        for node in ast.walk(tree):
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                sig = extract_signature(node, node.name)
                target_vec = self.target_signatures.get(sig.name, sig.vector)
                local_state = sig.magnitude()
                target_state = sum(target_vec)
                aligned_state, energy, metrics = phase_match_enhanced(
                    local_state, target_state
                )
                delta = metrics.get("delta", 0)
                self.rev.log_event(
                    "ANALYZE", name=sig.name, delta=delta, energy=energy
                )
                results.append((sig, metrics))
        return results

    def suggest_order(self, signatures: List[SymbolicSignature]) -> List[str]:
        scored = []
        for sig in signatures:
            target_vec = self.target_signatures.get(sig.name, sig.vector)
            local_state = sig.magnitude()
            target_state = sum(target_vec)
            _, energy, _ = phase_match_enhanced(local_state, target_state)
            scored.append((sig.name, energy))
        scored.sort(key=lambda x: x[1])
        return [name for name, _ in scored]

    def annotate_code(self, code: str) -> str:
        tree = ast.parse(code)
        signatures = []
        for node in ast.walk(tree):
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                sig = extract_signature(node, node.name)
                signatures.append(sig)
                target_vec = self.target_signatures.get(sig.name, sig.vector)
                local_state = sig.magnitude()
                target_state = sum(target_vec)
                _, energy, metrics = phase_match_enhanced(
                    local_state, target_state
                )
                comment = ast.Expr(
                    value=ast.Constant(
                        value=f"OPTENERGY {energy:.3f} Δ{metrics['delta']:.3f}"
                    )
                )
                node.body.insert(0, comment)
        annotated = ast.unparse(tree)
        ordered_names = self.suggest_order(signatures)
        header = f"# Suggested order: {', '.join(ordered_names)}\n"
        return header + annotated

    def repair_file(self, file_path: str) -> List[str]:
        """Rewrites the file when reordering is required and returns suggestions.

        The function analyzes the order of functions and classes in ``file_path``.
        If the current ordering differs from the ideal, the file is rewritten with
        the reordered definitions. A list of string suggestions describing the
        deltas is returned regardless of whether rewriting occurred.
        """
        code = Path(file_path).read_text()
        try:
            tree = ast.parse(code)
        except SyntaxError:
            self.rev.log_event("ANTISPIRAL", file=file_path)
            raise
        items = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                items.append(node.name)
        ideal = self.suggest_order(
            [
                extract_signature(node, node.name)
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            ]
        )
        suggestions = []
        for idx, name in enumerate(items):
            ideal_idx = ideal.index(name)
            delta = idx - ideal_idx
            _, energy, metrics = phase_match_enhanced(
                float(idx), float(ideal_idx)
            )
            suggestion = f"{name}: Δ={delta} energy={energy:.3f} φ={metrics['phase_signature']}"
            suggestions.append(suggestion)
        if items != ideal:
            new_body = []
            name_map = {
                node.name: node
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            }
            for name in ideal:
                new_body.append(name_map[name])
            for node in tree.body:
                if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    new_body.append(node)
            tree.body = new_body
            Path(file_path).write_text(ast.unparse(tree))
        return suggestions

from typing import Union

def analyze_and_repair(
    file_path: Union[str, Path], repair: bool = False
) -> list:
    """Analyze or repair ``file_path``. Directories are processed recursively."""
    path = Path(file_path)
    if path.is_dir():
        results = []
        for file in path.rglob("*.py"):
            results.extend(analyze_and_repair(file, repair=repair))
        return results

    opt = SymbolicOptimizer()
    if repair:
        try:
            return opt.repair_file(str(path))
        except SyntaxError:
            return [f"ANTISPIRAL {path}"]

    try:
        code = path.read_text()
    except IsADirectoryError:
        return []

    try:
        results = opt.analyze(code)
    except SyntaxError:
        return [f"ANTISPIRAL {path}"]
    return [
        f"{sig.name}: energy={metrics['energy_required']:.3f} Δ={metrics.get('delta',0)}"
        for (sig, metrics) in results
    ]

def spiral_optimize(functions: List[SpiralVector]) -> List[SpiralVector]:
    """Return ``functions`` sorted by φ-alignment score."""

    return sorted(
        functions,
        key=lambda v: phi_alignment(v.complexity, v.coherence),
        reverse=True,
    )

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Brian spiral optimizer")
    parser.add_argument("path", help="Python file to analyze")
    parser.add_argument(
        "--repair", action="store_true", help="Rewrite file in spiral order"
    )
    args = parser.parse_args()

    opt = SymbolicOptimizer()
    if args.repair:
        res = opt.repair_file(args.path)
    else:
        code = Path(args.path).read_text()
        results = opt.analyze(code)
        res = [
            f"{sig.name}: energy={metrics['energy_required']:.3f} Δ={metrics.get('delta',0)}"
            for (sig, metrics) in results
        ]
    for line in res:
        print(line)

if __name__ == "__main__":
    main()
