"""CLI workspace onboarding: init / join / refresh (auth P4, PF-350, §5.2).

These are the client half of onboarding — the pixelfuel-claude ``onboard-project``
skill moved into InnoDay. The server (``GET /api/v1/onboarding/resolve``)
resolves the org/project by alias and lists the repos; the CLI then runs the
local onboard/refresh algorithm below (the CLI has no DB access).

  innoday init <org>/<proj>   onboard by alias; if the target workspace already
                              has .innoday/project.yml it REFRESHES in place
  innoday join <org>[/<proj>] join an org (POST .../join) then onboard, in one step
  innoday refresh             re-onboard the CURRENT project (cwd's project.yml)

## The onboard/refresh algorithm (one definition, used by all three)

Given a resolved (org, project, github_topic, repos) and a target workspace:

  1. DETECT MODE — `<ws>/.innoday/project.yml` exists → REFRESH, else FRESH.
  2. ARCHIVE — before overwriting, copy the existing `project.yml` and workspace
     `CLAUDE.md` to `<ws>/.innoday/archive/<name>.<UTC-timestamp>`; prune archive
     entries older than 30 days. (No-op on FRESH.)
  3. RECONCILE REPOS —
       * every resolved repo: `git clone` if absent, else `git pull --ff-only`;
       * every repo listed in the OLD project.yml but NOT in the resolved set:
         `mv <ws>/<repo>` → `<ws>/archived/<repo>` (archived, not deleted).
  4. REGENERATE `project.yml` — fully rewritten from resolved state, preserving
     only blastoff-owned `release_configs` version fields from the old file.
  5. REGENERATE workspace `CLAUDE.md` — a fresh, regeneratable context header.

`refresh` is `init` with the mode forced to the cwd's existing project; `init`
run inside an already-onboarded workspace naturally hits the REFRESH branch.
"""

import argparse
import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Tuple

import yaml
from rich.console import Console

from src.cli.client import InnoDayAPIClient
from src.cli.config import CLIConfig
from src.cli.utils.formatters import format_error, format_success, format_warning
from src.cli.utils.project_context import PROJECT_YML_SCHEMA_VERSION, find_project_yml
from src.version import get_display_version

console = Console()

# release_configs fields owned by blastoff — preserved verbatim across a refresh
# (only `blastoff release`/`hotfix` should ever change them). Everything else in
# the file is regenerated from resolved state each run.
_BLASTOFF_OWNED_FIELDS = {
    "next_version",
    "prerelease",
    "last_released",
    "last_released_version",
    "last_hotfix",
    "hotfix_mode",
}
_ARCHIVE_RETENTION_DAYS = 30

# Version of the GENERATED half of the workspace CLAUDE.md. Bump this whenever
# the template below changes in a way worth propagating.
#
# It gates the push in `POST /onboarding/context`: the server keeps the highest
# version it has been given, so a colleague still on an older CLI cannot
# overwrite a newer generation with their older template's output. Deliberately
# an integer and NOT the CLI's own version -- `get_display_version()` moves for
# reasons unrelated to this file, and ordering `0.83.0-beta` against a dev build
# is exactly the kind of comparison that quietly gets it wrong.
CONTEXT_TEMPLATE_VERSION = 2

#: Where a refresh drops the timeline snapshot, relative to the workspace.
TIMELINE_SNAPSHOT_PATH = Path(".innoday") / "timeline.md"

# Standard development-workflow block included verbatim in EVERY generated
# workspace CLAUDE.md. Without it, an agent landing in a freshly-onboarded
# workspace has no instruction to route work through InnoDay, so it edits main
# directly and skips ticket/PR/worktree tracking. Inline string constant (not a
# packaged data file) to stay wheel-safe for the uvx-installed MCP server, the
# same convention as _PRE_COMMIT_HOOK. Deliberately short — a long block gets
# skimmed, and every line here is load-bearing.
_DEV_WORKFLOW_STANDARD = """## Development workflow (standard — applies to every repo here)

**When asked to do any development work — a feature, a bug fix, an issue — use
the InnoDay build-rockets skill (`/pixelfuel:build-rockets`), not direct edits.**
It applies the required InnoDay, git, and agent procedures for you:

- **Never code on `main`** — build-rockets creates a git worktree and a branch
- **Every change ships via PR** — never push to `main` directly
- **Work is tracked** — the InnoDay ticket and GitHub issue are linked and updated
- **Review before merge** — multi-agent review runs on the diff

Related: `/pixelfuel:design-rocket` to plan/scope a feature first,
`/pixelfuel:parallel-dev` for several independent tasks at once.
Ticket context: `innoday tickets list` · `innoday status`."""


# Included verbatim in EVERY generated workspace CLAUDE.md, for the same reason
# as _DEV_WORKFLOW_STANDARD: an agent landing in a freshly-onboarded workspace
# has no instruction about who it is talking to, and defaults to explaining work
# the way it explains it to itself. The person reading is usually the one who
# decided WHAT should happen and does not read this codebase — a summary written
# in file paths and function names tells them nothing they can act on, and asks
# them to translate before they can answer. Both halves below were written after
# exactly that failure. Deliberately short: a long block gets skimmed.
_COLLABORATION_STANDARD = """## How to explain your work here

**Write for someone who knows what the product should do, not how the code
works.** They chose the outcome; they should not have to read the codebase to
find out whether you delivered it.

- **Lead with what changed for a person using it** — then the reason, then the
  detail if it is still needed. Not the reverse.
- **Say the intention, not the mechanism.** "Taking a ticket would have looked
  like it worked and then quietly undone itself" beats naming the columns and
  the sync that overwrites them.
- **Go step by step** when something is not obvious. One idea per step, in the
  order it happens.
- **No file paths, function names, or line numbers in an explanation** unless
  asked for them, or unless you are pointing someone at where to look next.
- **Say plainly what is not done, what you skipped, and what you are unsure
  of.** A confident summary that omits a gap is worse than no summary.
- **Never imply a decision was approved when it was not.** If a choice is still
  open, say it is open and say what you would pick.

## How to break coding work up

- **Smallest change that solves the problem.** No speculative abstraction, no
  unrequested refactor riding along.
- **Reuse before building.** Check for an existing model, service, adapter or
  helper first — this codebase has repeatedly grown a second copy of something
  that already existed. If you must add a new one, say what you looked at and
  why it did not fit.
- **Break work into pieces that each stand on their own.** Prefer several small
  PRs, each shippable and reviewable alone, over one large one. A piece that
  only makes sense alongside the next piece is a sign the split is wrong.
- **Follow the repo's conventions over general best practice**, and its README
  over the general guide.
- **Ask when two readings of the request would produce materially different
  work.** Make the ordinary judgement calls yourself."""


# ---------------------------------------------------------------------------
# Carrying hand-written CLAUDE.md content across a regeneration
#
# The workspace CLAUDE.md is regenerated on every init/refresh, which used to
# mean anything a human or agent added to it was silently destroyed — the file
# says "do not hand-edit", but people reasonably do, because it is the file
# Claude Code loads for the workspace. One refresh of six workspaces discarded
# worktree policies, onboarding gotchas, and deploy notes; the archive copy
# under .innoday/archive/ was the only reason none of it was lost for good.
#
# So the file is now split in two. Everything above the sentinel is generated
# and rewritten each run. Everything below it is yours and copied through
# verbatim. Nothing about the generated half changes.
#
# Files written before the sentinel existed have no marker to split on, so they
# get a one-time salvage instead: every `## ` section whose heading the
# generator does not own is treated as hand-written and carried below the
# sentinel. That runs once — the next refresh finds the sentinel and takes the
# cheap path.
# ---------------------------------------------------------------------------

CUSTOM_SECTION_SENTINEL = "<!-- innoday:end-generated -->"

# The explanatory comment sits ABOVE the sentinel deliberately: the split is on
# the sentinel, so anything below it is user content and gets copied verbatim.
# Putting the comment below would re-emit it on every refresh and stack copies.
_CUSTOM_SECTION_HEADER = f"""<!-- Everything BELOW the next line is yours. `innoday refresh` regenerates
     everything above it and copies your part through untouched, so workspace
     notes, policies, and gotchas belong down there. Keep the marker intact. -->
{CUSTOM_SECTION_SENTINEL}"""

# Normalised `## ` headings the generator emits. A section keyed by any of these
# is generated content and must NOT be salvaged, or each refresh would stack a
# duplicate copy below the sentinel.
_GENERATED_HEADING_KEYS = frozenset(
    {
        "repositories",
        "recent activity",
        "working here",
        "development workflow",
        "how to explain your work here",
        "how to break coding work up",
    }
)


def _heading_key(line: str) -> str:
    """Normalise a markdown heading for comparison.

    Drops the leading hashes and any parenthetical suffix, so
    ``## Repositories (7)`` and ``## Repositories (0)`` are the same section.
    """
    text = line.lstrip("#").strip()
    return text.split(" (")[0].strip().lower()


def _salvage_legacy_sections(existing: str) -> str:
    """Pull hand-written `## ` sections out of a pre-sentinel CLAUDE.md.

    Content before the first `## ` is dropped: that is the generated preamble
    (title, org/project identity, the do-not-hand-edit note), all of which the
    generator re-emits. Only whole sections whose heading the generator does not
    own survive.
    """
    lines = existing.splitlines()
    kept: List[str] = []
    keeping = False

    for line in lines:
        if line.startswith("## "):
            keeping = _heading_key(line) not in _GENERATED_HEADING_KEYS
        elif line.startswith("# ") and not line.startswith("## "):
            # A new H1 ends any section we were keeping.
            keeping = False
        if keeping:
            kept.append(line)

    return "\n".join(kept).strip("\n")


def _extract_custom_content(claude_path: Path) -> str:
    """Return the hand-written portion of an existing CLAUDE.md, or ""."""
    try:
        existing = claude_path.read_text()
    except (OSError, UnicodeDecodeError):
        # Unreadable means we cannot prove there is nothing to keep. Returning
        # "" here would let a regeneration quietly drop it, so treat it as empty
        # only after the archive copy has already been taken (it has — archiving
        # is step 2, this runs in step 5).
        return ""

    if CUSTOM_SECTION_SENTINEL in existing:
        return existing.split(CUSTOM_SECTION_SENTINEL, 1)[1].strip("\n")
    return _salvage_legacy_sections(existing)


# ---------------------------------------------------------------------------
# Merging hand-written notes across machines
#
# The hand-written tail is stored on the project as well as in the file, so it
# survives a re-clone or a new laptop. That makes two copies, which can differ,
# so a refresh has to decide what the file becomes.
#
# It is a UNION, keyed on the section heading, local order first. The reasoning:
# a note only exists because somebody wrote it, and a refresh is a routine,
# repeatable, sometimes unattended operation. An unattended job that can delete
# prose is the wrong trade, so the merge never drops a section it has not been
# explicitly told to drop.
#
# Same heading on both sides -> LOCAL wins. The local file is the copy someone
# edited most recently on this machine, and re-rendering it from the server
# would silently revert an edit made seconds earlier.
#
# The consequence, stated plainly because it will surprise someone: deleting a
# section by editing CLAUDE.md does not stick. The next refresh finds it still
# on the server and appends it back. `--replace-context` is the way to actually
# delete -- it sends the local tail verbatim as the new server value.
# ---------------------------------------------------------------------------


def _split_blocks(text: str) -> List[Tuple[str, str]]:
    """Split hand-written content into (key, block) pairs.

    Blocks are `## `/`# ` sections. Anything before the first heading is one
    block keyed `""` -- freeform notes with no heading are common and must not
    be silently dropped just because they are unstructured.
    """
    lines = (text or "").strip("\n").splitlines()
    if not lines:
        return []
    blocks: List[Tuple[str, str]] = []
    key = ""
    buf: List[str] = []
    for line in lines:
        if line.startswith("#"):
            stripped = line.lstrip("#")
            # A heading is `#` followed by a space. `#!/usr/bin/env` or a `#`
            # inside content is not a section break.
            if stripped.startswith(" "):
                if buf:
                    blocks.append((key, "\n".join(buf).strip("\n")))
                key = _heading_key(line)
                buf = [line]
                continue
        buf.append(line)
    if buf:
        blocks.append((key, "\n".join(buf).strip("\n")))
    return [(k, b) for k, b in blocks if b.strip()]


def _union_custom_content(local: str, remote: str) -> str:
    """Local blocks in local order, then remote blocks local does not have."""
    local_blocks = _split_blocks(local)
    remote_blocks = _split_blocks(remote)

    seen = {k for k, _ in local_blocks}
    merged = [b for _, b in local_blocks]
    # A headingless remote block (key "") is only appended when local has no
    # headingless block of its own -- otherwise two unrelated preambles stack
    # up a little more on every refresh.
    merged.extend(b for k, b in remote_blocks if k not in seen)

    # One join for every path, including the common "server has nothing yet"
    # one. Joining differently there reflowed the blank line between sections,
    # so the first refresh after this shipped would have rewritten the spacing
    # of every existing workspace's notes for no reason.
    return "\n\n".join(x.strip("\n") for x in merged).strip("\n")


def _parse_ref(ref: str) -> Tuple[str, Optional[str]]:
    """Parse an ``org`` or ``org/project`` alias reference."""
    if "/" in ref:
        org, project = ref.split("/", 1)
        return org.strip(), project.strip() or None
    return ref.strip(), None


def _workspace_path(
    org_alias: str, project_alias: Optional[str], override: Optional[str]
) -> Path:
    if override:
        # An explicit --path is the user's decision; don't normalise their case away.
        return Path(override).expanduser()
    # Project aliases are conventionally uppercase (BPCL, BPAI, PF) but workspace
    # directories are lowercase everywhere else on disk. Passing the alias through
    # verbatim produced ~/workspaces/bp/BPCL, the odd one out — and on a
    # case-insensitive filesystem that is the same directory as bpcl while still
    # comparing unequal in code.
    leaf = (project_alias or org_alias).lower()
    return Path(os.path.expanduser(f"~/workspaces/{org_alias.lower()}/{leaf}"))


# -- step 2: archive prior context --------------------------------------------


def _archive_prior_context(workspace: Path) -> None:
    """Copy existing project.yml + CLAUDE.md into .innoday/archive/<name>.<ts>,
    then prune archive entries older than the retention window. No-op if neither
    file exists yet (FRESH onboard)."""
    yml_path = workspace / ".innoday" / "project.yml"
    claude_path = workspace / "CLAUDE.md"
    if not yml_path.exists() and not claude_path.exists():
        return

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    archive_dir = workspace / ".innoday" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    if yml_path.exists():
        shutil.copy2(yml_path, archive_dir / f"project.yml.{ts}")
    if claude_path.exists():
        shutil.copy2(claude_path, archive_dir / f"CLAUDE.md.{ts}")

    cutoff = datetime.now(timezone.utc) - timedelta(days=_ARCHIVE_RETENTION_DAYS)
    for entry in archive_dir.iterdir():
        stamp = entry.name.rsplit(".", 1)[-1]
        try:
            when = datetime.strptime(stamp, "%Y%m%d-%H%M%S").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
        if when < cutoff:
            entry.unlink(missing_ok=True)


def _load_existing_yml(workspace: Path) -> dict:
    yml_path = workspace / ".innoday" / "project.yml"
    if not yml_path.exists():
        return {}
    try:
        return yaml.safe_load(yml_path.read_text()) or {}
    except yaml.YAMLError:
        return {}


# -- step 3: repo reconcile ---------------------------------------------------


@lru_cache(maxsize=1)
def _gh_can_clone() -> bool:
    """Whether `gh` is installed AND authenticated.

    Installed-but-logged-out is the trap: `gh repo clone` then fails the same
    way a bare HTTPS clone does, so presence alone is not enough to prefer it.
    """
    if not shutil.which("gh"):
        return False
    try:
        return (
            subprocess.run(
                ["gh", "auth", "status"], capture_output=True, timeout=15
            ).returncode
            == 0
        )
    except (subprocess.SubprocessError, OSError):
        return False


def _owner_repo(github_org: Optional[str], name: Optional[str]) -> Optional[str]:
    """``owner/repo`` for `gh repo clone`, or None.

    The onboarding payload carries `clone_url` and `ssh_url` but **not**
    `full_name` (`src/routers/onboarding.py:8-19`), and `gh` needs the
    `owner/repo` form -- without it the gh branch below can never fire, and the
    whole preference silently degrades to plain git.

    The owner is the GitHub organisation attached to the project's InnoDay
    organisation (`org.github_org` in the resolve response); the repo is its
    own name. Both are on hand at clone time, so this needs no URL parsing and
    cannot be fooled by one: an earlier version derived this from the clone URL
    and turned `file:///srv/mirror.git` into `srv/mirror`, which `gh` cannot
    address.
    """
    if not github_org or not name:
        return None
    return f"{github_org.strip('/')}/{name.strip('/')}"


def _clone_command(
    repo: dict, target: Path, github_org: Optional[str] = None
) -> Optional[list]:
    """How to clone this repo, best available transport first.

    Order matters, and the old order was backwards. It preferred `clone_url`
    -- HTTPS -- which on a machine authenticated by SSH key (the normal setup
    here) fails every clone with `could not read Username for
    'https://github.com'`, because git has no credential helper and nothing to
    prompt. Onboarding a whole workspace failed on every repo.

    1. `gh repo clone` when gh is installed and logged in. It resolves auth
       itself and honours the user's own git protocol preference, so it works
       on an HTTPS-token machine and an SSH-key machine alike.
    2. `ssh_url`. Anyone cloning private repos by hand almost certainly has a
       key; every existing checkout on a dev machine here uses one.
    3. `clone_url` (HTTPS) last, for a machine with a credential helper and no
       key -- CI, a container, a fresh laptop.
    """
    ssh_url = repo.get("ssh_url")
    https_url = repo.get("clone_url")
    full_name = repo.get("full_name") or _owner_repo(github_org, repo.get("name"))
    if full_name and _gh_can_clone():
        return ["gh", "repo", "clone", full_name, str(target)]
    url = ssh_url or https_url
    return ["git", "clone", url, str(target)] if url else None


def _clone_or_pull(
    repo: dict, workspace: Path, github_org: Optional[str] = None
) -> str:
    name = repo["name"]
    target = workspace / name
    try:
        if (target / ".git").exists():
            subprocess.run(
                ["git", "-C", str(target), "pull", "--ff-only"],
                check=True,
                capture_output=True,
                text=True,
                timeout=180,
            )
            return "pulled"
        command = _clone_command(repo, target, github_org)
        if not command:
            return "error: no clone url"
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=600,
        )
        return "cloned"
    except subprocess.CalledProcessError as exc:
        return f"error: {(exc.stderr or str(exc)).strip()[:120]}"
    except subprocess.TimeoutExpired:
        return "error: timed out"


# ---------------------------------------------------------------------------
# Pixelfuel-managed git pre-commit hook (PF-350)
#
# Ported from the pixelfuel-claude `onboard-project` skill's
# `plugins/pixelfuel/git-hooks/`. `onboard-project` was retired (it is now
# `innoday init`), so its per-repo hook installation moved here. The hook
# bodies are embedded as inline strings and written into each cloned repo's
# `.git/hooks/` — the same house convention used for the workspace CLAUDE.md
# template (`_write_workspace_claude_md`) and the pre-push hook generated in
# `src/services/container_guardrails.py`. This keeps the feature wheel-safe
# (no bundled data files, so the `uvx`-installed MCP server works too).
#
# HOOK_MARKER sits on line 2 of the pre-commit hook; the installer uses it as
# a clobber guard — a pre-existing pre-commit hook WITHOUT this marker is a
# foreign hook and is never overwritten.
# ---------------------------------------------------------------------------

HOOK_MARKER = "# pixelfuel-managed-hook v1"

_PRE_COMMIT_HOOK = """#!/bin/sh
# pixelfuel-managed-hook v1
# Warns when the active branch has no linked InnoDay ticket and scans the
# staged diff for likely secrets. Vibe-coder branches (git config
# pixelfuel.vibeCoder=true) are hard-blocked on either failure; all other
# branches only get a stderr warning.
#
# git config pixelfuel.vibeCoder is a local, developer-editable placeholder
# pending a real InnoDay role flag — see PF-170 technical design §8/§9.

HOOK_DIR=$(dirname "$0")
SCRIPT_DIR="$HOOK_DIR"

BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --abbrev-ref HEAD 2>/dev/null)
VIBE_CODER=$(git config --bool pixelfuel.vibeCoder 2>/dev/null || echo "false")

TICKET_OK=1
if echo "$BRANCH" | grep -qiE '(HS|PF)-[0-9]+'; then
  TICKET_OK=0
fi

SECRET_OK=0
STAGED_FILES=$(git diff --cached --name-only)
if ! git diff --cached -U0 | grep '^+' | python3 "$SCRIPT_DIR/secret_scan.py" $STAGED_FILES; then
  SECRET_OK=1
fi

if [ "$TICKET_OK" -ne 0 ]; then
  echo "warning: branch '$BRANCH' has no linked ticket (expected HS-#### or PF-#### in branch name)" >&2
fi

if [ "$SECRET_OK" -ne 0 ]; then
  echo "warning: possible secret detected in staged changes (see secret_scan output above)" >&2
fi

if [ "$VIBE_CODER" = "true" ] && { [ "$TICKET_OK" -ne 0 ] || [ "$SECRET_OK" -ne 0 ]; }; then
  echo "error: commit blocked for vibe-coder branch — fix the issue(s) above" >&2
  if [ "$TICKET_OK" -ne 0 ]; then
    echo "  - add a ticket reference (HS-#### or PF-####) to the branch name" >&2
  fi
  if [ "$SECRET_OK" -ne 0 ]; then
    echo "  - remove the flagged secret from the staged diff" >&2
  fi
  exit 1
fi

exit 0
"""

_SECRET_SCAN = '''#!/usr/bin/env python3
"""Lightweight regex-based secret scanner for staged diff content.

Reads added-line diff text from stdin (e.g. `git diff --cached -U0` filtered
to `+` lines) plus a list of staged filenames as argv. Exits 1 and prints the
matched filename + rule name (never the secret value) to stderr if any
pattern matches. Exits 0 on a clean diff.

This is a fast local pre-flight, not a replacement for CI's TruffleHog pass.
"""

import re
import sys

PATTERNS = [
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key_header", re.compile(r"-----BEGIN[A-Z ]*PRIVATE KEY-----")),
    (
        "generic_credential_assignment",
        re.compile(
            r"(?i)(api_key|apikey|token|secret|password)\\s*[:=]\\s*['\\"]?[A-Za-z0-9/+_\\-]{12,}"
        ),
    ),
]

ENV_FILENAME_RE = re.compile(r"(^|/)\\.env(\\.[^/]+)?$")


def scan_diff(diff_text, staged_filenames):
    findings = []

    for line in diff_text.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for rule_name, pattern in PATTERNS:
            if pattern.search(line):
                findings.append((rule_name, None))

    for filename in staged_filenames:
        if ENV_FILENAME_RE.search(filename):
            findings.append(("staged_env_file", filename))

    return findings


def main():
    diff_text = sys.stdin.read()
    staged_filenames = [f for f in sys.argv[1:] if f]

    findings = scan_diff(diff_text, staged_filenames)

    if not findings:
        return 0

    for rule_name, filename in findings:
        label = filename or "(staged diff)"
        print(f"secret_scan: {rule_name} matched in {label}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    sys.exit(main())
'''


def _install_git_hooks(repo_dir: Path) -> str:
    """Install the pixelfuel-managed pre-commit hook into ``repo_dir``.

    Idempotent and marker-gated: a pre-existing pre-commit hook WITHOUT
    HOOK_MARKER on its second line is a foreign hook and is left untouched.
    Our own managed hook is refreshed on re-run. Returns a status string
    ("installed" / "skipped (foreign hook)" / "error: ...") — like
    ``_clone_or_pull``, it never raises, so a single bad repo degrades to a
    warning rather than aborting the onboard loop.
    """
    # Match _clone_or_pull's "is this a git repo?" check (.exists(), not
    # .is_dir()) so the two agree. `innoday init` only ever fresh-clones, so
    # .git is a directory here; the mkdir below handles creating hooks/.
    git_path = repo_dir / ".git"
    if not git_path.exists():
        return f"error: not a git repository: {repo_dir}"
    if not git_path.is_dir():
        # .git is a file (worktree/submodule) — the hooks dir lives elsewhere;
        # not a path `innoday init` produces, so skip rather than guess.
        return "skipped (worktree checkout)"
    hooks_dir = git_path / "hooks"

    pre_commit = hooks_dir / "pre-commit"
    if pre_commit.exists():
        try:
            second_line = pre_commit.read_text().splitlines()[1:2]
        except (OSError, UnicodeDecodeError):
            second_line = []
        if not second_line or HOOK_MARKER not in second_line[0]:
            return "skipped (foreign hook)"

    try:
        hooks_dir.mkdir(parents=True, exist_ok=True)
        pre_commit.write_text(_PRE_COMMIT_HOOK)
        (hooks_dir / "secret_scan.py").write_text(_SECRET_SCAN)
        os.chmod(pre_commit, 0o755)
        os.chmod(hooks_dir / "secret_scan.py", 0o755)
    except OSError as exc:
        return f"error: {exc}"

    return "installed"


def _archive_removed_repos(workspace: Path, removed_names: List[str]) -> List[str]:
    """`mv` the named repos into <ws>/archived/<repo>. Returns those moved.

    ``removed_names`` comes from the server's `removed_repos` — repos a sync
    positively observed losing the project's GitHub topic label
    (`ProjectRepository.is_active == False`).

    It used to be computed here instead, as "in my project.yml but not in this
    resolve response" — a diff against a live GitHub topic search. Archiving is
    a destructive move of a working directory, and a diff is the wrong evidence
    for it, because plenty of things make a repo drop out of that search
    without anyone removing it from the project:

    * the repo was archived on GitHub (``discover_repos`` filters those out) —
      a different fact from leaving the project;
    * the org's ``github_topics`` setting was edited mid-flight;
    * the directory was cloned by hand, or belongs to another project sharing
      the workspace, so it was never in the search to begin with.

    A recorded removal is better evidence than an absence: it has a timestamp
    and a sync behind it. ``ProjectRepository.is_active`` is set False only when
    ``sync_project_repositories`` positively observes a repo no longer carrying
    the project's topic.

    NOTE for anyone re-deriving the reasoning: an *expired GitHub token* is not
    one of the failure modes above. `search_organization_repositories` raises
    `GitHubAPIError` on any non-200, so a 401 makes resolve answer 502 and the
    CLI abort — it never yields a short list. The case was overstated in an
    earlier draft of this change; the reasons that remain are the ones listed.
    """
    archived: List[str] = []
    if not removed_names:
        return archived
    archived_dir = workspace / "archived"
    for name in removed_names:
        src = workspace / name
        if not src.exists():
            continue  # nothing on disk to archive; not worth reporting
        archived_dir.mkdir(parents=True, exist_ok=True)
        dest = archived_dir / name
        if dest.exists():
            dest = archived_dir / f"{name}.{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"
        shutil.move(str(src), str(dest))
        archived.append(name)
    return archived


def _write_timeline_snapshot(workspace: Path, entries: List[dict]) -> Optional[Path]:
    """Write the resolve response's timeline entries to `.innoday/timeline.md`.

    A workspace that carries its own recent history means an agent picking up
    work here can answer "what has been happening on this project" from the
    files in front of it, without an API call and without a person pasting
    context in. Refreshed wholesale on every run — it is a snapshot of the
    server's feed, never a place to write.
    """
    path = workspace / TIMELINE_SNAPSHOT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Project timeline",
        "",
        f"> Snapshot of the {len(entries)} most recent InnoDay timeline "
        f"entries, written by `innoday refresh` at {stamp}.",
        "> Regenerated wholesale each refresh — don't edit, it will be "
        "overwritten. Run `innoday timeline` for the full paginated feed.",
        "",
    ]
    if not entries:
        lines.append("_No timeline entries recorded for this project yet._")
    for e in entries:
        when = (e.get("occurred_at") or "")[:10] or "unknown date"
        etype = (e.get("event_type") or "").replace("_", " ")
        lines.append(f"## {e.get('title') or '(untitled)'}")
        lines.append("")
        lines.append(f"**{when}** · {etype} · {e.get('created_by') or 'unknown'}")
        lines.append("")
        lines.append((e.get("summary") or "").strip())
        lines.append("")
    path.write_text("\n".join(lines).rstrip("\n") + "\n")
    return path


# -- step 4: regenerate project.yml -------------------------------------------


def _merge_release_configs(
    existing: dict,
    org_alias: str,
    github_topic: Optional[str],
    project_alias: Optional[str],
):
    """Preserve blastoff-owned version fields from the existing file for THIS
    project only; repair organization/label fresh. Other projects' entries are
    dropped so one project's file never leaks another's blastoff state (PF-318).

    release_configs is a dict keyed by project alias (the shape blastoff writes).
    We keep only the current project's entry. A non-dict (unknown) shape is
    passed through untouched to avoid corrupting an unrecognised format."""
    old_rc = existing.get("release_configs")
    if not old_rc:
        return None
    if not isinstance(old_rc, dict):
        return old_rc  # unknown shape: don't touch it

    # Find this project's existing entry (by alias key), if any.
    cfg = old_rc.get(project_alias) if project_alias else None
    if not isinstance(cfg, dict):
        # No entry for this project — nothing blastoff-owned to preserve.
        return None
    preserved = {k: v for k, v in cfg.items() if k in _BLASTOFF_OWNED_FIELDS}
    preserved["organization"] = org_alias
    if github_topic:
        preserved["label"] = github_topic
    return {project_alias: preserved}


def _write_project_yml(workspace: Path, resolved: dict) -> Path:
    innoday_dir = workspace / ".innoday"
    innoday_dir.mkdir(parents=True, exist_ok=True)
    yml_path = innoday_dir / "project.yml"

    existing = _load_existing_yml(workspace)
    org = resolved["org"]
    project = resolved.get("project")
    project_alias = project["alias"] if project else None
    data = {
        # Format stamps — readers require schema_version and reject older files
        # (see src/cli/utils/project_context.py). generated_by aids debugging.
        #
        # NOTE: adding keys here does NOT need a schema_version bump. Readers
        # compare for INEQUALITY, so bumping would make every older CLI reject
        # the file outright rather than ignore what it doesn't recognise.
        "schema_version": PROJECT_YML_SCHEMA_VERSION,
        "generated_by": f"innoday {get_display_version()}",
        # When this workspace was last brought in line with the server. The
        # point of recording it is that refresh is meant to run repeatedly and
        # unattended: without a stamp there is no way to tell a workspace that
        # is current from one whose dispatcher stopped running weeks ago, and
        # both look identical on disk.
        "last_refreshed_at": datetime.now(timezone.utc).isoformat(),
        "context_template_version": CONTEXT_TEMPLATE_VERSION,
        "org": {
            "alias": org["alias"],
            "name": org["name"],
            "innoday_id": org["id"],
            "github_org": org["github_org"],
        },
        "project": {
            "alias": project_alias,
            "name": project["name"] if project else None,
            "innoday_id": project["id"] if project else None,
            "github_topic": resolved.get("github_topic"),
        },
        "repos": [{"name": r["name"]} for r in resolved.get("repos", [])],
    }
    # Mirror the archive guard in _run_algorithm: if discovery returned no repos
    # but the previous file listed some, keep the old list rather than blanking
    # the workspace's repo inventory on one bad/misconfigured refresh.
    if not data["repos"]:
        old_repos = [
            r
            for r in (existing.get("repos") or [])
            if isinstance(r, dict) and r.get("name")
        ]
        if old_repos:
            data["repos"] = [{"name": r["name"]} for r in old_repos]
    rc = _merge_release_configs(
        existing, org["alias"], resolved.get("github_topic"), project_alias
    )
    if rc:
        data["release_configs"] = rc

    yml_path.write_text(yaml.safe_dump(data, sort_keys=False))
    return yml_path


# -- step 5: regenerate workspace CLAUDE.md -----------------------------------


def _render_generated_context(resolved: dict) -> str:
    """The generated half of the workspace CLAUDE.md, as a string.

    Split out from writing the file because this exact text is also what gets
    pushed to `projects.project_context` for the UI to display. Rendering it
    once and using it for both is what keeps the stored copy and the on-disk
    copy from drifting into two subtly different documents.
    """
    org = resolved["org"]
    project = resolved.get("project")
    repos = resolved.get("repos", [])
    proj_label = f"{org['alias']}/{project['alias']}" if project else org["alias"]
    repo_rows = "\n".join(f"| {r['name']} |" for r in repos) or "| _(none)_ |"

    content = f"""# {project["name"] if project else org["name"]} — workspace context

> **This section is auto-generated by `innoday init`/`refresh` — every field in
> it is rewritten from InnoDay + GitHub state on each run, so don't hand-edit
> here.** Add your own notes below the `innoday:end-generated` marker at the
> bottom instead; that part is preserved across refreshes. Run `innoday refresh`
> from anywhere inside this workspace.

**Org:** {org["name"]} (`{org["alias"]}`)  ·  **InnoDay org id:** `{org["id"]}`
**GitHub org:** `{org["github_org"]}`  ·  **GitHub topic:** `{resolved.get("github_topic") or "—"}`
{"**Project:** " + project["name"] + " (`" + project["alias"] + "`)  ·  **id:** `" + project["id"] + "`" if project else "**Project:** _(org default / none)_"}

## Repositories ({len(repos)})

| Repo |
|------|
{repo_rows}

A repo is moved to `./archived/` only once a sync has observed it losing the
project's GitHub topic — never because one refresh failed to list it. Prior
`project.yml`/`CLAUDE.md` versions are kept under `.innoday/archive/` for
{_ARCHIVE_RETENTION_DAYS} days.

## Recent activity

`.innoday/timeline.md` holds the project's most recent InnoDay timeline
entries — releases, syncs, summaries — refreshed on every `innoday refresh`.
**Read it before asking what has been happening on this project.** For the
full paginated feed, `innoday timeline`.

## Working here

```bash
innoday status     # identity, current project, token, API health
innoday refresh    # re-onboard this workspace (pull repos, rewrite context)
innoday timeline   # what has happened on this project lately
```

{_DEV_WORKFLOW_STANDARD}

{_COLLABORATION_STANDARD}

Onboarded via `innoday init {proj_label}`.
"""
    return content


def _write_workspace_claude_md(
    workspace: Path, resolved: dict, custom: str
) -> Tuple[Path, str]:
    """Write CLAUDE.md as generated header + sentinel + ``custom``.

    The file is fully DERIVED output: both halves are passed in, and whatever
    was on disk is replaced rather than merged into. That is what makes a
    refresh reproducible — run it twice against the same server state and you
    get byte-identical files, regardless of what the previous run left behind.

    The merge that decides ``custom`` happens in the caller (``_run_algorithm``),
    which is the only place that holds both the local file and the server's
    copy. Returns the path and the generated half, since the caller pushes that
    same text to the server.
    """
    content = _render_generated_context(resolved)
    claude_path = workspace / "CLAUDE.md"
    out = f"{content}\n{_CUSTOM_SECTION_HEADER}\n"
    if custom:
        out = f"{out}\n{custom}\n"
    claude_path.write_text(out)
    return claude_path, content


class WorkspaceCommands:
    """init / join / refresh."""

    @staticmethod
    def setup_init_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "ref", help="Project reference as <org>/<project> alias (e.g. hs/pf)"
        )
        parser.add_argument("--path", help="Workspace directory override")
        parser.add_argument(
            "--no-clone",
            action="store_true",
            help="Write context only; skip git clone/pull",
        )
        parser.add_argument(
            "--no-hooks",
            action="store_true",
            help="Skip installing the pixelfuel-managed pre-commit hook",
        )

    @staticmethod
    def setup_join_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "ref", help="Org to join, optionally <org>/<project> (e.g. hs or hs/pf)"
        )
        parser.add_argument("--path", help="Workspace directory override")
        parser.add_argument(
            "--no-clone", action="store_true", help="Write context only"
        )
        parser.add_argument(
            "--no-hooks",
            action="store_true",
            help="Skip installing the pixelfuel-managed pre-commit hook",
        )

    @staticmethod
    def setup_refresh_parser(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--no-clone", action="store_true", help="Write context only"
        )
        parser.add_argument(
            "--no-hooks",
            action="store_true",
            help="Skip installing the pixelfuel-managed pre-commit hook",
        )
        parser.add_argument(
            "--replace-context",
            action="store_true",
            help=(
                "Replace the project's stored notes with this workspace's copy "
                "instead of merging them. This is how you DELETE a note: a "
                "normal refresh unions the two copies, so a section removed "
                "from CLAUDE.md comes back from the server."
            ),
        )

    # -- shared onboard/refresh core -----------------------------------------

    @staticmethod
    async def _resolve(
        config: CLIConfig, org_alias: str, project_alias: Optional[str]
    ) -> Tuple[Optional[dict], Optional[str]]:
        async with InnoDayAPIClient(config) as client:
            params = {"org": org_alias}
            if project_alias:
                params["project"] = project_alias
            resp = await client.get("/api/v1/onboarding/resolve", params=params)
            if resp.status_code == 200:
                return resp.json(), None
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text
            return None, detail

    @staticmethod
    async def _push_context(
        config: CLIConfig,
        org_alias: str,
        project_alias: str,
        generated: str,
        additional: str,
    ) -> Optional[str]:
        """Store this run's context on the project. Returns an error, or None.

        Best-effort by design: the workspace is already written and correct by
        the time this runs, so a server that is down or a token that lacks the
        org must not turn a successful refresh into a failure. The cost of
        failing is one run's notes not being backed up, and the next refresh
        pushes them again.
        """
        payload = {
            "org": org_alias,
            "project": project_alias,
            "project_context": generated,
            "template_version": CONTEXT_TEMPLATE_VERSION,
            "additional_context": additional,
        }
        try:
            async with InnoDayAPIClient(config) as client:
                resp = await client.post("/api/v1/onboarding/context", json=payload)
            if resp.status_code in (200, 201):
                return None
            try:
                return resp.json().get("detail", resp.text)
            except Exception:
                return resp.text
        except Exception as exc:  # network, auth, anything
            return str(exc)

    @staticmethod
    def _run_algorithm(
        resolved: dict,
        workspace: Path,
        no_clone: bool,
        no_hooks: bool = False,
        replace_context: bool = False,
    ) -> Tuple[int, str, str]:
        """Steps 1-5 of the onboard/refresh algorithm. Pure local FS + git.

        Returns ``(exit_code, generated_context, merged_custom_context)`` — the
        caller pushes the last two to the server, which is the only part of a
        refresh that needs the network after `resolve`.
        """
        # 1. detect mode
        existing = _load_existing_yml(workspace)
        mode = "refresh" if existing else "onboard"
        console.print(
            f"{'🔄 Refreshing' if mode == 'refresh' else '📦 Onboarding'} "
            f"{resolved['org']['alias']}"
            + (f"/{resolved['project']['alias']}" if resolved.get("project") else "")
            + f" → {workspace}"
        )
        workspace.mkdir(parents=True, exist_ok=True)

        # 2. archive prior context (no-op on fresh)
        _archive_prior_context(workspace)

        resolved_repos = resolved.get("repos", [])
        resolved_names = [r["name"] for r in resolved_repos]
        cloned = pulled = errored = 0
        hooks_installed = 0

        if not no_clone:
            # 3a. clone/pull resolved repos
            if resolved_repos:
                console.print(f"Syncing {len(resolved_repos)} repo(s) …")
            for repo in resolved_repos:
                action = _clone_or_pull(
                    repo, workspace, (resolved.get("org") or {}).get("github_org")
                )
                if action == "cloned":
                    cloned += 1
                elif action == "pulled":
                    pulled += 1
                else:
                    errored += 1
                    console.print(format_warning(f"  {repo['name']}: {action}"))
                    continue
                # 3a.i install the pixelfuel-managed pre-commit hook per repo
                # (on by default; the repo is on disk after a clone/pull). A
                # foreign or un-writable hook degrades to a warning, never a
                # hard failure of onboarding.
                if not no_hooks:
                    hook_status = _install_git_hooks(workspace / repo["name"])
                    if hook_status == "installed":
                        hooks_installed += 1
                    elif hook_status.startswith("error"):
                        console.print(
                            format_warning(
                                f"  {repo['name']}: pre-commit hook {hook_status}"
                            )
                        )

            # 3b. archive ONLY repos the server has recorded as removed —
            # `ProjectRepository.is_active == False`, set by a sync that saw the
            # topic label go. See _archive_removed_repos for why a diff against
            # the resolve response is not a safe substitute.
            #
            # The two sources can disagree, and the disagreement is routine:
            # `repos` is a LIVE GitHub topic search, while `removed_repos` is
            # the DB's record from the last sync. A repo that has just REGAINED
            # its topic is therefore in both — present on GitHub now, still
            # flagged removed until a sync catches up. Archiving it would mean
            # cloning a repo in 3a and moving it to ./archived/ seconds later,
            # on every single refresh, until someone happened to run a sync.
            # Anything the server just told us to clone is not removed.
            removed = [
                r.get("name")
                for r in (resolved.get("removed_repos") or [])
                if isinstance(r, dict)
                and r.get("name")
                and r.get("name") not in resolved_names
            ]
            archived = _archive_removed_repos(workspace, removed)
            for name in archived:
                console.print(
                    format_warning(
                        f"  📦 archived {name} (sync recorded it losing the "
                        f"project's GitHub topic)"
                    )
                )

            # A repo in the workspace that resolve did not list, and that is not
            # recorded as removed, is left exactly where it is. Say so rather
            # than passing over it silently — it is usually a token or topic
            # problem, and the whole point is that the workspace no longer acts
            # on the ambiguity.
            old_names = [
                r.get("name")
                for r in (existing.get("repos") or [])
                if isinstance(r, dict) and r.get("name")
            ]
            unexplained = [
                n
                for n in old_names
                if n not in resolved_names and n not in removed and n not in archived
            ]
            if unexplained:
                console.print(
                    format_warning(
                        f"{len(unexplained)} repo(s) in this workspace were not "
                        f"listed by the server and are not recorded as removed — "
                        f"keeping them: {', '.join(sorted(unexplained))}. Usually a "
                        f"GitHub token or topic problem; `innoday sync` then refresh."
                    )
                )

        # 4. merge the hand-written notes, then write every file from the merge.
        # Read the local tail BEFORE regenerating, or the tail is whatever this
        # run just wrote.
        claude_path = workspace / "CLAUDE.md"
        local_custom = (
            _extract_custom_content(claude_path) if claude_path.exists() else ""
        )
        server_custom = resolved.get("additional_context") or ""
        if replace_context:
            merged_custom = local_custom
            if server_custom and server_custom.strip() != local_custom.strip():
                console.print(
                    format_warning(
                        "--replace-context: the server's stored notes are being "
                        "replaced by this workspace's copy, not merged."
                    )
                )
        else:
            merged_custom = _union_custom_content(local_custom, server_custom)
            gained = merged_custom.strip() != local_custom.strip()
            if gained and server_custom:
                console.print(
                    "  📝 merged notes stored on the project into CLAUDE.md "
                    "(use --replace-context to overwrite them instead)"
                )

        # 5. regenerate every derived file
        yml_path = _write_project_yml(workspace, resolved)
        _, generated = _write_workspace_claude_md(workspace, resolved, merged_custom)
        timeline = resolved.get("timeline") or []
        tl_path = _write_timeline_snapshot(workspace, timeline)

        console.print(
            format_success(
                f"{'Refreshed' if mode == 'refresh' else 'Onboarded'} "
                f"— {cloned} cloned, {pulled} pulled"
                + (f", {errored} errored" if errored else "")
                + (f", {hooks_installed} hook(s) installed" if hooks_installed else "")
            )
        )
        console.print(f"Context: {yml_path}")
        if tl_path:
            console.print(
                f"Timeline: {tl_path} ({len(timeline)} entr"
                f"{'y' if len(timeline) == 1 else 'ies'})"
            )
        console.print(f"cd {workspace} to work.")
        return (0 if errored == 0 else 1), generated, merged_custom

    @staticmethod
    async def _onboard(
        config: CLIConfig,
        org_alias: str,
        project_alias: Optional[str],
        path: Optional[str],
        no_clone: bool,
        no_hooks: bool = False,
        replace_context: bool = False,
    ) -> int:
        resolved, detail = await WorkspaceCommands._resolve(
            config, org_alias, project_alias
        )
        if not resolved or "org" not in resolved:
            console.print(format_error(f"Could not resolve {org_alias}: {detail}"))
            return 1
        workspace = _workspace_path(org_alias, project_alias, path)
        status, generated, merged_custom = WorkspaceCommands._run_algorithm(
            resolved, workspace, no_clone, no_hooks, replace_context
        )
        await WorkspaceCommands._register_repos(config, resolved)

        # Store the context we just rendered. Only meaningful for a project —
        # context is a project-level field, and an org-only workspace has no
        # row to attach it to.
        project = (resolved or {}).get("project") or {}
        if project.get("alias"):
            err = await WorkspaceCommands._push_context(
                config,
                (resolved.get("org") or {}).get("alias") or org_alias,
                project["alias"],
                generated,
                merged_custom,
            )
            if err:
                console.print(
                    format_warning(
                        f"Workspace written, but its context was not stored on "
                        f"the project ({err}). Your notes are still in CLAUDE.md; "
                        f"the next refresh will try again."
                    )
                )
        return status

    @staticmethod
    async def _register_repos(config: CLIConfig, resolved: dict) -> None:
        """Tell InnoDay about the repos we just cloned.

        **Discovery and registration were two different things and only one of
        them ran.** `/onboarding/resolve` asks GitHub which repos carry the
        project's topic and hands back a list to clone -- it writes nothing.
        Registration (`repositories/discover`) is what creates the
        `repositories` and `project_repositories` rows everything else reads.
        Nothing in init/join/refresh called it, so a freshly-onboarded project
        had its repos on disk and *zero* repos in InnoDay: no repo list, no code
        activity, and therefore a summary that could only ever be empty. It
        looked like a stale workspace, so the instinct was to run `refresh`
        again -- which cloned again and still registered nothing.

        Best-effort and non-fatal: the local workspace is already usable, and
        failing the whole onboard because a server-side reconcile did not land
        would be a worse trade. `innoday sync --scope repos` is the retry.
        """
        project = (resolved or {}).get("project") or {}
        org = (resolved or {}).get("org") or {}
        if not project.get("id") or not org.get("id"):
            return
        try:
            async with InnoDayAPIClient(config) as client:
                resp = await client.post(
                    f"/api/v1/organizations/{org['id']}/projects/"
                    f"{project['id']}/repositories/discover"
                )
            if resp.status_code == 200:
                count = (resp.json() or {}).get("repositories_synced", 0)
                console.print(f"Registered {count} repo(s) with InnoDay")
            else:
                console.print(
                    format_warning(
                        f"Repos cloned but not registered with InnoDay "
                        f"(HTTP {resp.status_code}). Retry: innoday sync --scope repos"
                    )
                )
        except Exception as exc:  # noqa: BLE001 - never fail an onboard on this
            console.print(
                format_warning(
                    f"Repos cloned but not registered with InnoDay ({exc}). "
                    "Retry: innoday sync --scope repos"
                )
            )

    # -- commands ------------------------------------------------------------

    @staticmethod
    async def execute_init(args: argparse.Namespace, config: CLIConfig) -> int:
        org_alias, project_alias = _parse_ref(args.ref)
        if not project_alias:
            console.print(
                format_warning(
                    "init expects <org>/<project> (e.g. `innoday init hs/pf`). "
                    "Onboarding the org's default project."
                )
            )
        return await WorkspaceCommands._onboard(
            config, org_alias, project_alias, args.path, args.no_clone, args.no_hooks
        )

    @staticmethod
    async def execute_join(args: argparse.Namespace, config: CLIConfig) -> int:
        org_alias, project_alias = _parse_ref(args.ref)

        # 1. join the org (self-register / complete invite). Best-effort: a
        #    platform user or already-member gets a benign success.
        resolved, _ = await WorkspaceCommands._resolve(config, org_alias, None)
        if resolved and "org" in resolved:
            org_id = resolved["org"]["id"]
            async with InnoDayAPIClient(config) as client:
                join_resp = await client.post(
                    f"/api/v1/organizations/{org_id}/join", json={}
                )
                if join_resp.status_code in (200, 201):
                    msg = (join_resp.json() or {}).get("message", "")
                    if msg:
                        console.print(format_success(msg))

        # 2. then onboard exactly like init
        return await WorkspaceCommands._onboard(
            config, org_alias, project_alias, args.path, args.no_clone, args.no_hooks
        )

    @staticmethod
    async def execute_refresh(args: argparse.Namespace, config: CLIConfig) -> int:
        yml = find_project_yml()
        if not yml:
            console.print(
                format_error(
                    "Not inside a project workspace (no .innoday/project.yml found). "
                    "Run `innoday init <org>/<proj>` first."
                )
            )
            return 1
        try:
            data = yaml.safe_load(yml.read_text()) or {}
        except yaml.YAMLError:
            console.print(format_error(f"Could not parse {yml}"))
            return 1

        org_data = data.get("org") or {}
        project_data = data.get("project") or {}
        # Upgrading a legacy file IS refresh's job — a pre-alias file stamped
        # only with the old `org.slug` must not dead-end the user into a
        # from-scratch `innoday init`.
        #
        # `slug` is dead everywhere else and is never written back: the writer
        # emits `alias` only, so refreshing a legacy file drops `org.slug` and
        # `project.innoday_slug` for good. It is read here ONLY as the one-way
        # upgrade input, and only for the ORG — the org alias replaced org slug
        # one-for-one (same value, renamed field), so it is a valid alias
        # candidate, and `_resolve` validates it against the API before
        # anything is written.
        #
        # There is deliberately NO project-slug fallback: project slug was
        # removed outright rather than renamed (project aliases are per-org and
        # stored `slug` is NULL), so a legacy `innoday_slug` is not an alias and
        # sending it just 404s. A file with no project alias resolves the org's
        # default project instead.
        org_alias = org_data.get("alias") or org_data.get("slug")
        project_alias = project_data.get("alias")
        if not org_alias:
            console.print(
                format_error(
                    f"{yml} has no org.alias or legacy org.slug to refresh from. "
                    "Re-onboard with `innoday init <org>/<proj>`."
                )
            )
            return 1
        if not org_data.get("alias"):
            console.print(
                format_warning(
                    f"Upgrading legacy project file (org.slug → org.alias) "
                    f"→ schema v{PROJECT_YML_SCHEMA_VERSION}."
                )
            )

        # Refresh re-onboards into the SAME workspace (project.yml's grandparent).
        workspace = str(yml.parent.parent)
        return await WorkspaceCommands._onboard(
            config,
            org_alias,
            project_alias,
            workspace,
            args.no_clone,
            args.no_hooks,
            getattr(args, "replace_context", False),
        )
