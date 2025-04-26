import logging

import msgpack

from utf_queue_client.clients.async_consumer import LocalRaspiSqaTestResultConsumer


def message_handler(body: bytes):
    logger = logging.getLogger("main")
    data = msgpack.loads(body)
    logger.info(f"message received: {data}")


def main():
    consumer = LocalRaspiSqaTestResultConsumer("10.4.1.107", message_handler)
    consumer.run()


if __name__ == "__main__":
    main()
