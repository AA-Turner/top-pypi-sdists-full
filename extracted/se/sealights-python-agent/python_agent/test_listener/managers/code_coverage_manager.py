import logging
import os
import threading

import python_agent
from python_agent.common import constants
from python_agent.packages.coverage import Coverage
from python_agent.test_listener.managers._coverage_core import apply_pytrace_default
from python_agent.test_listener.method_footprints_collector import (
    MethodFootprintsCollector,
)

log = logging.getLogger(__name__)


class CodeCoverageManager(object):
    def __init__(self, config_data):
        self.config_data = config_data
        self.should_reset_coverage = not bool(self.config_data.covReport)
        self.coverage = self.init_coverage()
        self.coverage_lock = threading.Lock()
        self.coverage_collectors = {}
        self.coverage_collectors["methods"] = MethodFootprintsCollector(
            config_data.workspacepath
        )
        log.info("Started Code Coverage Manager")

    def get_footprints_and_clear(self):
        footprints = {}
        with self.coverage_lock:
            if constants.IN_TEST:
                # save coverage data that can be later be converted to footprints before reset
                self.coverage.save()
            # get_data creates or updates coverage.data with the CoverageData object and clears counters on the
            # collector but not on the coverage object
            coverage_object = self.coverage.get_data()
            log.debug(
                "before clearing coverage: %s"
                % self.extract_file_covered_lines(coverage_object)
            )
            if not coverage_object:
                log.info("No Coverage Found")
                return footprints
            for coverage_type, coverage_collector in list(
                self.coverage_collectors.items()
            ):
                footprints[coverage_type] = coverage_collector.get_footprints_and_clear(
                    coverage_object
                )

            if self.should_reset_coverage:
                self.clear_counters(coverage_object)
        return footprints

    def shutdown(self, is_master):
        self.coverage.stop()
        if constants.IN_TEST:
            # save coverage data that can be later be converted to footprints
            self.coverage.save()
        if self.config_data.covReport:
            self.generate_report(is_master)
        log.info("Finished Shutting Down Code Coverage Manager")

    def register_collector(self, coverage_type, collector):
        self.coverage_collectors[coverage_type] = collector

    def get_trace_function(self):
        return self.coverage._collector._installation_trace

    def clear_counters(self, coverage_object):
        # get_data creates or updates coverage.data with the CoverageData object and
        # clears counters on the collector but not on the coverage.data object
        # we make sure to erase coverage.data
        coverage_object.erase()

    def init_coverage(self):
        apply_pytrace_default(self.config_data.command_name)
        self.config_data.include = self.config_data.include or []
        self.config_data.include.append(
            "*%s/*" % os.path.abspath(self.config_data.workspacepath)
        )
        if constants.IN_TEST:
            # coverage.py ignores "include" if source is given so, in order to include python agent coverage
            # we move workspacepath to include, include python_agent, remove exclude and add "data_suffix=True" so
            # coverage files will be saved each time with a unique suffix so we won't loose coverage after each reset
            self.config_data.include.append("*/%s/*" % python_agent.__name__)
            coverage = Coverage(
                source=None,
                include=self.config_data.include,
                omit=None,
                data_suffix=True,
                branch=False,
            )
        else:
            coverage = Coverage(
                source=None,
                include=self.config_data.include,
                omit=self.config_data.exclude,
                data_suffix=True,
                branch=False,
                data_file=None,
            )
        if getattr(coverage, "_warn_no_data", False):
            coverage._warn_no_data = False
        if self.config_data.isOfflineMode:
            # no actual tracing is done here
            # we're loading the raw coverage data from the .coverage file
            # so coverage.get_data() will return it and we'll convert it to footprints
            coverage.load()
        else:
            coverage.start()

        return coverage

    def generate_report(self, is_master):
        self.coverage.save()
        if not is_master:
            # in case of xdist, we have multiple agent instances, only the master will load, combine all coverage files
            # and generated the xml report
            return
        self.coverage.load()
        self.coverage.combine()
        try:
            self.coverage.xml_report(
                ignore_errors=True, outfile=self.config_data.covReport
            )
            log.info("Coverage report created in %s" % self.config_data.covReport)
        except Exception as e:
            log.error("Failed creating report. error=%s" % e)

    def extract_file_covered_lines(self, coverage_object):
        return {
            filename: coverage_object.lines(filename)
            for filename in coverage_object.measured_files()
        }
