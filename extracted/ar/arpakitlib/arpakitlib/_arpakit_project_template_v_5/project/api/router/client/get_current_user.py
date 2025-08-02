from __future__ import annotations

import fastapi.requests
import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.out.client.complicated_user_1 import ComplicatedUser1ClientSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    "",
    name="Get current user",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ComplicatedUser1ClientSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ),
            require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.client]
            )
        ]))
):
    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        user_dbm = await async_session.scalar(
            sqlalchemy
            .select(UserDBM)
            .filter(UserDBM.id == api_auth_data.user_token_dbm.user_id)
            .options(joinedload(UserDBM.user_tokens))
        )
    return ComplicatedUser1ClientSO.from_dbm(simple_dbm=user_dbm)
