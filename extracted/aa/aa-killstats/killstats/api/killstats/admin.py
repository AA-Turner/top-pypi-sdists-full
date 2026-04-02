"""API"""

# Third Party
from ninja import NinjaAPI

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.api import schema
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class KillboardAdminApiEndpoints:
    tags = ["KillboardAdmin"]

    # pylint: disable=too-many-locals
    def __init__(self, api: NinjaAPI):
        self.register_endpoints(api)

    def register_endpoints(self, api: NinjaAPI):
        @api.get(
            "killboard/corporation/admin/",
            response={200: list[schema.CorporationAdmin], 403: str},
            tags=self.tags,
        )
        def get_corporation_admin(request):
            corporations = CorporationsAudit.objects.visible_to(request.user)

            if corporations is None:
                return 403, "Permission Denied"

            corporation_dict = {}

            for corporation in corporations:
                # pylint: disable=broad-exception-caught
                try:
                    corporation_dict[corporation.corporation.corporation_id] = {
                        "corporation_id": corporation.corporation.corporation_id,
                        "corporation_name": corporation.corporation.corporation_name,
                    }
                except Exception:
                    continue

            output = []
            output.append({"corporation": corporation_dict})

            return output

        @api.get(
            "killboard/alliance/admin/",
            response={200: list[schema.AllianceAdmin], 403: str},
            tags=self.tags,
        )
        def get_alliance_admin(request):
            alliances = AlliancesAudit.objects.visible_to(request.user)

            if alliances is None:
                return 403, "Permission Denied"

            alliance_dict = {}

            for alliance in alliances:
                # pylint: disable=broad-exception-caught
                try:
                    alliance_dict[alliance.alliance.alliance_id] = {
                        "alliance_id": alliance.alliance.alliance_id,
                        "alliance_name": alliance.alliance.alliance_name,
                    }
                except Exception:
                    continue

            output = []
            output.append({"alliance": alliance_dict})

            return output
