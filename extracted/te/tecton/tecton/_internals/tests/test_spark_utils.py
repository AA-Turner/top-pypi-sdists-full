from unittest import TestCase

from tecton._internals.spark_utils import EXECUTOR_ENV_VARIABLES
from tecton_core import conf


class SparkUtilsTest(TestCase):
    def test_config_presence(self):
        config_vars = set(conf._VALID_KEYS_TO_ALLOWED_SOURCES)
        # Make sure all executor environment variables are defined as valid config keys
        for e in EXECUTOR_ENV_VARIABLES:
            assert e in config_vars
