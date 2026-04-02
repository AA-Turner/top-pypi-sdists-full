"""API"""

# Third Party
from ninja import NinjaAPI

# Django
from django.db.models import Count, Q
from django.shortcuts import render

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.api.killstats import api_helper
from killstats.models.killboard import Attacker, Killmail
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class KillboardStatsApiEndpoints:
    tags = ["Stats"]

    # pylint: disable=too-many-locals
    def __init__(self, api: NinjaAPI):
        self.register_endpoints(api)

    # pylint: disable=too-many-statements
    def register_endpoints(self, api: NinjaAPI):
        @api.get(
            "stats/top/10/month/{month}/year/{year}/{entity_type}/{entity_id}/",
            response={200: list[dict], 403: str},
            tags=self.tags,
        )
        def get_top_10_api(request, month, year, entity_type: str, entity_id: int):
            cache_name = f"top_10_{month}_{year}_{entity_type}_{entity_id}"
            output, cache_key = api_helper.cache_sytem(request, cache_name, entity_id)
            if cache_key:
                top_10 = api_helper.get_top_10(
                    request=request,
                    month=month,
                    year=year,
                    entity_type=entity_type,
                    entity_id=entity_id,
                )

                output = {"top10": top_10}
                api_helper.set_cache_key(cache_key, output)

            return render(
                request,
                "killstats/partials/modal/view_top_10.html",
                output,
            )

        @api.get(
            "stats/all/month/{month}/year/{year}/{entity_type}/{entity_id}/",
            response={200: dict, 403: str},
            tags=self.tags,
        )
        def get_all_stats(request, month, year, entity_type: str, entity_id: int):
            cache_name = f"stats_{month}_{year}_{entity_type}_{entity_id}"
            output, cache_key = api_helper.cache_sytem(request, cache_name, entity_id)
            entities = api_helper.get_entities(request, entity_type, entity_id)

            if cache_key:
                # Get All Killmails
                killmail = Killmail.objects.filter(
                    Q(victim_id__in=entities)
                    | Q(victim_corporation_id__in=entities)
                    | Q(victim_alliance_id__in=entities),
                    killmail_date__year=year,
                )

                # Get All Attackers
                attackers = Attacker.objects.filter(
                    Q(corporation_id__in=entities)
                    | Q(alliance_id__in=entities)
                    | Q(character_id__in=entities),
                    killmail__killmail_date__year=year,
                )

                # Get for the month
                attackers_month = attackers.filter(killmail__killmail_date__month=month)
                killmail_month = killmail.filter(killmail_date__month=month)

                alltime_killer = (
                    attackers.values("character_id", "character__name")
                    .annotate(
                        alltime_killer=Count("killmail__killmail_id", distinct=True)
                    )
                    .order_by("-alltime_killer", "character__name")
                )

                alltime_victim = (
                    killmail.values("victim_id", "victim__name")
                    .annotate(alltime_victim=Count("killmail_id", distinct=True))
                    .order_by("-alltime_victim", "victim__name")
                )

                top_ship = (
                    attackers_month.values("ship__id", "ship__name")
                    .annotate(count=Count("killmail__killmail_id", distinct=True))
                    .order_by("-count")
                )

                top_killer = (
                    attackers_month.values("character_id", "character__name").annotate(
                        top_killer=Count("character_id")
                    )
                ).order_by("-top_killer", "character__name")

                top_victim = (
                    killmail_month.values("victim_id", "victim__name").annotate(
                        top_victim=Count("victim_id")
                    )
                ).order_by("-top_victim", "victim__name")

                top_victim_ship = (
                    killmail_month.exclude(victim_ship__group_id__in=[29])
                    .values("victim_ship_id", "victim_ship__name")
                    .annotate(top_victim_ship=Count("victim_ship_id"))
                ).order_by("-top_victim_ship", "victim_ship__name")

                highest_kill = attackers_month.values(
                    "killmail_id",
                    "killmail__victim_total_value",
                    "killmail__victim_ship__id",
                    "killmail__victim_ship__name",
                ).order_by("-killmail__victim_total_value")

                highest_loss = killmail_month.values(
                    "killmail_id",
                    "victim_total_value",
                    "victim_ship__id",
                    "victim_ship__name",
                ).order_by("-victim_total_value")

                output = {
                    "stats": {
                        "alltime_killer": alltime_killer.first(),
                        "alltime_victim": alltime_victim.first(),
                        "top_ship": top_ship.first(),
                        "top_victim_ship": top_victim_ship.first(),
                        "top_victim": top_victim.first(),
                        "top_killer": top_killer.first(),
                        "highest_kill": highest_kill.first(),
                        "highest_loss": highest_loss.first(),
                    }
                }
                api_helper.set_cache_key(cache_key, output)

            return output
