import asyncio
import inspect
import logging
from typing import Any

from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from arpakitlib.ar_exception_util import exception_to_traceback_str
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM

_logger = logging.getLogger(__name__)


class ExecuteWithStoryLogRes(BaseModel):
    func_res: Any = None
    story_log_dbm: StoryLogDBM | None = None
    exception: Exception | None = None

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    def raise_if_exception(self):
        if self.exception is not None:
            raise self.exception


def sync_execute_with_story_log(
        func,
        *,
        func_args: tuple[Any] | None = None,
        func_kwargs: dict[Any, Any] | None = None,
        session_: Session | None = None,
        story_log_level: str = StoryLogDBM.Levels.error,
        story_log_type: str = StoryLogDBM.Types.error_in_execute_with_story_log,
        story_log_title: str | None = None,
        story_log_extra_data: dict[Any, Any] | None = None,
        raise_if_exception: bool = False
) -> ExecuteWithStoryLogRes:
    if func_args is None:
        func_args = tuple()
    if func_kwargs is None:
        func_kwargs = {}
    if story_log_extra_data is None:
        story_log_extra_data = {}
    story_log_extra_data = story_log_extra_data.copy()

    execute_with_story_log_res = ExecuteWithStoryLogRes()

    try:
        execute_with_story_log_res.func_res = func(*func_args, **func_kwargs)
        return execute_with_story_log_res
    except Exception as exception:
        _logger.error(f"Error in {func.__name__}", exc_info=True)

        execute_with_story_log_res.exception = exception

        if story_log_title is None:
            story_log_title = f"Error in func {func.__name__}: {type(exception).__name__}: {exception}"
        story_log_extra_data.update({
            "exception": str(exception),
            "exception_traceback": exception_to_traceback_str(exception=exception),
            "exception_type_name": type(exception).__name__,
            "wrapper_func_name": inspect.currentframe().f_code.co_name,
            "called_func_name": func.__name__
        })

        if session_ is not None:
            execute_with_story_log_res.story_log_dbm = StoryLogDBM(
                level=story_log_level,
                type=story_log_type,
                title=story_log_title,
                extra_data=story_log_extra_data
            )
            session_.add(execute_with_story_log_res.story_log_dbm)
            session_.commit()
        else:
            with get_cached_sqlalchemy_db().new_session() as session:
                execute_with_story_log_res.story_log_dbm = StoryLogDBM(
                    level=story_log_level,
                    type=story_log_type,
                    title=story_log_title,
                    extra_data=story_log_extra_data
                )
                session.add(execute_with_story_log_res.story_log_dbm)
                session.commit()

        if raise_if_exception:
            raise

        return execute_with_story_log_res


async def async_execute_with_story_log(
        async_func,
        *,
        async_func_args: tuple[Any] | None = None,
        async_func_kwargs: dict[Any, Any] | None = None,
        async_session_: AsyncSession | None = None,
        story_log_level: str = StoryLogDBM.Levels.error,
        story_log_type: str = StoryLogDBM.Types.error_in_execute_with_story_log,
        story_log_title: str | None = None,
        story_log_extra_data: dict[Any, Any] | None = None,
        raise_if_exception: bool = False
) -> ExecuteWithStoryLogRes:
    if async_func_args is None:
        async_func_args = ()
    if async_func_kwargs is None:
        async_func_kwargs = {}
    if story_log_extra_data is None:
        story_log_extra_data = {}
    story_log_extra_data = story_log_extra_data.copy()

    execute_with_story_log_res = ExecuteWithStoryLogRes()

    try:
        execute_with_story_log_res.func_res = await async_func(*async_func_args, **async_func_kwargs)
        return execute_with_story_log_res
    except Exception as exception:
        _logger.error(f"Async error in {async_func.__name__}", exc_info=True)

        execute_with_story_log_res.exception = exception

        if story_log_title is None:
            story_log_title = f"Async error in func {async_func.__name__}: {type(exception).__name__}: {exception}"

        story_log_extra_data.update({
            "exception": str(exception),
            "exception_traceback": exception_to_traceback_str(exception=exception),
            "exception_type_name": type(exception).__name__,
            "wrapper_func_name": inspect.currentframe().f_code.co_name,
            "called_func_name": async_func.__name__
        })

        if async_session_ is not None:
            execute_with_story_log_res.story_log_dbm = StoryLogDBM(
                level=story_log_level,
                type=story_log_type,
                title=story_log_title,
                extra_data=story_log_extra_data
            )
            async_session_.add(execute_with_story_log_res.story_log_dbm)
            await async_session_.commit()
        else:
            async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                execute_with_story_log_res.story_log_dbm = StoryLogDBM(
                    level=story_log_level,
                    type=story_log_type,
                    title=story_log_title,
                    extra_data=story_log_extra_data
                )
                async_session.add(execute_with_story_log_res.story_log_dbm)
                await async_session.commit()

        if raise_if_exception:
            raise

        return execute_with_story_log_res


async def __async_example():
    pass


if __name__ == '__main__':
    asyncio.run(__async_example())
