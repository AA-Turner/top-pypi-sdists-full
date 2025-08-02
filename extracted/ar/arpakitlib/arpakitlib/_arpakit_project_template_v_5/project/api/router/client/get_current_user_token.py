from __future__ import annotations

import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.out.client.complicated_user_token_1 import ComplicatedUserToken1ClientSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    "",
    name="Get current user token",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ComplicatedUserToken1ClientSO | ErrorCommonSO,
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
    return ComplicatedUserToken1ClientSO.from_dbm(
        simple_dbm=api_auth_data.user_token_dbm
    )
