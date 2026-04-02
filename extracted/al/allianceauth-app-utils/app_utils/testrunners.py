"""Custom test runners for Django."""

import statistics
from time import time
from typing import List, NamedTuple
from unittest.runner import TextTestResult, TextTestRunner

from django.test.runner import DiscoverRunner

SLOWEST_TESTS_TOP_COUNT = 10


class _TestDurationResult(NamedTuple):
    name: str  # Name of the test
    duration: float  # duration in seconds


_results: List[_TestDurationResult] = []


class _TimedTextTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clocks = {}

    def startTest(self, test):
        self.clocks[test] = time()
        super().startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        super().addSuccess(test)
        duration = time() - self.clocks[test]
        _results.append(_TestDurationResult(name=str(test), duration=duration))
        if self.showAll:
            self.stream.writeln(f"{duration:.2f}s")
        elif self.dots:
            self.stream.write(".")
            self.stream.flush()


class _TimedTextTestRunner(TextTestRunner):
    resultclass = _TimedTextTestResult

    def run(self, test):
        result = super().run(test)
        self._output_slowest_tests()
        return result

    def _output_slowest_tests(self):
        """Write list of slowest tests to output."""
        self.stream.writeln()
        self.stream.writeln(f"Top {SLOWEST_TESTS_TOP_COUNT} slowest tests:")
        _results.sort(reverse=True, key=lambda o: o.duration)
        for obj in _results[:SLOWEST_TESTS_TOP_COUNT]:
            self.stream.writeln(f"{obj.duration:>8.2f}s: {obj.name}")
        values = [obj.duration for obj in _results]
        average_duration = statistics.mean(values)
        tests_count = len(values)
        self.stream.writeln(
            f"Average test duration of {tests_count} tests was {average_duration:.2f}s."
        )
        self.stream.writeln()
        self.stream.flush()


class TimedTestRunner(DiscoverRunner):
    """Test runner which adds duration measurements to each tests (when verbose)
    and shows list of slowest tests at the end.

    To use in tests define via the ``TEST_RUNNER`` setting
    or as ``--testrunner`` parameter for ``test``, e.g.:

    .. code-block:: python

        TEST_RUNNER = "app_utils.testrunners.TimedTestRunner"


    .. code-block:: bash

        python manage.py test -v 2 --testrunner app_utils.testrunners.TimedTestRunner

    """

    test_runner = _TimedTextTestRunner
