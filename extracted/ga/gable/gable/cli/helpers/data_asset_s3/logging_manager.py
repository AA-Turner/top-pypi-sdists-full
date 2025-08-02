"""
Logging configuration for the inventory report manager.
"""

import logging


class LoggingManager:
    """Manages application logging configuration"""

    @staticmethod
    def setup():
        """Configure the application logging"""
        logging.basicConfig(
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )
        return logging.getLogger(__name__)
