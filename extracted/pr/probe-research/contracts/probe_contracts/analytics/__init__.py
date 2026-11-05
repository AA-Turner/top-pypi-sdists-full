"""The product-analytics catalogs (events.json, surfaces.json) and their checked loaders."""

from .analytics import (
    CATALOG_PATH,
    SURFACE_CATALOG_PATH,
    CatalogError,
    CatalogEvent,
    CatalogGroup,
    CatalogSurface,
    EventCatalog,
    Runtime,
    SurfaceCatalog,
)

__all__ = [
    "CATALOG_PATH",
    "SURFACE_CATALOG_PATH",
    "CatalogError",
    "CatalogEvent",
    "CatalogGroup",
    "CatalogSurface",
    "EventCatalog",
    "Runtime",
    "SurfaceCatalog",
]
