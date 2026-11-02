"""Update processing status endpoint - permanently removed.

The HTTP write route ``POST /api/v1/pipeline/processing-status`` no longer
exists: the pipeline writes processing status in-process, so there is no
authorized HTTP write surface. The functions below preserve their import
paths and signatures for compatibility but raise
:class:`DeprecatedEndpointError` on call. Read status via
``api.pipeline.get_processing_status``.
"""

from typing import Any, Dict, List, Optional

from ...client import Client
from ...errors import DeprecatedEndpointError
from ...types import Response

_ENDPOINT = "update_processing_status"
_REMOVED_MSG = (
    "The processing-status write endpoint was removed; the pipeline writes "
    "status in-process. Read status via get_processing_status."
)


def sync_detailed(
    *,
    client: Optional[Client] = None,
    json_body: Optional[List[Dict[str, Any]]] = None,
) -> Response[Dict[str, Any]]:
    raise DeprecatedEndpointError(_ENDPOINT, _REMOVED_MSG)


def sync(
    *,
    client: Optional[Client] = None,
    json_body: Optional[List[Dict[str, Any]]] = None,
) -> Optional[Dict[str, Any]]:
    raise DeprecatedEndpointError(_ENDPOINT, _REMOVED_MSG)


async def asyncio_detailed(
    *,
    client: Optional[Client] = None,
    json_body: Optional[List[Dict[str, Any]]] = None,
) -> Response[Dict[str, Any]]:
    raise DeprecatedEndpointError(_ENDPOINT, _REMOVED_MSG)


async def asyncio(
    *,
    client: Optional[Client] = None,
    json_body: Optional[List[Dict[str, Any]]] = None,
) -> Optional[Dict[str, Any]]:
    raise DeprecatedEndpointError(_ENDPOINT, _REMOVED_MSG)
