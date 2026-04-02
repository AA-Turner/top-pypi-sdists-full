"""API"""

# Third Party
from ninja import NinjaAPI

# Django
from django.http import JsonResponse

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.api import schema
from killstats.api.killstats import api_helper
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class KillboardApiEndpoints:
    tags = ["Killboard"]

    def __init__(self, api: NinjaAPI):
        self.register_endpoints(api)

    def register_endpoints(self, api: NinjaAPI):
        # Killmails
        @api.get(
            "killmail/month/{month}/year/{year}/{entity_type}/{entity_id}/{mode}/",
            response={200: dict, 403: str},
            tags=self.tags,
        )
        # pylint: disable=too-many-positional-arguments
        def get_corporation_killmails(
            request, month, year, entity_type: str, entity_id: int, mode
        ):
            output = api_helper.get_killmails_data(
                request, month, year, entity_type, entity_id, mode
            )
            return JsonResponse(output, safe=False)

        # Hall of Fame/Shame
        @api.get(
            "halls/month/{month}/year/{year}/{entity_type}/{entity_id}/",
            response={200: list[schema.KillboardHall], 403: str},
            tags=self.tags,
        )
        def get_corporation_halls(
            request, month, year, entity_type: str, entity_id: int
        ):
            cache_name = f"hall_{month}_{year}_{entity_type}_{entity_id}"
            output, cache_key = api_helper.cache_sytem(request, cache_name, entity_id)

            if cache_key:
                output = api_helper.get_killstats_halls(
                    request, month, year, entity_type, entity_id
                )
                # Cache the output
                api_helper.set_cache_key(cache_key, output)
            return JsonResponse(output, safe=False)
