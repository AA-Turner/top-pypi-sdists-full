"""
`seq init` for the official templates: fetch one version's code from the platform and unpack it into a directory.

In one sentence: `seq init pi05-droid[@v<N>] my_pi05_user` asks the platform for that template's code - its one
version, or the version named (GET /v1/templates/{name}/code[?ref=v<N>], no key needed) → unpacks the archive into
./my_pi05_user → writes the user's own
deployment name into its policy.py → `seq deploy my_pi05_user` deploys it. The template repo is the source:
a new version there reaches users without an SDK release.

The platform is the only source: the SDK carries no copies of any template, so one that cannot be fetched is an error
that says why, never an older copy written instead.

A template has one version, the one `seq init --list` shows; `@v<N>` names an exact one. With sequence-cloud
installed, `seq init` says when this sequence-ai cannot deploy the version it wrote (deploy_check).


"""
from __future__ import annotations

import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import httpx

from sequence_ai._core.transport import DEFAULT_BASE_URL
from seq.errors import raise_for, unreachable
from sequence_ai._core.mock_gate import is_mock
from sequence_ai._core.names import segment
from sequence_ai._core.transport import _version
from sequence_ai.errors import Conflict, InternalError, InvalidRequest

_REF = re.compile(r"^(?P<name>[a-z0-9][a-z0-9-]*)(?:@(?P<ref>[a-z0-9]+))?$")

_NUMBERED = re.compile(r"v([1-9][0-9]*)")


_CHECK_TIMEOUT_S = 300.0






KINDS = ("policy", "adapter")
ENTRIES = {"policy": "policy.py", "benchmark": "benchmark.py", "adapter": "adapter.py"}



BENCHMARK_NEXT = ("nothing to build: seq benchmark tasks lists every task by its id, and seq eval run <policy> --task "
                  "<id> ... runs any of them")


def lines_by_kind(rows: list[dict]) -> list[str]:
    """The templates of GET /v1/templates (its `data`), one heading per kind — policy, adapter, then any kind the
    platform names that this SDK does not know — each template on a line of its own with its one version. What
    `seq init --list` prints."""
    kind_of = lambda r: r.get("kind") or "other"
    kinds = list(KINDS) + sorted({kind_of(r) for r in rows} - set(KINDS))
    out: list[str] = []
    for kind in kinds:
        mine = sorted((r for r in rows if kind_of(r) == kind), key=lambda r: r["name"])
        out.append(f"{kind} templates:")

        out += [f"  {r['name']:16} {r.get('version') or '—'}".rstrip() for r in mine] or ["  (none)"]
    return out





DEPLOY_FILE = "deploy.toml"
_DEPLOY_KEYS = ("gpu", "cpu", "memory")


def deploy_items(dest: Path) -> dict:
    """The card and worker size the template at `dest` deploys with (DEPLOY_FILE's gpu, cpu, memory); {} where it names
    none, or the file cannot be read here (Python 3.10 without tomli)."""
    try:
        import tomllib
    except ModuleNotFoundError:
        try:
            import tomli as tomllib
        except ModuleNotFoundError:
            return {}
    try:
        data = tomllib.loads((dest / DEPLOY_FILE).read_text())
    except (OSError, ValueError):
        return {}
    return {k: data[k] for k in _DEPLOY_KEYS if k in data}


def deploy_flags(items: dict) -> list[str]:
    """deploy_items as `seq deploy`'s flags: {"gpu": "L4", "cpu": 4} → ["--gpu", "L4", "--cpu", "4"]."""
    return [a for k in _DEPLOY_KEYS if k in items
            for a in (f"--{k}", f"{items[k]:g}" if isinstance(items[k], float) else str(items[k]))]


def weights_from_gs(dest: Path, entry: str) -> bool:
    """Whether the class in `entry` declares weights GS keeps (seq.Weights.template(...)): `seq serve` downloads them
    with a General Sequences key. Read from the file's syntax, never by running it."""
    import ast

    try:
        tree = ast.parse((dest / entry).read_text())
    except (OSError, SyntaxError, ValueError):
        return False
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "template"
               and (getattr(n.func.value, "attr", None) or getattr(n.func.value, "id", None)) == "Weights"
               for n in ast.walk(tree))


def entry_of(dest: Path) -> str | None:
    """The entry file an unpacked template has: policy.py, benchmark.py or adapter.py (None: none of them)."""
    return next((f for f in ENTRIES.values() if (dest / f).exists()), None)


def entry_in(archive: bytes) -> str | None:
    """The entry file a template's archive holds at its top, as entry_of reads an unpacked one - read before anything
    is written."""
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
        top = {m.name.removeprefix("./") for m in tf.getmembers() if m.isfile()}
    return next((f for f in ENTRIES.values() if f in top), None)


def benchmark_refused(name: str) -> InvalidRequest:
    """`seq init` of a benchmark's template a platform of before sends the code of: refused before anything is written,
    in the words today's platform refuses its name with, then what to do instead (BENCHMARK_NEXT)."""
    return InvalidRequest(f"{name} is a benchmark: the platform provides the benchmarks ready to run, so there is none "
                          "to start from a template - evaluate a deployed policy on it instead", hint=BENCHMARK_NEXT)


def entry_name(dest: Path, entry: str) -> str | None:
    """The name `seq deploy <dest> --name` picks the template's entry by, when its folder holds more than one class to
    deploy (seq.discover, reading its files); None when there is one, or none is found here."""
    from seq import discover

    found, _ = discover.find(discover.files_of(dest.resolve()))
    if len(found) < 2:
        return None
    return next((f.name for f in found if f.path == entry), None)


def names_a_template(spec: str) -> bool:
    """Whether `spec` has a template name's form - a name, an `@` and a word after it or not - whatever that word is:
    split_ref says what is wrong with one whose word is no version."""
    return bool(_REF.match(spec or ""))


def split_ref(spec: str) -> tuple[str, str | None]:
    """`pi05-droid@v12` → ("pi05-droid", "v12"); no `@` → ("pi05-droid", None): the template's one version. A template
    has no channels, so a word after `@` that is no version - `@stable`, `@beta` - is refused with the two ways there
    are.
    """
    m = _REF.match(spec or "")
    if not m:
        raise InvalidRequest(f"{spec!r} is not a template name (e.g. pi05-droid, or pi05-droid@v12 for one version)")
    if m["ref"] is not None and not _NUMBERED.fullmatch(m["ref"]):
        raise InvalidRequest(f"{spec!r}: a template has one version, so there is no @{m['ref']}: write {m['name']} for "
                             f"it, or {m['name']}@v<N> for an exact version")
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


def fetch(name: str, ref: str | None = None, base_url: str | None = None) -> tuple[bytes, str] | None:
    """(archive bytes, version) of template `name`'s one version, or of the version `ref` names (v<N>); None when the
    platform has no such template. A template it has without that version is NotFound, as the platform says it."""
    from seq._http import RetryReads

    base = _base(base_url)
    try:
        with httpx.Client(headers=_headers(), timeout=60, transport=RetryReads()) as client:

            r = client.get(f"{base}/v1/templates/{segment(name)}/code", params={"ref": ref} if ref else None)
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    if r.status_code == 404:
        detail = (r.json() if r.headers.get("content-type", "").startswith("application/json") else {}).get("detail", "")
        if "no template" in str(detail):
            return None
    try:
        raise_for(r)
    except InvalidRequest as exc:




        if exc.details.get("kind") == "benchmark":
            exc.hint = BENCHMARK_NEXT + (f"; {exc.hint}" if exc.hint else "")
        raise
    version = r.headers.get("X-Template-Version") or ref
    if not version:
        raise InternalError(f"the platform sent {name}'s code without saying which version it is")
    return r.content, version


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




def cache_dir() -> Path:
    """Where `seq serve <template>` keeps a template's code, a folder a version (<template>/v<N>), beside the weights
    `seq serve` keeps (weights_get.cache_dir)."""
    return Path.home() / ".cache" / "sequence-ai" / "templates"


def held(name: str, version: str) -> Path | None:
    """The folder of version `version` of template `name` kept here, or None: a folder there is always whole (keep)."""
    folder = cache_dir() / name / version
    return folder if folder.is_dir() else None


def keep(archive: bytes, name: str, version: str) -> Path:
    """
    One version of template `name` unpacked into the cache as `seq init` writes it under the template's own name: the
    folder `seq serve <template>` serves.

    In one sentence: the version's folder already there → it, untouched → else the archive unpacked (unpack, with its
    own checks) into a folder of its own beside the version's → moved into place in one rename → a rename another `seq
    serve` beat to it leaves that one's folder, and this one is removed.

    WHY one rename: a serve stopped mid-unpack, or two started at once, never leaves a folder there that holds part of a
    version, which held() would hand the next serve as whole.
    """
    folder = cache_dir() / name / version
    if folder.is_dir():
        return folder
    folder.parent.mkdir(parents=True, exist_ok=True)

    staging = Path(tempfile.mkdtemp(prefix=f".{version}-", dir=folder.parent))
    try:
        unpack(archive, staging / name, template=name, deploy_name=name)
        try:
            os.rename(staging / name, folder)
        except OSError:

            if not folder.is_dir():
                raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return folder




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

        flags = deploy_flags({"gpu": "cpu", **deploy_items(dest)}) if entry == ENTRIES["policy"] else []
        done = subprocess.run([sys.executable, "-m", "seq", "--json", "deploy", "--dry-run", dest.name,
                               *(["--name", name] if name else []), *flags],
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
