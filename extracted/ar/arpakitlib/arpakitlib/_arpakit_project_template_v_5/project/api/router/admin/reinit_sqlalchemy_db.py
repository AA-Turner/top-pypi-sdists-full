import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_not_prod_mode_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.ok import OkCommonSO
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    path="",
    name="Reinit sqlalchemy db",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=OkCommonSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_not_prod_mode_api_authorize_middleware(),
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ),
            require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin],
            ),
        ]))
):
    get_cached_sqlalchemy_db().reinit()
    return OkCommonSO()
