# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import abc
from collections.abc import Iterator

import pyarrow as pa

from geneva.apply.task import MapTask, ReadTask
from geneva.debug.logger import ErrorLogger


class BatchApplier(abc.ABC):
    """Interface class for all appliers"""

    @abc.abstractmethod
    def run(
        self,
        read_task: ReadTask,
        map_task: MapTask,
        error_logger: ErrorLogger,
    ) -> Iterator[pa.RecordBatch]:
        """Run the map task on data from ``read_task`` yielding batches one-by-one."""
