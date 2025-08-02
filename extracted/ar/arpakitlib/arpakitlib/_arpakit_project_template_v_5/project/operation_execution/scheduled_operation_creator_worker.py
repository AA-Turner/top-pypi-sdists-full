from datetime import timedelta
from typing import Any

from arpakitlib.ar_base_worker_util import BaseWorker
from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from arpakitlib.ar_type_util import raise_for_type
from project.operation_execution.scheduled_operations import ScheduledOperation, get_scheduled_operations
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM


class ScheduledOperationCreatorWorker(BaseWorker):
    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDb,
            scheduled_operations: ScheduledOperation | list[ScheduledOperation] | None = None,
            startup_funcs: list[Any] | None = None
    ):
        super().__init__(
            timeout_after_run=timedelta(seconds=0.1),
            timeout_after_error_in_run=timedelta(seconds=0.1),
            startup_funcs=startup_funcs
        )

        raise_for_type(sqlalchemy_db, SQLAlchemyDb)
        self.sqlalchemy_db = sqlalchemy_db

        if scheduled_operations is None:
            scheduled_operations = []
        if isinstance(scheduled_operations, ScheduledOperation):
            scheduled_operations = [scheduled_operations]
        raise_for_type(scheduled_operations, list)
        self.scheduled_operations = scheduled_operations

    def sync_run(self):
        timeout = None

        for scheduled_operation in self.scheduled_operations:

            if not scheduled_operation.is_time_func():
                continue

            with self.sqlalchemy_db.new_session() as session:
                operation_dbm = OperationDBM(
                    type=scheduled_operation.type,
                    input_data=transfer_data_to_json_str_to_data(
                        data=scheduled_operation.input_data,
                        fast=True
                    ),
                    status=OperationDBM.Statuses.waiting_for_execution
                )
                session.add(operation_dbm)
                session.commit()
                session.refresh(operation_dbm)
            self._logger.info(
                f"scheduled operation was created"
                f", operation_id={operation_dbm.id}"
                f", operation_type={operation_dbm.type}"
            )

            if scheduled_operation.timeout_after_creation is not None:
                if timeout is not None:
                    if scheduled_operation.timeout_after_creation > timeout:
                        timeout = scheduled_operation.timeout_after_creation
                else:
                    timeout = scheduled_operation.timeout_after_creation

        if timeout is not None:
            sync_safe_sleep(n=timeout)

    async def async_run(self):
        timeout: timedelta | None = None

        for scheduled_operation in self.scheduled_operations:

            if not scheduled_operation.is_time_func():
                continue

            async with self.sqlalchemy_db.new_async_session() as async_session:
                operation_dbm = OperationDBM(
                    type=scheduled_operation.type,
                    input_data=transfer_data_to_json_str_to_data(
                        data=scheduled_operation.input_data,
                        fast=True
                    ),
                )
                async_session.add(operation_dbm)
                await async_session.commit()
                await async_session.refresh(operation_dbm)
            self._logger.info(
                f"scheduled operation was created"
                f", operation_id={operation_dbm.id}"
                f", operation_type={operation_dbm.type}"
            )

            if scheduled_operation.timeout_after_creation is not None:
                if timeout is not None:
                    if scheduled_operation.timeout_after_creation > timeout:
                        timeout = scheduled_operation.timeout_after_creation
                else:
                    timeout = scheduled_operation.timeout_after_creation

        if timeout is not None:
            await async_safe_sleep(n=timeout)


def create_scheduled_operation_creator_worker() -> ScheduledOperationCreatorWorker:
    return ScheduledOperationCreatorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        scheduled_operations=get_scheduled_operations()
    )
