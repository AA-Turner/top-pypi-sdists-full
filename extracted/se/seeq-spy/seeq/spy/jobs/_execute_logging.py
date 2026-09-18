from __future__ import annotations

import logging
import os
import re
import sys
from datetime import datetime
from typing import TYPE_CHECKING, Any, Iterable, Optional, Tuple

if TYPE_CHECKING:
    # Imported for annotations only. nbconvert and nbformat are optional dependencies, so importing them at
    # runtime would make this module unusable wherever the jobs extra is not installed.
    from nbconvert.preprocessors import ExecutePreprocessor
    from nbformat import NotebookNode

# A traceback's frames are small -- IPython collapses repeated ones -- but the exception message it carries is not
# bounded. ApiException, for one, renders the entire HTTP response body, so cap what reaches the log and leave the
# complete traceback to the notebook result.
MAX_LOGGED_ERROR_CHARS = 10000

# The kernel colorizes the tracebacks it sends back
ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')


def get_log_level_from_executor() -> str:
    return str(os.environ.get('LOG_LEVEL', 'INFO')).upper()


def is_log_level_trace_from_executor() -> bool:
    return get_log_level_from_executor() == "TRACE"


def get_executor_logger(file_path: str, job_key: str) -> logging.Logger:
    """
    Logger to be used for logging inside executor container
    """
    log_level = get_log_level_from_executor()

    # python logging doesnt have TRACE
    log_level = "DEBUG" if log_level == "TRACE" else log_level

    executor_logger = logging.getLogger("executor_logger")
    exec_handler = logging.StreamHandler(sys.stdout)
    exec_formatter = logging.Formatter(
        f'%(levelname)s - Notebook {file_path.replace("%", "%%")} with jobKey {job_key} %(message)s')
    exec_handler.setFormatter(exec_formatter)
    # Replace rather than append so that the handler is not duplicated if this is called more than once
    executor_logger.handlers.clear()
    executor_logger.addHandler(exec_handler)
    executor_logger.setLevel(log_level)

    return executor_logger


def _seconds_since(start_time: datetime) -> float:
    return (datetime.now() - start_time).total_seconds()


class _NotebookExecutionLogger:
    """
    Echoes cell-by-cell execution progress, and any error a cell raises, to the executor log.

    This is a mixin for nbconvert's ExecutePreprocessor rather than a subclass of it, so that the logging behavior
    can be exercised without nbconvert, which is an optional dependency.
    """

    executor_logger: logging.Logger
    job_result_path: str
    login_cell_count: int
    cell_numbers: dict
    total_code_cells: int

    def initialize_logging(self, logger: logging.Logger, job_result_path: str, login_cell_count: int) -> None:
        self.executor_logger = logger
        self.job_result_path = job_result_path
        # How many cells the caller prepended to the scheduled notebook's own cells, which the log does not number
        self.login_cell_count = login_cell_count
        # Notebook cell index -> the number this cell is reported as in the log
        self.cell_numbers = dict()
        self.total_code_cells = 0

    def preprocess(self, nb: NotebookNode, resources: Optional[dict] = None,
                   km: Optional[Any] = None) -> Tuple[NotebookNode, Optional[dict]]:
        self._number_code_cells(nb.cells)
        self.executor_logger.info(
            f'started executing {self.total_code_cells} code cell(s) with kernel {self.kernel_name}')
        return super().preprocess(nb, resources, km)

    def _number_code_cells(self, cells: Iterable[Any]) -> None:
        # Number cells the way the exported HTML does: by their order among the scheduled notebook's code cells.
        # That excludes the cells the caller prepended as well as any markdown cells.
        scheduled_code_cells = [index for index, cell in enumerate(cells)
                                if index >= self.login_cell_count and cell.get('cell_type') == 'code']
        self.cell_numbers = {index: number for number, index in enumerate(scheduled_code_cells, start=1)}
        self.total_code_cells = len(scheduled_code_cells)

    def preprocess_cell(self, cell: NotebookNode, resources: Optional[dict], index: int,
                        **kwargs: Any) -> Tuple[NotebookNode, Optional[dict]]:
        if cell.get('cell_type') != 'code':
            return super().preprocess_cell(cell, resources, index, **kwargs)

        cell_label = self._cell_label(index)
        self.executor_logger.info(f'started executing {cell_label}')
        cell_start_time = datetime.now()
        try:
            result = super().preprocess_cell(cell, resources, index, **kwargs)
        except Exception:
            # Errors raised by the notebook itself are collected as cell output rather than raised, because the
            # preprocessor is configured with allow_errors. Reaching here means the execution itself failed, and how
            # long the cell ran is the useful part -- a cell that hit the execution timeout looks like any other
            # failure otherwise. The error itself is reported by the caller.
            self.executor_logger.error(
                f'failed executing {cell_label} after {_seconds_since(cell_start_time):.3f} seconds')
            raise

        self.executor_logger.info(
            f'finished executing {cell_label} in {_seconds_since(cell_start_time):.3f} seconds')
        return result

    def output(self, outs: list, msg: dict, display_id: Optional[str],
               cell_index: Optional[int]) -> Optional[NotebookNode]:
        # Called by nbclient for each output message as it arrives, which is what makes an error visible in the
        # executor log as soon as the cell raises it rather than only in the exported HTML
        result = super().output(outs, msg, display_id, cell_index)

        # noinspection PyBroadException
        try:
            self._log_cell_error(msg, cell_index)
        except Exception:
            # Logging must never break the notebook execution
            pass

        return result

    def _log_cell_error(self, msg: dict, cell_index: Optional[int]) -> None:
        msg_type = msg.get('msg_type') or msg.get('header', {}).get('msg_type')
        if msg_type != 'error':
            return

        content = msg.get('content', {})
        traceback = ANSI_ESCAPE_PATTERN.sub('', '\n'.join(content.get('traceback', [])))
        self.executor_logger.error(self._truncate_error(
            f'{self._cell_label(cell_index)} raised '
            f'{content.get("ename")}: {content.get("evalue")}\n{traceback}'))

    def _truncate_error(self, message: str) -> str:
        # allow_errors lets the run continue past a failing cell, so every cell in a notebook can raise.
        if is_log_level_trace_from_executor() or len(message) <= MAX_LOGGED_ERROR_CHARS:
            return message

        return (f'{message[:MAX_LOGGED_ERROR_CHARS]}\n'
                f'... [truncated after {MAX_LOGGED_ERROR_CHARS} characters; '
                f'the complete traceback is in /{self.job_result_path}]')

    def _cell_label(self, cell_index: Optional[int]) -> str:
        if cell_index is None:
            return 'an unknown cell'
        if cell_index < self.login_cell_count:
            return 'the login cell'
        cell_number = self.cell_numbers.get(cell_index)
        if cell_number is None:
            return f'the cell at index {cell_index}'
        return f'cell {cell_number} of {self.total_code_cells}'


def build_logging_execute_preprocessor(logger: logging.Logger, job_result_path: str, login_cell_count: int,
                                       **kwargs: Any) -> ExecutePreprocessor:
    """
    Build an ExecutePreprocessor that logs through _NotebookExecutionLogger, ready to preprocess a notebook. The
    class is built here rather than at module scope because nbconvert is an optional dependency that is imported
    lazily.
    """
    import nbconvert

    preprocessor_class = type('LoggingExecutePreprocessor',
                              (_NotebookExecutionLogger, nbconvert.preprocessors.ExecutePreprocessor), {})
    preprocessor = preprocessor_class(**kwargs)
    preprocessor.initialize_logging(logger, job_result_path, login_cell_count)
    return preprocessor
