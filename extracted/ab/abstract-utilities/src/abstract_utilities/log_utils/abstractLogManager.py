from .imports import *      
class AbstractLogManager(metaclass=SingletonMeta):
    def __init__(self):
        # Create a logger; use __name__ to have a module-specific logger if desired.
        self.logger = logging.getLogger("AbstractLogManager")
        self.logger.setLevel(logging.DEBUG)  # Set to lowest level to let handlers filter as needed.

        # Create a console handler with a default level.
        self.console_handler = logging.StreamHandler()
        # Default level: show warnings and above.
        self.console_handler.setLevel(logging.WARNING)

        # Formatter for the logs.
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.console_handler.setFormatter(formatter)

        # If there are no handlers already attached, add our console handler.
        if not self.logger.hasHandlers():
            self.logger.addHandler(self.console_handler)

    def set_debug(self, enabled: bool) -> None:
        """
        Enable or disable DEBUG level messages.
        When enabled, the console handler will output DEBUG messages and above.
        When disabled, it falls back to INFO or WARNING (adjust as needed).
        """
        if enabled:
            self.console_handler.setLevel(logging.DEBUG)
            self.logger.debug("DEBUG logging enabled.")
        else:
            # For example, disable DEBUG by raising the level to INFO.
            self.console_handler.setLevel(logging.INFO)
            self.logger.info("DEBUG logging disabled; INFO level active.")

    def set_info(self, enabled: bool) -> None:
        """
        Enable or disable INFO level messages.
        When enabled, INFO and above are shown; when disabled, only WARNING and above.
        """
        if enabled:
            # Lower the handler level to INFO if currently higher.
            self.console_handler.setLevel(logging.INFO)
            self.logger.info("INFO logging enabled.")
        else:
            self.console_handler.setLevel(logging.WARNING)
            self.logger.warning("INFO logging disabled; only WARNING and above will be shown.")

    def set_warning(self, enabled: bool) -> None:
        """
        Enable or disable WARNING level messages.
        When disabled, only ERROR and CRITICAL messages are shown.
        """
        if enabled:
            # WARNING messages enabled means handler level is WARNING.
            self.console_handler.setLevel(logging.WARNING)
            self.logger.warning("WARNING logging enabled.")
        else:
            self.console_handler.setLevel(logging.ERROR)
            self.logger.error("WARNING logging disabled; only ERROR and CRITICAL messages will be shown.")

    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self.logger

