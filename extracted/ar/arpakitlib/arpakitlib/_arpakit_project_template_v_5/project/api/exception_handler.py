import asyncio
import inspect
import logging
from contextlib import suppress
from typing import Any, Callable

import fastapi
import starlette.exceptions

from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_exception_util import exception_to_traceback_str
from arpakitlib.ar_func_util import raise_if_not_async_func, is_async_func, is_sync_func
from project.api.api_error_codes import APIErrorCodes
from project.api.api_exception import APIException
from project.api.response import APIJSONResponse
from project.api.schema.out.common.error import ErrorCommonSO
from project.business_service.exception import BaseBusinessServiceException
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import StoryLogDBM

_logger = logging.getLogger(__name__)


def create_api_exception_handler(
        *,
        funcs_before: list[Callable | None] | None = None,
        async_funcs_after: list[Callable | None] | None = None
) -> Callable:
    if funcs_before is None:
        funcs_before = []
    funcs_before = [v for v in funcs_before if v is not None]

    if async_funcs_after is None:
        async_funcs_after = []
    async_funcs_after = [v for v in async_funcs_after if v is not None]

    async def async_func(
            request: fastapi.requests.Request,
            exception: Exception
    ) -> APIJSONResponse:
        status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR

        error_common_so = ErrorCommonSO(
            has_error=True,
            error_code=APIErrorCodes.unknown_error,
            error_data={
                "exception_type": str(type(exception)),
                "exception_str": str(exception),
                "request.method": str(request.method),
                "request.url": str(request.url)
            }
        )

        if isinstance(exception, APIException):
            status_code = exception.status_code
            old_error_data = error_common_so.error_data
            error_common_so = exception.error_common_so
            error_common_so.error_data = combine_dicts(old_error_data, error_common_so.error_data)

        elif isinstance(exception, BaseBusinessServiceException):
            if exception.data_api_error_status_code is not None:
                status_code = exception.data_api_error_status_code
            if exception.data_api_error_common_so is not None:
                error_common_so = exception.data_api_error_common_so

        elif (
                isinstance(exception, fastapi.exceptions.HTTPException)
                or isinstance(exception, starlette.exceptions.HTTPException)
        ):
            status_code = exception.status_code
            if status_code in (fastapi.status.HTTP_403_FORBIDDEN, fastapi.status.HTTP_401_UNAUTHORIZED):
                error_common_so.error_code = APIErrorCodes.cannot_authorize
            elif status_code == fastapi.status.HTTP_404_NOT_FOUND:
                error_common_so.error_code = APIErrorCodes.not_found
            else:
                status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
            with suppress(Exception):
                error_common_so.error_data["exception.detail"] = exception.detail

        elif isinstance(exception, fastapi.exceptions.RequestValidationError):
            status_code = fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
            error_common_so.error_code = APIErrorCodes.error_in_request
            with suppress(Exception):
                error_common_so.error_data["exception.errors"] = str(exception.errors()) if exception.errors() else {}

        else:
            status_code = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
            error_common_so.error_code = APIErrorCodes.unknown_error

        if error_common_so.error_code is not None:
            error_common_so.error_code = error_common_so.error_code.upper().replace(" ", "_").strip()

        if error_common_so.error_specification_code is not None:
            error_common_so.error_specification_code = (
                error_common_so.error_specification_code.upper().replace(" ", "_").strip()
            )

        if error_common_so.error_code == APIErrorCodes.not_found:
            status_code = fastapi.status.HTTP_404_NOT_FOUND

        if error_common_so.error_code == APIErrorCodes.cannot_authorize:
            status_code = fastapi.status.HTTP_401_UNAUTHORIZED

        error_common_so.error_data["status_code"] = status_code

        # funcs_before

        _transmitted_kwargs = {}
        for func_before in funcs_before:
            if is_async_func(func_before):
                try:
                    await func_before(
                        request=request,
                        status_code=status_code,
                        error_common_so=error_common_so,
                        exception=exception,
                        transmitted_kwargs=_transmitted_kwargs
                    )
                except Exception as exception_:
                    _logger.exception(exception_)
                    raise exception_
            elif is_sync_func(func_before):
                try:
                    func_before(
                        request=request,
                        status_code=status_code,
                        error_common_so=error_common_so,
                        exception=exception,
                        transmitted_kwargs=_transmitted_kwargs
                    )
                except Exception as exception_:
                    _logger.exception(exception_)
                    raise exception_
            else:
                raise TypeError("unknown func_before type")

        # async_funcs_after

        for async_func_after in async_funcs_after:
            raise_if_not_async_func(async_func_after)
            _ = asyncio.create_task(async_func_after(
                request=request, status_code=status_code, error_common_so=error_common_so, exception=exception
            ))

        return APIJSONResponse(
            content=error_common_so,
            status_code=status_code
        )

    return async_func


def logging_func_before_in_api_exception_handler(
        *,
        ignore_api_error_codes: list[str] | None = None,
        ignore_status_codes: list[int] | None = None,
        ignore_exception_types: list[type[Exception]] | None = None
) -> Callable:
    current_func_name = inspect.currentframe().f_code.co_name

    def func(
            *,
            request: fastapi.requests.Request,
            status_code: int,
            error_common_so: ErrorCommonSO,
            exception: Exception,
            transmitted_kwargs: dict[str, Any],
            **kwargs
    ):
        transmitted_kwargs[current_func_name] = now_utc_dt()

        if ignore_api_error_codes is not None and error_common_so.error_code in ignore_api_error_codes:
            return

        if ignore_status_codes is not None and status_code in ignore_status_codes:
            return

        if ignore_exception_types is not None and (
                exception in ignore_exception_types or type(exception) in ignore_exception_types
        ):
            return

        if isinstance(exception, APIException):
            if exception.kwargs_.get("logging_full_error") is False:
                return

        _logger.exception(exception)

    return func


def create_story_log_func_before_in_api_exception_handler(
        *,
        ignore_api_error_codes: list[str] | None = None,
        ignore_status_codes: list[int] | None = None,
        ignore_exception_types: list[type[Exception]] | None = None,
) -> Callable:
    current_func_name = inspect.currentframe().f_code.co_name

    async def async_func(
            *,
            request: fastapi.requests.Request,
            status_code: int,
            error_common_so: ErrorCommonSO,
            exception: Exception,
            transmitted_kwargs: dict[str, Any],
            **kwargs
    ):
        transmitted_kwargs[current_func_name] = now_utc_dt()

        if ignore_api_error_codes is not None and error_common_so.error_code in ignore_api_error_codes:
            return

        if ignore_status_codes is not None and status_code in ignore_status_codes:
            return

        if ignore_exception_types is not None and (
                exception in ignore_exception_types or type(exception) in ignore_exception_types
        ):
            return

        if isinstance(exception, APIException):
            if exception.kwargs_.get("create_story_log") is False:
                return

        async with get_cached_sqlalchemy_db().new_async_session() as session:
            story_log_dbm = StoryLogDBM(
                level=StoryLogDBM.Levels.error,
                type=StoryLogDBM.Types.error_in_api,
                title=f"{status_code}, {str(type(exception))}, {str(exception)}",
                extra_data={
                    "exception_type": str(type(exception)),
                    "exception_str": str(exception),
                    "error_common_so": error_common_so.model_dump(),
                    "exception_traceback": exception_to_traceback_str(exception=exception)
                }
            )
            session.add(story_log_dbm)
            await session.commit()
            await session.refresh(story_log_dbm)

        error_common_so.error_data.update({"story_log_long_id": story_log_dbm.long_id})
        transmitted_kwargs["story_log_id"] = story_log_dbm.id

        return

    return async_func


def get_exception_handler() -> Callable:
    funcs_before = []
    async_funcs_after = []

    funcs_before.append(
        logging_func_before_in_api_exception_handler(
            ignore_api_error_codes=[
                APIErrorCodes.cannot_authorize,
                APIErrorCodes.error_in_request,
                APIErrorCodes.not_found
            ],
            ignore_status_codes=[
                fastapi.status.HTTP_401_UNAUTHORIZED,
                fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
                fastapi.status.HTTP_404_NOT_FOUND
            ],
            ignore_exception_types=[
                fastapi.exceptions.RequestValidationError
            ],
        )
    )

    if get_cached_sqlalchemy_db() is not None:
        funcs_before.append(
            create_story_log_func_before_in_api_exception_handler(
                ignore_api_error_codes=[
                    APIErrorCodes.cannot_authorize,
                    APIErrorCodes.error_in_request,
                    APIErrorCodes.not_found
                ],
                ignore_status_codes=[
                    fastapi.status.HTTP_401_UNAUTHORIZED,
                    fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
                    fastapi.status.HTTP_404_NOT_FOUND
                ],
                ignore_exception_types=[
                    fastapi.exceptions.RequestValidationError
                ],
            )
        )

    return create_api_exception_handler(
        funcs_before=funcs_before,
        async_funcs_after=async_funcs_after
    )


def add_exception_handler_to_api_app(*, app: fastapi.FastAPI) -> fastapi.FastAPI:
    exception_handler = get_exception_handler()

    app.add_exception_handler(
        exc_class_or_status_code=Exception,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=ValueError,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.RequestValidationError,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=fastapi.exceptions.HTTPException,
        handler=exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=starlette.exceptions.HTTPException,
        handler=exception_handler
    )

    return app
