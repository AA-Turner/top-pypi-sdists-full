"""The Iceberg REST catalog, wired for Lakekeeper's remote signer.

The important part of this module is what ``rest_catalog`` does *not* set.

pyiceberg implements remote signing only in ``pyiceberg.io.fsspec``, selected by
``s3.signer``; ``PyArrowFileIO`` has no signer support at all and is tried first
for ``s3://`` (``SCHEMA_TO_FILE_IO``). So a catalog that does not pin
``py-io-impl`` silently resolves to PyArrow and reaches S3 with whatever ambient
credentials the process happens to carry — or fails. ``s3.remote-signing-enabled``
is a Java-Iceberg property name and does nothing here.

``py-io-impl`` points at ``catalog_io.SigningFileIO``, an ``FsspecFileIO`` that
gives each table its own S3 client; pyiceberg's own shares one client between
tables and threads and swaps the signer on it. Lakekeeper names the stock
``FsspecFileIO`` in every ``loadTable`` response, so ``py-catalog-impl`` selects
``catalog_io.LakekeeperCatalog`` to swap it back. See ``catalog_io``.

``s3.signer.uri`` and ``s3.signer.endpoint`` are deliberately left unset: the
``loadTable`` response supplies both and pyiceberg concatenates them. Setting a
hand-built URI that already ends in ``/v1/aws/s3/sign`` yields
``.../v1/aws/s3/sign/v1/aws/s3/sign``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import requests

from databaas_utils.errors import LakehouseError
from databaas_utils.settings import (
    LakehouseSettings,
    OAuthClientCredentials,
    StaticToken,
)

if TYPE_CHECKING:
    from pyiceberg.catalog import Catalog

REQUEST_TIMEOUT = 30
SIGNING_FILE_IO = "databaas_utils.catalog_io.SigningFileIO"
LAKEKEEPER_CATALOG = "databaas_utils.catalog_io.LakekeeperCatalog"
REST_SIGNER = "S3V4RestSigner"
_HTTP_CONFLICT = 409


class CatalogClient:
    """The slice of Lakekeeper's REST API that pyiceberg does not cover.

    Usable as a context manager, which closes its HTTP session.

    Args:
        settings: Which warehouse, as which identity.
        session: A ``requests.Session`` to use; one is created if omitted.
        timeout: Per-request timeout in seconds.

    Example:
        >>> with CatalogClient(settings) as client:
        ...     client.ensure_namespace("open_meteo")
    """

    def __init__(
        self,
        settings: LakehouseSettings,
        *,
        session: requests.Session | None = None,
        timeout: float = REQUEST_TIMEOUT,
    ) -> None:
        self._settings = settings
        self._session = session or requests.Session()
        self._timeout = timeout
        self._warehouse_id: str | None = None

    @property
    def settings(self) -> LakehouseSettings:
        """The settings this client was built with."""
        return self._settings

    def _headers(self) -> dict[str, str]:
        return {"Authorization": self._settings.auth_header()}

    def warehouse_id(self) -> str:
        """The warehouse UUID, from ``/v1/config``. Cached per client.

        Raises:
            LakehouseError: If Lakekeeper does not know the warehouse name.
            requests.HTTPError: On a non-2xx response, e.g. 401 or 403.
        """
        if self._warehouse_id is None:
            response = self._session.get(
                f"{self._settings.catalog_url}/v1/config",
                params={"warehouse": self._settings.warehouse},
                headers=self._headers(),
                timeout=self._timeout,
                verify=self._settings.verify,
            )
            response.raise_for_status()
            prefix = response.json().get("defaults", {}).get("prefix")
            if not prefix:
                raise LakehouseError(
                    f"Lakekeeper returned no defaults.prefix for warehouse "
                    f"{self._settings.warehouse!r} — is the name correct?"
                )
            self._warehouse_id = str(prefix)
        return self._warehouse_id

    def ensure_namespace(self, namespace: str | None = None) -> None:
        """Create the namespace if absent. A 409 means someone else won the race.

        Args:
            namespace: Dotted namespace; ``settings.namespace`` if omitted.
        """
        name = namespace or self._settings.namespace
        response = self._session.post(
            f"{self._settings.catalog_url}/v1/{self.warehouse_id()}/namespaces",
            json={"namespace": name.split("."), "properties": {}},
            headers=self._headers(),
            timeout=self._timeout,
            verify=self._settings.verify,
        )
        if response.status_code == _HTTP_CONFLICT:
            return
        response.raise_for_status()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> Self:
        """Return ``self``; the session closes on exit."""
        return self

    def __exit__(self, *exc: object) -> None:
        """Close the session."""
        self.close()


class TokenProviderAuthManager:
    """Adapts any ``TokenProvider`` to pyiceberg's ``AuthManager`` interface.

    pyiceberg calls ``auth_header()`` fresh on every request (and reuses the
    same manager for the S3 signer's requests via ``FileIO``'s ``auth.manager``
    property — see ``pyiceberg.io.fsspec``), so a provider that refreshes
    itself — ``UserLogin`` in particular, whose token is short-lived — stays
    current for the life of the catalog. The frozen-``token`` property below
    would otherwise bake in whatever bearer was current at catalog-build time.
    """

    def __init__(self, provider: Any = None, **_ignored: Any) -> None:
        """Wrap ``provider``; extra pyiceberg config keys are ignored."""
        # pyiceberg's AuthManagerFactory instantiates with **config, so the
        # provider travels through as a keyword rather than a positional arg.
        self._provider = provider

    def auth_header(self) -> str:
        """The provider's current ``Authorization`` header value."""
        return str(self._provider.auth_header())


def catalog_properties(settings: LakehouseSettings) -> dict[str, Any]:
    """The properties handed to ``load_catalog``. Separated out so it is testable.

    Args:
        settings: Which warehouse, as which identity.

    Returns:
        pyiceberg catalog properties with remote signing enabled and no S3 keys.
    """
    props: dict[str, Any] = {
        "uri": settings.catalog_url,
        "warehouse": settings.warehouse,
        # Without these two, remote signing is silently off. See module docstring.
        "py-io-impl": SIGNING_FILE_IO,
        "py-catalog-impl": LAKEKEEPER_CATALOG,
        "s3.signer": REST_SIGNER,
        "s3.region": settings.region,
    }
    if settings.endpoint:
        props["s3.endpoint"] = settings.endpoint

    creds = settings.credentials
    if isinstance(creds, OAuthClientCredentials):
        props["credential"] = f"{creds.client_id}:{creds.client_secret}"
        props["oauth2-server-uri"] = creds.token_url
        props["scope"] = creds.effective_scope
    elif isinstance(creds, StaticToken):
        props["token"] = creds.token
    else:
        # A custom TokenProvider that can refresh itself (UserLogin,
        # ServiceAccountKey, ...): wire it in as a live auth manager instead of
        # freezing its current bearer into "token".
        props["auth"] = {
            "type": "custom",
            "impl": f"{__name__}.TokenProviderAuthManager",
            "custom": {"provider": creds},
        }
    return props


def rest_catalog(settings: LakehouseSettings, **overrides: str) -> Catalog:
    """A pyiceberg REST catalog bound to `settings`, signing through Lakekeeper.

    No S3 credentials are ever placed in the properties; object storage is
    reached by asking Lakekeeper to sign each request. Needs the ``iceberg``
    extra.

    Args:
        settings: Which warehouse, as which identity.
        **overrides: pyiceberg catalog properties that replace the defaults.

    Returns:
        A pyiceberg ``Catalog``. Use fully qualified ``namespace.table``
        identifiers with it.

    Example:
        >>> catalog = rest_catalog(settings)
        >>> catalog.load_table("open_meteo.daily_summary").scan(limit=10).to_arrow()
    """
    from pyiceberg.catalog import load_catalog

    props = catalog_properties(settings)
    props.update(overrides)
    return load_catalog("databaas", **props)
