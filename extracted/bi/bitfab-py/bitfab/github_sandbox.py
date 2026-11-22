from __future__ import annotations

import base64
import datetime
import difflib
import hashlib
import json
import os
import re
import shutil
import sys
import tarfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from bitfab.mock_override import MockOverrideCtx, SpanNodeMeta
from bitfab.sandbox import Sandbox, SandboxStartCtx, recorded_state

GITHUB_SANDBOX_NAME = "GitHub"
API_URL = "https://api.github.com"
GIT_URL = "https://github.com"
DOCS_URL = "https://docs.github.com/rest"
REPLAY_TOKEN = "bitfab-replay-token"
TOKEN_ENV = "GITHUB_TOKEN"
CACHE_DIR_ENV = "BITFAB_GITHUB_CACHE_DIR"
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "bitfab" / "github"
REF_READ_TIMEOUT_SECONDS = 10.0
EXPLICIT_REF_READ_TIMEOUT_SECONDS = 60.0
UPSTREAM_TIMEOUT_SECONDS = 300.0
FIRST_REPLAY_PULL = 1_000_000
SEARCH_MAX_FILE_BYTES = 384 * 1024
DIFF_MAX_BLOB_BYTES = 256 * 1024
JSON_TYPE = "application/json; charset=utf-8"
JSON_ACCEPT = "application/vnd.github+json"
USER_AGENT = "bitfab-github-sandbox"
ARCHIVE_TYPES = {"tarball": "application/x-gzip", "zipball": "application/zip"}
ARCHIVE_SUFFIXES = {"tarball": "tar.gz", "zipball": "zip"}
KEPT_HEADERS = ("Content-Type", "Link")
ANCESTOR_STATUSES = ("ahead", "identical")
REPLAY_PERSON = {"name": "Bitfab replay", "email": "replay@sandbox.invalid"}
SHORT_SHA = re.compile(r"^[0-9a-f]{7,40}$")
REPO_PATH = re.compile(r"^/repos/(?P<owner>[^/]+)/(?P<name>[^/]+)(?P<rest>/.*)?$")
TOKEN_PATH = re.compile(r"^/app/installations/[^/]+/access_tokens$")
SEARCH_TOKEN = re.compile(r'"[^"]*"|\S+')
SKIPPED_SEARCH_QUALIFIERS = ("language", "org", "user", "in", "size", "fork")

Reader = Callable[[str, str], tuple[int, dict[str, str], bytes]]

_archive_lock = threading.Lock()


@dataclass(frozen=True)
class Upstream:
    reader: Reader
    cache_dir: Path


@dataclass(frozen=True)
class GitHubRequest:
    state: dict[str, Any]
    upstream: Upstream
    repo: dict[str, Any]
    method: str
    query: dict[str, Any]
    body: Any

    @property
    def name(self) -> str:
        return self.repo["repo"]

    @property
    def base(self) -> str:
        return f"/repos/{self.repo['repo']}"


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_time(value: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def git_object_sha(kind: str, payload: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(payload)}\0".encode() + payload).hexdigest()


def tree_entry_bytes(entry: dict[str, Any]) -> bytes:
    mode = entry["mode"].lstrip("0") or "0"
    return f"{mode} {entry['path']}".encode() + b"\0" + bytes.fromhex(entry["sha"])


def tree_sort_key(entry: dict[str, Any]) -> bytes:
    name = entry["path"].encode()
    return name + b"/" if entry["type"] == "tree" else name


def hash_tree(entries: list[dict[str, Any]]) -> str:
    ordered = sorted(entries, key=tree_sort_key)
    return git_object_sha("tree", b"".join(tree_entry_bytes(e) for e in ordered))


def pkt_line(text: str) -> bytes:
    payload = text.encode("utf-8")
    return f"{len(payload) + 4:04x}".encode("ascii") + payload


LS_REFS_REQUEST = b"".join(
    [
        pkt_line("command=ls-refs\n"),
        pkt_line("object-format=sha1\n"),
        b"0001",
        pkt_line("peel\n"),
        pkt_line("symrefs\n"),
        pkt_line("ref-prefix HEAD\n"),
        pkt_line("ref-prefix refs/heads/\n"),
        pkt_line("ref-prefix refs/tags/\n"),
        b"0000",
    ]
)


def pkt_lines(data: bytes) -> Iterator[str]:
    position = 0
    while position + 4 <= len(data):
        length = int(data[position : position + 4], 16)
        if length < 4:
            position += 4
            continue
        yield data[position + 4 : position + length].decode("utf-8").rstrip("\n")
        position += length


def parse_ls_refs(data: bytes) -> dict[str, Any]:
    default_branch: str | None = None
    branches: dict[str, str] = {}
    tags: dict[str, str] = {}
    for line in pkt_lines(data):
        if line.startswith("ERR "):
            raise RuntimeError(f"GitHub refused the ref read: {line[4:]}")
        sha, _, rest = line.partition(" ")
        ref, *attributes = rest.split(" ")
        symref = next(
            (
                a[len("symref-target:") :]
                for a in attributes
                if a.startswith("symref-target:")
            ),
            None,
        )
        peeled = next(
            (a[len("peeled:") :] for a in attributes if a.startswith("peeled:")), None
        )
        if ref == "HEAD" and symref and symref.startswith("refs/heads/"):
            default_branch = symref[len("refs/heads/") :]
        elif ref.startswith("refs/heads/"):
            branches[ref[len("refs/heads/") :]] = sha
        elif ref.startswith("refs/tags/"):
            tags[ref[len("refs/tags/") :]] = peeled or sha
    return {
        "defaultBranch": default_branch,
        "branches": dict(sorted(branches.items())),
        "tags": dict(sorted(tags.items())),
    }


def read_repo_refs(
    repo: str, token: str | None, timeout: float = EXPLICIT_REF_READ_TIMEOUT_SECONDS
) -> dict[str, Any]:
    headers = {
        "Git-Protocol": "version=2",
        "Content-Type": "application/x-git-upload-pack-request",
        "Accept": "application/x-git-upload-pack-result",
        "User-Agent": "git/2.43 bitfab",
    }
    if token:
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode("ascii")
        headers["Authorization"] = f"Basic {basic}"
    request = urllib.request.Request(
        f"{GIT_URL}/{repo}.git/git-upload-pack",
        data=LS_REFS_REQUEST,
        method="POST",
        headers=headers,
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        refs = parse_ls_refs(response.read())
    if refs["defaultBranch"] is None:
        raise RuntimeError(f"GitHub reported no default branch for {repo}")
    return {"repo": repo, **refs}


def github_snapshot(
    repos: list[str],
    token: str | None,
    timeout: float = EXPLICIT_REF_READ_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    captured_at = now_iso()
    names = list(dict.fromkeys(repo.strip().strip("/") for repo in repos))
    bad = [name for name in names if name.count("/") != 1]
    if bad:
        raise ValueError(
            f"record_github_refs takes repos as owner/name; got {', '.join(bad)}"
        )
    return {
        "capturedAt": captured_at,
        "repos": [read_repo_refs(name, token, timeout) for name in names],
    }


def record_github_refs(
    repos: list[str], token: str | None = None, _timeout: float | None = None
) -> None:
    """Record the GitHub snapshot a replay of this trace starts from.

    Reads every branch and tag head and the default branch of each repo, and
    records them on the current trace for the GitHub sandbox. Call it once at
    the start of a run that works on several repos. A run on one repo gets it
    without this call when ``Bitfab(integrations={"github": True})`` is on.
    The first recording in a trace is kept. Outside a trace it reads the
    refs and records nothing.

    Args:
        repos: Repos as ``"owner/name"``.
        token: A GitHub token that can read the repos. ``None`` uses the
            ``GITHUB_TOKEN`` environment variable, then reads without one,
            which works only for public repos.

    Raises:
        ValueError: When a repo is not ``owner/name``.
        RuntimeError: When GitHub refuses or a repo has no default branch.
    """
    snapshot = github_snapshot(
        repos,
        token or os.environ.get(TOKEN_ENV),
        _timeout or EXPLICIT_REF_READ_TIMEOUT_SECONDS,
    )
    client = sys.modules.get("bitfab.client")
    if client is not None:
        client.get_current_trace().record_sandbox_state(GITHUB_SANDBOX_NAME, snapshot)


def url_reader(token: str | None) -> Reader:
    def read(path: str, accept: str) -> tuple[int, dict[str, str], bytes]:
        headers = {
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(API_URL + path, headers=headers)
        try:
            with urllib.request.urlopen(
                request, timeout=UPSTREAM_TIMEOUT_SECONDS
            ) as response:
                return response.status, dict(response.headers), response.read()
        except urllib.error.HTTPError as error:
            return error.code, dict(error.headers or {}), error.read()

    return read


def empty_writes() -> dict[str, Any]:
    return {
        "blobs": {},
        "trees": {},
        "commits": {},
        "branches": {},
        "deletedBranches": {},
        "pulls": {},
        "nextPull": FIRST_REPLAY_PULL,
    }


def _repo_entry(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "repo": raw["repo"],
        "defaultBranch": raw.get("defaultBranch") or raw.get("default_branch"),
        "branches": dict(raw.get("branches") or {}),
        "tags": dict(raw.get("tags") or {}),
    }


def state_from_snapshot(snapshot: Any) -> dict[str, Any]:
    given = snapshot if isinstance(snapshot, dict) else {}
    repos = [
        _repo_entry(repo)
        for repo in given.get("repos") or []
        if isinstance(repo, dict) and repo.get("repo")
    ]
    notes = list(given.get("notes") or [])
    if not repos:
        notes.append(
            "The original trace has no GitHub snapshot, so every repo call answers "
            "404 instead of guessing which commit the repo was at."
        )
    return {
        "capturedAt": given.get("capturedAt"),
        "repos": repos,
        "writes": {**empty_writes(), **(given.get("writes") or {})},
        "served": {"trees": {}, "blobs": {}, **(given.get("served") or {})},
        "resolvedHeads": dict(given.get("resolvedHeads") or {}),
        "notes": notes,
    }


def _result(
    status: int,
    body: Any,
    treatment: str,
    source: str = "sandbox",
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "status": status,
        "headers": {"Content-Type": JSON_TYPE, **(headers or {})},
        "json": body,
        "treatment": treatment,
        "source": source,
    }


def _not_found(treatment: str, message: str = "Not Found") -> dict[str, Any]:
    return _result(
        404,
        {"message": message, "documentation_url": DOCS_URL, "status": "404"},
        treatment,
    )


def _refused(why: str) -> dict[str, Any]:
    return _result(403, {"message": f"Refused by the replay sandbox: {why}"}, "refused")


def _no_snapshot(repo: str) -> dict[str, Any]:
    return _not_found(
        "refused",
        f"This trace has no GitHub snapshot, so the GitHub sandbox cannot tell "
        f"which commit {repo} was at. Record one on the original run with "
        f'bitfab.record_github_refs(["{repo}"]) or turn on '
        f'Bitfab(integrations={{"github": True}}).',
    )


def _not_in_snapshot(repo: str) -> dict[str, Any]:
    return _not_found(
        "refused",
        f"This trace's GitHub snapshot does not include {repo}. Record it on the "
        f'original run with bitfab.record_github_refs(["{repo}", ...]).',
    )


def _kept_headers(headers: dict[str, str]) -> dict[str, str]:
    lowered = {key.lower(): value for key, value in headers.items()}
    return {
        name: lowered[name.lower()] for name in KEPT_HEADERS if name.lower() in lowered
    }


def _repo_dir(upstream: Upstream, repo: str) -> Path:
    return upstream.cache_dir / repo.lower().replace("/", "__")


def _fetch(
    upstream: Upstream, repo: str, path: str, keep: bool, accept: str = JSON_ACCEPT
) -> tuple[int, dict[str, str], bytes, str]:
    folder = _repo_dir(upstream, repo) / "answers"
    key = hashlib.sha256(f"{accept} {path}".encode()).hexdigest()
    meta_file = folder / f"{key}.json"
    body_file = folder / f"{key}.body"
    if keep and meta_file.exists() and body_file.exists():
        meta = json.loads(meta_file.read_text())
        return meta["status"], meta["headers"], body_file.read_bytes(), "cache"
    status, headers, body = upstream.reader(path, accept)
    kept = _kept_headers(headers)
    if keep and status in (200, 404):
        folder.mkdir(parents=True, exist_ok=True)
        body_file.write_bytes(body)
        meta_file.write_text(
            json.dumps({"status": status, "headers": kept, "path": path})
        )
    return status, kept, body, "github"


def _decoded(body: bytes) -> Any:
    if not body:
        return None
    return json.loads(body)


def _forwarded(
    status: int, headers: dict[str, str], body: bytes, treatment: str, source: str
) -> dict[str, Any]:
    try:
        parsed = _decoded(body)
    except ValueError:
        return {
            "status": status,
            "headers": headers,
            "text": body.decode("utf-8", "replace"),
            "treatment": treatment,
            "source": source,
        }
    return _result(status, parsed, treatment, source, headers)


def _fetch_json(req: GitHubRequest, path: str) -> Any:
    status, _, body, _ = _fetch(req.upstream, req.name, path, keep=True)
    if status != 200:
        return None
    return json.loads(body)


def _query_value(query: dict[str, Any], name: str) -> str | None:
    value = query.get(name)
    if isinstance(value, list):
        value = value[-1] if value else None
    return None if value is None else str(value)


def _query_string(query: dict[str, Any]) -> str:
    return urllib.parse.urlencode(sorted(query.items()), doseq=True)


def _mark(state: dict[str, Any], kind: str, sha: Any) -> None:
    if isinstance(sha, str):
        state["served"][kind][sha] = True


def _mark_tree(state: dict[str, Any], data: Any) -> None:
    if not isinstance(data, dict):
        return
    _mark(state, "trees", data.get("sha"))
    for entry in data.get("tree") or []:
        if entry.get("type") == "tree":
            _mark(state, "trees", entry.get("sha"))
        elif entry.get("type") == "blob":
            _mark(state, "blobs", entry.get("sha"))


def _mark_contents(state: dict[str, Any], data: Any) -> None:
    for item in data if isinstance(data, list) else [data]:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "file":
            _mark(state, "blobs", item.get("sha"))
        elif item.get("type") == "dir":
            _mark(state, "trees", item.get("sha"))


def _mark_commit(state: dict[str, Any], data: Any) -> None:
    if not isinstance(data, dict):
        return
    commit = data.get("commit") if isinstance(data.get("commit"), dict) else data
    _mark(state, "trees", (commit.get("tree") or {}).get("sha"))


def _writes(state: dict[str, Any]) -> dict[str, Any]:
    return state["writes"]


def _own_commit(state: dict[str, Any], sha: str) -> str | None:
    commits = _writes(state)["commits"]
    if sha in commits:
        return sha
    return next((own for own in commits if own.startswith(sha)), None)


def _branches(state: dict[str, Any], repo: dict[str, Any]) -> dict[str, str]:
    name = repo["repo"]
    deleted = set(_writes(state)["deletedBranches"].get(name) or [])
    merged = {b: sha for b, sha in repo["branches"].items() if b not in deleted}
    merged.update(_writes(state)["branches"].get(name) or {})
    return merged


def _remember_head(state: dict[str, Any], repo: dict[str, Any], sha: str) -> None:
    heads = state["resolvedHeads"].setdefault(repo["repo"], [])
    if sha not in heads and _own_commit(state, sha) is None:
        heads.append(sha)


def _resolve(
    state: dict[str, Any], repo: dict[str, Any], ref: str | None
) -> tuple[str | None, bool]:
    name = urllib.parse.unquote(ref or "")
    if name in ("", "HEAD"):
        name = repo["defaultBranch"] or ""
    for prefix in ("refs/heads/", "heads/"):
        if name.startswith(prefix):
            name = name[len(prefix) :]
    branches = _branches(state, repo)
    if name in branches:
        return branches[name], True
    tag = name
    for prefix in ("refs/tags/", "tags/"):
        if tag.startswith(prefix):
            tag = tag[len(prefix) :]
    if tag in repo["tags"]:
        return repo["tags"][tag], True
    if SHORT_SHA.fullmatch(name):
        return name, False
    return None, False


def _ancestor_verdict(upstream: Upstream, repo: str, sha: str, head: str) -> str | None:
    folder = _repo_dir(upstream, repo) / "ancestry"
    verdict_file = folder / f"{sha}...{head}"
    if verdict_file.exists():
        return verdict_file.read_text().strip() or None
    status, _, body = upstream.reader(
        f"/repos/{repo}/compare/{sha}...{head}?per_page=1", JSON_ACCEPT
    )
    if status == 200:
        data = json.loads(body)
        full = (
            (data.get("base_commit") or {}).get("sha") or ""
            if data.get("status") in ANCESTOR_STATUSES
            else ""
        )
    elif status in (404, 422):
        full = ""
    else:
        return None
    folder.mkdir(parents=True, exist_ok=True)
    verdict_file.write_text(full)
    return full or None


def available_commit(
    state: dict[str, Any], upstream: Upstream, repo: dict[str, Any], sha: str
) -> str | None:
    own = _own_commit(state, sha)
    if own is not None:
        return own
    heads = [*repo["branches"].values(), *repo["tags"].values()]
    named = next((head for head in heads if head.startswith(sha)), None)
    if named is not None:
        return named
    default_head = repo["branches"].get(repo["defaultBranch"] or "")
    candidates = list(
        dict.fromkeys(
            [
                *([default_head] if default_head else []),
                *(state["resolvedHeads"].get(repo["repo"]) or []),
            ]
        )
    )
    for head in candidates:
        verdict = _ancestor_verdict(upstream, repo["repo"], sha, head)
        if verdict:
            return verdict
    return None


def _commit_for(req: GitHubRequest, ref: str | None) -> tuple[str | None, str]:
    sha, named = _resolve(req.state, req.repo, ref)
    if sha is None:
        return None, "branch-to-commit"
    if named:
        _remember_head(req.state, req.repo, sha)
        return sha, "branch-to-commit"
    full = available_commit(req.state, req.upstream, req.repo, sha)
    if full is None:
        return None, "refused"
    return full, "commit"


def _tree_entries(req: GitHubRequest, tree_sha: str) -> list[dict[str, Any]]:
    trees = _writes(req.state)["trees"]
    if tree_sha in trees:
        return [dict(entry) for entry in trees[tree_sha]]
    data = _fetch_json(req, f"{req.base}/git/trees/{tree_sha}")
    if data is None:
        raise KeyError(tree_sha)
    return [{k: e[k] for k in ("path", "mode", "type", "sha")} for e in data["tree"]]


def _commit_tree(req: GitHubRequest, commit_sha: str) -> str:
    commits = _writes(req.state)["commits"]
    if commit_sha in commits:
        return commits[commit_sha]["tree"]
    data = _fetch_json(req, f"{req.base}/git/commits/{commit_sha}")
    if data is None:
        raise KeyError(commit_sha)
    return data["tree"]["sha"]


def _blob(req: GitHubRequest, blob_sha: str) -> bytes:
    blobs = _writes(req.state)["blobs"]
    if blob_sha in blobs:
        return base64.b64decode(blobs[blob_sha])
    data = _fetch_json(req, f"{req.base}/git/blobs/{blob_sha}")
    if data is None:
        raise KeyError(blob_sha)
    return base64.b64decode(data["content"])


def _find_path(req: GitHubRequest, tree_sha: str, path: str) -> dict[str, Any] | None:
    entry: dict[str, Any] = {
        "type": "tree",
        "sha": tree_sha,
        "path": "",
        "mode": "040000",
    }
    for part in [p for p in path.strip("/").split("/") if p]:
        if entry["type"] != "tree":
            return None
        match = next(
            (e for e in _tree_entries(req, entry["sha"]) if e["path"] == part), None
        )
        if match is None:
            return None
        entry = match
    return entry


def _store_blob(state: dict[str, Any], content: bytes) -> str:
    sha = git_object_sha("blob", content)
    _writes(state)["blobs"][sha] = base64.b64encode(content).decode("ascii")
    return sha


def _store_tree(state: dict[str, Any], entries: list[dict[str, Any]]) -> str:
    sha = hash_tree(entries)
    _writes(state)["trees"][sha] = entries
    return sha


def replace_path(
    req: GitHubRequest,
    tree_sha: str | None,
    parts: list[str],
    blob_sha: str | None,
    mode: str = "100644",
) -> str | None:
    entries = _tree_entries(req, tree_sha) if tree_sha else []
    name = parts[0]
    existing = next((e for e in entries if e["path"] == name), None)
    entries = [e for e in entries if e["path"] != name]
    if len(parts) == 1:
        if blob_sha is not None:
            entries.append(
                {
                    "path": name,
                    "mode": existing["mode"] if existing else mode,
                    "type": "blob",
                    "sha": blob_sha,
                }
            )
    else:
        sub_tree = existing["sha"] if existing and existing["type"] == "tree" else None
        new_sub = replace_path(req, sub_tree, parts[1:], blob_sha, mode)
        if new_sub is not None:
            entries.append(
                {"path": name, "mode": "040000", "type": "tree", "sha": new_sub}
            )
    if not entries:
        return None
    return _store_tree(req.state, entries)


def store_commit(
    state: dict[str, Any],
    tree: str,
    parents: list[str],
    message: str,
    author: dict[str, Any] | None,
) -> str:
    person = {
        "name": (author or REPLAY_PERSON).get("name") or REPLAY_PERSON["name"],
        "email": (author or REPLAY_PERSON).get("email") or REPLAY_PERSON["email"],
    }
    stamp = int(time.time())
    signature = f"{person['name']} <{person['email']}> {stamp} +0000"
    lines = [f"tree {tree}"] + [f"parent {p}" for p in parents]
    lines += [f"author {signature}", f"committer {signature}", "", message]
    sha = git_object_sha("commit", "\n".join(lines).encode())
    when = datetime.datetime.fromtimestamp(stamp, datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    _writes(state)["commits"][sha] = {
        "sha": sha,
        "tree": tree,
        "parents": parents,
        "message": message,
        "author": {**person, "date": when},
        "committer": {**person, "date": when},
    }
    return sha


def commit_response(sha: str, commit: dict[str, Any]) -> dict[str, Any]:
    return {
        "sha": sha,
        "commit": {
            "message": commit["message"],
            "tree": {"sha": commit["tree"]},
            "author": commit["author"],
            "committer": commit["committer"],
        },
        "parents": [{"sha": p} for p in commit["parents"]],
    }


def _git_commit_response(commit: dict[str, Any]) -> dict[str, Any]:
    return {
        **commit,
        "tree": {"sha": commit["tree"]},
        "parents": [{"sha": p} for p in commit["parents"]],
    }


def contents_from_tree(
    req: GitHubRequest, commit_sha: str, path: str, ref_label: str
) -> tuple[int, Any]:
    entry = _find_path(req, _commit_tree(req, commit_sha), path)
    if entry is None:
        return 404, {"message": "Not Found", "status": "404"}
    clean = path.strip("/")
    if entry["type"] == "tree":
        listing = []
        for child in _tree_entries(req, entry["sha"]):
            child_path = f"{clean}/{child['path']}".strip("/")
            listing.append(
                {
                    "name": child["path"],
                    "path": child_path,
                    "sha": child["sha"],
                    "type": "dir" if child["type"] == "tree" else "file",
                    "url": f"{API_URL}{req.base}/contents/{child_path}?ref={ref_label}",
                }
            )
        return 200, listing
    content = _blob(req, entry["sha"])
    return 200, {
        "type": "file",
        "encoding": "base64",
        "size": len(content),
        "name": clean.rsplit("/", 1)[-1],
        "path": clean,
        "sha": entry["sha"],
        "content": base64.encodebytes(content).decode(),
        "url": f"{API_URL}{req.base}/contents/{clean}?ref={ref_label}",
    }


def _sha_not_found(treatment: str, ref: str) -> dict[str, Any]:
    return _result(
        422,
        {
            "message": f"No commit found for SHA: {ref}",
            "documentation_url": DOCS_URL,
            "status": "422",
        },
        treatment,
    )


def _read_repo_info(req: GitHubRequest) -> dict[str, Any]:
    status, headers, body, source = _fetch(req.upstream, req.name, req.base, keep=False)
    if status != 200:
        return _forwarded(status, headers, body, "repo-info-approximate", source)
    info = json.loads(body)
    info["default_branch"] = req.repo["defaultBranch"]
    return _result(200, info, "repo-info-approximate", source)


def _read_contents(req: GitHubRequest, path: str | None) -> dict[str, Any]:
    ref = _query_value(req.query, "ref")
    sha, treatment = _commit_for(req, ref)
    clean = urllib.parse.unquote(path or "")
    if sha is None:
        return _not_found(treatment, f"No commit found for the ref {ref}")
    if sha in _writes(req.state)["commits"]:
        status, body = contents_from_tree(req, sha, clean, ref or sha)
        return _result(status, body, "replay-writes")
    status, headers, raw, source = _fetch(
        req.upstream,
        req.name,
        f"{req.base}/contents/{urllib.parse.quote(clean)}?ref={sha}",
        keep=True,
    )
    answer = _forwarded(status, headers, raw, treatment, source)
    if status == 200:
        _mark_contents(req.state, answer.get("json"))
    return answer


def _read_readme(req: GitHubRequest, folder: str | None) -> dict[str, Any]:
    sha, treatment = _commit_for(req, _query_value(req.query, "ref"))
    if sha is None or sha in _writes(req.state)["commits"]:
        return _not_found(treatment)
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/readme{folder or ''}?ref={sha}", keep=True
    )
    answer = _forwarded(status, headers, raw, treatment, source)
    if status == 200:
        _mark_contents(req.state, answer.get("json"))
    return answer


def _flatten_tree(
    req: GitHubRequest, tree_sha: str, prefix: str
) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []
    for entry in _tree_entries(req, tree_sha):
        path = f"{prefix}{entry['path']}"
        flat.append({**entry, "path": path})
        if entry["type"] != "tree":
            continue
        if entry["sha"] in _writes(req.state)["trees"]:
            flat.extend(_flatten_tree(req, entry["sha"], f"{path}/"))
            continue
        data = _fetch_json(req, f"{req.base}/git/trees/{entry['sha']}?recursive=1")
        for child in (data or {}).get("tree") or []:
            flat.append(
                {
                    **{k: child[k] for k in ("mode", "type", "sha")},
                    "path": f"{path}/{child['path']}",
                }
            )
    return flat


def _own_tree_answer(req: GitHubRequest, tree_sha: str) -> dict[str, Any]:
    entries = (
        _flatten_tree(req, tree_sha, "")
        if _query_value(req.query, "recursive")
        else _writes(req.state)["trees"][tree_sha]
    )
    _mark_tree(req.state, {"sha": tree_sha, "tree": entries})
    return _result(
        200, {"sha": tree_sha, "tree": entries, "truncated": False}, "replay-writes"
    )


def _forward_tree(req: GitHubRequest, sha: str, treatment: str) -> dict[str, Any]:
    recursive = "?recursive=1" if _query_value(req.query, "recursive") else ""
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/git/trees/{sha}{recursive}", keep=True
    )
    answer = _forwarded(status, headers, raw, treatment, source)
    if status == 200:
        _mark_tree(req.state, answer.get("json"))
    return answer


def _read_tree(req: GitHubRequest, ref: str) -> dict[str, Any]:
    writes = _writes(req.state)
    if ref in writes["trees"]:
        return _own_tree_answer(req, ref)
    if ref in writes["commits"]:
        tree_sha = writes["commits"][ref]["tree"]
        if tree_sha in writes["trees"]:
            return _own_tree_answer(req, tree_sha)
        return _forward_tree(req, tree_sha, "replay-writes")
    if ref in req.state["served"]["trees"]:
        return _forward_tree(req, ref, "commit")
    sha, treatment = _commit_for(req, ref)
    if sha is None:
        return _not_found(treatment)
    if sha in writes["commits"]:
        return _read_tree(req, sha)
    return _forward_tree(req, sha, treatment)


def _read_blob(req: GitHubRequest, sha: str) -> dict[str, Any]:
    blobs = _writes(req.state)["blobs"]
    if sha in blobs:
        content = base64.b64decode(blobs[sha])
        return _result(
            200,
            {
                "sha": sha,
                "size": len(content),
                "encoding": "base64",
                "content": blobs[sha],
            },
            "replay-writes",
        )
    if sha not in req.state["served"]["blobs"]:
        return _not_found("refused")
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/git/blobs/{sha}", keep=True
    )
    return _forwarded(status, headers, raw, "commit", source)


def _read_git_commit(req: GitHubRequest, sha: str) -> dict[str, Any]:
    own = _writes(req.state)["commits"].get(sha)
    if own is not None:
        return _result(200, _git_commit_response(own), "replay-writes")
    full = available_commit(req.state, req.upstream, req.repo, sha)
    if full is None:
        return _not_found("refused")
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/git/commits/{full}", keep=True
    )
    answer = _forwarded(status, headers, raw, "commit", source)
    if status == 200:
        _mark_commit(req.state, answer.get("json"))
    return answer


def _read_branches_where_head(req: GitHubRequest, sha: str) -> dict[str, Any]:
    heads = [
        {"name": n, "commit": {"sha": s}, "protected": False}
        for n, s in _branches(req.state, req.repo).items()
        if s == sha
    ]
    return _result(200, heads, "ref-list-at-trace-time")


def _read_commit(req: GitHubRequest, ref: str) -> dict[str, Any]:
    sha, treatment = _commit_for(req, ref)
    if sha is None:
        return _sha_not_found(treatment, ref)
    own = _writes(req.state)["commits"].get(sha)
    if own is not None:
        return _result(200, commit_response(sha, own), "replay-writes")
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/commits/{sha}", keep=True
    )
    answer = _forwarded(status, headers, raw, treatment, source)
    if status == 200:
        _mark_commit(req.state, answer.get("json"))
    return answer


def _read_history(req: GitHubRequest) -> dict[str, Any]:
    sha, treatment = _commit_for(req, _query_value(req.query, "sha"))
    if sha is None:
        return _not_found(treatment)
    own = []
    commits = _writes(req.state)["commits"]
    walk: str | None = sha
    while walk in commits:
        commit = commits[walk]
        own.append(commit_response(walk, commit))
        walk = commit["parents"][0] if commit["parents"] else None
    if walk is None:
        return _result(200, own, "replay-writes")
    params = {k: v for k, v in req.query.items() if k != "sha"}
    params["sha"] = walk
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/commits?{_query_string(params)}", keep=True
    )
    answer = _forwarded(
        status, headers, raw, "replay-writes" if own else treatment, source
    )
    if status == 200 and isinstance(answer.get("json"), list):
        for item in answer["json"]:
            _mark_commit(req.state, item)
        answer["json"] = own + answer["json"]
    return answer


def _blob_text(req: GitHubRequest, sha: str | None) -> list[str] | None:
    if sha is None:
        return []
    content = _blob(req, sha)
    if len(content) > DIFF_MAX_BLOB_BYTES or b"\0" in content:
        return None
    return content.decode("utf-8", "replace").splitlines(keepends=True)


def _file_change(
    req: GitHubRequest,
    path: str,
    old: dict[str, Any] | None,
    new: dict[str, Any] | None,
) -> dict[str, Any]:
    status = "added" if old is None else "removed" if new is None else "modified"
    change: dict[str, Any] = {
        "filename": path,
        "status": status,
        "sha": (new or old or {}).get("sha"),
    }
    before = _blob_text(req, old["sha"] if old else None)
    after = _blob_text(req, new["sha"] if new else None)
    if before is None or after is None:
        return {**change, "additions": 0, "deletions": 0, "changes": 0}
    lines = list(difflib.unified_diff(before, after, n=3))[2:]
    additions = sum(1 for line in lines if line.startswith("+"))
    deletions = sum(1 for line in lines if line.startswith("-"))
    return {
        **change,
        "additions": additions,
        "deletions": deletions,
        "changes": additions + deletions,
        "patch": "".join(lines),
    }


def _diff_trees(
    req: GitHubRequest, old_sha: str | None, new_sha: str | None, prefix: str
) -> list[dict[str, Any]]:
    if old_sha == new_sha:
        return []
    old = {e["path"]: e for e in _tree_entries(req, old_sha)} if old_sha else {}
    new = {e["path"]: e for e in _tree_entries(req, new_sha)} if new_sha else {}
    files: list[dict[str, Any]] = []
    for name in sorted(set(old) | set(new)):
        before, after = old.get(name), new.get(name)
        if before and after and before["sha"] == after["sha"]:
            continue
        path = f"{prefix}{name}"
        old_tree = before["sha"] if before and before["type"] == "tree" else None
        new_tree = after["sha"] if after and after["type"] == "tree" else None
        if old_tree or new_tree:
            files.extend(_diff_trees(req, old_tree, new_tree, f"{path}/"))
        old_blob = before if before and before["type"] == "blob" else None
        new_blob = after if after and after["type"] == "blob" else None
        if old_blob or new_blob:
            files.append(_file_change(req, path, old_blob, new_blob))
    return files


def _own_compare(req: GitHubRequest, base_sha: str, head_sha: str) -> dict[str, Any]:
    commits = _writes(req.state)["commits"]
    chain: list[dict[str, Any]] = []
    walk: str | None = head_sha
    while walk is not None and walk != base_sha and walk in commits:
        chain.append(commit_response(walk, commits[walk]))
        parents = commits[walk]["parents"]
        walk = parents[0] if parents else None
    if walk != base_sha:
        return _result(
            501,
            {
                "message": "The GitHub sandbox compares the replay's own commits only "
                "against a commit on their first-parent history."
            },
            "replay-writes",
        )
    files = _diff_trees(
        req, _commit_tree(req, base_sha), _commit_tree(req, head_sha), ""
    )
    return _result(
        200,
        {
            "status": "identical" if not chain else "ahead",
            "ahead_by": len(chain),
            "behind_by": 0,
            "total_commits": len(chain),
            "base_commit": {"sha": base_sha},
            "merge_base_commit": {"sha": base_sha},
            "commits": list(reversed(chain)),
            "files": files,
        },
        "replay-writes",
    )


def _read_compare(req: GitHubRequest, base: str, head: str) -> dict[str, Any]:
    base_sha, base_treatment = _commit_for(req, base)
    head_sha, head_treatment = _commit_for(req, head)
    if base_sha is None or head_sha is None:
        return _not_found(
            "refused"
            if "refused" in (base_treatment, head_treatment)
            else "branch-to-commit"
        )
    commits = _writes(req.state)["commits"]
    if base_sha in commits or head_sha in commits:
        return _own_compare(req, base_sha, head_sha)
    query = f"?{_query_string(req.query)}" if req.query else ""
    status, headers, raw, source = _fetch(
        req.upstream,
        req.name,
        f"{req.base}/compare/{base_sha}...{head_sha}{query}",
        keep=True,
    )
    return _forwarded(status, headers, raw, "branch-to-commit", source)


def _download_archive(
    req: GitHubRequest, sha: str, kind: str
) -> tuple[Path | None, dict[str, Any] | None, str]:
    folder = _repo_dir(req.upstream, req.name) / "archives"
    target = folder / f"{sha}.{ARCHIVE_SUFFIXES[kind]}"
    with _archive_lock:
        if target.exists():
            return target, None, "cache"
        status, headers, body = req.upstream.reader(f"{req.base}/{kind}/{sha}", "*/*")
        if status != 200:
            return (
                None,
                _forwarded(status, _kept_headers(headers), body, "commit", "github"),
                "github",
            )
        folder.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(target.name + ".partial")
        partial.write_bytes(body)
        partial.replace(target)
        return target, None, "github"


def _read_archive(req: GitHubRequest, kind: str, ref: str | None) -> dict[str, Any]:
    sha, treatment = _commit_for(req, ref)
    if sha is None or sha in _writes(req.state)["commits"]:
        return _not_found(treatment)
    archive, failed, source = _download_archive(req, sha, kind)
    if archive is None:
        return failed or _not_found(treatment)
    return {
        "status": 200,
        "headers": {"Content-Type": ARCHIVE_TYPES[kind]},
        "file": str(archive),
        "treatment": treatment,
        "source": source,
    }


def _page(query: dict[str, Any], rows: list[Any]) -> list[Any]:
    per_page = min(int(_query_value(query, "per_page") or "30"), 100)
    page = int(_query_value(query, "page") or "1")
    return rows[(page - 1) * per_page : page * per_page]


def _read_branch_list(req: GitHubRequest) -> dict[str, Any]:
    rows = [
        {
            "name": n,
            "commit": {"sha": s, "url": f"{API_URL}{req.base}/commits/{s}"},
            "protected": False,
        }
        for n, s in sorted(_branches(req.state, req.repo).items())
    ]
    return _result(200, _page(req.query, rows), "ref-list-at-trace-time")


def _read_tag_list(req: GitHubRequest) -> dict[str, Any]:
    rows = [
        {
            "name": n,
            "commit": {"sha": s, "url": f"{API_URL}{req.base}/commits/{s}"},
            "zipball_url": f"{API_URL}{req.base}/zipball/refs/tags/{n}",
            "tarball_url": f"{API_URL}{req.base}/tarball/refs/tags/{n}",
        }
        for n, s in sorted(req.repo["tags"].items(), reverse=True)
    ]
    return _result(200, _page(req.query, rows), "ref-list-at-trace-time")


def _read_branch(req: GitHubRequest, branch: str) -> dict[str, Any]:
    name = urllib.parse.unquote(branch)
    sha = _branches(req.state, req.repo).get(name)
    if sha is None:
        return _not_found("ref-list-at-trace-time", "Branch not found")
    own = _writes(req.state)["commits"].get(sha)
    if own is not None:
        return _result(
            200,
            {"name": name, "commit": commit_response(sha, own), "protected": False},
            "ref-list-at-trace-time",
        )
    _remember_head(req.state, req.repo, sha)
    status, _, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/commits/{sha}", keep=True
    )
    commit = json.loads(raw) if status == 200 else {"sha": sha}
    _mark_commit(req.state, commit)
    return _result(
        200,
        {"name": name, "commit": commit, "protected": False},
        "ref-list-at-trace-time",
        source,
    )


def _ref_rows(req: GitHubRequest, namespace: str | None) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if namespace in (None, "heads"):
        rows += [
            (f"heads/{n}", s) for n, s in sorted(_branches(req.state, req.repo).items())
        ]
    if namespace in (None, "tags"):
        rows += [(f"tags/{n}", s) for n, s in sorted(req.repo["tags"].items())]
    return rows


def _ref_object(req: GitHubRequest, ref: str, sha: str) -> dict[str, Any]:
    return {
        "ref": f"refs/{ref}",
        "url": f"{API_URL}{req.base}/git/refs/{ref}",
        "object": {
            "sha": sha,
            "type": "commit",
            "url": f"{API_URL}{req.base}/git/commits/{sha}",
        },
    }


def _read_refs(
    req: GitHubRequest, kind: str, namespace: str | None, name: str | None
) -> dict[str, Any]:
    wanted = f"{namespace}/{urllib.parse.unquote(name or '')}" if namespace else ""
    rows = _ref_rows(req, namespace)
    exact = [_ref_object(req, r, s) for r, s in rows if r == wanted]
    matching = [_ref_object(req, r, s) for r, s in rows if r.startswith(wanted)]
    if kind == "matching-refs":
        return _result(200, matching, "ref-list-at-trace-time")
    if kind == "ref":
        if not exact:
            return _not_found("ref-list-at-trace-time")
        return _result(200, exact[0], "ref-list-at-trace-time")
    if exact:
        return _result(200, exact[0], "ref-list-at-trace-time")
    if not matching:
        return _not_found("ref-list-at-trace-time")
    return _result(200, matching, "ref-list-at-trace-time")


def _created_by_trace_time(state: dict[str, Any], item: Any) -> bool:
    captured = state.get("capturedAt")
    created = item.get("created_at") if isinstance(item, dict) else None
    if not captured or not created:
        return True
    return parse_time(created) <= parse_time(captured)


def _read_pull_or_issue_list(req: GitHubRequest, kind: str) -> dict[str, Any]:
    query = f"?{_query_string(req.query)}" if req.query else ""
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/{kind}{query}", keep=False
    )
    if status != 200:
        return _forwarded(status, headers, raw, "outside-git-approximate", source)
    items = [i for i in json.loads(raw) if _created_by_trace_time(req.state, i)]
    if kind == "pulls":
        own = _writes(req.state)["pulls"].get(req.name) or {}
        items = [own[n] for n in sorted(own, key=int)] + items
    return _result(200, items, "outside-git-approximate", source)


def _read_pull_or_issue(
    req: GitHubRequest, kind: str, number: str, sub: str | None
) -> dict[str, Any]:
    own = (_writes(req.state)["pulls"].get(req.name) or {}).get(number)
    if own is not None and not sub:
        return _result(200, own, "replay-writes")
    status, headers, raw, source = _fetch(
        req.upstream, req.name, f"{req.base}/{kind}/{number}{sub or ''}", keep=False
    )
    return _forwarded(status, headers, raw, "outside-git-approximate", source)


READS: tuple[tuple[str, Callable[..., dict[str, Any]]], ...] = (
    (r"^$", _read_repo_info),
    (r"^/contents(?:/(?P<path>.*))?$", _read_contents),
    (r"^/readme(?P<folder>/.*)?$", _read_readme),
    (r"^/git/trees/(?P<ref>.+)$", _read_tree),
    (r"^/git/blobs/(?P<sha>[0-9a-f]{40})$", _read_blob),
    (r"^/git/commits/(?P<sha>[0-9a-f]{7,40})$", _read_git_commit),
    (r"^/commits/(?P<sha>.+?)/branches-where-head$", _read_branches_where_head),
    (r"^/commits/(?P<ref>.+)$", _read_commit),
    (r"^/commits$", _read_history),
    (r"^/compare/(?P<base>.+?)\.\.\.(?P<head>.+)$", _read_compare),
    (r"^/(?P<kind>tarball|zipball)(?:/(?P<ref>.+))?$", _read_archive),
    (r"^/branches$", _read_branch_list),
    (r"^/branches/(?P<branch>.+)$", _read_branch),
    (r"^/tags$", _read_tag_list),
    (
        r"^/git/(?P<kind>ref|matching-refs|refs)(?:/(?P<namespace>heads|tags)(?:/(?P<name>.*))?)?/?$",
        _read_refs,
    ),
    (r"^/(?P<kind>pulls|issues)$", _read_pull_or_issue_list),
    (
        r"^/(?P<kind>pulls|issues)/(?P<number>\d+)(?P<sub>/(?:files|commits|comments|reviews|events|timeline))?$",
        _read_pull_or_issue,
    ),
)


def _known_commit(req: GitHubRequest, sha: Any) -> str | None:
    if not isinstance(sha, str) or not SHORT_SHA.fullmatch(sha):
        return None
    return available_commit(req.state, req.upstream, req.repo, sha)


def _write_create_ref(req: GitHubRequest) -> dict[str, Any]:
    ref = str(req.body.get("ref") or "")
    if not ref.startswith("refs/heads/"):
        return _refused(
            f"creating {ref or 'that ref'}; the sandbox takes branch refs only"
        )
    branch = ref[len("refs/heads/") :]
    if branch in _branches(req.state, req.repo):
        return _result(422, {"message": "Reference already exists"}, "replay-writes")
    sha = _known_commit(req, req.body.get("sha"))
    if sha is None:
        return _result(422, {"message": "Object does not exist"}, "replay-writes")
    writes = _writes(req.state)
    writes["branches"].setdefault(req.name, {})[branch] = sha
    deleted = writes["deletedBranches"].get(req.name) or []
    writes["deletedBranches"][req.name] = [b for b in deleted if b != branch]
    return _result(201, _ref_object(req, f"heads/{branch}", sha), "replay-writes")


def _write_move_ref(req: GitHubRequest, ref: str) -> dict[str, Any]:
    branch = urllib.parse.unquote(ref)
    current = _branches(req.state, req.repo).get(branch)
    if current is None:
        return _result(422, {"message": "Reference does not exist"}, "replay-writes")
    new = req.body.get("sha")
    commits = _writes(req.state)["commits"]
    ancestors: set[str] = set()
    walk = new
    while walk in commits:
        parents = commits[walk]["parents"]
        ancestors.update(parents)
        walk = parents[0] if parents else None
    if current not in ancestors and current != new and not req.body.get("force"):
        return _result(
            422, {"message": "Update is not a fast forward"}, "replay-writes"
        )
    if _known_commit(req, new) is None:
        return _result(422, {"message": "Object does not exist"}, "replay-writes")
    _writes(req.state)["branches"].setdefault(req.name, {})[branch] = new
    return _result(200, _ref_object(req, f"heads/{branch}", new), "replay-writes")


def _write_delete_ref(req: GitHubRequest, ref: str) -> dict[str, Any]:
    branch = urllib.parse.unquote(ref)
    writes = _writes(req.state)
    (writes["branches"].get(req.name) or {}).pop(branch, None)
    deleted = writes["deletedBranches"].setdefault(req.name, [])
    if branch not in deleted:
        deleted.append(branch)
    return _result(204, None, "replay-writes")


def _write_blob(req: GitHubRequest) -> dict[str, Any]:
    content = req.body.get("content") or ""
    raw = (
        base64.b64decode(content)
        if req.body.get("encoding") == "base64"
        else content.encode("utf-8")
    )
    sha = _store_blob(req.state, raw)
    return _result(
        201,
        {"sha": sha, "url": f"{API_URL}{req.base}/git/blobs/{sha}"},
        "replay-writes",
    )


def _usable_tree(req: GitHubRequest, sha: Any) -> bool:
    return isinstance(sha, str) and (
        sha in _writes(req.state)["trees"] or sha in req.state["served"]["trees"]
    )


def _write_tree(req: GitHubRequest) -> dict[str, Any]:
    tree = req.body.get("base_tree")
    if tree is not None and not _usable_tree(req, tree):
        return _result(
            422, {"message": "base_tree is not a valid tree oid"}, "replay-writes"
        )
    for item in req.body.get("tree") or []:
        blob_sha = (
            _store_blob(req.state, item["content"].encode("utf-8"))
            if "content" in item
            else item.get("sha")
        )
        tree = replace_path(
            req, tree, item["path"].split("/"), blob_sha, item.get("mode", "100644")
        )
    tree = tree or _store_tree(req.state, [])
    return _result(
        201,
        {
            "sha": tree,
            "tree": _writes(req.state)["trees"].get(tree, []),
            "truncated": False,
        },
        "replay-writes",
    )


def _write_commit(req: GitHubRequest) -> dict[str, Any]:
    parents = list(req.body.get("parents") or [])
    known = [_known_commit(req, parent) for parent in parents]
    if any(sha is None for sha in known):
        return _result(
            422,
            {"message": "Parent SHA does not exist or is not a commit object"},
            "replay-writes",
        )
    sha = store_commit(
        req.state,
        req.body["tree"],
        [sha for sha in known if sha is not None],
        req.body.get("message") or "",
        req.body.get("author"),
    )
    return _result(
        201, _git_commit_response(_writes(req.state)["commits"][sha]), "replay-writes"
    )


def _write_file(req: GitHubRequest, path: str) -> dict[str, Any]:
    clean = urllib.parse.unquote(path).strip("/")
    branch = req.body.get("branch") or req.repo["defaultBranch"]
    head = _branches(req.state, req.repo).get(branch)
    if head is None:
        return _not_found("replay-writes", f"Branch {branch} not found")
    tree = _commit_tree(req, head)
    existing = _find_path(req, tree, clean)
    if existing is not None and req.body.get("sha") != existing["sha"]:
        status = 409 if req.body.get("sha") else 422
        return _result(
            status,
            {"message": f"{clean} does not match {req.body.get('sha')}"},
            "replay-writes",
        )
    if req.method == "DELETE" and existing is None:
        return _not_found("replay-writes")
    blob_sha = (
        _store_blob(req.state, base64.b64decode(req.body.get("content") or ""))
        if req.method == "PUT"
        else None
    )
    new_tree = replace_path(req, tree, clean.split("/"), blob_sha) or _store_tree(
        req.state, []
    )
    commit_sha = store_commit(
        req.state,
        new_tree,
        [head],
        req.body.get("message") or f"Update {clean}",
        req.body.get("committer"),
    )
    _writes(req.state)["branches"].setdefault(req.name, {})[branch] = commit_sha
    content = None
    if blob_sha:
        content = {
            "name": clean.rsplit("/", 1)[-1],
            "path": clean,
            "sha": blob_sha,
            "size": len(base64.b64decode(_writes(req.state)["blobs"][blob_sha])),
            "type": "file",
        }
    result = {
        "content": content,
        "commit": {
            "sha": commit_sha,
            "tree": {"sha": new_tree},
            "parents": [{"sha": head}],
            "message": req.body.get("message"),
        },
    }
    return _result(201 if existing is None else 200, result, "replay-writes")


def _write_pull(req: GitHubRequest) -> dict[str, Any]:
    head_ref = str(req.body.get("head") or "")
    base_ref = str(req.body.get("base") or "")
    head, _ = _resolve(req.state, req.repo, head_ref.split(":")[-1])
    base_sha, _ = _resolve(req.state, req.repo, base_ref)
    if head is None or base_sha is None or not head_ref or not base_ref:
        return _result(
            422,
            {"message": "Validation Failed: head or base not found"},
            "replay-writes",
        )
    writes = _writes(req.state)
    number = writes["nextPull"]
    writes["nextPull"] = number + 1
    pull = {
        "number": number,
        "state": "open",
        "title": req.body.get("title", ""),
        "body": req.body.get("body"),
        "draft": bool(req.body.get("draft")),
        "created_at": now_iso(),
        "head": {"ref": head_ref, "sha": head},
        "base": {"ref": base_ref, "sha": base_sha},
        "url": f"{API_URL}{req.base}/pulls/{number}",
        "html_url": f"{GIT_URL}/{req.name}/pull/{number}",
    }
    writes["pulls"].setdefault(req.name, {})[str(number)] = pull
    return _result(201, pull, "replay-writes")


WRITES: tuple[tuple[str, str, Callable[..., dict[str, Any]]], ...] = (
    ("POST", r"^/git/refs$", _write_create_ref),
    ("PATCH", r"^/git/refs/heads/(?P<ref>.+)$", _write_move_ref),
    ("DELETE", r"^/git/refs/heads/(?P<ref>.+)$", _write_delete_ref),
    ("POST", r"^/git/blobs$", _write_blob),
    ("POST", r"^/git/trees$", _write_tree),
    ("POST", r"^/git/commits$", _write_commit),
    ("PUT", r"^/contents/(?P<path>.+)$", _write_file),
    ("DELETE", r"^/contents/(?P<path>.+)$", _write_file),
    ("POST", r"^/pulls$", _write_pull),
)


def _safe_extract(archive: Path, target: Path) -> Path:
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as tar:
        for member in tar:
            parts = PurePosixPath(member.name).parts
            if not parts or member.name.startswith("/") or ".." in parts:
                continue
            destination = target.joinpath(*parts)
            if member.isdir():
                destination.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                destination.parent.mkdir(parents=True, exist_ok=True)
                source = tar.extractfile(member)
                if source is None:
                    continue
                with source, destination.open("wb") as out:
                    shutil.copyfileobj(source, out)
    roots = sorted(p for p in target.iterdir() if p.is_dir())
    if not roots:
        raise RuntimeError(f"the archive {archive.name} held no files")
    return roots[0]


def _extracted(req: GitHubRequest, sha: str) -> Path:
    archive, failed, _ = _download_archive(req, sha, "tarball")
    if archive is None:
        raise RuntimeError(
            f"GitHub answered {(failed or {}).get('status')} for the archive of {sha}"
        )
    target = _repo_dir(req.upstream, req.name) / "trees" / sha
    marker = target / ".complete"
    with _archive_lock:
        if marker.exists():
            return target / marker.read_text().strip()
        if target.exists():
            shutil.rmtree(target)
        root = _safe_extract(archive, target)
        marker.write_text(root.name)
        return root


def _files_under(root: Path) -> list[Path]:
    found: list[Path] = []
    for folder, children, files in os.walk(root):
        children.sort()
        for name in sorted(files):
            path = Path(folder) / name
            if path.is_file() and not path.is_symlink():
                found.append(path)
    return found


def _search_terms(
    q: str,
) -> tuple[list[str], str | None, list[str], list[str], list[str]]:
    terms: list[str] = []
    repo_name: str | None = None
    path_filters: list[str] = []
    names: list[str] = []
    extensions: list[str] = []
    for token in SEARCH_TOKEN.findall(q):
        key, sep, value = token.partition(":")
        value = value.strip('"')
        if sep and key == "repo":
            repo_name = value
        elif sep and key == "path":
            path_filters.append(value.strip("/"))
        elif sep and key == "filename":
            names.append(value)
        elif sep and key == "extension":
            extensions.append(value.lstrip("."))
        elif sep and key in SKIPPED_SEARCH_QUALIFIERS:
            continue
        else:
            terms.append(token.strip('"'))
    return terms, repo_name, path_filters, names, extensions


def _search_code(
    state: dict[str, Any], upstream: Upstream, query: dict[str, Any]
) -> dict[str, Any]:
    terms, repo_name, path_filters, names, extensions = _search_terms(
        _query_value(query, "q") or ""
    )
    repos = state["repos"]
    if not repos:
        return _no_snapshot(repo_name or "the repo")
    repo = (
        _find_repo(state, repo_name)
        if repo_name
        else (repos[0] if len(repos) == 1 else None)
    )
    if repo is None:
        return _result(
            422,
            {
                "message": "The GitHub sandbox searches only the trace's repos. Add repo:owner/name."
            },
            "search-over-commit",
        )
    if not terms:
        return _result(
            422, {"message": "Validation Failed: no search terms"}, "search-over-commit"
        )
    req = GitHubRequest(state, upstream, repo, "GET", query, None)
    sha = repo["branches"][repo["defaultBranch"]]
    root = _extracted(req, sha)
    items = []
    for file_path in _files_under(root):
        rel = file_path.relative_to(root).as_posix()
        if file_path.stat().st_size > SEARCH_MAX_FILE_BYTES:
            continue
        if path_filters and not any(
            rel.startswith(p + "/") or rel == p for p in path_filters
        ):
            continue
        if names and file_path.name not in names:
            continue
        if extensions and file_path.suffix.lstrip(".") not in extensions:
            continue
        data = file_path.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8", "replace")
        if not all(term in text for term in terms):
            continue
        blob_sha = git_object_sha("blob", data)
        _mark(state, "blobs", blob_sha)
        items.append(
            {
                "name": file_path.name,
                "path": rel,
                "sha": blob_sha,
                "url": f"{API_URL}{req.base}/contents/{rel}?ref={sha}",
                "git_url": f"{API_URL}{req.base}/git/blobs/{blob_sha}",
                "html_url": f"{GIT_URL}/{req.name}/blob/{sha}/{rel}",
                "repository": {"full_name": req.name, "name": req.name.split("/")[1]},
                "score": 1.0,
            }
        )
    return _result(
        200,
        {
            "total_count": len(items),
            "incomplete_results": False,
            "items": _page(query, items),
        },
        "search-over-commit",
    )


def _installation_token() -> dict[str, Any]:
    expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    return _result(
        201,
        {
            "token": REPLAY_TOKEN,
            "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "permissions": {},
            "repository_selection": "all",
        },
        "replay-token",
    )


def _find_repo(state: dict[str, Any], name: str) -> dict[str, Any] | None:
    return next(
        (repo for repo in state["repos"] if repo["repo"].lower() == name.lower()), None
    )


def _route_repo(
    state: dict[str, Any],
    upstream: Upstream,
    method: str,
    found: re.Match[str],
    query: dict[str, Any],
    body: Any,
) -> dict[str, Any]:
    name = f"{found.group('owner')}/{found.group('name')}"
    if not state["repos"]:
        return _no_snapshot(name)
    repo = _find_repo(state, name)
    if repo is None:
        return _not_in_snapshot(name)
    rest = found.group("rest") or ""
    req = GitHubRequest(
        state, upstream, repo, method, query, body if isinstance(body, dict) else {}
    )
    if method == "GET":
        for pattern, read in READS:
            matched = re.match(pattern, rest)
            if matched:
                return read(req, **matched.groupdict())
        return _refused(f"GET {rest or '/'} is outside code and history")
    for verb, pattern, write in WRITES:
        matched = re.match(pattern, rest)
        if verb == method and matched:
            return write(req, **matched.groupdict())
    return _refused(f"{method} {rest} is a write the sandbox does not take")


def answer_github_request(
    state: dict[str, Any], upstream: Upstream, params: dict[str, Any]
) -> dict[str, Any]:
    method = str(params.get("method") or "GET").upper()
    path = str(params.get("path") or "/")
    query = dict(params.get("query") or {})
    body = params.get("body")
    if method == "POST" and TOKEN_PATH.match(path):
        return _installation_token()
    if method == "GET" and path == "/search/code":
        return _search_code(state, upstream, query)
    found = REPO_PATH.match(path)
    if found is None:
        return _refused(
            f"{method} {path} is not a repo endpoint, code search, or an installation token"
        )
    return _route_repo(state, upstream, method, found, query, body)


def answer_github_call(
    state: dict[str, Any], call: MockOverrideCtx, upstream: Upstream
) -> dict[str, Any]:
    try:
        return answer_github_request(state, upstream, dict(call.kwargs))
    except Exception as error:
        return _result(500, {"message": f"GitHub sandbox error: {error!r}"}, "error")


def is_github_call(node: SpanNodeMeta) -> bool:
    return node.trace_function_key.startswith("github.")


def make_upstream(
    token: str | None, cache_dir: str | os.PathLike[str] | None, reader: Reader | None
) -> Upstream:
    chosen_dir = cache_dir or os.environ.get(CACHE_DIR_ENV) or DEFAULT_CACHE_DIR
    return Upstream(
        reader=reader or url_reader(token or os.environ.get(TOKEN_ENV)),
        cache_dir=Path(chosen_dir).expanduser(),
    )


def github_sandbox(
    start: Callable[[SandboxStartCtx], Any] | None = None,
    token: str | None = None,
    cache_dir: str | os.PathLike[str] | None = None,
    _reader: Reader | None = None,
) -> Sandbox:
    """The GitHub sandbox: answers GitHub REST calls during replay as of the trace's time.

    It answers calls to ``api.github.com`` made through ``requests`` (which
    PyGithub and most GitHub clients use). A branch, a tag, ``HEAD`` or no
    ref is read at the commit the trace's GitHub snapshot recorded for it;
    branch and tag lists come from the snapshot; a commit named directly is
    served only if it existed at the trace's time. Writes (branches, blobs,
    trees, commits, file updates, pull requests) stay in the sandbox for the
    rest of the replay item and never reach GitHub. Reads at a fixed commit
    are fetched from GitHub once and kept on disk. It is on by default; pass
    it only to change its snapshot, token, or cache.

    Args:
        start: Builds the starting state for one replay item from a
            ``SandboxStartCtx``. Return a snapshot:
            ``{"capturedAt": ..., "repos": [{"repo": "owner/name",
            "defaultBranch": ..., "branches": {name: sha}, "tags":
            {name: sha}}]}``. ``None`` uses the snapshot recorded on the
            original trace.
        token: A GitHub token for the reads at a fixed commit. ``None`` uses
            the ``GITHUB_TOKEN`` environment variable, then reads without
            one, which works only for public repos.
        cache_dir: Where those reads are kept. ``None`` uses
            ``BITFAB_GITHUB_CACHE_DIR``, then ``~/.cache/bitfab/github``.
    """
    upstream = make_upstream(token, cache_dir, _reader)
    chosen = start or recorded_state
    return Sandbox(
        name=GITHUB_SANDBOX_NAME,
        match=is_github_call,
        handle=lambda state, call: answer_github_call(state, call, upstream),
        start=lambda ctx: state_from_snapshot(chosen(ctx)),
        integration="github",
        load=lambda _ctx, value: state_from_snapshot(value),
    )
