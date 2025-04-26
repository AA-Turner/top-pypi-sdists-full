import logging
from datetime import datetime

from tecton_core import conf
from tecton_core.query.dialect import Dialect
from tecton_proto.materialization.job_metadata__client_pb2 import TectonManagedStage


logger = logging.getLogger(__name__)


class QueryTreeMonitor:
    def create_stage(self, type_: TectonManagedStage.StageType, description: str) -> int:
        """Returns stage identifier"""

    def set_query(self, stage_id: int, sql: str) -> None:
        pass

    def update_progress(self, stage_id: int, progress: float) -> None:
        pass

    def set_failed(self, stage_id: int, user_error: bool) -> None:
        pass

    def set_completed(self, stage_id: int) -> None:
        pass

    def set_overall_state(self, state: TectonManagedStage.State) -> None:
        pass


class DebugOutput(QueryTreeMonitor):
    def __init__(self):
        self.start_time = None
        self.step = None
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")

    def create_stage(self, type_: TectonManagedStage.StageType, description: str) -> int:
        self.start_time = datetime.now()
        self.step = description
        if self.is_debug:
            logger.warning(f"------------- Executing stage: {description} -------------")
        return 0

    def set_completed(self, stage_id: int) -> None:
        stage_done_time = datetime.now()
        if self.is_debug:
            logger.warning(f"{self.step} took time (sec): {(stage_done_time - self.start_time).total_seconds()}")

    def set_failed(self, stage_id: int, user_error: bool) -> None:
        return self.set_completed(stage_id)


def get_stage_type_for_dialect(dialect: Dialect) -> TectonManagedStage.StageType:
    if dialect == Dialect.SNOWFLAKE:
        return TectonManagedStage.StageType.SNOWFLAKE
    elif dialect == Dialect.BIGQUERY:
        return TectonManagedStage.StageType.BIGQUERY

    return TectonManagedStage.StageType.PYTHON
