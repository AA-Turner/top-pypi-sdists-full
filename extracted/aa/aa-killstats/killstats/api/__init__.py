# Third Party
from ninja import NinjaAPI
from ninja.security import django_auth

# Django
from django.conf import settings

# AA Killstats
from killstats import __title__
from killstats.api import admin, general, killboard, stats

api = NinjaAPI(
    title="Killstats API",
    version="0.2.0",
    urls_namespace="killstats:new_api",
    auth=django_auth,
    openapi_url=settings.DEBUG and "/openapi.json" or "",
)


def setup(ninja_api):
    killboard.ApiEndpoints(ninja_api)
    admin.ApiEndpoints(ninja_api)
    stats.ApiEndpoints(ninja_api)
    general.ApiEndpoints(ninja_api)


# Initialize API endpoints
setup(api)
