from __future__ import annotations

import inspect
import logging
from functools import wraps
from typing import Any, Callable, Awaitable, Tuple, TypeVar, ParamSpec, cast

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

PARAMS_SPEC = ParamSpec("PARAMS_SPEC")
RESULT_SPEC = TypeVar("RESULT_SPEC")

_logger = logging.getLogger(__name__)

def raise_own_exception_if_exception(
        *,
        catching_exceptions: type[BaseException] | Tuple[type[BaseException], ...] | None = Exception,
        except_catching_exceptions: type[BaseException] | Tuple[type[BaseException], ...] | None = None,
        own_exception: type[Exception],
        kwargs_in_own_exception: dict[str, Any] | None = None,
        forward_kwargs_in_own_exception: dict[str, Any] | None = None,
) -> (
        Callable[[Callable[PARAMS_SPEC, RESULT_SPEC] | Callable[PARAMS_SPEC, Awaitable[RESULT_SPEC]]],
        Callable[PARAMS_SPEC, RESULT_SPEC] | Callable[PARAMS_SPEC, Awaitable[RESULT_SPEC]]]
):
    """
    Ловит любые Exception и оборачивает в own_exception(**kwargs_).
    Исключения из except_exceptions пропускает как есть.
    Работает и для sync, и для async функций.
    """

    # normalize catching_exceptions -> tuple[type, ...]
    if catching_exceptions is None:
        catching_exceptions = (Exception,)
    elif isinstance(catching_exceptions, tuple):
        catching_exceptions = catching_exceptions
    else:
        catching_exceptions = (catching_exceptions,)

    # Нормализуем except_exceptions к кортежу типов
    if except_catching_exceptions is None:
        except_catching_exceptions = ()
    elif isinstance(except_catching_exceptions, tuple):
        except_catching_exceptions = except_catching_exceptions
    elif except_catching_exceptions:
        except_catching_exceptions = (except_catching_exceptions,)
    else:
        except_catching_exceptions = ()

    if kwargs_in_own_exception is not None:
        kwargs_in_own_exception = dict(kwargs_in_own_exception or {})
        kwargs_in_own_exception["catching_exceptions"] = catching_exceptions
        kwargs_in_own_exception["except_catching_exceptions"] = except_catching_exceptions
        kwargs_in_own_exception["own_exception"] = own_exception

    # Если явно передали пустой набор для ловли — возвращаем функцию как есть
    if not catching_exceptions:
        def _passthrough_decorator(func):
            return func

        return _passthrough_decorator

    def decorator(func: Callable[PARAMS_SPEC, RESULT_SPEC] | Callable[PARAMS_SPEC, Awaitable[RESULT_SPEC]]):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: PARAMS_SPEC.args, **kwargs: PARAMS_SPEC.kwargs) -> RESULT_SPEC:
                try:
                    return await cast(Callable[PARAMS_SPEC, Awaitable[RESULT_SPEC]], func)(*args, **kwargs)
                except catching_exceptions as caught_exception:  # ловим ТОЛЬКО нужные типы
                    if except_catching_exceptions and isinstance(caught_exception, except_catching_exceptions):
                        raise  # пропускаем как есть
                    if kwargs_in_own_exception is not None:
                        copied_kwargs_in_own_exception = kwargs_in_own_exception.copy()
                        copied_kwargs_in_own_exception["caught_exception"] = caught_exception
                        copied_kwargs_in_own_exception["caught_exception_type"] = str(type(caught_exception))
                        copied_kwargs_in_own_exception["caught_exception_str"] = str(caught_exception)
                    try:
                        _kwargs = {}
                        if kwargs_in_own_exception is not None:
                            _kwargs.update({"kwargs_in_own_exception": copied_kwargs_in_own_exception})
                        if forward_kwargs_in_own_exception is not None:
                            _kwargs.update(forward_kwargs_in_own_exception)
                        raise own_exception(**_kwargs) from caught_exception
                    except TypeError as exception:
                        _logger.warning(exception)
                        raise own_exception() from caught_exception

            return cast(Callable[PARAMS_SPEC, Awaitable[RESULT_SPEC]], async_wrapper)

        @wraps(func)
        def wrapper(*args: PARAMS_SPEC.args, **kwargs: PARAMS_SPEC.kwargs) -> RESULT_SPEC:
            try:
                return cast(Callable[PARAMS_SPEC, RESULT_SPEC], func)(*args, **kwargs)
            except catching_exceptions as caught_exception:
                if except_catching_exceptions and isinstance(caught_exception, except_catching_exceptions):
                    raise
                if kwargs_in_own_exception is not None:
                    copied_kwargs_in_own_exception = kwargs_in_own_exception.copy()
                    copied_kwargs_in_own_exception["caught_exception"] = caught_exception
                    copied_kwargs_in_own_exception["caught_exception_type"] = str(type(caught_exception))
                    copied_kwargs_in_own_exception["caught_exception_str"] = str(caught_exception)
                try:
                    _kwargs = {}
                    if kwargs_in_own_exception is not None:
                        _kwargs.update({"kwargs_in_own_exception": copied_kwargs_in_own_exception})
                    if forward_kwargs_in_own_exception is not None:
                        _kwargs.update(forward_kwargs_in_own_exception)
                    raise own_exception(**_kwargs) from caught_exception
                except TypeError as exception:
                    _logger.warning(exception)
                    raise own_exception() from caught_exception

        return cast(Callable[PARAMS_SPEC, RESULT_SPEC], wrapper)

    return decorator
