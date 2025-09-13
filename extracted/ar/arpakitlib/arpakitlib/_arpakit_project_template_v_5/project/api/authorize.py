from typing import Callable, Any

import fastapi
import fastapi.exceptions
import fastapi.responses
import fastapi.security
import sqlalchemy
from fastapi import Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import joinedload

from arpakitlib.ar_func_util import is_async_func, is_sync_func
from arpakitlib.ar_json_util import transfer_data_to_json_str_to_data
from project.api.api_error_codes import APIErrorCodes
from project.api.api_exception import APIException
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM, UserTokenDBM


class APIAuthorizeData(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    api_key_string: str | None = None
    user_token_string: str | None = None

    is_api_key_correct: bool | None = None

    api_key_dbm: ApiKeyDBM | None = None
    user_token_dbm: UserTokenDBM | None = None

    prod_mode: bool = False

    extra_data: dict[str, Any] = {}


def api_authorize(
        *,
        middlewares: list[Callable] | None = None
) -> Callable:
    if middlewares is None:
        middlewares = []

    async def async_func(
            *,
            ac: fastapi.security.HTTPAuthorizationCredentials | None = fastapi.Security(
                fastapi.security.HTTPBearer(auto_error=False)
            ),
            api_key_string: str | None = Security(
                APIKeyHeader(name="apikey", auto_error=False)
            ),
            request: fastapi.requests.Request
    ) -> APIAuthorizeData:

        api_auth_data = APIAuthorizeData(
            prod_mode=get_cached_settings().prod_mode
        )

        # parse api_key_string

        api_auth_data.api_key_string = api_key_string

        if not api_auth_data.api_key_string and "api_key" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["api_key"]
        if not api_auth_data.api_key_string and "api-key" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["api-key"]
        if not api_auth_data.api_key_string and "apikey" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["apikey"]
        if not api_auth_data.api_key_string and "api_key_string" in request.headers.keys():
            api_auth_data.api_key_string = request.headers["api_key_string"]

        if not api_auth_data.api_key_string and "api_key" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["api_key"]
        if not api_auth_data.api_key_string and "api-key" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["api-key"]
        if not api_auth_data.api_key_string and "apikey" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["apikey"]
        if not api_auth_data.api_key_string and "api_key_string" in request.query_params.keys():
            api_auth_data.api_key_string = request.query_params["api_key_string"]

        if api_auth_data.api_key_string:
            api_auth_data.api_key_string = api_auth_data.api_key_string.strip()
        if not api_auth_data.api_key_string:
            api_auth_data.api_key_string = None

        # parse user_token_string

        api_auth_data.user_token_string = ac.credentials if ac and ac.credentials and ac.credentials.strip() else None

        if not api_auth_data.user_token_string and "token" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["token"]

        if not api_auth_data.user_token_string and "user_token" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["user_token"]
        if not api_auth_data.user_token_string and "user-token" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["user-token"]
        if not api_auth_data.user_token_string and "usertoken" in request.headers.keys():
            api_auth_data.user_token_string = request.headers["usertoken"]

        if not api_auth_data.user_token_string and "token" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["token"]

        if not api_auth_data.user_token_string and "user_token" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["user_token"]
        if not api_auth_data.user_token_string and "user-token" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["user-token"]
        if not api_auth_data.user_token_string and "usertoken" in request.query_params.keys():
            api_auth_data.user_token_string = request.query_params["usertoken"]

        if api_auth_data.user_token_string:
            api_auth_data.user_token_string = api_auth_data.user_token_string.strip()
        if not api_auth_data.user_token_string:
            api_auth_data.user_token_string = None

        # is_api_key_correct

        if api_auth_data.api_key_string is not None:
            if get_cached_settings().api_correct_api_keys is None:
                api_auth_data.is_api_key_correct = None
            else:
                api_auth_data.is_api_key_correct = (
                        api_auth_data.api_key_string in get_cached_settings().api_correct_api_keys
                )

        # api_key_dbm

        if api_auth_data.api_key_string is not None:
            if get_cached_sqlalchemy_db() is not None:
                async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                    api_auth_data.api_key_dbm = await async_session.scalar(
                        sqlalchemy.select(ApiKeyDBM).where(ApiKeyDBM.value == api_auth_data.api_key_string)
                    )

        # user_token_dbm

        if api_auth_data.user_token_string is not None:
            if get_cached_sqlalchemy_db() is not None:
                async with get_cached_sqlalchemy_db().new_async_session() as async_session:
                    api_auth_data.user_token_dbm = await async_session.scalar(
                        sqlalchemy.select(UserTokenDBM)
                        .options(joinedload(UserTokenDBM.user))
                        .where(UserTokenDBM.value == api_auth_data.user_token_string)
                    )

        # middlewares

        for middleware in middlewares:
            api_auth_data.extra_data[middleware.__name__] = True

        for middleware in middlewares:
            if is_async_func(middleware):
                await middleware(
                    api_auth_data=api_auth_data,
                    request=request
                )
            elif is_sync_func(middleware):
                middleware(
                    api_auth_data=api_auth_data,
                    request=request
                )
            else:
                raise TypeError(f"unknown middleware type, {middleware.__name__}")

        return api_auth_data

    return async_func


def require_prod_mode_api_authorize_middleware():
    def func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if not get_cached_settings().prod_mode:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"prod_mode is required, {get_cached_settings().prod_mode=}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    func.__name__ = require_prod_mode_api_authorize_middleware.__name__

    return func


def require_not_prod_mode_api_authorize_middleware():
    def func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if get_cached_settings().prod_mode:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"not prod_mode is required, {get_cached_settings().prod_mode=}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    func.__name__ = require_not_prod_mode_api_authorize_middleware.__name__

    return func


def require_api_key_string_api_authorize_middleware():
    def func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if api_auth_data.api_key_string is None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description="api_key_string is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    func.__name__ = require_api_key_string_api_authorize_middleware.__name__

    return func


def require_user_token_string_api_authorize_middleware():
    def func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if api_auth_data.user_token_string is None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description="user_token_string is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    func.__name__ = require_user_token_string_api_authorize_middleware.__name__

    return func


def require_correct_api_key_api_authorize_middleware():
    def func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if not api_auth_data.is_api_key_correct:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description="correct api_key_string is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    func.__name__ = require_correct_api_key_api_authorize_middleware.__name__

    return func


def require_api_key_dbm_api_authorize_middleware(*, require_active: bool = True):
    async def async_func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if api_auth_data.api_key_dbm is None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"api_key_dbm is required, {require_active=}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )
        if require_active and not api_auth_data.api_key_dbm.is_active:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"api_key_dbm is required, {require_active=}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    async_func.__name__ = require_api_key_dbm_api_authorize_middleware.__name__

    return async_func


def require_correct_api_key_or_api_key_dbm_api_authorize_middleware(*, require_active_api_key_dbm: bool = True):
    async def async_func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if not api_auth_data.is_api_key_correct and (
                api_auth_data.api_key_dbm is None
                or (require_active_api_key_dbm and not api_auth_data.api_key_dbm.is_active)
        ):
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=(
                    f"correct api_key is required or api_key_dbm is required, {require_active_api_key_dbm=}"
                ),
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    async_func.__name__ = require_correct_api_key_or_api_key_dbm_api_authorize_middleware.__name__

    return async_func


def require_user_token_dbm_api_authorize_middleware(
        *, require_active_user_token: bool = True,
        require_user_roles: list[str] | None = None
):
    async def async_func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if api_auth_data.user_token_dbm is None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"user_token_dbm is required, {require_active_user_token=}, {require_user_roles=}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )
        if require_active_user_token and not api_auth_data.user_token_dbm.is_active:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"user_token_dbm is required, {require_active_user_token=}, {require_user_roles=}",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )
        if require_user_roles is not None:
            if not api_auth_data.user_token_dbm.user.compare_roles(require_user_roles):
                raise APIException(
                    status_code=fastapi.status.HTTP_403_FORBIDDEN,
                    error_code=APIErrorCodes.cannot_authorize,
                    error_description=f"user_token_dbm is required, {require_active_user_token=}, {require_user_roles=}",
                    error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
                )

    async_func.__name__ = require_user_token_dbm_api_authorize_middleware.__name__

    return async_func


def require_not_api_key_dbm_api_authorize_middleware():
    async def async_func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if api_auth_data.api_key_dbm is not None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"no api_key_dbm is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    async_func.__name__ = require_api_key_dbm_api_authorize_middleware.__name__

    return async_func


def require_not_user_token_dbm_api_authorize_middleware():
    async def async_func(*, api_auth_data: APIAuthorizeData, request: fastapi.requests.Request):
        if api_auth_data.user_token_dbm is not None:
            raise APIException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                error_code=APIErrorCodes.cannot_authorize,
                error_description=f"no user_token_dbm is required",
                error_data=transfer_data_to_json_str_to_data(api_auth_data.model_dump())
            )

    async_func.__name__ = require_api_key_dbm_api_authorize_middleware.__name__

    return async_func
