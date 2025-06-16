import pika
import json
import signal
import time
import traceback
from pika.exceptions import AMQPConnectionError, ChannelWrongStateError
from cneura_ai.logger import logger


class MessageWorker:
    def __init__(self, input_queue: str, process_message, host: str = 'localhost', username: str = None, password: str = None, dlq: str = None, max_retries: int = 3):
        self.host = host
        self.input_queue = input_queue
        self.process_message = process_message
        self.dlq = dlq
        self.max_retries = max_retries
        self.connection = None
        self.channel = None
        self.credentials = pika.PlainCredentials(username, password) if username and password else None
        self.parameters = pika.ConnectionParameters(host=self.host, credentials=self.credentials) if self.credentials else pika.ConnectionParameters(host=self.host)

        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def reconnect(self, consume: bool = False):
        while True:
            try:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.input_queue, durable=True)
                if self.dlq:
                    self.channel.queue_declare(queue=self.dlq, durable=True)
                self.channel.basic_qos(prefetch_count=1)
                if consume:
                    self.channel.basic_consume(queue=self.input_queue, on_message_callback=self.callback)
                logger.info("[*] Connected to RabbitMQ")
                break
            except AMQPConnectionError as e:
                logger.error(f"[!] Connection failed: {e}, retrying in 5 seconds...")
                time.sleep(5)

    def validate_response(self, response):
        if not isinstance(response, dict):
            raise ValueError("process_message must return a dictionary")
        if "data" not in response or "queue" not in response:
            raise ValueError("process_message must return 'data' and 'queue'")
        if not isinstance(response["queue"], str) or not response["queue"].strip():
            raise ValueError("'queue' must be a non-empty string")
        # Optional: validate `data` is JSON-serializable
        try:
            json.dumps(response["data"])
        except Exception as e:
            raise ValueError(f"'data' must be JSON-serializable: {e}")

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            response = self.process_message(message)
            logger.debug(f"[>] process_message response: {response}")

            self.validate_response(response)

            target_queue = response["queue"]
            response_data = json.dumps(response["data"])

            self.ensure_queue(target_queue)
            self.safe_publish(target_queue, response_data)
            logger.info(f"[x] Sent to '{target_queue}': {response_data}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception:
            logger.exception("[!] Error processing message")
            self.handle_dlq(ch, method, body, properties)

    def handle_dlq(self, ch, method, body, properties):
        if not self.dlq:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        headers = properties.headers or {}
        retry_count = headers.get("x-retry-count", 0)

        new_headers = {
            **headers,
            "x-retry-count": retry_count + 1,
            "x-original-routing-key": method.routing_key
        }

        if retry_count < self.max_retries:
            delay_seconds = min(2 ** retry_count, 60)  # optional cap at 60s
            logger.warning(f"[!] Retry {retry_count + 1}/{self.max_retries}. Delaying {delay_seconds}s before retry...")
            time.sleep(delay_seconds)
        else:
            logger.warning(f"[!] Max retries reached. Sending to DLQ: {self.dlq}")

        self.safe_publish(self.dlq, body, new_headers)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def ensure_queue(self, queue_name):
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
        except Exception as e:
            logger.error(f"[!] Failed to declare queue '{queue_name}': {e}")

    def safe_publish(self, queue, message, headers=None):
        while True:
            try:
                if not self.channel or self.channel.is_closed:
                    logger.warning("[!] Channel is closed, reconnecting before publishing...")
                    self.reconnect()
                properties = pika.BasicProperties(headers=headers or {}, delivery_mode=2)
                self.channel.basic_publish(exchange='', routing_key=queue, body=message, properties=properties)
                return
            except (AMQPConnectionError, ChannelWrongStateError):
                logger.error("[!] Connection/channel issue during publish, reconnecting...")
                self.reconnect()

    def start(self):
        logger.info(f"[*] Listening for messages in '{self.input_queue}'...")
        self.reconnect(consume=True)
        while True:
            try:
                self.channel.start_consuming()
            except (AMQPConnectionError, ChannelWrongStateError) as e:
                logger.error(f"[!] Connection/channel error: {e}, reconnecting...")
                self.reconnect(consume=True)
            except Exception:
                logger.exception("[!] Unexpected error, stopping worker...")
                self.stop()
                break

    def stop(self):
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
        if self.connection and self.connection.is_open:
            self.connection.close()
        logger.info("[!] Worker stopped.")

    def handle_shutdown(self, signum, frame):
        logger.info("[!] Received shutdown signal. Stopping worker...")
        self.stop()
