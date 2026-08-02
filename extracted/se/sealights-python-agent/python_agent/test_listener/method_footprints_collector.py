import logging
import os
import re

from python_agent.build_scanner.file_scanner import FileScanner
from python_agent.common import constants
from python_agent.test_listener.footprints_collector import FootprintsCollector
from python_agent.utils import get_top_relative_path

log = logging.getLogger(__name__)


class MethodFootprintsCollector(FootprintsCollector):
    def __init__(self, workspacepath):
        self.file_scanner = FileScanner()
        self.files_signatures = {}
        self.workspacepath = workspacepath

    def get_footprints_and_clear(self, coverage_object):
        footprints = []
        for filename in coverage_object.measured_files():
            covered_lines = coverage_object.lines(filename)
            if not re.match(constants.PYTHON_FILES_REG, os.path.split(filename)[1]):
                continue
            file_signature = self.files_signatures.get(filename)
            if not file_signature:
                file_data = self.file_scanner.calculate_file_signature(
                    filename,
                    get_top_relative_path(filename, workspacepath=self.workspacepath),
                )
                file_signature = {
                    "file_data": file_data,
                    "line_map": {},
                    "sorted": False,
                }
                self.files_signatures[filename] = file_signature
            covered_methods = self._lines_to_methods(file_signature, covered_lines)

            if covered_methods:
                file_footprints = [
                    {"unique_id": method.uniqueId, "hits": 1, "filename": filename}
                    for method in covered_methods
                ]
                footprints.extend(file_footprints)
        return footprints

    def _lines_to_methods(self, file_signature, covered_lines):
        line_methods = {}
        for line_num in covered_lines:
            if file_signature["line_map"].get(line_num):
                method = file_signature["line_map"].get(line_num)
                line_methods[method.uniqueId] = method
                continue
            if not file_signature["sorted"]:
                file_signature["file_data"].methods = sorted(
                    file_signature["file_data"].methods,
                    key=lambda method: method.position[0],
                    reverse=True,
                )
                file_signature["sorted"] = True
            for method in file_signature["file_data"].methods:
                if self._is_match(method, int(line_num)):
                    line_methods[method.uniqueId] = method
                    file_signature["line_map"][line_num] = method
                    break
        return list(line_methods.values())

    def _is_match(self, method, line_num):
        """
        In python, on file import, the python interpreter scans the file and goes over method definitions.
         That means, that all method definition lines get hit from the coverage.py perspective,
         even though, this method might not be called.

         Sadly, there are methods that their definition and body is on the same line.
         example:
            (1) def foo(a, b): return a + b
            (2) lambda x: x + 1
        These kind of methods we count as a hit anyway. We do that since the coverage.py tool does that too.
        :param method: the candidate method to match against the line number
        :param line_num: the line number that was hit
        :return: True if we have a match, False otherwise
        """

        # default method definition. We don't include the first line
        is_match = method.position[0] < line_num <= method.endPosition[0]

        # one liner method. We include the first line
        if method.position[0] == method.endPosition[0]:
            is_match = method.position[0] <= line_num <= method.endPosition[0]

        return is_match
