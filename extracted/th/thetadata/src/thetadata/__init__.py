import logging

from .client import ThetaClient

# Set up a null handler for the library's logger
logging.getLogger(__name__).addHandler(logging.NullHandler())

