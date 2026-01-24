from abc import ABC
from logging import WARNING
from typing import Any, Dict, Optional

from galileo_core.helpers.logger import logger


class BaseGalileoException(Exception, ABC):
    """Base exception for all exceptions in galileo.

    Attributes:
        message: Human-readable error message
        error_code: Optional EMS catalog lookup key for standardized error handling
        LOG_LEVEL: Logging level for this exception type
    """

    LOG_LEVEL: int = WARNING

    def __init__(
        self,
        message: str,
        logging_extra: Optional[Dict[str, Any]] = None,
        *,
        error_code: Optional[int] = None,
    ) -> None:
        logger.log(self.LOG_LEVEL, message, extra=logging_extra)
        self.message: str = message
        self.error_code: Optional[int] = error_code
        super().__init__(self.message)
