"""Auto-generated stub for module: logging_config."""

# Functions
def configure_logging() -> None:
    """
    Configure the root logger from the LOG_LEVEL environment variable.
    
    Call once at application startup. If the root logger already has
    handlers, this is a no-op to avoid duplicate configuration.
    
    Environment
    -----------
    LOG_LEVEL : str, optional
        One of DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is WARNING
        so that debug/info output is silent in production.
    """
    ...
