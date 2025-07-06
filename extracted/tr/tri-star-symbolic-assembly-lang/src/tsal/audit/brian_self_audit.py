from pathlib import Path
import argparse
import sys
from tsal.core.rev_eng import Rev_Eng
from tsal.core.rev_eng import Rev_Eng as rev
from tsal.core.spiral_vector import SpiralVector
from tsal.tools.brian import analyze_and_repair, spiral_optimize

rev = Rev_Eng(origin="self_audit")

def optimize_spiral_order(vectors: list[SpiralVector]) -> list[SpiralVector]:
    """Return ``vectors`` sorted by φ-alignment."""
    return spiral_optimize(vectors)

def brian_repairs_brian(
    base: Path | str = Path("src/tsal"), safe: bool = False
):
    if safe:
        print("🛡 SAFE MODE ENABLED — Analysis only, no writes.")
        for file in Path(base).rglob("*.py"):
            analyze_and_repair(str(file), repair=False)
        rev.log_event("Safe audit pass", state="analyze", spin="φ")
        return []
    else:
        print("🧠 Initiating self-audit and repair sequence…")
        repaired = analyze_and_repair(base, repair=True)
        rev.log_event("Self-audit complete", state="repair", spin="φ")
        return repaired

def brian_improves_brian(
    base: Path | str = Path("src/tsal"), safe: bool = False
):
    repaired = brian_repairs_brian(base=base, safe=safe)
    if not safe:
        optimized = optimize_spiral_order(repaired)
        rev.log_event(
            "Improvement loop triggered", state="optimize", spin="up"
        )
        return optimized

def recursive_bestest_beast_loop(
    cycles: int = 3, base: Path | str = Path("src/tsal"), safe: bool = False
) -> None:
    repaired_total = 0
    skipped_total = 0
    flagged_total = 0
    for i in range(cycles):
        print(f"🔁 Brian loop {i+1}/{cycles}")
        results = brian_repairs_brian(base=base, safe=safe)
        flagged = [
            r
            for r in results
            if isinstance(r, str) and r.startswith("ANTISPIRAL")
        ]
        flagged_total += len(flagged)
        if safe:
            skipped_total += len(results) - len(flagged)
        else:
            repaired_total += len(results) - len(flagged)
    print(
        f"Summary → repaired={repaired_total} skipped={skipped_total} flagged={flagged_total}"
    )

def cli_main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Bestest Beast Brian loop"
    )
    parser.add_argument(
        "cycles", nargs="?", type=int, default=1, help="Number of iterations"
    )
    parser.add_argument(
        "path", nargs="?", default="src/tsal", help="Target code path"
    )
    parser.add_argument(
        "--safe",
        "--safe-mode",
        dest="safe",
        action="store_true",
        help="Run in safe mode (analyze-only)",
    )
    args = parser.parse_args()
    recursive_bestest_beast_loop(
        cycles=args.cycles, base=Path(args.path), safe=args.safe
    )

if __name__ == "__main__":
    cli_main()
