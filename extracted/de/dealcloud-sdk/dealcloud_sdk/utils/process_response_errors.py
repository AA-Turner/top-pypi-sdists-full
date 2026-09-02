"""
For Processing error responses from the API
"""

import logging

logger = logging.getLogger(__name__)


def process_errors(
    response: list[dict],
    throw_error: bool = False,
):
    errors = [x for x in response if "Errors" in x.keys()]

    for e in errors:
        logger.error(e)

    if throw_error:
        raise (Exception(errors))
