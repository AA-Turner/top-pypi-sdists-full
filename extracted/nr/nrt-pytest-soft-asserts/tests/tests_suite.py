from typing import Optional

import pytest
from coverage import Coverage


class TestsSuite:
    CONFIG_FILE = ".coveragerc"

    is_tests_suite_run: bool = False
    log_file_path: Optional[str] = None

    __coverage: Optional[Coverage] = None
    __is_coverage: bool

    def __init__(self, is_coverage: bool = False):
        self.__coverage = Coverage(config_file=self.CONFIG_FILE)
        self.__is_coverage = is_coverage
        TestsSuite.is_tests_suite_run = True

    def run_tests(self):
        if self.__is_coverage:
            self.__coverage.start()

        pytest.main(['-x', './tests'])

        if self.__is_coverage:
            self.__coverage.stop()

    def create_report(self):
        self.__coverage.report()
        self.__coverage.json_report()
        self.__coverage.lcov_report()
        self.__coverage.html_report()

    def erase_data(self):
        self.__coverage.erase()
