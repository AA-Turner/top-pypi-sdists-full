import os
import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from openapi_client.models import ExperimentMetricEntry
from openapi_client.models.v1_plot_entry import (
    V1PlotEntry,
)
from vessl.util import logger
from vessl.util.common import safe_cast


class Collector(ABC):
    DROP_THRESHOLD = 360

    def __init__(self):
        self.buffer: Union[List[ExperimentMetricEntry], List[V1PlotEntry]] = []
        self.lock = threading.Lock()

    def add(self, entries: Union[List[ExperimentMetricEntry], List[V1PlotEntry]]):
        with self.lock:
            self.buffer += entries

    def collect(self):
        with self.lock:
            if len(self.buffer) > self.DROP_THRESHOLD:
                dropped = len(self.buffer) - self.DROP_THRESHOLD
                logger.warning(f"{dropped} collector entries dropped")
                self.buffer = self.buffer[-self.DROP_THRESHOLD :]

            return self.buffer[:]

    def truncate(self, idx):
        with self.lock:
            self.buffer = self.buffer[idx:]

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class IOCollector(Collector):
    def create_write_hook(self, orig_write, io_name):
        def _write(s: str) -> int:
            if s.strip() != "":
                self.add(
                    [
                        ExperimentMetricEntry(
                            measurement="log",
                            ts=time.time(),
                            tags={},
                            fields={io_name: s},
                        )
                    ]
                )
            return orig_write(s)

        return _write

    def __init__(self):
        super().__init__()

    def start(self):
        self.old_stdout_write = sys.stdout.write
        self.old_stderr_write = sys.stderr.write

        stdout_write_hook = self.create_write_hook(sys.stdout.write, "stdout")
        stderr_write_hook = self.create_write_hook(sys.stderr.write, "stderr")

        sys.stdout.write = stdout_write_hook
        sys.stderr.write = stderr_write_hook

    def create_callback(self, io_name):
        def f(ts, content):
            self.add(
                [
                    ExperimentMetricEntry(
                        measurement="log", ts=ts, tags={}, fields={io_name: content}
                    )
                ]
            )

        return f

    def stop(self):
        sys.stdout.write = self.old_stdout_write
        sys.stderr.write = self.old_stderr_write


class UserMetricCollector(Collector):
    def __init__(self) -> None:
        super().__init__()
        self.step = 0

    def start(self):
        pass

    def stop(self):
        pass

    def handle_step(self, step: Optional[int]):
        if step is not None:
            if step < self.step:
                logger.warning("Step should not go backwards")
            self.step = step
        else:
            self.step += 1

    def _read_distributed_info(self) -> Dict[str, int]:
        distributed_info = {}
        distributed_number = safe_cast(os.environ.get("VESSL_DISTRIBUTED_NUMBER", None), int)
        if distributed_number is not None:
            distributed_info = {"distributed_number": distributed_number}
        else:
            workload_id = safe_cast(os.environ.get("VESSL_WORKLOAD_ID", None), int)
            if workload_id is not None:
                distributed_info = {"workload_id": workload_id}

        return distributed_info

    def build_metric_payload(self, payload: Dict[str, Any], ts: float):
        fields = payload
        tags = {"step": str(self.step)}

        distributed_info = self._read_distributed_info()
        if "distributed_number" in distributed_info:
            tags["distributed_number"] = str(distributed_info["distributed_number"])
        if "workload_id" in distributed_info:
            fields["workload_id"] = distributed_info["workload_id"]

        return ExperimentMetricEntry(
            measurement="experiment_plot_metric",
            ts=ts,
            tags=tags,
            fields=fields,
        )

    def build_media_payload(self, payload: Dict[str, Any], ts: float):
        fields = payload
        tags = {"step": str(self.step)}

        distributed_info = self._read_distributed_info()
        if "distributed_number" in distributed_info:
            tags["distributed_number"] = str(distributed_info["distributed_number"])
        if "workload_id" in distributed_info:
            fields["workload_id"] = distributed_info["workload_id"]

        return ExperimentMetricEntry(
            measurement="experiment_plot_file",
            ts=ts,
            tags=tags,
            fields=fields,
        )

    def log_metrics(self, payloads: List[ExperimentMetricEntry]) -> int:
        self.add(payloads)
        return self.step

    def log_media(self, payloads: List[ExperimentMetricEntry]) -> int:
        self.add(payloads)
        return self.step


class K8sCollector(Collector):
    def __init__(self) -> None:
        super().__init__()

    def start(self):
        # TODO
        pass

    def stop(self):
        # TODO
        pass


class RunExecutionMetricCollector(Collector):
    def __init__(self) -> None:
        super().__init__()
        self.step = 0

    def start(self):
        pass

    def stop(self):
        pass

    def handle_step(self, step: Optional[int]):
        if step is not None:
            if step < self.step:
                logger.warning("Step should not go backwards")
            self.step = step
        else:
            self.step += 1

    def build_metric_payload(self, payload: Dict[str, Any], ts: float):
        fields = payload
        tags = {"step": str(self.step)}

        return V1PlotEntry(
            measurement="run_execution_plot_metric",
            ts=ts,
            tags=tags,
            fields=fields,
        )

    def build_media_payload(self, payload: Dict[str, Any], ts: float):
        fields = payload
        tags = {"step": str(self.step)}

        return V1PlotEntry(
            measurement="run_execution_plot_file",
            ts=ts,
            tags=tags,
            fields=fields,
        )

    def log_metrics(self, payloads: List[V1PlotEntry]) -> int:
        self.add(payloads)
        return self.step

    def log_media(self, payloads: List[V1PlotEntry]) -> int:
        self.add(payloads)
        return self.step
