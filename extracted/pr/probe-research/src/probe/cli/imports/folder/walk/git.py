"""the folder's local git identity and a bounded, deterministic digest of its history."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path


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
    from probe.sdk.capture.code.git import _git
    from probe.sdk.capture.code.git_remote import _remote_url

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
    index = lowered.find("github.com")
    if index == -1:
        return None
    # `github.com` must be the HOST, not a path segment: it may follow userinfo
    # (`@`), a scheme (`//`), or the string start. A single `/` before it is a
    # path — `https://evil.com/github.com/attacker/repo` is NOT github.com, and
    # accepting it would let a hostile imported .git/config steer the wizard's
    # `probe project code attach` suggestion at an attacker-named repo. `gist.`
    # / `evilgithub.com` are excluded because the char before the match is a
    # host character, not `@`/`/`/start.
    before = text[index - 1] if index > 0 else ""
    at_host = index == 0 or before == "@" or (before == "/" and index >= 2 and text[index - 2] == "/")
    if not at_host:
        return None
    tail = text[index + len("github.com") :]
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

    from probe.sdk.capture.code.git import _git

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
