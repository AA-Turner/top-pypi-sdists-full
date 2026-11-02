"""One immutable source publication shared by a bounded stream of host invocations."""

from threading import Lock
from typing import Generic, TypeVar

from labqoat._generated.compute_publication import ComputePublication
from labqoat._generated.transport import Transport
from labqoat.assets_client import AssetsClient
from labqoat.base_client import BaseClient
from labqoat.compute.function import Function
from labqoat.compute.function_signature import FunctionSignature
from labqoat.compute.publication import Publication
from labqoat.compute.run_options import RunOptions
from labqoat.compute.submission import Submission
from labqoat.runs.run_handle import RunHandle

R = TypeVar("R")


class PreparedSubmission(BaseClient, Generic[R]):
    """Capture on first valid input and serialize concurrent first-publication requests."""

    def __init__(self, transport: Transport, function: Function[..., R]) -> None:
        """Retain explicit dependencies without capturing files or starting requests."""
        super().__init__(transport)
        self.function = function
        self._lock = Lock()
        self._publication: ComputePublication | None = None

    def submit(self, arguments: tuple[object, ...], options: RunOptions) -> RunHandle[R]:
        """Validate each scalar input against the single retained declaration before admission."""
        from labqoat.runs_client import RunsClient

        encoded = self.function.encode(arguments, {})
        record = Submission(self._transport).accept(self.function, encoded, self._capture(), options)
        result_type = FunctionSignature(self.function.local).annotations["return"]
        return RunHandle(record.id, RunsClient(self._transport, options), result_type)

    def _capture(self) -> ComputePublication:
        """Make every input in this stream refer to the same bytes even if host files change."""
        with self._lock:
            if self._publication is None:
                self._publication = Publication(AssetsClient(self._transport)).capture(self.function)
            return self._publication
