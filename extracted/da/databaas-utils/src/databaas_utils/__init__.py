"""Lakekeeper/Iceberg lakehouse access for Databaas.

Read Iceberg tables, store files and zarr arrays in the Databaas lakehouse,
from a notebook, a laptop, or an Airflow DAG. Object storage is reached by
asking Lakekeeper to sign each request, so no S3 keys are ever involved.

Where to start:

- **As yourself (JupyterHub notebook, laptop, script):** ``databaas_utils.user``
  — ``get_catalog()``, ``get_store()``, ``get_zarr_group()``. It signs in as you.
- **Airflow DAG:** ``databaas_utils.airflow`` — the same helpers, authenticated
  through an Airflow connection, plus ``scoped()`` and ``target_for()`` for dev
  deployments.
- **Anywhere else:** build a :class:`LakehouseSettings` (``from_env()``,
  ``from_profile()``) and pass it to :func:`rest_catalog`,
  :class:`GenericTableStore`, :class:`FileIndex` or :func:`open_zarr_group`.

Install only what you need; the core is small and the rest are extras::

    pip install "databaas-utils[local]"    # laptop: iceberg, obstore, zarr, login
    pip install "databaas-utils[airflow]"  # inside a DAG environment

Example:
    >>> from databaas_utils.user import get_catalog
    >>> catalog = get_catalog()
    >>> catalog.load_table("open_meteo.daily_summary").scan(limit=10).to_arrow()

The names below are the package's semver contract. Anything not listed here —
and anything underscore-prefixed — may change in a patch release.

Re-exports are lazy (PEP 562) so that importing this package does not drag
pyiceberg, pyarrow and obstore into a process that only wanted `scoped()`. That
matters at Airflow dag-processor parse time, which imports every DAG file in
every bundle.
"""

from __future__ import annotations

from importlib import import_module
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _installed_version
from typing import TYPE_CHECKING, Any

try:
    # Single source of truth: pyproject.toml's version, via installed package
    # metadata. A hand-maintained literal here drifted from it once already —
    # 0.2.0 shipped to PyPI reporting __version__ == "0.1.0" — and a second
    # copy to keep in sync is how that kind of thing recurs.
    __version__ = _installed_version("databaas-utils")
except PackageNotFoundError:  # editable/dev checkout with no installed metadata
    __version__ = "0.0.0+unknown"

_LAZY: dict[str, str] = {
    # settings
    "LakehouseSettings": "databaas_utils.settings",
    "OAuthClientCredentials": "databaas_utils.settings",
    "ServiceAccountKey": "databaas_utils.settings",
    "StaticToken": "databaas_utils.settings",
    "TokenProvider": "databaas_utils.settings",
    # local user login
    "Profile": "databaas_utils.profiles",
    "load_profile": "databaas_utils.profiles",
    "UserLogin": "databaas_utils.userauth",
    "JupyterHubToken": "databaas_utils.jupyterhub",
    "login": "databaas_utils.userauth",
    # catalog
    "CatalogClient": "databaas_utils.catalog",
    "rest_catalog": "databaas_utils.catalog",
    "catalog_properties": "databaas_utils.catalog",
    # generic / blob
    "BlobStore": "databaas_utils.generic",
    "GenericTableStore": "databaas_utils.generic",
    "LocalStore": "databaas_utils.generic",
    "ResolvedTable": "databaas_utils.generic",
    "resolve": "databaas_utils.generic",
    "signed_store": "databaas_utils.generic",
    "remote_signing_available": "databaas_utils.generic",
    # index
    "FileRecord": "databaas_utils.index",
    "FileIndex": "databaas_utils.index",
    "NullIndex": "databaas_utils.index",
    "Index": "databaas_utils.index",
    # zarr
    "open_zarr_group": "databaas_utils.zarr",
    "local_zarr_group": "databaas_utils.zarr",
    # scoping
    "scoped": "databaas_utils.scoping",
    "slug": "databaas_utils.scoping",
    "set_default_slug": "databaas_utils.scoping",
    # errors
    "LakehouseError": "databaas_utils.errors",
    "ConfigurationError": "databaas_utils.errors",
    "ConnectionNotConfigured": "databaas_utils.errors",
    "AuthenticationError": "databaas_utils.errors",
    "RemoteSigningUnavailable": "databaas_utils.errors",
    "SignError": "databaas_utils.errors",
}

# Spelled out rather than derived from _LAZY: a computed __all__ is invisible
# to static analysers. test_public_api keeps the two in step.
__all__ = [
    "AuthenticationError",
    "BlobStore",
    "CatalogClient",
    "ConfigurationError",
    "ConnectionNotConfigured",
    "FileIndex",
    "FileRecord",
    "GenericTableStore",
    "Index",
    "JupyterHubToken",
    "LakehouseError",
    "LakehouseSettings",
    "LocalStore",
    "NullIndex",
    "OAuthClientCredentials",
    "Profile",
    "RemoteSigningUnavailable",
    "ResolvedTable",
    "ServiceAccountKey",
    "SignError",
    "StaticToken",
    "TokenProvider",
    "UserLogin",
    "__version__",
    "catalog_properties",
    "load_profile",
    "local_zarr_group",
    "login",
    "open_zarr_group",
    "remote_signing_available",
    "resolve",
    "rest_catalog",
    "scoped",
    "set_default_slug",
    "signed_store",
    "slug",
]


def __getattr__(name: str) -> Any:
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module), name)


def __dir__() -> list[str]:
    return list(__all__)


if TYPE_CHECKING:  # give type checkers and IDEs the real symbols
    from databaas_utils.catalog import CatalogClient, catalog_properties, rest_catalog
    from databaas_utils.errors import (
        AuthenticationError,
        ConfigurationError,
        ConnectionNotConfigured,
        LakehouseError,
        RemoteSigningUnavailable,
        SignError,
    )
    from databaas_utils.generic import (
        BlobStore,
        GenericTableStore,
        LocalStore,
        ResolvedTable,
        remote_signing_available,
        resolve,
        signed_store,
    )
    from databaas_utils.index import FileIndex, FileRecord, Index, NullIndex
    from databaas_utils.jupyterhub import JupyterHubToken
    from databaas_utils.profiles import Profile, load_profile
    from databaas_utils.scoping import scoped, set_default_slug, slug
    from databaas_utils.settings import (
        LakehouseSettings,
        OAuthClientCredentials,
        ServiceAccountKey,
        StaticToken,
        TokenProvider,
    )
    from databaas_utils.userauth import UserLogin, login
    from databaas_utils.zarr import local_zarr_group, open_zarr_group
