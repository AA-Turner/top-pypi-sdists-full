import asyncio
import logging
from rabbithole.asyncio_rabbit_manager import AsyncioRabbitManager, RabbitConfig
import traceback
from typing import Callable
from rabbithole.constants import Constants


class HoleWrapper:
    """
    RabbitHoleManager manages the connection and communication with a RabbitMQ server.
    It provides methods to connect, send messages, and handle incoming messages with optional asynchronous callbacks.

    Attributes:
    rabbit_config (RabbitConfig): Configuration settings for RabbitMQ.
    logger (Logger): Logger for recording messages and errors.
    rabbit_manager (AsyncioRabbitManager): The manager handling the RabbitMQ operations.
    on_event_callback (Callable): Asynchronous callback function for incoming messages.

    Example:
    # Initialize the manager with proper configuration and logger
    manager = RabbitHoleManager(rabbit_config, logger, use_callback=True)

    # Define an asynchronous callback function
    async def my_callback(channel, method, properties, body):
        print("Received message: ", body)

    # Set the callback function
    manager.set_on_event_callback(my_callback)

    # Connect to the RabbitMQ server
    await manager.connect()

    # Send a message
    manager.send_message('Hello, World!')

    # Close the connection
    await manager.close_connection()
    """

    def __init__(
        self,
        rabbit_config: RabbitConfig,
        logger: logging.Logger,
        use_callback: bool = False,
    ):
        """
        Initialize the RabbitHoleManager with a given RabbitMQ configuration and logger.

        :param rabbit_config: Configuration settings for RabbitMQ.
        :param logger: Logger for recording messages and errors.
        :param use_callback: Whether to use a callback for incoming messages.
        """

        self.rabbit_config = rabbit_config
        self.logger = logger
        self.rabbit_manager = AsyncioRabbitManager(
            rabbit_config,
            self.logger,
            on_message_callback=self.on_message_callback if use_callback else None,
        )

    async def connect(self):
        """
        Asynchronously connect to the RabbitMQ server.
        """
        await self.rabbit_manager.connect()

    async def close_connection(self):
        """
        Asynchronously close the connection to the RabbitMQ server.
        """
        await self.rabbit_manager.close_connection()

    def send_message(self, message):
        """
        Send a message to the RabbitMQ server.

        :param message: The message to be sent.
        """
        self.rabbit_manager.send_message(message)

    async def on_message_callback(self, channel, method, properties, body):
        """
        Asynchronous callback for processing messages from RabbitMQ.

        :param channel: The channel object.
        :param method: The method frame.
        :param properties: The properties frame.
        :param body: The message body.
        """
        if asyncio.iscoroutinefunction(self.on_event_callback):
            try:
                await self.on_event_callback(channel, method, properties, body)
            except Exception as e:
                self.logger.error(Constants.ERROR_EXECUTION_CALLBACK.format(e))
                # Nuovo: log dell'intera traccia dello stack per avere più contesto sull'errore.
                # Questo può aiutare significativamente nel debugging.
                traceback_details = traceback.format_exc()
                self.logger.error(Constants.ERROR_STACK_TRACE.format(traceback_details))

                # Nuovo: considera di aggiungere meccanismi di notifica per errori critici
                # esempio: invio di una notifica email, invio a un sistema di monitoraggio, ecc.
                # self.notify_critical_error(e, traceback_details)

        else:
            self.logger.error(Constants.ERROR_CALLBACK_NOT_ASYNC)

    def set_on_event_callback(self, callback: Callable):
        """
        Set the callback function for handling events, verifying that it's an asynchronous function.

        :param callback: The callback function to be set.
        """
        if asyncio.iscoroutinefunction(callback):
            self.on_event_callback = callback
        else:
            self.logger.error(Constants.ERROR_CALLBACK_NOT_ASYNC_PROVIDED)
