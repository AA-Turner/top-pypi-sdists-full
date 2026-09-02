"""Where does matrx-ai use the dataclasses API on a CONTRACT type?

agent-engine-extraction, Phase 1b.2. `dataclasses.replace()`, `.fields()` and
`.asdict()` stop working the moment a contract type becomes a pydantic model
(CUTOVER failure mode 4) — they raise `TypeError`, they do not degrade. PLAN.md
carried "35 call sites" as an estimate; like the "149 siblings" estimate before
it, that number deserves to be measured.

GREP CANNOT DO THIS. `replace(` matches every `str.replace`, `fields(` matches
`model_fields`, and the raw counts come out at 113 and 66 respectively. This
walks the AST instead, resolves how `dataclasses` was imported in each module,
and reports only real calls — separating those on a CONTRACT type from those on
some other dataclass, because only the former are migration work.

    python scripts/dataclass_api_inventory.py            # summary
    python scripts/dataclass_api_inventory.py --list     # every site
    python scripts/dataclass_api_inventory.py --max N    # ratchet for CI

The ratchet only goes DOWN.
"""

from __future__ import annotations

import argparse
import ast
import pathlib
import sys

API = {"replace", "asdict", "fields", "astuple", "is_dataclass"}
MIGRATES = {"replace", "asdict", "fields", "astuple"}  # is_dataclass keeps working

def _closure_names() -> set[str]:
    """The REAL contract closure, not a guess at variable names.

    The first version of this script classified by name hints and under-counted
    badly: `asdict(self)` inside `ImageContent`, `fields(cls)` inside
    `UnifiedConfig` and `asdict(item.provider_charge)` all read as "some other
    dataclass". Ask the closure instead.
    """
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import contract_closure

    closure, _, _ = contract_closure.walk()
    return {c.__name__ for c in closure if contract_closure.classify(c).startswith("DATACLASS")}


def _module_aliases(tree: ast.Module) -> tuple[set[str], dict[str, str]]:
    """(module aliases for `dataclasses`, {bare_name: api_name} from `from` imports)."""
    mods: set[str] = set()
    bare: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name == "dataclasses":
                    mods.add(a.asname or a.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "dataclasses":
            for a in node.names:
                if a.name in API:
                    bare[a.asname or a.name] = a.name
    return mods, bare


def _enclosing_class(tree: ast.Module, target: ast.AST) -> str | None:
    """The class a node sits inside, so `self` / `cls` can be resolved."""
    for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
        for child in ast.walk(cls):
            if child is target:
                return cls.name
    return None


# Names that SUGGEST a contract value without naming its class. Static analysis
# cannot resolve `asdict(usage_obj)` or `replace(original_request.config)` — the
# value's type is not in the source. These land in SUSPECTED, which is reported
# separately rather than folded into either certainty.
_SUSPECT_HINTS = {"config", "cfg", "message", "msg", "response", "resp", "usage", "charge", "content"}


def _classify(node: ast.AST, tree: ast.Module, call: ast.AST, names: set[str]) -> str:
    """CONFIRMED | SUSPECTED | OTHER.

    Three buckets on purpose. The first version of this script guessed from
    variable names and under-counted `asdict(self)` inside ImageContent; the
    second resolved self/cls against the real closure and then LOST
    `asdict(usage_obj)` and `replace(original_request.config)`, whose types are
    simply not in the source. Neither number is exact, so neither is presented
    as though it were.
    """
    if node is None:
        return "OTHER"
    text = ast.unparse(node)
    if text in ("self", "cls"):
        enclosing = _enclosing_class(tree, call)
        return "CONFIRMED" if enclosing in names else "OTHER"
    if any(n in text for n in names):
        return "CONFIRMED"
    lowered = text.lower()
    if any(h in lowered for h in _SUSPECT_HINTS):
        return "SUSPECTED"
    return "OTHER"


def scan(root: pathlib.Path) -> list[dict]:
    names = _closure_names()
    sites: list[dict] = []
    for path in sorted(root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError:
            continue
        mods, bare = _module_aliases(tree)
        if not mods and not bare:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            api = None
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id in mods and node.func.attr in API:
                    api = node.func.attr
            elif isinstance(node.func, ast.Name) and node.func.id in bare:
                api = bare[node.func.id]
            if api is None or api not in MIGRATES:
                continue
            arg = node.args[0] if node.args else None
            sites.append({
                "file": str(path),
                "line": node.lineno,
                "api": api,
                "arg": ast.unparse(arg) if arg is not None else "",
                "bucket": _classify(arg, tree, node, names),
            })
    return sites


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--max", type=int, default=None, help="ratchet: fail if contract sites exceed N")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent / "matrx_ai"
    sites = scan(root)
    confirmed = [s for s in sites if s["bucket"] == "CONFIRMED"]
    suspected = [s for s in sites if s["bucket"] == "SUSPECTED"]
    other = [s for s in sites if s["bucket"] == "OTHER"]

    print("dataclasses-API CALL SITES (AST-resolved, not grep)\n")
    for api in sorted(MIGRATES):
        c = sum(1 for s in confirmed if s["api"] == api)
        p_ = sum(1 for s in suspected if s["api"] == api)
        o = sum(1 for s in other if s["api"] == api)
        if c or p_ or o:
            print(f"  {api:10s} {c:3d} confirmed   {p_:3d} suspected   {o:3d} other")
    print(f"\n  TOTAL      {len(confirmed):3d} confirmed   {len(suspected):3d} suspected   {len(other):3d} other")
    print(f"\n  MIGRATION WORK: {len(confirmed)}–{len(confirmed) + len(suspected)} sites.")
    print("  SUSPECTED cannot be resolved statically — the value's type is not in")
    print("  the source. Those need eyes, and the range is reported rather than")
    print("  collapsed into a single number that would be wrong either way.")

    if args.list:
        for label, group in (("CONFIRMED", confirmed), ("SUSPECTED", suspected), ("OTHER", other)):
            print(f"\n{label}:")
            for s in group:
                rel = s["file"].split("matrx_ai/", 1)[-1]
                print(f"  {rel}:{s['line']}  {s['api']}({s['arg'][:52]})")

    if args.max is not None and len(confirmed) + len(suspected) > args.max:
        total = len(confirmed) + len(suspected)
        print(f"\n🚨 RATCHET: {total} contract-or-suspected sites, limit {args.max}. This count only goes DOWN.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
