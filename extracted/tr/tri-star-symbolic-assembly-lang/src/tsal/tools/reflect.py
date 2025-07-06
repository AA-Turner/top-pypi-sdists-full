from pathlib import Path
import json
from tsal.core.rev_eng import Rev_Eng
from tsal.tools.brian.optimizer import SymbolicOptimizer

def reflect(path: str = "src/tsal", as_json: bool = False) -> str:
    """Reconstruct spiral path and summarize changes."""
    opt = SymbolicOptimizer()
    rev = Rev_Eng(origin="reflect")
    report = {}

    for file in Path(path).rglob("*.py"):
        results = opt.analyze(file.read_text())
        delta = sum(m["delta"] for _, m in results)
        rev.log_event(
            "AUDIT", payload={"file": str(file), "count": len(results)}
        )
        report[str(file)] = delta

    summary = rev.summary()
    summary["deltas"] = report
    summary["files"] = list(report.keys())

    return (
        json.dumps(summary, indent=2)
        if as_json
        else "\n".join(f"{k}: Δ{v}" for k, v in report.items())
    )

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="reflect on repo")
    parser.add_argument("path", nargs="?", default="src/tsal")
    parser.add_argument("--origin", dest="origin")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = args.origin or args.path
    print(reflect(path, as_json=args.json))

if __name__ == "__main__":
    main()
