# Standard Library
from unittest.mock import patch

# Django
from django.test import TestCase

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.decorators import (
    log_timing,
)
from killstats.providers import AppLogger

DECORATOR_PATH = "killstats.decorators."


class TestDecorators(TestCase):
    def test_log_timing(self):
        # given
        logger = AppLogger(get_extension_logger(__name__), __title__)

        @log_timing(logger)
        def trigger_log_timing():
            return "Log Timing"

        # when
        result = trigger_log_timing()
        # then
        self.assertEqual(result, "Log Timing")
