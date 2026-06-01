#!/usr/bin/env python3
# ruff: noqa: T201
import ast
import argparse
import subprocess
import sys

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

EXPORTS_PATH = "workflow_sdk/mistralai/workflows/exports.py"


def get_all_from_ref(ref: str, path: str) -> set[str]:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"WARNING: Could not read {path} from ref {ref!r} — skipping __all__ check")
        return set()
    tree = ast.parse(result.stdout)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == "__all__"
                    and isinstance(node.value, ast.List)
                ):
                    return {
                        str(elt.value)
                        for elt in node.value.elts
                        if isinstance(elt, ast.Constant)
                    }
    return set()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--against-ref", default="HEAD")
    args = parser.parse_args()

    old_all = get_all_from_ref(args.base_ref, EXPORTS_PATH)
    new_all = get_all_from_ref(args.against_ref, EXPORTS_PATH)

    if not old_all:
        return 0

    removed = old_all - new_all
    if removed:
        print(f"\n{RED}{BOLD}⚠️  BREAKING CHANGES DETECTED{RESET}\n")
        print(f"Breaking change: symbols removed from mistralai.workflows public API: {sorted(removed)}")
        print()
        return 1

    added = new_all - old_all
    if added:
        print(f"OK: new symbols added to public API: {sorted(added)}")
        return 0

    print(f"OK: public API surface unchanged ({len(new_all)} symbols)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
