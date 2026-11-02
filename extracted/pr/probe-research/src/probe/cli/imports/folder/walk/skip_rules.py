"""what the walk never enters or reads: credential and tool folders, hidden-folder admission (--include-hidden), skipped files and suffixes."""

from __future__ import annotations


#: CREDENTIAL STORES. Never walked, never counted, never admitted -- not by the
#: research allowlist below and not by `--include-hidden`. Named HERE, apart
#: from the hidden-folder policy, so that a future edit to that allowlist cannot
#: admit one: an admitted store is not merely sampled, it is WALKED, inherited
#: into a project, manifested and UPLOADED whole, and scrubbing samples does not
#: touch that path because the upload sends bytes off disk and never reads a
#: sample. `walk` prunes SKIP_DIRS (which carries these) before it asks whether
#: a hidden folder is admitted, and `hidden_admitted` refuses them as well.
CREDENTIAL_DIRS = frozenset(
    {".ssh", ".aws", ".gnupg", ".kube", ".docker", ".azure", ".gcloud", ".config"}
)

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
        # Every OTHER dot-folder is skipped by the hidden-folder policy below,
        # but that skip COUNTS what it passes over and names it in the plan.
        # These are pruned outright instead: machine-written caches whose
        # counts would swamp the "skipped" line and cost a walk of their own.
        ".cache",
        ".local",
        ".npm",
        ".cargo",
        ".conda",
        ".jupyter",
        ".terraform",
        ".gradle",
        ".Trash",
        *CREDENTIAL_DIRS,
    }
)

#: HIDDEN FOLDERS ARE SKIPPED BY DEFAULT; these are the research ones admitted.
#:
#: The policy was a denylist (SKIP_DIRS above) until a customer import walked
#: seven Claude Code agent worktrees under `.claude/worktrees/` -- 65,491 of the
#: 78,628 files it uploaded were copies of one repo. Any dot-folder nobody had
#: named was imported. Now a dot-folder is skipped unless it is named here or
#: passed as `--include-hidden <name>`.
#:
#: The blanket dotfile skip this replaces had the opposite flaw, which is why
#: the list exists rather than a bare `startswith(".")`: it dropped
#: `.hydra/config.yaml` -- where Hydra writes the config that NAMES the
#: experiment -- along with `.dvc/`, and it dropped them from the CENSUS too, so
#: the denominator claimed a completeness it did not have. So a skipped hidden
#: folder is still WALKED for a count (`backfill_evidence.walk`) and listed with
#: it in the plan; only its files stay out of the import.
#:
#: Hidden FILES (`.condarc`, `.gitignore`) are not governed by this: they are
#: walked as before, and SKIP_FILES below refuses the credential ones.
RESEARCH_DOT_DIRS = frozenset({".hydra", ".dvc", ".aim", ".neptune"})

#: Inside an admitted research dot-folder, the subfolders that are copies:
#: `.dvc/cache` holds a content-addressed copy of every DVC-tracked file (the
#: workspace already has them) and `.dvc/tmp` is DVC's scratch. Skipped and
#: counted like a hidden folder, so `.dvc/config` still names the remote.
RESEARCH_DOT_DIR_SKIPS = {".dvc": frozenset({"cache", "tmp"})}

#: The walk's rules, carried on the census (`Census.walk_rules`). 0 is the
#: rules before hidden folders and worktree copies were skipped -- the default,
#: so a census an older CLI saved into a queued job re-walks by ITS rules.
WALK_RULES = 1


def hidden_admitted(name: str, include: frozenset[str] | tuple[str, ...] = ()) -> bool:
    """Whether the hidden folder `name` is walked into the import.

    The allowlist and the researcher's `--include-hidden` names decide; a
    credential store is refused whatever either says.
    """
    if name in CREDENTIAL_DIRS:
        return False
    return name in RESEARCH_DOT_DIRS or name in include


def hidden_includes(names) -> tuple[str, ...]:
    """`--include-hidden` values as folder names: `.claude`, `claude/` -> `.claude`.

    A NAME, matched wherever the folder sits in the tree, not a path. Raises
    ValueError on a path, so a value that could never match is not silently
    ignored.
    """
    out: list[str] = []
    for raw in names or ():
        name = str(raw).strip().rstrip("/")
        if not name or "/" in name or "\\" in name or name in (".", ".."):
            raise ValueError(
                f"--include-hidden takes a hidden folder's name, such as .claude; got {raw!r}"
            )
        name = name if name.startswith(".") else "." + name
        if name not in out:
            out.append(name)
    return tuple(out)


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
