"""Pin the mechanical_rename return-annotation contract.

Bug: 2026-06-08 — the user's work-box TUI hit
  "MechanicalRename.run must yield a Pydantic model as result;
   got <class 'collections.abc.AsyncGenerator'>"
on every session save (every user turn). Root cause: `mechanical_rename.py`
declared `async def run(...) -> AsyncGenerator:` (bare, no type
parameters). BaseTool._extract_result_type can't parse a bare
AsyncGenerator and falls through line 283 (isinstance(t, type) check),
returning AsyncGenerator itself as the result type. The Pydantic
check at line 270-274 then rejects it.

Reproduce in TUI: open drydock in a folder, type any message — drydock
attempts to save the session, validates all tool annotations, blows
up on this one, and the loop pattern emerges because the model retries
its previous tool call (often nothing in particular) on the next turn.
"""
from drydock.core.tools.builtins.mechanical_rename import (
    MechanicalRename, MechanicalRenameResult, MechanicalRenameArgs,
)


def test_run_return_annotation_resolves_to_result_type():
    """BaseTool._extract_result_type must return the Pydantic result class."""
    args_t, result_t = MechanicalRename._get_tool_args_results()
    assert args_t is MechanicalRenameArgs
    assert result_t is MechanicalRenameResult, (
        f"expected MechanicalRenameResult, got {result_t!r} — "
        "the run() annotation is probably a bare AsyncGenerator again"
    )


def test_all_builtin_tools_extract_clean_result_types():
    """Every builtin tool's run() annotation must be parameterized correctly.

    Discovers every BaseTool subclass under drydock/core/tools/builtins/
    by walking the package — so a freshly-added tool gets covered with
    no test maintenance. Catches the same class of bug for any other
    tool that ships with a bare AsyncGenerator annotation in the future.
    """
    import importlib
    import pkgutil

    from pydantic import BaseModel

    from drydock.core.tools import builtins as builtins_pkg
    from drydock.core.tools.base import BaseTool

    seen_tools: list[tuple[str, type]] = []
    failures: list[str] = []

    for module_info in pkgutil.iter_modules(builtins_pkg.__path__):
        modname = f"{builtins_pkg.__name__}.{module_info.name}"
        try:
            mod = importlib.import_module(modname)
        except ImportError:
            # Optional deps (e.g. solve_tool needs z3, prolog needs swipl);
            # if the module can't import, skip it — the tool isn't going
            # to ship in this env either.
            continue
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if not (
                isinstance(obj, type)
                and issubclass(obj, BaseTool)
                and obj is not BaseTool
                and obj.__module__ == modname  # skip re-exports
            ):
                continue
            try:
                _, result_t = obj._get_tool_args_results()
            except Exception as e:
                failures.append(f"{modname}.{attr}: extraction failed: {e}")
                continue
            if not (isinstance(result_t, type) and issubclass(result_t, BaseModel)):
                failures.append(
                    f"{modname}.{attr}: resolved result_t={result_t!r}, "
                    f"not a Pydantic BaseModel — bare AsyncGenerator annotation?"
                )
                continue
            seen_tools.append((modname, obj))

    assert not failures, (
        "tool annotation regressions:\n  " + "\n  ".join(failures)
    )
    # Sanity: we should have discovered at least the obvious tools.
    discovered = {cls.__name__ for _, cls in seen_tools}
    for expected in ("Bash", "WriteFile", "ReadFile", "SearchReplace", "MechanicalRename"):
        assert expected in discovered, (
            f"discovery missed {expected!r}; only saw: {sorted(discovered)[:15]}…"
        )
