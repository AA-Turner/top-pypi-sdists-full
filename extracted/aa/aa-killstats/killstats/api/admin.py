"""API"""

# Standard Library
from http import HTTPStatus

# Third Party
from ninja import NinjaAPI

# AA Killstats
from killstats.api import schema
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit


class ApiEndpoints:
    tags = ["KillboardAdmin"]

    # pylint: disable=too-many-locals
    def __init__(self, api: NinjaAPI):
        self.register_endpoints(api)

    def register_endpoints(self, api: NinjaAPI):
        @api.get(
            "killboard/corporation/admin/",
            response={
                HTTPStatus.OK: list[schema.CorporationAdmin],
                HTTPStatus.FORBIDDEN: schema.ErrorSchema,
            },
            tags=self.tags,
        )
        def get_corporation_admin(request):
            corporations = CorporationsAudit.objects.visible_to(request.user)

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
            response={
                HTTPStatus.OK: list[schema.AllianceAdmin],
                HTTPStatus.FORBIDDEN: schema.ErrorSchema,
            },
            tags=self.tags,
        )
        def get_alliance_admin(request):
            alliances = AlliancesAudit.objects.visible_to(request.user)

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
