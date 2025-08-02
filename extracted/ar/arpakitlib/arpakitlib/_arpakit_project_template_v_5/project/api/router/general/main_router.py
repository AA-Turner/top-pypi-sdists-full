from fastapi import APIRouter

from project.api.router.general import healthcheck, now_utc_datetime, get_current_api_key, check_authorization, \
    get_errors_info

main_general_api_router = APIRouter()

main_general_api_router.include_router(
    router=healthcheck.api_router,
    prefix="/healthcheck"
)

main_general_api_router.include_router(
    router=now_utc_datetime.api_router,
    prefix="/now_utc_datetime"
)

main_general_api_router.include_router(
    router=get_current_api_key.api_router,
    prefix="/get_current_api_key"
)

main_general_api_router.include_router(
    router=check_authorization.api_router,
    prefix="/check_authorization"
)

main_general_api_router.include_router(
    router=get_errors_info.api_router,
    prefix="/get_errors_info"
)
