"""
`seq volume put | ls | rm` — upload your own checkpoint or dataset to the platform, list, delete.

In one sentence: `put` lists the directory's files with their sizes and md5s → POST /v1/volumes/{name}/uploads
(?changed_only=true) answers one signed resumable target per file the volume's version in use does not already hold
as it is - none at all, and no version, when it holds every one (`unchanged`) → each file is sent in chunks straight
to storage, several files at a time, with every opened session remembered in a local state file → `put` run again
after an interruption asks each session how much it already holds and sends only the rest → POST .../commit, where
the platform checks every file's size and md5 and makes the version active, the one it replaces billed no more →
`weights="vol://<name>"` deploys it.

WHY resumable chunks and a state file: a checkpoint is gigabytes over whatever link the user has; a dropped
connection must cost the chunk in flight, not the upload. WHY the md5s: the commit proves the platform holds
exactly these bytes. The upload targets and session addresses are capabilities, so they are never printed and the
state file is written owner-only (0600).

"""
from __future__ import annotations

import base64
import concurrent.futures
import datetime
import hashlib
import json
import os
import pathlib
import re
import threading
from dataclasses import dataclass

import httpx

from seq._account import auth_headers, credential
from seq._gateway import DEFAULT_BASE_URL
from seq.errors import raise_for, unreachable
from sequence_ai._core.mock_gate import is_mock
from sequence_ai.errors import InvalidRequest, SequencesError, Unavailable


CHUNK = 16 * 1024 * 1024
_PARALLEL = 4
_TIMEOUT = httpx.Timeout(60.0, write=300.0)

_START_TIMEOUT = httpx.Timeout(60.0, read=600.0)



_RESUME = "run the same command again: it resumes where this one stopped"


class _Expired(Exception):
    """A refusal of an upload's signed address or session that no retry gets past - one past its life, as a rule: the
    state that holds it can resume nothing. Its message says what was refused."""


def _gone(status: int) -> bool:
    """A refusal no retry of the same address gets past: a 4xx, but a timeout or a rate limit."""
    return 400 <= status < 500 and status not in (408, 429)


def _past(iso: str | None) -> bool:
    """Whether an upload's own lifetime (the expires_at its start answered) is over; unknown is not over."""
    try:
        t = datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return False
    return (t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)) <= datetime.datetime.now(datetime.timezone.utc)


@dataclass(frozen=True)
class LocalFile:
    path: str
    abspath: pathlib.Path
    size: int
    md5: str


def scan(root: str | os.PathLike, *, kind: str = "checkpoint") -> list[LocalFile]:
    """Every regular file under `root` (symlinked files followed, symlinked directories not), sorted, hashed - once
    their count and paths are within the platform's bounds on one upload, read where the gateway reads them
    (sequence_base VolumeUploadRequest), so a directory past them is refused before a byte of it is hashed: before,
    the bounds were asked after every md5, and a too large upload was told so only once all of it had been read.
    """
    base = pathlib.Path(root)
    if not base.is_dir():
        raise InvalidRequest(f"{root} is not a directory")
    found = [(p.relative_to(base).as_posix(), p, p.stat().st_size) for p in sorted(base.rglob("*")) if p.is_file()]
    if not found:
        raise InvalidRequest(f"{root} has no files to upload")
    _within_bounds(root, kind, found)
    out = []
    for rel, p, size in found:
        h = hashlib.md5()
        with open(p, "rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                h.update(block)
        out.append(LocalFile(rel, p, size, base64.b64encode(h.digest()).decode()))
    return out



_NO_MD5 = base64.b64encode(bytes(16)).decode()


def _within_bounds(root, kind: str, found: list[tuple[str, pathlib.Path, int]]) -> None:
    """The upload `found` would open, held to the platform's bounds on one: its files' count and their paths - an
    InvalidRequest in the bounds' own words when it is past one. Never its total size: what an account keeps counts
    toward its one storage limit, which the platform checks as the upload opens."""
    from pydantic import ValidationError
    from sequence_base.contract.volumes import MAX_FILES, VolumeFile, VolumeUploadRequest

    if len(found) > MAX_FILES:
        raise InvalidRequest(f"{root} has {len(found):,} files; one upload may hold at most {MAX_FILES:,}")
    try:
        VolumeUploadRequest(kind=kind, files=[VolumeFile(path=rel, size=size, md5=_NO_MD5) for rel, _, size in found])
    except ValidationError as exc:
        said = str(exc.errors()[0].get("msg") or exc).removeprefix("Value error, ")
        raise InvalidRequest(f"{root}: {said}") from None




_RECORDING = re.compile(r"eval:[0-9a-f-]{36}|capture:[A-Za-z0-9][A-Za-z0-9._-]{0,72}")


def _volume_name(name: str, *, recordings: bool = False) -> str:
    """`name` checked before it goes anywhere: it is pasted into the request's path, where `../deployments/x` reached
    DELETE /v1/deployments/x, and into the upload state's file name, where
    `../x` wrote outside the state directory. The gateway's own rule (sequence_base check_volume_name), or, where a
    delete takes one, an eval's recordings (`eval:<eval id>`) or a dataset of captured data (`capture:<name>-<id8>`)."""
    if recordings and _RECORDING.fullmatch(name or ""):
        return name
    from sequence_base.contract.volumes import check_volume_name
    try:
        return check_volume_name(name)
    except ValueError as exc:
        raise InvalidRequest(str(exc)) from None


def _state_path(name: str) -> pathlib.Path:
    return pathlib.Path(os.environ.get("SEQ_STATE_DIR") or pathlib.Path.home() / ".cache" / "seq") / "uploads" / \
        f"{name}.json"


class _State:
    """The resumable state of one upload: its id, targets, opened sessions and finished files. Owner-only.

    Its files go _PARALLEL at a time, and each change to it is made and written under one lock (`opened`, `finished`):
    before, a file's thread added its session while another's write read the sessions, unlocked, so a session added
    between two of its reads could raise "dictionary changed size during iteration" and stop the upload.
    """

    def __init__(self, path: pathlib.Path, data: dict) -> None:
        self.path, self.data, self._lock = path, data, threading.Lock()

    def save(self) -> None:
        with self._lock:
            self._write()

    def opened(self, rel: str, session: str) -> None:
        """File `rel`'s upload session, remembered for a run that resumes it."""
        with self._lock:
            self.data["sessions"][rel] = session
            self._write()

    def finished(self, rel: str) -> None:
        """File `rel` is all there: a run that resumes sends nothing of it."""
        with self._lock:
            self.data["done"].append(rel)
            self._write()

    def _write(self) -> None:

        text = json.dumps(self.data)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, self.path)

    def drop(self) -> None:
        self.path.unlink(missing_ok=True)


class VolumesClient:
    """The /v1/volumes calls, authenticated with the caller's API key."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        if is_mock(self.base):
            raise InvalidRequest("volumes need the live platform; unset SEQUENCES_BASE_URL=mock")

        self._key = credential(api_key, self.base)

    def _call(self, method: str, path: str, **kw) -> dict:
        """One /v1/volumes call. A refusal that names files, deployments or benchmarks keeps them in its `details`,
        which `seq` prints under the error."""
        from seq._http import RetryReads

        try:

            with httpx.Client(headers=auth_headers(self._key), timeout=60, transport=RetryReads()) as client:
                r = client.request(method, f"{self.base}{path}", **kw)
        except httpx.TransportError as exc:
            raise unreachable(self.base, exc) from None
        raise_for(r)
        return r.json()

    def start(self, name: str, kind: str, files: list[LocalFile]) -> dict:
        """Open a version of `name` for `files`, asking the platform for the changed ones alone (changed_only): with
        every file the version in use's, its answer is the volume as it is, `unchanged`, and no version is opened; with
        some, they are `held` - copied into the new version on the platform - and only the others get a target. The
        copies take their time on the
        platform before the answer: a longer wait for it than a call's minute."""
        return self._call("POST", f"/v1/volumes/{_volume_name(name)}/uploads", params={"changed_only": "true"},
                          timeout=_START_TIMEOUT, json={
                              "kind": kind, "files": [{"path": f.path, "size": f.size, "md5": f.md5} for f in files]})

    def commit(self, name: str, upload_id: str) -> dict:
        return self._call("POST", f"/v1/volumes/{_volume_name(name)}/uploads/{upload_id}/commit")

    def get(self, name: str) -> dict:
        """One volume as the gateway sends it: its kind, state, version, size, and what it is in use by (referenced_by:
        the policies whose weights and the benchmarks whose assets it is, an eval's recordings their eval)."""
        return self._call("GET", f"/v1/volumes/{_volume_name(name, recordings=True)}")

    def list(self, *, limit: int | None = None, cursor: str | None = None) -> list[dict]:
        """Your volumes, one page."""
        return self.page(limit=limit, cursor=cursor)["data"]

    def page(self, *, limit: int | None = None, cursor: str | None = None) -> dict:
        """One page of the volumes as the gateway sends it: {"data": [...], "total": N, "offset": 0,
        "next_cursor": "50" or None} - `limit` rows from the `cursor` the previous page printed
."""
        params = {k: v for k, v in (("limit", limit), ("cursor", cursor)) if v is not None}
        return self._call("GET", "/v1/volumes", params=params or None)

    def delete(self, name: str, *, force: bool = False) -> dict:
        """Delete a volume, an eval's recordings (`eval:<eval id>`) or a dataset of captured data
        (`capture:<name>-<id8>`). `force`: the version dependencies too, whose delete the platform refuses (409) until
        told, saying which versions they hold."""
        return self._call("DELETE", f"/v1/volumes/{_volume_name(name, recordings=True)}",
                          params={"force": "true"} if force else None)

    def files(self, name: str, *, prefix: str | None = None, limit: int | None = None,
              cursor: str | None = None) -> dict:
        """One page of a volume's files, as the gateway sends it: {"name", "files": [{"path","bytes"}...], "total",
        "offset", "next_cursor"}; `prefix` narrows them to a folder."""
        params = {k: v for k, v in (("prefix", prefix), ("limit", limit), ("cursor", cursor)) if v is not None}
        return self._call("GET", f"/v1/volumes/{_volume_name(name, recordings=True)}/files", params=params or None)

    def delete_file(self, name: str, path: str) -> dict:
        """Delete one file or folder of a volume: the platform makes a new version without it, and the replaced one goes.
        Refused (409) while a deployment's weights or a benchmark's assets name the volume, and when it would remove the
        last file (delete the volume instead)."""
        return self._call("DELETE", f"/v1/volumes/{_volume_name(name)}/files/{path.strip('/')}")


def _open_session(client: httpx.Client, target: dict) -> str:
    r = client.post(target["url"], headers={**target.get("headers", {}), "Content-Length": "0"})
    if _gone(r.status_code):
        raise _Expired(f"could not open the upload of {target['path']} ({r.status_code})")
    if r.status_code not in (200, 201) or "Location" not in r.headers:
        raise Unavailable(f"could not open the upload of {target['path']} ({r.status_code})", hint=_RESUME)
    return r.headers["Location"]


def _offset(client: httpx.Client, session: str, size: int) -> int | None:
    """How many bytes the session already holds; None when the object is complete."""
    r = client.put(session, headers={"Content-Range": f"bytes */{size}", "Content-Length": "0"})
    if r.status_code in (200, 201):
        return None
    if r.status_code == 308:
        rng = r.headers.get("Range")
        return int(rng.rsplit("-", 1)[1]) + 1 if rng else 0
    if _gone(r.status_code):
        raise _Expired(f"the upload session stopped answering ({r.status_code})")
    raise Unavailable(f"the upload session stopped answering ({r.status_code})", hint=_RESUME)


def _send(client: httpx.Client, session: str, f: LocalFile) -> None:
    """Send what the session does not hold yet, chunk by chunk."""
    at = _offset(client, session, f.size)
    if at is None:
        return
    if f.size == 0:
        r = client.put(session, headers={"Content-Range": "bytes */0", "Content-Length": "0"})
        if _gone(r.status_code):
            raise _Expired(f"the upload of {f.path} was refused ({r.status_code})")
        if r.status_code // 100 != 2:
            raise Unavailable(f"the upload of {f.path} was refused ({r.status_code})", hint=_RESUME)
        return
    with open(f.abspath, "rb") as fh:
        fh.seek(at)
        while at < f.size:
            data = fh.read(CHUNK)
            end = at + len(data) - 1
            r = client.put(session, content=data, headers={"Content-Range": f"bytes {at}-{end}/{f.size}"})
            if r.status_code in (200, 201):
                return
            if _gone(r.status_code):
                raise _Expired(f"the upload of {f.path} was refused ({r.status_code})")
            if r.status_code != 308:
                raise Unavailable(f"the upload of {f.path} was refused ({r.status_code})", hint=_RESUME)
            rng = r.headers.get("Range")
            at = int(rng.rsplit("-", 1)[1]) + 1 if rng else 0
            fh.seek(at)


def _files(n: int) -> str:
    return f"{n} file" if n == 1 else f"{n} files"


def put(name: str, root: str, *, kind: str = "checkpoint", base_url: str | None = None,
        echo=print) -> dict:
    """Upload `root` as volume `name` and commit it. Resumes an interrupted upload of the same files - or, when that
    upload has outlived its addresses (a day), starts it over. Run again on a directory the volume's version in use is
    already made of, file for file, it sends nothing and makes no version: the platform says so (`unchanged`); with
    some files changed, only those are sent, as a new version, the rest taken from the version in use on the platform
    (`held`). Before, every run sent every file again as a new version: the same 514.7 MB went up twice, as v1 and v2.


    
"""
    name = _volume_name(name)
    api = VolumesClient(base_url)
    files = scan(root, kind=kind)
    digest = hashlib.sha256(json.dumps([[f.path, f.size, f.md5] for f in files]).encode()).hexdigest()
    path = _state_path(name)
    data = None
    if path.exists():
        try:
            data = json.loads(path.read_text())
        except ValueError:
            data = None
    expired = bool(data) and _past(data.get("expires_at"))
    resumed = False
    if not data or data.get("digest") != digest or data.get("base") != api.base or expired:
        if expired:
            echo(f"the upload of {name} that stopped earlier has expired; starting it again")
        start = api.start(name, kind, files)
        if start.get("unchanged"):

            path.unlink(missing_ok=True)
            echo(f"{name} v{start['version']} is already up to date: its {_files(len(files))} are these, each the same "
                 f"({int(start.get('size_bytes') or 0) / 1e6:.1f} MB), so nothing was sent and no new version was made")
            return start

        mine = {f.path for f in files}
        held = [p for p in start.get("held") or [] if p in mine]
        data = {"digest": digest, "base": api.base, "upload_id": start["upload_id"], "version": start["version"],
                "expires_at": start.get("expires_at"), "targets": {t["path"]: t for t in start["targets"]},
                "sessions": {}, "done": held}
        kept = set(held)
        sending = [f for f in files if f.path not in kept]
        said = (f"uploading {_files(len(files))}" if not held else
                f"uploading {len(sending)} of {_files(len(files))}")
        verb = "is" if len(held) == 1 else "are"
        echo(f"{said}, {sum(f.size for f in sending) / 1e6:.1f} MB, as {name} v{data['version']}"
             + (f": the other {len(held)} {verb} the same as in v{data['version'] - 1} and {verb} not sent again"
                if held else ""))
    else:
        resumed = True
        echo(f"resuming the upload of {name} v{data['version']} ({len(data['done'])}/{len(files)} files done)")
    state = _State(path, data)
    state.save()

    def one(f: LocalFile) -> None:
        if f.path in state.data["done"]:
            return
        with httpx.Client(timeout=_TIMEOUT) as c:
            session = state.data["sessions"].get(f.path)
            if not session:
                session = _open_session(c, state.data["targets"][f.path])
                state.opened(f.path, session)
            _send(c, session, f)
        state.finished(f.path)
        echo(f"  {f.path} ({f.size / 1e6:.1f} MB)")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=_PARALLEL) as pool:
            for fut in [pool.submit(one, f) for f in files]:
                fut.result()
    except httpx.TransportError as exc:

        raise Unavailable(f"the upload stopped: {exc}", hint=_RESUME) from None
    except _Expired as exc:


        state.drop()
        if not resumed:
            raise Unavailable(str(exc), hint="run the same command again later: it starts the upload over") from None
        echo(f"the upload of {name} that stopped earlier can no longer be resumed; starting it again")
        return put(name, root, kind=kind, base_url=base_url, echo=echo)
    try:
        info = api.commit(name, state.data["upload_id"])
    except SequencesError:
        state.drop()
        raise
    state.drop()
    use = (f"deploy it with weights=\"vol://{name}\"" if kind == "checkpoint" else
           f"mount it in a benchmark with assets=seq.Volume.from_name(\"{name}\")")



    version = int(info.get("version") or 0)
    replaced = f"; v{version - 1}, which it replaces, is no longer billed" if version > 1 else ""
    echo(f"{name} v{info['version']} is ready ({info['size_bytes'] / 1e6:.1f} MB) — {use}{replaced}")
    return info





def _all_files(client: VolumesClient, name: str, prefix: str | None = None) -> list[dict]:
    """Every file of a volume, page after page (the gateway pages them)."""
    out: list[dict] = []
    cursor = None
    while True:
        page = client.files(name, prefix=prefix, cursor=cursor)
        out.extend(page.get("files") or [])
        cursor = page.get("next_cursor")
        if not cursor:
            return out


def volume_files(name: str, path: str | None = None, *, base_url: str | None = None) -> list[dict]:
    """The files of a volume you uploaded — a checkpoint or a dataset — each `{"path", "bytes"}`, all of them; `path`
    narrows them to a folder. Also a deployment's captured data (`capture:<name>-<id8>`) and an eval's recordings
    (`eval:<id>`). Upstream: `seq volume files`."""
    return _all_files(VolumesClient(base_url), name, prefix=path)


def volume_rm(name: str, path: str | None = None, *, force: bool = False, base_url: str | None = None) -> dict:
    """Delete a volume for good, or one file or folder of it (`path`). Deleting a file leaves a new version without it, and
    the replaced one goes; it is refused while a deployment's weights or a benchmark's assets name the volume. Upstream:
    `seq volume rm`."""
    client = VolumesClient(base_url)
    return client.delete_file(name, path) if path else client.delete(name, force=force)


def _download_one(name: str, obj_path: str, dest: pathlib.Path, base: str, key: str) -> None:
    """Relay one file to `dest`, resuming from what is already there with a Range request (the gateway serves it, 206),
    so a large download that dropped sends only the rest. Raises Unavailable on a dropped connection — run it again."""
    from seq._http import RetryReads

    url = f"{base}/v1/volumes/{_volume_name(name, recordings=True)}/files/{obj_path}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    have = dest.stat().st_size if dest.exists() else 0
    rest = {"Range": f"bytes={have}-"} if have else {}
    try:
        with httpx.Client(headers=auth_headers(key), timeout=_TIMEOUT, transport=RetryReads()) as client:
            with client.stream("GET", url, headers=rest) as r:
                raise_for(r)
                append = bool(have) and r.status_code == 206
                with open(dest, "ab" if append else "wb") as f:
                    for chunk in r.iter_bytes():
                        f.write(chunk)
    except httpx.TransportError as exc:
        raise Unavailable(f"the download of {obj_path} stopped: {exc}",
                          hint="run the same command again: it resumes where it stopped") from None


def volume_get(name: str, path: str | None = None, *, out: str, base_url: str | None = None,
               echo=print) -> list[str]:
    """Download a volume's files into the directory `out`, keeping each file's path under it: one file (`path` names a
    file), a folder (`path` names a folder) or the whole volume (`path` None). A large file that drops resumes with a
    byte range — run the same command again. Returns the paths written. Upstream: `seq volume get`."""
    base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    key = credential(None, base)
    if is_mock(base):
        raise InvalidRequest("volumes need the live platform; unset SEQUENCES_BASE_URL=mock")
    files = _all_files(VolumesClient(base_url), name, prefix=path)
    if not files:
        raise InvalidRequest(f"nothing to download: {name!r}"
                             + (f" has no file under {path!r}" if path else " has no files"))
    outdir = pathlib.Path(out)
    written: list[str] = []
    for f in files:
        dest = outdir / f["path"]
        _download_one(name, f["path"], dest, base, key)
        written.append(str(dest))
        echo(f"  {f['path']} ({f['bytes'] / 1e6:.1f} MB)")
    return written


def _storage_rate(base_url: str | None) -> float | None:
    """The platform's storage price, USD per GB-month (GET /v1/pricing), or None when it cannot be read."""
    from seq._http import RetryReads
    from seq.template_fetch import _headers

    try:
        base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        with httpx.Client(headers=_headers(), timeout=30, transport=RetryReads()) as client:
            r = client.get(f"{base}/v1/pricing")
        r.raise_for_status()
        rate = (r.json().get("storage") or {}).get("usd_per_gb_month")
        return float(rate) if rate is not None else None
    except Exception:
        return None


def _storage_group(name: str, kind: str) -> str:
    """What a volume counts as in the overview: a user's uploaded checkpoint or dataset by its kind, a deployment's
    captured data and an eval's recordings by their own names."""
    if name.startswith("eval:"):
        return "recordings"
    if name.startswith("capture:"):
        return "captured data"
    return kind or "other"


def _storage_cap(client: VolumesClient) -> dict:
    """GET /v1/storage — the account's bytes, its limit (its own or its plan's, both said), whether it nears it (warn)
    and whether it reached it (full). {} when it cannot be read, so the overview still stands without the limit."""
    try:
        r = client._call("GET", "/v1/storage")
        return r if isinstance(r, dict) else {}
    except Exception:
        return {}


def storage(*, base_url: str | None = None) -> dict:
    """What you keep on the platform: the total bytes and, by kind — checkpoints, datasets, captured data, eval
    recordings — how many volumes and how many bytes each, with about what it costs a month at the platform's storage
    price (the current size at that rate: roughly the month's run-rate, the basis the bill accrues by the day), and the
    account's storage limit - its own or its plan's - and whether it is full, at which point nothing new is stored
    (nothing stored is deleted). Upstream: `seq storage`."""
    client = VolumesClient(base_url)
    vols: list[dict] = []
    cursor = None
    while True:
        page = client.page(cursor=cursor)
        vols.extend(page.get("data") or [])
        cursor = page.get("next_cursor")
        if not cursor:
            break
    by_kind: dict[str, dict] = {}
    total = 0
    for v in vols:
        size = int(v.get("size_bytes") or 0)
        row = by_kind.setdefault(_storage_group(v.get("name") or "", v.get("kind") or ""), {"volumes": 0, "bytes": 0})
        row["volumes"] += 1
        row["bytes"] += size
        total += size
    rate = _storage_rate(base_url)
    cap = _storage_cap(client)
    used = cap.get("used_bytes")
    return {"bytes": total, "by_kind": by_kind, "usd_per_gb_month": rate,
            "monthly_usd": round(total / 1e9 * rate, 2) if rate is not None else None,
            "limit_bytes": cap.get("limit_bytes"), "used_bytes": used if used is not None else total,
            "full": bool(cap.get("full")), "warn": bool(cap.get("warn")),
            **{k: cap[k] for k in ("used_share", "warn_share", "own_limit_bytes", "plan_limit_bytes") if k in cap}}
