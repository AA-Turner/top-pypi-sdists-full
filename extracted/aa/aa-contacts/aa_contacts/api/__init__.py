from ninja import NinjaAPI
from ninja.security import django_auth

from django.conf import settings

from .alliance import router as alliance_router
from .corporation import router as corporation_router
from .permissions import router as permissions_router

api = NinjaAPI(
    title="AA Contacts API",
    version="0.0.1",
    urls_namespace='aa_contacts:api',
    auth=django_auth,
    openapi_url=settings.DEBUG and "/openapi.json" or ""
)

api.add_router("/alliances", alliance_router)
api.add_router("/corporations", corporation_router)
api.add_router("/permissions", permissions_router)
