import logging
from collections.abc import Callable


class Pipeline:
    def __init__(self) -> None:
        self.steps: list[Callable] = []
        self.logger = logging.getLogger(__name__)

    def add_step(self, step: Callable[[], None]) -> None:
        self.steps.append(step)

    def run(self) -> None:
        for i, step in enumerate(self.steps, 1):
            self.logger.info(f"Running step {i}: {step.__name__}")
            try:
                step()
            except Exception as e:
                self.logger.error(f"Error in step {i} ({step.__name__}): {e!s}")
                raise
