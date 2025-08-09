import asyncio
import inspect
import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from arpakitlib.ar_exception_util import exception_to_traceback_str
from project.core.util import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM

_logger = logging.getLogger(__name__)


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
) -> Any:
    if func_args is None:
        func_args = tuple()
    if func_kwargs is None:
        func_kwargs = {}
    if story_log_extra_data is None:
        story_log_extra_data = {}

    try:
        return func(*func_args, **func_kwargs)
    except Exception as exception:
        _logger.error(f"Error in {func.__name__}", exc_info=True)

        if story_log_title is None:
            story_log_title = f"Error in func {func.__name__}: {type(exception).__name__}: {exception}"
        story_log_extra_data.update({
            "exception": str(exception),
            "exception_traceback": exception_to_traceback_str(exception=exception),
            "exception_type_name": type(exception).__name__,
            "func_name": inspect.currentframe().f_code.co_name
        })

        if session_ is not None:
            story_log_dbm = StoryLogDBM(
                level=story_log_level,
                type=story_log_type,
                title=story_log_title,
                extra_data=story_log_extra_data
            )
            session_.add(story_log_dbm)
            session_.commit()
        else:
            with get_cached_sqlalchemy_db().new_session() as session:
                story_log_dbm = StoryLogDBM(
                    level=story_log_level,
                    type=story_log_type,
                    title=story_log_title,
                    extra_data=story_log_extra_data
                )
                session.add(story_log_dbm)
                session.commit()

        raise exception


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
) -> Any:
    if async_func_args is None:
        async_func_args = ()
    if async_func_kwargs is None:
        async_func_kwargs = {}
    if story_log_extra_data is None:
        story_log_extra_data = {}

    try:
        return await async_func(*async_func_args, **async_func_kwargs)
    except Exception as exception:
        _logger.error(f"Async error in {async_func.__name__}", exc_info=True)

        if story_log_title is None:
            story_log_title = f"Async error in func {async_func.__name__}: {type(exception).__name__}: {exception}"

        story_log_extra_data.update({
            "exception": str(exception),
            "exception_traceback": exception_to_traceback_str(exception=exception),
            "exception_type_name": type(exception).__name__,
            "func_name": inspect.currentframe().f_code.co_name
        })

        if async_session_ is not None:
            story_log_dbm = StoryLogDBM(
                level=story_log_level,
                type=story_log_type,
                title=story_log_title,
                extra_data=story_log_extra_data
            )
            async_session_.add(story_log_dbm)
            await async_session_.commit()
        else:
            async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                story_log_dbm = StoryLogDBM(
                    level=story_log_level,
                    type=story_log_type,
                    title=story_log_title,
                    extra_data=story_log_extra_data
                )
                async_session.add(story_log_dbm)
                await async_session.commit()

        raise exception


async def __async_example():
    setup_logging()

    def hello_world():
        print(inspect.currentframe().f_code.co_name)
        # raise ValueError("1111111")

    print(hello_world())

    # async def async_hello_world():
    #     print(1)
    #     raise ValueError("1111111")

    # sync_execute_with_story_log(
    #     func=hello_world
    # )
    # await async_execute_with_story_log(
    #     func=async_hello_world
    # )


if __name__ == '__main__':
    asyncio.run(__async_example())
