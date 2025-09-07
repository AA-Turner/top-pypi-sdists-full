from __future__ import annotations

import inspect
from datetime import timedelta
from typing import Any

import sqlalchemy
from sqlalchemy import asc

from arpakitlib.ar_base_worker_util import BaseWorker
from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_exception_util import exception_to_traceback_str
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDb
from arpakitlib.ar_type_util import raise_for_type
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM, StoryLogDBM


class OperationExecutorWorker(BaseWorker):

    def __init__(
            self,
            *,
            sqlalchemy_db: SQLAlchemyDb,
            filter_operation_types: str | list[str] | None = None,
            filter_operation_markers: str | list[str] | None = None,
            startup_funcs: list[Any] | None = None,
            data: dict[str, Any] | None = None,
    ):
        super().__init__(
            timeout_after_run=timedelta(seconds=0.01),
            timeout_after_error_in_run=timedelta(seconds=0.1),
            startup_funcs=startup_funcs,
            data=data
        )

        raise_for_type(sqlalchemy_db, SQLAlchemyDb)
        self.sqlalchemy_db = sqlalchemy_db

        if isinstance(filter_operation_types, str):
            filter_operation_types = [filter_operation_types]
        self.filter_operation_types = filter_operation_types

        if isinstance(filter_operation_markers, str):
            filter_operation_markers = [filter_operation_markers]
        self.filter_operation_markers = filter_operation_markers

    def sync_execute_operation(self, operation_dbm: OperationDBM):
        if operation_dbm.type == OperationDBM.Types.healthcheck_:
            self._logger.info(f"healthcheck {now_utc_dt()}")
        elif operation_dbm.type == OperationDBM.Types.raise_fake_error_:
            self._logger.error(f"{OperationDBM.Types.raise_fake_error_}")
            raise Exception(f"{OperationDBM.Types.raise_fake_error_}")
        else:
            with self.sqlalchemy_db.new_session() as session:
                operation_dbm: OperationDBM = session.query(
                    OperationDBM
                ).filter(OperationDBM.id == operation_dbm.id).one()
                operation_dbm.output_data = combine_dicts(
                    operation_dbm.output_data,
                    {"warning": f"unknown operation_type = {operation_dbm.type=}"}
                )
                session.commit()
                session.refresh(operation_dbm)
            self._logger.info(f"unknown operation_type, {operation_dbm.id=}, {operation_dbm.type=}")

    async def async_execute_operation(self, *, operation_dbm: OperationDBM):
        if operation_dbm.type == OperationDBM.Types.healthcheck_:
            self._logger.info(f"healthcheck {now_utc_dt()}")
        elif operation_dbm.type == OperationDBM.Types.raise_fake_error_:
            self._logger.error(f"{OperationDBM.Types.raise_fake_error_}")
            raise Exception(f"{OperationDBM.Types.raise_fake_error_}")
        else:
            async with self.sqlalchemy_db.new_async_session() as session:
                result = await session.execute(
                    sqlalchemy.select(OperationDBM).filter(OperationDBM.id == operation_dbm.id)
                )
                operation_dbm: OperationDBM = result.scalar_one()
                operation_dbm.output_data = combine_dicts(
                    operation_dbm.output_data,
                    {"warning": f"unknown operation_type = {operation_dbm.type}"}
                )
                await session.commit()
                await session.refresh(operation_dbm)
            self._logger.info(f"unknown operation_type, {operation_dbm.id=}, {operation_dbm.type=}")

    def sync_run(self):
        # 1
        with self.sqlalchemy_db.new_session() as sync_session:
            query = (
                sync_session
                .query(OperationDBM)
                .filter(OperationDBM.status == OperationDBM.Statuses.waiting_for_execution)
            )
            if self.filter_operation_types is not None:
                query = query.filter(OperationDBM.type.in_(self.filter_operation_types))
            if self.filter_operation_markers is not None:
                query = query.filter(OperationDBM.marker.in_(self.filter_operation_markers))
            query = query.with_for_update()
            query = query.order_by(asc(OperationDBM.creation_dt))
            operation_dbm: OperationDBM | None = query.first()
            if operation_dbm is None:
                return
            operation_dbm.execution_start_dt = now_utc_dt()
            operation_dbm.status = OperationDBM.Statuses.executing
            operation_dbm.output_data = combine_dicts(
                operation_dbm.output_data,
                {
                    self.worker_fullname: True,
                    f"{inspect.currentframe().f_code.co_name}": True
                }
            )
            sync_session.commit()
            sync_session.refresh(operation_dbm)

        # 2
        self._logger.info(
            f"start execute_operation"
            f", operation_id={operation_dbm.id}"
            f", operation_type={operation_dbm.type})"
            f", worker_fullname={self.worker_fullname}"
        )
        exception_in_execute_operation: Exception | None = None
        try:
            self.sync_execute_operation(operation_dbm=operation_dbm)
        except Exception as exception:
            self._logger.exception(
                f"exception in execute_operation"
                f", operation_id={operation_dbm.id}"
                f", operation_type={operation_dbm.type}"
                f", worker_fullname={self.worker_fullname}",
            )
            exception_in_execute_operation = exception

        # 3
        with self.sqlalchemy_db.new_session() as sync_session:
            operation_dbm: OperationDBM = (
                sync_session.query(OperationDBM).with_for_update().filter(OperationDBM.id == operation_dbm.id).one()
            )
            operation_dbm.execution_finish_dt = now_utc_dt()
            if exception_in_execute_operation is not None:
                operation_dbm.status = OperationDBM.Statuses.executed_with_error
                operation_dbm.error_data = combine_dicts(
                    operation_dbm.error_data,
                    {
                        "exception_in_execute_operation": str(exception_in_execute_operation),
                        "traceback_in_execute_operation": exception_to_traceback_str(
                            exception=exception_in_execute_operation
                        ),
                    }
                )
            else:
                operation_dbm.status = OperationDBM.Statuses.executed_without_error
            sync_session.commit()
            sync_session.refresh(operation_dbm)
        self._logger.info(
            f"finish execute_operation"
            f", operation_id={operation_dbm.id}"
            f", operation_type={operation_dbm.type}"
            f", worker_fullname={self.worker_fullname}"
        )

        # 4
        if exception_in_execute_operation is not None:
            with self.sqlalchemy_db.new_session() as sync_session:
                story_log_dbm = StoryLogDBM(
                    level=StoryLogDBM.Levels.error,
                    type=StoryLogDBM.Types.error_in_execute_operation,
                    title=(
                        f"error in execute_operation"
                        f", operation_id={operation_dbm.id}"
                        f", operation_type={operation_dbm.type}"
                    ),
                    extra_data={
                        "operation_id": operation_dbm.id,
                        "operation_type": operation_dbm.type,
                    }
                )
                sync_session.add(story_log_dbm)
                sync_session.commit()
                sync_session.refresh(story_log_dbm)

    async def async_run(self):
        # 1
        async with self.sqlalchemy_db.new_async_session() as async_session:
            query = (
                sqlalchemy.select(OperationDBM)
                .filter(OperationDBM.status == OperationDBM.Statuses.waiting_for_execution)
            )
            if self.filter_operation_types is not None:
                query = query.filter(OperationDBM.type.in_(self.filter_operation_types))
            if self.filter_operation_markers is not None:
                query = query.filter(OperationDBM.marker.in_(self.filter_operation_markers))
            query = query.order_by(asc(OperationDBM.creation_dt)).with_for_update()

            result = await async_session.execute(query)
            operation_dbm = result.scalars().first()
            if operation_dbm is None:
                return

            operation_dbm.execution_start_dt = now_utc_dt()
            operation_dbm.status = OperationDBM.Statuses.executing
            operation_dbm.output_data = combine_dicts(
                operation_dbm.output_data,
                {
                    self.worker_fullname: True,
                    f"{inspect.currentframe().f_code.co_name}": True
                }
            )
            await async_session.commit()
            await async_session.refresh(operation_dbm)

        # 2
        self._logger.info(
            f"start execute_operation"
            f", operation_id={operation_dbm.id}"
            f", operation_type={operation_dbm.type})"
            f", worker_fullname={self.worker_fullname}"
        )
        exception_in_execute_operation = None
        try:
            await self.async_execute_operation(operation_dbm=operation_dbm)
        except Exception as exception:
            self._logger.exception(
                f"exception in execute_operation"
                f", operation_id={operation_dbm.id}"
                f", operation_type={operation_dbm.type}"
                f", worker_fullname={self.worker_fullname}",
            )
            exception_in_execute_operation = exception

        # 3
        async with self.sqlalchemy_db.new_async_session() as async_session:
            result = await async_session.execute(
                sqlalchemy.select(OperationDBM).filter(OperationDBM.id == operation_dbm.id).with_for_update()
            )
            operation_dbm = result.scalars().one()
            operation_dbm.execution_finish_dt = now_utc_dt()
            if exception_in_execute_operation is not None:
                operation_dbm.status = OperationDBM.Statuses.executed_with_error
                operation_dbm.error_data = combine_dicts(
                    {
                        "exception_in_execute_operation": str(exception_in_execute_operation),
                        "traceback_in_execute_operation": exception_to_traceback_str(
                            exception=exception_in_execute_operation
                        )
                    },
                    operation_dbm.error_data
                )
            else:
                operation_dbm.status = OperationDBM.Statuses.executed_without_error
            await async_session.commit()
            await async_session.refresh(operation_dbm)
        self._logger.info(
            f"finish execute_operation"
            f", operation_id={operation_dbm.id}"
            f", operation_type={operation_dbm.type}"
            f", worker_fullname={self.worker_fullname}"
        )

        # 4
        if exception_in_execute_operation is not None:
            async with self.sqlalchemy_db.new_async_session() as async_session:
                story_log_dbm = StoryLogDBM(
                    level=StoryLogDBM.Levels.error,
                    type=StoryLogDBM.Types.error_in_execute_operation,
                    title=(
                        f"error in execute_operation"
                        f", operation_id={operation_dbm.id}"
                        f", operation_type={operation_dbm.type}"
                    ),
                    extra_data={
                        "operation_id": operation_dbm.id,
                        "operation_type": operation_dbm.type,
                    }
                )
                async_session.add(story_log_dbm)
                await async_session.commit()
                await async_session.refresh(story_log_dbm)


def create_operation_executor_worker(
        *,
        filter_operation_types: str | list[str] | None = None,
        filter_operation_markers: str | list[str] | None = None,
        startup_funcs: list[Any] | None = None
) -> OperationExecutorWorker:
    return OperationExecutorWorker(
        sqlalchemy_db=get_cached_sqlalchemy_db(),
        filter_operation_types=filter_operation_types,
        filter_operation_markers=filter_operation_markers,
        startup_funcs=startup_funcs
    )
