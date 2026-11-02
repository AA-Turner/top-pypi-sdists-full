"""Matrx Files API layer — the package's own HTTP surface.

Router factories take a configured ``FileService`` and return an ``APIRouter``;
auth is caller-supplied via the ``user_id_dep`` parameter so every host (and
the standalone app) plugs in its own JWT/guest flow. Hosts mount these
factories; ``standalone/app.py`` mounts the SAME factories — a router that
only works in host mode violates INDEPENDENCE.md.

    from matrx_files import FileService
    from matrx_files.api import build_file_router, build_asset_router, build_share_router

    app.include_router(build_file_router(file_service))
"""

from .router_assets import build_asset_router
from .router_files import build_file_router
from .router_share import build_share_router
from .router_sync_mappings import build_sync_mappings_router
from .router_tus import build_tus_router

__all__ = [
    "build_asset_router",
    "build_file_router",
    "build_share_router",
    "build_sync_mappings_router",
    "build_tus_router",
]
