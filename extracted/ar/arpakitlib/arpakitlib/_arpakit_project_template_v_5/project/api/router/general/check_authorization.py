import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize
from project.api.schema.common import BaseSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.general.api_key import ApiKey1GeneralSO
from project.api.schema.out.general.user import User1GeneralSO
from project.api.schema.out.general.user_token import UserToken1GeneralSO


class _CheckAuthorizationGeneralSO(BaseSO):
    is_current_api_key_ok: bool = False
    is_current_user_token_ok: bool = False
    current_api_key: ApiKey1GeneralSO | None = None
    current_user_token: UserToken1GeneralSO | None = None
    current_user: User1GeneralSO | None = None


api_router = APIRouter()


@api_router.get(
    "",
    name="Check authorization",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=_CheckAuthorizationGeneralSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize())
):
    return _CheckAuthorizationGeneralSO(
        is_current_api_key_ok=api_auth_data.api_key_dbm is not None,
        is_current_user_token_ok=api_auth_data.user_token_dbm is not None,
        current_api_key=ApiKey1GeneralSO.from_dbm(
            simple_dbm=api_auth_data.api_key_dbm
        ) if api_auth_data.api_key_dbm is not None else None,
        current_user_token=UserToken1GeneralSO.from_dbm(
            simple_dbm=api_auth_data.user_token_dbm
        ) if api_auth_data.user_token_dbm is not None else None,
        current_user=User1GeneralSO.from_dbm(
            simple_dbm=api_auth_data.user_token_dbm.user
        ) if (api_auth_data.user_token_dbm is not None and api_auth_data.user_token_dbm.user is not None) else None
    )
