import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.general.api_key import ApiKey1GeneralSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    "",
    name="Get current api key",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=ApiKey1GeneralSO | str | ErrorCommonSO,
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
    return ApiKey1GeneralSO.from_dbm(
        simple_dbm=api_auth_data.api_key_dbm
    )
