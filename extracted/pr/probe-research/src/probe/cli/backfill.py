"""`probe wizard` -> Import existing work: point one agent at one folder.

The wizard cannot read a research folder. Forty files -- a report, a config,
three CSVs, a training script -- are an experiment to a person and an
undifferentiated pile to `find`, and the mapping from file to experiment is
exactly the judgment nobody wrote down at the time. So the wizard does the two
things a program is better at and hands the middle to an agent:

* ENUMERATE (here, deterministic): walk the folder, count files and bytes.
  That count is the DENOMINATOR, and it is trustworthy precisely because no
  model produced it. Silent 2% coverage that reads as "done" is the failure
  mode this whole module exists to make impossible.
* DECIDE (the agent): what these files are, which deserve a description,
  whether they amount to an experiment. If the folder is large the agent
  subdivides it ITSELF -- it can see the shape, and a histogram cannot.
* RECONCILE (here, deterministic): what landed, against what was counted.

The agent is launched with a FIXED anchor. It may decide what a folder means;
it may not decide what the folder is called. A second run inventing a second
project slug is the one mistake in this flow nobody can undo, so the slug is
resolved by code before the agent starts and passed in as a given.

stdlib plus a lazy questionary/client import, like the rest of cli/ -- `probe
log` runs inside training loops and must not pay for any of this.
"""

from __future__ import annotations

import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from functools import lru_cache
from probe._compat import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .telemetry import TelemetryContext

from ..sdk.errors import NotFoundError

# For `which_agent`'s pi branch only. Module-level and cheap: `pi_config` is
# stdlib plus `claude_cli` (itself stdlib), so this costs the lazy-import
# discipline in the docstring above nothing.
from . import pi_config


_BACKFILL_CLI_LOCK = threading.Lock()
_BACKFILL_CLI_BIN: tempfile.TemporaryDirectory | None = None


def _backfill_cli_bin() -> tempfile.TemporaryDirectory:
    """Keep agent shell commands on the importer's package and interpreter.

    A wizard launched from an isolated installation can inherit an older
    ``probe`` on PATH. That CLI may lack backfill attribution and attach the
    importing agent's session to reconstructed entities. A private launcher
    also supports editable/source installs without a sibling console script.
    The cached directory stays alive until this importer process exits.
    """
    global _BACKFILL_CLI_BIN
    with _BACKFILL_CLI_LOCK:
        if _BACKFILL_CLI_BIN is None:
            directory = tempfile.TemporaryDirectory(prefix="probe-backfill-cli-")
            bootstrap = (
                "import os, sys; "
                f"sys.path.insert(0, {str(Path(__file__).resolve().parents[2])!r}); "
                "os.environ['PROBE_ATTRIBUTION'] = 'backfill'; "
                "from probe.cli import main; raise SystemExit(main())"
            )
            launcher = Path(directory.name) / "probe"
            launcher.write_text(
                "#!/bin/sh\nexec "
                + shlex.quote(sys.executable)
                + " -c "
                + shlex.quote(bootstrap)
                + ' "$@"\n',
                encoding="utf-8",
            )
            launcher.chmod(0o700)
            _BACKFILL_CLI_BIN = directory
        return _BACKFILL_CLI_BIN


def _backfill_agent_env() -> dict[str, str]:
    return {
        **os.environ,
        "PROBE_ATTRIBUTION": "backfill",
        "PATH": _backfill_cli_bin().name + os.pathsep + os.environ.get("PATH", ""),
    }


#: Never walked, never offered, never counted. Not a judgment call about what
#: is interesting -- these are machine-generated trees whose file counts would
#: swamp the denominator and whose contents nobody wrote.
SKIP_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        ".ipynb_checkpoints",
        ".tox",
        ".eggs",
        ".idea",
        ".vscode",
        ".probe",
        # Dot-directories were ALL skipped until this list had to carry them
        # explicitly. A blanket `name.startswith(".")` also dropped
        # `.hydra/config.yaml` -- which is where Hydra writes the config that
        # NAMES the experiment -- along with `.dvc/` and `.condarc`, and it
        # dropped them from the CENSUS too, so the denominator claimed a
        # completeness it did not have. What belongs here is what a machine
        # wrote and nobody would look for in an import.
        ".cache",
        ".local",
        ".npm",
        ".cargo",
        ".conda",
        ".jupyter",
        ".ruff_cache",
        ".terraform",
        ".gradle",
        ".Trash",
        # CREDENTIAL STORES. These were covered by the blanket dotfile skip
        # that used to live in the walk; dropping that skip to admit
        # `.hydra/config.yaml` uncovered them, and an uncovered one is not
        # merely sampled -- it is WALKED, inherited into a project, manifested
        # and UPLOADED whole. Scrubbing samples does not touch that path,
        # because the upload sends bytes off disk and never reads a sample.
        ".ssh",
        ".aws",
        ".gnupg",
        ".kube",
        ".docker",
        ".azure",
        ".gcloud",
        ".config",
    }
)

#: Never counted, never sampled -- machine-written FILES.
#:
#: A separate set because SKIP_DIRS is only consulted for directories, and
#: these are files. They used to be caught by the blanket `startswith(".")`
#: that also ate `.hydra/config.yaml`; dropping that skip without this set put
#: `.DS_Store` back in the denominator, where it reads as a file someone wrote.
SKIP_FILES = frozenset(
    {
        # Machine-written junk.
        ".DS_Store",
        ".localized",
        "Thumbs.db",
        "desktop.ini",
        ".directory",
        # CREDENTIALS. Same reason as the credential directories above: the
        # walk admits dotfiles now, and admitting one of these means uploading
        # it. `tier_for` already refuses to SAMPLE them, which is a different
        # door -- a TAIL file is never sampled and is always uploaded.
        ".env",
        ".envrc",
        ".netrc",
        ".git-credentials",
        ".pypirc",
        ".npmrc",
        ".dockercfg",
        ".htpasswd",
        ".pgpass",
        "credentials",
        "id_rsa",
        "id_ed25519",
    }
)

#: Suffixes that are private keys or credential bundles whatever they are named.
SKIP_SUFFIXES = frozenset({".pem", ".key", ".p12", ".pfx", ".keystore", ".jks"})

#: Above this, record the PATH and not the bytes. A 1.2B-parameter checkpoint
#: is ~10GB and there is one every 2k steps; uploading them is neither possible
#: nor useful, and on a shared cluster mount a `file://` reference resolves
#: from every other researcher's pod anyway.
REFERENCE_ABOVE_BYTES = 100 * 1024 * 1024


#: One page of the anchor listing, matching the server's per-request artifact
#: ceiling. Hitting it exactly means "at least this many", never "this many".
RECONCILE_PAGE = 1_000


class Agent(StrEnum):
    """Which coding agent reads the folder.

    The importer's two are driven headlessly, do the work the same way, and are
    held to the SAME rule -- see CONFINEMENT below. Only the mechanism differs.
    """

    CLAUDE = "claude"
    CODEX = "codex"
    #: A RECOGNISED BINARY THE IMPORTER REFUSES. pi never runs the file
    #: importer: that lane needs the probe CLI via Bash, which pi's
    #: `DIGEST_TOOLS` allowlist deliberately lacks, so an import run on pi
    #: would read the whole folder and land nothing. `IMPORTER_AGENTS` below
    #: keeps the importer's picker off it and `resolve_agent` refuses
    #: `--agent pi` by name. The per-transcript digest lane that used to
    #: launch it retired server-side; no lane launches pi today.
    PI = "pi"


#: The agents the FILE IMPORTER offers, and the reason this is a tuple rather
#: than `list(Agent)`: enumerating the enum silently adopts whatever is added to
#: it, and `Agent.PI` is not an importer. Stated once, HERE, so a new
#: non-importer agent is opted in deliberately instead of leaking into every
#: picker that happened to iterate. Never filter PI out downstream -- that is
#: the same bug written once per call site.
IMPORTER_AGENTS: tuple[Agent, ...] = (Agent.CLAUDE, Agent.CODEX)


#: CONFINEMENT, and it is one property for both IMPORTER agents:
#:
#:     the imported folder is READ-ONLY; the agent writes only its own
#:     scratch directory, which is somewhere else entirely.
#:
#: This is the whole safety story, and stating it that way is what fixed it. The
#: earlier version confused "must not modify the folder" with "must not write at
#: all", so Claude ran with no Write tool while the import prompt instructed it
#: to write a manifest -- an impossible job, and every unit failed. Meanwhile
#: Codex ran `workspace-write` over the imported folder itself, which is the
#: property inverted: the customer's data was the one writable thing on disk.
#:
#: A scratch directory resolves both. The agent needs somewhere to put the
#: manifest; it does not need that somewhere to be the folder it is reading.
#:
#: The two mechanisms, and why each is the right instrument for its agent:
#:
#:   Claude   a PERMISSION RULE. `Edit(<folder>/**)` in a generated settings
#:            file, with the folder handed over read-only via `--add-dir` and
#:            the process cwd set to the scratch dir.
#:
#:            The rule MUST be spelled `Edit(...)`. A `Write(...)` deny rule is
#:            a silent no-op -- Claude Code prints "is not matched by file
#:            permission checks ... only Edit(path) rules are" and carries on.
#:            `Edit` covers every file-editing tool, Write included. Verified
#:            2026-08-06 against the real binary, both ways: with the rule the
#:            write is refused, without it the identical prompt succeeds.
#:
#:   Codex    the OS SANDBOX. `workspace-write` scoped by `-C <scratch>`.
#:            Codex confines where commands may WRITE, not which commands run,
#:            and reads are unrestricted -- so pointing the workspace at the
#:            scratch dir leaves the folder readable and unwritable in one move,
#:            with no pattern to get wrong. Verified the same day: read outside
#:            the workspace succeeded, write outside it was blocked.
#:
#: `workspace-write` rather than `read-only` because the upload has to reach the
#: network, and read-only mode has none. `--skip-git-repo-check` is REQUIRED,
#: not tidiness: Codex refuses to run outside a git repo, and neither a research
#: folder on a shared mount nor a scratch dir under XDG state is one.
#:
#: The DIGEST lane restates the property rather than weakening it: there is no
#: second tree at all. The agent is pointed at its own scratch dir, containing a
#: rendered view and nothing else, so "read the folder, write elsewhere" becomes
#: "the only readable thing is already derived". That is why `agent_argv` skips
#: the Claude pair when folder == workdir, and why pi -- which has neither a
#: permission file nor an OS sandbox -- can be launched here at all.
#:
#: Say precisely what pi's mechanism IS, because it is easy to over-claim. The
#: confinement is the `--tools` VALUE THIS CALL SENDS, whatever the caller
#: passed: pi has no rule file to fall back on, so an allowlist with `bash` in
#: it is an unconfined pi and nothing else refuses it. `DIGEST_TOOLS[Agent.PI]`
#: is the value the digest lane sends and the value this branch falls back to
#: -- it is the safe default, not the enforcement. And even that is only
#: sufficient because there is nothing outside the scratch dir to reach: pi is
#: launched for digests, never for an import over a researcher's folder.
AGENT_COPY: dict[Agent, tuple[str, str]] = {
    Agent.CLAUDE: (
        "Claude Code",
        "Imports files from the selected folder.",
    ),
    Agent.CODEX: (
        "Codex",
        "Imports files from the selected folder.",
    ),
    # Not an importer row, and no longer any picker's row: this copy is what
    # `too_old` and the launcher's not-on-PATH message name it as. pi is a
    # binary the folder importer recognises and refuses (`resolve_agent`); the
    # per-transcript digest lane that offered it retired server-side.
    Agent.PI: (
        "pi",
        "Not offered: its tool allowlist has no shell to run a folder import.",
    ),
}

#: Claude's tool allowlist. `Write`/`Edit` are here because the agent's whole
#: output IS a file it writes; the deny rule above is what keeps that file out
#: of the imported folder. Bash stays scoped to `probe` so the CLI is reachable
#: and nothing else is -- an unscoped Bash would route around the deny rule with
#: one `echo >`.
AGENT_TOOLS = "Bash(probe:*),Read,Glob,Grep,Task,Write,Edit"

#: The RECONSTRUCTION lane's allowlist, PER AGENT. Its one caller is
#: `backfill_reconstruction.py`, which launches a project-summary draft with
#: `tools=bf.DIGEST_TOOLS.get(agent)`; the `DIGEST_` name is the job these
#: three tables were sized for -- one agent, one rendered input file, one
#: written output -- and the reconstruction draft is that same job. (The
#: per-transcript digest lane that shared them retired server-side.) Per agent
#: because the tool names are not a shared vocabulary: Claude Code spells them
#: `Read,Write` and pi spells them `read,write`, and a lowercase name in
#: Claude's `--allowedTools` is not an error, it is an allowlist that matches
#: nothing. Keyed like `DIGEST_MODEL` below so the caller writes
#: `DIGEST_TOOLS[agent]` and cannot pick the wrong spelling; Codex is None
#: because it has no allowlist flag at all (its confinement is the OS
#: sandbox), not because it is unrestricted. The pi entry is also what
#: `agent_argv` falls back to for `--tools`, so it stays although no lane
#: launches pi today.
#:
#: What every entry has in common: no Bash AT ALL. The input is pre-rendered
#: text the lane writes into the agent's scratch dir (`evidence.json` for a
#: reconstruction draft), so there is nothing to parse and nothing a shell is
#: for. The 84-denial flail of 2026-08-29 was the model reaching for
#: python3/jq over raw JSONL; with a rendered view, read+write is the whole
#: job. Also no edit and no subagents: the output is one written file.
DIGEST_TOOLS: dict[Agent, str | None] = {
    Agent.CLAUDE: "Read,Write",
    Agent.CODEX: None,
    Agent.PI: "read,write",
}

#: Model override per agent, same caller. Claude gets haiku -- summarizing one
#: pre-rendered view is a haiku-class task and the launcher's default was
#: silently the session default model; `backfill_reconstruction.MODEL` layers
#: sonnet over this table for its cross-document drafts, which need more.
#: Codex and pi keep their configured defaults: neither has a stable cheap
#: alias worth pinning here, and a `None` entry is what says so rather than
#: an absent key a lookup would KeyError on.
DIGEST_MODEL: dict[Agent, str | None] = {
    Agent.CLAUDE: "haiku",
    Agent.CODEX: None,
    Agent.PI: None,
}

#: How long ONE reconstruction draft may take (`backfill_reconstruction.py`
#: passes it as `timeout=`). Far tighter than the import's deadlines
#: (`backfill_run.UNIT_TIMEOUT_S` 45 min, `CLASSIFY_TIMEOUT_S` 90 min) and for a
#: different reason: those bound an open-ended traversal of somebody's drive,
#: where thinking for minutes is legitimate work. A draft reads ONE file whose
#: size is already capped (`MAX_INPUT_BYTES`) and writes one small JSON --
#: there is no input that makes it long. And there is one PER PROJECT, up to
#: `MAX_PROJECTS` of them: a lane cannot spend 45 minutes apiece discovering
#: that each is wedged. Also the default bound for a pi launch (`_run_pi`).
DIGEST_TIMEOUT_S = 300.0

#: NOT `--bare`, which removes more and is the obvious-looking answer: it takes
#: auth down with it. "Anthropic auth is strictly ANTHROPIC_API_KEY or
#: apiKeyHelper (OAuth and keychain are never read)", so on a normal
#: subscription install every agent exits 1 with "Not logged in". Verified.
#: What a Claude invocation loads before it reads a single file. Measured on
#: this machine, 2026-08-06, as cache_creation + cache_read on a trivial prompt:
#:
#:     baseline (allowlist only)                47,198
#:     + --strict-mcp-config                    33,050
#:     + --disable-slash-commands               35,631
#:     + both                                   21,483   <- what we send
#:
#: A backfill launches one of these per unit and again per retry, so halving
#: the floor is the difference between fitting a unit's evidence in context and
#: compacting in the middle of describing it.
CONTEXT_FLAGS = ("--strict-mcp-config", "--disable-slash-commands")

CODEX_ARGS = (
    "-s",
    "workspace-write",
    "-c",
    "sandbox_workspace_write.network_access=true",
    "--skip-git-repo-check",
)

#: A permission rule's argument is delimited by parentheses, so a folder whose
#: own name contains one cannot be expressed as a rule -- and a rule that fails
#: to parse does not fail loudly, it just stops denying. `Research (old)` is an
#: ordinary macOS folder name, so this is a real path, not a theoretical one.
_UNRULEABLE = ("(", ")")


def readonly_settings(folder: Path) -> str:
    """Claude settings JSON that makes `folder` unwritable.

    Returned as a JSON string for `--settings`, which takes either that or a
    path. A string keeps the rule in the argv the test can read, rather than in
    a temp file whose lifetime is one more thing to get wrong.
    """
    import json

    return json.dumps({"permissions": {"deny": [f"Edit({folder}/**)"]}})


def unruleable(folder: Path) -> bool:
    """Whether `folder` cannot be confined by a Claude permission rule."""
    return any(ch in str(folder) for ch in _UNRULEABLE)


@dataclass(frozen=True)
class Census:
    """What the deterministic walk found. The denominator.

    Produced by folding :func:`probe.cli.backfill_evidence.walk`, which is now
    the only traversal in the flow. There used to be a second walker here --
    `scan` -- computing these two integers over provably the same file set,
    so a large folder was read end to end twice before the agent started.

    There is no `capped` any more. It existed for the folder picker, which
    wanted a bounded count so the cursor could move; the picker no longer
    counts at all, and the import was always uncapped. Its only lasting effect
    was a branch in `reconcile` that suppressed the shortfall warning -- a
    safety net that switched itself off at exactly the size that needed it.
    """

    files: int
    bytes: int
    #: Symlinked directories the walk declined to follow.
    #:
    #: NOT followed, and that is the right call -- a symlink can point at its
    #: own parent (an unbounded walk) or, on a shared drive, at somebody else's
    #: dataset, which an import would then file under this project. What was
    #: wrong is that it happened SILENTLY: the census reported the smaller
    #: number, the reconcile agreed with it, and a folder reachable through a
    #: link was simply absent with nothing to say so. That is the "silent 2%
    #: coverage that reads as done" this module exists to make impossible.
    #: Sorted, so two runs over the same drive show the same list -- the gate
    #: prints only the first few, and a reviewer who cannot reproduce what they
    #: were shown cannot act on it. Each entry is (link, target): the advice is
    #: "import what it points at", which is unusable without the target.
    linked_dirs: tuple[tuple[str, str], ...] = ()
    #: Directories the walk could not list at all. The SAME failure as
    #: `linked_dirs`, arriving through permissions instead of symlinks:
    #: everything beneath them is missing from this count and from the
    #: evidence, and it used to happen without a word.
    unreadable_dirs: tuple[str, ...] = ()

    @property
    def incomplete(self) -> bool:
        """True when the walk is known to have missed part of the folder."""
        return bool(self.linked_dirs or self.unreadable_dirs)

    def describe(self) -> str:
        noun = "file" if self.files == 1 else "files"
        line = f"{self.files:,} {noun}   {human_bytes(self.bytes)}"
        if self.linked_dirs:
            n = len(self.linked_dirs)
            line += f"   ({n} linked director{'y' if n == 1 else 'ies'} not followed)"
        if self.unreadable_dirs:
            n = len(self.unreadable_dirs)
            line += f"   ({n} director{'y' if n == 1 else 'ies'} unreadable)"
        return line


def human_bytes(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"  # pragma: no cover - loop always returns


def subdirectories(root: Path) -> list[Path]:
    """The browsable children of `root`. ALL of them, and no counting.

    This used to return a census per child, and the picker showed it as a label.
    Two problems fell out of that, and deleting the counting deletes both:

    * Every child was walked RECURSIVELY before the screen could draw. On a
      network mount with a dataset directory that is the slowest moment in the
      whole flow, paid again on every keypress that changes directory.
    * Because that was expensive, the picker capped the list at 40 children and
      said nothing about the rest. A workspace with sixty researcher folders
      showed forty, with no scrollbar, no count and no hint -- so a folder you
      could not see read as a folder that was not there.

    The counts were justified as "knowing `checkpoints/` is 2.9 TB before
    pointing an importer at it". They do not earn their cost: this is a folder
    picker, the import runs one uncapped census afterwards where precision
    actually matters, and anything over the reference threshold uploads as a
    path rather than bytes anyway.

    `os.scandir`, not `iterdir()` + `is_dir()`: the latter costs one `lstat`
    per child on top of reading the directory. 44 us/child locally is nothing,
    but a thousand children on a slow mount is seconds of pure listing before
    a row is drawn.

    FOLLOWING links, on purpose. `is_dir()` follows by default and so did the
    `Path` version this replaces, so a symlinked directory has always been a
    browsable row here. `follow_symlinks=False` would be faster still and would
    silently drop those rows -- a speedup is not a licence to change what the
    picker shows.
    """
    try:
        with os.scandir(root) as it:
            entries = [
                Path(e.path)
                for e in it
                if not e.name.startswith(".") and e.name not in SKIP_DIRS and _entry_is_dir(e)
            ]
    except OSError:
        return []
    return sorted(entries)


def _entry_is_dir(entry) -> bool:
    """`entry.is_dir()`, with an unreadable entry treated as not-a-directory."""
    try:
        return entry.is_dir()
    except OSError:
        return False


@dataclass(frozen=True)
class GitContext:
    """What the wizard knows about the folder's repository, if it is one."""

    toplevel: Path
    remote: str | None  # credential-scrubbed URL, or None (no remote)
    repo: str | None  # owner/name when the remote is github.com
    branch: str | None  # current branch, or None (detached)
    head: str | None = None
    upstream: str | None = None
    remote_name: str | None = None
    path_prefix: str = ""
    issue: str | None = None


def git_context(folder: Path) -> GitContext | None:
    """The folder's git identity, or None when it is not inside a work tree.

    Read-only by construction (`rev-parse`, `remote get-url`, `symbolic-ref`)
    and quick to give up: the same fail-fast env the snapshot capture uses, so
    a credential-prompting remote cannot hang the wizard.
    """
    from probe.sdk.snapshot import _git, _remote_url

    toplevel = _git(str(folder), "rev-parse", "--show-toplevel", check=False)
    if not toplevel:
        return None
    branch = _git(str(folder), "symbolic-ref", "--short", "-q", "HEAD", check=False) or None
    head = _git(str(folder), "rev-parse", "--verify", "HEAD", check=False) or None
    upstream = (
        _git(
            str(folder),
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{upstream}",
            check=False,
        )
        or None
    )
    names = (_git(str(folder), "remote", check=False) or "").splitlines()
    remotes = {name: _remote_url(toplevel, name) for name in names[:16]}
    remote_name = None
    issue = "remote_limit" if len(names) > 16 else None
    # branch.<name>.remote is authoritative when the branch tracks a remote;
    # the first component of upstream is not (remote names may contain '/').
    tracked = (
        _git(str(folder), "config", "--get", f"branch.{branch}.remote", check=False)
        if branch
        else None
    )
    if tracked and tracked in remotes:
        remote_name = tracked
    elif len(remotes) == 1:
        remote_name = next(iter(remotes))
    elif remotes:
        repos = {_github_repo(remote) for remote in remotes.values()}
        if len(repos) == 1 and None not in repos:
            remote_name = "origin" if "origin" in remotes else sorted(remotes)[0]
        else:
            issue = "ambiguous_remotes"
    remote = remotes.get(remote_name) if remote_name else None
    relative = Path(folder).resolve().relative_to(Path(toplevel).resolve()).as_posix()
    return GitContext(
        toplevel=Path(toplevel),
        remote=remote,
        repo=_github_repo(remote),
        branch=branch,
        head=head,
        upstream=upstream,
        remote_name=remote_name,
        path_prefix="" if relative == "." else relative + "/",
        issue=issue,
    )


def _github_repo(remote: str | None) -> str | None:
    """``owner/name`` when a remote points at github.com; None otherwise.

    The agent-side twin of the backend's `repo_from_remote_url`, with one extra
    tolerance: the value arrives CREDENTIAL-SCRUBBED (`<redacted>@github.com:…`),
    so the host is found structurally rather than by whole-prefix match. A
    GitLab or self-hosted remote is a normal answer, never an error.
    """
    if not remote:
        return None
    text = remote.strip()
    lowered = text.lower()
    idx = lowered.find("github.com")
    if idx == -1:
        return None
    # `github.com` must be the HOST, not a path segment: it may follow userinfo
    # (`@`), a scheme (`//`), or the string start. A single `/` before it is a
    # path — `https://evil.com/github.com/attacker/repo` is NOT github.com, and
    # accepting it would let a hostile imported .git/config steer the wizard's
    # `probe project code attach` suggestion at an attacker-named repo. `gist.`
    # / `evilgithub.com` are excluded because the char before the match is a
    # host character, not `@`/`/`/start.
    before = text[idx - 1] if idx > 0 else ""
    at_host = idx == 0 or before == "@" or (before == "/" and idx >= 2 and text[idx - 2] == "/")
    if not at_host:
        return None
    tail = text[idx + len("github.com") :]
    if not tail or tail[0] not in (":", "/"):
        return None
    tail = tail[1:].split("#", 1)[0].split("?", 1)[0].strip("/")
    if tail.lower().endswith(".git"):
        tail = tail[: -len(".git")]
    parts = tail.split("/")
    if len(parts) == 2 and all(parts) and not any(" " in part for part in parts):
        return "/".join(parts)
    return None


#: git-history.md is context for ONE agent prompt, not an archive: past this
#: it stops being read and starts being paid for.
GIT_HISTORY_MAX_BYTES = 40 * 1024


def write_git_history(context: GitContext, work_dir: Path) -> Path | None:
    """A bounded, DETERMINISTIC digest of the repository's history.

    Written by git, not by the agent: per-month roll-up (commits, authors, most
    touched paths), the tags, and the newest first-parent subjects. The durable
    record stays on the server side (the attached code source's timeline);
    this file exists so the import agent can order the work in time and tell
    superseded approaches from current ones without pausing to spelunk.
    """
    from collections import Counter, defaultdict

    from probe.sdk.snapshot import _git

    cwd = str(context.toplevel)
    log = _git(
        cwd,
        "log",
        "--first-parent",
        "--date=format:%Y-%m",
        "--name-only",
        "--pretty=format:%x1e%h%x1f%ad%x1f%an%x1f%s",
        "-n",
        "2000",
        check=False,
        timeout=30,
    )
    if not log:
        return None

    months: dict[str, dict] = defaultdict(
        lambda: {"commits": 0, "authors": set(), "paths": Counter()}
    )
    newest: list[str] = []
    total = 0
    for record in log.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        head, _, files = record.partition("\n")
        parts = head.split("\x1f")
        if len(parts) != 4:
            continue
        sha, month, author, subject = parts
        total += 1
        bucket = months[month]
        bucket["commits"] += 1
        bucket["authors"].add(author)
        for path in files.splitlines():
            if path:
                bucket["paths"][path.split("/", 1)[0]] += 1
        if len(newest) < 50:
            newest.append(f"- `{sha}` {month} {author}: {subject[:120]}")

    tags = _git(
        cwd,
        "tag",
        "--sort=-creatordate",
        "--format=%(refname:short)  %(creatordate:short)",
        check=False,
        timeout=10,
    )
    tag_lines = [line for line in (tags or "").splitlines() if line.strip()][:30]

    lines = [
        "# Git history digest (generated by `probe wizard`, read-only)",
        "",
        f"Repository: {context.repo or context.remote or '(no remote)'}"
        + (f"  branch: {context.branch}" if context.branch else ""),
        f"First-parent commits walked: {total}"
        + (" (capped at 2000 — older history exists)" if total >= 2000 else ""),
        "",
        "## By month (commits · authors · most-touched top-level paths)",
        "",
    ]
    for month in sorted(months, reverse=True):
        bucket = months[month]
        tops = ", ".join(path for path, _ in bucket["paths"].most_common(5))
        lines.append(
            f"- {month}: {bucket['commits']} commits · "
            f"{len(bucket['authors'])} authors · {tops or '(no paths)'}"
        )
    if tag_lines:
        lines += ["", "## Tags (newest first)", ""] + [f"- {line}" for line in tag_lines]
    lines += ["", "## Newest first-parent commits", ""] + newest + [""]

    text = "\n".join(lines)
    if len(text.encode()) > GIT_HISTORY_MAX_BYTES:
        text = text.encode()[:GIT_HISTORY_MAX_BYTES].decode(errors="ignore") + "\n(truncated)\n"
    out = work_dir / "git-history.md"
    out.write_text(text)
    return out


def slug_for(folder: Path) -> str:
    """A project slug derived from the folder name, deterministically.

    Derived rather than asked because the same folder must resolve to the same
    project on a re-run. A prompt would let a typo fork the identity, which is
    the one failure this flow cannot recover from.
    """
    raw = folder.resolve().name.lower()
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned or "backfill"


def resolve_anchor(client, folder: Path, *, requested: str | None = None) -> tuple[str, str]:
    """The project this folder imports into, as ``(project_id, slug)``.

    Returns the UUID, never the slug, because that is what the agent's commands
    need: every ``/v1/projects/{project_id}`` route types the path param as a
    UUID, so a slug arrives as a 422 about UUID parsing rather than a lookup.
    The slug rides along only to be shown to a human.

    THE FOLDER DECIDES, unless someone names a project on this command.

    The AMBIENT active project (`probe project use`, `PROBE_PROJECT`) is
    deliberately NOT consulted. It used to win, on the reasoning that whoever
    set it had already answered this question -- but it answers a different
    one. `project use` sets where new RUNS go by default; it is not a statement
    that every folder imported from here on belongs there. Honouring it meant
    pointing at `anthrogen-backfill-test` and watching 37 artifacts land in
    whatever project happened to be active, which is a surprising place to have
    to go looking for them.

    `requested` is an explicit `--project` on this invocation -- a slug, or an
    id written `id:<uuid>` -- and it still wins.

    Creation goes through ``ensure_project``, whose near-miss guard refuses a
    slug that looks like a typo of one already there. A folder called
    `odyssey-v2` sitting next to an existing `odyssey_v2` should stop, not
    quietly open a second identity for the same work.
    """
    if requested:
        return _resolve_ref(client, requested)
    proj = client.ensure_project(slug_for(folder), name=folder.resolve().name)
    return str(proj["id"]), proj.get("slug") or slug_for(folder)


def _resolve_ref(client, ref: str) -> tuple[str, str]:
    """An explicitly named project slug (or ``id:<uuid>``) -> ``(project_id, slug)``.

    Shares :mod:`probe.cli.refs` with the project verbs so an anchor cannot mean
    one project here and another one there -- this names every artifact the
    import uploads, and getting it wrong files someone's whole folder into a
    stranger's project.
    """
    from . import refs

    try:
        found = refs.resolve(client, "project", ref)
    except NotFoundError as exc:
        raise ValueError(str(exc)) from None
    return found.id, found.row.get("slug") or ref


def _subdivide_line(agent: Agent) -> str:
    """How to handle a big folder — which differs by what the agent HAS.

    Claude has a Task tool, so it can fan out over the subdirectories itself.
    Codex has no equivalent; telling it to "use subagents" would invite it to
    invent something, so it is told to work through the folder in passes
    instead.
    """
    if agent is Agent.CLAUDE:
        return (
            "If the folder is large or clearly splits into several independent pieces\n"
            "of work, subdivide it and use subagents — one per piece, each with this\n"
            "same anchor."
        )
    return (
        "If the folder is large, work through it one subdirectory at a time and\n"
        "keep going until every one is done. Do not stop at a sample."
    )


#: The skills whose text the importing agent reads, in order. These are the same
#: documents a live research session is given, and loading them is the whole
#: point: the hand-written command list they replace had drifted -- it never
#: mentioned subprojects, though `probe project create --parent` has existed for
#: a while, and it named eight commands out of a CLI the agent can already run
#: in full. A second copy of a vocabulary is a copy that goes stale.
VOCABULARY_SKILLS = ("track-work",)

#: What the importer overrides. A live session is told to register a project
#: before it designs anything, to create entities as it goes, and its work is
#: attributed to its session. None of that is true here, so the overrides are
#: stated ONCE, before the shared text, and the parity test asserts they are
#: still present.
VOCABULARY_PREAMBLE = """
HOW THIS RUN DIFFERS FROM AN ORDINARY RESEARCH SESSION. The reference below is
the same guidance a live session gets. Three of its instructions do not apply
to an import, and where they conflict, these win:

  1. The project list is FIXED. It was decided before you started, from evidence
     across the whole folder. Do not create projects or subprojects, and do not
     rename one. File into what you were given.
  2. Create an experiment only where the evidence is in front of you, and never
     to tidy up. An invented experiment is a wrong answer that looks right.
  3. Nothing here is attributed to a session. You are describing work that has
     already happened, not doing new work.

Everything else below is accurate, and the commands in it are available to you.
"""


def _skills_root() -> Path | None:
    """Where this installation's skill documents live, if they are readable.

    Shipped as package shared data (`share/probe-research/skills`), so an
    installed CLI carries them; a source checkout has them at `agent/skills`.
    Both are tried because both are real: the wizard runs from a released
    wheel, and the tests run from the tree.
    """
    candidates = [
        Path(sys.prefix) / "share" / "probe-research" / "skills",
        Path(__file__).resolve().parents[3] / "skills",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


@lru_cache(maxsize=1)
def vocabulary_text() -> str:
    """The shared skill text, or "" when this installation has none.

    EMPTY IS A VALID ANSWER. The importer's own rules live in the prompt around
    this and do not depend on it; a wheel built without the shared data should
    import a folder slightly less well, not fail to import it at all.
    """
    root = _skills_root()
    if root is None:
        return ""
    parts = []
    for name in VOCABULARY_SKILLS:
        try:
            body = (root / name / "SKILL.md").read_text(encoding="utf-8")
        except OSError:
            continue
        parts.append(f"--- reference: {name} ---\n{body.strip()}")
    if not parts:
        return ""
    return VOCABULARY_PREAMBLE + "\n\n" + "\n\n".join(parts) + "\n"


def build_prompt(
    *,
    folder: Path,
    census: Census,
    project: str | None = None,
    agent: Agent = Agent.CLAUDE,
) -> str:
    """The prompt the wizard hands the agent.

    This is the actual deliverable of the feature: the user never writes it, and
    every rule that keeps the import honest lives here rather than in code the
    agent cannot see.

    THE AGENT OWNS THE PROJECT STRUCTURE. An earlier version pinned one project,
    resolved before launch, on the reasoning that an agent free to name things
    would fork identities. That traded a real problem for a worse one: a folder
    like `/workspace` holds Michael's work, Xian's work and Connor's work, and
    collapsing three lines of research into one project named after the
    directory is a wrong answer that no amount of naming discipline fixes. The
    shape of the work is exactly the judgment we are paying an agent for.

    What replaces the pin is DISCIPLINE, not a lock: list what exists, reuse
    before creating, and let `ensure_project`'s near-miss guard refuse a slug
    that reads as a typo of one already there. `--project` still forces a single
    destination for anyone who wants the old behaviour.
    """
    vocabulary = vocabulary_text()
    fixed = (
        f"""
EVERYTHING GOES IN ONE PROJECT, named by the person who started this:

    --project {project}

Do not create any other project. If some of this work does not belong there,
say so in your summary rather than filing it elsewhere.
"""
        if project
        else """
YOU DECIDE THE PROJECTS. This is the judgement you are here for.

    First, see what already exists:
        probe project list

    Then decide. A folder is not automatically one project. `/workspace` with
    three researchers' directories under it is at least three; a single
    experiment directory is one. Split where the WORK is genuinely separate —
    different question, different model, different line of research — and keep
    it together where it is not.

    REUSE BEFORE YOU CREATE. If a project for this work already exists, file
    into it. Two projects for the same research is the one mistake here that
    nobody can undo later, and it is much easier to make than it looks: a
    second run that invents `odyssey-infill-v3` next to an existing
    `odyssey_infill_v3` has silently split the record in half.

    Name them for the WORK, not the directory. `odyssey-infill-v3` and
    `esm3-baseline` are names someone will recognise in six months;
    `workspace`, `data` and `michael` are not. Read enough of the folder to
    name it honestly before you create anything.

        probe project create <slug> --name "<human name>" \\
            --description "<what this project is, up to 3 sentences>" \\
            --tag <topic> --tag <model-or-dataset>

    ALWAYS pass --description: a plain description of the project. A few words is
    fine and three sentences is the ceiling — the point is that it is WRITTEN.
    Nothing else fills it in — the server generates one only when a child RUN
    reaches a terminal status, and importing a folder creates no runs, so a
    project left undescribed here stays undescribed forever. Missed one? Add it
    with `probe project set <slug> --description "..."`.

    `--project` takes the SLUG -- the one you just chose -- in every command
    that follows. (An id needs the `id:` prefix: `--project id:<uuid>`.)
"""
    )
    return f"""\
You are backfilling existing research work into Probe.

FOLDER: {folder}
This folder and its subdirectories are your entire scope. Do not read outside it.
A deterministic walk counted {census.files:,} files here — roughly what you should
expect to account for.
{fixed}
Step 1 — upload everything of substance.

    files under {human_bytes(REFERENCE_ABOVE_BYTES)}:
        probe artifact add --project <project> <path>

    files over {human_bytes(REFERENCE_ABOVE_BYTES)} (checkpoints, datasets, archives):
        probe artifact add --project <project> <path> --reference --allow-missing

    The second form records the PATH and uploads no bytes. Use it for anything
    large. Do NOT pass --hash on those: fingerprinting a 10GB file over a shared
    mount costs minutes and buys nothing here.

    Skip build noise and caches (.git, __pycache__, .venv, node_modules).

Step 2 — say what things are.

    For each artifact that carries meaning — a report, a result table, a config,
    a plot, a script someone would look for again — say in one line what it is,
    what produced it, what it shows. This is the part that makes a file findable
    later, and it is the part nobody did at the time. It matters more than the
    upload.

    The description goes in --notes:

        probe artifact add --project <project> <path> \\
            --notes "<what it is, what produced it, what it shows>"

    NEVER put the description in --name. The name is the file's relative path
    and nothing else: the folder tree is built by splitting it on '/', the
    dashboard works out how to preview a file from the extension at its end, and
    both break the moment a sentence is appended to it. --notes is a real field
    on every anchor; use it and leave the name alone.

    For what no single file explains, use the two project-level documents for
    their different audiences:

    - Put what this project is and how the pieces relate in its dashboard-visible
      authored Markdown, which is a block INSIDE the Overview page that the
      page's AI writer may not rewrite. Preserve the existing document before
      replacing it:

        probe project get <project> | jq -r '.document // ""' > PROJECT.md
        # Edit PROJECT.md, retaining useful existing sections.
        probe project set <project> --summary @PROJECT.md
        probe project get <project> | jq -r '.document // ""'

      This is a whole-document, last-write-wins field, so the first and last
      reads are required. The last read answers from the PAGE, which renders
      the document: a fenced block loses its language and a non-https link
      loses its href. Check that what you wrote is THERE; do not expect the
      bytes to match, and do not rewrite it again to try to make them.

    - Add what is missing, what a reader should not trust, and operational
      handoff details to the project's hidden notes:

        probe notes checkout --project <project>
        # add your paragraph to the file it names, then
        probe notes push --project <project>

      Notes are the agent briefing, not the dashboard documentation. `push`
      MERGES, so a concurrent import's paragraph is not erased -- and a real
      clash comes back as conflict markers rather than a silent overwrite.

Step 3 — group into experiments ONLY if the evidence is there.

    If some part of this plainly IS one experiment — a question, a method, a
    result you can point at — create it and attach those artifacts.
    If that would be a guess, DO NOT. Leave them at the project level.
    Artifacts at the project level are findable; an invented experiment is a
    wrong answer that looks like a right one.

        probe experiment create <slug> --project <project> \\
            --name "<human name>" --question "<what it tests>" \\
            --description "<what this experiment is, up to 3 sentences>"

    --description here too, and for the same reason: only a terminal run
    generates one, and this import creates none. Missed one? Add it with
    `probe experiment set <slug> --description "..."`. The files that convinced
    you this was a real experiment go in `probe notes write`, not here.

{_subdivide_line(agent)}

Finish with a JSON summary on its own line. `projects` must list every project
you filed into, by slug — it is how the import is checked against the {census.files:,}
files counted above:
{{{{"files_seen": N, "files_landed": N, "files_skipped": N,
  "projects": ["<slug>", ...], "experiments_created": N,
  "summary": "one sentence on what this folder contains"}}}}

{vocabulary}
"""


#: Flags whose ABSENCE stops the run, per agent. These are not preferences:
#: `--add-dir` + `--settings` ARE the Claude half of CONFINEMENT, and
#: `--output-format`/`--verbose`/`--allowedTools` are how the run is driven and
#: read at all. Running without any of them is either unconfined or blind.
REQUIRED_FLAGS: dict[Agent, tuple[str, ...]] = {
    Agent.CLAUDE: (
        "--output-format",
        "--verbose",
        "--allowedTools",
        "--add-dir",
        "--settings",
        "--session-id",
        "--resume",
    ),
    Agent.CODEX: ("--json", "--skip-git-repo-check"),
    # pi's `--tools` IS its confinement -- there is no permission file and no OS
    # sandbox behind it -- and `--no-session` is what stops a digest run minting
    # a pi session our own live tap then captures. `--mode` picks plain text over
    # pi's interactive stream. `--print` is how pi's help spells `-p`.
    Agent.PI: ("--print", "--tools", "--no-session", "--mode"),
}

#: Flags DROPPED, with a note, when the binary predates them. Each costs
#: something real -- context headroom, MCP isolation -- but none of them is
#: load-bearing for correctness or confinement, and refusing to import a
#: researcher's folder over a compaction hint is the wrong trade.
#:
#: NOT A LIST OF EVERY DROPPABLE FLAG, and `--model` is the one that proves it.
#: This table feeds `degraded_note`, which is printed by the FOLDER IMPORT lane
#: and only there -- the lane that never sends `--model` at all. Listing it here
#: would tell someone importing a research folder that their import is running
#: degraded because of a flag their import does not use, which is a false
#: statement in the wrong lane's copy. The `_has(supported, "--model")` gate in
#: `agent_argv` is untouched by this: `supported_flags` asks the binary, and
#: owes nothing to this table. The one lane that still sends `--model`, the
#: reconstruction draft (`backfill_reconstruction.py`), prints no degraded
#: note at all, so a dropped `--model` is surfaced nowhere today.
OPTIONAL_FLAGS: dict[Agent, tuple[str, ...]] = {
    Agent.CLAUDE: ("--autocompact", *CONTEXT_FLAGS),
    Agent.CODEX: (),
    # Extensions/skills/context files each load our own tap or the user's
    # configuration into a run whose entire job is reading one rendered file.
    # Worth dropping on an older pi rather than refusing the run. Kept
    # despite the caveat above only because they are still the honest answer to
    # `unsupported_flags`; pi never runs the import lane and no lane launches
    # it today, so nothing reports them to anyone.
    Agent.PI: ("--no-extensions", "--no-skills", "--no-context-files", "--model"),
}

#: WHICH help to ask, per agent, because the flags do not live in the same
#: place. Claude takes its options on the root command; Codex takes ours on the
#: `exec` SUBCOMMAND -- `codex --help` does not mention `--json` or
#: `--skip-git-repo-check` at all. Probing the root for Codex reports every
#: install, current ones included, as missing both: `too_old` then refuses
#: every Codex import with an upgrade instruction that cannot help, and on a
#: Codex-only machine backfill stops working entirely.
HELP_ARGV: dict[Agent, tuple[str, ...]] = {
    Agent.CLAUDE: ("--help",),
    Agent.CODEX: ("exec", "--help"),
    # pi takes everything on the root command; there is no subcommand.
    Agent.PI: ("--help",),
}

#: `--help` should answer instantly. A binary that cannot is a binary we are
#: about to hand a folder to for an hour, so a short bound is generous.
HELP_TIMEOUT_S = 20

#: An option DEFINITION line: indented, optionally a short form first, then the
#: long form. Anchored on purpose -- a bare scan of the help text also matches
#: flags named inside OTHER options' descriptions, and `claude --help` has
#: three of those today (`--allowed-tools`, `--background`,
#: `--disallowed-tools`). Reading a cross-reference as support is the guard
#: failing open on precisely the crash it exists to prevent.
_OPTION_LINE = re.compile(r"^\s{2,}(?:-[A-Za-z]\w*,\s*)?(--[A-Za-z][\w-]*)", re.M)


def _has(supported: frozenset[str] | None, flag: str) -> bool:
    """Whether `flag` may be passed. UNKNOWN counts as yes.

    The probe failing must never be the thing that removes a flag: that would
    turn a slow machine into a silently degraded import, which is the failure
    class this whole guard exists to close.
    """
    return supported is None or flag in supported


def supported_flags(binary: str, agent: Agent = Agent.CLAUDE) -> frozenset[str] | None:
    """Long options `binary --help` advertises, or None if it would not say.

    THE PROBE, AND WHY IT IS A PROBE. The CLI hands the agent binary a fixed
    argv, and an agent CLI parses options strictly: one it does not recognise
    is a non-zero exit before it reads a single file. Anthrogen hit this on
    2026-08-12 -- `--autocompact` had landed in #194 six days earlier, their
    Claude Code predated it, and all 33 classify slices died identically with
    `error: unknown option '--autocompact'`. The import reported "the
    classification did not produce a usable plan" and nothing else.

    ASKING THE BINARY, not comparing versions. A floor means knowing which
    release added each flag, writing it down, and remembering to raise it every
    time a flag is added -- and the failure of forgetting is silent and total.
    `--help` is the same question asked of the thing that will actually answer
    it, and it stays correct for flags nobody has written yet.

    ASKING THE RIGHT HELP. The flags are not all on the root command -- see
    `HELP_ARGV`. Getting this wrong does not fail open: the wrong subcommand
    answers rc 0 with a real option list, so every flag we care about reads as
    missing and the guard refuses a binary that was fine.

    None on ANY doubt -- non-zero exit, timeout, unreadable output. See `_has`:
    unknown means "pass the flag", so a broken probe leaves behaviour exactly
    as it was rather than quietly stripping the argv.
    """
    return _supported_flags_cached(binary, HELP_ARGV[agent])


@lru_cache(maxsize=8)
def _supported_flags_cached(binary: str, help_argv: tuple[str, ...]) -> frozenset[str] | None:
    """One help call per (binary, subcommand) per process. See `supported_flags`."""
    try:
        done = subprocess.run(
            [binary, *help_argv],
            capture_output=True,
            text=True,
            timeout=HELP_TIMEOUT_S,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    found = set(_OPTION_LINE.findall(done.stdout or ""))
    # An empty parse is a help text we did not understand, not a binary with no
    # options. Treating it as "supports nothing" would strip every flag.
    return frozenset(found) or None


def unsupported_flags(agent: Agent, binary: str) -> tuple[list[str], list[str]]:
    """``(required_missing, optional_missing)`` for this binary."""
    supported = supported_flags(binary, agent)
    if supported is None:
        return [], []
    return (
        [f for f in REQUIRED_FLAGS[agent] if f not in supported],
        [f for f in OPTIONAL_FLAGS[agent] if f not in supported],
    )


def too_old(agent: Agent, binary: str) -> str | None:
    """Why this binary cannot run an import, or None if it can.

    Checked ONCE, before the folder is walked. Per-invocation would be correct
    and useless: the walk is minutes on the drives this feature is for, and
    finding out afterwards -- 33 times, once per slice -- is what actually
    happened.
    """
    missing, _ = unsupported_flags(agent, binary)
    if not missing:
        return None
    return (
        f"{_describe(agent, binary)} is too old for the import: it does not "
        f"accept {', '.join(missing)}. Upgrade {AGENT_COPY[agent][0]} and "
        "re-run — nothing was read."
    )


def _describe(agent: Agent, binary: str) -> str:
    """`This Claude Code (1.0.4)`, or without the version when it would not say.

    NAMING THE VERSION. "Upgrade Claude Code" is advice the reader cannot check
    against anything: they do not know what they have, and neither did we --
    `doctor` recorded a boolean until 0.79.0. With the number in the sentence
    they can compare it to the release notes, and a bug report carries the one
    fact that would otherwise take a round trip to establish.

    Omitted rather than guessed when the probe could not read it: `This Claude
    Code (unknown)` reads like a broken install on top of an old one.
    """
    name = AGENT_COPY[agent][0]
    version = _agent_version_cached(binary)
    return f"This {name} ({version})" if version else f"This {name}"


def degraded_note(agent: Agent) -> str | None:
    """What this binary is too old to be given, or None if nothing.

    Said out loud rather than dropped quietly. Each of these costs something a
    reader would want to know about: without `--autocompact` a long
    classification has less context headroom, and without the isolation flags
    the agent runs with whatever MCP servers and slash commands the user has
    configured, inside an import that is supposed to see only the folder.
    """
    binary = which_agent(agent)
    if binary is None:
        return None
    _, optional = unsupported_flags(agent, binary)
    if not optional:
        return None
    return (
        f"{_describe(agent, binary)} does not accept {', '.join(optional)}, so "
        "the import runs without them. It will work; upgrade "
        f"{AGENT_COPY[agent][0]} for the isolation and context headroom they buy."
    )


def agent_version(agent: Agent) -> str | None:
    """The agent binary's own version string, or None.

    Recorded so the NEXT flag break is visible. `doctor` knew only whether the
    binary existed -- a boolean -- so a fleet-wide failure caused entirely by
    old Claude Code installs produced no signal at all, and the one report that
    surfaced it was a screenshot in a meeting.
    """
    binary = which_agent(agent)
    if binary is None:
        return None
    return _agent_version_cached(binary)


@lru_cache(maxsize=8)
def _agent_version_cached(binary: str) -> str | None:
    try:
        done = subprocess.run(
            [binary, "--version"], capture_output=True, text=True, timeout=HELP_TIMEOUT_S
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    first = (done.stdout or "").strip().splitlines()
    if not first:
        return None
    # "2.1.231 (Claude Code)" / "codex-cli 0.24.0" -- the number is the part
    # worth comparing, and the rest is branding that changes on its own.
    match = re.search(r"\d+\.\d+\.\d+", first[0])
    return match.group(0) if match else first[0][:32] or None


def which_agent(agent: Agent) -> str | None:
    """The agent's real binary, or None.

    `shutil.which`, never a shell: `codex` in particular is commonly SHADOWED by
    a shell alias (a local wrapper here), and an alias would silently swallow
    the arguments below. A PATH lookup with no shell cannot see one.

    pi needs a second question asked. "pi" is two letters and anything can be
    named that, so a bare `which` hit is not evidence -- the `--help` "coding"
    sniff is the impostor guard the wizard already uses, and this is the same
    one, so pi is detected by one rule in one place.
    """
    if agent is Agent.PI:
        path = shutil.which("pi")
        return path if path and pi_config.pi_binary_available() else None
    return shutil.which(agent.value)


def available_agents() -> list[Agent]:
    """Installed IMPORTER agents, in menu order. Empty means backfill cannot run.

    `IMPORTER_AGENTS`, not the enum: the digest lane has its own resolver and
    its own idea of what is usable, and a picker that walked every enum member
    would offer a folder import to an agent with no shell to run `probe` in.
    """
    return [a for a in IMPORTER_AGENTS if which_agent(a) is not None]


#: The largest a SINGLE argv element may be, in BYTES.
#:
#: Not `getconf ARG_MAX` (2MB here), which is the total and is the number
#: everyone checks. Linux caps each individual element at `MAX_ARG_STRLEN` =
#: 32 pages, and exceeding it is `E2BIG` from `execve` -- surfaced by this
#: module as "argument list too long" with no hint about which element.
#:
#: This is why the prompt is NOT in the argv. It used to be (`-p <prompt>`),
#: sized against the model's CONTEXT window: `SINGLE_SHOT_TOKEN_BUDGET` of 90k
#: tokens is 288,000 chars, 2.2x over this ceiling, and `CHUNK_TOKEN_BUDGET`
#: at 176,000 chars was over it too -- so the chunked route, which exists to
#: fix "too big for one prompt", crashed identically. Measured: any folder
#: past ~154 sampled evidence files. Those two budgets are context budgets
#: again now, and nothing but this constant guards the transport.
MAX_ARG_STRLEN = 131_071


class ArgvTooLargeError(ValueError):
    """An argv element would be rejected by `execve`.

    Raised rather than asserted: `assert` vanishes under `python -O`, and a
    guard that silently disappears in one deployment mode is worse than none.
    """


def check_argv(argv: list[str]) -> list[str]:
    """Fail loudly, and BEFORE the exec, on an argv element `execve` will reject.

    A tripwire, not a routine check. Nothing in the argv is user content any
    more -- the prompt goes to stdin and what remains is flags, a binary path,
    a folder path and a small settings JSON. That is the point: if this ever
    fires again, something put content back in the argv, and the message says
    which element rather than leaving `[Errno 7]` to be re-diagnosed.

    BYTES, not characters. `len(str)` counts code points and this ceiling is
    bytes, so a folder path or a sample carrying non-ASCII passes a character
    check and still fails the exec. The same units bug has shipped twice in
    this repo (`team_note_file.py`, hooks `additionalContextLimit`).
    """
    for i, element in enumerate(argv):
        size = len(element.encode("utf-8", "replace"))
        if size >= MAX_ARG_STRLEN:
            raise ArgvTooLargeError(
                f"argv[{i}] is {size:,} bytes, over the {MAX_ARG_STRLEN:,}-byte "
                f"per-element limit execve enforces (starts: {element[:60]!r}). "
                "Anything this large belongs on stdin or in a file the agent reads."
            )
    return argv


def agent_argv(
    agent: Agent,
    binary: str,
    folder: Path,
    *,
    workdir: Path | None = None,
    tools: str | None = None,
    model: str | None = None,
    session_id: str | None = None,
    resume: str | None = None,
) -> list[str]:
    """The headless invocation for one agent. THE PROMPT IS NOT IN IT.

    All three read the prompt from stdin: `claude -p` and `pi -p` with no
    prompt argument, and `codex exec` with no positional. See `MAX_ARG_STRLEN`
    for why, and `run_one` for how the prompt is fed.

    Codex must be given NEITHER a positional NOR `-`, only piped stdin: its
    own docs say a prompt supplied alongside piped stdin makes the stdin
    arrive as a separate `<stdin>` block rather than as the instructions.

    The two IMPORTER agents are asked for a JSONL EVENT STREAM, and that is not
    a preference. A bare `claude -p` prints nothing at all until the whole run
    finishes, so a backfill over a real folder sat silent for minutes and read
    as hung -- which is exactly what it looked like. The event stream is the
    only way to know the agent is alive, and the only way to count what it has
    done so far. pi is asked for plain `--mode text` instead: it runs one
    bounded digest with `progress=False`, so there is nothing to fold and
    nobody watching a counter.

    `workdir` is the agent's SCRATCH directory -- the one place it may write.
    The importer's agents are pointed at it as their working root and given
    `folder` as something to read, by the two different mechanisms CONFINEMENT
    describes. Claude takes cwd from the process, so its half is `--add-dir`
    plus the deny rule; Codex resolves its writable workspace from `-C` rather
    than from cwd, so pointing that there is the whole of its half.

    Without a `workdir` both fall back to running IN `folder`, which is what the
    non-import callers (and the tests that predate the scratch dir) expect.

    `session_id` names the session so the ledger can record it; `resume` picks
    one back up. A unit killed mid-turn leaves a transcript whose last message
    asks for a tool result that never arrived, and that DOES replay cleanly --
    verified 2026-08-06 against a SIGKILL, exit 0 with context intact, and a
    SIGTERM is safer still because Claude Code writes the missing tool_result
    before dying. The journal still decides WHICH units rerun; resume only
    decides whether a rerun keeps what it had already read.

    Codex has no equivalent, so its units restart clean. That is why `resume` is
    ignored for it rather than approximated with something that looks similar.

    `tools` and `model` are the digest lane's two overrides -- the caller sends
    `DIGEST_TOOLS[agent]` and `DIGEST_MODEL[agent]`, both keyed because the tool
    names are spelled differently per agent. Absent, both mean "exactly what the
    importer has always sent": the allowlist stays `AGENT_TOOLS` and no
    `--model` is passed at all, which is not the same as passing a default we
    picked. Codex takes neither -- it has no allowlist flag, and its
    `DIGEST_MODEL` entry is None on purpose.
    """
    supported = supported_flags(binary, agent)
    if agent is Agent.PI:
        argv = [
            binary,
            "-p",  # no prompt argument: it arrives on stdin, like the other two
            "--mode",
            "text",
            # pi has no permission file and no OS sandbox, so whatever value
            # lands here IS the confinement -- see CONFINEMENT. The fallback is
            # the digest entry rather than a literal, so the safe default is
            # written down in exactly one place.
            "--tools",
            tools or DIGEST_TOOLS[Agent.PI],
            # A digest run must not mint a session our own live tap then
            # captures -- a recursive capture whose input is the last digest.
            "--no-session",
        ]
        argv += [
            f
            for f in ("--no-extensions", "--no-skills", "--no-context-files")
            if _has(supported, f)
        ]
        if model and _has(supported, "--model"):
            argv += ["--model", model]
        return check_argv(argv)
    if agent is Agent.CLAUDE:
        argv = [
            binary,
            "-p",  # no prompt argument: it arrives on stdin
            "--output-format",
            "stream-json",
            "--verbose",  # required: stream-json emits only the result without it
            "--allowedTools",
            tools or AGENT_TOOLS,
        ]
        # OPTIONAL flags are filtered against the binary in front of us. An
        # older Claude Code exits on the first option it does not recognise,
        # before reading a single file -- see `supported_flags`.
        if _has(supported, "--autocompact"):
            argv += ["--autocompact", "auto"]
        argv += [f for f in CONTEXT_FLAGS if _has(supported, f)]
        if model and _has(supported, "--model"):
            argv += ["--model", model]
        # RESOLVED, not compared as written: the question is whether these are
        # the same directory on disk, and a scratch path reached through a
        # symlink (macOS `/var` -> `/private/var`, a `..` in a caller's path)
        # is the same dir spelled differently. Getting that wrong writes a deny
        # rule over the agent's own output file.
        if workdir is not None and Path(folder).resolve() != Path(workdir).resolve():
            # Read the folder, write only the scratch dir. Both halves, or
            # neither: --add-dir alone makes the folder WRITABLE, which is the
            # opposite of what it is here for.
            #
            # SAME DIR IS THE EXCEPTION, not an oversight. When the folder IS
            # the workdir the only visible tree is the scratch dir the agent was
            # given to write in, so a deny rule on it would block the output
            # file this run exists to produce -- and there is no second tree
            # left to protect. That is the digest lane: it hands the agent a
            # rendered view inside its own scratch dir and nothing else.
            argv += [
                "--add-dir",
                str(folder),
                "--settings",
                readonly_settings(folder),
            ]
        if resume:
            argv += ["--resume", resume]
        elif session_id:
            # Mutually exclusive: --session-id MINTS one, --resume ADOPTS one,
            # and passing both asks for a session that must be simultaneously
            # new and pre-existing.
            argv += ["--session-id", session_id]
        return check_argv(argv)
    return check_argv(
        [
            binary,
            "exec",
            "--json",
            *CODEX_ARGS,
            "-C",
            str(workdir if workdir is not None else folder),
            # No positional prompt and no `-`: stdin alone is the instructions.
        ]
    )


#: Spinner frames. Something has to MOVE while the agent is thinking, or a long
#: quiet turn is indistinguishable from a hang -- the bug this replaced.
_SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

#: How an upload is recognised in either agent's event stream.
#:
#: It no longer happens, and that is the point of the comment. Agents stopped
#: running `artifact add` when the two-pass split landed -- the classify pass
#: uploads nothing by design, and an import unit writes a manifest that ONE
#: process enqueues afterwards. So the counter this drove sat at `0/204` for
#: entire runs, in both passes, and looked like a hang on a working import.
#: Kept because a stray `artifact add` is still worth counting if one appears.
_UPLOAD_MARKER = "artifact add"

#: Reads before an ETA is offered. An estimate from two files is noise wearing
#: a number's clothes -- file sizes vary by orders of magnitude and the first
#: reads include the agent's start-up.
_ETA_FLOOR = 5


@dataclass
class Activity:
    """Live state of one agent run, folded from its event stream.

    PROGRESS IS FILES READ, not files uploaded. The denominator is the unit's
    own file list -- exactly what the agent was told to read -- so the fraction
    is real and the ETA derived from it means something. Counting uploads gave
    a permanent zero (see `_UPLOAD_MARKER`).

    `seen` is a set, not a counter: an agent re-reading a file it already read
    must not advance the bar past what it has actually covered.
    """

    total: int
    uploaded: int = 0
    doing: str = "starting up"
    ticks: int = 0
    seen: set = field(default_factory=set)
    queued: bool = False

    @property
    def done(self) -> int:
        """Files covered so far, never more than the denominator.

        Clamped because an agent may legitimately read something outside its
        unit -- a shared config, a README one directory up -- and `14/8` reads
        as a bug in the tool rather than curiosity in the agent.
        """
        return min(len(self.seen) or self.uploaded, self.total) if self.total else 0

    def eta(self, elapsed: float) -> str:
        """`~2:05 left`, or "" when there is not enough to say.

        Deliberately blank rather than optimistic: no reads yet, nothing left
        to do, or too few samples all produce a number that would be invented.
        """
        done = self.done
        if done < _ETA_FLOOR or done >= self.total or elapsed <= 0:
            return ""
        remaining = elapsed * (self.total - done) / done
        mins, secs = divmod(int(remaining), 60)
        return f"~{mins}:{secs:02d} left" if mins < 60 else "~over an hour left"

    def line(self, elapsed: float, width: int = 46) -> str:
        if self.queued:
            return f"  ·  queued · 0/{self.total}" if self.total else "  ·  queued"
        mins, secs = divmod(int(elapsed), 60)
        parts = [
            _SPIN[self.ticks % len(_SPIN)],
            f"{mins}:{secs:02d}",
        ]
        if self.total:
            parts.append(f"· {self.done}/{self.total}")
        eta = self.eta(elapsed)
        if eta:
            parts.append(f"· {eta}")
        head = "  " + " ".join(parts) + " · "
        room = max(12, width - (len(head) - len(f"  {_SPIN[0]} 0:00 · 0/0 · ")))
        doing = self.doing if len(self.doing) <= room else self.doing[: room - 1] + "…"
        return head + doing


#: Commands that mean "the agent looked at this file". Codex has no Read tool
#: event, so its progress has to be read out of the shell it runs.
_READ_COMMANDS = ("cat", "head", "tail", "less", "more", "bat", "sed", "nl")


def _read_target(command: str) -> str | None:
    """The file a read-shaped shell command names, or None.

    Conservative on purpose. Over-counting inflates the bar and the ETA with
    it, so anything ambiguous -- a pipeline, a glob, a flag where the path
    should be -- returns None and simply does not count. An under-reported bar
    catches up; an over-reported one strands at "almost done".
    """
    text = " ".join(command.split())
    for wrapper in ("/bin/zsh -lc ", "/bin/bash -lc ", "/bin/sh -c "):
        if text.startswith(wrapper):
            text = text[len(wrapper) :].strip("'\"")
    if any(ch in text for ch in "|><*?"):
        return None
    parts = text.split()
    if len(parts) < 2 or Path(parts[0]).name not in _READ_COMMANDS:
        return None
    targets = [p for p in parts[1:] if not p.startswith("-")]
    return targets[-1] if len(targets) == 1 else None


def _shorten(command: str) -> str:
    """A shell command as a phrase worth showing on one line.

    The interesting part of `probe artifact add --project <uuid> /long/path`
    is the filename, and the uuid is the least interesting thing in it.
    """
    text = " ".join(command.split())
    for wrapper in ("/bin/zsh -lc ", "/bin/bash -lc ", "/bin/sh -c "):
        if text.startswith(wrapper):
            text = text[len(wrapper) :].strip("'\"")
    if _UPLOAD_MARKER in text:
        parts = [
            p
            for p in text.split()
            if not p.startswith("--") and p not in ("probe", "artifact", "add")
        ]
        # Drop the project id; keep the path.
        paths = [p for p in parts if "/" in p or "." in p]
        return f"uploading {Path(paths[-1]).name}" if paths else "uploading"
    return text


def fold_event(raw: str, state: Activity) -> bool:
    """Fold one stdout line into `state`. True if it said something new.

    Tolerant by construction: both agents interleave NON-JSON on stdout (Claude
    prints the connectors warning there, Codex a stdin notice and tracing), and
    a parser that treated that as fatal would blank the display for the rest of
    the run.
    """
    import json

    line = raw.strip()
    if not line or not line.startswith("{"):
        return False
    try:
        event = json.loads(line)
    except ValueError:
        return False
    if not isinstance(event, dict):
        return False

    kind = event.get("type")

    # Claude: assistant turns carry tool_use blocks.
    if kind == "assistant":
        for block in event.get("message", {}).get("content", []) or []:
            if block.get("type") != "tool_use":
                continue
            args = block.get("input") or {}
            name = block.get("name", "")
            if name == "Bash":
                command = str(args.get("command", ""))
                if _UPLOAD_MARKER in command:
                    state.uploaded += 1
                state.doing = str(args.get("description") or _shorten(command))
            elif args.get("file_path"):
                # THE PROGRESS SIGNAL. A unit is told to read a known list of
                # files, so distinct reads against that list is a real fraction
                # -- and the only one available, since agents no longer upload.
                path = str(args["file_path"])
                state.seen.add(path)
                state.doing = f"reading {Path(path).name}"
            elif args.get("pattern"):
                state.doing = f"searching {args['pattern']}"
            else:
                state.doing = name.lower() or "working"
            return True
        return False

    # Codex: item.started / item.completed carry command_execution + messages.
    if kind in ("item.started", "item.completed"):
        item = event.get("item") or {}
        if item.get("type") == "command_execution":
            command = str(item.get("command", ""))
            if kind == "item.started":
                if _UPLOAD_MARKER in command:
                    state.uploaded += 1
                # Codex reads by shelling out, so its progress signal is the
                # file a read-shaped command names -- there is no Read tool
                # event to count. Same denominator, same fraction.
                read = _read_target(command)
                if read:
                    state.seen.add(read)
                state.doing = _shorten(command)
                return True
        elif item.get("type") == "agent_message" and kind == "item.completed":
            text = " ".join(str(item.get("text", "")).split())
            if text:
                state.doing = text
                return True
        return False

    if kind == "turn.started":
        state.doing = "thinking"
        return True
    return False


#: Every agent process this run has started and not yet reaped.
#:
#: A registry, not a local, because leaving the wizard has to stop EVERYTHING
#: and the thing being left is spread across threads: the import pass runs
#: several agents at once, and whichever thread takes the Ctrl-C can only see
#: its own. A 106,007-file import kept reading after "Cancelled by user" for
#: exactly this reason.
#:
#: The outbox is deliberately NOT in here. It is a background drainer with its
#: own `probe outbox pause`, and killing it on the way out would abandon files
#: that are already queued and already the user's -- the one thing leaving a
#: wizard must not do.
_LIVE: set = set()
_LIVE_LOCK = threading.Lock()


def _kill_tree(proc) -> None:
    """Kill an agent and everything it started.

    The PROCESS GROUP, not the process. An agent starts MCP servers, subagents
    and shells; `proc.kill()` reaps the direct child and orphans the rest,
    which keep running with no parent to stop them.

    SIGTERM first, because Claude Code writes the missing tool_result on the
    way down and that transcript is what `--resume` replays -- a SIGKILL here
    costs the unit its resumability. SIGKILL only for what ignores it.
    """
    if proc.poll() is not None:
        return
    for sig, grace in ((signal.SIGTERM, 3.0), (signal.SIGKILL, 2.0)):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError, OSError):
            # No group (Windows, or already reaped) -- fall back to the child.
            try:
                proc.kill()
            except OSError:
                return
        try:
            proc.wait(timeout=grace)
            return
        except subprocess.TimeoutExpired:
            continue


def stop_all() -> None:
    """Stop every agent this process started. Safe to call more than once.

    What "leaving the wizard" means. Called from the interrupt path and from a
    `finally` at the top of the import, so no exit route leaves an agent
    reading someone's folder.
    """
    with _LIVE_LOCK:
        procs = list(_LIVE)
        _LIVE.clear()
    for proc in procs:
        _release_agent(proc)


def _register_agent(proc, cancel_event: threading.Event | None = None) -> bool:
    """Register a launch, or stop it if cancellation overtook its spawn.

    The cancellation event is sticky. If stop_all snapshots the registry before
    this child arrives, the child sees the event here and releases itself. If
    cancellation comes afterwards, the child is already in stop_all's snapshot.
    No lock is held while spawning, waiting for model output, or killing a child.
    """
    with _LIVE_LOCK:
        _LIVE.add(proc)
        cancelled = cancel_event is not None and cancel_event.is_set()
    if cancelled:
        _release_agent(proc)
    return not cancelled


def _release_agent(proc) -> None:
    """Stop a still-live launch before releasing its durable ownership.

    The job supervisor interrupts with a BaseException, which can reach a
    launch's finally without passing through its KeyboardInterrupt handler.
    Removing that live process from _LIVE first used to orphan it even on a
    graceful worker stop.
    """
    from . import import_jobs

    pid = getattr(proc, "pid", None)
    if isinstance(pid, int):
        if proc.poll() is None:
            _kill_tree(proc)
        if proc.poll() is None:
            return  # Keep the durable registry until the process really stops.
        try:
            import_jobs.unregister_child(pid)
        except Exception:
            # A stale entry is safe: recovery verifies its original process
            # identity. Cleanup must still stop every other registered child.
            pass
    with _LIVE_LOCK:
        _LIVE.discard(proc)


#: How often the idle-deadline poller checks the gap since the last event. It is
#: the RESOLUTION of `timeout`, not a second deadline: a kill lands up to one
#: tick late, which against bounds measured in minutes (`UNIT_TIMEOUT_S` is 45
#: of them) is noise. Fixed rather than derived from `timeout` so one wedged
#: agent cannot spin a poller at whatever rate a caller's number implies.
_WATCHDOG_TICK_S = 1.0

#: How much of pi's output is kept. This string is the entire record of a failed
#: digest, and an unbounded one puts a runaway run's megabytes into a lane report
#: somebody reads.
_PI_TAIL_CHARS = 2000


def _pi_tail(*chunks) -> str:
    """The last `_PI_TAIL_CHARS` of pi's output, decoded defensively.

    BYTES ARE A REAL CASE here, not paranoia. `TimeoutExpired.stdout` carries
    the raw chunks read before the deadline -- the process decoder never saw
    them -- so it is `bytes` even on a `Popen` opened with an `encoding`.
    Formatting that into a message gives `b'...'` with the escapes visible;
    calling `.decode` unconditionally raises on the normal path, where it is
    already `str`. Both, or this helper is a crash in the error path.
    """
    text = ""
    for chunk in chunks:
        if not chunk:
            continue
        text += chunk.decode("utf-8", "replace") if isinstance(chunk, bytes) else chunk
    return text[-_PI_TAIL_CHARS:]


def _run_pi(
    binary: str,
    folder: Path,
    prompt: str,
    *,
    workdir: Path | None,
    tools: str | None,
    model: str | None,
    timeout: float | None,
    label: str,
    out,
    paint_to,
    cancel_event: threading.Event | None = None,
) -> tuple[bool, str]:
    """One headless pi digest: launch it, feed the prompt, wait, report.

    THIS SHORT-CIRCUITS THE STREAMING MACHINERY, NOT THE TEARDOWN CONTRACT, and
    the distinction is the whole reason this is not the four-line
    `subprocess.run` it looks like it wants to be. pi runs `--mode text`, which
    is not our stream-json: no event to fold, no file counter to advance, and a
    digest runs `progress=False` anyway, so `fold_event` and the spinner have
    nothing to do. Everything ELSE `launch_agent` documents still holds. An
    agent is not one process -- it starts servers and shells of its own -- so it
    needs its OWN PROCESS GROUP and a row in `_LIVE`, or Ctrl-C leaves it
    reading with the wizard gone. `subprocess.run` gives neither, and that exact
    bug has already shipped once (see `stop_all`).

    `communicate` is what makes the prompt safe on stdin: it writes and reads
    concurrently, so the pipe-buffer deadlock the streaming path stages a temp
    file to avoid cannot happen. The prompt is never an argv element -- a
    rendered view is far past `MAX_ARG_STRLEN`.
    """
    from . import import_jobs

    if cancel_event is not None and cancel_event.is_set():
        return False, "agent cancelled"
    tag = f"{label} " if label else ""

    def note(text: str) -> None:
        # The two destinations the streaming path writes its status line to,
        # and no third one. TWO LINES is the entire budget: a pi digest prints
        # nothing at all until it exits, and this module's own history is that
        # a silent agent is indistinguishable from a hang -- for up to
        # DIGEST_TIMEOUT_S here. There is no event stream to drive more than
        # "started" and "finished", and inventing a spinner for one bounded
        # call would be the machinery this branch exists to skip.
        if paint_to is not None:
            paint_to(text)
            return
        out.write(f"  {text}\n")
        out.flush()

    # `is None`, not `or`: an explicit `timeout=0` is a caller asking for
    # something specific, and `or` would silently substitute five minutes.
    bound = DIGEST_TIMEOUT_S if timeout is None else timeout
    try:
        argv = agent_argv(Agent.PI, binary, folder, workdir=workdir, tools=tools, model=model)
    except ArgvTooLargeError as exc:
        return False, str(exc)

    if cancel_event is not None and cancel_event.is_set():
        return False, "agent cancelled"

    # Same copy shape as the claude/codex quiet-run notes: the label prefix
    # already names the session and the agent, so the note is just the verb.
    note(f"{tag}reading the view")
    started = time.monotonic()
    try:
        proc = import_jobs.spawn_child(
            argv,
            cwd=str(workdir if workdir is not None else folder),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # one ordered stream, like the streaming path
            # NOT `text=True`, which encodes AND decodes with the LOCALE codec
            # in strict mode. Under `LC_ALL=C` that is ASCII, and a rendered
            # transcript view is routinely not ASCII -- so writing the prompt
            # raises `UnicodeEncodeError`, which is a `ValueError`, not a
            # `SubprocessError`, and takes the wizard down instead of failing
            # one digest. Pinned to utf-8 with replacement in both directions.
            encoding="utf-8",
            errors="replace",
            # The tail is read by people and stored in lane reports, and nothing
            # downstream strips ANSI. Ask pi not to emit it -- and pin
            # FORCE_COLOR too: an inherited FORCE_COLOR=1 overrides NO_COLOR
            # in node, bringing the escapes back PLUS a node warning line
            # about the conflict, merged into the tail. Verified on a real
            # machine carrying FORCE_COLOR=1 ambiently.
            env={**_backfill_agent_env(), "NO_COLOR": "1", "FORCE_COLOR": "0"},
            # ITS OWN PROCESS GROUP, for the reason `launch_agent` gives at
            # length: only a group can be killed as one.
            start_new_session=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, str(exc)
    if not _register_agent(proc, cancel_event):
        return False, "agent cancelled"

    try:
        stdout, _stderr = proc.communicate(input=prompt, timeout=bound)
    except subprocess.TimeoutExpired as exc:
        _kill_tree(proc)
        # NAME THE BOUND AND SHOW THE OUTPUT. "pi timed out" is unactionable:
        # the reader cannot tell a wedged binary from a deadline set too tight,
        # and whatever pi managed to say is usually the answer.
        partial = _pi_tail(exc.stdout, exc.stderr)
        return False, (
            f"pi did not finish within {bound:g}s"
            + (f" — last output: {partial}" if partial else ", and printed nothing")
        )
    except KeyboardInterrupt:
        # Same rule as the streaming path: the thread taking the interrupt must
        # not leave its siblings running.
        stop_all()
        raise
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        # `ValueError` is deliberate belt-and-braces on top of the pinned
        # encoding above: a codec failure out of `communicate` must fail ONE
        # digest, never the lane.
        _kill_tree(proc)
        return False, str(exc)
    finally:
        _release_agent(proc)

    ok = proc.returncode == 0
    note(f"{tag}{'finished' if ok else 'failed'} in {time.monotonic() - started:.1f}s")
    return ok, _pi_tail(stdout)


def launch_agent(
    folder: Path,
    prompt: str,
    *,
    agent: Agent = Agent.CLAUDE,
    workdir: Path | None = None,
    tools: str | None = None,
    model: str | None = None,
    heading: str = "",
    label: str = "",
    timeout: float | None = None,
    stream=None,
    raw_stream=None,
    progress: bool = True,
    total: int = 0,
    session_id: str | None = None,
    resume: str | None = None,
    paint_to=None,
    cancel_event: threading.Event | None = None,
) -> tuple[bool, str]:
    """Run one headless agent over `folder`, showing what it is doing.

    ONE self-updating line, not the transcript. A raw agent transcript is
    thousands of lines nobody reads, and the previous version showed neither --
    a bare `claude -p` emits nothing until it exits, so a long import was
    indistinguishable from a hang. What a watcher actually needs is that it is
    alive, roughly how far along it is, and what it is touching right now.

    `workdir` is the agent's scratch directory and the only place it may write;
    `folder` stays read-only. See CONFINEMENT.

    `tools` and `model` override the allowlist and the model for one launch --
    the digest lane's two, `DIGEST_TOOLS[agent]` and `DIGEST_MODEL[agent]`.
    Absent, the importer's launch is byte-for-byte what it always was.

    `timeout` is an IDLE DEADLINE for claude/codex: the longest this may go
    WITHOUT AN EVENT, not the longest it may run. That is what the numbers have
    always meant -- `backfill_run.UNIT_TIMEOUT_S`'s own docstring reads "a unit
    that has not produced an event in this long is wedged" -- and a wall clock
    in its place would kill a 46-minute import that was healthy the whole way.

    What it did NOT used to be is enforceable. It bounded only the `wait` AFTER
    stdout reached EOF, and `for line in proc.stdout` blocks forever on an
    agent that neither speaks nor exits, so `proc.wait(timeout=)` on the next
    line was never reached: the one case the deadline exists for was the one
    case it could not fire in. A single poller thread now compares the clock
    against the last event stamped by the read loop and kills the process group
    when the gap exceeds the bound. A wedged agent is bounded just as tightly
    as a wall clock would bound it -- it emits nothing, so its last event stays
    at launch -- and the caller gets `False` with a message naming the bound.

    pi keeps a true WALL CLOCK (`communicate(timeout=)`) for the reason the
    idle clock cannot apply to it: `--mode text` is not an event stream, so
    there is nothing to stamp. Its whole run is one bounded call.

    `None` still means unbounded, and costs no thread: a caller that wants a
    deadline says so.

    `raw_stream` is where the agent's VERBATIM stream-json goes under
    `progress=False`; it defaults to `stream`, which is what every existing
    caller wants. The digest lane sends it somewhere that keeps nothing: that
    JSON quotes the conversation being summarized, and echoing it to stdout
    made `probe backfill > import.log` a durable second copy of every session
    -- next to a digester that unlinks its rendered view for exactly that
    reason. Digests still print the two liveness lines (start, finish with
    elapsed) to `stream`, because an agent that says nothing for five minutes
    is indistinguishable from a hang.

    `heading` and `paint_to` decide where that line goes. Alone, the agent draws
    its OWN centred page -- title, blank row, live line -- because appended
    under whatever the picker left on screen it reads as a different program's
    output leaking into the wizard. `paint_to` hands the row to a caller running
    several agents at once, which owns the screen instead (see `tui.Board`).

    `cancel_event` closes the gap between cancelling a worker pool and a
    worker registering its child: a late spawn stops before reading stdout.

    `total` is the census, so the counter reads against the denominator the
    reconcile will check. The tail is returned so the caller can pull the
    agent's JSON summary out of it.
    """
    from . import import_jobs

    if cancel_event is not None and cancel_event.is_set():
        return False, "agent cancelled"
    binary = which_agent(agent)
    if not binary:
        name = AGENT_COPY[agent][0]
        # "another", not "the other": there are three now, and which alternatives
        # exist depends on which lane is asking.
        return False, f"`{agent.value}` is not on PATH — install {name}, or pick another agent"
    if workdir is not None and agent is Agent.CLAUDE and unruleable(folder):
        # Refusing beats running unconfined. The rule is the only thing keeping
        # the agent out of the folder, and an unparseable one denies nothing
        # while looking exactly like a working configuration.
        return False, (
            f"{folder} has a parenthesis in its path, which cannot be written as a "
            "Claude permission rule — the folder could not be protected from writes. "
            "Re-run with Codex, whose sandbox needs no path pattern."
        )

    out = stream if stream is not None else sys.stdout

    if agent is Agent.PI:
        return _run_pi(
            binary,
            folder,
            prompt,
            workdir=workdir,
            tools=tools,
            model=model,
            timeout=timeout,
            label=label,
            out=out,
            paint_to=paint_to,
            cancel_event=cancel_event,
        )

    # Defaults to `out`, so every caller that predates the split behaves
    # exactly as it did; only the digest lane sends it elsewhere.
    raw_out = raw_stream if raw_stream is not None else out

    live = progress and hasattr(out, "isatty") and out.isatty()
    state = Activity(total=total or 0)
    started = time.monotonic()
    tail: list[str] = []
    tag = f"{label} " if label else ""
    board = None

    def note(text: str) -> None:
        """The quiet run's two lines. Same shape and same destinations as
        `_run_pi`'s, because it is the same problem: with the stream silenced
        there is nothing else to prove the agent is alive."""
        if paint_to is not None:
            paint_to(text)
            return
        out.write(f"  {text}\n")
        out.flush()

    def paint() -> None:
        if not live:
            return
        text = state.line(time.monotonic() - started)
        if paint_to is not None:
            paint_to(text)
        elif board is not None:
            board.update(0, text)

    # One live screen component for both standalone and concurrent agents.
    # A caller-owned painter already has its board; opening another would
    # erase the other agents' rows.
    if live and paint_to is None:
        from probe.cli import tui

        board = tui.Board(heading, [""], out=out)
        board.open()

    stop = threading.Event()

    def tick() -> None:
        # The spinner has to advance on its own: an agent can think for a minute
        # between events, and a frozen spinner is the thing we set out to fix.
        while not stop.wait(0.12):
            state.ticks += 1
            paint()

    try:
        # THE PROMPT, as a file the child reads at its own pace. Not
        # `stdin=PIPE` + `proc.communicate()`: we hold stdout as a pipe and do
        # not start reading it until below, so a prompt past the pipe buffer
        # (64KB here, against prompts of 300KB) deadlocks -- we block writing
        # while the child blocks writing its event stream. An unnamed temp file
        # needs no writer, no thread, and no cleanup path: it is unlinked on
        # close, including when the exec fails.
        prompt_file = tempfile.TemporaryFile()
        prompt_file.write(prompt.encode("utf-8", "replace"))
        prompt_file.flush()
        prompt_file.seek(0)
    except OSError as exc:
        if board is not None:
            board.close(erase=True)
        return False, f"could not stage the prompt: {exc}"
    try:
        argv = agent_argv(
            agent,
            binary,
            folder,
            workdir=workdir,
            tools=tools,
            model=model,
            session_id=session_id,
            resume=resume,
        )
        if cancel_event is not None and cancel_event.is_set():
            if board is not None:
                board.close(erase=True)
            return False, "agent cancelled"
        proc = import_jobs.spawn_child(
            argv,
            cwd=str(workdir if workdir is not None else folder),
            stdin=prompt_file,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=_backfill_agent_env(),
            # ITS OWN PROCESS GROUP, so the whole tree can be killed at once.
            # An agent is not one process: it starts MCP servers, subagents and
            # shells of its own, and `proc.kill()` reaps only the direct child
            # -- leaving the grandchildren running, reading the folder, with no
            # parent left to stop them. That is what survived a Ctrl-C and kept
            # a 106,007-file import going after the wizard had said "Cancelled".
            start_new_session=True,
        )
    except (OSError, subprocess.SubprocessError, ArgvTooLargeError) as exc:
        if board is not None:
            board.close(erase=True)
        return False, str(exc)
    finally:
        # The child has its own dup of the fd from here on, so ours is done.
        # Closing it is also what unlinks the file on the failure path.
        prompt_file.close()
    if not _register_agent(proc, cancel_event):
        if board is not None:
            board.close(erase=True)
        return False, "agent cancelled"

    ticker = threading.Thread(target=tick, daemon=True)
    if live:
        ticker.start()

    # THE IDLE DEADLINE. See the `timeout` paragraph above: the bound is time
    # WITHOUT AN EVENT, so the read loop stamps `last_event` and this thread
    # only watches the gap. Killing the GROUP closes the pipe, which is what
    # ends a loop that would otherwise block forever.
    #
    # ONE POLLER on a fixed tick, never a timer re-armed per line: an agent
    # emits thousands of events over an import, and a thread per event is a
    # thread pool nobody asked for. The tick is the resolution of the deadline,
    # and a second's slack on a bound measured in minutes costs nothing.
    expired = threading.Event()
    stop_watch = threading.Event()
    watchdog = None
    last_event = time.monotonic()
    if timeout is not None:

        def _watch() -> None:
            while not stop_watch.wait(_WATCHDOG_TICK_S):
                if time.monotonic() - last_event > timeout:
                    expired.set()
                    _kill_tree(proc)
                    return

        watchdog = threading.Thread(target=_watch, daemon=True)
        watchdog.start()

    if not progress:
        # The label already names the work and the session; repeating the agent
        # after it reads as two subjects in one sentence.
        note(f"{tag}reading the view")

    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            # THE STAMP the idle deadline is measured from. Every line counts,
            # not only the ones `fold_event` finds interesting: an agent
            # emitting anything at all is an agent that has not wedged.
            last_event = time.monotonic()
            tail.append(line.rstrip("\n"))
            del tail[:-40]
            changed = fold_event(line, state)
            if not progress:
                # RAW TRANSCRIPT, and this has to be tested FIRST. Underneath
                # the `changed` branch it was unreachable for anything worth
                # reading: `fold_event` returns True for every tool call,
                # command and message, so `progress=False` handed back a
                # mangled hybrid -- counter lines where the interesting events
                # should have been, raw JSON only for the lines nobody wanted.
                #
                # `raw_out`, not `out`: this JSON quotes the conversation, and
                # the digest lane sends it to a sink that keeps nothing while
                # its status line still reaches the reader.
                raw_out.write(line)
                raw_out.flush()
            elif live:
                if changed:
                    paint()
            elif changed:
                # No TTY (a pipe, a CI log): one plain line per step. Rewriting
                # with \r into a log file produces an unreadable single line.
                #
                # `done`, not `uploaded`. The live line was moved onto files
                # READ when the upload counter turned out to be permanently
                # zero, and this branch -- the one a pipe, a CI log or `nohup`
                # takes -- was left behind counting the dead field. So the fix
                # was invisible to exactly the runs nobody is watching, which
                # are the runs that get read later to find out what happened.
                #
                # LABELLED, because there is no board out here. `run_units`
                # only builds one when interactive, so an unattended import
                # writes up to `concurrency` units into ONE stream -- and
                # without a name the only thing telling `3/704` from `5/704`
                # is a denominator two units can easily share.
                count = f"{state.done}/{state.total} · " if state.total else ""
                out.write(f"  {tag}{count}{state.doing}\n")
                out.flush()
        # UNBOUNDED ON PURPOSE, and only safe because of the poller above. EOF
        # is not exit: a process can close stdout and linger. That is silence,
        # which is exactly what the idle deadline measures -- the poller is
        # still armed here and kills the tree, which is what releases this
        # wait. A `timeout=` here as well would be a second deadline with
        # different semantics and its own message for the same condition.
        code = proc.wait()
    except KeyboardInterrupt:
        # Ctrl-C should stop the agent, not orphan it holding the folder.
        # EVERY agent, not just this one: under `run_units` there are several,
        # and one thread taking the interrupt must not leave its siblings
        # running -- see `stop_all`.
        stop_all()
        raise
    finally:
        # Always, and BEFORE anything else in here. An abandoned poller is a
        # live thread holding a reference to a reaped pid, and a lane of 200
        # digests would leave 200 of them; joined rather than merely signalled
        # so "the run is over" also means "nothing is still about to kill
        # something". The join is prompt -- `Event.wait` returns the moment the
        # event is set, it does not sit out the rest of its tick.
        stop_watch.set()
        if watchdog is not None:
            watchdog.join(timeout=5.0)
        _release_agent(proc)
        # Always: an abandoned ticker keeps repainting over whatever the wizard
        # prints next, and the status line must not outlive the run either way.
        stop.set()
        if live:
            ticker.join(timeout=1.0)
        if board is not None:
            board.close(erase=True)

    elapsed = time.monotonic() - started
    if expired.is_set():
        # NAME THE BOUND AND WHICH CLOCK RAN OUT. "did not finish within 300s"
        # would be false of a run that was talking the whole time and is
        # unactionable besides: what happened is SILENCE, and the fix for a
        # deadline set too tight differs from the fix for a wedged binary.
        # Whatever it managed to say before going quiet is usually the answer.
        partial = "\n".join(tail[-5:])
        if not progress:
            note(f"{tag}stopped after {timeout:g}s with no output")
        return False, (
            f"{AGENT_COPY[agent][0]} produced no output for {timeout:g}s and was stopped"
            + (f" — last output: {partial}" if partial else ", having printed nothing")
        )
    ok = code == 0
    if not progress:
        note(f"{tag}{'finished' if ok else 'failed'} in {elapsed:.1f}s")
    return ok, "\n".join(tail)


def _rows(payload) -> list | None:
    """The item list out of a bare list, a page dict, or a Page object.

    dict is tested BEFORE the attribute lookup: `dict.items` is a bound method,
    so a getattr-first version reads every page dict as "no rows" and quietly
    counts zero.
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        items = payload.get("items", payload)
    else:
        items = getattr(payload, "items", None)
    return items if isinstance(items, list) else None


def _project_id(client, project: str) -> str | None:
    """`project` as a UUID. A bare ref is a SLUG; ids arrive as `id:<uuid>`.

    ``/v1/projects/{project_id}/artifacts`` types its path param as a UUID, so a
    slug arrives as a 422 about UUID parsing rather than a lookup -- the same
    trap :func:`resolve_anchor` documents. It matters here because the slugs come
    from :func:`summary_projects`, i.e. the read-back is fed the one form the
    route cannot take, and the 422 is swallowed as "could not read back".
    """
    from . import refs

    try:
        # verify=False: this is a READ-BACK, so an `id:` ref needs no round trip
        # to confirm what it already states, and one fewer request per project.
        return refs.resolve(client, "project", project, verify=False).id
    except Exception:  # noqa: BLE001 - a read-back miss degrades, never raises here
        return None


def count_landed(client, project: str) -> tuple[int, bool]:
    """Artifacts under a project, INCLUDING its experiments. (count, at_least).

    Counting only the project anchor would undercount every import that did what
    it was told: step 3 of the prompt asks the agent to attach artifacts to an
    experiment where the evidence supports one, and an experiment-anchored
    artifact is not returned by the project listing. A faithful 204-file import
    that grouped 83 of them read back as 121, printing a 40% shortfall that was
    entirely an artifact of where the reconcile looked.

    One page per anchor, deliberately. Walking every page of a 12,000-artifact
    project to print one number would make the cheap half of this feature the
    slow half; hitting the page exactly reports "at least", which is honest,
    instead of a total that is quietly a page size.

    The experiment reads run CONCURRENTLY. Serially this was an N+1 -- one
    round trip per experiment, after the one for the project -- and a project
    with fifty experiments spent fifty sequential round trips producing a
    single number at the very end of an import someone is already waiting on.
    They are independent reads of independent anchors, so nothing is ordered
    between them and the only reason it was a loop is that it was written as
    one.
    """
    from concurrent.futures import ThreadPoolExecutor

    from probe.sdk.client import Anchor

    try:
        project_id = _project_id(client, project)
        if project_id is None:
            return -1, False
        counted = _rows(client.list_anchored(Anchor.PROJECT, project_id, limit=RECONCILE_PAGE))
        if counted is None:
            return -1, False
        total = len(counted)
        at_least = total >= RECONCILE_PAGE

        experiments = _rows(client.list_experiments(project_id=project_id))
        exp_ids = []
        for exp in experiments or []:
            exp_id = exp.get("id") if isinstance(exp, dict) else getattr(exp, "id", None)
            if exp_id:
                exp_ids.append(str(exp_id))
        if not exp_ids:
            return total, at_least

        def page(exp_id: str):
            return _rows(client.list_anchored(Anchor.EXPERIMENT, exp_id, limit=RECONCILE_PAGE))

        # Bounded: a project with hundreds of experiments must not open
        # hundreds of sockets to print one number.
        with ThreadPoolExecutor(max_workers=min(8, len(exp_ids))) as pool:
            for rows in pool.map(page, exp_ids):
                if rows is None:
                    # One unreadable anchor makes the WHOLE count unknown rather
                    # than silently short: reporting a shortfall that is really a
                    # failed lookup trains people to ignore the one number this
                    # feature exists for.
                    return -1, False
                total += len(rows)
                at_least = at_least or len(rows) >= RECONCILE_PAGE
        return total, at_least
    except Exception:  # noqa: BLE001 - reconcile must never fail the import
        return -1, False


def _embedded_summaries(text: str, key: str = "projects"):
    """Every ``{...}`` in `text` that parses and carries a list under `key`.

    `key` exists because the chunked classification asks for three different
    shapes -- a survey, a project list, a slice of assignments -- and each has
    to be told apart from the others in the same stream. Defaulting to
    ``projects`` keeps every existing caller reading the same thing.

    The summary does not arrive on a line of its own. Both agents are run with
    an EVENT STREAM (`agent_argv`), so the closing JSON is a STRING INSIDE an
    envelope -- `{"type":"result","result":"...done.\\n{...}"}` -- and the
    braces of the two are nested in one line of stdout. Scanning for balanced
    brace runs finds the inner object wherever it sits; matching only the whole
    line finds it exactly when the agent is NOT streaming, which is never.
    """
    import json

    def scan(blob: str):
        depth = 0
        start = -1
        for i, ch in enumerate(blob):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}" and depth:
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        data = json.loads(blob[start : i + 1])
                    except ValueError:
                        continue
                    if isinstance(data, dict) and isinstance(data.get(key), list):
                        yield data

    def strings(node):
        """Every string anywhere in a decoded envelope."""
        if isinstance(node, str):
            yield node
        elif isinstance(node, dict):
            for value in node.values():
                yield from strings(value)
        elif isinstance(node, list):
            for value in node:
                yield from strings(value)

    yield from scan(text)
    # The inner object is a STRING FIELD of the envelope, so in the raw line its
    # quotes are backslash-escaped and no substring of it parses. It only becomes
    # JSON again once the envelope itself is decoded — hence the second pass over
    # the decoded strings rather than more clever matching on the raw text.
    try:
        envelope = json.loads(text)
    except ValueError:
        return
    for blob in strings(envelope):
        if key in blob:
            yield from scan(blob)


def summary_projects(tail: str) -> list[str]:
    """The project slugs the agent says it filed into.

    Parsed from its closing JSON summary. This is the ONLY thing taken from the
    agent's own account of the run, and deliberately the least load-bearing one:
    it says WHERE to look, never how much landed. The count still comes from the
    server and the denominator still comes from the walk, so an agent that
    overstates its work cannot make the numbers agree — the gap just shows up.

    It says where to look, but nothing looks anywhere if this returns empty:
    with no pinned `--project` there is no fallback, so a parse miss here
    silently downgrades the whole run to "could not read back". That is what a
    top-level-only match did -- see :func:`_embedded_summaries`.
    """
    found: list[str] = []
    for line in reversed(tail.splitlines()):
        text = line.strip()
        if "projects" not in text:
            continue
        for data in _embedded_summaries(text):
            for slug in data["projects"]:
                if isinstance(slug, str) and slug and slug not in found:
                    found.append(slug)
        if found:
            return found
    return found


def count_landed_across(client, projects: list[str]) -> tuple[int, bool]:
    """Artifacts across every project the agent used. Returns (count, at_least).

    A project that cannot be read counts as unknown for the whole reconcile
    rather than silently zero: reporting a shortfall that is really a failed
    lookup would train people to ignore the one number this feature exists for.
    """
    if not projects:
        return -1, False
    total = 0
    at_least = False
    for slug in projects:
        count, capped = count_landed(client, slug)
        if count < 0:
            return -1, False
        total += count
        at_least = at_least or capped
    return total, at_least


def reconcile(census: Census, landed: int, at_least: bool) -> list[str]:
    """The denominator, printed. The whole point of enumerating first."""
    found = f"{census.files:,}"
    if landed < 0:
        return [f"{found} files found — could not read back the project to confirm what landed."]
    shown = f"{landed:,}{'+' if at_least else ''}"
    lines = [f"{found} files found on disk · {shown} artifacts now on the project."]
    # UNCONDITIONAL now, bar the one honest exclusion. `census.capped` used to
    # gate this too, which meant the shortfall warning switched itself off on
    # exactly the folders big enough to need it. The census is never capped.
    if not at_least and landed < census.files:
        lines.append(
            f"{census.files - landed:,} unaccounted for — build noise and caches are "
            "expected here; re-run to pick up anything genuinely missed."
        )
    return lines


# -- the folder picker ------------------------------------------------------


def choose_directory(start: Path):
    """Browse to the folder to import. Returns a Path, None (quit), or tui.BACK.

    THIS SCREEN DOES NOT WALK THE TREE. It reads one directory, one level deep,
    and draws. It used to census the folder you were standing in before it could
    render a single row -- a full recursive stat walk, capped at 20,000 files,
    paid again on every `cd`, and `../` paid it on a bigger tree. On a research
    drive that is minutes of blank terminal to produce a label reading
    "20,000+ files", which is barely a signal and cost the whole screen.

    What that label was for -- not pointing an importer at 2.9 TB unawares --
    is answered better and later: the import's own walk reports a live count as
    it runs, and it runs before anything is written or any agent starts, so
    Ctrl-C there costs walk time and nothing else.
    """
    from .directory_picker import DirectoryPicker

    return DirectoryPicker(start, subdirectories).run()


# -- the wizard action ------------------------------------------------------


def choose_agent(available: list[Agent], *, selected: Agent | None = None):
    """Pick the agent. Returns an Agent, None (quit), or tui.BACK.

    Only ever reached with a real choice to make -- `resolve_agent` answers it
    without asking when one agent is installed, which is the common case.
    """
    import questionary

    from probe.cli import tui

    choices: list = [questionary.Separator(" ")]
    for index, agent in enumerate(available):
        if index:
            choices.append(questionary.Separator(" "))
        choices.append(questionary.Choice(title=AGENT_COPY[agent][0], value=agent))

    message = tui.framed(
        # Count-aware because a third agent can be installed; the importer
        # only ever reaches this with two, so its screen is unchanged.
        "Both agents are installed here."
        if len(available) == 2
        else f"{len(available)} coding agents are installed here.",
        tui.wrap("Choose the coding agent that will read this folder and import its contents."),
        "Which agent should read it?",
    )
    return tui.ask(
        tui.select(
            message,
            choices=choices,
            instruction="(arrow keys, enter to choose, esc goes back)",
            **({"default": selected} if selected in available else {}),
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )


def resolve_agent(
    requested: Agent | None, *, interactive: bool, chooser=None
) -> tuple[object, str | None]:
    """Which agent runs, as ``(choice, error)``.

    A TUPLE rather than a union return, because `Agent` is a `StrEnum` and
    therefore IS a str: an `isinstance(result, str)` check meant to catch the
    error case swallows every successful one too, and `run` then returns the
    enum where the caller expected output lines. Separate slots cannot be
    confused that way.

    `choice` is an Agent, None (quit), or tui.BACK. An explicit `--agent` wins
    and is NOT silently downgraded when that agent is missing: someone who named
    one wants that one, and quietly running the other over their filesystem is
    the wrong kind of helpful.
    """
    from probe.cli import tui

    if requested is not None:
        if requested not in IMPORTER_AGENTS:
            # `--agent pi` reaches here because the enum parses it. Running it
            # would be the module's own failure mode: pi's allowlist has no
            # shell, so every `probe artifact add` the import depends on has
            # nowhere to run and the folder reads back as imported and empty.
            return None, (
                f"`{requested.value}` cannot run a folder import — its tool allowlist has no "
                f"shell, and the import files what it finds through the probe CLI. Use "
                f"{' or '.join(a.value for a in IMPORTER_AGENTS)}."
            )
        binary = which_agent(requested)
        if binary is None:
            name = AGENT_COPY[requested][0]
            return None, (
                f"`{requested.value}` is not on PATH — install {name}, or drop --agent to pick."
            )
        # BEFORE THE WALK. On PATH is not the same as able to run this, and
        # finding out afterwards costs the whole traversal -- then repeats the
        # same message once per slice. See `too_old`.
        stale = too_old(requested, binary)
        if stale:
            return None, stale
        return requested, None

    available = available_agents()
    if not available:
        return None, (
            "No coding agent found. Backfill needs Claude Code or Codex on PATH — "
            "the agent is what reads the folder."
        )
    # An agent too old to run the import is not a choice worth offering. If
    # that leaves nothing, say WHY rather than "no coding agent found" -- the
    # binary is right there on PATH and a reader who is told it is absent will
    # go and install what they already have.
    usable = [a for a in available if too_old(a, which_agent(a) or "") is None]
    if not usable:
        reasons = [too_old(a, which_agent(a) or "") for a in available]
        return None, " ".join(r for r in reasons if r)
    if len(usable) == 1 or not interactive:
        return usable[0], None
    tui.clear()
    return (chooser or choose_agent)(usable), None


class FolderImportMode(StrEnum):
    REVIEW_FIRST = "review_first"
    AUTOMATIC = "automatic"


class StartedFolderImport(list[str]):
    """Report lines plus proof that a resumable folder job was registered."""

    def __init__(self, job: dict, lines):
        super().__init__(lines)
        self.job = job

    @classmethod
    def status_unavailable(cls, job: dict, error: Exception):
        return cls(
            job,
            [
                f"Folder import was saved, but its status is unavailable ({type(error).__name__}).",
                "Open Existing imports to view its progress or resume it.",
            ],
        )


def _unstarted_import(lines):
    """Keep an unregistered attempt visible until retried, skipped, or backed out."""
    from . import tui

    action = tui.review(
        "Folder import did not start",
        lines or ["No files were queued for import."],
        [("Retry", "retry"), ("Skip folder", tui.SKIP), ("Back", tui.BACK)],
    )
    if action is None:
        raise KeyboardInterrupt
    return action


def choose_import_mode(folder: Path, agent: Agent, *, wandb_source=None):
    """Offer automatic planning only as an explicit alternative to review."""
    from . import tui

    if wandb_source is not None:
        return tui.review(
            "Import files and W&B history",
            [
                f"Folder: {folder}",
                f"W&B project: {wandb_source['external_id']}",
                "Automatic import runs in the background without file review.",
                "Choose one Probe project for both files and W&B history next.",
            ],
            [
                ("Review the plan first", FolderImportMode.REVIEW_FIRST),
                ("Scan and import in background", FolderImportMode.AUTOMATIC),
                ("Skip folder", tui.SKIP),
            ],
        )

    return tui.review(
        "Import this folder",
        [
            f"Folder: {folder}",
            f"{AGENT_COPY[agent][0]} will scan the files and propose an import plan.",
            "Review it first, or let Probe apply the resulting plan and upload",
            "the files automatically in the background.",
        ],
        [
            ("Review the plan first", FolderImportMode.REVIEW_FIRST),
            ("Scan and import in background", FolderImportMode.AUTOMATIC),
            ("Skip folder", tui.SKIP),
        ],
    )


def choose_folder_wandb(client_factory, *, default=None):
    """Offer a connected W&B source before scanning; no destination is approved."""
    from . import backfill_wandb, tui

    while True:
        try:
            with client_factory() as client:
                with tui.working("Checking W&B connection"):
                    accounts = backfill_wandb.eligible_connections(client)
                if not accounts:
                    return None, False
                return backfill_wandb.choose_source(
                    client, accounts=accounts, default=default
                ), True
        except Exception as exc:
            action = tui.review(
                "W&B connection unavailable",
                [
                    f"Could not check connected W&B accounts ({type(exc).__name__}).",
                    "Retry the W&B check or continue with files.",
                ],
                [("Retry", "retry"), ("Continue with files", "files"), ("Back", tui.BACK)],
                default="files",
            )
            if action is None:
                raise KeyboardInterrupt
            if action == "retry":
                continue
            return (tui.BACK if action is tui.BACK else None), True


def run(
    *,
    client_factory,
    start: Path | None = None,
    folder: Path | None = None,
    project: str | None = None,
    interactive: bool = True,
    agent: Agent | None = None,
    yes: bool = False,
    concurrency: int | None = None,
    telemetry: "TelemetryContext | None" = None,
    transcripts: bool = False,
    transcripts_budget: int | None = None,
    source_id: str | None = None,
    import_changed: bool = False,
    import_unverified: bool = False,
    retry_dead: bool = False,
    background: bool = False,
    back_to_selection: bool = False,
):
    """The `Import existing work` action. Returns the lines the wizard pages,
    or None for a pure back-out -- the wizard loop's signal to skip the result
    page, the press-enter pause, and the per-agent state re-read.

    With ``back_to_selection``, Back revisits the previous visible form and
    returns ``tui.BACK`` from the first one; Skip still advances with None.
    Interactive background attempts that do not register a job ask for Retry,
    Skip, or Back here, before their caller can finish onboarding.

    Delegates to :func:`probe.cli.backfill_run.execute`, which is the two-pass
    flow: classify once over evidence, review, then import in resumable units.
    This function is the door -- the picker, the agent choice, and the shape the
    wizard expects back.

    `folder` skips the picker and `agent` skips the agent prompt, which is what
    makes this reachable from `--action backfill` on a box with no TTY. `yes`
    accepts the classification without review. Interactive background imports
    offer review first by default, with an explicit automatic-plan alternative.
    """
    from probe.cli import backfill_run, tui

    target = folder
    picker_start = start or Path.cwd()
    previous_agent = None
    mode_only = False
    retry_mode = None
    resolve_outcome = interactive and background and back_to_selection
    wandb_choices = {}
    wandb_shown = {}
    wandb_approvals = {}
    revisit_wandb = False
    while True:
        if target is None:
            if not interactive:
                return ["Backfill needs a folder. Re-run interactively, or pass --folder."]
            picked = choose_directory(picker_start)
            if picked is None:
                raise KeyboardInterrupt  # quit the installer, not just this import
            if picked is tui.BACK and back_to_selection:
                return tui.BACK
            if picked is tui.BACK or picked is tui.SKIP:
                return None  # backed out: nothing happened, nothing to pause on
            target = picked

        target = Path(target).resolve()
        if not target.is_dir():
            lines = [f"{target} is not a directory."]
            if not resolve_outcome:
                return lines
            action = _unstarted_import(lines)
            if action == "retry":
                continue
            if action is tui.SKIP:
                return None
            if folder is not None:
                return tui.BACK
            target = None
            mode_only = False
            retry_mode = None
            continue
        picker_start = target
        if interactive and not yes and (target not in wandb_choices or revisit_wandb):
            pending, shown = choose_folder_wandb(client_factory, default=wandb_choices.get(target))
            revisit_wandb = False
            if pending is tui.BACK:
                if folder is not None:
                    return tui.BACK if back_to_selection else None
                revisit_wandb = True
                target = None
                continue
            if wandb_choices.get(target) != pending:
                wandb_approvals.pop(target, None)
            wandb_choices[target] = pending
            wandb_shown[target] = shown
        if not mode_only:
            agent_screen_shown = False

            def pick_agent(available):
                nonlocal agent_screen_shown
                agent_screen_shown = True
                return (
                    choose_agent(available, selected=previous_agent)
                    if previous_agent is not None
                    else choose_agent(available)
                )

            chosen, agent_error = resolve_agent(
                agent,
                interactive=interactive,
                **({"chooser": pick_agent} if back_to_selection else {}),
            )
            if agent_error:
                if not resolve_outcome:
                    return [agent_error]
                action = _unstarted_import([agent_error])
                if action == "retry":
                    continue
                if action is tui.SKIP:
                    return None
                if wandb_shown.get(target):
                    revisit_wandb = True
                    continue
                if folder is not None:
                    return tui.BACK
                target = None
                continue
            if chosen is None and back_to_selection:
                raise KeyboardInterrupt
            if chosen is tui.BACK and back_to_selection:
                if wandb_shown.get(target):
                    revisit_wandb = True
                    continue
                if folder is None:
                    target = None
                    continue
                return tui.BACK
            if chosen is None or chosen is tui.BACK:
                return None
            previous_agent = chosen

        mode_only = False

        if interactive and background and not yes:
            mode = retry_mode or choose_import_mode(
                target,
                chosen,
                **({"wandb_source": wandb_choices[target]} if wandb_choices.get(target) else {}),
            )
            retry_mode = None
            if mode is None:
                raise KeyboardInterrupt
            if mode is tui.BACK and back_to_selection:
                wandb_approvals.pop(target, None)
                if agent_screen_shown:
                    continue
                if wandb_shown.get(target):
                    revisit_wandb = True
                    continue
                if folder is None:
                    target = None
                    continue
                return tui.BACK
            if mode is tui.BACK or mode is tui.SKIP:
                return None
            if mode == FolderImportMode.AUTOMATIC:
                from . import backfill_import, backfill_wandb, import_jobs_ui
                from .backfill_coverage import CoverageError
                from .import_job_messages import enqueue_report

                try:
                    if wandb_choices.get(target) and target not in wandb_approvals:
                        with client_factory() as client:
                            approval = backfill_wandb.choose_automatic_destination(
                                client,
                                folder=target,
                                wandb_source=wandb_choices[target],
                                project=project,
                            )
                            if approval is tui.BACK:
                                mode_only = True
                                continue
                            if approval is None:
                                wandb_choices[target] = None
                            else:
                                wandb_approvals[target] = approval
                    job = backfill_import.enqueue_auto_import(
                        client_factory=client_factory,
                        folder=target,
                        agent=chosen,
                        auto_approve=True,
                        project=project,
                        concurrency=concurrency,
                        source_id=source_id,
                        import_changed=import_changed,
                        import_unverified=import_unverified,
                        retry_dead=retry_dead,
                        **(
                            {"wandb_approval": wandb_approvals[target]}
                            if target in wandb_approvals
                            else {}
                        ),
                    )
                except CoverageError as exc:
                    lines = [f"Folder import could not start: {exc}"]
                except Exception as exc:
                    lines = [
                        f"Folder import could not start ({type(exc).__name__}).",
                        "Check Existing imports before trying again.",
                    ]
                else:
                    registered_job = job
                    try:
                        job = import_jobs_ui.show_started_import(job)
                        lines = StartedFolderImport(job, enqueue_report(job, "Folder import"))
                        if transcripts:
                            from . import backfill_transcripts

                            with client_factory() as client:
                                lines.extend(
                                    backfill_transcripts.run_lane(
                                        client=client,
                                        interactive=True,
                                        background=True,
                                        budget_bytes=transcripts_budget,
                                    )
                                )
                        return lines
                    except Exception as exc:
                        return StartedFolderImport.status_unavailable(registered_job, exc)
                if not resolve_outcome:
                    return lines
                action = _unstarted_import(lines)
                if action is tui.SKIP:
                    return None
                mode_only = True
                if action == "retry":
                    retry_mode = FolderImportMode.AUTOMATIC
                else:
                    wandb_approvals.pop(target, None)
                continue

        result = backfill_run.execute(
            client_factory=client_factory,
            folder=target,
            agent=chosen,
            project=project,
            interactive=interactive,
            yes=yes,
            concurrency=concurrency,
            telemetry=telemetry,
            transcripts=transcripts,
            transcripts_budget=transcripts_budget,
            source_id=source_id,
            import_changed=import_changed,
            import_unverified=import_unverified,
            retry_dead=retry_dead,
            background=background,
            **(
                {"wandb_source": wandb_choices[target], "offer_wandb": False}
                if target in wandb_choices
                else {}
            ),
            **({"back_to_selection": True} if back_to_selection else {}),
        )

        if result is tui.BACK and back_to_selection:
            if interactive and background and not yes:
                mode_only = True
                continue
            if agent_screen_shown:
                continue
            if folder is None and interactive:
                target = None
                continue
            return tui.BACK
        if resolve_outcome and result is not None and not isinstance(result, StartedFolderImport):
            action = _unstarted_import(result)
            if action is tui.SKIP:
                return None
            if action == "retry":
                mode_only = True
                retry_mode = FolderImportMode.REVIEW_FIRST
                continue
            if interactive and background and not yes:
                mode_only = True
                continue
            if agent_screen_shown:
                continue
            if folder is None:
                target = None
                continue
            return tui.BACK
        return result
