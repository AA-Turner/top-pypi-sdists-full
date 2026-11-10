"""The data catalog from inside a training job (plan data-catalog C5, C8-C11).

    src = probe.source("https://huggingface.co/datasets/allenai/c4", revision="1588ec4",
                       license="ODC-BY")                      # upsert, returns a ref
    run.use_dataset(src, role="train")                        # POST /v1/runs/{id}/uses
    run.use_dataset("dataset:c4-clean@3", role="validation")
    run.use_mixture({"dataset:a@2": 0.7, "dataset:b@1": 0.3})  # one batch, replaces train shares
    run.use_checkpoint("checkpoint:sft-7b@best")              # role init: the weights it started from
    ds = run.log_dataset("data/clean/", name="c4-clean", sources=[src],
                         note="dropped 1,204 seqs >90% identical to test")

NEVER RAISES INTO A JOB: every verb warns once and returns quietly on an old server
(404/405 for the route), a network error, a refusal (409, 422, 402) or a bug of ours.
The CLI's raising HTTP calls are `Client` methods (`create_source`, `use_in_run`, ...).

`log_dataset` (C5, Q9): a folder is identified by its sorted MANIFEST (relative path, size,
sha256 or fingerprint per file), PUT to `/v1/catalog/manifests/{sha256}`, then ONE
`POST /v1/catalog/datasets` registers it. It waits at most `REGISTER_WAIT_SECONDS`, then
returns `DatasetRef(pending=True)` and finishes in the background (queued if Probe is
unreachable). A remote uri is never read: identity is ``sha256("uri\\nrevision")``.
`upload=True` (C8) hosts the bytes in Probe (`hosting.py`). Preview samples
(C11): the first 100 records (or 256 KiB) of an unhosted dataset go up as a run file
`.probe/previews/<dataset file id><ext>` (`meta.preview_of`, `storage_class='preview'`,
hidden); `preview=False` turns it off.

Full text: DESIGN.md in this folder.
"""

from __future__ import annotations
import threading
import time
from typing import TYPE_CHECKING, Any, Mapping

from .. import errors
from .vocab import Role, SourceKind

if TYPE_CHECKING:  # pragma: no cover
    from ..client.client import Client
    from ..run.run import Run
from probe.sdk.catalog.refs import (
    CatalogRefused,
    DatasetRef,
    SourceRef,
    check_share,
    is_moving_ref,
    mixture_parts,
    ref_of,
)
from probe.sdk.catalog.server import _warn_failure, could_succeed_later, warn_not_queued
#: Bound on one small catalog request on the training thread (use, source, catalog probe) and on waiting for a pending ref.
REQUEST_SECONDS = 10.0
#: `lineage_edges.provenance` for a use the SDK saw; the CLI's are a person's word. The server
#: stores the daemon's key as `inferred` whatever it sends.
OBSERVED = "observed_call"


def _role(role: Any) -> str:
    try:
        return Role(str(role)).value
    except ValueError:
        raise CatalogRefused(
            f"`{role}` is not a role; use one of {', '.join(r.value for r in Role)}"
        ) from None


def _send(client: "Client", path: str, body: dict, *, what: str, queue: bool = True) -> dict | None:
    """One small catalog write from a training thread, sent within `REQUEST_SECONDS`; a refusal
    warns once, a failure that could still succeed is queued (the SDK's fail-open path).

    ``queue=False`` (a use naming a moving ref, D17): NOT queued, since a replay would resolve
    the ref later, maybe to a newer version than the run used, yet still read as seen in code."""
    from ..delivery.transport.deadlines import deadline_scope

    try:
        with deadline_scope(time.monotonic() + REQUEST_SECONDS):
            if queue:
                return client.send("POST", path, body, raise_permanent=True)
            return client.send("POST", path, body, strict=True)
    except errors.RosError as exc:
        if not queue and could_succeed_later(exc):
            warn_not_queued(client, what, exc)
            return None
        _warn_failure(exc, what)
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, what)
    return None


_ambient: "Client | None" = None
_ambient_lock = threading.Lock()


def _client_for(client: "Client | None") -> "Client | None":
    """The client a module-level verb uses: the one given, the bound run's, or one built from
    the environment (kept per process). None (nothing sent, no Client built) under
    `PROBE_MODE=disabled`/`offline` or when the bound run records nothing (disabled, `off` folder)."""
    global _ambient
    if client is not None:
        return client
    from ..settings.settings import Mode, resolve_mode

    try:
        if resolve_mode() is not Mode.ONLINE:
            return None
    except Exception:  # noqa: BLE001 - an unreadable PROBE_MODE sends nothing
        return None
    try:
        from ..fluent.fluent import active_run

        run = active_run()
    except Exception:  # noqa: BLE001
        run = None
    if run is not None:
        if getattr(run, "disabled", False):
            return None
        return getattr(run, "_client", None)
    with _ambient_lock:
        if _ambient is None:
            from ..client.client import Client

            _ambient = Client()
        return _ambient


# Sources and uses


#: Query/fragment parameters carrying a secret (case-insensitive). The client's copy of the
#: server's `app/catalog/uris.py` `CREDENTIAL_PARAMS` (held equal by `test_catalog_sdk.py`):
#: refusing here keeps the token on this machine; the server refuses it too.
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
#: Schemes whose userinfo is a plain name (server: `_NAME_ONLY_USERINFO_SCHEMES`); a password is refused on these too.
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
    """Why `uri` carries a credential (presigned signature, token, password, token before `@`), else None. The server's rule."""
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
    """Refuse a credential-bearing pointer before it leaves this machine (catalog pointers are shown to the team and agents)."""
    if not isinstance(uri, str):
        return
    reason = credential_in_uri(uri)
    if reason is not None:
        raise CatalogRefused(
            f"the {field} carries a credential ({reason}); a catalog pointer is shown to the "
            "whole team, so give it without the secret"
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
    """The `POST /v1/sources` body. ``kind`` omitted is inferred by the server (Hub model repo: `model`, else `dataset`)."""
    if not isinstance(uri, str) or not uri.strip():
        raise CatalogRefused("a source needs a uri")
    _refuse_credential(uri.strip())
    _refuse_credential(homepage, "homepage")
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
    """Register an external source (Hub dataset, bucket prefix, URL, base model) or get the
    registered one (same canonical uri and revision). Returns a `SourceRef` for
    `run.use_dataset` or `log_dataset(sources=...)`. Never raises: a failure warns once and
    returns a `SourceRef` with ``ref`` None. Under `PROBE_MODE=disabled` (or a run recording
    nothing) it sends nothing and builds no client."""
    unsent = SourceRef(uri=uri if isinstance(uri, str) else None, kind=kind, revision=revision)
    try:
        body = source_body(
            uri, kind=kind, revision=revision, title=title, license=license, homepage=homepage,
            citation=citation, retrieved_at=retrieved_at, description=description,
        )
        owner = _client_for(client)
        if owner is None:
            return unsent
        from ..delivery.transport.deadlines import deadline_scope

        with deadline_scope(time.monotonic() + REQUEST_SECONDS):
            row = owner.create_source(body)
        return SourceRef.from_row(row or {}, uri=body["uri"])
    except Exception as exc:  # noqa: BLE001 - never into the job
        _warn_failure(exc, f"probe.source({uri!r})")
        return unsent


def use(run: "Run", target: Any, *, role: str = Role.TRAIN.value, share: Any = None, what: str = "use_dataset") -> dict | None:
    """`POST /v1/runs/{run}/uses`: the run used ``target`` (dataset version, source or checkpoint)
    for ``role``. The server pins what a bare `dataset:<name>` means NOW, so a later version
    never rewrites it; for that reason a moving ref is never queued (see `_send`). A `SourceRef`
    not registered (no ``ref``, a ``uri``) goes by its uri: the server finds or registers the
    source in the same request, which a run token may do. Never raises."""
    uri = getattr(target, "uri", None) if isinstance(target, SourceRef) else None
    if isinstance(uri, str) and credential_in_uri(uri) is not None:
        uri = "a uri carrying a credential"  # never into a warning
    named = ref_of(target) or uri or getattr(target, "name", None)
    label = f"{what}({named or repr(target)})"
    try:
        if isinstance(target, SourceRef) and not target.ref and target.uri:
            wire = source_body(target.uri, kind=target.kind, revision=target.revision)
            body: dict[str, Any] = {"source": wire, "roles": [_role(role)], "provenance": OBSERVED}
            if share is not None:
                body["share"] = check_share(share)
            return _send(run._client, f"/v1/runs/{run.id}/uses", body, what=label)
        if isinstance(target, DatasetRef) and target.pending and not target.ref:
            # Registered moments ago, still landing: wait briefly.
            target.wait(REQUEST_SECONDS)
            if not target.ref:
                raise CatalogRefused(
                    "the dataset is still pending (its registration has not landed): record the use "
                    "once `ds.wait()` returns"
                )
        ref = ref_of(target)
        if not ref:
            raise CatalogRefused("no ref to record (a source or dataset that was never registered?)")
        body = {"target": ref, "roles": [_role(role)], "provenance": OBSERVED}
        if share is not None:
            body["share"] = check_share(share)
        return _send(run._client, f"/v1/runs/{run.id}/uses", body, what=label, queue=not is_moving_ref(ref))
    except Exception as exc:  # noqa: BLE001
        _warn_failure(exc, label)
        return None


def use_mixture(run: "Run", parts: Mapping[Any, Any], *, role: str = Role.TRAIN.value) -> dict | None:
    """One `/uses` batch that REPLACES the run's shares for ``role`` (V12): `{ref: share}`, summing
    to 1. Never raises. A mixture with any moving ref is never queued (see `_send`)."""
    label = "use_mixture"
    try:
        wire = mixture_parts(parts)
        body = {"mixture": wire, "role": _role(role), "provenance": OBSERVED}
        queue = not any(is_moving_ref(p["target"]) for p in wire)
        return _send(run._client, f"/v1/runs/{run.id}/uses", body, what=label, queue=queue)
    except Exception as exc:  # noqa: BLE001
        _warn_failure(exc, label)
        return None
