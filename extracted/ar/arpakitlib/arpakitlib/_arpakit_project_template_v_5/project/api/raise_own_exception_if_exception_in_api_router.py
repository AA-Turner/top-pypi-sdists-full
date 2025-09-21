from typing import Any

import fastapi
from arpakitlib.ar_raise_own_exception_if_exception import raise_own_exception_if_exception

from project.api.api_exception import APIException
from project.api.schema.out.common.error import ErrorCommonSO


def raise_own_exception_if_exception_in_api_router(
        *,
        status_code: int = fastapi.status.HTTP_400_BAD_REQUEST,
        error_common_so: ErrorCommonSO | None = None,
        kwargs_: dict[str, Any] | None = None,
        kwargs_create_story_log: bool = True,
        kwargs_logging_full_error: bool = True,
):
    """Обертка над декоратором raise_own_exception_if_exception"""

    def decorator(func):
        # просто возвращаем результат применения исходного декоратора
        return raise_own_exception_if_exception(
            catching_exceptions=Exception,
            own_exception=APIException,
            kwargs_in_own_exception={raise_own_exception_if_exception_in_api_router.__name__: True},
            forward_kwargs_in_own_exception={
                "status_code": status_code,
                "error_common_so": error_common_so,
                "kwargs_": kwargs_,
                "kwargs_create_story_log": kwargs_create_story_log,
                "kwargs_logging_full_error": kwargs_logging_full_error,
            }
        )(func)

    return decorator
