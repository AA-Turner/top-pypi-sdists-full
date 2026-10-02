"""The pi settings.json `packages` array entry this CLI owns.

pi (the coding-agent harness) has no plugin marketplace the way Claude Code
and Codex do -- the only install surface is a `packages` array in
`<agent-dir>/settings.json`, read at startup by pi itself AND, independently,
by pi-mcp-adapter (if present) to discover any package's `pi.mcp` manifest.
One settings entry therefore does the whole job: it is how pi loads our
extension and skills, and it is the ONLY thing that makes our MCP server
auto-discoverable to the adapter. There is no separate "install" step for
either half.

pi's own identity semantics, read directly out of the installed pi 0.84.3
dist (`dist/core/package-manager.js`, see the plan's Verified fact 1;
byte-identical in 0.86.0):
entries may be a bare string or `{"source": "..."}`; a `npm:<name>` source
identifies by NAME, everything else (`git:<url>`, or a plain path -- absolute,
or relative to the agent dir) is `type: "local"` and identifies by RESOLVED
ABSOLUTE PATH. Idempotency and removal here mirror that exactly: never a raw
string compare, because a relative entry and an absolute entry pointing at the
same checkout are the same package as far as pi is concerned, and treating
them as different would let a wizard re-run append a duplicate pi would
happily also load.

Kept STDLIB-ONLY (with one deliberate exception -- see the `claude_cli` import
below) so `agent_rules.py` can import `pi_agent_dir()` from here without
pulling that module's whole dependency graph along, and so this module can be
imported early without caring what else is wired up yet.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

# The only non-stdlib import in this module, and it does not cost anything:
# claude_cli.py is itself stdlib-only (shutil/subprocess/dataclasses, see its
# own docstring), so importing it adds no dependency weight and, critically,
# no import cycle -- it does not import agent_rules, pi_config, or anything
# else in this package back. It is imported for exactly one thing: `Result`.
# setup.py's install_plugin/uninstall_plugin already return claude_cli.Result,
# and a later task wires pi's install/remove into the SAME call sites
# (apply_capture, apply_tracking) that already know how to read `.ok` and
# `.detail` off one. Inventing a second, differently-shaped result type here
# would make that wiring a translation layer instead of a drop-in.
from probe.cli import claude_cli

#: The npm name our package.json declares, and the identity a
#: `npm:probe-research-pi` entry is matched against. Not yet installable this
#: way -- see `resolve_package_root`'s docstring -- but an entry in this form
#: can already exist (a researcher who published a fork, or ran this after we
#: publish) and must be recognised, not duplicated.
PACKAGE_NAME = "probe-research-pi"
OUR_NPM_SOURCE = f"npm:{PACKAGE_NAME}"

#: The env var naming an explicit package root, for dev/CI and for any install
#: shape where the checkout-walk in `resolve_package_root` cannot apply (e.g.
#: this CLI running from an installed wheel, outside any research-os checkout).
PACKAGE_ROOT_ENV = "PROBE_PI_PACKAGE_ROOT"

#: Relative to a candidate checkout root. Matched literally against
#: `package.json` presence -- see `resolve_package_root`.
_PACKAGE_RELATIVE_PATH = ("agent", "plugins", "probe-research-pi")

#: Where the pre-packages-array symlink install used to live. `migrate_legacy_symlink`
#: only ever touches this one path.
_LEGACY_EXTENSION_RELATIVE = ("extensions", PACKAGE_NAME)

#: The PUBLIC mirror repo, and the source string we write when no local
#: checkout resolves -- i.e. every real install. `mirror_render.py` renders
#: `plugins/probe-research-pi` plus a root `package.json` whose `pi` manifest
#: points into it, so a `git clone` of this repo IS a loadable pi package:
#: pi clones the repo, sees the root `package.json`, and runs its dependency
#: install there (`installGit` -> `runNpmCommand(getGitDependencyInstallArgs())`).
#:
#: This is the SAME channel Claude and Codex already install from (their
#: marketplace manifests are rendered into this repo by the same script), which
#: is why the pi package is deliberately NOT published to npm: one release
#: mechanism -- the mirror push -- covers all three clients, and an unpinned
#: source tracks the mirror's `main` exactly as those two already do.
MIRROR_REPO = "prbe-ai/research-os-agent"

#: `git:`-prefixed, NOT `github:`. pi's `isLocalPath()` lists `github:` as a
#: non-local prefix, which reads like support -- but `parseGitUrl()` accepts a
#: source only when it is `git:`-prefixed OR a full `https|http|ssh|git://`
#: URL, so `github:owner/repo` parses as NEITHER and falls through to
#: `{type: "local"}`. pi then looks for a DIRECTORY of that literal name:
#:
#:     $ pi install github:prbe-ai/research-os-agent
#:     Error: Path does not exist: <cwd>/github:prbe-ai/research-os-agent
#:
#: Verified against pi 0.84.3: `git:github.com/...` and
#: `https://github.com/...` both install; `github:...` does not. 0.86.0's
#: parsers (`dist/core/package-manager.js`, `dist/utils/{paths,git}.js`) are
#: byte-identical.
MIRROR_GIT_SOURCE = f"git:github.com/{MIRROR_REPO}"

#: `(host, owner/repo)`, lowercased, as `_git_repo_identity` yields it.
_MIRROR_IDENTITY = ("github.com", MIRROR_REPO.lower())


@lru_cache(maxsize=1)
def pi_binary_available() -> bool:
    """Whether the `pi` binary is on PATH and is really pi.

    ONCE PER PROCESS. The sniff below spawns `pi --help` with a 3s cap, and
    `backfill.which_agent(Agent.PI)` is its caller; the retired per-transcript
    digest lane asked once per transcript -- hundreds in a run -- which is
    when an uncached answer became minutes of subprocess spawning to re-derive
    a fact that cannot change mid-run. This is
    the same trade `backfill._supported_flags_cached` and `_agent_version_cached`
    already make for claude/codex, and the same reason. It is deliberately NOT
    what `plugin_cli.available` does for those two: that is a bare
    `shutil.which` costing nothing, so it has nothing to cache.

    The cost is that a pi installed DURING a wizard session is not noticed until
    the next one. `pi_binary_available.cache_clear()` is the escape hatch, and
    the tests that exercise the real sniff use it.

    HERE rather than in `setup.py`, where it was written, because two callers
    now need it and neither can reach the other: `backfill.which_agent` needs
    the sniff to tell a real pi from a two-letter impostor, and setup.py is a
    wizard module that reaches INTO backfill. `pi_config` imports neither, so
    it is the one place both can import from without a cycle.
    `setup.pi_binary_available` re-exports it, so the wizard and its tests are
    unaffected.

    The ONE `shutil.which` call for pi, kept as its own function rather than
    inlined in `detectable_sources` for two reasons: it is the single seam a
    caller (or a test) mocks to control pi detection without also touching
    `plugin_cli.available`'s claude/codex behaviour -- and it is NOT routed
    through `plugin_cli.available`/`binary_name` on purpose, because
    `plugin_cli.binary_name` RAISES for pi (see that module's docstring: pi has
    no marketplace CLI to route through). pi's binary is real even though its
    marketplace is not, and this is where that distinction is drawn.

    `which` alone is not enough here, unlike for `claude`/`codex`: "pi" is
    two letters, and an unrelated binary of that name on someone's PATH
    would put a phantom pi checkbox in every wizard run. So a hit is
    confirmed by running `pi --help` (3s cap) and looking for "coding" in
    the output -- pi 0.84.3's (and 0.86.0's) first help line is "pi - AI coding assistant
    with read, bash, edit, write tools", and the loose match is deliberate
    so forks that reword it still detect. The failure direction matters: a
    false NEGATIVE only hides the auto-detected row, and `--agent pi` still
    works; a false POSITIVE offers an install the machine cannot use.
    """
    path = shutil.which("pi")
    if path is None:
        return False
    try:
        completed = subprocess.run(  # noqa: S603 - resolved binary, no shell
            [path, "--help"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return completed.returncode == 0 and "coding" in completed.stdout.lower()


class PackageRootError(Exception):
    """`resolve_package_root` could not find our package anywhere it looks.

    Never silently skipped: every caller that hits this must surface the
    message, which is written to name BOTH resolution options so a researcher
    (or a later task's error path) does not have to go read this file to know
    what to do next.
    """


class _SettingsRefusal(Exception):
    """Internal only. `install_package_entry`/`remove_package_entry` catch this
    and turn it into a `claude_cli.Result(ok=False, ...)` -- callers of THIS
    module never see it, because the whole point of the settings-edit contract
    (plan D3) is "return a refusal", never "raise into the wizard".
    """


def pi_agent_dir(env: Mapping[str, str] | None = None) -> Path:
    """pi's own global agent directory: `PI_CODING_AGENT_DIR`, else `~/.pi/agent`.

    Moved here from `agent_rules.memory_path`'s pi branch (this logic must not
    exist in a third place -- `agent/plugins/probe-research-pi/src/paths.ts`'s
    `piAgentDir` is the second). `PI_CODING_AGENT_DIR` is not a guess: pi
    0.86.0's own `dist/config.js` (as 0.84.3's) derives it as
    `${APP_NAME.toUpperCase()}_CODING_AGENT_DIR` and `getAgentDir()` -- read by
    every pi entry point -- returns it verbatim when set. Unlike Codex's
    `CODEX_HOME` (a parent directory Codex appends `AGENTS.md` onto), this
    names the agent directory itself, so nothing is appended before it here
    either.
    """
    active = env if env is not None else os.environ
    configured = active.get("PI_CODING_AGENT_DIR")
    return Path(configured).expanduser() if configured else Path.home() / ".pi" / "agent"


def settings_path(env: Mapping[str, str] | None = None) -> Path:
    """`<agent-dir>/settings.json` -- the file pi and pi-mcp-adapter both read."""
    return pi_agent_dir(env) / "settings.json"


def project_settings_path(cwd: Path | str) -> Path:
    """`<cwd>/.pi/settings.json` -- pi's project-scope settings.

    Not an ancestor walk: pi reads the project file at the directory it was
    started in, and inventing a walk here would claim an install pi itself
    would not load.
    """
    return Path(cwd) / ".pi" / "settings.json"


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

    return MergedPackageEntry(True, scope, _filter("extensions"), _filter("skills"))


def resolve_package_root(env: Mapping[str, str] | None = None) -> Path:
    """Where the `probe-research-pi` package directory actually lives, right now.

    Resolution order (plan D2, "dev era" -- pre-publish):

    1. `PROBE_PI_PACKAGE_ROOT` env, explicit and always wins. Must contain a
       `package.json`, or this is a loud failure rather than a silent
       fall-through to option 2 -- a researcher who set it made a specific
       claim, and finding NOTHING there is more likely a typo than "I meant
       the checkout instead."
    2. Walk up from this module's own file looking for
       `agent/plugins/probe-research-pi/package.json` beneath each ancestor --
       true only when this CLI is running from a research-os checkout, the
       same sibling-checkout philosophy `tapRuntime.ts` rule 2 uses for the tap
       daemon. A bounded walk (not a fixed parent-count offset) so this keeps
       working if the CLI's own depth inside the checkout ever changes.

    If neither resolves -- most likely this CLI installed as a standalone
    wheel outside any checkout -- raise `PackageRootError` naming both options.
    Never a silent skip: a caller that swallowed this would report a
    successful pi install that loaded nothing.

    The `npm:probe-research-pi` source (post-publish) is NOT produced here --
    today it can only be an already-present entry we *recognise* (see
    `_identifies_ours`), never one we *write*, because nothing has been
    published yet. Flipping that on is documented as a one-line change in the
    plan; this function is where it lands.
    """
    active = env if env is not None else os.environ
    override = active.get(PACKAGE_ROOT_ENV)
    if override:
        candidate = Path(override).expanduser().resolve()
        if (candidate / "package.json").is_file():
            return candidate
        raise PackageRootError(
            f"{PACKAGE_ROOT_ENV}={candidate} has no package.json in it -- point it at "
            "the probe-research-pi package directory, or unset it and run from a "
            "research-os checkout containing agent/plugins/probe-research-pi/package.json"
        )

    here = Path(__file__).resolve()
    for ancestor in here.parents:
        candidate = ancestor.joinpath(*_PACKAGE_RELATIVE_PATH)
        if (candidate / "package.json").is_file():
            return candidate.resolve()

    raise PackageRootError(
        "could not find the probe-research-pi package: set "
        f"{PACKAGE_ROOT_ENV} to its directory, or run probe from a research-os "
        "checkout containing agent/plugins/probe-research-pi/package.json"
    )


def local_package_root(env: Mapping[str, str] | None = None) -> Path | None:
    """`resolve_package_root`, but "not found" is None instead of a raise.

    Every caller that merely needs to RECOGNISE a local-path entry (install's
    dedupe scan, remove's filter, `package_entry_installed`) wants this shape:
    with the mirror source now the normal install, a missing checkout is the
    ordinary case, not a failure, and those callers must keep working without
    one. `resolve_package_root` keeps raising for the callers that genuinely
    need a directory on disk (`migrate_legacy_symlink`).

    A BROKEN `PROBE_PI_PACKAGE_ROOT` still raises. Swallowing that would make
    the mirror fallback silently override an explicit claim -- someone who set
    the var to a typo'd path would get the published package installed and
    never learn their override did nothing.
    """
    active = env if env is not None else os.environ
    if active.get(PACKAGE_ROOT_ENV):
        return resolve_package_root(active)
    try:
        return resolve_package_root(active)
    except PackageRootError:
        return None


def resolve_install_source(env: Mapping[str, str] | None = None) -> str:
    """The exact string to write into pi's `packages` array. NEVER raises.

    Resolution order, and note that only the first two are "dev era":

    1. `PROBE_PI_PACKAGE_ROOT` / a research-os checkout -- whichever
       `resolve_package_root` finds. A developer working on the plugin gets
       their own tree, not the published mirror.
    2. Otherwise `MIRROR_GIT_SOURCE` -- the published mirror repo. This is what
       a customer gets: pi clones it and loads the package from its root.

    The old behaviour was to RAISE here (`PackageRootError`) whenever no
    checkout resolved, which is every install that is not a developer's own
    machine -- so `probe setup` reported "could not install probe-research-pi"
    to every user who had no research-os clone, which was all of them. That
    was never a machine misconfiguration: the plugin simply had no
    distribution channel, and this function is where it gained one.
    """
    root = local_package_root(env)
    return str(root) if root is not None else MIRROR_GIT_SOURCE


def _git_repo_identity(source: str) -> tuple[str, str] | None:
    """`(host, "owner/repo")` lowercased for a git-ish source, else None.

    A deliberately small subset of pi's own `parseGitUrl`: we only ever need
    to answer "is this entry OUR mirror repo?", never to resolve an arbitrary
    git source the way pi does. Covers the forms pi accepts and a person might
    hand-write -- `github:owner/repo`, `git:`-prefixed anything, https/http/
    ssh/git URLs, and scp-like `git@host:owner/repo` -- with an optional
    `#ref` or `@ref` committish stripped, since a pinned entry is still ours.
    Anything that is not clearly a git source (a bare local path, an `npm:`
    spec) yields None and falls through to the caller's path comparison.
    """
    text = source.strip()
    had_git_prefix = text.startswith("git:")
    if had_git_prefix:
        text = text[len("git:") :].strip()
    text = text.split("#", 1)[0]

    if text.startswith("github:"):
        host, path = "github.com", text[len("github:") :]
    elif text.startswith("git@"):
        rest = text[len("git@") :]
        if ":" not in rest:
            return None
        host, path = rest.split(":", 1)
    else:
        for scheme in ("https://", "http://", "ssh://", "git://"):
            if text.startswith(scheme):
                rest = text[len(scheme) :]
                if "/" not in rest:
                    return None
                host, path = rest.split("/", 1)
                if "@" in host:  # ssh://git@github.com/owner/repo
                    host = host.split("@", 1)[1]
                break
        else:
            if not had_git_prefix:
                # Mirrors pi: WITHOUT a `git:` prefix only explicit protocol
                # URLs are git sources -- everything else is a local path, and
                # must fall through to the caller's path comparison.
                return None
            # `git:github.com/owner/repo` -- the bare host/path shorthand pi
            # accepts only behind that prefix (`parseGenericGitUrl`). The dot
            # test is pi's own guard against reading a relative path's first
            # segment as a hostname.
            if "/" not in text:
                return None
            host, path = text.split("/", 1)
            if "." not in host and host != "localhost":
                return None

    path = path.strip("/").split("@", 1)[0]
    if path.endswith(".git"):
        path = path[: -len(".git")]
    parts = [part for part in path.split("/") if part]
    if not host or len(parts) != 2:
        return None
    return host.lower(), "/".join(parts).lower()


def _entry_source(entry: object) -> str | None:
    """The `source` string an entry identifies by, or None for a shape we
    cannot read (bare non-string, or an object with no usable `source`).

    Not our concern to fix or refuse over -- an entry we cannot read is not
    ours, and it is preserved untouched either way (see `_rewrite_packages`).
    """
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        source = entry.get("source")
        if isinstance(source, str):
            return source
    return None


def _identifies_ours(source: str, *, package_root: Path | None, agent_dir: Path) -> bool:
    """pi's own match-key semantics (plan D1): npm sources match by NAME, git
    sources match by REPO, everything else is a local path matched by RESOLVED
    absolute path.

    A relative local source resolves against the AGENT DIR, not this
    process's cwd and not the package root -- that is where pi itself (and
    pi-mcp-adapter's `package-mcp-loader.ts`, verified fact 3) resolves
    relative `packages` entries from, for the same user-scope settings.json.
    Resolving anywhere else would make an entry pi considers "ours" invisible
    to us, or vice versa.

    `package_root` is None when no checkout resolves -- the normal customer
    case. That disables only the local-path comparison; the npm and mirror
    identities still match, so a mirror-installed user is still recognised as
    installed (and can still be cleanly removed) with no research-os clone
    anywhere on the machine.
    """
    if source == OUR_NPM_SOURCE:
        return True

    identity = _git_repo_identity(source)
    if identity is not None:
        # Our mirror repo in any spelling, pinned or not, is ours. Any OTHER
        # git repo is not -- and is never touched, however it is written.
        return identity == _MIRROR_IDENTITY

    if source.startswith("npm:"):
        # A different npm package -- never how WE install, so never ours.
        return False

    candidate = Path(source)
    if not candidate.is_absolute():
        candidate = agent_dir / candidate
    try:
        resolved = candidate.resolve()
    except OSError:
        # A path that cannot be resolved (e.g. permission denied walking it)
        # is not something we can prove is ours -- treat as foreign rather
        # than raising out of what is meant to be a pure comparison.
        return False
    if package_root is not None and resolved == package_root:
        return True
    # No local root to compare against, or a DIFFERENT one: fall back to the
    # package's own declared name, exactly as the TypeScript side already does
    # (`adapterHandoff.ts`'s `readPackageJsonName`).
    #
    # This is what makes the dev-era install removable. Someone who installed
    # from a checkout has an absolute path in `packages`; their CLI is a wheel,
    # so `local_package_root()` is None and a path comparison has nothing to
    # compare to. Without this, `probe`'s uninstall silently leaves that entry
    # behind and the next install appends the mirror source beside it -- two
    # entries, and pi loads the extension twice.
    return _declared_package_name(resolved) == PACKAGE_NAME


def _declared_package_name(directory: Path) -> str | None:
    """The `name` in `<directory>/package.json`, or None for anything unreadable.

    Never raises: this feeds a pure identity comparison, and a directory we
    cannot read is simply not provably ours. Mirrors the TypeScript side's
    `readPackageJsonName` so both halves answer "is this our package" the same
    way -- a local clone of the mirror repo also declares `probe-research-pi`
    at its root (see `agent/mirror-package.json`), so one check covers the
    checkout install and the hand-cloned mirror alike.
    """
    try:
        data = json.loads((directory / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    name = data.get("name")
    return name if isinstance(name, str) else None


def _load_settings(path: Path) -> dict:
    """Read `settings.json` under the D3 contract, or raise `_SettingsRefusal`.

    Missing file is NOT a refusal -- it is the documented "treat as {}" case,
    because a fresh pi install (fact 8: this machine's real settings.json has
    no `packages` key at all yet) is the common case, not an error.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as exc:
        raise _SettingsRefusal(f"could not read {path}: {exc}") from exc

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise _SettingsRefusal(f"{path} is not valid JSON, refusing to edit it ({exc})") from exc
    if not isinstance(data, dict):
        raise _SettingsRefusal(
            f"{path}'s root is a {type(data).__name__}, not a JSON object -- refusing to edit it"
        )
    packages = data.get("packages")
    if packages is not None and not isinstance(packages, list):
        raise _SettingsRefusal(f'{path}\'s "packages" key is not a list -- refusing to edit it')
    return data


def _write_settings(path: Path, data: dict) -> None:
    """Atomic write: tmp file in the SAME directory, then `os.replace`.

    Same-directory is load-bearing, not decoration -- `os.replace` is only
    atomic within one filesystem, and a tmp file in `/tmp` replacing a target
    under `~/.pi` can cross a mount boundary silently on some setups.
    2-space indent + trailing newline matches how pi itself writes this file,
    so a subsequent pi-side write does not show a whole-file diff.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2) + "\n"
    tmp = path.with_name(path.name + ".probe.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except OSError as exc:
        tmp.unlink(missing_ok=True)
        raise _SettingsRefusal(f"could not write {path}: {exc}") from exc


def install_package_entry(
    package_root: Path | None = None, *, env: Mapping[str, str] | None = None
) -> claude_cli.Result:
    """Append our package to `settings.json`'s `packages` array. Idempotent.

    D3, exactly: missing file becomes `{}` (parent dirs created on write);
    unparseable JSON, a non-object root, or a non-list `packages` REFUSE
    without writing anything; an existing entry that already identifies us
    (local-path, npm, or mirror form) is a no-op success, never a duplicate;
    otherwise the install source is appended as a plain string, every other
    key and key order preserved.

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

    packages.append(source_to_add)
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
