from typing import Callable, Union

from fastapi import Depends, HTTPException
from starlette import status

from ..token_throttler import TokenThrottler, TokenThrottlerException


class FastAPIThrottler:
    def __init__(self, throttler: TokenThrottler, exc: Union[Exception, None] = None):
        self._throttler: TokenThrottler = throttler
        self._exc: Union[Exception, None] = exc

    def enable(self, callback) -> Callable:
        def _dependency(identifier: str = Depends(callback)) -> None:
            if not self._throttler.consume(identifier=identifier):
                raise self._exc or HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=TokenThrottlerException().message,
                )

        return _dependency
