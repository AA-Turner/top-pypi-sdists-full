import fastapi
from fastapi import APIRouter

from project.api.authorize import require_api_key_dbm_api_authorize_middleware, APIAuthorizeData, \
    require_user_token_dbm_api_authorize_middleware, api_authorize
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.ok import OkCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.test_data.make_test_data_4 import make_test_data_4

api_router = APIRouter()


@api_router.get(
    path="",
    name="Make test data 4",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=OkCommonSO | ErrorCommonSO
)
def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ),
            require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin]
            )
        ]))
):
    make_test_data_4()
    return OkCommonSO()
