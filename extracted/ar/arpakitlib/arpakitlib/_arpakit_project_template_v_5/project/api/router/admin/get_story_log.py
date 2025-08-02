import fastapi.requests
import sqlalchemy
from fastapi import APIRouter

from arpakitlib.ar_str_util import make_none_if_blank, strip_if_not_none
from project.api.authorize import APIAuthorizeData, api_authorize, require_user_token_dbm_api_authorize_middleware, \
    require_api_key_dbm_api_authorize_middleware
from project.api.schema.out.admin.story_log import StoryLog1AdminSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM, StoryLogDBM

api_router = APIRouter()


@api_router.get(
    "",
    name="Get story log",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=StoryLog1AdminSO | None | ErrorCommonSO,
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
        ])),
        filter_id: int | None = fastapi.Query(default=None),
        filter_long_id: str | None = fastapi.Query(default=None),
):
    filter_long_id = make_none_if_blank(strip_if_not_none(filter_long_id))

    if filter_id is None and filter_long_id is None:
        return None

    query = sqlalchemy.select(StoryLogDBM)
    if filter_id is not None:
        query = query.filter(StoryLogDBM.id == filter_id)
    if filter_long_id is not None:
        query = query.filter(StoryLogDBM.long_id == filter_long_id)

    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        result = await async_session.scalar(query)
        if result is None:
            return None
        return StoryLog1AdminSO.from_dbm(simple_dbm=result)
