import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize, require_api_key_dbm_api_authorize_middleware
from project.api.api_error_codes import APIErrorCodes, APIErrorSpecificationCodes
from project.api.schema.common import BaseSO
from project.api.schema.out.common.error import ErrorCommonSO


class _GetErrorsInfoGeneralSO(BaseSO):
    api_error_codes: list[str] = []
    api_error_specification_codes: list[str] = []


api_router = APIRouter()


@api_router.get(
    "",
    name="Get errors info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=_GetErrorsInfoGeneralSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            )
        ]))
):
    return _GetErrorsInfoGeneralSO(
        api_error_codes=APIErrorCodes.values_list(),
        api_error_specification_codes=APIErrorSpecificationCodes.values_list()
    )
