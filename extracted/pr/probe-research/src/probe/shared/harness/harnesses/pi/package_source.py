"""which packages entry is ours: package root, the source to install from, pi's own match-key identity."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path

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


class PackageRootError(Exception):
    """`resolve_package_root` could not find our package anywhere it looks.

    Never silently skipped: every caller that hits this must surface the
    message, which is written to name BOTH resolution options so a researcher
    (or a later task's error path) does not have to go read this file to know
    what to do next.
    """


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


def _our_entry_index(data: dict, *, root: Path | None, agent_dir: Path) -> int | None:
    for index, entry in enumerate(data.get("packages") or []):
        source = _entry_source(entry)
        if source is not None and _identifies_ours(source, package_root=root, agent_dir=agent_dir):
            return index
    return None


def _skill_prefix(source: str) -> str:
    """Where skills sit inside the package an entry names: the mirror's root
    package.json points into plugins/probe-research-pi/, a local checkout IS the
    package directory."""
    return "plugins/probe-research-pi/skills/" if _git_repo_identity(source) else "skills/"
