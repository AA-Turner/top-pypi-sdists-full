"""
Loading what a command names — a file, file.py:Class, pkg.module:Class, or -m pkg.module[:Class] — and what the class
it finds is: a @seq.policy, a @seq.benchmark or a @seq.adapter. `seq deploy` (its --dry-run too), `seq adapter check`,
`seq port export` and `seq eval run --adapter ./file.py:Class` all load through here.
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

from seq._partial import refusals_kept
from seq.errors import SeqAuthoringError


def load_deployable(ref: str) -> tuple[str, type]:
    """The decorated class `ref` names, and what it is: "policy", "benchmark" or "adapter".

    `ref` is `path/to/file.py`, `file.py:Class`, `pkg.module` or `pkg.module:Class` (`-m` passes the module forms).
    Without a class name the module must define exactly one decorated class. A file is imported under its own module
    name with its directory on `sys.path` — the name `handler_ref` records — so a file that loads here also loads on
    the worker."""
    from seq.adapter import _ADAPTER_ATTR
    from seq.benchmark_registry import _BENCH_ATTR
    from seq.registry import _REG_ATTR

    def kind_of(obj: Any) -> str | None:
        own = getattr(obj, "__dict__", {}) if isinstance(obj, type) else {}
        return ("policy" if _REG_ATTR in own else "benchmark" if _BENCH_ATTR in own
                else "adapter" if _ADAPTER_ATTR in own else None)

    target, _, cls_name = ref.partition(":")
    module = import_target(target)
    if cls_name:
        cls = getattr(module, cls_name, None)
        if cls is None:
            raise SeqAuthoringError(f"{ref}: no attribute {cls_name!r} in {target}")
        kind = kind_of(cls)
        if kind is None:
            raise SeqAuthoringError(f"{ref}: {cls_name} is not a @seq.policy, @seq.planner, @seq.benchmark or @seq.adapter "
                                    "class")
        return kind, cls
    found = {id(obj): obj for obj in vars(module).values() if kind_of(obj)}
    if any(kind_of(c) != "adapter" for c in found.values()):

        found = {k: c for k, c in found.items() if kind_of(c) != "adapter"}
    if not found:
        raise SeqAuthoringError(f"{target} defines no @seq.policy, @seq.planner, @seq.benchmark or @seq.adapter class; "
                                f"decorate one, or name it with '{target}:ClassName'")
    if len(found) > 1:
        names = ", ".join(sorted(c.__name__ for c in found.values()))
        raise SeqAuthoringError(f"{target} defines {len(found)} policies, benchmarks and adapters ({names}); name one "
                                f"with '{target}:ClassName'")
    cls = next(iter(found.values()))
    return kind_of(cls), cls



_OWN_DISTS = {"seq": "sequence-ai", "sequence_ai": "sequence-ai", "sequence_base": "sequence-base"}


def _version_of(dist: str) -> str:
    """' 0.55.0', the installed release of `dist`, or '' where its metadata cannot be read."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        return f" {version(dist)}"
    except PackageNotFoundError:
        return ""


def _missing_dependency(exc: ModuleNotFoundError, own: str) -> str | None:
    """A package the policy file imports that is not installed here, when that - not the policy module itself - is why
    its import failed: ModuleNotFoundError.name is the missing top-level module, and here it differs from the policy's
    own name. seq deploy imports the file on this machine to build the deployment, so what it imports at the top must
    be installed here too; naming the package and the fix beats re-raising "No module named 'numpy'". None when the
    policy module itself was not found (a different problem, with its own words)."""
    missing = getattr(exc, "name", None)
    if not missing:
        return None
    top = own.split(".", 1)[0]
    if missing == own or missing == top or own.startswith(missing + "."):
        return None



    dist = _OWN_DISTS.get(missing.split(".", 1)[0]) if "." in missing else None
    if dist:
        return f"imports {missing!r}, which this {dist}{_version_of(dist)} does not have: a module of its own, not a " \
               "package to install"
    return (f"imports {missing!r}, which is not installed here. seq deploy reads your policy file on this machine to "
            f"build the deployment, so a package it imports at the top must be installed here too - pip install "
            f"{missing} (or move a heavy import into the method that uses it)")


def load_folder(folder: str | os.PathLike, name: str | None = None) -> tuple[str, type]:
    """The class `seq deploy [folder]` deploys, and what it is: found by reading the folder's files (seq.discover) and
    imported by its path in the folder - the folder first on sys.path and the class's own folder second, as running
    that file would put it - so what imports here imports on the worker, where the folder is the code's top.
    """
    from seq import discover

    path = Path(folder)
    if path.suffix == ".py" or path.is_file():
        place = path.parent if str(path.parent) not in ("", ".") else Path(".")
        raise SeqAuthoringError(f"seq deploy takes a folder: deploy the folder {path.name} is in - seq deploy {place} "
                                "(add --name <name> when it holds several)")
    if not path.is_dir():
        raise SeqAuthoringError(f"{folder}: no such folder")
    root = path.resolve()
    found, read = discover.find(discover.files_of(root))
    chosen = discover.choose(found, name, str(folder), read)
    top = chosen.module.split(".", 1)[0]
    held = sys.modules.get(top)
    held_at = getattr(held, "__file__", None) or next(iter(getattr(held, "__path__", []) or []), None)
    if held is not None and top in _LOADED:



        brought = [m for m in _IMPORTED_WITH.get(chosen.module, ()) if _within(sys.modules.get(m), root)]
        for loaded in [m for m in sys.modules if m == top or m.startswith(top + ".")] + brought:
            sys.modules.pop(loaded, None)
    elif held is not None and held_at and root not in Path(held_at).resolve().parents:
        raise SeqAuthoringError(f"{discover.shown(root, chosen.path)}: rename it or its folder - {top!r} is already a "
                                f"module here ({held_at}), so the platform would import that instead of your code")
    _LOADED.add(top)



    own = root.joinpath(*chosen.module.split(".")[:-1])
    for at, place in ((0, root), (1, own)):
        if str(place) not in sys.path:
            sys.path.insert(at, str(place))
    before = set(sys.modules)
    try:
        with refusals_kept():
            module = importlib.import_module(chosen.module)
    except SeqAuthoringError:
        raise
    except ModuleNotFoundError as exc:
        dep = _missing_dependency(exc, chosen.module)
        raise SeqAuthoringError(f"{discover.shown(root, chosen.path)}: {dep}" if dep else
                                f"{discover.shown(root, chosen.path)}: failed to import — {exc}"
                                f"{_newer_contract(exc)}") from exc
    except Exception as exc:
        raise SeqAuthoringError(f"{discover.shown(root, chosen.path)}: failed to import — {exc}"
                                f"{_newer_contract(exc)}") from exc
    _record(chosen.module, before, fresh=chosen.module not in before)
    cls = getattr(module, chosen.qualname, None)
    if cls is None:
        raise SeqAuthoringError(f"{chosen.ref}: no class {chosen.qualname!r} after importing {chosen.module}")
    return chosen.deploys_as, cls


def _within(module: Any, root: Path) -> bool:
    """Whether `module` was loaded from a file under the folder `root`."""
    where = getattr(module, "__file__", None)
    return bool(where) and root in Path(where).resolve().parents


def load_kind(ref: str, kind: str) -> type:
    got, cls = load_deployable(ref)
    if got != kind:
        raise SeqAuthoringError(f"{ref}: {cls.__name__} is a @seq.{got}, not a @seq.{kind}")
    return cls



_LOADED: set[str] = set()


_IMPORTED_WITH: dict[str, tuple[str, ...]] = {}


def imported_with(module_name: str) -> tuple[str, ...] | None:
    """The modules first loaded while `module_name` was imported through here; None when it was not."""
    return _IMPORTED_WITH.get(module_name)


def _record(name: str, before: set[str], *, fresh: bool = False) -> None:
    """Keep what importing `name` loaded: a fresh import's replaces the record (a folder loaded again in this process,
    its module of the same name), an import that found the module loaded keeps the first."""
    got = tuple(sorted(set(sys.modules) - before))
    if fresh:
        _IMPORTED_WITH[name] = got
    else:
        _IMPORTED_WITH.setdefault(name, got)


def _newer_contract(exc: Exception) -> str:
    """What to add when a policy file declares a contract field this machine's sequence-base does not know - a file
    written for a newer SDK, as a template's next version is: pydantic's own words ("Extra inputs are not permitted")
    do not say to upgrade. "" for any other failure."""
    errors = getattr(exc, "errors", None)
    try:
        extra = [e for e in errors() if e.get("type") == "extra_forbidden"] if callable(errors) else []
    except Exception:
        extra = []
    if not extra:
        return ""
    try:
        from importlib.metadata import version

        have = version("sequence-base")
    except Exception:
        have = "here"
    names = ", ".join(sorted({".".join(str(p) for p in e.get("loc", ())) for e in extra}))
    return (f"\n{names}: this sequence-base ({have}) does not know that field, so the file was written for a newer "
            f"one: pip install -U sequence-ai")


def import_target(target: str) -> Any:
    """Import `target`, which is either a dotted module path or a path to a `.py` file."""
    before = set(sys.modules)
    if target.endswith(".py") or os.sep in target or (os.altsep and os.altsep in target):
        path = Path(target).resolve()
        if not path.is_file():
            raise SeqAuthoringError(f"{target}: no such file")
        mod_name = path.stem


        taken = ("the standard library's" if mod_name in sys.stdlib_module_names
                 else "an installed" if mod_name in sys.modules and mod_name not in _LOADED else None)
        if taken:
            raise SeqAuthoringError(f"{target}: rename the file — {mod_name!r} is {taken} module, so the platform "
                                    "would import that instead of your code")
        _LOADED.add(mod_name)
        parent = str(path.parent)

        if parent not in sys.path:
            sys.path.insert(0, parent)
        spec = importlib.util.spec_from_file_location(mod_name, path)
        if spec is None or spec.loader is None:
            raise SeqAuthoringError(f"{target}: could not load as a module")
        module = importlib.util.module_from_spec(spec)


        sys.modules[mod_name] = module
        try:

            with refusals_kept():
                spec.loader.exec_module(module)
        except SeqAuthoringError:
            raise
        except ModuleNotFoundError as exc:
            dep = _missing_dependency(exc, mod_name)
            raise SeqAuthoringError(f"{target}: {dep}" if dep else
                                    f"{target}: failed to import — {exc}{_newer_contract(exc)}") from exc
        except Exception as exc:
            raise SeqAuthoringError(f"{target}: failed to import — {exc}{_newer_contract(exc)}") from exc
        _record(mod_name, before)
        return module




    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)
    try:
        with refusals_kept():
            module = importlib.import_module(target)
        _record(target, before)
        return module
    except SeqAuthoringError:
        raise
    except ModuleNotFoundError as exc:
        dep = _missing_dependency(exc, target)
        raise SeqAuthoringError(f"{target}: {dep}" if dep else
                                f"{target}: no module named {target!r} (run from the policy's directory, or pass "
                                f"the path as {target}.py:ClassName)") from exc
    except Exception as exc:
        raise SeqAuthoringError(f"{target}: could not import module — {exc}{_newer_contract(exc)}") from exc
