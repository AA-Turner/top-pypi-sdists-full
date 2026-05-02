import asyncio
from uu import Error
import pika
import json
import logging
from pika.adapters.asyncio_connection import AsyncioConnection
from rabbithole.constants import Constants
from rabbithole.config import RabbitConfig


class AsyncioRabbitManager:
    """
    The AsyncioRabbitManager class provides an asynchronous interface to connect and interact with RabbitMQ
    using Python and asyncio. Designed for applications that require responsive, non-blocking processing,
    this class handles connecting to RabbitMQ, sending and receiving messages, and declaring exchanges and queues, all asynchronously.

    Key Features:
    - Asynchronous Connection: Establishes non-blocking connections to RabbitMQ, allowing the rest of the application
      to continue execution while it handles network operations in the background.
    - Channel Management: Opens and configures RabbitMQ channels to send and receive messages.
    - Sending and Receiving Messages: Supports sending messages to queues or exchanges and configuring asynchronous callbacks
      for handling incoming messages.
    - Integration with Asyncio: Built around asyncio primitives, it facilitates integration with other
      asynchronous operations and the event loop.
    - Advanced Logging: Uses a customizable logging system to monitor activities and quickly diagnose
      any problems.

    Usage:
    Ideal for asyncio-based applications that require efficient, asynchronous communication with RabbitMQ.
    It is especially useful in contexts where performance and responsiveness are critical, such as in microservices,
    in bots or real-time data processing systems.

    Properties:
    - amqp_url (str): URL for connecting to RabbitMQ.
    - sending_queue (str): Name of the queue for sending messages.
    - listening_queue (str): Name of the queue for receiving messages.
    - sending_exchange (str): Name of the exchange used to send messages.
    - reconnect_delay (int): Time to wait before attempting to reconnect.
    - max_reconnect_attempts (int): Maximum number of reconnect attempts.

    Public Methods:
    - connect(): Establishes an asynchronous connection with RabbitMQ and prepares the channel and exchange.
    - attempt_reconnect(): Attempts to reconnect to RabbitMQ if the connection is lost.
    - send_message(message, routing_key="", to_exchange=False): Sends a message to RabbitMQ.
    - close_connection(): Closes the connection to RabbitMQ asynchronously.
    - close_resources(): Gently closes the channel and connection.

    Callbacks:
    - on_message_callback: Asynchronous callback invoked on receipt of a message.

    Args:
        rabbit_config (RabbitConfig): Configuration object for RabbitMQ.
        logger (logging.Logger): Logger for logging activities and errors.
        log_level (str, optional): Log level. Defaults to "INFO".
        on_message_callback (Callable, optional): Asynchronous callback invoked when a message is received.
    """

    __doc__ = "The AsyncioRabbitManager class provides an asynchronous interface to connect and interact with RabbitMQ using Python and asyncio."
    __author__ = "Massimo Ghiani <m.ghiani@gmail.com>"
    __status__ = "production"
    # The following module attributes are no longer updated.
    __version__ = "1.6.0"
    __date__ = "01 January 2024"
    __maintainer__ = "Massimo Ghiani <m.ghiani@gmail.com>"

    def __init__(
        self,
        rabbit_config: RabbitConfig,
        logger: logging.Logger,
        log_level: str = "INFO",
        on_message_callback=None,
    ):
        self.__init_configuration(rabbit_config.config)
        self.__init_logger(logger, log_level)
        self.on_message_callback = on_message_callback
        self.__connection: AsyncioConnection = None
        self.__reconnect_attempts: int = 0
        self.__is_connected: bool = False
        self.__should_reconnect: bool = True
        self.__channel: pika.channel.Channel = None
        self.__connection_opened_event = asyncio.Event()
        self.__channel_opened_event = asyncio.Event()
        self.__sending_queue_declared_event = asyncio.Event()
        self.__listening_queue_declared_event = asyncio.Event()
        self.__exchange_declared_event = asyncio.Event()

    def __init_logger(self, logger: logging.Logger, log_level: str):
        self.__logger = logger or logging.getLogger(__name__)
        self.__logger.setLevel(getattr(logging, log_level, logging.INFO))

    def __init_configuration(self, config: dict):
        self.amqp_url: str = config.get("amqp_url")
        self.sending_queue: str = config.get("sending_queue")
        self.listening_queue: str = config.get("listening_queue")
        self.sending_exchange: str = config.get("sending_exchange")
        self.exchange_type: str = config.get("exchange_type", "direct")
        self.reconnect_delay: int = int(config.get("reconnect_delay", 5))
        self.max_reconnect_attempts: int = int(config.get("max_reconnect_attempts", 3))
        self.log_on_receiving: bool = config.get("log_on_receiving", False)
        self.log_on_sending: bool = config.get("log_on_sending", False)

    def __del__(self):
        """
        Distruttore della classe. Chiama la pulizia delle risorse.
        """
        asyncio.run(self.close_resources())

    async def connect(self):
        """
        Establishes an asynchronous connection with RabbitMQ and prepares the channel and exchange.
        """
        try:
            self.__should_reconnect = True
            connection_parameters = pika.URLParameters(self.amqp_url)
            self.__connection: AsyncioConnection = AsyncioConnection(
                parameters=connection_parameters,
                on_open_callback=self.__on_connection_open,
                on_open_error_callback=self.__on_connection_open_error,
                on_close_callback=self.__on_connection_closed,
            )
            await self.__connection_opened_event.wait()
            await self.__channel_opened_event.wait()
            await self.__sending_queue_declared_event.wait()
            await self.__listening_queue_declared_event.wait()
            await self.__exchange_declared_event.wait()
            # self.__connection_opened_event.clear()
        except pika.exceptions.AMQPConnectionError as e:
            self.__logger.error(
                f"{Constants.CONNECTION_FAILED} AMQPConnectionError: {e}"
            )
        except asyncio.TimeoutError as e:
            self.__logger.error(f"{Constants.CONNECTION_FAILED} TimeoutError: {e}")
        except Exception as e:
            self.__logger.error(Constants.CONNECTION_FAILED.format(e))

    async def attempt_reconnect(self):
        while (
            not self.__is_connected
            and self.__reconnect_attempts < self.max_reconnect_attempts
            and self.__should_reconnect
        ):
            self.__reconnect_attempts += 1
            self.__logger.info(
                Constants.ATTEMPT_RECONNECT.format(
                    self.__reconnect_attempts,
                    self.max_reconnect_attempts,
                    self.reconnect_delay,
                )
            )
            await asyncio.sleep(self.reconnect_delay)
            await self.connect()

        if not self.__is_connected and self.__should_reconnect:
            self.__logger.error(
                Constants.MAX_RECONNECT_ATTEMPTS_REACHED.format(
                    self.max_reconnect_attempts
                )
            )

    def __on_connection_open(self, connection):
        """
        Callback invoked when the connection to RabbitMQ is opened.

        Args:
            connection: Connection to RabbitMQ.
        """
        self.__logger.info(Constants.CONNECTION_OPENED)
        self.__logger.debug(
            f"on_connection_open: {Constants.CONNECTION_OPENED_DEBUG.format(connection)}"
        )
        self.__connection.channel(on_open_callback=self.__on_channel_open)
        self.__connection_opened_event.set()
        self.__is_connected = True
        self.__reconnect_attempts = 0

    def __on_connection_closed(self, connection, reason):
        """
        Callback invoked when the connection to RabbitMQ is closed.

        Args:
            connection: Connection to RabbitMQ.
            reason: Reason for closing the connection.
        """
        self.__logger.info(Constants.CONNECTION_CLOSED.format(reason))
        self.__logger.debug(
            f"on_connection_closed: {Constants.CONNECTION_CLOSED_DEBUG.format(connection)}"
        )

        self.__is_connected = False
        if self.__should_reconnect:
            asyncio.create_task(self.attempt_reconnect())
        # asyncio.create_task(self.close_resources())

    def __on_connection_open_error(self, connection, error):
        """
        Callback invoked in case of an error during connection opening.

        Args:
            connection: Connection to RabbitMQ.
            error: Error object describing the encountered issue.
        """
        self.__logger.error(Constants.CONNECTION_OPEN_ERROR.format(error))
        self.__logger.debug(
            f"on_connection_open_error: {Constants.CONNECTION_OPEN_ERROR_DEBUG.format(connection, error)}"
        )
        self.__is_connected = False
        self.__connection_opened_event.set()
        self.__should_reconnect = False
        asyncio.create_task(self.attempt_reconnect())

    def __on_channel_open(self, channel):
        """
        Callback invoked when a RabbitMQ channel is opened.

        Args:
            channel: Opened RabbitMQ channel.
        """
        try:
            self.__logger.info(Constants.CHANNEL_OPENED)
            self.__logger.debug(
                f"on_channel_open: {Constants.CHANNEL_OPENED_DEBUG.format(channel)}"
            )
            self.__channel: pika.channel.Channel = channel
            self.__channel_opened_event.set()
            if self.sending_queue and self.sending_queue != "":
                self.__channel.queue_declare(
                    queue=self.sending_queue,
                    callback=self.__on_sending_queue_declareok,
                    durable=True,
                )
            else:
                self.__sending_queue_declared_event.set()
            if self.listening_queue and self.listening_queue != "":
                self.__channel.queue_declare(
                    queue=self.listening_queue,
                    callback=self.__on_listening_queue_declareok,
                    durable=True,
                )
            else:
                self.__listening_queue_declared_event.set()
            if self.sending_exchange and self.sending_exchange != "":
                self.__channel.exchange_declare(
                    exchange=self.sending_exchange,
                    exchange_type=self.exchange_type,
                    callback=self.__on_exchange_declareok,
                )
                if self.sending_queue and self.sending_queue != "":
                    self.__channel.queue_bind(
                        exchange=self.sending_exchange,
                        queue=self.sending_queue,
                        routing_key=self.sending_queue,
                    )
            else:
                self.__exchange_declared_event.set()
        except pika.exceptions.ChannelError as e:
            self.__logger.error(Constants.CHANNEL_OPEN_ERROR.format(e))
            self.__logger.debug(
                f"on_channel_open: {Constants.CHANNEL_OPEN_ERROR_DEBUG.format(channel, e)}"
            )
        except Exception as e:
            self.__logger.error(Constants.GENERIC_ERROR.format(e))

    def __on_exchange_declareok(self, frame):
        """
        Callback invoked after the exchange declaration.

        Args:
            frame: RabbitMQ response frame.
        """
        self.__logger.info(Constants.QUEUE_DECLARED.format(self.sending_exchange))
        self.__logger.debug(
            f"on_exchange_declareok: {Constants.QUEUE_DECLARED_DEBUG.format(self.send_message, frame)}"
        )
        self.__exchange_declared_event.set()

    def __on_listening_queue_declareok(self, frame):
        """
        Callback invoked after the listening queue declaration.

        Args:
            frame: RabbitMQ response frame.
        """
        self.__logger.info(Constants.QUEUE_DECLARED.format(self.listening_queue))
        self.__logger.debug(
            f"on_listening_queue_declareok: {Constants.QUEUE_DECLARED_DEBUG.format(self.listening_queue, frame)}"
        )
        if self.listening_queue:
            self.__channel.basic_consume(
                queue=self.listening_queue,
                on_message_callback=self.__on_message_wrapper,
                auto_ack=True,
            )

        self.__listening_queue_declared_event.set()

    def __on_sending_queue_declareok(self, frame):
        """
        Callback invoked after the sending queue declaration.

        Args:
            frame: RabbitMQ response frame.
        """
        self.__logger.info(Constants.QUEUE_DECLARED.format(self.sending_queue))
        self.__logger.debug(
            f"on_sending_queue_declareok: {Constants.QUEUE_DECLARED_DEBUG.format(self.sending_queue, frame)}"
        )
        self.__sending_queue_declared_event.set()

    def __on_message_wrapper(self, channel, method, properties, body):
        """
        Wrapper for the on_message callback, creates an asynchronous task.

        Args:
            channel: RabbitMQ channel.
            method: RabbitMQ messaging method.
            properties: RabbitMQ message properties.
            body: Message body.
        """
        asyncio.create_task(self.__on_message(channel, method, properties, body))

    async def __on_message(self, channel, method, properties, body):
        """
        Asynchronous callback for handling received messages.

        Args:
            channel: RabbitMQ channel.
            method: RabbitMQ messaging method.
            properties: RabbitMQ message properties.
            body: Message body.
        """
        try:
            if self.log_on_receiving:
                self.__logger.info(Constants.MESSAGE_RECEIVED.format(body, channel))
            if self.on_message_callback:
                if self.log_on_receiving:
                    self.__logger.debug(
                        f"on_message: {Constants.MESSAGE_RECEIVED_DEBUG.format(body, channel, method, properties)}"
                    )
                await self.on_message_callback(channel, method, properties, body)

            else:
                if self.log_on_receiving:
                    self.__logger.info(Constants.MESSAGE_RECEIVED.format(body, channel))
                    self.__logger.debug(
                        f"on_message: {Constants.MESSAGE_RECEIVED_DEBUG.format(body, channel, method, properties)}"
                    )
        except Exception as e:
            self.__logger.error(Constants.MESSAGE_PROCESSING_ERROR.format(e))
            self.__logger.debug(
                f"on_message: {Constants.MESSAGE_PROCESSING_ERROR_DEBUG.format(body, channel, method, properties, e)}"
            )
            raise Error(Constants.MESSAGE_PROCESSING_ERROR.format(e))

    def send_message(self, message, routing_key="", to_exchange=False):
        """
        Sends a message to RabbitMQ.

        Args:
            message: The message to send.
            routing_key (str, optional): Routing key for the message.
            to_exchange (bool, optional): Whether to send the message to the exchange.
        """
        try:
            if not self.__connection or not self.__connection.is_open:
                raise ConnectionError(Constants.CONNECTION_NOT_OPENED)
            if not self.__channel or not self.__channel.is_open:
                raise ConnectionError(Constants.CHANNEL_NOT_OPENED)
            if not self.__is_connected:
                raise ConnectionError(Constants.CONNECTION_NOT_ESTABLISHED)
            message = json.dumps(message)
            routing_key = (
                self.sending_queue
                if routing_key is None or routing_key == ""
                else routing_key
            )
            properties = pika.BasicProperties(
                app_id="rabbit-hole", content_type="application/json"
            )
            exchange = self.sending_exchange if to_exchange else ""
            self.__channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message,
                properties=properties,
            )
            if self.log_on_sending:
                self.__logger.info(Constants.MESSAGE_SENT.format(message, routing_key))
        except Exception as e:
            self.__logger.error(Constants.MESSAGE_SENDING_ERROR.format(e))
            self.__logger.debug(
                f"send_message: {Constants.MESSAGE_SENDING_ERROR_DEBUG.format(message, routing_key, e)}"
            )
            raise Error(Constants.MESSAGE_SEND_FAILED.format(e))

    async def close_connection(self):
        """
        Closes the connection with RabbitMQ asynchronously.
        """
        self.__should_reconnect = False
        if self.__connection.is_closing or self.__connection.is_closed:
            self.__logger.info("Connection is closing or already closed")
        else:
            self.__logger.info("Closing connection")
            self.__connection.close()

    async def close_resources(self):
        """
        Chiude delicatamente il canale e la connessione.
        """
        try:
            if self.__channel and self.__channel.is_open:
                await self.__channel.close()
                self.__logger.info(Constants.CHANNEL_CLOSED)
        except Exception as e:
            self.__logger.error(Constants.CHANNEL_CLOSING_ERROR.format(e))

        try:
            if self.__connection and self.__connection.is_open:
                await self.close_connection()
                self.__logger.info(Constants.CONNECTION_CLOSED)
        except Exception as e:
            self.__logger.error(Constants.CONNECTION_CLOSING_ERROR.format(e))

        self.__is_connected = False
