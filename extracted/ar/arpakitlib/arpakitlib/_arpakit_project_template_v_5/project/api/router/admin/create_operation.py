from typing import Any

import fastapi
from fastapi import APIRouter

from project.api.authorize import require_api_key_dbm_api_authorize_middleware, \
    require_user_token_dbm_api_authorize_middleware, APIAuthorizeData, api_authorize
from project.api.schema.common import BaseSI
from project.api.schema.out.admin.operation import Operation1AdminSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM, OperationDBM


class _CreateOperationAdminSI(BaseSI):
    slug: str | None = None
    type: str
    title: str | None = None
    input_data: dict[str, Any] = None


api_router = APIRouter()


@api_router.post(
    "",
    name="Create operation",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=Operation1AdminSO | ErrorCommonSO,
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
        create_operation_admin_si: _CreateOperationAdminSI = fastapi.Body()
):
    operation_dbm = OperationDBM(
        status=OperationDBM.Statuses.waiting_for_execution
    )

    if "slug" in create_operation_admin_si.model_fields_set:
        operation_dbm.slug = create_operation_admin_si.slug

    if "type" in create_operation_admin_si.model_fields_set:
        operation_dbm.type = create_operation_admin_si.type

    if "title" in create_operation_admin_si.model_fields_set:
        operation_dbm.title = create_operation_admin_si.title

    if "input_data" in create_operation_admin_si.model_fields_set:
        operation_dbm.input_data = create_operation_admin_si.input_data

    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        async_session.add(operation_dbm)
        await async_session.commit()
        await async_session.refresh(operation_dbm)

    return Operation1AdminSO.from_dbm(simple_dbm=operation_dbm)
