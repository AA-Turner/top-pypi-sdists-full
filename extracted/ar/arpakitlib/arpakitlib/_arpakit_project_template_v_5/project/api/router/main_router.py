from fastapi import APIRouter

from project.api.router.admin.main_router import main_admin_api_router
from project.api.router.client.main_router import main_client_api_router
from project.api.router.general.main_router import main_general_api_router

main_api_router = APIRouter()

main_api_router.include_router(
    prefix="/general",
    router=main_general_api_router,
    tags=["General"]
)
main_api_router.include_router(
    prefix="/client",
    router=main_client_api_router,
    tags=["Client"]
)
main_api_router.include_router(
    prefix="/admin",
    router=main_admin_api_router,
    tags=["Admin"]
)
