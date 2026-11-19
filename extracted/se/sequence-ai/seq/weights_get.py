"""
`seq weights get` and `seq serve`'s weights: an official template's weights on this machine - one version's files, each
checked by its sha256, kept under ~/.cache/sequence-ai/weights/<template>/v<N> ($SEQ_WEIGHTS_DIR, or a folder named).

In one sentence: GET /v1/templates/{name}/weights with your key → each file's size, sha256 and a URL signed for an hour
→ each file this machine does not hold already is read from its URL into `<file>.part`, hashed as it arrives, and put in
place only when its size and sha256 are the listed ones → a file whose URL ran out is asked for again → `.complete` is
written last, so a folder that has it holds every file.

WHY by sha256: they are the bytes a deployment of the template reads, so a policy served here answers as it does on the
platform. WHY kept: pi05-libero's are 12.4 GB, and a second `seq serve` reads none of them again.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import threading
from pathlib import Path
from typing import Any, Callable

import httpx

from seq.errors import raise_for, unreachable

CACHE_ENV = "SEQ_WEIGHTS_DIR"
COMPLETE = ".complete"
VERIFIED = ".verified.json"
_CHUNK = 8 * 1024 * 1024
_EXPIRED = (401, 403, 410)


class _Expired(Exception):
    """A file's URL ran out before it was read: ask for the list again."""


def cache_dir() -> Path:
    """Where weights are kept when no folder is named: $SEQ_WEIGHTS_DIR, else ~/.cache/sequence-ai/weights."""
    return Path(os.environ.get(CACHE_ENV) or Path.home() / ".cache" / "sequence-ai" / "weights")


def listing(name: str, version: str | None = None, *, api_key: str | None = None,
            base_url: str | None = None) -> dict[str, Any]:
    """The platform's list of one version of template `name`'s weights (the latest when `version` is None): each file's
    path, size, sha256 and URL, and the license and source they come with."""
    from seq import template_fetch
    from seq._account import auth_headers, credential
    from seq._http import RetryReads

    base = template_fetch._base(base_url)
    try:
        with httpx.Client(headers=auth_headers(credential(api_key, base_url)), timeout=60,
                          transport=RetryReads()) as client:
            r = client.get(f"{base}/v1/templates/{template_fetch.segment(name)}/weights",
                           params={"version": version} if version else None)
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    raise_for(r)
    return r.json()


def _version(version: int | str | None) -> str | None:
    """v<N> for a version given as N, "N" or "vN"; None for the latest."""
    if version is None:
        return None
    text = str(version)
    return text if text.startswith("v") else f"v{text}"


def fetch(name: str, version: int | str | None = None, *, dest: str | os.PathLike | None = None,
          api_key: str | None = None, base_url: str | None = None, say: Callable[[str], Any] = print,
          workers: int = 4) -> Path:
    """One version of template `name`'s weights in a folder of this machine (the latest when `version` is None), every
    file checked by its sha256: the folder. Files already there and checked are not read again; a version a folder holds
    whole (`.complete`) asks the platform nothing."""
    pinned = _version(version)
    if pinned and dest is None:
        held = cache_dir() / name / pinned
        if (held / COMPLETE).is_file():
            return held
    listed = listing(name, pinned, api_key=api_key, base_url=base_url)
    folder = Path(dest) if dest is not None else cache_dir() / name / str(listed["version"])
    folder.mkdir(parents=True, exist_ok=True)
    complete = folder / COMPLETE
    files = list(listed.get("files") or [])
    if complete.is_file() and _complete_of(complete) == _ids(files):
        return folder
    verified = _Verified(folder)
    todo = [f for f in files if not verified.holds(f)]
    if todo:
        size = sum(int(f["size"]) for f in todo)
        say(f"{name} {listed['version']}: {len(todo)} of {len(files)} files to download, {size / 1e9:.2f} GB, "
            f"into {folder}")
    for attempt in range(2):
        urls = {f["path"]: f.get("url") for f in (listed.get("files") or [])}
        expired: list[dict] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            jobs = {pool.submit(_download, folder, f, urls.get(f["path"]), verified): f for f in todo}
            for job in concurrent.futures.as_completed(jobs):
                try:
                    job.result()
                except _Expired:
                    expired.append(jobs[job])
        if not expired:
            break
        if attempt:
            raise _unavailable(f"{len(expired)} files of {name} {listed['version']} could not be read before their "
                               "links ran out: run the command again, and the files already here are kept")
        listed = listing(name, str(listed["version"]), api_key=api_key, base_url=base_url)
        todo = expired
    complete.write_text(json.dumps({"template": name, "version": listed["version"], "files": _ids(files),
                                    "license": listed.get("license"), "source": listed.get("source")}, indent=1))
    if listed.get("license"):
        say(f"{name} {listed['version']}: weights under {listed['license']} - the template's LICENSE and NOTICE say "
            "its terms")
    return folder


def _ids(files: list[dict]) -> list[list[str]]:
    return sorted([str(f["path"]), str(f.get("sha256") or "")] for f in files)


def _complete_of(path: Path) -> list | None:
    try:
        return json.loads(path.read_text()).get("files")
    except (OSError, ValueError, AttributeError):
        return None


class _Verified:
    """The files of a folder already checked in place, by path and sha256: a run again hashes none of them."""

    def __init__(self, folder: Path) -> None:
        self.path = folder / VERIFIED
        self.folder = folder
        self.lock = threading.Lock()
        try:
            self.seen: dict[str, str] = json.loads(self.path.read_text())
        except (OSError, ValueError):
            self.seen = {}

    def holds(self, f: dict) -> bool:
        target = self.folder / f["path"]
        return (target.is_file() and target.stat().st_size == int(f["size"])
                and self.seen.get(str(f["path"])) == f.get("sha256"))

    def add(self, f: dict) -> None:
        with self.lock:
            self.seen[str(f["path"])] = str(f.get("sha256"))
            tmp = self.path.with_name(self.path.name + ".part")
            tmp.write_text(json.dumps(self.seen, indent=0, sort_keys=True))
            os.replace(tmp, self.path)


def _download(folder: Path, f: dict, url: str | None, verified: _Verified) -> None:
    """Read one file from its URL into place, checked by its size and sha256 before it takes its place."""
    target = folder / f["path"]
    if folder.resolve() not in target.resolve().parents:
        raise _unavailable(f"{f['path']}: a path outside the weights folder")
    target.parent.mkdir(parents=True, exist_ok=True)
    part = target.with_name(target.name + ".part")
    digest = hashlib.sha256()
    if int(f["size"]) == 0:
        part.write_bytes(b"")
    else:
        if not url:
            raise _unavailable(f"{f['path']}: the platform gave no link to read it from")
        from seq import template_fetch
        from seq._http import RetryReads


        with httpx.Client(headers=template_fetch._headers(), timeout=httpx.Timeout(30.0, read=120.0),
                          transport=RetryReads(), follow_redirects=True) as client:
            with client.stream("GET", url) as r:
                if r.status_code in _EXPIRED:
                    raise _Expired(f["path"])
                if r.status_code >= 400:
                    raise _unavailable(f"{f['path']}: its link answered {r.status_code}")
                with part.open("wb") as out:
                    for chunk in r.iter_bytes(_CHUNK):
                        digest.update(chunk)
                        out.write(chunk)
    size = part.stat().st_size
    got = digest.hexdigest()
    if size != int(f["size"]) or (f.get("sha256") and got != f["sha256"]):
        part.unlink(missing_ok=True)
        raise _unavailable(f"{f['path']}: {size} bytes with sha256 {got[:12]}, where the template lists "
                           f"{f['size']} bytes and {str(f.get('sha256'))[:12]}: run the command again")
    os.replace(part, target)
    verified.add(f)


def _unavailable(message: str) -> Exception:
    from sequence_ai.errors import Unavailable

    return Unavailable(message)
