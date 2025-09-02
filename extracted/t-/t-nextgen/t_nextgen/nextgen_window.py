"""NextGenWindow module."""

from logging import Logger
from t_nextgen.ng_app_manager import NGAppManager


class NextGenWindow:
    """NextGenWindow class."""

    def __init__(self, app_path: str, logger: Logger) -> None:
        """Initialize NextGenWindow."""
        self.desktop_app = NGAppManager(app_path, logger)
        self.logger = logger
