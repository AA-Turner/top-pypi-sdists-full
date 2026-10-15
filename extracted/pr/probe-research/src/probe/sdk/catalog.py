"""The data catalog from inside a training job (plan data-catalog C5, C8-C11).

    src = probe.source("https://huggingface.co/datasets/allenai/c4", revision="1588ec4",
                       license="ODC-BY")                      # upsert, returns a ref
    run.use_dataset(src, role="train")                        # POST /v1/runs/{id}/uses
    run.use_dataset("dataset:c4-clean@3", role="validation")
    run.use_mixture({"dataset:a@2": 0.7, "dataset:b@1": 0.3})  # one batch, replaces train shares
    run.use_checkpoint("checkpoint:sft-7b@best")              # role init: the weights it started from
    ds = run.log_dataset("data/clean/", name="c4-clean", sources=[src],
                         note="dropped 1,204 seqs >90% identical to test")

NEVER RAISES INTO A JOB. Every verb here warns once and returns quietly on a
server that predates the catalog (its own 404/405 for the route), a network
error, a refusal (409, 422, 402) or a bug of ours: the training loop is never
the place a provenance record fails. The plain HTTP calls the CLI uses, which
do raise, are `Client` methods (`create_source`, `use_in_run`, ...).

`log_dataset` (C5, Q9): a folder is identified by its MANIFEST -- every file's
relative path, size and sha256 (or, past the run's I/O budget or over 1 GiB,
its fingerprint), sorted -- hashed the way `manifest_identity` says. The
manifest goes to `PUT /v1/catalog/manifests/{sha256}` (gzip JSON, idempotent),
then ONE `POST /v1/catalog/datasets` carries the run's file, so the server
writes the run file and the version in one transaction. The call waits at most
`REGISTER_WAIT_SECONDS`; past that it returns `DatasetRef(pending=True)` and
the request finishes in the background (queued in the outbox if Probe cannot
be reached), filling the ref when it lands. A remote uri is never read: its
identity is ``sha256("uri\\nrevision")``, `identity="pointer"`.

`upload=True` (C8) hosts the bytes in Probe: the manifest, then
`POST /v1/catalog/datasets/uploads` answers which blobs Probe already holds
and an upload for each of the rest (one PUT, or the multipart doors over
64 MiB), at most 1,000 per call with `deferred` saying how many wait: the
client sends each round, waits for Probe to verify its large uploads, and asks
again until `deferred` is 0 (at most `door_call_limit` calls). Then the
registration names `hosted: {manifest_hash, run_id}`.

`.probe.config` (C9): an `off` or `read` path records nothing at all; a
`hash` path is recorded by identity only (path, sha256, size, rows; under 64
bytes no hash), is never uploaded and never sampled for a preview.

Preview samples (C11): a dataset kept outside Probe gets its first 100 records
(or 256 KiB) uploaded as a run file named `.probe/previews/<dataset file
id><ext>` with `meta.preview_of`, so its page can show something; the server
stamps it `storage_class='preview'` and hides it. Only for `on` paths, and
`preview=False` turns it off; one line says when it happens.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import mimetypes
import os
import re
import socket
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Iterable, Mapping

from . import errors, safe_warn
from .catalog_vocab import HashMode, Identity, Role, SourceKind

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client
    from .run import Run

#: How long `log_dataset` waits for its registration before it returns a
#: pending ref (Q9): a slow server must never hold a training loop.
REGISTER_WAIT_SECONDS = 10.0
#: The bound on the registration's own retries, in the background, after which
#: a request that still has no answer is queued in the outbox.
REGISTER_DEADLINE_SECONDS = 60.0
#: The bound on one small catalog request made on the training thread (a use,
#: a source, the catalog probe), and on waiting for a pending ref before a use.
REQUEST_SECONDS = 10.0
#: The bound on one manifest PUT (up to 16 MB of gzip).
MANIFEST_SECONDS = 30.0
#: The bound on one hosting door call, retries included: it may open 500
#: multipart uploads (8 store calls at a time) and sign 1,000 PUTs before it
#: answers, and asking again is safe (it resumes what the first call staged).
DOOR_SECONDS = 60.0
#: The fewest blobs one door call answers while any wait (the server's 500
#: multipart uploads per call; up to 1,000 in all), so a manifest of N blobs
#: needs at most ceil(N / 500) calls; `DOOR_SPARE_CALLS` more are allowed.
DOOR_ANSWERS_AT_LEAST = 500
DOOR_SPARE_CALLS = 4
#: How long hosting waits for Probe to verify one round's large uploads (its
#: verifier hashes each one server side) before giving up, and how often it looks.
HOSTED_VERIFY_SECONDS = 3600.0
HOSTED_VERIFY_POLL_SECONDS = 5.0
#: After Probe could not be reached, the catalog probe is not asked again for
#: this long: every call would otherwise pay `REQUEST_SECONDS` to learn it again.
UNREACHABLE_TTL_SECONDS = 60.0
#: The server's ceiling per manifest (`dataset_manifest_files`).
MAX_MANIFEST_FILES = 100_000
#: Entries a folder walk looks at before it stops (it runs on the training thread).
MAX_WALK_ENTRIES = 1_000_000
#: The hashing of one `log_dataset` (budget mode) stops starting files after
#: this long; the rest are left unhashed and the version is `partial`. The walk
#: and the hashing run on a daemon thread the caller waits for at most this
#: plus `HASH_GRACE_SECONDS` (a stalled mount costs the call, never the job).
HASH_DEADLINE_SECONDS = 120.0
#: The same bound for `hash="full"` and hosting (`upload=True`), which must read
#: every byte: one hour, waited for in one-second slices (Ctrl-C interrupts).
FULL_HASH_DEADLINE_SECONDS = 3600.0
#: How long past its deadline a hashing worker may take to wind down (the file
#: in progress stops at its next 1 MiB) before the call gives up on it.
HASH_GRACE_SECONDS = 30.0
#: `share` values must sum to 1 within this (C10, V12).
SHARE_TOLERANCE = 0.01
#: A preview sample: at most this many records, and at most this many bytes.
PREVIEW_MAX_RECORDS = 100
PREVIEW_MAX_BYTES = 256 * 1024
#: Names reserved for Probe's own rows at the server (C8g).
PREVIEW_PREFIX = ".probe/previews/"
HOSTED_PREFIX = ".probe/datasets/"
#: Line-record formats a preview (and a row count) reads as text.
_LINE_SUFFIXES = (".jsonl", ".ndjson", ".csv", ".tsv", ".txt")
_HEADER_SUFFIXES = (".csv", ".tsv")
#: Dataset names (C3, Q8): no `@`, `/` or uuid shape, so the ref grammar holds.
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
#: Schemes a pointer may use; anything else with `://` is refused here.
_SCHEME = re.compile(r"^([A-Za-z][A-Za-z0-9+.-]*)://")
#: The manifest's identity format, named in its body so the server can recompute it.
MANIFEST_FORMAT = "probe-manifest-v1"
#: How a use is known (`lineage_edges.provenance`): the SDK saw the job use it;
#: the CLI's are a person's (or an agent's) word. The daemon's key is stored
#: `inferred` by the server whatever it sends.
OBSERVED = "observed_call"
STATED = "human"
#: The limit a hosted-data refusal names (402, C8 D2).
HOSTED_DATA_LIMIT = "hosted_data_bytes"

_warned: set[str] = set()
_warned_lock = threading.Lock()


def _warn_once(key: str, message: str) -> None:
    """One line per kind of trouble per process: a loop that calls a verb every
    step must not print it every step."""
    with _warned_lock:
        if key in _warned:
            return
        _warned.add(key)
    safe_warn.warn(message, stacklevel=3)


def _say(message: str) -> None:
    """A line the researcher should see once, on stderr, never raising."""
    try:
        if safe_warn.streams_allowed():
            print(message, file=sys.stderr, flush=True)
    except Exception:  # noqa: BLE001 - a notice never breaks the caller
        pass


class CatalogRefused(Exception):
    """A catalog call that cannot go ahead, with the sentence that says why.
    The CLI prints it; the SDK verbs warn it."""


# ---------------------------------------------------------------------------
# Refs
# ---------------------------------------------------------------------------


@dataclass(eq=False)  # hashable by identity: a ref is a `{ref: share}` key
class SourceRef:
    """What `probe.source(...)` registered: ``ref`` is ``source:<id>``, or None
    when it could not be registered (the warning said why)."""

    ref: str | None = None
    id: str | None = None
    uri: str | None = None
    canonical_key: str | None = None
    provider: str | None = None
    kind: str | None = None
    revision: str | None = None
    created: bool | None = None

    def __str__(self) -> str:
        return self.ref or ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any], *, uri: str | None = None) -> "SourceRef":
        source_id = row.get("id")
        ref = row.get("ref") or (f"source:{source_id}" if source_id else None)
        return cls(
            ref=ref,
            id=str(source_id) if source_id else None,
            uri=uri,
            canonical_key=row.get("canonical_key"),
            provider=row.get("provider"),
            kind=row.get("kind"),
            revision=row.get("revision"),
            created=row.get("created"),
        )


@dataclass(eq=False)  # hashable by identity: a ref is a `{ref: share}` key
class DatasetRef:
    """What `log_dataset` recorded. ``ref`` is ``dataset:<name>@<n>`` once
    registered (``artifact:<id>`` with ``register=False``). ``pending``: the
    registration had not answered within the wait; the fields fill in when it
    does (``wait()``), and stay empty if it was queued in the outbox."""

    ref: str | None = None
    name: str | None = None
    version_id: str | None = None
    content_hash: str | None = None
    identity: str | None = None
    pending: bool = False
    created_version: bool | None = None
    recorded_step: bool | None = None
    #: The run's own file row (the dataset file the version pins), when known.
    artifact_id: str | None = None
    _done: threading.Event = field(default_factory=threading.Event, repr=False, compare=False)

    def __str__(self) -> str:
        return self.ref or ""

    def wait(self, timeout: float | None = None) -> bool:
        """Block until a pending registration has answered (or was queued).
        True when it is settled."""
        return self._done.wait(timeout)

    def _fill(self, answer: Mapping[str, Any]) -> None:
        version = answer.get("version") if isinstance(answer.get("version"), dict) else {}
        entry = answer.get("entry") if isinstance(answer.get("entry"), dict) else {}
        self.ref = version.get("ref") or entry.get("ref") or self.ref
        self.version_id = version.get("id") or self.version_id
        self.content_hash = version.get("content_hash") or self.content_hash
        self.identity = version.get("identity") or self.identity
        self.created_version = answer.get("created_version")
        self.recorded_step = answer.get("recorded_step")
        self.pending = False


def ref_of(value: Any) -> str | None:
    """The ref string of a `str`, `SourceRef` or `DatasetRef` (None when it has none)."""
    if isinstance(value, (SourceRef, DatasetRef)):
        return value.ref or None
    if isinstance(value, str):
        return value.strip() or None
    return None


def _role(role: Any) -> str:
    try:
        return Role(str(role)).value
    except ValueError:
        raise CatalogRefused(
            f"`{role}` is not a role; use one of {', '.join(r.value for r in Role)}"
        ) from None


def check_share(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CatalogRefused(f"a share must be a number between 0 and 1, not {value!r}")
    share = float(value)
    if not math.isfinite(share) or share <= 0 or share > 1:
        raise CatalogRefused(f"a share must be more than 0 and at most 1, not {value!r}")
    return share


def mixture_parts(parts: Mapping[Any, Any]) -> list[dict]:
    """`{ref: share}` as the wire's `[{target, share}]`, checked the way the
    server checks it (finite, > 0, summing to 1 within `SHARE_TOLERANCE`)."""
    if not isinstance(parts, Mapping) or not parts:
        raise CatalogRefused("a mixture needs at least one {dataset ref: share}")
    out = []
    for target, share in parts.items():
        ref = ref_of(target)
        if not ref:
            raise CatalogRefused(f"{target!r} has no ref (was it registered?)")
        out.append({"target": ref, "share": check_share(share)})
    total = sum(p["share"] for p in out)
    if abs(total - 1.0) > SHARE_TOLERANCE:
        raise CatalogRefused(f"a mixture's shares must sum to 1 (+-{SHARE_TOLERANCE}); these sum to {total:g}")
    return out


def composition_parts(composition: Mapping[Any, Any]) -> list[dict]:
    """`log_dataset(composition=...)` (C10) as the wire's `[{target, rows?, share}]`.

    Row counts (ints) give shares computed from them; shares (floats summing to
    1 within `SHARE_TOLERANCE`) are sent as given. Never both kinds at once."""
    if not isinstance(composition, Mapping) or not composition:
        raise CatalogRefused("a composition needs at least one {dataset ref: rows or share}")
    refs = []
    for target in composition:
        ref = ref_of(target)
        if not ref:
            raise CatalogRefused(f"{target!r} has no ref (was it registered?)")
        refs.append(ref)
    values = list(composition.values())
    if all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        if any(v <= 0 for v in values):
            raise CatalogRefused("a composition's row counts must be more than 0")
        total = sum(values)
        return [{"target": ref, "rows": int(v), "share": v / total} for ref, v in zip(refs, values)]
    shares = [check_share(v) for v in values]
    total = sum(shares)
    if abs(total - 1.0) > SHARE_TOLERANCE:
        raise CatalogRefused(
            f"a composition's shares must sum to 1 (+-{SHARE_TOLERANCE}); these sum to {total:g}. "
            "Pass row counts (ints) to have the shares computed"
        )
    return [{"target": ref, "share": share} for ref, share in zip(refs, shares)]


def check_name(name: Any) -> str:
    """A dataset name the server takes (C3, Q8), or `CatalogRefused`."""
    if not isinstance(name, str) or not NAME_PATTERN.match(name) or _UUID.match(name):
        raise CatalogRefused(
            f"{name!r} is not a dataset name: lower-case letters, digits, `.`, `_` and `-`, "
            "starting with a letter or digit, at most 128 characters (no `@`, `/` or id)"
        )
    return name


# ---------------------------------------------------------------------------
# Talking to the server
# ---------------------------------------------------------------------------


def old_server(exc: BaseException) -> bool:
    """The server has no such route: FastAPI's own 404, or a 405 for a path
    that exists with other methods. Either way it predates the catalog."""
    from .client import _route_absent

    if isinstance(exc, errors.RosError) and exc.status == 405:
        return True
    return isinstance(exc, errors.RosError) and _route_absent(exc)


def hosted_limit_message(exc: errors.LimitReachedError) -> str:
    """The sentence for a 402 over the hosted-data cap (C8, D2)."""
    figure = ""
    if exc.current is not None and exc.maximum is not None:
        figure = f" ({bytes_figure(exc.current)} of {bytes_figure(exc.maximum)} used)"
    return (
        f"the team's hosted datasets and checkpoints are at their cap{figure}, so nothing was "
        "uploaded. Record it as a reference instead (leave out upload / --upload), or free "
        "hosted data by deleting unused versions."
    )


def bytes_figure(value: Any) -> str:
    """A 402 figure as a size. The storage refusals send GiB (`storage_guard._gib`);
    a figure too big to be GiB is taken as bytes."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return str(value)
    if value >= 1 << 20:
        return human_bytes(int(value))
    return f"{value:g} GB"


def describe(exc: BaseException, what: str) -> str:
    """One warning line for a failed catalog call."""
    if old_server(exc):
        return (
            f"probe: {what}: this Probe server predates the data catalog, so nothing was recorded "
            "(it needs the catalog routes)."
        )
    if isinstance(exc, errors.LimitReachedError):
        if exc.limit == HOSTED_DATA_LIMIT:
            return f"probe: {what}: {hosted_limit_message(exc)}"
        return f"probe: {what}: refused by a plan limit: {exc}"
    if isinstance(exc, errors.TransportError):
        return f"probe: {what}: Probe could not be reached ({type(exc).__name__}: {exc}); nothing was recorded."
    if isinstance(exc, errors.RosError):
        status = f" ({exc.status})" if exc.status else ""
        return f"probe: {what} was refused{status}: {exc}"
    if isinstance(exc, CatalogRefused):
        return f"probe: {what}: {exc}"
    return f"probe: {what} failed ({type(exc).__name__}: {exc}); nothing was recorded."


def _warn_failure(exc: BaseException, what: str) -> None:
    kind = "old" if old_server(exc) else type(exc).__name__
    _warn_once(f"{what.split('(')[0]}:{kind}:{getattr(exc, 'status', '')}", describe(exc, what))


def catalog_available(client: "Client") -> bool | None:
    """Does this server have the catalog? Asked once per client: by the
    `catalog` feature when it declares one, else by whether the datasets list
    route exists, within `REQUEST_SECONDS`. None when the server could not be
    asked; that answer is kept for `UNREACHABLE_TTL_SECONDS`, so a run of
    calls pays the timeout once."""
    from .transport import deadline_scope

    known = getattr(client, "_catalog_available", None)
    if known is not None:
        return known
    if time.monotonic() < float(getattr(client, "_catalog_unreachable_until", 0.0) or 0.0):
        return None
    try:
        with deadline_scope(time.monotonic() + REQUEST_SECONDS):
            if client.supports_feature("catalog"):
                answer = True
            else:
                client.list_datasets(limit=1)
                answer = True
    except errors.RosError as exc:
        if old_server(exc):
            answer = False
        elif isinstance(exc, (errors.TransportError, errors.ServerError)):
            try:
                client._catalog_unreachable_until = time.monotonic() + UNREACHABLE_TTL_SECONDS  # type: ignore[attr-defined]
            except Exception:  # noqa: BLE001
                pass
            return None
        else:
            answer = True  # the route exists and refused this ask: the catalog is there
    try:
        client._catalog_available = answer  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    return answer


def _send(client: "Client", path: str, body: dict, *, what: str) -> dict | None:
    """One small catalog write from a training thread: sent now, within
    `REQUEST_SECONDS`; a refusal warns once, a failure that could still succeed
    is queued in the outbox (the SDK's ordinary fail-open path)."""
    from .transport import deadline_scope

    try:
        with deadline_scope(time.monotonic() + REQUEST_SECONDS):
            return client.write("POST", path, body, sync=True, raise_permanent=True)
    except errors.RosError as exc:
        _warn_failure(exc, what)
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, what)
    return None


_ambient: "Client | None" = None
_ambient_lock = threading.Lock()


def _client_for(client: "Client | None") -> "Client | None":
    """The client a module-level verb uses: the one given, the bound run's, or
    one built from the environment (kept for the process). None -- nothing is
    sent, and no Client is built -- under `PROBE_MODE=disabled` or `offline`
    and when the bound run records nothing (a disabled run, an `off` folder)."""
    global _ambient
    if client is not None:
        return client
    from .config import Mode, resolve_mode

    try:
        if resolve_mode() is not Mode.ONLINE:
            return None
    except Exception:  # noqa: BLE001 - an unreadable PROBE_MODE sends nothing
        return None
    try:
        from .fluent import active_run

        run = active_run()
    except Exception:  # noqa: BLE001
        run = None
    if run is not None:
        if getattr(run, "disabled", False):
            return None
        return getattr(run, "_client", None)
    with _ambient_lock:
        if _ambient is None:
            from .client import Client

            _ambient = Client()
        return _ambient


# ---------------------------------------------------------------------------
# Sources and uses
# ---------------------------------------------------------------------------


#: Query (or fragment) parameters that carry a secret, compared
#: case-insensitively. The client's copy of the server's rule
#: (`app/catalog/uris.py` `CREDENTIAL_PARAMS`, held equal by
#: `test_catalog_sdk.py`): refusing here keeps the token on this machine; the
#: server refuses it too.
CREDENTIAL_PARAMS: frozenset[str] = frozenset(
    {
        "x-amz-signature",
        "x-amz-credential",
        "x-amz-security-token",
        "x-goog-signature",
        "x-goog-credential",
        "sig",
        "signature",
        "token",
        "access_token",
        "refresh_token",
        "id_token",
        "api_key",
        "apikey",
        "client_secret",
        "password",
        "secret",
    }
)
#: Schemes whose userinfo is a plain name, never a secret (the server's
#: `_NAME_ONLY_USERINFO_SCHEMES`); a password is refused on these too.
NAME_ONLY_USERINFO_SCHEMES: frozenset[str] = frozenset(
    {
        "ssh",
        "git+ssh",
        "abfs",
        "abfss",
        "wasb",
        "wasbs",
        "postgres",
        "postgresql",
        "mysql",
        "mariadb",
        "mssql",
        "sqlserver",
        "redshift",
        "snowflake",
        "clickhouse",
        "mongodb",
        "mongodb+srv",
    }
)


def credential_in_uri(uri: str) -> str | None:
    """Why `uri` carries a credential (a presigned signature, a token, a
    password, a token before `@`), or None. Same rule as the server's."""
    from urllib.parse import parse_qsl, urlsplit

    try:
        parts = urlsplit(uri.strip())
        username, password = parts.username, parts.password
    except ValueError:
        return None
    scheme = parts.scheme.lower()
    if password:
        return "a password in the url (user:password@)"
    if username and scheme not in NAME_ONLY_USERINFO_SCHEMES:
        return "a user or token before @ in the url"
    for section in (parts.query, parts.fragment):
        for key, _ in parse_qsl(section, keep_blank_values=True):
            if key.strip().lower() in CREDENTIAL_PARAMS:
                return f"a `{key}` parameter (a signature or token)"
    return None


def _refuse_credential(uri: Any, field: str = "uri") -> None:
    """Refuse a pointer that carries a credential before it leaves this
    machine: a catalog pointer is shown to the whole team and to agents."""
    if not isinstance(uri, str):
        return
    reason = credential_in_uri(uri)
    if reason is not None:
        raise CatalogRefused(
            f"the {field} carries a credential ({reason}); a catalog pointer is shown to the "
            "whole team, so give it without the secret"
        )


def _refuse_excluded_local(uri: str) -> None:
    """A source naming a LOCAL path (`file:`, absolute, `./`, `~`, or one that
    exists here) a `.probe.config` keeps out (`off`, `read`) is refused: its
    path is shown to the whole team. A `hash` path may be named (its identity
    is what `hash` allows)."""
    from . import exclusions
    from . import probe_config as pc

    if _remote(uri) is not None:
        return
    local = pc.local_path_of(uri)
    if local is None:
        if not (uri.startswith(("/", "./", "../", "~")) or os.path.exists(uri)):
            return
        local = uri
    local = os.path.abspath(os.path.expanduser(local))
    verdict = exclusions.excluded(local)
    if verdict.excluded and not getattr(verdict, "identity_only", False):
        raise CatalogRefused(
            f"`{pc.shown(local)}` is excluded by `{exclusions.source(verdict)}`, so nothing was recorded about it"
        )


def source_body(
    uri: str,
    *,
    kind: str | None = None,
    revision: str | None = None,
    title: str | None = None,
    license: str | None = None,  # noqa: A002 - the field's name
    homepage: str | None = None,
    citation: str | None = None,
    retrieved_at: Any = None,
    description: str | None = None,
) -> dict:
    """The `POST /v1/sources` body. ``kind`` left out is the server's to infer
    (a Hub model repo is a `model`, everything else a `dataset`)."""
    if not isinstance(uri, str) or not uri.strip():
        raise CatalogRefused("a source needs a uri")
    _refuse_credential(uri.strip())
    _refuse_credential(homepage, "homepage")
    _refuse_excluded_local(uri.strip())
    if kind is not None:
        try:
            kind = SourceKind(str(kind)).value
        except ValueError:
            raise CatalogRefused(
                f"`{kind}` is not a source kind; use one of {', '.join(k.value for k in SourceKind)}"
            ) from None
    if retrieved_at is not None and hasattr(retrieved_at, "isoformat"):
        retrieved_at = retrieved_at.isoformat()
    fields = {
        "uri": uri.strip(),
        "kind": kind,
        "revision": revision,
        "title": title,
        "license": license,
        "homepage": homepage,
        "citation": citation,
        "retrieved_at": retrieved_at,
        "description": description,
    }
    return {k: v for k, v in fields.items() if v is not None}


def source(
    uri: str,
    *,
    kind: str | None = None,
    revision: str | None = None,
    title: str | None = None,
    license: str | None = None,  # noqa: A002 - the field's name
    homepage: str | None = None,
    citation: str | None = None,
    retrieved_at: Any = None,
    description: str | None = None,
    client: "Client | None" = None,
) -> SourceRef:
    """Register an external source -- a Hub dataset, a bucket prefix, a URL, a
    base model -- or get the one already registered (same canonical uri and
    revision). Returns a `SourceRef` to pass to `run.use_dataset` or to
    `log_dataset(sources=...)`. Never raises: a failure warns once and returns a
    `SourceRef` whose ``ref`` is None. Under `PROBE_MODE=disabled` (or a run
    that records nothing) it sends nothing and builds no client."""
    unsent = SourceRef(uri=uri if isinstance(uri, str) else None, kind=kind, revision=revision)
    try:
        body = source_body(
            uri, kind=kind, revision=revision, title=title, license=license, homepage=homepage,
            citation=citation, retrieved_at=retrieved_at, description=description,
        )
        owner = _client_for(client)
        if owner is None:
            return unsent
        from .transport import deadline_scope

        with deadline_scope(time.monotonic() + REQUEST_SECONDS):
            row = owner.create_source(body)
        return SourceRef.from_row(row or {}, uri=body["uri"])
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, f"probe.source({uri!r})")
        return unsent


def use(run: "Run", target: Any, *, role: str = Role.TRAIN.value, share: Any = None, what: str = "use_dataset") -> dict | None:
    """`POST /v1/runs/{run}/uses`: the run used ``target`` (a dataset version,
    a source or a checkpoint) for ``role``. The server pins the version a bare
    `dataset:<name>` means NOW, so a later version never rewrites what this run
    used. Never raises."""
    label = f"{what}({ref_of(target) or getattr(target, 'name', None) or target!r})"
    try:
        if isinstance(target, DatasetRef) and target.pending and not target.ref:
            # Registered moments ago and still landing: wait for it, briefly.
            target.wait(REQUEST_SECONDS)
            if not target.ref:
                raise CatalogRefused(
                    "the dataset is still pending (its registration has not landed): record the use "
                    "once `ds.wait()` returns"
                )
        ref = ref_of(target)
        if not ref:
            raise CatalogRefused("no ref to record (a source or dataset that was never registered?)")
        body: dict[str, Any] = {"target": ref, "roles": [_role(role)], "provenance": OBSERVED}
        if share is not None:
            body["share"] = check_share(share)
        return _send(run._client, f"/v1/runs/{run.id}/uses", body, what=label)
    except Exception as exc:  # noqa: BLE001
        _warn_failure(exc, label)
        return None


def use_mixture(run: "Run", parts: Mapping[Any, Any], *, role: str = Role.TRAIN.value) -> dict | None:
    """One batch to `/uses` that REPLACES the run's shares for ``role`` (V12):
    `{ref: share}`, shares summing to 1. Never raises."""
    label = "use_mixture"
    try:
        body = {"mixture": mixture_parts(parts), "role": _role(role), "provenance": OBSERVED}
        return _send(run._client, f"/v1/runs/{run.id}/uses", body, what=label)
    except Exception as exc:  # noqa: BLE001
        _warn_failure(exc, label)
        return None


# ---------------------------------------------------------------------------
# Identity: manifests, pointers
# ---------------------------------------------------------------------------


@dataclass
class ManifestFile:
    relpath: str
    size_bytes: int
    content_hash: str | None = None
    fingerprint: str | None = None
    rows: int | None = None
    #: Where it is on this machine (never sent).
    full: str = ""

    def identity_line(self) -> str:
        return f"{self.relpath}\t{self.size_bytes}\t{self.content_hash or self.fingerprint or ''}\n"

    def wire(self) -> dict:
        row: dict[str, Any] = {"relpath": self.relpath, "size_bytes": self.size_bytes}
        if self.content_hash:
            row["content_hash"] = self.content_hash
        if self.fingerprint:
            row["fingerprint"] = self.fingerprint
        if self.rows is not None:
            row["rows"] = self.rows
        return row


@dataclass
class Manifest:
    files: list[ManifestFile] = field(default_factory=list)
    #: Something is not identified by its full bytes (fingerprinted, unhashed,
    #: skipped, cut at the file ceiling).
    partial: bool = False
    #: Files a `.probe.config` keeps out (`off`/`read`): counted, never named.
    excluded: int = 0
    #: Paths left out for another reason (a link, not a regular file, unreadable).
    skipped: int = 0
    #: Some file is `hash`-level: identity only, never bytes.
    identity_only: bool = False

    @property
    def total_bytes(self) -> int:
        return sum(f.size_bytes for f in self.files)

    @property
    def rows_complete(self) -> bool:
        return bool(self.files) and all(f.rows is not None for f in self.files)

    @property
    def total_rows(self) -> int | None:
        return sum(f.rows or 0 for f in self.files) if self.rows_complete else None

    def identity(self) -> str:
        """sha256 of the sorted ``(relpath, size, sha256 | fingerprint)`` lines,
        one per file, tab-separated, newline-terminated, UTF-8 (`MANIFEST_FORMAT`).
        Rows are NOT part of it: the same bytes are the same dataset whatever
        could be counted this time."""
        digest = hashlib.sha256()
        for f in sorted(self.files, key=lambda f: f.relpath):
            digest.update(f.identity_line().encode("utf-8", "surrogatepass"))
        return digest.hexdigest()

    def body(self) -> dict:
        body: dict[str, Any] = {
            "format": MANIFEST_FORMAT,
            "files": [f.wire() for f in sorted(self.files, key=lambda f: f.relpath)],
            "partial": self.partial,
            "rows_complete": self.rows_complete,
        }
        if self.excluded:
            body["excluded"] = self.excluded
        return body

    def gz(self) -> bytes:
        raw = json.dumps(self.body(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return gzip.compress(raw.encode("utf-8", "surrogatepass"), mtime=0)


def pointer_hash(uri: str, revision: str | None = None) -> str:
    """A remote pointer's identity: ``sha256("uri\\nrevision")`` (C3)."""
    return hashlib.sha256(f"{uri}\n{revision or ''}".encode()).hexdigest()


def _levels() -> tuple[str, str, str, str]:
    from . import probe_config as pc

    return pc.ON, getattr(pc, "HASH", "hash"), pc.READ, pc.OFF


def _verdict(checker: Any, path: str, *, is_dir: bool) -> Any:
    return checker.check(path, is_dir=is_dir)


def _identify(
    path: str, *, budget: list[int], deadline: float, hash_level: bool, full: bool = False, cache: Any = None
) -> dict | None:
    """One file's identity through the recorder's own hasher (same cache, same
    budget, rows counted in the same read; `inputs.file_identity`). ``full``
    (`hash="full"`, and hosting, whose blobs are content-addressed): a file
    over the recorder's 1 GiB fingerprint line is read whole too."""
    from . import inputs

    if full and not hash_level:
        try:
            size = os.stat(path).st_size
        except OSError:
            return None
        if size > inputs.FULL_HASH_MAX_BYTES:
            from .hashing import fingerprint

            try:
                digest, size = fingerprint(path)
            except OSError:
                return None
            return {"content_hash": digest, "fingerprint": None, "size_bytes": size, "rows": None}
    return inputs.file_identity(path, budget=budget, cache=cache, deadline=deadline, hash_level=hash_level)


def _hash_cache() -> Any:
    """The recorder's per-machine hash cache: a dataset is hashed once per machine."""
    from . import inputs

    return inputs._HashCache(batch=256)


def build_manifest(
    local: str, *, budget: list[int], deadline: float, require_full: bool = False, full: bool = False
) -> Manifest:
    """The manifest of a folder (or of one file, named by its basename). The
    walk never follows a link (so it cannot escape the folder), never enters an
    `off`/`read` folder, and stops after `MAX_MANIFEST_FILES` files."""
    from . import exclusions

    cache = _hash_cache()
    try:
        return _walk_manifest(local, checker=exclusions.checker(hot=True), cache=cache, budget=budget,
                              deadline=deadline, require_full=require_full, full=full)
    finally:
        cache.flush()


def _walk_manifest(
    local: str, *, checker: Any, cache: Any, budget: list[int], deadline: float, require_full: bool, full: bool
) -> Manifest:
    on, hash_level, _read, _off = _levels()
    manifest = Manifest()
    if os.path.isfile(local):
        verdict = _verdict(checker, local, is_dir=False)
        level = getattr(verdict, "level", on)
        manifest.identity_only = level == hash_level
        _add(manifest, os.path.basename(local), local, budget=budget, deadline=deadline,
             hash_level=level == hash_level, full=full, cache=cache)
        return _settle(manifest, require_full=require_full)
    seen = 0
    walk_errors: list[OSError] = []
    for root, dirs, leaves in os.walk(local, followlinks=False, onerror=walk_errors.append):
        seen += len(dirs) + len(leaves)
        if seen > MAX_WALK_ENTRIES:
            manifest.partial = True
            break
        kept = []
        for d in sorted(dirs):
            path = os.path.join(root, d)
            if os.path.islink(path):
                manifest.skipped += 1
                continue
            level = getattr(_verdict(checker, path, is_dir=True), "level", on)
            if level not in (on, hash_level):
                manifest.excluded += 1
                continue
            kept.append(d)
        dirs[:] = kept
        for leaf in sorted(leaves):
            path = os.path.join(root, leaf)
            level = getattr(_verdict(checker, path, is_dir=False), "level", on)
            if level not in (on, hash_level):
                manifest.excluded += 1
                continue
            if os.path.islink(path) or not os.path.isfile(path):
                manifest.skipped += 1
                continue
            if len(manifest.files) >= MAX_MANIFEST_FILES:
                manifest.partial = True
                break
            if level == hash_level:
                manifest.identity_only = True
            rel = os.path.relpath(path, local).replace(os.sep, "/")
            _add(manifest, rel, path, budget=budget, deadline=deadline, hash_level=level == hash_level,
                 full=full, cache=cache)
    if walk_errors:
        manifest.skipped += len(walk_errors)
    return _settle(manifest, require_full=require_full)


def _add(
    manifest: Manifest, rel: str, path: str, *, budget: list[int], deadline: float, hash_level: bool,
    full: bool = False, cache: Any = None,
) -> None:
    got = _identify(path, budget=budget, deadline=deadline, hash_level=hash_level, full=full, cache=cache)
    if got is None:
        manifest.skipped += 1
        return
    manifest.files.append(
        ManifestFile(
            relpath=_shown_relpath(rel),
            size_bytes=int(got.get("size_bytes") or 0),
            content_hash=got.get("content_hash"),
            fingerprint=got.get("fingerprint"),
            rows=got.get("rows"),
            full=path,
        )
    )


def _shown_relpath(rel: str) -> str:
    """A relative path as it leaves the machine: scrubbed once, as the read
    recorder scrubs the paths it sends (a credential in a file name stays
    home). The identity is taken over this, so it is the same every time."""
    from . import redaction

    return redaction.scrub_string(rel)


def _settle(manifest: Manifest, *, require_full: bool) -> Manifest:
    if manifest.skipped or any(not f.content_hash for f in manifest.files):
        manifest.partial = True
    if require_full and manifest.partial:
        missing = [f.relpath for f in manifest.files if not f.content_hash]
        raise CatalogRefused(
            "hosting needs every file fully hashed and readable, and "
            + (f"{len(missing)} file(s) are not (e.g. {missing[0]})" if missing else f"{manifest.skipped} path(s) were not readable files")
        )
    return manifest


@dataclass
class Prepared:
    """A dataset's identity, ready to register."""

    uri: str
    content_hash: str
    size_bytes: int | None
    identity: str
    meta: dict
    manifest: Manifest | None = None
    #: The local file or folder, or None for a remote uri.
    local: str | None = None
    #: The `.probe.config` level of ``local`` (`on` or `hash`).
    level: str = "on"


def _remote(path_or_uri: str) -> str | None:
    """The uri when ``path_or_uri`` names something remote (`s3://`, `hf://`,
    `https://`), None for a local path (a `file://` uri included)."""
    match = _SCHEME.match(path_or_uri)
    if not match or match.group(1).lower() == "file":
        return None
    return path_or_uri


def prepare(
    path_or_uri: str | os.PathLike,
    *,
    hash_mode: str = HashMode.BUDGET.value,
    budget: list[int] | None = None,
    upload: bool = False,
) -> Prepared:
    """Work out what is being registered: a remote pointer, or a local file or
    folder hashed within ``budget`` (``hash_mode="full"``, or ``upload``: every
    byte). Raises `CatalogRefused` for a path a `.probe.config` keeps out, a
    missing path, or an upload of a `hash` path."""
    from . import exclusions
    from . import probe_config as pc
    from .hashing import local_file_uri

    try:
        mode = HashMode(str(hash_mode))
    except ValueError:
        raise CatalogRefused(f"hash must be one of {', '.join(m.value for m in HashMode)}, not {hash_mode!r}") from None
    raw = os.fspath(path_or_uri)
    remote = _remote(raw)
    if remote is not None:
        if upload:
            raise CatalogRefused(f"{remote} is remote: Probe can only host local files (leave out upload)")
        return Prepared(
            uri=remote,
            content_hash=pointer_hash(remote),
            size_bytes=None,
            identity=Identity.POINTER.value,
            meta={"identity": Identity.POINTER.value},
        )
    local = pc.local_path_of(raw) or raw
    local = os.path.abspath(os.path.expanduser(local))
    if not os.path.exists(local):
        raise CatalogRefused(f"no such file or folder: {local}")
    is_dir = os.path.isdir(local)
    on, hash_level, _read, _off = _levels()
    verdict = exclusions.excluded(local, is_dir=is_dir)
    level = getattr(verdict, "level", on if not verdict.excluded else pc.OFF)
    if level not in (on, hash_level):
        raise CatalogRefused(
            f"`{pc.shown(local)}` is excluded by `{exclusions.source(verdict)}`, so nothing was recorded about it"
        )
    if upload and level == hash_level:
        raise CatalogRefused(
            f"`{pc.shown(local)}` is `hash` in `{exclusions.source(verdict)}`: Probe records its identity "
            "only and never uploads it (leave out upload to register it as a reference)"
        )
    full = upload or mode is HashMode.FULL
    spend = [1 << 62] if full else (budget if budget is not None else _fresh_budget())
    bound = FULL_HASH_DEADLINE_SECONDS if full else HASH_DEADLINE_SECONDS
    deadline = time.monotonic() + bound
    hashed_level = level == hash_level
    host = socket.gethostname()
    meta: dict[str, Any] = {"local_path": local, "host": host}
    content_hash = size = rows = None
    identity = Identity.BYTES.value
    got, manifest = _hash_off_thread(
        lambda: _hash_local(local, single=not is_dir, upload=upload, spend=spend, deadline=deadline,
                            hashed_level=hashed_level, full=full),
        deadline=deadline,
        what=pc.shown(local),
        bound=bound,
    )
    if got is not None:
        size, rows, content_hash = got.get("size_bytes"), got.get("rows"), got.get("content_hash")
    if manifest is not None:
        content_hash = manifest.identity()
        size = manifest.total_bytes
        rows = manifest.total_rows
        identity = Identity.PARTIAL.value if manifest.partial else Identity.BYTES.value
        meta["files"] = len(manifest.files)
        if manifest.excluded:
            meta["excluded"] = manifest.excluded
        meta["rows_complete"] = manifest.rows_complete
    if rows is not None:
        meta["rows"] = rows
    meta["identity"] = identity
    if level == hash_level:
        meta["identity_only"] = True
    return Prepared(
        uri=local_file_uri(local),
        content_hash=str(content_hash),
        size_bytes=size,
        identity=identity,
        meta=meta,
        manifest=manifest,
        local=local,
        level=level,
    )


def identity_meta(local: str, run_id: str) -> dict:
    """What a `hash`-level path's reference row records beyond its location
    (`Run.log_artifact(reference=True)`: a checkpoint saved under a `.probe.config`
    `hash` rule): ``identity_only``, and its identity by the dataset rule,
    paid from the run's one hashing budget -- a file's sha256 (over 1 GiB, or
    past the budget, its fingerprint's), a folder's manifest -- as
    ``fingerprint``, the meta key the server pins a hashless checkpoint's bytes
    by, with ``identity`` saying which (`bytes` or `partial`). Never raises: a
    path gone or unreadable records its location only."""
    from . import inputs

    meta: dict[str, Any] = {"identity_only": True}
    budget = inputs.run_hash_budget(run_id)
    before = budget[0]
    try:
        prepared = prepare(local, budget=budget)
    except Exception:  # noqa: BLE001 -- the identity is evidence, never the call's failure
        return meta
    finally:
        inputs.charge_run_hash(run_id, before - budget[0])
    meta.update(fingerprint=prepared.content_hash, identity=prepared.identity)
    if prepared.meta.get("rows") is not None:
        meta["rows"] = prepared.meta["rows"]
    return meta


def _hash_local(
    local: str, *, single: bool, upload: bool, spend: list[int], deadline: float, hashed_level: bool, full: bool
) -> tuple[dict | None, Manifest | None]:
    """The walk and the hashing `prepare` waits for: ``(identity, None)`` for a
    single file fully hashed, else ``(None, manifest)``. Runs on a worker
    thread, its opens marked as Probe's own (never the run's reads)."""
    if single and not upload:
        cache = _hash_cache()
        try:
            got = _identify(local, budget=spend, deadline=deadline, hash_level=hashed_level, full=full, cache=cache)
        finally:
            cache.flush()
        if got is None:
            raise CatalogRefused(f"{local} could not be read")
        if got.get("content_hash"):
            return got, None
        # Fingerprinted, over budget or under the hash level's floor: a
        # one-file manifest carries what is known, and says partial.
        manifest = Manifest(identity_only=hashed_level, partial=True)
        manifest.files.append(ManifestFile(
            relpath=_shown_relpath(os.path.basename(local)), size_bytes=int(got.get("size_bytes") or 0),
            fingerprint=got.get("fingerprint"), rows=got.get("rows"), full=local,
        ))
        return None, manifest
    manifest = build_manifest(local, budget=spend, deadline=deadline, require_full=upload, full=full)
    if not manifest.files:
        raise CatalogRefused(f"{local} holds no file Probe may record")
    if upload and manifest.identity_only:
        from . import probe_config as pc

        raise CatalogRefused(
            f"`{pc.shown(local)}` holds files a `.probe.config` sets to `hash`: Probe records their identity "
            "only and never uploads them (leave out upload to register it as a reference)"
        )
    return None, manifest


def _hash_off_thread(work: Any, *, deadline: float, what: str, bound: float) -> Any:
    """``work()`` on a daemon thread, waited for in one-second slices (so
    Ctrl-C interrupts) until ``deadline`` plus `HASH_GRACE_SECONDS`, as
    `inputs.reference_hash` does: a stalled mount costs this call, never the
    training thread for good. Raises what ``work`` raised."""
    from . import inputs

    box: dict[str, Any] = {}

    def run() -> None:
        with inputs.internal():
            try:
                box["result"] = work()
            except BaseException as exc:  # noqa: BLE001 - handed to the caller
                box["error"] = exc

    worker = threading.Thread(target=run, name="probe-dataset-hash", daemon=True)
    worker.start()
    give_up = deadline + HASH_GRACE_SECONDS
    while worker.is_alive():
        left = give_up - time.monotonic()
        if left <= 0:
            raise CatalogRefused(
                f"hashing `{what}` did not finish within {bound:g}s (a stalled mount?); nothing was recorded"
            )
        worker.join(min(1.0, left))
    if "error" in box:
        raise box["error"]
    return box["result"]


def _fresh_budget() -> list[int]:
    from . import inputs

    return [inputs.RUN_HASH_BUDGET_BYTES]


# ---------------------------------------------------------------------------
# Registration bodies
# ---------------------------------------------------------------------------


def run_file_spec(run_id: str, name: str, prepared: Prepared) -> dict:
    """`run_file` in `POST /v1/catalog/datasets`: the producing run's file."""
    return {
        "run_id": run_id,
        "name": name,
        "uri": prepared.uri,
        "content_hash": prepared.content_hash,
        "size_bytes": prepared.size_bytes,
        "identity": prepared.identity,
        "meta": dict(prepared.meta),
    }


def reference_spec(prepared: Prepared) -> dict:
    """`reference` in `POST /v1/catalog/datasets`: a pointer no run produced."""
    return {
        "uri": prepared.uri,
        "content_hash": prepared.content_hash,
        "size_bytes": prepared.size_bytes,
        "identity": prepared.identity,
    }


def registration_body(
    name: str,
    *,
    run_file: dict | None = None,
    reference: dict | None = None,
    hosted: dict | None = None,
    note: str | None = None,
    stats: Mapping[str, Any] | None = None,
    sources: Iterable[Any] = (),
    publish: bool = False,
    description: str | None = None,
    composition: list[dict] | None = None,
) -> dict:
    """The `POST /v1/catalog/datasets` body: exactly one of ``run_file``,
    ``reference`` or ``hosted``."""
    given = [k for k, v in (("run_file", run_file), ("reference", reference), ("hosted", hosted)) if v]
    if len(given) != 1:
        raise CatalogRefused("a registration names exactly one of run_file, reference or hosted")
    body: dict[str, Any] = {"name": check_name(name), given[0]: run_file or reference or hosted}
    if reference:
        _refuse_credential(reference.get("uri"))
    change: dict[str, Any] = {}
    if note is not None:
        change["note"] = str(note)
    if stats:
        if not isinstance(stats, Mapping):
            raise CatalogRefused("stats must be a mapping of counts, e.g. {'rows': 98796, 'removed': 1204}")
        change["stats"] = dict(stats)
    if change:
        body["change"] = change
    refs = []
    for item in sources or ():
        ref = ref_of(item)
        if not ref:
            raise CatalogRefused(f"source {item!r} has no ref (was it registered?)")
        refs.append(ref)
    if refs:
        body["sources"] = refs
    if publish:
        body["publish"] = True
    if description:
        body["description"] = description
    if composition:
        body["composition"] = composition
    return body


# ---------------------------------------------------------------------------
# Hosting (C8)
# ---------------------------------------------------------------------------


def door_call_limit(blobs: int) -> int:
    """The most hosting door calls one `host` makes for a manifest naming
    ``blobs`` distinct blobs: every call answers at least
    `DOOR_ANSWERS_AT_LEAST` of those still to send, plus `DOOR_SPARE_CALLS`."""
    return max(1, math.ceil(max(0, blobs) / DOOR_ANSWERS_AT_LEAST)) + DOOR_SPARE_CALLS


def host(
    client: "Client", name: str, prepared: Prepared, *, progress: Any = None, say: Any = None
) -> dict:
    """Put the manifest, then ask the upload door for what Probe lacks, round
    by round: send each round's uploads (one PUT + confirm each, or the
    multipart doors), wait for Probe to verify the large ones, and ask again
    until the door's `deferred` is 0, within `door_call_limit` calls. Returns
    ``{have, sent, rounds}``: ``have`` the blobs Probe held before the first
    round. ``progress(n, total, file)`` is called per file sent; ``say(line)``
    once per round of a manifest that takes more than one, and before a wait
    for verification.
    Raises what the server raised (402 `hosted_data_bytes` over the cap) and
    `CatalogRefused` for an upload Probe refused or never verified."""
    manifest = prepared.manifest
    if manifest is None or prepared.local is None:
        raise CatalogRefused("only a local file or folder can be hosted")
    from .transport import deadline_scope

    digest = manifest.identity()
    with deadline_scope(time.monotonic() + MANIFEST_SECONDS):
        client.put_manifest(digest, manifest.gz())
    by_hash: dict[str, ManifestFile] = {}
    for f in manifest.files:
        if f.content_hash:
            by_hash.setdefault(f.content_hash, f)
    limit = door_call_limit(len(by_hash))
    sent: set[str] = set()
    have: list[str] | None = None
    total = 0
    for round_no in range(1, limit + 1):
        with deadline_scope(time.monotonic() + DOOR_SECONDS):
            answer = client.host_dataset_uploads(name, digest) or {}
        uploads = [u for u in answer.get("uploads") or [] if isinstance(u, Mapping)]
        deferred = answer.get("deferred")
        deferred = deferred if isinstance(deferred, int) and not isinstance(deferred, bool) and deferred > 0 else 0
        if have is None:
            have = [str(h) for h in answer.get("have") or []]
            total = len(uploads) + deferred
        # An upload this call already sent comes back only while Probe still
        # verifies it; it is never sent twice.
        fresh = [u for u in uploads if u.get("content_hash") not in sent]
        files: list[tuple[Mapping[str, Any], ManifestFile]] = []
        for item in fresh:
            f = by_hash.get(str(item.get("content_hash")))
            if f is None:
                raise CatalogRefused(
                    f"the upload door asked for {item.get('content_hash')}, which this manifest does not name"
                )
            files.append((item, f))
        if callable(say) and (deferred or round_no > 1):
            size = sum(_declared_size(item, f) for item, f in files)
            say(f"hosting round {round_no}: {len(files):,} file(s) to send ({human_bytes(size)}), "
                f"{deferred:,} more after this round")
        verifying: list[tuple[str, ManifestFile]] = []
        for item, f in files:
            sent.add(str(f.content_hash))
            if callable(progress):
                progress(len(sent), max(total, len(sent)), f)
            upload_id = _upload_blob(client, item, f, name=name, manifest_hash=digest)
            if upload_id:
                verifying.append((upload_id, f))
        # Before the next call or the registration: a large blob is hosted
        # only once Probe's verifier has hashed it, and until then the door
        # answers it again and the registration counts it missing.
        _await_verified(client, verifying, say=say)
        if not deferred:
            return {"have": have, "sent": len(sent), "rounds": round_no}
    raise CatalogRefused(
        f"the hosting door still had files to send after {limit} calls ({len(sent):,} sent); "
        "nothing was registered: run it again to send the rest (what was sent is kept)"
    )


def _declared_size(item: Mapping[str, Any], f: ManifestFile) -> int:
    """The size the door reserved for a blob, else the manifest's."""
    size = item.get("size_bytes")
    return size if isinstance(size, int) and not isinstance(size, bool) else f.size_bytes


def _upload_blob(
    client: "Client", item: Mapping[str, Any], f: ManifestFile, *, name: str, manifest_hash: str
) -> str | None:
    """Send one blob the door asked for. Returns the multipart upload id of a
    large one (Probe verifies it after), None for a PUT it confirmed. ``name``
    and ``manifest_hash`` are the door call's, should a large upload need
    opening again."""
    content_type = mimetypes.guess_type(f.relpath)[0] or "application/octet-stream"
    if item.get("multipart"):
        return _upload_parts(client, item, f, name=name, manifest_hash=manifest_hash)
    url = item.get("url")
    if not url:
        raise CatalogRefused(f"the upload door named no upload for {f.relpath}")
    client.transport.put_file(
        url, f.full, content_type=content_type, headers=item.get("headers") or item.get("upload_headers")
    )
    artifact_id = item.get("artifact_id")
    if artifact_id:
        confirm = str(item.get("confirm") or item.get("confirm_path") or "")
        try:
            client.confirm_hosted_blob(str(artifact_id), shared=confirm.startswith("/v1/shared/files/"))
        except errors.ConflictError as exc:
            # Among them: the stored object is LARGER than the size the door
            # reserved for it (its cap check trusted that size), so it is
            # never confirmed and nothing can register it.
            raise CatalogRefused(
                f"Probe refused the upload of {f.relpath} ({human_bytes(_declared_size(item, f))} "
                f"reserved): {exc}. Did it change after it was hashed? Run it again."
            ) from exc
    return None


def _upload_parts(
    client: "Client", item: Mapping[str, Any], f: ManifestFile, *, name: str, manifest_hash: str
) -> str | None:
    """A blob over the single-PUT ceiling, through the existing multipart
    client at the Shared anchor: the door already opened the upload (or
    resumed it), so the op starts with its id and goes straight to parts and
    complete. An upload Probe gives up on is opened again by the door, never
    the generic create (`reopen_hosted`). Returns the id of the upload Probe
    verifies after, or None when the blob turned out hosted already."""
    from . import multipart
    from .anchors import Anchor

    spec = item["multipart"] if isinstance(item.get("multipart"), dict) else {}
    upload_id = spec.get("upload_id")
    if not upload_id or not spec.get("part_size") or not spec.get("part_count"):
        raise CatalogRefused(f"the upload door's multipart answer for {f.relpath} names no upload")
    st = os.stat(f.full)
    op = {
        "op_id": f"hosted-{f.content_hash}",
        "multipart": {
            "staged_path": f.full,
            "stage_mode": "none",
            "identity": multipart._identity(st),
            "staged_at": time.time(),
            "upload_id": upload_id,
            "artifact_id": item.get("artifact_id") or spec.get("artifact_id"),
            "part_size": spec["part_size"],
            "part_count": spec["part_count"],
            "state": spec.get("state") or "uploading",
        },
        "upload": {
            "anchor": Anchor.SHARED.value,
            "anchor_id": None,
            "name": f"{HOSTED_PREFIX}{f.content_hash}",
            "src_path": f.full,
            "blob": f.content_hash,
            "size_bytes": f.size_bytes,
            # Which door opens it again (`multipart._create`).
            "hosted": {"name": name, "manifest_hash": manifest_hash},
        },
    }
    multipart.advance(client, op, lambda: None, deadline=float("inf"), wait_for_verify=False)
    state = op["multipart"]
    if state.get("state") == "have":
        return None
    # A restart opened a new upload: that one is what Probe verifies.
    return str(state.get("upload_id") or upload_id)


def reopen_hosted(client: "Client", upload: Mapping[str, Any]) -> dict:
    """Open a hosted blob's large upload again, in the multipart create's
    answer shape (`multipart._create`): after Probe gave up on the first one
    (idle past its sweep, say), the multipart client starts again. Its name,
    `.probe/datasets/<sha256>`, is one only the hosting door may stage -- the
    generic Shared create refuses it (422) -- so the door is asked again: it
    re-stages the blob and answers a fresh `multipart` for it, or lists it
    under `have` once it is hosted by now."""
    from .transport import deadline_scope

    door, blob = upload["hosted"], str(upload.get("blob"))
    with deadline_scope(time.monotonic() + DOOR_SECONDS):
        answer = client.host_dataset_uploads(door["name"], door["manifest_hash"]) or {}
    if blob in [str(h) for h in answer.get("have") or []]:
        return {"have": True, "artifact_id": None}
    item = next(
        (u for u in answer.get("uploads") or [] if isinstance(u, Mapping) and u.get("content_hash") == blob),
        None,
    )
    spec = item.get("multipart") if item is not None else None
    if not (isinstance(spec, Mapping) and spec.get("upload_id") and spec.get("part_size") and spec.get("part_count")):
        raise CatalogRefused(
            f"the hosting door did not open the upload of blob {blob} again; nothing was registered: "
            "run it again (what was sent is kept)"
        )
    return {
        "upload_id": spec["upload_id"],
        "artifact_id": item.get("artifact_id"),
        "part_size": spec["part_size"],
        "part_count": spec["part_count"],
        "state": spec.get("state") or "uploading",
    }


def _await_verified(client: "Client", waiting: list[tuple[str, ManifestFile]], *, say: Any = None) -> None:
    """Wait, within `HOSTED_VERIFY_SECONDS`, until Probe has verified every
    large upload in ``waiting`` (`verified`: the blob is hosted). Its verifier
    hashes them one after another server side, so they are waited for in turn."""
    if not waiting:
        return
    from . import multipart
    from .anchors import Anchor

    if callable(say):
        size = sum(f.size_bytes for _id, f in waiting)
        say(f"waiting for Probe to verify {len(waiting):,} large file(s) ({human_bytes(size)})")
    shared = {"anchor": Anchor.SHARED.value}
    deadline = time.monotonic() + HOSTED_VERIFY_SECONDS
    for upload_id, f in waiting:
        while True:
            status = multipart._status(client, shared, upload_id) or {}
            state = status.get("state")
            if state == "verified":
                break
            if state != "verifying":
                raise CatalogRefused(
                    f"Probe could not verify the upload of {f.relpath}: it is {state or 'gone'} "
                    f"({status.get('failure_reason') or 'no reason given'}); nothing was registered: run it again"
                )
            if time.monotonic() >= deadline:
                raise CatalogRefused(
                    f"Probe was still verifying {f.relpath} after {HOSTED_VERIFY_SECONDS:g}s; nothing was "
                    "registered: run it again later to register it (the upload is kept)"
                )
            time.sleep(HOSTED_VERIFY_POLL_SECONDS)


# ---------------------------------------------------------------------------
# Preview samples (C11)
# ---------------------------------------------------------------------------


def preview_sample(path: str) -> tuple[bytes, int, str] | None:
    """The first `PREVIEW_MAX_RECORDS` records of a line-record file (CSV/TSV:
    the header plus that many), cut at a whole line within `PREVIEW_MAX_BYTES`;
    a Parquet file's first rows as JSONL only when `pyarrow` is already
    imported. ``(bytes, records, extension)``, or None when there is nothing
    to show."""
    from . import inputs

    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        with inputs.internal():  # Probe's own read, never one of the run's
            return _parquet_sample(path)
    if ext not in _LINE_SUFFIXES:
        return None
    try:
        with inputs.internal(), open(path, "rb") as handle:
            head = handle.read(PREVIEW_MAX_BYTES + 1)
    except OSError:
        return None
    lines = head.splitlines(keepends=True)
    if len(head) > PREVIEW_MAX_BYTES and lines and not lines[-1].endswith((b"\n", b"\r")):
        lines = lines[:-1]  # cut at the last whole line
    keep = PREVIEW_MAX_RECORDS + (1 if ext in _HEADER_SUFFIXES else 0)
    kept = lines[:keep]
    out = b"".join(kept)
    while len(out) > PREVIEW_MAX_BYTES and kept:
        kept = kept[:-1]
        out = b"".join(kept)
    records = len(kept) - (1 if ext in _HEADER_SUFFIXES and kept else 0)
    if records <= 0:
        return None
    return out, records, ".jsonl" if ext == ".ndjson" else ext


def _parquet_sample(path: str) -> tuple[bytes, int, str] | None:
    if "pyarrow" not in sys.modules:
        return None  # never imported for this (R27): no sample
    try:
        import pyarrow.parquet as pq

        batch = next(pq.ParquetFile(path).iter_batches(batch_size=PREVIEW_MAX_RECORDS), None)
        if batch is None:
            return None
        out = b""
        records = 0
        for row in batch.to_pylist():
            line = (json.dumps(row, default=str, ensure_ascii=False) + "\n").encode("utf-8")
            if len(out) + len(line) > PREVIEW_MAX_BYTES:
                break
            out += line
            records += 1
        return (out, records, ".jsonl") if records else None
    except Exception:  # noqa: BLE001 - no sample, never a failure
        return None


def _previewable(prepared: Prepared) -> str | None:
    """The file a preview is cut from: the dataset itself, or a folder's first
    line-record (or Parquet) file in path order. Only `on` paths."""
    on, *_ = _levels()
    if prepared.local is None or prepared.level != on:
        return None
    if prepared.manifest is None:
        return prepared.local
    from . import exclusions

    checker = exclusions.checker(hot=True)
    for f in sorted(prepared.manifest.files, key=lambda f: f.relpath):
        ext = os.path.splitext(f.relpath)[1].lower()
        if ext not in _LINE_SUFFIXES + (".parquet",):
            continue
        if getattr(checker.check(f.full, is_dir=False), "level", on) == on:
            return f.full
    return None


def upload_preview(send: Any, prepared: Prepared, dataset_file_id: str) -> bool:
    """Upload a preview sample of a dataset kept outside Probe, as the run file
    `.probe/previews/<dataset file id><ext>` with `meta.preview_of`, and say so
    in one line. ``send(name, path, meta)`` uploads one file to the producing
    run (the SDK's `log_artifact`, the CLI's `upload_file`). True when one was
    uploaded. Never raises."""
    try:
        source_path = _previewable(prepared)
        if source_path is None:
            return False
        sample = preview_sample(source_path)
        if sample is None:
            return False
        data, records, ext = sample
        handle, tmp = tempfile.mkstemp(prefix="probe-preview-", suffix=ext)
        try:
            with os.fdopen(handle, "wb") as out:
                out.write(data)
            send(f"{PREVIEW_PREFIX}{dataset_file_id}{ext}", tmp, {"preview_of": dataset_file_id})
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        from . import probe_config as pc

        _say(
            f"probe: uploaded a {records}-row preview of {pc.shown(source_path)}; "
            "preview=False (--no-preview) to stop"
        )
        return True
    except Exception as exc:  # noqa: BLE001 - a preview is never worth a failure
        _warn_once(f"preview:{type(exc).__name__}", f"probe: no preview sample was uploaded ({exc})")
        return False


# ---------------------------------------------------------------------------
# log_dataset
# ---------------------------------------------------------------------------


def _run_sender(run: "Run") -> Any:
    def send(name: str, path: str, meta: dict) -> None:
        run.log_artifact(name, path=path, sync=True, meta=meta)

    return send


def log_dataset(
    run: "Run",
    path_or_uri: str | os.PathLike,
    name: str,
    *,
    register: bool = True,
    publish: bool = False,
    upload: bool = False,
    sources: Iterable[Any] = (),
    note: str | None = None,
    stats: Mapping[str, Any] | None = None,
    hash: str = HashMode.BUDGET.value,  # noqa: A002 - the plan's name
    composition: Mapping[Any, Any] | None = None,
    preview: bool = True,
    description: str | None = None,
    wait: float = REGISTER_WAIT_SECONDS,
) -> DatasetRef:
    """`Run.log_dataset`; see the module docstring. Never raises."""
    out = DatasetRef(name=name if isinstance(name, str) else None)
    what = f"log_dataset({name!r})"
    try:
        _log_dataset(
            run, out, path_or_uri, name, register=register, publish=publish, upload=upload, sources=sources,
            note=note, stats=stats, hash_mode=hash, composition=composition, preview=preview,
            description=description, wait=wait, what=what,
        )
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, what)
        out._done.set()
    return out


def _log_dataset(
    run: "Run",
    out: DatasetRef,
    path_or_uri: str | os.PathLike,
    name: str,
    *,
    register: bool,
    publish: bool,
    upload: bool,
    sources: Iterable[Any],
    note: str | None,
    stats: Mapping[str, Any] | None,
    hash_mode: str,
    composition: Mapping[Any, Any] | None,
    preview: bool,
    description: str | None,
    wait: float,
    what: str,
) -> None:
    client = run._client
    check_name(name)
    parts = composition_parts(composition) if composition else None
    if catalog_available(client) is False:
        raise errors.NotFoundError("Not Found", status=404, detail="Not Found")
    from . import inputs

    # The run's ONE hashing budget (its reads, its outputs, its datasets).
    budget = inputs.run_hash_budget(run.id)
    before = budget[0]
    try:
        prepared = prepare(path_or_uri, hash_mode=hash_mode, budget=budget, upload=upload)
    finally:
        inputs.charge_run_hash(run.id, before - budget[0])
    out.content_hash, out.identity = prepared.content_hash, prepared.identity
    common = dict(note=note, stats=stats, sources=sources, publish=publish, description=description,
                  composition=parts)
    if upload:
        host(client, name, prepared, say=lambda line: _say(f"probe: {what}: {line}"))
        # The run is the version's producer: the server records it as the step.
        body = registration_body(
            name, hosted={"manifest_hash": prepared.content_hash, "run_id": run.id}, **common
        )
        _register_bounded(client, body, out, wait=wait, what=what, after=None)
        return
    queued = prepared.manifest is not None and not _ship_manifest(client, prepared)
    if not register:
        row = _record_run_file(run, name, prepared)
        if row and row.get("id"):
            out.artifact_id = str(row["id"])
            out.ref = f"artifact:{row['id']}"
            if preview:
                upload_preview(_run_sender(run), prepared, out.artifact_id)
        out._done.set()
        return
    body = registration_body(name, run_file=run_file_spec(run.id, name, prepared), **common)
    if queued:
        # The manifest waits in the outbox: the registration that needs it
        # waits right behind it, never ahead of it.
        _queue_registration(client, body, out, what=what)
        return

    def after() -> None:
        if not preview or prepared.local is None:
            return
        row = run.reconcile_artifact(name, prepared.content_hash)
        if row and row.get("id") and row.get("state") != "queued":
            out.artifact_id = str(row["id"])
            upload_preview(_run_sender(run), prepared, out.artifact_id)

    _register_bounded(client, body, out, wait=wait, what=what, after=after)


def _ship_manifest(client: "Client", prepared: Prepared) -> bool:
    """PUT the manifest within `MANIFEST_SECONDS`. True when it landed; False
    when Probe could not take it now and it was queued in the outbox (the
    caller then queues the registration behind it). A refusal raises."""
    from .journal import classify
    from .transport import deadline_scope

    manifest = prepared.manifest
    assert manifest is not None
    gz = manifest.gz()
    try:
        with deadline_scope(time.monotonic() + MANIFEST_SECONDS):
            client.put_manifest(prepared.content_hash, gz)
        return True
    except errors.RosError as exc:
        if old_server(exc) or classify(exc) in ("permanent", "idempotent"):
            raise
    client.journal.append_catalog_manifest(prepared.content_hash, gz)
    return False


def _queue_registration(client: "Client", body: dict, out: DatasetRef, *, what: str) -> None:
    """Queue the registration behind its queued manifest; ``out`` stays pending."""
    landed = client._enqueue("POST", "/v1/catalog/datasets", body)
    if landed:
        client._after_enqueue()
    out.pending = bool(landed)
    out._done.set()
    _warn_once(
        "log_dataset:queued",
        f"probe: {what}: Probe could not take the dataset's manifest now"
        + (", so it and the registration are queued in the outbox and go when Probe answers."
           if landed else "; the outbox could not hold the registration either, so it was not recorded."),
    )


def _record_run_file(run: "Run", name: str, prepared: Prepared) -> dict | None:
    """`register=False`: the run's dataset file alone, a reference row on the
    run (the manifest already names its files)."""
    from .artifact_kinds import ArtifactKind

    body = {
        "kind": ArtifactKind.DATASET.value,
        "name": name,
        "uri": prepared.uri,
        "content_hash": prepared.content_hash,
        "size_bytes": prepared.size_bytes,
        "is_reference": True,
        "meta": dict(prepared.meta),
    }
    return _send(run._client, f"/v1/runs/{run.id}/artifacts", body, what=f"log_dataset({name!r}, register=False)")


def _register_bounded(
    client: "Client", body: dict, out: DatasetRef, *, wait: float, what: str, after: Any
) -> None:
    """Send the registration on a thread and wait at most ``wait`` seconds for
    it; past that ``out`` is returned pending and filled when it lands. A
    failure that could succeed later is queued in the outbox."""

    def work() -> None:
        from .transport import deadline_scope

        try:
            # One bound for the registration AND what follows it (finding the
            # run file, the preview upload).
            with deadline_scope(time.monotonic() + REGISTER_DEADLINE_SECONDS):
                answer = client.write("POST", "/v1/catalog/datasets", body, sync=True, raise_permanent=True)
                if isinstance(answer, dict):
                    out._fill(answer)
                    if callable(after):
                        after()
                else:
                    out.pending = True  # queued in the outbox: delivered later, never filled here
        except Exception as exc:  # noqa: BLE001
            out.pending = False
            _warn_failure(exc, what)
        finally:
            out._done.set()

    out.pending = True
    worker = threading.Thread(target=work, name="probe-log-dataset", daemon=False)
    worker.start()
    if not out._done.wait(max(0.0, float(wait))):
        _warn_once(
            "log_dataset:pending",
            f"probe: {what}: Probe has not answered within {wait:g}s; the registration goes on in "
            "the background (the returned ref fills in when it lands; DatasetRef.wait() waits for it).",
        )


# ---------------------------------------------------------------------------
# Printing (the CLI's tables)
# ---------------------------------------------------------------------------


def human_bytes(n: Any) -> str:
    """`41.2 GB` (decimal units, as the plan's examples print)."""
    if not isinstance(n, (int, float)) or isinstance(n, bool):
        return "-"
    value = float(n)
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if abs(value) < 1000 or unit == "TB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1000
    return f"{value:.1f} PB"
