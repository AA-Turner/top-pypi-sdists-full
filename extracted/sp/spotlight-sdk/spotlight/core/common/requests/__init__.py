"""
Base asynchronous and synchronous request functions inherited by all API request functions.
"""

from spotlight.core.common.requests.asynchronous import (
    __async_get_request,
    __async_put_request,
    __async_post_request,
    __async_delete_request,
)
from spotlight.core.common.requests.synchronous import (
    __get_request,
    __put_request,
    __post_request,
    __delete_request,
)
