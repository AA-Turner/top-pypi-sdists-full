from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.logging.enums import Level
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.exceptions import LoggerRuntimeError
from orionis.services.log.handlers.filename import FileNameLogger
from orionis.services.log.handlers.size_rotating import PrefixedSizeRotatingFileHandler
from orionis.services.log.handlers.timed_rotating import PrefixedTimedRotatingFileHandler

class LoggerService(ILoggerService):

    def __init__(
        self,
        config: Logging | dict = None,
        **kwargs
    ):
        """
        Initializes the LoggerService instance with the provided logging configuration.

        This constructor sets up the logger configuration using either a `Logging` object,
        a configuration dictionary, or keyword arguments. It validates the input and
        ensures that the configuration is properly instantiated before initializing
        the logger. If no configuration is provided, it attempts to create one using
        the supplied keyword arguments.

        Parameters
        ----------
        config : Logging or dict, optional
            The logging configuration. Can be an instance of the `Logging` class,
            a dictionary containing configuration parameters, or None. If None,
            configuration is initialized using `kwargs`.
        **kwargs
            Additional keyword arguments used to initialize the `Logging` configuration
            if `config` is None.

        Returns
        -------
        None
            This method does not return any value. It sets up the logger service instance.

        Raises
        ------
        LoggerRuntimeError
            If the logger configuration cannot be initialized from the provided arguments,
            such as invalid types or missing required parameters.
        """

        # Initialize private attributes for logger and configuration
        self.__logger = None
        self.__config = None

        # If no configuration is provided, attempt to create one using kwargs
        if config is None:
            try:
                self.__config = Logging(**kwargs)
            except Exception as e:
                # Raise a runtime error if configuration initialization fails
                raise LoggerRuntimeError(
                    f"Error initializing logger configuration: {e}. "
                    "Please check the provided parameters. "
                    f"Expected a Logging dataclass or a configuration dictionary. "
                    f"Type received: {type(config).__module__}.{type(config).__name__}. "
                    f"Expected: {Logging.__module__}.{Logging.__name__} or dict."
                )

        # If config is a dictionary, convert it to a Logging instance
        elif isinstance(config, dict):
            self.__config = Logging(**config)

        # If config is already a Logging instance, use it directly
        elif isinstance(config, Logging):
            self.__config = config

        # Initialize the logger using the validated configuration
        self.__initLogger()

    def __initLogger(self):
        """
        Initializes and configures the logger instance based on the provided settings.

        This method sets up the logger to write logs to a file, using different handlers
        depending on the logging channel type (e.g., stack, hourly, daily, weekly, monthly, chunked).
        It ensures the log format includes a timestamp, log level, and message. If the specified
        log directory does not exist, it is created automatically. The logger's level and retention
        policies are determined by the configuration.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It sets up the logger instance as an attribute.

        Raises
        ------
        LoggerRuntimeError
            If the logger cannot be initialized due to an error in configuration or handler setup.
        """
        import logging
        from datetime import datetime

        try:
            # List to hold the logging handlers
            handlers = []

            # Retrieve the default logging channel from configuration
            channel: str = self.__config.default

            # Get the configuration object for the selected channel
            config_channels = getattr(self.__config.channels, channel)

            # Generate the log file path using the FileNameLogger utility
            path: str = FileNameLogger(getattr(config_channels, 'path')).generate()

            # Determine the logging level (default to DEBUG if not specified)
            level: Level | int = getattr(config_channels, 'level', 10)
            level = level if isinstance(level, int) else level.value

            # Select and configure the appropriate handler based on the channel type
            if channel == "stack":
                # Simple file handler for stack channel
                handlers = [
                    logging.FileHandler(
                        filename=path,
                        encoding="utf-8"
                    )
                ]

            elif channel == "hourly":
                # Rotating file handler for hourly logs
                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename=path,
                        when="h",
                        interval=1,
                        backupCount=getattr(config_channels, 'retention_hours', 24),
                        encoding="utf-8",
                        utc=False
                    )
                ]

            elif channel == "daily":
                # Rotating file handler for daily logs
                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename=path,
                        when="d",
                        interval=1,
                        backupCount=getattr(config_channels, 'retention_days', 7),
                        encoding="utf-8",
                        atTime=datetime.strptime(getattr(config_channels, 'at', "00:00"), "%H:%M").time(),
                        utc=False
                    )
                ]

            elif channel == "weekly":
                # Rotating file handler for weekly logs
                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename=path,
                        when="w0",
                        interval=1,
                        backupCount=getattr(config_channels, 'retention_weeks', 4),
                        encoding="utf-8",
                        utc=False
                    )
                ]

            elif channel == "monthly":
                # Rotating file handler for monthly logs
                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename=path,
                        when="midnight",
                        interval=30,
                        backupCount=getattr(config_channels, 'retention_months', 4),
                        encoding="utf-8",
                        utc=False
                    )
                ]

            elif channel == "chunked":
                # Size-based rotating file handler for chunked logs
                handlers = [
                    PrefixedSizeRotatingFileHandler(
                        filename=path,
                        maxBytes=getattr(config_channels, 'mb_size', 10) * 1024 * 1024,
                        backupCount=getattr(config_channels, 'files', 5),
                        encoding="utf-8"
                    )
                ]

            # Configure the logger with the selected handlers and formatting
            logging.basicConfig(
                level=level,
                format="%(asctime)s [%(levelname)s] - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                encoding="utf-8",
                handlers=handlers
            )

            # Store the logger instance as a private attribute
            self.__logger = logging.getLogger(__name__)

        except Exception as e:
            # Raise a runtime error if logger initialization fails
            raise LoggerRuntimeError(f"Failed to initialize logger: {e}")

    def info(self, message: str) -> None:
        """
        Logs an informational message to the configured logger.

        This method records informational messages that highlight the progress or state
        of the application at a coarse-grained level. The message is stripped of leading
        and trailing whitespace before being logged.

        Parameters
        ----------
        message : str
            The informational message to log.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Log the informational message after stripping whitespace
        self.__logger.info(message.strip())

    def error(self, message: str) -> None:
        """
        Logs an error-level message to the configured logger.

        This method records error messages that indicate serious issues or failures
        within the application. The message is stripped of leading and trailing
        whitespace before being logged.

        Parameters
        ----------
        message : str
            The error message to log.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Log the error message after stripping whitespace
        self.__logger.error(message.strip())

    def warning(self, message: str) -> None:
        """
        Log a warning-level message to the configured logger.

        This method records warning messages that indicate potential issues or
        unexpected situations in the application. The message is stripped of
        leading and trailing whitespace before being logged.

        Parameters
        ----------
        message : str
            The warning message to log.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Log the warning message after stripping whitespace
        self.__logger.warning(message.strip())

    def debug(self, message: str) -> None:
        """
        Logs a debug-level message to the configured logger.

        This method records diagnostic messages that are useful for debugging
        and development purposes. The message is stripped of leading and trailing
        whitespace before being logged.

        Parameters
        ----------
        message : str
            The debug message to be logged.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Log the debug message after stripping whitespace
        self.__logger.debug(message.strip())