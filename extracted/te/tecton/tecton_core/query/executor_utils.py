import logging
import uuid
from datetime import datetime

from tecton_core import conf
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage


logger = logging.getLogger(__name__)


class QueryTreeMonitor:
    def create_stage(self, pid: int, staging_node_id: uuid.UUID, description: str) -> int:
        """Returns the index of the stage within the attempt's stage list"""

    def set_query(self, stage_idx: int, sql: str) -> None:
        pass

    def update_progress(self, stage_idx: int, progress: float) -> None:
        pass

    def set_failed(self, stage_idx: int, user_error: bool) -> None:
        pass

    def set_completed(self, stage_idx: int) -> None:
        pass

    def set_overall_state(self, state: TectonManagedStage.State) -> None:
        pass


class DebugOutput(QueryTreeMonitor):
    def __init__(self):
        self.start_time = None
        self.step = None
        self.pid = None
        self.staging_node_id = None
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")

    def create_stage(self, pid: int, staging_node_id: uuid.UUID, description: str) -> int:
        self.start_time = datetime.now()
        self.step = description
        self.pid = pid
        self.staging_node_id = staging_node_id
        if self.is_debug:
            logger.warning(f"------------- [PID: {pid}] Executing stage: {staging_node_id} {description} -------------")
        return 0

    def set_completed(self, stage_id: int) -> None:
        stage_done_time = datetime.now()
        if self.is_debug:
            logger.warning(
                f"[PID: {self.pid}] {self.staging_node_id} {self.step} took time (sec): {(stage_done_time - self.start_time).total_seconds()}"
            )

    def set_failed(self, stage_id: int, user_error: bool) -> None:
        return self.set_completed(stage_id)
