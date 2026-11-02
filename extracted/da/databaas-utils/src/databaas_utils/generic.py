"""Blob storage under a Lakekeeper generic table, without S3 credentials.

Every request is signed by Lakekeeper's own signer: the client asks the catalog
to sign a method/URI/header triple and then issues the signed request itself, so
no long-lived S3 key ever reaches the task.

The credentialed fallback from the prior art is deliberately absent. A fallback
that quietly works without signing is how a deployment ends up on it without
anyone deciding to.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Iterator
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from databaas_utils.catalog import CatalogClient
from databaas_utils.diagnostics import check_obstore
from databaas_utils.errors import LakehouseError, RemoteSigningUnavailable, SignError
from databaas_utils.settings import (
    LakehouseSettings,
    OAuthClientCredentials,
    StaticToken,
)

if TYPE_CHECKING:
    from obstore.store import RemoteSignedS3Store

log = logging.getLogger(__name__)

SIGN_TIMEOUT = 30

# urllib3 excludes POST from default retries as unsafe. Signing is the
# exception: it returns a signature and mutates nothing, so retrying a dropped
# sign POST is safe.
_SIGN_RETRY = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=(502, 503, 504),
    allowed_methods=frozenset({"POST"}),
)

_thread_local = threading.local()


def _session_for_thread() -> requests.Session:
    """One pooled, retrying session per thread.

    `requests.Session` is not thread-safe, and obstore's Rust/tokio runtime
    invokes the sign callback from several threads for one store (concurrent
    multipart parts), so a session must never be shared across threads.
    """
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=_SIGN_RETRY)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        _thread_local.session = session
    return session


def remote_signing_available() -> bool:
    """Whether this environment can sign generic-table requests.

    A capability probe, not a version check: it asks whether the class and
    method exist rather than which distribution or release provided them.
    """
    try:
        from obstore.store import RemoteSignedS3Store
    except ImportError:
        return False
    return hasattr(RemoteSignedS3Store, "from_s3_url")


class _TokenProviderAuth:
    """Adapts any ``TokenProvider`` to pylakekeeper's ``Auth`` interface.

    Unlike ``LkStaticToken``, this re-reads ``settings.credentials`` on every
    call, so a provider that refreshes itself (``UserLogin``,
    ``ServiceAccountKey``, ...) stays current for the life of the client
    instead of being frozen at construction time.
    """

    def __init__(self, provider: Any) -> None:
        self._provider = provider

    def auth_header(self) -> str:
        return str(self._provider.auth_header())

    def invalidate(self) -> None:
        invalidate = getattr(self._provider, "invalidate", None)
        if invalidate is not None:
            invalidate()


def lakekeeper_auth(settings: LakehouseSettings) -> Any:
    """A pylakekeeper Auth for these settings."""
    from pylakekeeper import ClientCredentials
    from pylakekeeper import StaticToken as LkStaticToken

    creds = settings.credentials
    if isinstance(creds, OAuthClientCredentials):
        return ClientCredentials(
            token_url=creds.token_url,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scope=creds.effective_scope,
        )
    if isinstance(creds, StaticToken):
        return LkStaticToken(creds.token)
    # A custom, self-refreshing TokenProvider (UserLogin, ServiceAccountKey, ...).
    return _TokenProviderAuth(creds)


@dataclass(frozen=True)
class ResolvedTable:
    """A generic table's location plus what is needed to sign requests under it.

    Attributes:
        location: The table's ``s3://`` base URI.
        signer_uri: The full URL of Lakekeeper's signing endpoint.
        region: Storage region reported by Lakekeeper.
        endpoint: S3 endpoint, or ``""`` for AWS proper.
    """

    location: str
    signer_uri: str
    region: str
    endpoint: str


def resolve(
    settings: LakehouseSettings,
    table: str,
    *,
    create: bool = True,
    doc: str = "Generic table",
    client: CatalogClient | None = None,
) -> ResolvedTable:
    """Look up `settings.namespace`.`table`, creating it if asked.

    Args:
        settings: Which warehouse and namespace, as which identity.
        table: Generic table name.
        create: Create the table (and namespace) if missing. With ``False`` a
            missing table raises.
        doc: Description recorded on a newly created table.
        client: A ``CatalogClient`` to reuse.

    Returns:
        The table's location and signing details.

    Raises:
        pylakekeeper.NotFoundError: The table is missing and ``create`` is false.
        LakehouseError: Lakekeeper did not advertise a signer for the table.
    """
    from pylakekeeper import Client, ConflictError, GenericTableFormat, NotFoundError

    catalog = client or CatalogClient(settings)
    warehouse_id = catalog.warehouse_id()

    with Client(
        base_url=settings.base_url,
        warehouse=warehouse_id,
        auth=lakekeeper_auth(settings),
    ) as lk:
        try:
            loaded = lk.generic_tables.load(settings.namespace, table, vended=True)
        except NotFoundError:
            if not create:
                raise
            log.info("creating generic table %s.%s", settings.namespace, table)
            catalog.ensure_namespace(settings.namespace)
            # A parallel task may win the create race; the load below is what
            # actually matters.
            with suppress(ConflictError):
                lk.generic_tables.create(
                    settings.namespace,
                    table,
                    format=GenericTableFormat.DATASET,
                    doc=doc,
                )
            loaded = lk.generic_tables.load(settings.namespace, table, vended=True)

    config: dict[str, Any] = {
        key: value
        for credential in (loaded.storage_credentials or [])
        for key, value in credential.config.items()
    }
    config.update(loaded.config or {})

    signer_uri = config.get("s3.signer.uri")
    if not signer_uri:
        raise LakehouseError(
            f"{settings.namespace}.{table} advertises no s3.signer.uri — is this "
            "Lakekeeper new enough to sign for generic tables?"
        )

    return ResolvedTable(
        location=loaded.location,
        # Lakekeeper returns base and endpoint separately; joining them here is
        # why the catalog properties must not hand pyiceberg a prebuilt URI.
        signer_uri=urljoin(signer_uri, config.get("s3.signer.endpoint")),
        region=config.get("s3.region") or config.get("region") or "",
        endpoint=(config.get("s3.endpoint") or "").rstrip("/"),
    )


def signing_callback(
    settings: LakehouseSettings,
    resolved: ResolvedTable,
    *,
    session: requests.Session | None = None,
):
    """Build the per-request signer obstore calls out to.

    `session` pins every call to one session and is test-only. Production
    callers leave it unset so each invocation reads the *calling thread's* own
    pooled session — the store this backs may be cached and later invoked from
    a different thread.
    """

    def sign(method: str, uri: str, headers: dict[str, Any]):
        http = session if session is not None else _session_for_thread()
        payload: dict[str, Any] = {
            "method": method,
            "region": resolved.region,
            "uri": uri,
            # The signer replaces the headers it is given, so it must echo back
            # everything the request still needs (range, content-length, ...).
            "headers": {
                key: ([value] if isinstance(value, str) else value)
                for key, value in headers.items()
            },
        }
        response = http.post(
            resolved.signer_uri,
            json=payload,
            # Re-read per call: a cached store must not pin a stale bearer.
            headers={"Authorization": settings.auth_header()},
            timeout=SIGN_TIMEOUT,
        )
        if not response.ok:
            raise SignError(
                f"signing {method} {uri} failed with {response.status_code}: "
                f"{response.text}"
            )
        signed = response.json()
        return signed["uri"], {
            key: (value[0] if isinstance(value, list) else value)
            for key, value in signed["headers"].items()
        }

    return sign


def _client_options(resolved: ResolvedTable) -> dict[str, bool]:
    """Client options for the resolved endpoint.

    obstore's Rust object_store refuses a plaintext endpoint outright —
    `reqwest::Error { kind: Builder, source: BadScheme }`, raised before any I/O
    — unless `allow_http` is set. Production endpoints are https and unaffected;
    this only enables it where the endpoint is *already* plaintext by
    configuration, so it weakens nothing that was not already plaintext.
    """
    if resolved.endpoint.startswith("http://"):
        return {"allow_http": True}
    return {}


def signed_store(
    settings: LakehouseSettings,
    resolved: ResolvedTable,
    *,
    prefix: str = "",
    session: requests.Session | None = None,
    client_options: Any = None,
) -> RemoteSignedS3Store:
    """An obstore store over `resolved`, signing each request as it goes out.

    Args:
        settings: Supplies the bearer used to call Lakekeeper's signer.
        resolved: The table to open, from :func:`resolve`.
        prefix: Restrict the store to keys under this prefix.
        session: Pin all signing calls to one session (tests only).
        client_options: Extra obstore client options.

    Raises:
        RemoteSigningUnavailable: If ``obstore-databaas`` is not installed.
    """
    check_obstore()
    try:
        from obstore.store import RemoteSignedS3Store
    except ImportError as exc:
        raise RemoteSigningUnavailable(
            "obstore is not installed — remote-signed access needs the "
            "obstore-databaas distribution, which carries RemoteSignedS3Store. "
            "Install databaas-utils[obstore]."
        ) from exc
    if not hasattr(RemoteSignedS3Store, "from_s3_url"):
        raise RemoteSigningUnavailable(
            "the installed obstore has no RemoteSignedS3Store.from_s3_url — an "
            "upstream obstore has probably shadowed obstore-databaas; they share "
            "the same top-level module name. Install databaas-utils[obstore]."
        )

    location = resolved.location.rstrip("/")
    if prefix:
        location = f"{location}/{prefix.strip('/')}"

    options: Any = {**_client_options(resolved), **(client_options or {})}
    return RemoteSignedS3Store.from_s3_url(
        location,
        signing_callback(settings, resolved, session=session),
        endpoint=resolved.endpoint,
        client_options=options or None,
    )


class BlobStore(Protocol):
    """Opaque bytes under a named table.

    Implemented by :class:`GenericTableStore` (remote-signed storage) and
    :class:`LocalStore` (a directory), so code written against this runs on
    either.
    """

    def put(self, table: str, key: str, source: Path) -> str:
        """Store the local file ``source`` as ``key``; return its URI."""
        ...

    def get(self, table: str, key: str, dest: Path) -> Path:
        """Download ``key`` to ``dest`` and return ``dest``."""
        ...

    def uri(self, table: str, key: str) -> str:
        """The URI ``key`` has (or would have) under ``table``."""
        ...


@dataclass
class GenericTableStore(BlobStore):
    """Blob access under generic tables, signed rather than credentialed.

    Caches are instance-scoped on purpose. `settings` varies by namespace across
    call sites, so a module-level cache keyed only on table name would collide
    across namespaces and branch deploys.

    Needs the ``obstore`` extra. Tables are created on first write.

    Args:
        settings: Which warehouse and namespace, as which identity.
        client: A ``CatalogClient`` to reuse.

    Example:
        >>> store = GenericTableStore(settings)
        >>> store.put("grib", "2026/09/30/run.grib2", Path("run.grib2"))
        's3://.../2026/09/30/run.grib2'
        >>> for meta in store.list("grib", prefix="2026/09"):
        ...     print(meta["path"], meta["size"])
    """

    settings: LakehouseSettings
    client: CatalogClient | None = None
    _tables: dict[str, ResolvedTable] = field(default_factory=dict, repr=False)
    _stores: dict[tuple[str, str], Any] = field(default_factory=dict, repr=False)
    _lock: threading.Lock = field(
        default_factory=threading.Lock, repr=False, compare=False
    )

    def table(
        self, table: str, *, create: bool = True, doc: str = "Generic table"
    ) -> ResolvedTable:
        """The table's location and signing details. Cached per instance."""
        resolved = self._tables.get(table)
        if resolved is None:
            with self._lock:
                resolved = self._tables.get(table)
                if resolved is None:
                    resolved = resolve(
                        self.settings, table, create=create, doc=doc, client=self.client
                    )
                    self._tables[table] = resolved
        return resolved

    def object_store(
        self, table: str, *, prefix: str = "", create: bool = True
    ) -> RemoteSignedS3Store:
        """The raw obstore handle, for callers that need more than put/get.

        Args:
            table: Generic table name.
            prefix: Restrict the handle to keys under this prefix.
            create: Create the table if missing.
        """
        resolved = self.table(table, create=create)
        cache_key = (table, prefix)
        store = self._stores.get(cache_key)
        if store is None:
            with self._lock:
                store = self._stores.get(cache_key)
                if store is None:
                    store = signed_store(self.settings, resolved, prefix=prefix)
                    self._stores[cache_key] = store
        return store

    def uri(self, table: str, key: str) -> str:
        """The ``s3://`` URI of ``key`` under ``table``."""
        return f"{self.table(table).location.rstrip('/')}/{key}"

    def put(self, table: str, key: str, source: Path) -> str:
        """Upload a local file under the table; returns its s3:// URI.

        Args:
            table: Generic table name; created if missing.
            key: Object key within the table.
            source: Local file to upload.
        """
        import obstore

        obstore.put(self.object_store(table), key, source)
        uri = self.uri(table, key)
        log.info("uploaded %s to %s", Path(source).name, uri)
        return uri

    def get(self, table: str, key: str, dest: Path) -> Path:
        """Stream one object under the table to `dest`.

        Args:
            table: Generic table name; it must already exist.
            key: Object key within the table.
            dest: Local path to write; parent directories are created.

        Returns:
            ``dest``.
        """
        import obstore

        store = self.object_store(table, create=False)
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as handle:
            handle.writelines(bytes(chunk) for chunk in obstore.get(store, key).stream())
        return dest

    def open(self, table: str, key: str) -> Any:
        """A readable file object, without staging to disk first.

        Args:
            table: Generic table name; it must already exist.
            key: Object key within the table.
        """
        import obstore

        return obstore.open_reader(self.object_store(table, create=False), key)

    def list(self, table: str, *, prefix: str = "") -> Iterator[Any]:
        """Object metadata under the table.

        Lakekeeper records only a location for a generic table, so listing is
        the only way to learn what actually landed.

        Args:
            table: Generic table name; it must already exist.
            prefix: Only list keys under this prefix.

        Yields:
            obstore object-metadata dicts (``path``, ``size``, ``last_modified``, ...).
        """
        import obstore

        yield from obstore.list(self.object_store(table, create=False, prefix=prefix))

    def delete(self, table: str, key: str) -> None:
        """Delete one object under the table."""
        import obstore

        obstore.delete(self.object_store(table, create=False), key)


@dataclass
class LocalStore(BlobStore):
    """A filesystem stand-in for laptop runs and tests. Never a silent fallback.

    Files live at ``<root>/<table>/<key>``.

    Args:
        root: Directory that plays the role of the warehouse.
    """

    root: Path

    def _path(self, table: str, key: str) -> Path:
        return Path(self.root) / table / key

    def uri(self, table: str, key: str) -> str:
        """The filesystem path of ``key`` under ``table``."""
        return str(self._path(table, key))

    def put(self, table: str, key: str, source: Path) -> str:
        """Copy ``source`` to ``<root>/<table>/<key>``; return that path."""
        import shutil

        dest = self._path(table, key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        return str(dest)

    def get(self, table: str, key: str, dest: Path) -> Path:
        """Copy ``<root>/<table>/<key>`` to ``dest`` and return ``dest``."""
        import shutil

        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self._path(table, key), dest)
        return dest
