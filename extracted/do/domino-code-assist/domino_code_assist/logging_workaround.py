# workaround: turn off logging to stderr, which is turned on in Domino (and by an unknown other library)
import logging

logging.basicConfig(level=logging.CRITICAL)
