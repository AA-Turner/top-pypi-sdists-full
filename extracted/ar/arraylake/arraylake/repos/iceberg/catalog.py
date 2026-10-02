"""Open an Arraylake org's iceberg catalog as a pyiceberg catalog.

The Arraylake Iceberg REST catalog is served at ``{service_uri}/iceberg``. A
warehouse is an *org*, addressed as ``warehouse=<org>``: every org has exactly
one implicit catalog, holding that org's (flat, single-level) iceberg
namespaces, so tables are addressed as ``"<namespace>.<table>"``.

The caller's ordinary Arraylake bearer token (an ``ema_...`` api-client token
or the logged-in user's OAuth token) is the catalog credential; the catalog
vends storage credentials per table, so no other configuration is needed.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyiceberg.catalog.rest import RestCatalog


def get_iceberg_catalog(*, name: str, service_uri: str, warehouse: str, token: str | None) -> "RestCatalog":
    """Construct a pyiceberg RestCatalog for an Arraylake iceberg warehouse.

    Args:
        name: Catalog name (conventionally the org name).
        service_uri: The Arraylake API base URI.
        warehouse: The warehouse, which is the org name.
        token: An explicit bearer token, or None to use the cached user login.

    Returns:
        A ready-to-use ``pyiceberg.catalog.rest.RestCatalog``.
    """
    try:
        from pyiceberg.catalog.rest import RestCatalog
    except ImportError as exc:
        raise ImportError("pyiceberg is required to open an iceberg catalog. Install it with: pip install 'arraylake[iceberg]'") from exc

    # Custom auth is PyIceberg's supported extension point. Machine tokens stay
    # static; user logins are reloaded and refreshed before each request as needed.
    properties: dict[str, Any] = {"header.X-Iceberg-Access-Delegation": "vended-credentials"}
    if token is not None:
        properties["token"] = token
    else:
        properties["auth"] = {
            "type": "custom",
            "impl": "arraylake.repos.iceberg.auth.ArraylakeAuthManager",
            "custom": {"service_uri": service_uri},
        }
    return RestCatalog(
        name=name,
        uri=f"{service_uri.rstrip('/')}/iceberg",
        warehouse=warehouse,
        **properties,
    )
