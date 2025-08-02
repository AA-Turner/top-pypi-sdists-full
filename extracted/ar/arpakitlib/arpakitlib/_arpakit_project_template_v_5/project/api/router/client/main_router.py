from fastapi import APIRouter

from project.api.router.client import get_current_user, get_current_user_token

main_client_api_router = APIRouter()

main_client_api_router.include_router(
    router=get_current_user.api_router,
    prefix="/get_current_user"
)

main_client_api_router.include_router(
    router=get_current_user_token.api_router,
    prefix="/get_current_user_token"
)
