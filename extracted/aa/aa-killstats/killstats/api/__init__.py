# Third Party
from ninja import NinjaAPI
from ninja.security import django_auth

# Django
from django.conf import settings

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.api import killstats

api = NinjaAPI(
    title="Killstats API",
    version="0.2.0",
    urls_namespace="killstats:new_api",
    auth=django_auth,
    openapi_url=settings.DEBUG and "/openapi.json" or "",
)

# Add the character endpoints
killstats.setup(api)
