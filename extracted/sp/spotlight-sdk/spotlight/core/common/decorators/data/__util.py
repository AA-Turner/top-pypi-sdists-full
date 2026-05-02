import logging
from functools import reduce
from typing import Any, Callable, List

from requests import Response

from spotlight.core.common.errors import ApiError

logger = logging.getLogger(__name__)


def __process_response(
    response: Response,
    processor: Callable[[Response], Any],
    transformers: List[Callable[[Any], Any]],
):
    if response.status_code != 200 | response.status_code != 201:
        error = ApiError(
            f"Request to {response.url} failed with status code {response.status_code}: {response.text}"
        )
        logger.error(error)
        raise error

    data = processor(response)
    return reduce(lambda res, fxn: fxn(res), transformers, data)
