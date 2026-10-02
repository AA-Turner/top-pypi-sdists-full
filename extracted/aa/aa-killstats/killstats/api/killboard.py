# Standard Library
from http import HTTPStatus
from typing import Literal

# Third Party
from ninja import NinjaAPI, Query
from ninja.decorators import decorate_view

# Django
from django.db.models import Count, Sum
from django.views.decorators.cache import cache_page

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from eve_sde.models import SolarSystem

# AA Killstats
from killstats import __title__
from killstats.api import schema
from killstats.api.helpers import _build_main_name_map
from killstats.models.killboard import Attacker, Killmail
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class ApiEndpoints:
    tags = ["Killboard v2"]

    def __init__(self, api: NinjaAPI):
        self.register_top(api)
        self.register_killmails(api)

    def register_top(self, api: NinjaAPI):
        @api.get(
            "stats/v2/attackers/{entity_type}/{entity_id}/",
            response={
                HTTPStatus.OK: schema.TopPilotsResponse,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
            summary="Top-10 attackers for an entity",
        )
        @decorate_view(cache_page(60 * 5))  # Cache the response for 5 minutes
        def get_top_attackers_api(
            request,
            entity_type: Literal["alliance", "corporation", "character"],
            entity_id: int,
            filters: schema.TopPilotsFilter = Query(...),
        ):
            if not request.user.has_perm("killstats.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": "Permission denied."}

            alt_mapping = _build_main_name_map(entity_type, entity_id)

            top_qs = (
                Attacker.objects.for_entity(entity_type, entity_id)
                .filter(filters.att_date_q)
                .values("character_id", "character__name")
                .annotate(
                    kills=Count("killmail_id", distinct=True),
                    total_value=Sum("killmail__victim_total_value"),
                )
                .order_by("-kills", "character__name")[: filters.limit]
            )

            pilots = [
                schema.TopPilotSchema(
                    character_id=row["character_id"],
                    character_name=row["character__name"] or "Unknown",
                    main_name=alt_mapping.get(row["character_id"]),
                    count=row["kills"],
                    total_value=row["total_value"] or 0,
                )
                for row in top_qs
            ]

            return schema.TopPilotsResponse(pilots=pilots)

        @api.get(
            "stats/v2/victims/{entity_type}/{entity_id}/",
            response={
                HTTPStatus.OK: schema.TopPilotsResponse,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
            summary="Top-10 victims for an entity",
        )
        @decorate_view(cache_page(60 * 5))  # Cache the response for 5 minutes
        def get_top_victims_api(
            request,
            entity_type: Literal["alliance", "corporation", "character"],
            entity_id: int,
            filters: schema.TopPilotsFilter = Query(...),
        ):
            if not request.user.has_perm("killstats.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": "Permission denied."}

            alt_mapping = _build_main_name_map(entity_type, entity_id)

            top_qs = (
                Killmail.objects.for_victim_entity(entity_type, entity_id)
                .filter(filters.km_date_q)
                .exclude(victim_id__isnull=True)
                .values("victim_id", "victim__name")
                .annotate(
                    deaths=Count("killmail_id", distinct=True),
                    total_value=Sum("victim_total_value"),
                )
                .order_by("-deaths", "victim__name")[: filters.limit]
            )

            pilots = [
                schema.TopPilotSchema(
                    character_id=row["victim_id"],
                    character_name=row["victim__name"] or "Unknown",
                    main_name=alt_mapping.get(row["victim_id"]),
                    count=row["deaths"],
                    total_value=row["total_value"] or 0,
                )
                for row in top_qs
            ]

            return schema.TopPilotsResponse(pilots=pilots)

    # pylint: disable=too-many-locals, too-many-branches
    def register_killmails(self, api: NinjaAPI):
        @api.get(
            "killmails/{entity_type}/{entity_id}/",
            response={
                HTTPStatus.OK: schema.KillmailListResponse,
                HTTPStatus.FORBIDDEN: dict,
                HTTPStatus.INTERNAL_SERVER_ERROR: str,
            },
            tags=self.tags,
            summary="Retrieve killmails for an entity",
        )
        @decorate_view(cache_page(60 * 5))  # Cache the response for 5 minutes
        def get_killmails_endpoint(
            request,
            entity_type: Literal["alliance", "corporation", "character"],
            entity_id: int,
            filters: schema.KillmailFilter = Query(...),
        ):
            if not request.user.has_perm("killstats.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": "Permission denied."}

            try:
                # 1. Fetch paged IDs and total count across kills, losses or both
                paged_ids, total = Killmail.objects.get_paged_ids(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    mode=filters.mode,
                    att_date_q=filters.att_date_q,
                    km_date_q=filters.km_date_q,
                    page=filters.page,
                    page_size=filters.page_size,
                )

                # 2. Two-phase loading: only load and annotate the paged IDs
                km_slice = (
                    list(Killmail.objects.for_paged_killboard(paged_ids))
                    if paged_ids
                    else []
                )

                # 3. Bulk resolve solar systems via native Django in_bulk
                system_ids = {
                    km.victim_solar_system_id
                    for km in km_slice
                    if km.victim_solar_system_id
                }
                system_map = (
                    SolarSystem.objects.in_bulk(system_ids) if system_ids else {}
                )

                # Initialize the list that will hold the serialized killmail data.
                killmails_list = []
                for km in km_slice:
                    final_blow_id = 0
                    final_blow_name = "Unknown"
                    security_status = 0.0
                    solar_system_name = "Unknown"

                    fb_list = getattr(km, "final_blow_attacker", [])
                    if fb_list:
                        fb = fb_list[0]
                        final_blow_id = fb.character_id or 0
                        final_blow_name = (
                            fb.character.name if fb.character else "Unknown"
                        )

                    solar_system = system_map.get(km.victim_solar_system_id)
                    if solar_system:
                        solar_system_name = solar_system.name
                        security_status = solar_system.security_status

                    is_loss = False
                    if entity_type == "alliance":
                        is_loss = km.victim_alliance_id == entity_id
                    elif entity_type == "corporation":
                        is_loss = km.victim_corporation_id == entity_id
                    elif entity_type == "character":
                        is_loss = km.victim_id == entity_id

                    killmails_list.append(
                        schema.KillmailItemSchema(
                            killmail_id=km.killmail_id,
                            killmail_date=km.killmail_date.isoformat(),
                            victim_id=km.victim_id or 0,
                            victim_name=km.victim.name if km.victim else "Unknown",
                            victim_ship_id=km.victim_ship_id or 0,
                            victim_ship_name=(
                                km.victim_ship.name if km.victim_ship else "Unknown"
                            ),
                            total_value=km.victim_total_value,
                            solar_system_id=km.victim_solar_system_id or 0,
                            solar_system_name=solar_system_name,
                            security_status=security_status,
                            pilot_count=km.pilot_count,
                            final_blow_id=final_blow_id,
                            final_blow_name=final_blow_name,
                            is_loss=is_loss,
                            zkb_link=f"https://zkillboard.com/kill/{km.killmail_id}/",
                        )
                    )
                return HTTPStatus.OK, schema.KillmailListResponse(
                    killmails=killmails_list,
                    total=total,
                    page=filters.page,
                    page_size=filters.page_size,
                )
            except Exception as e:  # pylint: disable=broad-except
                return HTTPStatus.INTERNAL_SERVER_ERROR, str(e)
