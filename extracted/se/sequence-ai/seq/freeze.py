"""
Freezing a version: only the official templates are frozen by the
platform; your own version reads upstream as it builds, and is frozen only when you choose - its base and everything
its build installed kept in your storage, so it can be built again exactly as it is with nothing read from upstream.

You choose it as you deploy - `@seq.policy(freeze=True)` / `@seq.benchmark(freeze=True)` freezes every version of the
file, `seq deploy --freeze` this one - or later, for a version its deployment still holds: `seq policy freeze <name>
v<n>` (`--off` unfreezes it), the copy made from the very images the version runs, never rebuilt. A frozen version's
storage is billed by the GB-month as your version dependencies, each part kept once; the copy's own compute is not
billed (the platform's, as at a build).
"""
from __future__ import annotations

from typing import Any, Callable

from sequence_ai._core.names import segment

_ATTR = "__seq_freeze__"


def declare(cls: type, kwargs: dict, error: type[Exception]) -> type:
    """`cls` with what its decorator said of freeze= kept on it (declared): True or False alone."""
    got = kwargs.get("freeze")
    if got is not None and not isinstance(got, bool):
        raise error(f"freeze= takes True or False, not {got!r}")
    setattr(cls, _ATTR, bool(got))
    return cls


def declared(cls: type) -> bool:
    """Whether the class's decorator froze its versions (freeze=True)."""
    return bool(getattr(cls, _ATTR, False))


def freeze(kind: str, ref: str, *, off: bool = False, base_url: str | None = None,
           echo: Callable[[str], None] = print) -> dict:
    """`seq policy freeze NAME[@vN] [--off]` / `seq benchmark freeze ...`: POST (or, `off`, DELETE)
    /v1/{deployments,benchmarks}/<name>/versions/<n>/freeze, its answer printed - the version named, else the one
    serving (a benchmark's: the one new evals run)."""
    from seq.cli_parser import at_version
    from seq.deployments_cli import _call

    name, version = at_version(ref)
    where = "deployments" if kind == "policy" else "benchmarks"
    if version is None:
        version = _serving(kind, where, name, _call, base_url)
    out: dict[str, Any] = _call("DELETE" if off else "POST",
                                f"/v1/{where}/{segment(name)}/versions/{int(version)}/freeze", base_url) or {}
    state = out.get("dependencies_state")
    if off:
        echo(f"{name} v{version} is not frozen: its version dependencies are deleted within a day, unless another "
             "version still uses them, and billed until then")
    elif state == "copying":
        echo(f"{name} v{version} is being frozen: `seq {kind} versions {name}` says when it is kept")
    elif state == "kept":
        from seq.deps_cost import size

        got = out.get("dependencies_bytes")
        echo(f"{name} v{version} is frozen" + (f": {size(got)} kept in your storage" if got else ""))
    else:
        missing = "; ".join(str(m) for m in out.get("not_self_contained") or []) or "not all of it could be kept"
        echo(f"{name} v{version} is not fully frozen: {missing}")
    return out


def _serving(kind: str, where: str, name: str, call, base_url: str | None) -> int:
    """The version a bare NAME means: the one serving (a benchmark's: the one new evals run)."""
    from sequence_ai.errors import InvalidRequest

    if kind == "policy":
        rows = (call("GET", f"/v1/deployments/{segment(name)}/versions", base_url) or {}).get("data") or []
        got = next((r.get("version") for r in rows if r.get("state") == "serving"), None)
    else:
        rows = (call("GET", f"/v1/benchmarks/{segment(name)}/builds", base_url) or {}).get("builds") or []
        got = next((r.get("version") for r in rows if r.get("serving")), None)
    if got is None:
        raise InvalidRequest(f"{name} has no version {'serving' if kind == 'policy' else 'evals run'}: name one, "
                             f"{name}@v<n>")
    return int(got)


def footer(kind: str, name: str, rows: list[dict]) -> str | None:
    """The versions list's last line when none of the versions it lists is frozen and one could be: how to freeze
    one."""
    if any(r.get("dependencies_state") in ("kept", "copying") for r in rows) or not any(r.get("freezable")
                                                                                         for r in rows):
        return None
    return (f"freeze a version - its base and everything its build installed kept in your storage, to be built again "
            f"exactly as it is: seq {kind} freeze {name}@v<ver>")
