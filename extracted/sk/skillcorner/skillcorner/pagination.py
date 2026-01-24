import inspect
import logging
from collections.abc import Callable
from typing import Any

import makefun
from progress.bar import Bar

from skillcorner.errors import InfinitePaginationError

logger = logging.getLogger(__name__)


def _is_response_paginated(response: Any) -> bool:
    return not isinstance(response, dict) or 'next' not in response


def _paginate_and_return(fit_request: Callable, response: dict, *args, **kwargs) -> dict:
    results = response['results']
    bar = None
    url_stack = []

    if response.get('count'):
        bar = Bar('Loading all pages', max=response['count'] / len(results))

    while not _is_response_paginated(response) and response.get('next'):
        if response['next'] in url_stack:
            url_stack.append(response['next'])
            raise InfinitePaginationError(url_stack=url_stack)

        url_stack.append(response['next'])

        response = fit_request(*args, url=response['next'], **kwargs)
        results.extend(response['results'])

        if bar:
            bar.next()
    if bar:
        bar.finish()
    return results


async def _async_paginate_and_return(fit_request: Callable, response: dict, *args, **kwargs) -> dict:
    results = response['results']
    bar = None
    url_stack = []

    if response.get('count'):
        bar = Bar('Loading all pages', max=response['count'] / len(results))

    while not _is_response_paginated(response) and response.get('next'):
        if response['next'] in url_stack:
            url_stack.append(response['next'])
            raise InfinitePaginationError(url_stack=url_stack)

        url_stack.append(response['next'])

        response = await fit_request(*args, url=response['next'], **kwargs)
        results.extend(response['results'])

        if bar:
            bar.next()
    if bar:
        bar.finish()
    return results


def paginated(fit_request: Callable) -> Callable:
    @makefun.wraps(fit_request)
    def wrapper(*args, **kwargs) -> Any:
        response = fit_request(*args, **kwargs)

        if _is_response_paginated(response):
            return response
        return _paginate_and_return(fit_request, response, *args, **kwargs)

    @makefun.wraps(fit_request)
    async def async_wrapper(*args, **kwargs) -> Any:
        response = await fit_request(*args, **kwargs)

        if _is_response_paginated(response):
            return response
        return await _async_paginate_and_return(fit_request, response, *args, **kwargs)

    return async_wrapper if inspect.iscoroutinefunction(fit_request) else wrapper
