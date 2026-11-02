"""The pre-9.0 ``adcp.types.generated_poc`` path resolves, as the same objects.

#1360 measured 110 deep ``generated_poc`` imports in ONE production seller, so
9.0 keeps the old path working and warns rather than breaking all of them at
once. The danger in doing that is the one the review named: redirecting a
package's ``__path__`` makes the import machinery LOAD each module a second
time under the old name, so there are two module objects and two class objects
per class, and an ``isinstance`` against the wrong one fails for no visible
reason. ``tests/test_export_surface_is_derived.py`` exists to refuse that, by
asserting every generated class is DEFINED at the address it is imported from.

``adcp.types._generated_poc_alias`` is not that. Its loader executes nothing:
it imports the canonical module and hands that object back, so ``sys.modules``
holds ONE object under both keys. This module grades that claim, and the four
others the alias has to keep:

1. the leaf class is the SAME object, ``is`` not ``==``;
2. ``sys.modules`` holds one module object under both keys;
3. a ``DeprecationWarning`` naming the new path, once per module;
4. the shared object carries no trace of having been reached through the old
   name — which is the property ``test_export_surface_is_derived`` rests on;
5. the alias does not outlive the major that removes it.

The module list is derived — the root, every entry in
``adcp.types.domains.DOMAINS``, and the first few leaf modules each domain
package actually contains — rather than hand-listed, because a hand-listed
sample stops covering the tree the moment the tree changes.

**A root discovery schema is the one name for which (2) cannot hold, and #1402
is what happens when nothing says so.** ``generated_poc.brand`` resolved to
``domains.brand`` and ``from ... import Brand`` raised, because ``brand.json``
now generates to ``domains/brand_discovery.py`` and ``domains/brand/__init__.py``
is the domain aggregator. The suite above could not see it: it asserted over the
names the CANONICAL module binds, never over the names the PRE-9.0 module
exported. The split family below asserts the second direction, over every public
name of both halves, and takes its split set from the generator's own
``ROOT_DISCOVERY_SCHEMAS`` so the next split is graded without anyone extending
a list here.
"""

from __future__ import annotations

import importlib
import importlib.util
import pkgutil
import re
import subprocess
import sys
import warnings
from pathlib import Path
from types import ModuleType

import pytest

import adcp.types  # noqa: F401  — importing it is what installs the finder
import adcp.types.domains as domains
from adcp.types._generated_poc_alias import (
    CANONICAL_ROOT,
    DEPRECATED_ROOT,
    REMOVED_IN_MAJOR,
    ROOT_DISCOVERY_SUFFIX,
    _AliasFinder,
    _AliasLoader,
    _SplitAliasModule,
    canonical_name,
    discovery_half,
    install,
)
from scripts.generate_types import ROOT_DISCOVERY_SCHEMAS

_REPO_ROOT = Path(__file__).resolve().parents[1]

#: Leaf modules sampled per domain. Two is enough to grade the mechanism —
#: which is per-name, not per-module — without importing 1088 modules.
_LEAVES_PER_DOMAIN = 2


def _canonical_module_names() -> list[str]:
    """The canonical modules this suite grades, derived from the tree."""

    names = [CANONICAL_ROOT]
    for domain in domains.DOMAINS:
        package_name = f"{CANONICAL_ROOT}.{domain}"
        names.append(package_name)
        package = importlib.import_module(package_name)
        # A domain whose schemas are few enough generates a module, not a
        # package, and has no submodules to sample.
        search_path = getattr(package, "__path__", None)
        if search_path is None:
            continue
        leaves = sorted(info.name for info in pkgutil.iter_modules(search_path))
        names.extend(f"{package_name}.{leaf}" for leaf in leaves[:_LEAVES_PER_DOMAIN])
    return names


CANONICAL_MODULES = _canonical_module_names()
DEPRECATED_MODULES = [DEPRECATED_ROOT + name[len(CANONICAL_ROOT) :] for name in CANONICAL_MODULES]
PAIRS = list(zip(DEPRECATED_MODULES, CANONICAL_MODULES, strict=True))
PAIR_IDS = [deprecated[len(DEPRECATED_ROOT) + 1 :] or "<root>" for deprecated, _ in PAIRS]

#: The schemas whose pre-9.0 module and 9.0 module are not the same address,
#: read from the generator's own declaration rather than named here. Each entry
#: is ``(deprecated module, discovery half, aggregator half)``: ``brand.json``
#: generated into ``generated_poc/brand/__init__.py`` and now generates into
#: ``domains/brand_discovery.py``, leaving ``domains/brand/__init__.py`` to the
#: domain aggregator, so one deprecated name has two canonical halves.
SPLITS = [
    (
        f"{DEPRECATED_ROOT}.{schema.stem}",
        f"{CANONICAL_ROOT}.{output.stem}",
        f"{CANONICAL_ROOT}.{schema.stem}",
    )
    for schema, output in sorted(ROOT_DISCOVERY_SCHEMAS.items())
]
SPLIT_IDS = [schema.stem for schema in sorted(ROOT_DISCOVERY_SCHEMAS)]
SPLIT_DEPRECATED = frozenset(deprecated for deprecated, _, _ in SPLITS)

#: The pairs for which one deprecated name has exactly one canonical module.
UNSPLIT_PAIRS = [pair for pair in PAIRS if pair[0] not in SPLIT_DEPRECATED]
UNSPLIT_PAIR_IDS = [
    deprecated[len(DEPRECATED_ROOT) + 1 :] or "<root>" for deprecated, _ in UNSPLIT_PAIRS
]


def _import_deprecated(name: str) -> ModuleType:
    """Import a deprecated path with the warning suppressed.

    Suppressed because every import here is deliberate; the warning itself is
    graded by ``test_the_warning_fires_once_per_module_and_names_the_new_path``
    and, on a real import, by the subprocess test below.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        return importlib.import_module(name)


def test_the_graded_module_list_is_not_empty() -> None:
    """A tree reorganization must not empty this suite silently."""
    assert len(domains.DOMAINS) == 26, domains.DOMAINS
    assert len(PAIRS) > 60, len(PAIRS)
    assert CANONICAL_MODULES[0] == CANONICAL_ROOT


# ---------------------------------------------------------------------------
# Properties 1 and 2 — one module object, one class object
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("deprecated", "canonical"), UNSPLIT_PAIRS, ids=UNSPLIT_PAIR_IDS)
def test_sys_modules_holds_one_object_under_both_keys(deprecated: str, canonical: str) -> None:
    """The property a ``__path__`` redirect cannot keep.

    Stated over every name that did not split. A split name has two canonical
    halves and so cannot be one object with either; what it keeps instead —
    the shim defines no class, so every class reached through it is still the
    canonical class, which is the property this one exists to protect — is
    graded by ``test_a_split_name_defines_nothing_and_serves_canonical_classes``.
    """
    old = _import_deprecated(deprecated)
    new = importlib.import_module(canonical)

    assert old is new
    assert sys.modules[deprecated] is sys.modules[canonical]
    assert len({id(sys.modules[deprecated]), id(sys.modules[canonical])}) == 1


@pytest.mark.parametrize(("deprecated", "canonical"), UNSPLIT_PAIRS, ids=UNSPLIT_PAIR_IDS)
def test_every_class_reached_through_the_old_path_is_the_canonical_class(
    deprecated: str, canonical: str
) -> None:
    """Stated over every public class the module binds, not over a sample.

    ``is`` rather than ``==``: two pydantic models built from one schema compare
    unequal as classes but would both satisfy a structural check, and it is
    object identity that makes ``isinstance`` work.

    A split name is graded by the split tests instead. Not because the identity
    is weaker there — it is not, the shim defines no class — but because the
    canonical module this compares against is only HALF of what the pre-9.0
    module bound, and the two halves share 12 names (``Logo``, ``Colors``,
    ``Fonts``, ...) that the pre-9.0 import resolved to the discovery class.
    """
    old = _import_deprecated(deprecated)
    new = importlib.import_module(canonical)

    public = [name for name in dir(new) if not name.startswith("_")]
    assert public, f"{canonical} binds nothing public"
    for name in public:
        assert getattr(old, name) is getattr(new, name), f"{deprecated}.{name}"


def test_the_identity_sweep_grades_thousands_of_classes() -> None:
    """The floor the per-module test cannot carry.

    A module that binds only aliases still passes the sweep above, and a tree
    reorganization could leave every graded module in that state. This counts
    the classes the sweep actually compared, so the suite cannot go quiet.
    """
    modules = [_import_deprecated(name) for name in DEPRECATED_MODULES]

    classes = sum(
        1
        for module in modules
        for name in dir(module)
        if not name.startswith("_") and isinstance(getattr(module, name), type)
    )
    assert classes > 1000, f"only {classes} classes graded — the sample collapsed"


def test_every_spelling_an_adopter_may_have_written_resolves() -> None:
    """Each of these reaches the import system by a different route.

    A dotted ``from ... import <name>`` resolves the leaf through
    ``_find_and_load``; ``from <package> import <submodule>`` goes through
    ``_handle_fromlist``; and reaching ``adcp.types.generated_poc`` as an
    attribute goes through ``adcp.types.__getattr__``'s submodule passthrough,
    which probes with ``find_spec`` before importing. The finder has to answer
    for all three.

    ``importlib.reload`` of a deprecated name is graded in the subprocess test
    below, not here: reloading a generated module rebuilds its classes, so the
    domain root and ``_generated`` keep the pre-reload objects and
    ``test_export_surface_is_derived`` fails for the rest of the session. It
    caught exactly that when the assertion lived here.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from adcp.types.generated_poc import core as old_core
        from adcp.types.generated_poc.core import format_id as old_format_id
        from adcp.types.generated_poc.media_buy.package_request import (
            PackageRequest as OldPackageRequest,
        )

        from adcp.types import generated_poc as old_root

    import adcp.types.domains as new_root
    from adcp.types.domains import core as new_core
    from adcp.types.domains.core import format_id as new_format_id
    from adcp.types.domains.media_buy.package_request import PackageRequest

    assert old_root is new_root
    assert old_core is new_core
    assert old_format_id is new_format_id
    assert OldPackageRequest is PackageRequest
    assert adcp.types.generated_poc.core.format_id is new_format_id


# ---------------------------------------------------------------------------
# A root discovery schema — the one case a prefix rename gets wrong (#1402)
# ---------------------------------------------------------------------------


def test_the_split_set_is_read_from_the_generator_not_named_here() -> None:
    """A split this suite does not know about is a hole it cannot see.

    ``ROOT_DISCOVERY_SCHEMAS`` is the generator's own declaration of which
    schema's module is not at its own stem, so a schema added there is graded
    by the tests below without anyone remembering to extend a list. This
    asserts the derivation is wired and non-empty — a renamed or emptied
    declaration would otherwise leave every test below vacuously green.
    """
    assert SPLITS, "ROOT_DISCOVERY_SCHEMAS is empty — the split tests grade nothing"
    assert (
        f"{DEPRECATED_ROOT}.brand",
        f"{CANONICAL_ROOT}.brand_discovery",
        f"{CANONICAL_ROOT}.brand",
    ) in SPLITS


@pytest.mark.parametrize(("deprecated", "discovery", "aggregator"), SPLITS, ids=SPLIT_IDS)
def test_a_root_discovery_module_is_named_the_way_the_alias_derives_it(
    deprecated: str, discovery: str, aggregator: str
) -> None:
    """The alias derives the second half by suffix; the generator must spell it so.

    ``discovery_half`` appends ``ROOT_DISCOVERY_SUFFIX`` to the domain package's
    name rather than carrying a second copy of ``ROOT_DISCOVERY_SCHEMAS``. That
    is a derivation, not a guess, only while the generator keeps naming these
    modules ``<stem>_discovery`` — so this is the assertion that a differently
    named entry fails the build instead of silently reopening #1402.
    """
    assert discovery == aggregator + ROOT_DISCOVERY_SUFFIX
    assert discovery_half(aggregator) == discovery
    # And the derivation fires for nothing else: a leaf module, and a domain
    # with no discovery sibling, are ordinary prefix renames.
    assert discovery_half(f"{CANONICAL_ROOT}.core.format_id") is None
    assert discovery_half(f"{CANONICAL_ROOT}.media_buy") is None


@pytest.mark.parametrize(("deprecated", "discovery", "aggregator"), SPLITS, ids=SPLIT_IDS)
def test_every_name_a_split_pre_9_0_module_exported_resolves_through_the_alias(
    deprecated: str, discovery: str, aggregator: str
) -> None:
    """#1402: the module resolved and its contents did not.

    ``generated_poc/brand/__init__.py`` WAS ``brand.json`` — 140 classes, among
    them ``Brand``, ``BrandDiscovery3`` and ``LocalizedName``. Those classes are
    now in ``domains/brand_discovery.py``, and a prefix rename sent the
    deprecated name to ``domains/brand``, where they are not. An adopter got
    ``ImportError: cannot import name 'Brand' from 'adcp.types.domains.brand'``
    — an error naming a module they never wrote, which is worse than no alias
    at all.

    Stated over every public name of the discovery half, not a sample, and over
    the aggregator half too: a deprecated name has to serve everything both of
    its canonical halves bind.
    """
    old = _import_deprecated(deprecated)
    discovery_module = importlib.import_module(discovery)
    aggregator_module = importlib.import_module(aggregator)

    graded = 0
    for half in (discovery_module, aggregator_module):
        public = [name for name in dir(half) if not name.startswith("_")]
        assert public, f"{half.__name__} binds nothing public"
        for name in public:
            expected = getattr(half, name)
            if half is aggregator_module and hasattr(discovery_module, name):
                # A name both halves bind resolved to the discovery class
                # pre-9.0, because the pre-9.0 module was the discovery schema
                # and nothing else. That ordering is the fidelity claim.
                expected = getattr(discovery_module, name)
            assert getattr(old, name) is expected, f"{deprecated}.{name}"
            graded += 1
    assert graded > 250, f"only {graded} names graded — the sweep collapsed"


@pytest.mark.parametrize(("deprecated", "discovery", "aggregator"), SPLITS, ids=SPLIT_IDS)
def test_a_split_name_defines_nothing_and_serves_canonical_classes(
    deprecated: str, discovery: str, aggregator: str
) -> None:
    """The property the one-module-object rule was protecting, kept without it.

    Two canonical modules cannot be one object, so a split name gets its own.
    What must not follow is a second LOAD of either half: that is what makes two
    class objects per class and an ``isinstance`` fail for no visible reason.
    The shim executes nothing and binds no class — every class it hands back
    reports a canonical ``__module__``.
    """
    old = _import_deprecated(deprecated)

    assert isinstance(old, _SplitAliasModule)
    assert sys.modules[deprecated] is old
    assert old is not importlib.import_module(discovery)
    assert old is not importlib.import_module(aggregator)

    discovery_module = importlib.import_module(discovery)
    classes = [
        getattr(old, name)
        for name in dir(discovery_module)
        if not name.startswith("_") and isinstance(getattr(old, name), type)
    ]
    assert len(classes) > 150, f"only {len(classes)} classes reached — the sweep collapsed"
    # Every class the discovery half DEFINES reports that half, never the
    # deprecated name. The handful it merely imports (``AdCPBaseModel``,
    # ``Annotated``, the pydantic bases) report where they are defined, which is
    # the same answer: a second load under the deprecated name is what would
    # show up here, and it would show up on all of them.
    defined_here = [cls for cls in classes if cls.__module__ == discovery]
    assert len(defined_here) > 150, f"only {len(defined_here)} classes defined in {discovery}"
    for cls in classes:
        assert DEPRECATED_ROOT not in cls.__module__, cls


@pytest.mark.parametrize(("deprecated", "discovery", "aggregator"), SPLITS, ids=SPLIT_IDS)
def test_a_split_name_warns_about_both_halves_not_the_prefix_rename(
    deprecated: str, discovery: str, aggregator: str
) -> None:
    """The advice an adopter reads has to be the advice that works for them.

    "import adcp.types.domains.brand instead" is the prefix rename, and for this
    one name it sends the reader to a module that does not bind what they
    imported — the same wrong answer #1402 was about, delivered as guidance
    rather than as an ``ImportError``. Graded on a fresh finder, because the
    installed one has already warned for this name.
    """
    finder = _AliasFinder()

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert finder.find_spec(deprecated) is not None

    assert len(caught) == 1, [str(entry.message) for entry in caught]
    message = str(caught[0].message)
    assert discovery in message, message
    assert aggregator in message, message
    assert "split in two" in message, message
    assert "prefix rename" in message and "not a prefix rename" in message, message
    assert f"v{REMOVED_IN_MAJOR}" in message, message


@pytest.mark.parametrize(("deprecated", "discovery", "aggregator"), SPLITS, ids=SPLIT_IDS)
def test_a_split_deprecated_package_still_resolves_its_leaf_modules(
    deprecated: str, discovery: str, aggregator: str
) -> None:
    """``_find_and_load`` reads the parent's ``__path__`` before any finder runs.

    So a shim without one answers "is not a package" for every leaf under it —
    20 modules in ``brand``'s case, broken to serve 193 names. It borrows the
    aggregator package's own ``__path__``, and the finder ahead of
    ``PathFinder`` still serves each leaf as the canonical module object.
    """
    old = _import_deprecated(deprecated)
    aggregator_module = importlib.import_module(aggregator)

    assert old.__path__ is aggregator_module.__path__

    leaves = sorted(info.name for info in pkgutil.iter_modules(aggregator_module.__path__))
    assert len(leaves) > 5, leaves
    for leaf in leaves:
        through_alias = _import_deprecated(f"{deprecated}.{leaf}")
        assert through_alias is importlib.import_module(f"{aggregator}.{leaf}")


# ---------------------------------------------------------------------------
# Property 4 — the shared object carries no trace of the old name
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("deprecated", "canonical"), UNSPLIT_PAIRS, ids=UNSPLIT_PAIR_IDS)
def test_the_shared_module_carries_no_trace_of_the_deprecated_name(
    deprecated: str, canonical: str
) -> None:
    """``test_export_surface_is_derived`` reads these, so the alias must not move them.

    The import machinery writes exactly one of them when a loader hands back an
    existing module: ``_init_module_attrs`` always replaces ``__spec__``, and
    sets the rest only when absent. ``exec_module`` puts the canonical spec
    back; this is the assertion that says so.

    A split name is its own module and says so, which is the honest answer when
    there are two canonical halves — what
    ``test_export_surface_is_derived`` actually reads is each CLASS's
    ``__module__``, and the shim creates no class to stamp.
    """
    module = _import_deprecated(deprecated)

    assert module.__name__ == canonical
    assert module.__spec__ is not None
    assert module.__spec__.name == canonical
    # ``__loader__`` is the real source loader, never the alias's. If
    # ``_init_module_attrs`` ever started overriding it, a reload would re-run
    # the alias instead of the file.
    assert not isinstance(module.__loader__, _AliasLoader)
    assert module.__loader__ is module.__spec__.loader

    traces = {
        "__name__": module.__name__,
        "__package__": module.__package__ or "",
        "__file__": module.__file__ or "",
        "__spec__.name": module.__spec__.name,
        "__spec__.origin": module.__spec__.origin or "",
    }
    leaked = {key: value for key, value in traces.items() if DEPRECATED_ROOT in value}
    assert leaked == {}, leaked


def test_a_class_reached_through_the_old_path_reports_the_canonical_module() -> None:
    """``__module__`` is what grades #911, over 4000 classes.

    A second load under the deprecated name would stamp the deprecated path
    onto every class it created, and
    ``test_export_surface_is_derived::test_no_generated_type_is_reachable_under_zero_names``
    would fail. Here is the same invariant, asserted on a class reached the
    deprecated way.
    """
    old = _import_deprecated(f"{DEPRECATED_ROOT}.core.format_id")

    assert old.FormatReferenceStructuredObject.__module__ == f"{CANONICAL_ROOT}.core.format_id"


# ---------------------------------------------------------------------------
# Property 3 — a DeprecationWarning, once per module
# ---------------------------------------------------------------------------


def test_the_warning_fires_once_per_module_and_names_the_new_path() -> None:
    """Graded on a fresh finder, because the installed one has already warned.

    ``find_spec`` is called again for a name already in ``sys.modules``
    whenever something probes it — ``adcp.types.__getattr__`` does, for its
    submodule passthrough — so the once-per-module rule is the finder's own
    bookkeeping rather than a side effect of ``sys.modules``.
    """
    finder = _AliasFinder()
    name = f"{DEPRECATED_ROOT}.core.format_id"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert finder.find_spec(name) is not None
        assert finder.find_spec(name) is not None
        assert finder.find_spec(f"{DEPRECATED_ROOT}.core.product") is not None

    messages = [str(entry.message) for entry in caught]
    assert all(entry.category is DeprecationWarning for entry in caught)
    assert len(messages) == 2, messages
    assert sum(name in message for message in messages) == 1, messages

    first = messages[0]
    assert canonical_name(name) in first
    assert f"v{REMOVED_IN_MAJOR}" in first


def test_the_finder_declines_every_name_outside_the_deprecated_root() -> None:
    """A finder at the front of ``sys.meta_path`` must not answer for anything else."""
    finder = _AliasFinder()
    for name in (
        "adcp",
        "adcp.types",
        CANONICAL_ROOT,
        f"{CANONICAL_ROOT}.core",
        "adcp.types.generated_pocket",
        "json",
    ):
        assert finder.find_spec(name) is None, name


def test_a_name_that_exists_under_neither_root_is_reported_as_itself() -> None:
    """The error names what the caller asked for, not the rewritten target."""
    with pytest.raises(ModuleNotFoundError) as caught:
        importlib.import_module(f"{DEPRECATED_ROOT}.core.not_a_schema")
    assert f"{DEPRECATED_ROOT}.core.not_a_schema" in str(caught.value)
    assert CANONICAL_ROOT not in str(caught.value)


def test_installing_twice_leaves_one_finder_ahead_of_the_path_finder() -> None:
    """``adcp.types`` installs it; a second call must not stack a second copy."""
    install()
    install()
    ours = [index for index, f in enumerate(sys.meta_path) if isinstance(f, _AliasFinder)]
    assert len(ours) == 1, sys.meta_path

    path_finder = [
        index for index, f in enumerate(sys.meta_path) if getattr(f, "__name__", "") == "PathFinder"
    ]
    assert path_finder, sys.meta_path
    assert ours[0] < path_finder[0], (
        "PathFinder would find the real files on the canonical package's __path__ "
        "and load a SECOND copy of every module under the deprecated name"
    )


def test_a_real_import_in_a_clean_process_warns_and_keeps_identity() -> None:
    """The adopter-facing behaviour, measured where ``sys.modules`` is empty.

    In-process tests cannot show this: whichever test imports the deprecated
    path first consumes the warning for the whole session. Two subprocesses —
    one that turns the warning into an error, one that ignores it and checks
    identity — pin both halves.
    """
    deep = f"{DEPRECATED_ROOT}.core.format_id"

    refused = subprocess.run(
        [sys.executable, "-W", "error::DeprecationWarning", "-c", f"import {deep}"],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert refused.returncode != 0, refused.stdout
    assert "DeprecationWarning" in refused.stderr
    assert canonical_name(DEPRECATED_ROOT) in refused.stderr

    accepted = subprocess.run(
        [
            sys.executable,
            "-W",
            "ignore::DeprecationWarning",
            "-c",
            f"import {deep} as old, {canonical_name(deep)} as new; "
            "print(old is new, old.FormatReferenceStructuredObject "
            "is new.FormatReferenceStructuredObject, old.__name__)",
        ],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert accepted.returncode == 0, accepted.stderr
    assert accepted.stdout.strip() == f"True True {canonical_name(deep)}"


def test_reload_of_a_deprecated_name_re_runs_the_canonical_module() -> None:
    """``reload`` must not re-enter the alias — it reads the restored ``__spec__``.

    In its own process, because reloading a generated module rebuilds its
    classes and every other module in the tree keeps the old ones.
    """
    deep = f"{DEPRECATED_ROOT}.core.format_id"
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "ignore::DeprecationWarning",
            "-c",
            f"import importlib, {deep} as m; "
            "again = importlib.reload(m); "
            "print(again is m, again.__name__, type(again.__loader__).__name__)",
        ],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, result.stderr
    # ``reload`` returns the same object, re-executed from the canonical file by
    # the canonical loader.
    assert result.stdout.strip() == f"True {canonical_name(deep)} SourceFileLoader"


# ---------------------------------------------------------------------------
# Property 5 — the alias does not outlive its removal major
# ---------------------------------------------------------------------------


def _declared_major() -> int:
    """The major version ``pyproject.toml`` declares, which release-please bumps."""
    pyproject = (_REPO_ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version = "(\d+)\.', pyproject, re.MULTILINE)
    assert match, "pyproject.toml declares no [project] version"
    return int(match.group(1))


def _installed_major() -> int:
    """The major version of the built distribution, which may run ahead of the tree."""
    import adcp

    match = re.match(r"(\d+)\.", adcp.__version__)
    assert match, adcp.__version__
    return int(match.group(1))


def test_the_alias_does_not_outlive_its_removal_major() -> None:
    """A deprecation with no expiry is a permanent second surface.

    Read from both places a major can appear, because they diverge: a dev tree
    carries ``pyproject.toml``'s version while the venv's metadata still holds
    whatever was last installed. Either reaching v10 means this module, its
    ``install()`` call in ``adcp/types/__init__.py``, and this suite go.
    """
    reached = max(_declared_major(), _installed_major())
    assert reached < REMOVED_IN_MAJOR, (
        f"adcp is at v{reached} and {DEPRECATED_ROOT} was to be removed in "
        f"v{REMOVED_IN_MAJOR}. Delete src/adcp/types/_generated_poc_alias.py, its "
        f"install() call in src/adcp/types/__init__.py, and this test module."
    )


def test_the_removal_major_is_stated_where_an_adopter_reads_it() -> None:
    """The expiry is in the warning and in the migration guide, not only in code."""
    assert REMOVED_IN_MAJOR == 10
    guide = (_REPO_ROOT / "docs" / "types-9-migration.md").read_text()
    assert f"v{REMOVED_IN_MAJOR}" in guide
    assert DEPRECATED_ROOT in guide
