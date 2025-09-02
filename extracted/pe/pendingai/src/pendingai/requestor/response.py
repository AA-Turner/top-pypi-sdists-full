#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from requests import Response

from pendingai.exceptions import (
    ForbiddenError,
    PaymentGatewayError,
    RequestValidationError,
    UnauthorizedError,
    UnsubscribedError,
)
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class RequestorResponse(Response):
    """
    Requestor response class for post-request error handling and
    reporting; shared response methods that handle specific conditions.
    """

    def __init__(self, response: Response) -> None:
        super().__init__()
        self.__dict__.update(response.__dict__)
        self.log()

    def log(self, level: int = 20) -> None:
        """
        Log a response summary at a specified log level.
        """
        seconds: float = self.elapsed.total_seconds()
        logger.log(level, f"Response [{self.status_code}] in {seconds:.2} seconds")

    def raise_for_service_errors(self) -> None:
        """
        Capture shared service errors in a response status and raise
        corresponding runtime errors.
        """
        if self.status_code == 401:
            logger.debug(f"Unuauthorized status code error received: {self.json()}")
            raise UnauthorizedError

        elif self.status_code == 402:
            logger.debug(f"Payment gateway status code error received: {self.json()}")
            raise PaymentGatewayError

        elif self.status_code == 403:
            logger.debug(f"Forbidden status code error received: {self.json()}")
            if "not_subscribed" in self.content.decode():
                raise UnsubscribedError
            raise ForbiddenError

        elif self.status_code == 422:
            logger.debug(f"Validation error status code error received: {self.json()}")
            raise RequestValidationError(self.json().get("error", {}).get("details", []))
