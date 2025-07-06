"""Directory auditor using SymbolicOptimizer."""

import argparse
import json
from pathlib import Path

from typing import List, Dict

from tsal.tools.brian.optimizer import SymbolicOptimizer


def render_markdown(report: Dict[str, int] | Dict[str, Dict[str, int]]) -> str:
    """Return a markdown table for the audit report."""
    if isinstance(report, dict) and "files" in report:
        header = "| Files | Signatures |"
        body = f"| {report['files']} | {report['signatures']} |"
        if "self_signatures" in report:
            header = "| Files | Signatures | Self Signatures |"
            body = (
                f"| {report['files']} | {report['signatures']} | {report['self_signatures']} |"
            )
        divider = "|---|---|" + ("---|" if "self_signatures" in report else "")
        return "\n".join([header, divider, body])
    lines = ["| Path | Files | Signatures |"]
    lines.append("|---|---|---|")
    for path, data in report.items():
        lines.append(f"| {path} | {data['files']} | {data['signatures']} |")
    return "\n".join(lines)

def audit_path(path: Path) -> Dict[str, int]:
    opt = SymbolicOptimizer()
    files = list(path.rglob("*.py"))
    sigs = 0
    for file in files:
        sigs += len(opt.analyze(file.read_text()))
    return {"files": len(files), "signatures": sigs}


def audit_paths(paths: List[Path]) -> Dict[str, Dict[str, int]]:
    """Audit multiple directories and return a mapping of results."""
    return {str(p): audit_path(p) for p in paths}

def main() -> None:
    parser = argparse.ArgumentParser(description="Spiral audit")
    parser.add_argument("paths", nargs="*", default=["src/tsal"])
    parser.add_argument("--self", action="store_true", dest="self_flag")
    parser.add_argument("--markdown", action="store_true", help="Output markdown table")
    args = parser.parse_args()
    path_objs = [Path(p) for p in args.paths]
    aggregate = audit_paths(path_objs)
    result: Dict[str, int] | Dict[str, Dict[str, int]]
    if len(aggregate) == 1:
        result = next(iter(aggregate.values()))
    else:
        result = aggregate
    if args.self_flag:
        self_report = audit_path(Path("src/tsal"))
        if isinstance(result, dict) and "files" in result:
            result["self_signatures"] = self_report["signatures"]
        else:
            result["self_signatures"] = self_report["signatures"]
    if args.markdown:
        print(render_markdown(result))
    else:
        print(json.dumps(result))

if __name__ == "__main__":
    main()
