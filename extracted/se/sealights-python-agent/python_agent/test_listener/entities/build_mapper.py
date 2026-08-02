import logging
from typing import List

from python_agent.build_scanner.app import scan_files
from python_agent.common.config_data import ConfigData

log = logging.getLogger(__name__)


class BuildMapper(object):
    EXCLUDE_PARAM = "exclude"
    INCLUDE_PARAM = "include"
    WORKSPACE_PATH_PARAM = "workspacepath"

    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.build_context: dict[str, dict[int, str]] = {}
        self.build_coverage: dict[str, dict[str, List[int]]] = {}
        self.current_coverage: dict[str, dict[str, List[int]]] = {}
        self.last_covered_lines_count = 0

    def scan_files_and_calculate_metrics(self) -> "BuildMapper":
        log.info("Start scanning files and calculating metrics.")
        workspacepath, excluded, included = self._get_config_params()
        scanned_files = self._get_scanned_files(workspacepath, included, excluded)
        total_files_count, total_methods_count, total_lines_count = (
            self._calculate_metrics(scanned_files)
        )
        log.info(
            f"Completed scanning files and calculating metrics with total files: {total_files_count}, total methods: {total_methods_count}, total lines: {total_lines_count}"
        )
        return self

    def _get_config_params(self):
        return (
            self.config_data.additionalParams.get(self.WORKSPACE_PATH_PARAM),
            self.config_data.additionalParams.get(self.EXCLUDE_PARAM),
            self.config_data.additionalParams.get(self.INCLUDE_PARAM),
        )

    def _get_scanned_files(self, workspacepath, included, excluded):
        scanned_files = scan_files(workspacepath, included, excluded)
        if not scanned_files:
            log.warning("Total scanned files is 0. Coverage will not be sent to server")
        return scanned_files

    def _calculate_metrics(self, scanned_files):
        total_files_count = 0
        total_methods_count = 0
        total_lines_count = 0
        for full_path, file_data in scanned_files.items():
            normalized_file_path = full_path.replace("\\", "/")
            total_files_count += 1
            lines_to_methods, method_count = self._get_file_data(
                normalized_file_path, file_data
            )
            if lines_to_methods:
                total_methods_count += method_count
                total_lines_count += len(lines_to_methods)
                self.build_context[normalized_file_path] = lines_to_methods
        return total_files_count, total_methods_count, total_lines_count

    def _get_file_data(self, full_path, file_data):
        method_count = 0
        lines_to_methods: dict[int, str] = {}
        if full_path not in self.build_coverage:
            self.build_coverage[full_path] = {}
        for method in file_data.methods:
            method_count += 1
            for line in method.lines:
                lines_to_methods[line] = method.uniqueId
            self.build_coverage.setdefault(full_path, {}).setdefault(
                method.uniqueId, []
            ).extend(method.lines)

        return lines_to_methods, method_count

    def has_file(self, file_path: str) -> bool:
        return file_path in self.build_context

    def get_method_unique_id(self, file_path: str, line: int) -> [str, None]:
        unique_id = self.build_context.get(file_path, {}).get(line)
        if unique_id:
            if line not in self.current_coverage.get(file_path, {}).get(unique_id, []):
                self.current_coverage.setdefault(file_path, {}).setdefault(
                    unique_id, []
                ).append(line)
        return unique_id

    def get_coverage_metrics(self):
        total_current_lines = sum(
            sum(len(lines) for lines in methods.values())
            for methods in self.current_coverage.values()
        )
        self.last_covered_lines_count = total_current_lines
        total_build_files = len(self.build_coverage)
        total_current_files = len(self.current_coverage)
        total_build_methods = sum(
            len(methods) for methods in self.build_coverage.values()
        )
        total_current_methods = sum(
            len(methods) for methods in self.current_coverage.values()
        )
        total_build_lines = sum(
            sum(len(lines) for lines in methods.values())
            for methods in self.build_coverage.values()
        )

        file_coverage_percentage = total_current_files / total_build_files * 100
        method_coverage_percentage = total_current_methods / total_build_methods * 100
        line_coverage_percentage = total_current_lines / total_build_lines * 100
        coverage_message = (
            f"Current coverage collected: "
            f"Files: {file_coverage_percentage:.2f}% ({total_current_files}/{total_build_files}), "
            f"Methods: {method_coverage_percentage:.2f}% ({total_current_methods}/{total_build_methods}), "
            f"Lines: {line_coverage_percentage:.2f}% ({total_current_lines}/{total_build_lines})"
        )
        return coverage_message
