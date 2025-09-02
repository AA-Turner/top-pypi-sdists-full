import logging

faker_logger = logging.getLogger("faker.factory")
faker_logger.setLevel("INFO")

pytest_plugins = ["tests.http_protocol.fixtures"]
