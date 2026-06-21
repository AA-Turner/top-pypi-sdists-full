"""Guard against private-module leaks on the public SDK surface.

Every public class an IDE, ``help()``, ``repr()``, or Sphinx renders shows its
*home module* on hover — e.g. ``smplkit.audit.clients.AuditClient``. If that
home is an underscore-private module (``smplkit.audit._client``), customers see
internal plumbing, which is a documentation leak.

**Why the previous version of this guard was not enough.** It asserted only
that each export's runtime ``__module__`` carried no private segment. But
``__module__`` is a writable attribute: an earlier fix set
``AuditClient.__module__ = "smplkit.audit"`` at import time on classes that
physically lived in ``smplkit/audit/_client.py``. That satisfied the runtime
check — and ``repr()``/``help()``/``python -c`` looked clean — yet PyCharm kept
showing ``smplkit.audit._client`` on hover, because a static analyzer reads
where the ``class`` statement *physically lives*, not the runtime
``__module__``. The runtime override is invisible to static analysis, so the
old guard passed while the leak was still visible in the IDE.

The real fix was to move the ``class`` statements into public (non-underscore)
modules and delete every runtime override. This guard is therefore structured
around two complementary checks:

* :func:`test_source_tree_has_no_runtime_module_overrides` forbids any
  ``__module__`` assignment in the wrapper source. This is the load-bearing
  check: once no override can exist, a class's runtime ``__module__`` is
  guaranteed to equal the module its ``class`` statement physically lives in —
  i.e. exactly what the static analyzer (and PyCharm hover) reports.

* The reachability checks then assert that ``__module__`` carries no private
  segment *and* that a matching ``class`` statement is physically present in
  the public module ``__module__`` names (parsed from source via ``ast``, not
  trusted from the attribute). Together with the override ban, that asserts the
  thing the IDE actually reads: no reachable public class is defined in an
  underscore-private module.

Pure import + AST introspection — no network and no credentials. Where a client
is constructed an explicit ``api_key`` is passed, so nothing resolves
``~/.smplkit``.
"""

from __future__ import annotations

import ast
import asyncio
import importlib
import inspect
import re
from pathlib import Path

import pytest

# ``tests/unit/test_public_module_paths.py`` -> repo root -> ``src/smplkit``.
_SRC_SMPLKIT = Path(__file__).resolve().parents[2] / "src" / "smplkit"

# Every public package whose ``__all__`` defines customer-facing surface. The
# active-record model classes (``Config``, ``Flag``, ``SmplLogger``, ``Job``,
# ``Forwarder``, ``Environment``, ``AccountSettings`` …) and the live-surface
# event/list-page wrappers are all members of one of these ``__all__`` lists,
# so walking these packages covers them too.
_PUBLIC_PACKAGES = [
    "smplkit",
    "smplkit.account",
    "smplkit.audit",
    "smplkit.config",
    "smplkit.flags",
    "smplkit.jobs",
    "smplkit.logging",
    "smplkit.platform",
]

# (top-level namespace, nested sub-namespace accessors). These sub-namespace
# clients (``EnvironmentsClient``, ``SettingsClient``, ``EventsClient``,
# ``RunsClient``, ``LoggersClient`` …) are not in any package ``__all__`` but
# are customer-visible on the client object graph, so their home module must be
# public too.
_SUBNAMESPACE_ACCESSORS = {
    "audit": ("events", "resource_types", "event_types", "categories", "forwarders"),
    "config": (),
    "flags": (),
    "logging": ("loggers", "log_groups"),
    "jobs": ("runs", "retry_policies"),
    "platform": ("environments", "services", "contexts", "context_types"),
    "account": ("settings",),
}


def _private_segment(module_name: str | None) -> str | None:
    """Return the first underscore-prefixed segment of ``module_name``, if any.

    ``"smplkit.audit._client"`` -> ``"_client"``; ``"smplkit.audit.clients"``
    -> None. The generated tree (``smplkit._generated.*``) is private by this
    rule too, which is intentional: a public class must never advertise a home
    inside it.
    """
    if not module_name:
        return None
    for segment in module_name.split("."):
        if segment.startswith("_"):
            return segment
    return None


def _module_to_source(module_name: str) -> Path | None:
    """Map a dotted ``smplkit`` module to the ``.py`` file that defines it.

    ``"smplkit.audit.clients"`` -> ``src/smplkit/audit/clients.py``;
    ``"smplkit"`` -> ``src/smplkit/__init__.py``. Returns ``None`` if neither a
    module file nor a package ``__init__.py`` exists at that path.
    """
    parts = module_name.split(".")
    assert parts[0] == "smplkit", module_name
    rel = parts[1:]
    candidates = []
    if rel:
        candidates.append(_SRC_SMPLKIT.joinpath(*rel).with_suffix(".py"))
        candidates.append(_SRC_SMPLKIT.joinpath(*rel) / "__init__.py")
    else:
        candidates.append(_SRC_SMPLKIT / "__init__.py")
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def _defines_class(source: Path, class_name: str) -> bool:
    """True if ``source`` physically contains a ``class <class_name>`` statement.

    Parsed from the file's AST — the same physical signal a static analyzer
    reads — so a faked ``__module__`` cannot make this pass.
    """
    tree = ast.parse(source.read_text())
    return any(isinstance(node, ast.ClassDef) and node.name == class_name for node in ast.walk(tree))


def _assert_home_is_public(label: str, obj: object) -> None:
    """Assert ``obj``'s home module is public and physically defines it.

    ``obj`` may be a class or an instance; for instances we check ``type(obj)``.
    """
    cls = obj if inspect.isclass(obj) else type(obj)
    module_name = getattr(cls, "__module__", None)

    leaked = _private_segment(module_name)
    assert leaked is None, (
        f"{label}: {cls.__name__}.__module__ == {module_name!r} advertises a "
        f"private module segment {leaked!r}. Move the class to a public module."
    )

    source = _module_to_source(module_name)  # type: ignore[arg-type]
    assert source is not None, f"{label}: cannot locate source file for module {module_name!r}"
    assert _defines_class(source, cls.__name__), (
        f"{label}: {cls.__name__}.__module__ claims {module_name!r}, but no "
        f"`class {cls.__name__}` statement physically lives in {source}. The "
        f"runtime __module__ is faked — a static analyzer (PyCharm hover) will "
        f"show the real, private definition site instead."
    )


def _all_exports() -> list[tuple[str, str]]:
    """Yield ``(package, export_name)`` for every name in each public __all__."""
    params: list[tuple[str, str]] = []
    for pkg_name in _PUBLIC_PACKAGES:
        pkg = importlib.import_module(pkg_name)
        for name in pkg.__all__:
            params.append((pkg_name, name))
    return params


def test_source_tree_has_no_runtime_module_overrides() -> None:
    """No wrapper source file may assign ``__module__`` at runtime.

    This is the load-bearing guard. A runtime ``__module__ = "..."`` override
    masks the underscore-private file a class is physically defined in: it
    cleans up ``repr()``/``help()`` while a static analyzer (and PyCharm hover)
    still reads the real, private location. Banning the assignment outright
    guarantees every class's runtime ``__module__`` equals its physical
    definition module, which is what the reachability tests below rely on.

    Fails on the pre-rename tree (which carried ~70 such overrides) and passes
    once the private modules are renamed public and the overrides removed.
    """
    assert _SRC_SMPLKIT.is_dir(), f"expected wrapper source at {_SRC_SMPLKIT}"
    # Match ``X.__module__ =`` and ``__module__ =`` assignments; exclude the
    # ``__module__ ==`` comparison form.
    override = re.compile(r"__module__\s*=(?!=)")
    offenders: list[str] = []
    for path in sorted(_SRC_SMPLKIT.rglob("*.py")):
        if "_generated" in path.parts:  # generated client code is out of scope
            continue
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            if override.search(line):
                rel = path.relative_to(_SRC_SMPLKIT)
                offenders.append(f"src/smplkit/{rel}:{lineno}: {line.strip()}")

    assert not offenders, (
        "Runtime __module__ overrides found. These reintroduce the IDE-hover "
        "leak this guard prevents: they mask the underscore-private file a "
        "class is physically defined in. Move the class into a public "
        "(non-underscore) module instead of rewriting __module__:\n" + "\n".join(offenders)
    )


@pytest.mark.parametrize(("package_name", "export_name"), _all_exports(), ids=lambda v: v)
def test_public_export_is_defined_in_a_public_module(package_name: str, export_name: str) -> None:
    """Every name in a public ``__all__`` must have a public, real home module.

    Covers the top-level exports, the per-product exports, the active-record
    model classes, and the live-surface event/list-page wrappers — all of which
    are members of one of the public ``__all__`` lists.
    """
    pkg = importlib.import_module(package_name)
    obj = getattr(pkg, export_name)
    _assert_home_is_public(f"{package_name}.{export_name}", obj)


@pytest.mark.parametrize("client_kind", ["sync", "async"])
def test_reachable_subnamespace_clients_are_defined_in_public_modules(client_kind: str) -> None:
    """Attribute-reachable sub-namespace clients must have public home modules.

    ``client.platform.environments``, ``client.audit.events``,
    ``client.jobs.runs`` … are not in any ``__all__`` but are customer-visible
    on the client object graph. Built inside the test body (not at
    parametrize/collection time) so the autouse fixtures that no-op telemetry
    and set ``SMPLKIT_SERVICE`` apply.
    """
    from smplkit import AsyncSmplClient, SmplClient

    client_cls = SmplClient if client_kind == "sync" else AsyncSmplClient
    client = client_cls(api_key="sk_test", base_domain="example.test")

    errors: list[str] = []
    try:
        for ns_name, sub_names in _SUBNAMESPACE_ACCESSORS.items():
            namespaces = [getattr(client, ns_name)]
            namespaces.extend(getattr(namespaces[0], sub) for sub in sub_names)
            for obj in namespaces:
                try:
                    _assert_home_is_public(f"client.{ns_name}", obj)
                except AssertionError as exc:  # collect all leaks, not just the first
                    errors.append(str(exc))
    finally:
        # SmplClient.close() is sync; AsyncSmplClient.close() is a coroutine.
        result = client.close()
        if inspect.isawaitable(result):
            asyncio.run(result)

    assert not errors, f"{client_kind} sub-namespace client leaks:\n" + "\n".join(errors)
