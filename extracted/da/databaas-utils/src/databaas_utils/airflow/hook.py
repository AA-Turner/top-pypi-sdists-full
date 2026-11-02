"""The Airflow hook for the lakehouse connection.

Its real value is `test_connection`: one click at configuration time tells an
admin whether the client secret, token URL, project scope and warehouse name are
all correct together. Without it the first signal is a DAG failure hours later,
with an error that does not mention the connection.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.sdk import BaseHook

from databaas_utils.airflow.connection import (
    DEFAULT_CONN_ID,
    get_settings,
    resolve_connection,
    settings_from_connection,
)
from databaas_utils.airflow.provider import CONNECTION_TYPE
from databaas_utils.errors import LakehouseError

if TYPE_CHECKING:
    from databaas_utils.generic import BlobStore
    from databaas_utils.index import Index
    from databaas_utils.settings import LakehouseSettings


class LakehouseHook(BaseHook):
    """Access to a Lakekeeper warehouse, as one Zitadel service account.

    Args:
        conn_id: The Airflow connection to authenticate with.

    Example:
        >>> hook = LakehouseHook()
        >>> catalog = hook.get_catalog(namespace="open_meteo")
    """

    conn_name_attr = "conn_id"
    default_conn_name = DEFAULT_CONN_ID
    conn_type = CONNECTION_TYPE
    hook_name = "DataBaas Lakehouse"

    def __init__(self, conn_id: str = DEFAULT_CONN_ID, **kwargs: Any) -> None:
        """Bind the hook to ``conn_id``."""
        super().__init__(**kwargs)
        self.conn_id = conn_id

    @staticmethod
    def get_ui_field_behaviour() -> dict[str, Any]:
        """Field labels and hints for the connection form."""
        from databaas_utils.airflow.provider import get_provider_info

        return get_provider_info()["connection-types"][0]["ui-field-behaviour"]

    def get_settings(self, *, namespace: str | None = None) -> LakehouseSettings:
        """The connection's :class:`~databaas_utils.LakehouseSettings`."""
        return get_settings(self.conn_id, namespace=namespace)

    def get_catalog(self, *, namespace: str | None = None) -> Any:
        """A pyiceberg REST catalog for this connection."""
        from databaas_utils.catalog import rest_catalog

        return rest_catalog(self.get_settings(namespace=namespace))

    def get_store(self, *, namespace: str | None = None) -> BlobStore:
        """A remote-signed blob store for this connection."""
        from databaas_utils.generic import GenericTableStore

        return GenericTableStore(self.get_settings(namespace=namespace))

    def get_index(self, *, namespace: str | None = None, table: str = "files") -> Index:
        """The Iceberg file index for this connection."""
        from databaas_utils.index import FileIndex

        return FileIndex(self.get_settings(namespace=namespace), table=table)

    def test_connection(self) -> tuple[bool, str]:
        """Fetch a token and read the warehouse config.

        Exercises the whole chain an admin can get wrong — client secret, token
        URL, project scope, host, warehouse name — and reports which link
        failed rather than just that something did.
        """
        from databaas_utils.catalog import CatalogClient

        try:
            connection = resolve_connection(self.conn_id)
        except LakehouseError as exc:
            return False, str(exc)

        try:
            settings = settings_from_connection(connection)
        except LakehouseError as exc:
            return False, f"Connection fields are incomplete — {exc}"

        try:
            settings.auth_header()
        except Exception as exc:
            return False, (
                f"Authentication failed against the token endpoint: {exc}. Check "
                "the client id, client secret and token URL."
            )

        try:
            with CatalogClient(settings) as client:
                warehouse_id = client.warehouse_id()
        except Exception as exc:
            return False, (
                f"Authenticated, but reading warehouse {settings.warehouse!r} "
                f"failed: {exc}. Check the warehouse name, the Lakekeeper URL, "
                "and that this service account has been granted access to it."
            )

        return True, (
            f"Connected to {settings.base_url} — warehouse "
            f"{settings.warehouse!r} resolved to {warehouse_id}."
        )
