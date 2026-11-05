"""
`seq init` for the official templates: fetch one version's code from the platform and unpack it into a directory.

In one sentence: `seq init pi05-droid[@stable|@beta|@v<N>] my_pi05_user` asks the platform for that template's code
(GET /v1/templates/{name}/code?ref=…, no key needed) → unpacks the archive into ./my_pi05_user → writes the user's own
deployment name into its policy.py → `seq deploy my_pi05_user` deploys it. The template repo is the source:
a new version there reaches users without an SDK release.

The platform is the only source: the SDK carries no copies of any template, so one that cannot be fetched is an error
that says why, never an older copy written instead.

With no channel named, `seq init` writes only a version this sequence-ai deploys: the stable when it does, else the
newest version that does (deploy_check, newest_deployable), and says so. A channel or version named is written as named.
"""
from __future__ import annotations

import contextlib
import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import httpx

from seq._gateway import DEFAULT_BASE_URL
from seq.errors import raise_for, unreachable
from sequence_ai._core.mock_gate import is_mock
from sequence_ai._core.names import segment
from sequence_ai._core.transport import _version
from sequence_ai.errors import Conflict, InternalError, InvalidRequest, NotFound

_REF = re.compile(r"^(?P<name>[a-z0-9][a-z0-9-]*)(?:@(?P<ref>[a-z0-9]+))?$")

_NUMBERED = re.compile(r"v([1-9][0-9]*)")


_CHECK_TIMEOUT_S = 300.0


KINDS = ("policy", "benchmark", "adapter")
ENTRIES = {"policy": "policy.py", "benchmark": "benchmark.py", "adapter": "adapter.py"}
def lines_by_kind(rows: list[dict]) -> list[str]:
    """The templates of GET /v1/templates (its `data`), one heading per kind — policy, benchmark, adapter, then any kind
    the platform names that this SDK does not know — each template with the version its channels point at. What
    `seq init --list` prints."""
    kind_of = lambda r: r.get("kind") or "other"
    kinds = list(KINDS) + sorted({kind_of(r) for r in rows} - set(KINDS))
    out: list[str] = []
    for kind in kinds:
        mine = sorted((r for r in rows if kind_of(r) == kind), key=lambda r: r["name"])
        out.append(f"{kind} templates:")
        out += [f"  {r['name']:16} stable={r.get('stable') or '—':5} beta={r.get('beta') or '—'}" for r in mine] \
            or ["  (none)"]
    return out


def entry_of(dest: Path) -> str | None:
    """The entry file an unpacked template has: policy.py, benchmark.py or adapter.py (None: none of them)."""
    return next((f for f in ENTRIES.values() if (dest / f).exists()), None)


def entry_name(dest: Path, entry: str) -> str | None:
    """The name `seq deploy <dest> --name` picks the template's entry by, when its folder holds more than one class to
    deploy (seq.discover, reading its files); None when there is one, or none is found here."""
    from seq import discover

    found, _ = discover.find(discover.files_of(dest.resolve()))
    if len(found) < 2:
        return None
    return next((f.name for f in found if f.path == entry), None)


def split_ref(spec: str) -> tuple[str, str | None]:
    """`pi05-droid@beta` → ("pi05-droid", "beta"); no `@` → ("pi05-droid", None): no channel named, which `seq init`
    reads as the stable when this sequence-ai deploys it, else the newest version it does."""
    m = _REF.match(spec or "")
    if not m:
        raise InvalidRequest(f"{spec!r} is not a template name (e.g. pi05-droid, pi05-droid@stable, pi05-droid@beta)")
    return m["name"], m["ref"]


def _base(base_url: str | None) -> str:
    base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    if is_mock(base):
        raise InvalidRequest("official templates come from the platform; unset SEQUENCES_BASE_URL=mock")
    return base


def _headers() -> dict[str, str]:
    """Which sequence-ai asks, as the SDK's own transport says it: the platform answers a `seq init` of a template
    version this SDK is too old to read with the version it needs ("toy-benchmark v4 needs sequence-ai 0.34.17 or later:
    pip install -U sequence-ai"), where an SDK that said nothing was handed files it then failed to import without
    saying why."""
    return {"User-Agent": f"sequence-ai-python/{_version()}"}


def list_remote(base_url: str | None = None) -> list[dict]:
    """The official templates and the version each channel points at."""
    from seq._http import RetryReads

    base = _base(base_url)
    try:
        with httpx.Client(headers=_headers(), timeout=30, transport=RetryReads()) as client:
            r = client.get(f"{base}/v1/templates")
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    raise_for(r)
    return r.json()["data"]


def fetch(name: str, ref: str, base_url: str | None = None) -> tuple[bytes, str] | None:
    """(archive bytes, version) of one template version; None when the platform has no such template. A template it
    has without that channel or version is NotFound, as the platform says it."""
    from seq._http import RetryReads

    base = _base(base_url)
    try:
        with httpx.Client(headers=_headers(), timeout=60, transport=RetryReads()) as client:
            r = client.get(f"{base}/v1/templates/{segment(name)}/code", params={"ref": ref})
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    if r.status_code == 404:
        detail = (r.json() if r.headers.get("content-type", "").startswith("application/json") else {}).get("detail", "")
        if "no template" in str(detail):
            return None
    raise_for(r)
    return r.content, r.headers.get("X-Template-Version", ref)


@contextlib.contextmanager
def source_stream(name: str, version: str, upstream: str, base_url: str | None = None):
    """The official package of one large upstream a template version installs (third_party/SOURCES.json), streamed:
    GET /v1/templates/{name}/source answers with where the platform keeps it, and the download follows there (no key;
    the platform's address for it is never printed)."""
    base = _base(base_url)
    try:
        with httpx.stream("GET", f"{base}/v1/templates/{segment(name)}/source",
                          params={"ref": version, "upstream": upstream}, headers=_headers(), follow_redirects=True,
                          timeout=httpx.Timeout(60.0, read=300.0)) as r:
            if r.status_code >= 400:
                r.read()
                raise_for(r)
            yield r
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None


def refuse_occupied(dest: Path) -> None:
    """A directory that exists and holds anything is refused: `seq init` writes into an empty one only."""
    if dest.exists() and any(dest.iterdir()):
        raise Conflict(f"{dest} already exists and is not empty",
                       hint="name another directory: seq init <template> <dir>")


def unpack(archive: bytes, dest: Path, *, template: str, deploy_name: str) -> list[Path]:
    """Unpack into `dest` (which must not exist or be empty) and name the deployment in policy.py. Refuses any member that
    would land outside `dest`."""
    refuse_occupied(dest)
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
        for member in tf.getmembers():
            target = (dest / member.name).resolve()
            if not str(target).startswith(str(dest.resolve())) or member.issym() or member.islnk():

                raise InternalError(f"refusing archive member {member.name!r}: it would land outside {dest}")
        tf.extractall(dest, filter="data")
        written = [dest / m.name for m in tf.getmembers() if m.isfile()]
    policy = dest / "policy.py"
    if policy.exists():
        text = policy.read_text()
        policy.write_text(text.replace(f'name="{template}"', f'name="{deploy_name}"', 1))
    return written




def deploy_check(dest: Path) -> str | None:
    """
    Why this sequence-ai cannot deploy the template unpacked at `dest` - the refusal `seq deploy` would end with, in its
    own words - or None when it can.

    In one sentence: `seq --json deploy --dry-run <folder> [--name <its entry's name>]` - the folder's class found and
    loaded and the request `seq deploy` sends assembled and checked, offline (--json: before anything is asked of the
    platform), nothing built or sent - run by this interpreter in a process of its own, from the folder's parent as a
    person runs `seq deploy <folder>` → exit 0 is None, a refusal is its `error[<code>]: <message>`.

    WHY the SDK's own reading, and not the template's metadata: what a version needs is published as the OLDEST
    sequence-ai it works with (channels.json "needs"); nothing says which newer one stops reading it. The five pi05
    stables were written with @seq.batched, which 0.35.0 removed, and a `seq init` of them handed out files that `seq
    deploy` then refused.



    A process of its own, because the loader puts the file's folder on sys.path and keeps its modules: a second version
    checked in this process would import the first one's.

    A check that cannot be run (the interpreter does not start, or it takes past _CHECK_TIMEOUT_S) says nothing: the
    version is written as it was before this check existed.
    """
    entry = entry_of(dest)
    if entry is None:
        return None
    return _deploy_check(dest, entry)


def _deploy_check(dest: Path, entry: str) -> str | None:
    """deploy_check of the class the file `entry` holds."""


    name = entry_name(dest, entry)


    root = str(Path(__file__).resolve().parent.parent)
    path = os.pathsep.join(p for p in (root, os.environ.get("PYTHONPATH")) if p)
    try:
        done = subprocess.run([sys.executable, "-m", "seq", "--json", "deploy", "--dry-run", dest.name,
                               *(["--name", name] if name else [])],
                              cwd=dest.parent, capture_output=True, text=True, timeout=_CHECK_TIMEOUT_S,
                              env={**os.environ, "PYTHONPATH": path, "PYTHONDONTWRITEBYTECODE": "1"})
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode == 0:
        return None

    lines = [ln.strip() for ln in done.stderr.splitlines() if ln.strip()]
    said = next((ln.split("]: ", 1)[1] for ln in lines if ln.startswith("error[") and "]: " in ln), None)
    return said or (lines[-1] if lines else f"`seq deploy --dry-run` ended with exit code {done.returncode}")


def check_archive(archive: bytes, name: str) -> str | None:
    """deploy_check on one version's archive of template `name`, unpacked into a folder of its own that is removed
    after: None when this sequence-ai deploys it, else why not."""
    with tempfile.TemporaryDirectory(prefix="seq-init-") as tmp:
        dest = Path(tmp) / name
        unpack(archive, dest, template=name, deploy_name=name)
        return deploy_check(dest)


def _number(version: str | None) -> int | None:
    """v20 → 20; None for a missing or unnumbered version."""
    m = _NUMBERED.fullmatch(version or "")
    return int(m[1]) if m else None


def newest_deployable(name: str, *, besides: str,
                      base_url: str | None = None) -> tuple[bytes, str, str | None] | None:
    """
    The newest version of template `name` this sequence-ai deploys, other than `besides` (one already found not to):
    (archive, version, the channel that points at it or None), or None when none does.

    Looked for among the versions the platform offers a person: its beta and every version under it down to its
    stable, newest first. The platform lists no versions, so each is asked for by number; one it has withdrawn answers
    not found and one it says needs a newer sequence-ai is refused, and both are passed over. Each is checked as
    deploy_check checks it.

    """
    row = next((r for r in list_remote(base_url) if r.get("name") == name), None) or {}
    stable, beta = row.get("stable"), row.get("beta")
    low, high = _number(stable), _number(beta) or _number(stable)
    if low is None or high is None:
        return None
    for n in range(high, low - 1, -1):
        version = f"v{n}"
        if version == besides:
            continue
        try:
            got = fetch(name, version, base_url)
        except (NotFound, InvalidRequest):
            continue
        if got is None:
            return None
        if check_archive(got[0], name) is None:
            return got[0], got[1], "beta" if got[1] == beta else "stable" if got[1] == stable else None
    return None
