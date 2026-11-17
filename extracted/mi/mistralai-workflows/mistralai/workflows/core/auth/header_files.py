import functools
from collections.abc import Mapping
from pathlib import Path

from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.config.config import WorkerConfig, config
from mistralai.workflows.exceptions import WorkflowError

logger = get_logger(__name__)


class HeaderFiles:
    """Header values read from files, re-read on every use so rotated files are picked up.

    A failed or empty read keeps the last value read, so a file briefly missing during rotation does not
    drop the header. It raises a retryable ``WorkflowError`` only when a header has never been read.
    """

    def __init__(self, paths: Mapping[str, str]) -> None:
        self._paths = {name: Path(path) for name, path in paths.items()}
        self._last_values: dict[str, str] = {}

    @property
    def names(self) -> frozenset[str]:
        return frozenset(self._paths)

    def read(self) -> dict[str, str]:
        for name, path in self._paths.items():
            value = self._read_file(path)
            if value:
                self._last_values[name] = value
                continue
            if name not in self._last_values:
                raise WorkflowError(f"Cannot read the value of header {name} from {path}")
            logger.warning("Failed to re-read header file; keeping the last value", header=name, path=str(path))
        return dict(self._last_values)

    @staticmethod
    def _read_file(path: Path) -> str:
        try:
            return path.read_text().strip()
        except (OSError, ValueError):
            return ""


def get_header_files(worker_config: WorkerConfig | None = None) -> HeaderFiles | None:
    paths = (worker_config or config.worker).mistral_api_header_files
    if not paths:
        return None
    return _header_files_for(tuple(sorted(paths.items())))


@functools.cache
def _header_files_for(paths: tuple[tuple[str, str], ...]) -> HeaderFiles:
    return HeaderFiles(dict(paths))


def get_deployment_headers(worker_config: WorkerConfig | None = None) -> dict[str, str]:
    """The worker's identity headers: ``MISTRAL_API_HEADERS`` plus current ``MISTRAL_API_HEADER_FILES`` values."""
    worker_config = worker_config or config.worker
    header_files = get_header_files(worker_config)
    return {**(worker_config.mistral_api_headers or {}), **(header_files.read() if header_files else {})}


def get_deployment_header_names(worker_config: WorkerConfig | None = None) -> frozenset[str]:
    worker_config = worker_config or config.worker
    header_files = get_header_files(worker_config)
    return frozenset(worker_config.mistral_api_headers or {}) | (header_files.names if header_files else frozenset())
