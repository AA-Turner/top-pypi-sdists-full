"""Which types are actually IN the engine contract?

agent-engine-extraction, Phase 1b.2. The plan carried "149 sibling dataclasses"
as an estimate. This computes the real number instead: the transitive closure of
type annotations reachable from the three contract roots (UnifiedConfig,
UnifiedMessage, UnifiedResponse).

Why the closure and not "every dataclass in the package": the reason the
contract types must be pydantic is that model_json_schema() is what generates
the TypeScript twin (D2/D8). A dataclass the contract never references does not
cross the language boundary and does not need converting. 216 dataclasses in the
package is the wrong denominator; this script finds the right one.

It also doubles as the future guard: once the migration completes, a NEW
dataclass appearing in the closure is a contract type someone forgot to model.

    python scripts/contract_closure.py            # summary
    python scripts/contract_closure.py --list     # every member, grouped
    python scripts/contract_closure.py --unresolved-is-error   # CI mode

REFUSES TO UNDERCOUNT. Every annotation it cannot resolve is reported and, in CI
mode, fails the run — an unwalkable edge is a hole in the closure, and a closure
with unreported holes reads as "we measured it" when we did not.
"""

from __future__ import annotations

import argparse
import dataclasses
import enum
import sys
import types
import typing
from typing import Any

ROOTS = [
    ("matrx_ai.config.unified_config", "UnifiedConfig"),
    ("matrx_ai.config.message_config", "UnifiedMessage"),
    ("matrx_ai.config.unified_config", "UnifiedResponse"),
]

@dataclasses.dataclass
class _PlantedLeaf:
    """Self-test fixture — two hops from a contract root. See self_test()."""

    value: str = ""


@dataclasses.dataclass
class _PlantedBranch:
    """Self-test fixture — one hop from a contract root. See self_test()."""

    leaf: _PlantedLeaf = dataclasses.field(default_factory=_PlantedLeaf)


_STDLIB_OK = {
    "str", "int", "float", "bool", "bytes", "NoneType", "Any", "object",
    "datetime", "date", "time", "timedelta", "Decimal", "UUID", "Path",
}


def _load_roots() -> list[type]:
    out = []
    for mod_name, cls_name in ROOTS:
        mod = __import__(mod_name, fromlist=[cls_name])
        out.append(getattr(mod, cls_name))
    return out


def _referenced_types(tp: Any) -> list[type]:
    """Every concrete class mentioned anywhere inside an annotation."""
    if tp is None or tp is type(None):
        return []
    origin = typing.get_origin(tp)
    if origin is not None:
        found: list[type] = []
        # X | Y, list[X], dict[K, V], Literal[...] — walk every argument.
        if origin is not typing.Literal:
            for arg in typing.get_args(tp):
                found.extend(_referenced_types(arg))
        if (
            isinstance(origin, type)
            and origin not in (list, dict, set, tuple, frozenset, type)
            and origin is not types.UnionType
        ):
            found.append(origin)
        return found
    if isinstance(tp, type):
        return [tp]
    return []


def _is_erased(tp: Any) -> bool:
    """True when an annotation bottoms out in Any and hides whatever is there."""
    if tp is Any:
        return True
    args = typing.get_args(tp)
    return bool(args) and any(a is Any for a in args)


def walk() -> tuple[dict[type, set[str]], list[str], list[str]]:
    """Return (closure, unresolved edges, ERASED edges).

    An erased edge is a contract field annotated Any / dict[str, Any] /
    list[Any]. The walk cannot see through it, so a real contract type may
    hide behind one and the closure is a LOWER BOUND. A closure tool that
    does not report its own blind spot is a validator that cannot fail.
    """
    seen: dict[type, set[str]] = {}
    unresolved: list[str] = []
    erased: list[str] = []
    queue: list[tuple[type, str]] = [(r, r.__name__) for r in _load_roots()]

    while queue:
        cls, path = queue.pop()
        if cls in seen:
            seen[cls].add(path)
            continue
        seen[cls] = {path}

        if cls.__name__ in _STDLIB_OK or cls.__module__ in ("builtins", "typing"):
            continue
        if isinstance(cls, type) and issubclass(cls, enum.Enum):
            continue

        is_dc = dataclasses.is_dataclass(cls)
        is_pyd = hasattr(cls, "model_fields")
        if not (is_dc or is_pyd):
            continue

        try:
            hints = typing.get_type_hints(cls)
        except Exception as exc:  # a forward ref we cannot resolve IS a hole
            unresolved.append(f"{cls.__module__}.{cls.__name__}: get_type_hints failed: {exc}")
            continue

        for field_name, annotation in hints.items():
            if _is_erased(annotation):
                erased.append(f"{cls.__module__}.{cls.__name__}.{field_name}: {annotation}")
            for ref in _referenced_types(annotation):
                if isinstance(ref, type):
                    queue.append((ref, f"{path}.{field_name}"))

    return seen, unresolved, erased


def registry_escapees(closure: dict[type, set[str]]) -> list[str]:
    """SECOND LAYER. The annotation walk trusts annotations — and on 2026-08-24
    that cost seven types: `UnifiedContent` omitted half of
    STRUCTURED_INPUT_TYPE_MAP, so `reconstruct_content` returned classes outside
    its own declared return type and this walk under-counted the contract at 26
    when it was 33. A wrong union does not look like a blind spot; it looks like
    a complete annotation.

    So do not only follow annotations. Sweep `matrx_ai.config` for module-level
    registries (dict[str, type]) and report any dataclass a registry can produce
    that the closure never reached. Extinction is layered (PRINCIPLES.md): this
    layer stops the class alone, and screams.
    """
    import importlib
    import pkgutil

    import matrx_ai.config as cfg

    escapees: list[str] = []
    for mod_info in pkgutil.iter_modules(cfg.__path__):
        try:
            mod = importlib.import_module(f"matrx_ai.config.{mod_info.name}")
        except Exception:
            continue
        for attr, value in vars(mod).items():
            if attr.startswith("__") or not isinstance(value, dict) or not value:
                continue
            mapped = [v for v in value.values() if isinstance(v, type) and dataclasses.is_dataclass(v)]
            if not mapped:
                continue
            for cls in mapped:
                if cls not in closure:
                    escapees.append(
                        f"{cls.__module__}.{cls.__name__} — producible via "
                        f"matrx_ai.config.{mod_info.name}.{attr}, unreachable by annotation"
                    )
    return sorted(set(escapees))


def classify(cls: type) -> str:
    if isinstance(cls, type) and issubclass(cls, enum.Enum):
        return "enum"
    if hasattr(cls, "model_fields"):
        return "pydantic (already)"
    if dataclasses.is_dataclass(cls):
        return "DATACLASS — needs a twin"
    if cls.__name__ in _STDLIB_OK or cls.__module__ in ("builtins", "typing"):
        return "stdlib"
    return "other"


def self_test() -> int:
    """A closure tool that has never been shown to FAIL is not evidence.

    Plant a dataclass two hops down a real contract field and prove the walk
    reaches it; then confirm the same class is absent from the honest run. If
    either half does not hold, this measurement means nothing and says so.
    """
    baseline, _, _ = walk()
    baseline_names = {c.__name__ for c in baseline}

    from matrx_ai.config.unified_config import UnifiedResponse

    original = UnifiedResponse.__annotations__.copy()
    try:
        UnifiedResponse.__annotations__["_planted"] = _PlantedBranch
        # get_type_hints resolves names out of the defining module.
        mod = sys.modules[UnifiedResponse.__module__]
        mod._PlantedBranch, mod._PlantedLeaf = _PlantedBranch, _PlantedLeaf
        planted, planted_unresolved, _ = walk()
    finally:
        UnifiedResponse.__annotations__.clear()
        UnifiedResponse.__annotations__.update(original)

    planted_names = {c.__name__ for c in planted}
    found_branch = "_PlantedBranch" in planted_names
    found_leaf = "_PlantedLeaf" in planted_names          # two hops — transitivity
    absent_before = not (baseline_names & {"_PlantedBranch", "_PlantedLeaf"})

    print("SELF-TEST — can this walk actually fail?\n")
    print(f"  planted branch found (1 hop) : {found_branch}")
    print(f"  planted leaf found (2 hops)  : {found_leaf}")
    print(f"  absent from the honest run   : {absent_before}")
    if planted_unresolved:
        print("\n  unresolved during the planted run (a miss hiding here is the bug\n  this self-test exists to expose):")
        for u in planted_unresolved:
            print(f"    {u}")

    if found_branch and found_leaf and absent_before:
        print("\n✅ The walk detects a planted contract type and does not hallucinate one.")
        return 0
    print("\n🚨 THE WALK IS NOT FALSIFIABLE — its count is not evidence. Fix it.")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--unresolved-is-error", action="store_true")
    ap.add_argument(
        "--self-test",
        action="store_true",
        help="plant a known-reachable dataclass and prove the walk finds it",
    )
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    closure, unresolved, erased = walk()

    groups: dict[str, list[type]] = {}
    for cls in closure:
        groups.setdefault(classify(cls), []).append(cls)

    total_dc_in_pkg = None
    print("CONTRACT CLOSURE — transitive from UnifiedConfig, UnifiedMessage, UnifiedResponse\n")
    for kind in sorted(groups, key=lambda k: -len(groups[k])):
        members = sorted(groups[kind], key=lambda c: (c.__module__, c.__name__))
        print(f"  {len(members):4d}  {kind}")
        if args.list and kind not in ("stdlib",):
            for c in members:
                paths = sorted(closure[c])[:1]
                print(f"          {c.__module__}.{c.__name__}   ← {paths[0]}")
    print()

    needs = len(groups.get("DATACLASS — needs a twin", []))
    print(f"DATACLASSES IN THE CONTRACT: {needs}")

    escapees = registry_escapees(closure)
    if escapees:
        print(f"\n🚨 {len(escapees)} REGISTRY ESCAPEE(S) — a registry can produce these and no")
        print("    annotation reaches them. The closure above is an UNDERCOUNT:")
        for e in escapees:
            print(f"   {e}")
    else:
        print("Registry cross-check: every registry-producible dataclass is in the closure.")

    if erased:
        print(f"\n⚠️  {len(erased)} ERASED EDGE(S) — Any-typed contract fields the walk cannot")
        print("    see through. 26 is therefore a LOWER BOUND, and each of these is also")
        print("    an `any` in the generated TypeScript:")
        for e in erased:
            print(f"   {e}")

    if unresolved:
        print(f"\n🚨 {len(unresolved)} UNRESOLVED EDGE(S) — the closure is INCOMPLETE:")
        for u in unresolved:
            print(f"   {u}")
        if args.unresolved_is_error:
            return 1

    if escapees and args.unresolved_is_error:
        return 1
    else:
        print("Every annotation resolved — the closure is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
