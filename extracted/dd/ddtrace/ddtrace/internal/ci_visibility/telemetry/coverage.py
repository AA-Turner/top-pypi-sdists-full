from enum import Enum
from typing import List
from typing import Optional
from typing import Tuple

from ddtrace.internal.ci_visibility.telemetry.constants import TEST_FRAMEWORKS
from ddtrace.internal.logger import get_logger
from ddtrace.internal.telemetry import telemetry_writer
from ddtrace.internal.telemetry.constants import TELEMETRY_NAMESPACE


log = get_logger(__name__)


class COVERAGE_TELEMETRY(str, Enum):
    STARTED = "code_coverage_started"
    FINISHED = "code_coverage_finished"
    IS_EMPTY = "code_coverage.is_empty"
    FILES = "code_coverage.files"
    ERRORS = "code_coverage.errors"


class COVERAGE_LIBRARY(str, Enum):
    COVERAGEPY = "coveragepy"
    DD_COVERAGE = "ddcoverage"


def record_code_coverage_started(coverage_library: COVERAGE_LIBRARY, test_framework: Optional[TEST_FRAMEWORKS] = None):
    log.debug("Recording code coverage started telemetry: %s, %s", test_framework, coverage_library)
    _tags: List[Tuple[str, str]] = [("library", coverage_library)]
    if test_framework is not None:
        _tags.append(("test_framework", test_framework))
    telemetry_writer.add_count_metric(TELEMETRY_NAMESPACE.CIVISIBILITY, COVERAGE_TELEMETRY.STARTED, 1, tuple(_tags))


def record_code_coverage_finished(coverage_library: COVERAGE_LIBRARY, test_framework: Optional[TEST_FRAMEWORKS] = None):
    log.debug("Recording code coverage finished telemetry: %s, %s", test_framework, coverage_library)
    _tags: List[Tuple[str, str]] = [("library", coverage_library)]
    if test_framework is not None:
        _tags.append(("test_framework", test_framework))
    telemetry_writer.add_count_metric(TELEMETRY_NAMESPACE.CIVISIBILITY, COVERAGE_TELEMETRY.FINISHED, 1, tuple(_tags))


def record_code_coverage_empty():
    log.debug("Recording code coverage empty telemetry")
    telemetry_writer.add_count_metric(TELEMETRY_NAMESPACE.CIVISIBILITY, COVERAGE_TELEMETRY.IS_EMPTY, 1)


def record_code_coverage_files(count_files: int):
    log.debug("Recording code coverage files telemetry: %s", count_files)
    telemetry_writer.add_distribution_metric(TELEMETRY_NAMESPACE.CIVISIBILITY, COVERAGE_TELEMETRY.FILES, count_files)


def record_code_coverage_error():
    log.debug("Recording code coverage error telemetry")
    telemetry_writer.add_count_metric(TELEMETRY_NAMESPACE.CIVISIBILITY, COVERAGE_TELEMETRY.ERRORS, 1)
