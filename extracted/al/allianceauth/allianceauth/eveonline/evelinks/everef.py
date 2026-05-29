# this module generates profile URLs for everef

from urllib.parse import urljoin

from . import _ESI_CATEGORY_INVENTORYTYPE

_BASE_URL = 'https://everef.net/'


def _build_url(category: str, eve_id: int) -> str:
    """return url to profile page for an eve entity"""

    if category == _ESI_CATEGORY_INVENTORYTYPE:
        partial = 'types'

    else:
        raise NotImplementedError(
            "Not implemented yet for category:" + category
        )

    url = urljoin(
        _BASE_URL,
        f'{partial}/{int(eve_id)}'
    )
    return url


def type_url(eve_id: int) -> str:
    """url for page about given inventory type on everef"""
    return _build_url(_ESI_CATEGORY_INVENTORYTYPE, eve_id)
