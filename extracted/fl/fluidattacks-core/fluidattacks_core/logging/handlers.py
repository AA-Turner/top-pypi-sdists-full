import logging
import sys
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import TextIO

from fluidattacks_core.logging.filters import NoProductionFilter, ProductionOnlyFilter
from fluidattacks_core.logging.formatters import ColorfulFormatter, CustomJsonFormatter


class DebuggingHandler(logging.StreamHandler[TextIO]):
    """Logging handler for console environments implemented with `QueueHandler`.

    Includes:
    - Filters: `NoProductionFilter`
    - Formatter: `ColorfulFormatter`
    """

    def __init__(self) -> None:
        super().__init__(sys.stdout)
        self.addFilter(NoProductionFilter())
        self.setFormatter(ColorfulFormatter())


class ProductionSyncHandler(logging.StreamHandler[TextIO]):
    """Logging handler for production environments implemented with `logging.StreamHandler`.

    Includes:
    - Filters: `ProductionOnlyFilter`
    - Formatter: `CustomJsonFormatter`
    """

    def __init__(self) -> None:
        super().__init__(sys.stdout)
        self.addFilter(ProductionOnlyFilter())
        self.setFormatter(CustomJsonFormatter())


class ProductionAsyncHandler(QueueHandler):
    """Logging handler for production environments implemented with `QueueHandler`.

    Includes:
    - Filters: `NoBatchFilter`, `ProductionOnlyFilter`
    - Formatter: `CustomJsonFormatter`
    """

    def __init__(self) -> None:
        handler = logging.StreamHandler(sys.stdout)
        handler.addFilter(ProductionOnlyFilter())
        handler.setFormatter(CustomJsonFormatter())

        self.queue = Queue()
        self.listener = QueueListener(self.queue, handler)

        self.listener.start()
        self.shutting_down = False
        super().__init__(self.queue)

    def emit(self, record: logging.LogRecord) -> None:
        if self.shutting_down:
            return
        super().emit(record)

    def close(self) -> None:
        self.shutting_down = True
        self.listener.stop()
        super().close()
