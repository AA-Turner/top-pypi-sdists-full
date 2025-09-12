import os

import fastapi
from arpakitlib.ar_datetime_util import now_utc_dt
from arpakitlib.ar_logging_util import init_log_file
from fastapi import APIRouter

from project.api.authorize import require_api_key_dbm_api_authorize_middleware, APIAuthorizeData, \
    require_user_token_dbm_api_authorize_middleware, api_authorize
from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM

api_router = APIRouter()


@api_router.get(
    path="",
    name=os.path.splitext(os.path.basename(__file__))[0].title(),
    status_code=fastapi.status.HTTP_200_OK,
    response_class=fastapi.responses.FileResponse
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
                require_user_roles=[UserDBM.Roles.admin]
            )
        ]))
):
    init_log_file(log_filepath=get_cached_settings().log_filepath)
    return fastapi.responses.FileResponse(
        path=get_cached_settings().log_filepath,
        media_type="text/plain",
        filename=f"story_{now_utc_dt().strftime('%d.%m.%Y_%H:%M_%Z%z')}.log"
    )
