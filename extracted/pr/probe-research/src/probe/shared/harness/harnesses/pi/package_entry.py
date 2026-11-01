"""install, remove and read our entry in pi's packages array (global and project merged), the MCP adapter, the legacy symlink."""

from __future__ import annotations
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

# One of the two non-stdlib imports here (`durable` below is the other), and free:
# claude_cli.py is itself stdlib-only (shutil/subprocess/dataclasses, see its
# own docstring), so importing it adds no dependency weight and, critically,
# no import cycle -- it does not import agent_rules, pi_config, or anything
# else in this package back. It is imported for `Result`, and for the bounded
# way to run a binary (`claude_cli.capture`, `pi_binary_available`'s sniff).
# setup.py's install_plugin/uninstall_plugin already return claude_cli.Result,
# and a later task wires pi's install/remove into the SAME call sites
# (apply_capture, apply_tracking) that already know how to read `.ok` and
# `.detail` off one. Inventing a second, differently-shaped result type here
# would make that wiring a translation layer instead of a drop-in.
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness.harnesses.pi.package_source import (
    PACKAGE_NAME,
    PackageRootError,
    _declared_package_name,
    _entry_source,
    _identifies_ours,
    local_package_root,
    resolve_install_source,
)
from probe.shared.harness.harnesses.pi.profile import TRACKING_KEY, _entry_for
from probe.shared.harness.harnesses.pi.settings import (
    _SettingsRefusal,
    _load_settings,
    _write_settings,
    pi_agent_dir,
    project_settings_path,
    settings_path,
)

#: Where the pre-packages-array symlink install used to live. `migrate_legacy_symlink`
#: only ever touches this one path.
_LEGACY_EXTENSION_RELATIVE = ("extensions", PACKAGE_NAME)


@dataclass(frozen=True)
class MergedPackageEntry:
    """Our `packages` entry as pi would resolve it, global and project merged.

    `installed` is the consent signal: the user asked for this package
    somewhere. `extension_filtered_out` is the strand-ai condition -- pi loads
    the package's skills and MCP manifest but not `index.ts`, so capture
    never starts and nothing says so.
    """

    installed: bool
    scope: str | None
    extensions_filter: list[str] | None
    skills_filter: list[str] | None
    #: `probeTracking: false` on the winning entry: Probe's tracking (skills +
    #: MCP) is switched off while the extension keeps capturing. The extension
    #: enforces it from this same merged read (`src/trackingSetting.ts`).
    tracking_off: bool = False

    @property
    def extension_filtered_out(self) -> bool:
        """Whether pi would decline to load our extension entry point.

        pi's filter vocabulary (its own `docs/packages.md`, "Package
        Filtering"): omitting the key loads everything, `[]` loads nothing,
        `!pattern` excludes, `+path`/`-path` force-include and force-exclude
        an EXACT path relative to the package root. So a `+`-prefixed pin of
        our own entry point -- the shape a live customer machine carries,
        `"+plugins/probe-research-pi/index.ts"` against the mirror package --
        means the extension LOADS, and reading that as filtered out would make
        `probe doctor` cry wolf on a healthy install.

        Deliberately a question about the ENTRY POINT, not about the filter
        being non-empty: both our manifests (`agent/plugins/probe-research-pi/
        package.json` and `agent/mirror-package.json`) declare exactly one
        extension, and it is an `index.ts`.
        """
        if not self.installed or self.extensions_filter is None:
            return False
        return not any(
            pattern.strip().lstrip("+").endswith("index.ts")
            for pattern in self.extensions_filter
            if isinstance(pattern, str) and not pattern.strip().startswith(("!", "-"))
        )


def _our_entry_in(path: Path, *, package_root: Path | None, agent_dir: Path) -> dict | None:
    """Our entry in ONE settings file, normalised to the object form, or None.

    A bare-string entry comes back as `{"source": ...}` so callers can read
    filters off whatever they get without re-testing the shape. An unreadable
    or malformed file is None -- the same "cannot tell, so do not claim yes"
    `package_entry_installed` has always given, and the reason a broken
    project file degrades to the global answer instead of erasing it.
    """
    try:
        data = _load_settings(path)
    except _SettingsRefusal:
        return None
    for entry in data.get("packages") or []:
        source = _entry_source(entry)
        if source is not None and _identifies_ours(
            source, package_root=package_root, agent_dir=agent_dir
        ):
            return entry if isinstance(entry, dict) else {"source": source}
    return None


def merged_package_entry(
    env: Mapping[str, str] | None = None, *, cwd: Path | str | None = None
) -> MergedPackageEntry:
    """Resolve our entry the way pi does.

    pi's rule (`docs/packages.md`, "Scope and Deduplication"): a package may
    appear in both scopes, and the project entry wins UNLESS it carries
    `autoload: false`, in which case it applies as a delta over the global
    entry. Implementing only the first half would misreport every
    `autoload:false` project entry's filters.

    `cwd=None` reads the global file only -- see `package_entry_installed`.
    """
    active = env if env is not None else os.environ
    try:
        root = local_package_root(active)
    except PackageRootError:
        # A broken explicit `PROBE_PI_PACKAGE_ROOT`. Loud for install/remove,
        # which can act on it; this read has no repair to offer, so it keeps
        # this module's "cannot tell, so do not claim yes" contract rather
        # than answering off a half-resolved identity.
        return MergedPackageEntry(False, None, None, None)
    agent_dir = pi_agent_dir(active)

    global_entry = _our_entry_in(settings_path(active), package_root=root, agent_dir=agent_dir)
    project_entry = (
        _our_entry_in(project_settings_path(cwd), package_root=root, agent_dir=agent_dir)
        if cwd is not None
        else None
    )

    if project_entry is None and global_entry is None:
        return MergedPackageEntry(False, None, None, None)

    if project_entry is None:
        winner, scope = global_entry, "global"
    elif project_entry.get("autoload") is False and global_entry is not None:
        winner, scope = {**global_entry, **project_entry}, "project"
    else:
        winner, scope = project_entry, "project"

    def _filter(key: str) -> list[str] | None:
        value = winner.get(key)
        return value if isinstance(value, list) else None

    return MergedPackageEntry(
        True, scope, _filter("extensions"), _filter("skills"), winner.get(TRACKING_KEY) is False
    )


#: The pi extension that, when installed, serves every package's `pi.mcp`
#: manifest itself, ours included (our extension then stands down, D6).
MCP_ADAPTER_NAME = "pi-mcp-adapter"


def mcp_adapter_installed(env: Mapping[str, str] | None = None, *, cwd: Path | str | None = None) -> bool:
    """Whether pi-mcp-adapter is in pi's packages, global or project scope.

    The same identity test as the extension's `adapterHandoff.matchesAdapter`
    (npm name, git basename, a local directory's package.json name), so the
    status names the provider pi actually uses. Unreadable files read as
    absent."""
    active = env if env is not None else os.environ
    scopes = [(settings_path(active), pi_agent_dir(active))]
    if cwd is not None:
        scopes.append((project_settings_path(cwd), Path(cwd) / ".pi"))
    for path, base in scopes:
        try:
            data = _load_settings(path)
        except _SettingsRefusal:
            continue
        for entry in data.get("packages") or []:
            source = (_entry_source(entry) or "").strip()
            if not source:
                continue
            if source.startswith("npm:"):
                name = source[4:].strip()
                name = name.rsplit("@", 1)[0] if name.count("@") > (1 if name.startswith("@") else 0) else name
                if name == MCP_ADAPTER_NAME:
                    return True
            elif source.startswith(("git:", "github:", "http:", "https:", "ssh:")):
                tail = source.split("#", 1)[0].split("?", 1)[0].rstrip("/")
                last = tail.replace(":", "/").rsplit("/", 1)[-1]
                if last.removesuffix(".git") == MCP_ADAPTER_NAME:
                    return True
            elif _declared_package_name((Path(source) if Path(source).is_absolute() else base / source)) == MCP_ADAPTER_NAME:
                return True
    return False


def install_package_entry(
    package_root: Path | None = None,
    *,
    env: Mapping[str, str] | None = None,
    tracking: bool = True,
) -> claude_cli.Result:
    """Append our package to `settings.json`'s `packages` array. Idempotent.

    D3, exactly: missing file becomes `{}` (parent dirs created on write);
    unparseable JSON, a non-object root, or a non-list `packages` REFUSE
    without writing anything; an existing entry that already identifies us
    (local-path, npm, or mirror form) is a no-op success, never a duplicate;
    otherwise the install source is appended as a plain string, every other
    key and key order preserved.

    `tracking=False` appends the tracking-off form instead (`_entry_for`):
    capture installed on its own must not bring Probe's skills and MCP along.
    It shapes a FRESH entry only; an existing entry's tracking is
    `set_tracking`'s to change.

    The appended source is an explicit `package_root` if the caller passed
    one, else whatever `resolve_install_source` picks -- a local checkout for
    a plugin developer, the published mirror repo for everybody else. This no
    longer fails when there is no checkout: that case is the normal install.
    """
    active = env if env is not None else os.environ
    if package_root is not None:
        root: Path | None = package_root.resolve()
        source_to_add = str(root)
    else:
        try:
            source_to_add = resolve_install_source(active)
            root = local_package_root(active)
        except PackageRootError as exc:
            # Only reachable via a BROKEN explicit `PROBE_PI_PACKAGE_ROOT` --
            # the no-checkout case now resolves to the mirror. Still a
            # `reachable=False` refusal rather than a raise: the wizard's step
            # runner reads Results, and an exception here would crash the run
            # instead of failing one step.
            return claude_cli.Result(ok=False, detail=str(exc), reachable=False)

    agent_dir = pi_agent_dir(active)
    path = settings_path(active)
    try:
        data = _load_settings(path)
    except _SettingsRefusal as exc:
        return claude_cli.Result(ok=False, detail=str(exc))

    packages = list(data.get("packages") or [])
    for entry in packages:
        source = _entry_source(entry)
        if source is not None and _identifies_ours(source, package_root=root, agent_dir=agent_dir):
            return claude_cli.Result(
                ok=True, detail=f"probe-research-pi is already installed in {path} (no-op)"
            )

    packages.append(
        source_to_add if tracking else _entry_for(source_to_add, source_to_add, tracking=False, daemon=False)
    )
    data["packages"] = packages
    try:
        _write_settings(path, data)
    except _SettingsRefusal as exc:
        return claude_cli.Result(ok=False, detail=str(exc))
    return claude_cli.Result(ok=True, detail=f"added probe-research-pi ({source_to_add}) to {path}")


def remove_package_entry(
    package_root: Path | None = None, *, env: Mapping[str, str] | None = None
) -> claude_cli.Result:
    """Remove ONLY the entries that identify our package. Idempotent.

    Leaves `packages: []` behind rather than deleting the key -- pi treats
    absent and empty identically (`?? []`), so this never needs to reconstruct
    "was there a packages key before us" and can just always leave one. Same
    refuse rules as install; missing file or missing entry is a no-op success.

    A missing checkout is NOT a failure here either: a mirror-installed entry
    must be removable on a machine that has no research-os clone, which is
    every machine the mirror install targets. `_identifies_ours` matches the
    mirror source without a local root, so removal still finds it.
    """
    active = env if env is not None else os.environ
    try:
        root = package_root.resolve() if package_root is not None else local_package_root(active)
    except PackageRootError as exc:
        return claude_cli.Result(ok=False, detail=str(exc), reachable=False)

    agent_dir = pi_agent_dir(active)
    path = settings_path(active)
    if not path.exists():
        return claude_cli.Result(ok=True, detail=f"{path} does not exist; nothing to remove")

    try:
        data = _load_settings(path)
    except _SettingsRefusal as exc:
        return claude_cli.Result(ok=False, detail=str(exc))

    packages = data.get("packages")
    if not packages:
        return claude_cli.Result(
            ok=True, detail=f"no probe-research-pi entry in {path}; nothing to remove"
        )

    kept = [
        entry
        for entry in packages
        if not (
            (source := _entry_source(entry)) is not None
            and _identifies_ours(source, package_root=root, agent_dir=agent_dir)
        )
    ]
    if len(kept) == len(packages):
        return claude_cli.Result(
            ok=True, detail=f"no probe-research-pi entry in {path}; nothing to remove"
        )

    data["packages"] = kept
    try:
        _write_settings(path, data)
    except _SettingsRefusal as exc:
        return claude_cli.Result(ok=False, detail=str(exc))
    return claude_cli.Result(ok=True, detail=f"removed probe-research-pi from {path}")


def package_entry_installed(
    env: Mapping[str, str] | None = None, *, cwd: Path | str | None = None
) -> bool:
    """Whether our `packages` entry is present in settings.json, right now.

    The read-only sibling of `install_package_entry`'s own idempotency check
    -- same identity matching (`_identifies_ours`/`_entry_source`), same
    `_load_settings`, but no writing and no `_SettingsRefusal` reaching the
    caller. `capabilities.installed_plugins()` (plan D7) is the intended
    caller: a status read has no repair to offer the way install/remove do,
    so unlike them, EVERYTHING this cannot cleanly determine -- an unreadable
    or malformed settings.json, a non-list `packages` key -- collapses to
    `False` rather than raising.

    A missing checkout is no longer one of those cases. It used to be: this
    returned False whenever `resolve_package_root` raised, so a
    mirror-installed customer -- who by definition has no research-os clone --
    was reported as NOT having the pi plugin, on a machine where it was
    installed and loading. The local root is now optional (see
    `local_package_root`) and only gates the local-path comparison. That is indistinguishable here from "genuinely not
    installed", which is the same "cannot tell, so do not claim yes" a
    doctor-style check gives any other absent signal (see
    `capabilities.PluginState`'s own docstring on that exact distinction).

    `cwd` opts into the project-scope read (`<cwd>/.pi/settings.json`). It
    defaults to None so every existing caller keeps the global-only answer it
    was written against; `ensure_capture` passes the session's cwd because a
    project-scope install is consent just as much as a global one.
    """
    return merged_package_entry(env, cwd=cwd).installed


def migrate_legacy_symlink(
    package_root: Path, *, env: Mapping[str, str] | None = None
) -> claude_cli.Result:
    """Retire the pre-packages-array install (plan D4).

    Before the `packages` entry existed, the documented install was a manual
    symlink at `<agent-dir>/extensions/probe-research-pi` pointing into a
    checkout. Once the packages entry is in place that symlink is redundant --
    pi would load the package twice, once from each -- so this deletes it, but
    ONLY when deleting is unambiguously safe:

    * a symlink whose resolved target sits inside `package_root` -- ours,
      pre-migration, remove it;
    * a symlink pointing anywhere else -- some OTHER thing is installed there
      under our package's name; leave it and say why, never guess;
    * a real directory (not a symlink at all) -- same reasoning, leave it;
    * nothing there -- nothing to migrate.

    Called by install in a later task; implemented and tested standalone here
    per the plan, since a caller needs `package_root` already in hand (this
    function does not resolve it itself -- the caller has typically just done
    so for `install_package_entry`, and re-resolving here could silently
    disagree with the value install actually used).
    """
    active = env if env is not None else os.environ
    link = pi_agent_dir(active).joinpath(*_LEGACY_EXTENSION_RELATIVE)
    root = package_root.resolve()

    # is_symlink() first, deliberately: exists() follows the link and reports
    # False for a broken symlink, which would misroute a broken-but-ours link
    # into the "nothing there" case instead of removing it.
    if link.is_symlink():
        target = link.resolve()
        if target == root or root in target.parents:
            try:
                link.unlink()
            except OSError as exc:
                return claude_cli.Result(
                    ok=False, detail=f"could not remove legacy symlink {link}: {exc}"
                )
            return claude_cli.Result(
                ok=True,
                detail=f"removed legacy symlink {link} (pointed inside the package root; "
                "the packages entry now serves it)",
            )
        return claude_cli.Result(
            ok=True,
            detail=f"left {link} alone: it is a symlink but resolves to {target}, "
            f"outside the package root {root}",
        )

    if link.exists():
        return claude_cli.Result(
            ok=True,
            detail=f"left {link} alone: it is a real directory, not the legacy symlink install",
        )

    return claude_cli.Result(ok=True, detail=f"no legacy symlink at {link}; nothing to migrate")
