"""nx_code_gate — THE CODING LANE. `classify_code_action(action) -> CodeVerdict`.

A SEPARATE lane from risk_tiers.py (the money wall). git / shell / file edits are NOT money movement or
legal signing, so routing `git commit` through `is_untouchable()` would be a category error — the money
lexicon has no honest opinion on `push`. This lane classifies the CODING verb-space instead, but inherits
the SAME structural posture that makes the money wall trustworthy:

  • FAIL-CLOSED. A recognized-safe read is the ONLY thing that resolves SAFE. Everything unrecognized —
    a new tool, a typo, a glued compound — resolves GATED (staged), never SAFE. The guarantee cannot be
    defeated by a missing string because the DEFAULT is "hold it".
  • POSITIVE allowlist for the autonomous path; explicit denylist for the never-path; staged in between.
  • HOMOGLYPH-FOLDED (shared with risk_tiers._fold) so `rm` / `push` can't be spelled with lookalikes.

Because both clone targets are allowed and push is allowed, the safety line is NOT sandbox-vs-real — it is
STAGED-vs-APPLIED. Diff-staging is the entire mechanism: a write/edit/commit is shown as a diff and fires
only on the operator's OK; a push to a protected branch needs an explicit confirm EVERY time (never a
blanket approve-all); and a small set of actions never fire at all.

Tiers
  SAFE        read · list · grep · diff · inspect · clone · fetch      → autonomous
  GATED       write · edit · delete · fork · commit · branch · push    → staged as a diff, fires on OK
  GATED_MAIN  push to a protected branch (main/master/prod/release)    → explicit confirm EVERY time
  PROHIBITED  force-push · history rewrite · rm -rf · secret write ·    → NEVER, even if approved by mistake
              env/secret exfiltration · remote-exec · sudo/system-destroy

Credentials never enter model context: push auth is a keyring seam (resolved by the executor, never inlined),
and any command that reads a secret and sends it outward is PROHIBITED here. Stdlib-only, no side effects —
meant to be audited in one sitting and unit-proven without live infra, exactly like risk_tiers.py.
"""
import re as _re
import shlex as _shlex

try:  # inherit the hardened homoglyph/compat folder from the money wall (single source of truth)
    from risk_tiers import _fold
except Exception:  # pragma: no cover — degrade to identity if risk_tiers is unavailable (still fail-closed below)
    def _fold(s):
        return str(s or "")

from typing import NamedTuple

SAFE = "SAFE"
GATED = "GATED"
GATED_MAIN = "GATED_MAIN"
PROHIBITED = "PROHIBITED"

# Severity order — combining multiple shell segments takes the MOST restrictive verdict.
_SEVERITY = {SAFE: 0, GATED: 1, GATED_MAIN: 2, PROHIBITED: 3}


class CodeVerdict(NamedTuple):
    """The typed decision for one coding action."""
    tier: str      # SAFE | GATED | GATED_MAIN | PROHIBITED
    reason: str

    @property
    def autonomous(self) -> bool:
        """True ONLY for SAFE — the single path that may fire without staging."""
        return self.tier == SAFE

    @property
    def staged(self) -> bool:
        """True for GATED / GATED_MAIN — shown as a diff, fires on operator approval."""
        return self.tier in (GATED, GATED_MAIN)

    @property
    def needs_explicit_confirm(self) -> bool:
        """True for GATED_MAIN — a protected-branch push: confirm every time, never a blanket approve-all."""
        return self.tier == GATED_MAIN

    @property
    def prohibited(self) -> bool:
        """True for PROHIBITED — never fires, even post-approval (the executor's fail-safe net)."""
        return self.tier == PROHIBITED


# ── secret / protected surfaces ──────────────────────────────────────────────────────────────────────────
# A write to any of these is never staged — it is refused. Substring-matched against the folded, lowered path.
_SECRET_PATH_SUBSTRINGS = (
    "/.ssh/", "/.aws/", "/.gnupg/", "/.pypirc", "/.netrc", "/.npmrc", "/.docker/config",
    "/.nx/config", "/.nx/credentials", "/.nx/mcp_credentials", "/.nx/auth", "/.config/nx/config",
    "id_rsa", "id_ed25519", "id_ecdsa", "id_dsa", "credentials.json", ".env", "secrets", ".pem", ".key",
    ".p12", ".keystore", ".htpasswd", "private_key", "privatekey", "service-account", "serviceaccount",
)
# Protected branches — a push whose destination is one of these needs explicit confirmation every time.
_PROTECTED_BRANCHES = frozenset(("main", "master", "production", "prod", "release", "stable", "live"))

# Outbound network tools — a secret/env reference in the same command as one of these is exfiltration.
_NET_SEND = frozenset((
    "curl", "wget", "nc", "ncat", "netcat", "scp", "sftp", "rsync", "ssh", "telnet", "ftp", "socat", "httpie", "http",
))
# Shell interpreters — piping a remote fetch into one is remote code execution.
_INTERPRETERS = frozenset(("sh", "bash", "zsh", "ksh", "dash", "fish", "python", "python2", "python3",
                           "node", "deno", "bun", "ruby", "perl", "php", "eval", "source"))
# Environment-dumping programs (never autonomous; exfil-relevant when paired with a net-send tool).
_ENV_DUMP = frozenset(("env", "printenv", "set", "export"))


def _is_secret_path(path: str) -> bool:
    p = _fold(str(path or "")).lower()
    return any(sub in p for sub in _SECRET_PATH_SUBSTRINGS)


def _is_protected_branch(name: str) -> bool:
    n = _fold(str(name or "")).strip().lower().lstrip("+").split("/")[-1]
    return n in _PROTECTED_BRANCHES or n == "head"


# ── SAFE (read/inspect) vocabularies ─────────────────────────────────────────────────────────────────────
# Read-only, non-mutating programs. The WHOLE command must be read-shaped to fire autonomously.
_SAFE_PROGRAMS = frozenset((
    "ls", "cat", "head", "tail", "wc", "stat", "file", "tree", "pwd", "realpath", "readlink", "basename",
    "dirname", "du", "df", "less", "more", "nl", "cut", "sort", "uniq", "comm", "column", "hexdump", "xxd",
    "od", "md5sum", "sha1sum", "sha256sum", "cksum", "type", "which", "whereis", "grep", "egrep", "fgrep",
    "rg", "ag", "ack", "ripgrep", "fd", "locate", "wc", "date", "uname", "hostname", "whoami", "id", "echo",
    "printf", "true", "false", "test", "diff", "cmp", "jq", "yq", "awk", "sed",  # awk/sed read-only when no -i / no redirect (checked below)
))
# git read-only subcommands (list/inspect). branch/tag/config are read ONLY in their listing forms (checked below).
_GIT_READ_SUBS = frozenset((
    "status", "log", "diff", "show", "remote", "rev-parse", "describe", "ls-files", "ls-remote", "ls-tree",
    "blame", "shortlog", "cat-file", "whatchanged", "name-rev", "merge-base", "symbolic-ref", "for-each-ref",
    "count-objects", "rev-list", "grep", "reflog", "fetch", "clone", "version", "help", "config",
))
# git write subcommands → GATED (staged). Not exhaustive; unknown git subs also fall through to GATED.
_GIT_WRITE_SUBS = frozenset((
    "add", "commit", "checkout", "switch", "restore", "merge", "stash", "cherry-pick", "revert", "tag",
    "mv", "rm", "init", "apply", "am", "pull", "clean", "worktree", "submodule", "notes", "bisect", "gc", "prune",
))
# camelCase/typecheck read-only invocations recognized by their first-flag shape.
_INSPECT_FLAGS = frozenset(("--version", "-v", "--help", "-h", "--noemit", "--dry-run", "--check", "--list", "-t"))


def _segments(cmd: str):
    """Split a shell command into pipeline/sequence segments. Over-splitting is fine — each piece is
    classified and the most restrictive verdict wins, so a hidden mutation in any segment is caught."""
    raw = str(cmd or "")
    # split on ; && || | & and newlines (keep it structural, not a full parser)
    parts = _re.split(r"(?:\|\||&&|[;\|\n&])", raw)
    return [p.strip() for p in parts if p.strip()]


def _tokenize(seg: str):
    """Tokenize one segment, folded + lowercased. shlex first (honours quotes); regex fallback on failure."""
    seg = _fold(seg)
    try:
        toks = _shlex.split(seg, posix=True)
    except Exception:
        toks = _re.split(r"\s+", seg)
    return [t.lower() for t in toks if t]


def _program(tokens):
    """The effective program of a segment: skip leading VAR=val assignments and benign wrappers
    (env/command/time/nice/nohup/xargs/sudo-is-handled-separately) to find the real command."""
    i = 0
    wrappers = {"command", "time", "nice", "nohup", "stdbuf", "ionice", "setsid"}
    while i < len(tokens):
        t = tokens[i]
        if "=" in t and _re.match(r"^[a-z_][a-z0-9_]*=", t):   # FOO=bar prefix
            i += 1
            continue
        if t == "env":
            # `env FOO=bar cmd` is a wrapper; bare `env` (or `env | …`) is a dump handled by the caller
            if i + 1 < len(tokens):
                i += 1
                continue
            return "env"
        if t in wrappers:
            i += 1
            continue
        return t
    return ""


def _has_redirect_to(tokens, raw):
    """Return the redirection target path if the segment writes to a file (`>`/`>>`), else None."""
    m = _re.search(r"(?:>>|>)\s*([^\s;|&]+)", raw)
    return m.group(1) if m else None


# ── PROHIBITED detection ─────────────────────────────────────────────────────────────────────────────────
def _prohibited_whole(raw_low):
    """Cross-segment prohibited patterns — evaluated on the FULL command, because a pipe (`curl … | sh`,
    `cat secret | curl`) is split away before per-segment checks see it. Exfiltration and remote-exec are
    inherently multi-segment, so they must be caught here on the whole (folded, lowered) command."""
    # remote fetch piped into an interpreter → remote code execution
    if _re.search(r"\b(?:curl|wget|fetch|httpie)\b[^\n]*\|\s*(?:sudo\s+)?(?:sh|bash|zsh|python3?|node|deno|bun|ruby|perl|php)\b", raw_low):
        return "remote code execution (fetch | shell) — never"
    net = bool(_re.search(r"\b(?:curl|wget|nc|ncat|netcat|scp|sftp|rsync|ssh|telnet|ftp|socat|httpie)\b", raw_low))
    if net:
        if any(sub in raw_low for sub in _SECRET_PATH_SUBSTRINGS):
            return "exfiltrates a secret/credential path over the network — never"
        if _re.search(r"\b(?:env|printenv)\b", raw_low):
            return "exfiltrates the environment over the network — never"
        if _re.search(r"\$\(\s*(?:cat|printenv|env|echo)\b", raw_low) or _re.search(r"`\s*(?:cat|printenv|env)\b", raw_low):
            return "exfiltrates command-substituted data over the network — never"
    return None


def _prohibited_reason(seg, tokens, raw_low):
    prog = _program(tokens)
    tokset = set(tokens)

    # sudo / privilege escalation
    if "sudo" in tokset or "doas" in tokset or prog in ("sudo", "doas"):
        return "privilege escalation (sudo/doas) never fires autonomously"

    # remote-fetch piped into an interpreter → remote code execution
    if _re.search(r"\b(curl|wget|fetch)\b[^\n]*\|\s*(?:sudo\s+)?(sh|bash|zsh|python3?|node|deno|bun|ruby|perl|php)\b", raw_low):
        return "remote code execution (fetch | shell) — never"

    # secret write via redirection
    tgt = _has_redirect_to(tokens, seg)
    if tgt and _is_secret_path(tgt):
        return "writes a secret/credential path — never"

    # env / secret EXFILTRATION: an outbound network tool in the same command as a secret path or env dump
    net = bool(tokset & _NET_SEND) or any(p in _NET_SEND for p in (prog,))
    if net:
        if any(sub in raw_low for sub in _SECRET_PATH_SUBSTRINGS):
            return "exfiltrates a secret path over the network — never"
        if tokset & _ENV_DUMP or "printenv" in raw_low or _re.search(r"\benv\b", raw_low):
            return "exfiltrates the environment over the network — never"
        if _re.search(r"\$\(\s*(cat|printenv|env|echo)\b", raw_low) or _re.search(r"`\s*(cat|printenv|env)\b", raw_low):
            return "exfiltrates command-substituted data over the network — never"

    # rm -rf and destructive recursive deletes
    if prog == "rm":
        flags = "".join(t for t in tokens if t.startswith("-") and not t.startswith("--"))
        recursive = ("r" in flags) or ("R" in flags) or ("--recursive" in tokset)
        force = ("f" in flags) or ("--force" in tokset)
        targets = [t for t in tokens[1:] if not t.startswith("-")]
        broad = any(t in ("/", "~", "*", ".", "..", "/*", "$home", "${home}", "~/") or t.endswith("/*")
                    or t in ("$home/*",) for t in targets)
        if recursive and (force or broad):
            return "recursive/forced delete (rm -rf) — never"
        if recursive and not targets:
            return "recursive delete with no explicit target — never"

    # find with -delete / -exec rm → mass delete
    if prog == "find" and ("-delete" in tokset or _re.search(r"-exec\s+rm\b", raw_low)):
        return "find -delete / -exec rm — never"

    # disk / device / system destroyers
    if prog in ("mkfs", "fdisk", "parted", "sgdisk", "wipefs") or raw_low.startswith("mkfs"):
        return "filesystem/partition operation — never"
    if prog == "dd" and _re.search(r"of=/dev/", raw_low):
        return "dd to a device — never"
    if _re.search(r">\s*/dev/(sd|nvme|disk|hd)", raw_low):
        return "write to a raw disk device — never"
    if prog in ("shutdown", "reboot", "halt", "poweroff") or _re.match(r"^init\s+[06]\b", raw_low):
        return "system power/state change — never"
    if _re.search(r":\s*\(\s*\)\s*\{[^}]*\|[^}]*&\s*\}", seg) or ":(){:|:&};:" in seg.replace(" ", ""):
        return "fork bomb — never"

    # broad recursive permission/ownership changes
    if prog in ("chmod", "chown", "chgrp") and (("-r" in tokset) or ("-R" in tokset) or ("--recursive" in tokset)):
        targets = [t for t in tokens[1:] if not t.startswith("-")]
        if any(t in ("/", "~", "*", ".", "/*") for t in targets) or "777" in tokset:
            return "recursive permission/ownership change on a broad target — never"

    # git force-push / history rewrite / ref deletion
    if prog == "git":
        sub = _git_sub(tokens)
        if sub == "push":
            if (tokset & {"--force", "-f", "--force-with-lease", "--mirror", "--delete", "-d"}
                    or any(t.startswith("+") for t in tokens[2:] if ":" in t or t.lstrip("+"))
                    or any(t.startswith(":") for t in tokens)):
                return "force-push / ref-delete / mirror rewrites remote history — never"
        if sub in ("rebase", "filter-branch", "filter-repo"):
            return "history rewrite (git %s) — never" % sub
        if sub == "reset" and ("--hard" in tokset):
            return "git reset --hard discards work irrecoverably — never"
        if sub == "reflog" and (tokset & {"delete", "expire"}):
            return "git reflog delete/expire destroys the recovery log — never"
        if sub == "update-ref" and ("-d" in tokset):
            return "git update-ref -d deletes a ref — never"
        # -D (force-delete) / -M (force-move) are case-significant; tokens were lowercased, so match the raw seg.
        if sub == "branch" and _re.search(r"(?:^|\s)-[DM]\b", _fold(seg)):
            return "git branch force-delete/force-rename — never"
        if sub == "config" and _re.search(r"credential\.helper|user\.password|\.token", raw_low):
            return "git config writing a credential — never"

    return None


def _git_sub(tokens):
    """The git subcommand: first non-flag token after 'git' (skipping global -C/-c/--git-dir style flags)."""
    if not tokens or tokens[0] != "git":
        return ""
    i = 1
    while i < len(tokens):
        t = tokens[i]
        if t in ("-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path"):
            i += 2
            continue
        if t.startswith("-"):
            i += 1
            continue
        return t
    return ""


# ── SAFE / GATED classification for a single (non-prohibited) segment ─────────────────────────────────────
def _segment_tier(seg):
    tokens = _tokenize(seg)
    if not tokens:
        return SAFE, "empty"
    # Check the ORIGINAL (pre-fold) for ANY non-ASCII: a homoglyph that folds cleanly to a benign word
    # (lѕ→ls, gеt→get) must never auto-fire — same discipline as risk_tiers.is_read_only. A PROHIBITED
    # match still wins (it is checked first in classify_shell, on the folded form), so ｒｍ -rf still blocks;
    # a benign-looking read carrying obfuscation is merely staged, never lost.
    if any(ord(c) > 127 for c in str(seg or "")):
        return GATED, "non-ASCII in the raw command — staged, not auto-fired"

    prog = _program(tokens)
    tokset = set(tokens)

    # A redirection to a file is a WRITE (secret targets were already caught as PROHIBITED upstream).
    if _has_redirect_to(tokens, seg):
        return GATED, "redirects output to a file — staged as a write"

    # bare env/printenv (a dump) is not a read we auto-fire
    if prog in _ENV_DUMP:
        return GATED, "environment dump — staged, not auto-fired"

    # git: subcommand-driven
    if prog == "git":
        sub = _git_sub(tokens)
        if sub == "push":
            # protected-branch destination → explicit confirm every time; else a normal staged push
            refs = [t for t in tokens[_git_pos(tokens, "push") + 1:] if not t.startswith("-")]
            # refs = [remote, refspec...]; a bare `git push` (no refspec) is ambiguous → fail-safe to MAIN
            dests = []
            for r in refs[1:] or []:
                dests.append(r.split(":")[-1] if ":" in r else r)
            if not refs or len(refs) <= 1 or any(_is_protected_branch(d) for d in dests):
                return GATED_MAIN, "push to a protected/ambiguous branch — explicit confirm every time"
            return GATED, "push to a feature branch — staged"
        if sub == "branch":
            # listing forms are read; a positional new-branch name is a write
            positionals = [t for t in tokens[_git_pos(tokens, "branch") + 1:] if not t.startswith("-")]
            if not positionals:
                return SAFE, "git branch listing — read"
            return GATED, "git branch creates a ref — staged"
        if sub == "config":
            if tokset & {"--get", "--list", "-l", "--get-all", "--get-regexp"} or len([t for t in tokens[2:] if not t.startswith("-")]) <= 1:
                return SAFE, "git config read — read"
            return GATED, "git config write — staged"
        if sub in _GIT_READ_SUBS:
            return SAFE, "git %s — read/inspect" % sub
        if sub in _GIT_WRITE_SUBS or sub:
            return GATED, "git %s — staged write" % (sub or "?")
        return GATED, "unrecognized git action — staged (default-closed)"

    # sed/awk are read-only UNLESS in-place editing (-i) — those are writes
    if prog in ("sed", "awk"):
        if "-i" in tokset or any(t.startswith("-i") for t in tokens):
            return GATED, "%s in-place edit — staged" % prog
        return SAFE, "%s stream read — read" % prog

    # a version/help/typecheck-style invocation of ANY program is a read
    if tokset & _INSPECT_FLAGS:
        return SAFE, "inspect/version invocation — read"

    # recognized read-only program with no write side effect
    if prog in _SAFE_PROGRAMS:
        return SAFE, "%s — read/inspect" % prog

    # recognized write-ish filesystem ops → staged
    if prog in ("touch", "mkdir", "mv", "cp", "ln", "rm", "rmdir", "install", "tee", "patch"):
        return GATED, "%s — staged write" % prog

    # everything else (build/test/run/package-install/unknown) → default-closed: staged, never auto-fired
    return GATED, "unrecognized or side-effecting command — staged (default-closed)"


def _git_pos(tokens, sub):
    try:
        return tokens.index(sub)
    except ValueError:
        return 0


# ── the gate ─────────────────────────────────────────────────────────────────────────────────────────────
def classify_shell(cmd: str) -> CodeVerdict:
    """Classify a full shell command string. Splits into segments; PROHIBITED if ANY segment is prohibited;
    otherwise the MOST restrictive segment tier wins (a hidden mutation in a pipeline can't hide behind a read)."""
    # cross-segment prohibited patterns (exfil / remote-exec) first — a pipe hides them from per-segment checks
    whole = _prohibited_whole(_fold(str(cmd or "")).lower())
    if whole:
        return CodeVerdict(PROHIBITED, whole)
    segs = _segments(cmd)
    if not segs:
        return CodeVerdict(GATED, "empty/unparseable command — staged (default-closed)")
    worst = CodeVerdict(SAFE, "read")
    for seg in segs:
        tokens = _tokenize(seg)
        raw_low = _fold(seg).lower()
        pr = _prohibited_reason(seg, tokens, raw_low)
        if pr:
            return CodeVerdict(PROHIBITED, pr)
        tier, reason = _segment_tier(seg)
        if _SEVERITY[tier] > _SEVERITY[worst.tier]:
            worst = CodeVerdict(tier, reason)
    return worst


# The named file-op verbs and their base tiers (path-sensitive: a secret path escalates a write to PROHIBITED).
_READ_KINDS = frozenset(("read", "list", "grep", "inspect", "diff", "show", "cat", "view", "clone", "fetch"))
_WRITE_KINDS = frozenset(("write", "edit", "create", "delete", "remove", "fork", "commit"))


def classify_file_op(kind: str, path: str = "", branch: str = "") -> CodeVerdict:
    """Classify a structured (non-shell) coding action — the file-edit / git-object path where the executor
    already knows the verb and target. Language-AGNOSTIC by construction: the target file's extension is
    never consulted, so a .tsx edit and a .rs edit resolve identically."""
    k = _fold(str(kind or "")).strip().lower()
    if k in _READ_KINDS:
        return CodeVerdict(SAFE, "%s — read/inspect" % k)
    if k == "push":
        if _is_protected_branch(branch) or not branch:
            return CodeVerdict(GATED_MAIN, "push to a protected/ambiguous branch — explicit confirm every time")
        return CodeVerdict(GATED, "push to %s — staged" % branch)
    if k in ("write", "edit", "create", "delete", "remove"):
        if _is_secret_path(path):
            return CodeVerdict(PROHIBITED, "%s of a secret/credential path — never" % k)
        return CodeVerdict(GATED, "%s — staged as a diff, fires on OK" % k)
    if k in _WRITE_KINDS:
        return CodeVerdict(GATED, "%s — staged" % k)
    return CodeVerdict(GATED, "unrecognized code action %r — staged (default-closed)" % kind)


def classify_code_action(action) -> CodeVerdict:
    """The coding lane's single chokepoint. `action` is either:
        • a str                                   → treated as a shell command
        • {"kind": "shell", "cmd": "..."}         → shell command
        • {"kind": "<verb>", "path": "...", "branch": "..."}  → structured file/git op
    Never raises; never returns SAFE for anything unrecognized (fail-closed)."""
    try:
        if isinstance(action, str):
            return classify_shell(action)
        if isinstance(action, dict):
            kind = str(action.get("kind", "")).lower()
            if kind in ("shell", "cmd", "command", "run", "run_command", "bash"):
                return classify_shell(action.get("cmd") or action.get("command") or "")
            return classify_file_op(kind, action.get("path", ""), action.get("branch", ""))
        return CodeVerdict(GATED, "unknown action shape — staged (default-closed)")
    except Exception as e:  # never let a classifier crash open — fail closed to staged
        return CodeVerdict(GATED, "classifier error (%s) — staged, fail-closed" % type(e).__name__)
