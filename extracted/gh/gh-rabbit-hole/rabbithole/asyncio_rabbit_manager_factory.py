from colorlog import ColoredFormatter
import logging
from rabbithole.asyncio_rabbit_manager import AsyncioRabbitManager, RabbitConfig
from rabbithole.config.config_file_manager import ConfigFileManager


class AsyncioRabbitManagerFactory:
    """
    Factory for creating instances of AsyncioRabbitManager with various configurations.

    This factory encapsulates the creation logic of AsyncioRabbitManager, allowing for easy customization and extension.

    Example:
        # Create a factory instance
        factory = AsyncioRabbitManagerFactory()

        # Use the factory to create an AsyncioRabbitManager instance
        rabbit_manager = factory.create(rabbit_config, logger, callback)
    """

    def create(
        self,
        config_file_name,
        config_directory: str = "app_config",
        sending_queue: str = "",
        listening_queue: str = "",
        sending_exchange: str = "",
        log_level: str = "INFO",
        on_message_callback=None,
    ):
        """
        Creates and returns an instance of AsyncioRabbitManager.

        :param rabbit_config: The configuration settings for RabbitMQ.
        :param logger: The logger instance to be used by the manager.
        :param on_message_callback: Optional callback for incoming messages.
        :return: An instance of AsyncioRabbitManager.
        """

        logger = self.__init_logger()
        config = self.__init_config(
            config_file_name=config_file_name,
            config_directory=config_directory,
            sending_queue=sending_queue,
            listening_queue=listening_queue,
            sending_exchange=sending_exchange,
        )
        # Potentially add more complex initialization logic here
        return AsyncioRabbitManager(config, logger, log_level, on_message_callback)

    def __init_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        log_colors = {
            "DEBUG": "green",
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        }
        formatter = ColoredFormatter(
            "%(log_color)s%(levelname)s%(reset)s - %(asctime)s - %(name)s - %(funcName)s - line %(lineno)d - %(message)s",
            log_colors=log_colors,
            secondary_log_colors={},
            style="%",
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def __init_config(
        self,
        config_file_name: str,
        config_directory: str = "app_config",
        sending_queue: str = "",
        listening_queue: str = "",
        sending_exchange: str = "",
    ):
        config = {
            "amqp_url": "amqp://guest:guest@localhost:5672/%2F",
            "sending_exchange": sending_exchange,
            "sending_queue": sending_queue,
            "listening_queue": listening_queue,
            "reconnect_delay": 5,
            "max_reconnect_attempts": 3,
            "log_level": "INFO",
        }
        return RabbitConfig(
            config_file_manager=ConfigFileManager(config_directory, config_file_name),
            default_config=config,
        )
