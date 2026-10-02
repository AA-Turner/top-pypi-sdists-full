"""New API Endpoints for Killboard V2."""

# Standard Library
from http import HTTPStatus
from typing import Literal

# Third Party
from ninja import NinjaAPI, Query
from ninja.decorators import decorate_view

# Django
from django.db.models import Q, Sum
from django.views.decorators.cache import cache_page

# AA Killstats
from killstats.api import schema
from killstats.models import Attacker, Killmail


class ApiEndpoints:
    tags = ["Killboard Stats v2"]

    def __init__(self, api: NinjaAPI):
        self.register_hall(api)
        self.register_stats(api)

    def register_hall(self, api: NinjaAPI):
        @api.get(
            "hall/v2/{entity_type}/{entity_id}/",
            response={
                HTTPStatus.OK: schema.HallResponseSchema,
                HTTPStatus.FORBIDDEN: dict,
                HTTPStatus.INTERNAL_SERVER_ERROR: str,
            },
            tags=self.tags,
            summary="Retrieve the hall of fame for an entity",
        )
        @decorate_view(cache_page(60 * 5))  # Cache the response for 5 minutes
        # pylint: disable=too-many-locals
        def get_hall_endpoint(
            request,
            entity_type: Literal["alliance", "corporation", "character"],
            entity_id: int,
            filters: schema.HallFilter = Query(...),
        ):
            if not request.user.has_perm("killstats.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": "Permission denied."}

            try:
                # Determine the query for the attacker's killmails based on the entity type.
                if entity_type == "alliance":
                    attacker_km_q = Q(attacker_killmail__alliance_id=entity_id)
                elif entity_type == "corporation":
                    attacker_km_q = Q(attacker_killmail__corporation_id=entity_id)
                elif entity_type == "character":
                    attacker_km_q = Q(attacker_killmail__character_id=entity_id)
                else:
                    attacker_km_q = Q()

                # Fetch the top killmails for the given entity and time period.
                fame_killmails = list(
                    Killmail.objects.filter(attacker_km_q, filters.km_date_q)
                    .distinct()
                    .select_related("victim", "victim_ship")
                    .order_by("-victim_total_value")[: filters.limit]
                )
                top_km_ids = [km.killmail_id for km in fame_killmails]

                # For each of the top killmails, find the best attacker from the entity.
                best_attackers_by_km = {}
                if top_km_ids:
                    entity_attackers = (
                        Attacker.objects.for_entity(entity_type, entity_id)
                        .filter(killmail_id__in=top_km_ids)
                        .select_related("character", "ship")
                        .order_by("-damage_done", "-final_blow")
                    )
                    for att in entity_attackers:
                        if att.killmail_id not in best_attackers_by_km:
                            best_attackers_by_km[att.killmail_id] = att

                hall_of_fame = []
                for km in fame_killmails:
                    a = best_attackers_by_km.get(km.killmail_id)
                    if not a:
                        continue
                    hall_of_fame.append(
                        schema.HallEntrySchema(
                            killmail_id=km.killmail_id,
                            char_id=a.character_id or 0,
                            char_name=a.character.name if a.character else "Unknown",
                            ship_id=a.ship_id or 0,
                            ship_name=a.ship.name if a.ship else "Unknown",
                            victim_ship_id=km.victim_ship_id or 0,
                            victim_ship_name=(
                                km.victim_ship.name if km.victim_ship else "Unknown"
                            ),
                            total_value=km.victim_total_value,
                            damage_done=a.damage_done or 0,
                            zkb_link=f"https://zkillboard.com/kill/{km.killmail_id}/",
                        )
                    )

                # --- Hall of Shame (losses) ---
                shame_killmails = (
                    Killmail.objects.for_victim_entity(entity_type, entity_id)
                    .filter(filters.km_date_q)
                    .select_related("victim", "victim_ship")
                    .order_by("-victim_total_value")[: filters.limit]
                )

                hall_of_shame = [
                    schema.HallEntrySchema(
                        killmail_id=km.killmail_id,
                        char_id=km.victim_id or 0,
                        char_name=km.victim.name if km.victim else "Unknown",
                        ship_id=km.victim_ship_id or 0,
                        ship_name=km.victim_ship.name if km.victim_ship else "Unknown",
                        victim_ship_id=km.victim_ship_id or 0,
                        victim_ship_name=(
                            km.victim_ship.name if km.victim_ship else "Unknown"
                        ),
                        total_value=km.victim_total_value,
                        damage_done=0,
                        zkb_link=f"https://zkillboard.com/kill/{km.killmail_id}/",
                    )
                    for km in shame_killmails
                ]

                return HTTPStatus.OK, schema.HallResponseSchema(
                    hall_of_fame=hall_of_fame, hall_of_shame=hall_of_shame
                )
            except Exception as e:  # pylint: disable=broad-except
                return HTTPStatus.INTERNAL_SERVER_ERROR, str(e)

    def register_stats(self, api: NinjaAPI):
        @api.get(
            "stats/v2/summary/{entity_type}/{entity_id}/",
            response={
                HTTPStatus.OK: schema.CombatSummaryResponse,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
            summary="Fast summary: total kills, ISK & active PvPers",
        )
        @decorate_view(cache_page(60 * 5))  # Cache the response for 5 minutes
        # pylint: disable=too-many-locals
        def get_combat_summary_api(
            request,
            entity_type: Literal["alliance", "corporation", "character"],
            entity_id: int,
            filters: schema.DateRangeFilter = Query(...),
        ):
            if not request.user.has_perm("killstats.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": "Permission denied."}

            # Kills side
            kill_qs = Attacker.objects.for_entity(entity_type, entity_id).filter(
                filters.att_date_q
            )

            # Get distinct killmail IDs for the attacker queryset
            killmail_ids = kill_qs.values_list("killmail_id", flat=True).distinct()
            total_kills = killmail_ids.count()

            # Count active PvPers (distinct characters who participated in kills)
            active_pvpers = (
                kill_qs.exclude(character_id__isnull=True)
                .values("character_id")
                .distinct()
                .count()
            )

            # Calculate destroyed ISK for the attacker side
            destroyed_isk = (
                Killmail.objects.filter(killmail_id__in=killmail_ids).aggregate(
                    total=Sum("victim_total_value")
                )["total"]
                or 0
            )

            # Losses side
            lost_isk = (
                Killmail.objects.for_victim_entity(entity_type, entity_id)
                .filter(filters.km_date_q)
                .aggregate(total=Sum("victim_total_value"))["total"]
                or 0
            )

            return schema.CombatSummaryResponse(
                total_kills=total_kills,
                active_pvpers=active_pvpers,
                destroyed_isk=destroyed_isk,
                lost_isk=lost_isk,
            )
