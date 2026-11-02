from .imports import (
    logging,
    SingletonMeta,
    LevelFilter,
)

class AbstractLogManager(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger("AbstractLogManager")
        self.logger.setLevel(logging.DEBUG)  # Logger accepts everything
        
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)  # Handler accepts everything
        
        # Filter does the actual control
        self.level_filter = LevelFilter()
        self.console_handler.addFilter(self.level_filter)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.console_handler.setFormatter(formatter)
        
        if not self.logger.hasHandlers():
            self.logger.addHandler(self.console_handler)
    
    def set_debug(self, enabled: bool) -> None:
        """Enable or disable DEBUG level messages."""
        if enabled:
            self.level_filter.enable_level(logging.DEBUG)
            self.logger.debug("DEBUG logging enabled.")
        else:
            self.level_filter.disable_level(logging.DEBUG)
            self.logger.info("DEBUG logging disabled.")
    
    def set_info(self, enabled: bool) -> None:
        """Enable or disable INFO level messages."""
        if enabled:
            self.level_filter.enable_level(logging.INFO)
            self.logger.info("INFO logging enabled.")
        else:
            self.level_filter.disable_level(logging.INFO)
            self.logger.warning("INFO logging disabled.")
    
    def set_warning(self, enabled: bool) -> None:
        """Enable or disable WARNING level messages."""
        if enabled:
            self.level_filter.enable_level(logging.WARNING)
            self.logger.warning("WARNING logging enabled.")
        else:
            self.level_filter.disable_level(logging.WARNING)
            self.logger.error("WARNING logging disabled.")
    
    def set_error(self, enabled: bool) -> None:
        """Enable or disable ERROR level messages."""
        if enabled:
            self.level_filter.enable_level(logging.ERROR)
        else:
            self.level_filter.disable_level(logging.ERROR)
    
    def is_level_enabled(self, level: int) -> bool:
        """Check if a level is currently enabled."""
        return self.level_filter.is_enabled(level)
    
    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self.logger
