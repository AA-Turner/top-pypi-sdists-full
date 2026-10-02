"""General API Endpoints including Menu and User endpoints for Killstats V2."""

# Standard Library
from http import HTTPStatus

# Third Party
from ninja import NinjaAPI

# Django
from django.urls import reverse
from django.utils.translation import gettext as _

# AA Killstats
from killstats.api import schema
from killstats.helpers.eveonline import get_character_portrait_url


class ApiEndpoints:
    tags = ["General"]

    def __init__(self, api: NinjaAPI):
        @api.get(
            "menu/",
            response={
                HTTPStatus.OK: schema.MenuSchema,
            },
            tags=self.tags,
            summary="Get Killstats navigation menu",
        )
        def get_menu(request):
            left_menu: list[schema.MenuLink] = []

            main_char = getattr(
                getattr(request.user, "profile", None), "main_character", None
            )
            corp_id = getattr(main_char, "corporation_id", None)
            alliance_id = getattr(main_char, "alliance_id", None)

            corp_name = getattr(main_char, "corporation_name", None)
            alliance_name = getattr(main_char, "alliance_name", None)

            if corp_id:
                left_menu.append(
                    schema.MenuLink(
                        name=corp_name or _("Corporation"),
                        link=f"/v2/corporation/{corp_id}/",
                    )
                )

            if alliance_id:
                left_menu.append(
                    schema.MenuLink(
                        name=alliance_name or _("Alliance"),
                        link=f"/v2/alliance/{alliance_id}/",
                    )
                )

            left_menu.append(
                schema.MenuLink(
                    name=_("Corporation Overview"),
                    link="/overview/corporations/",
                )
            )

            if alliance_id or request.user.has_perm("killstats.admin_access"):
                left_menu.append(
                    schema.MenuLink(
                        name=_("Alliance Overview"),
                        link="/overview/alliances/",
                    )
                )

            right_menu: list[schema.MenuLink] = []
            if request.user.has_perm("killstats.admin_access"):
                right_menu.append(
                    schema.MenuLink(
                        name=_("Add Corporation"),
                        link=reverse("killstats:add_corp"),
                        is_external=True,
                    )
                )
                right_menu.append(
                    schema.MenuLink(
                        name=_("Add Alliance"),
                        link=reverse("killstats:add_alliance"),
                        is_external=True,
                    )
                )

            return schema.MenuSchema(
                left_links=left_menu,
                right_links=right_menu,
            )

        @api.get(
            "user/",
            response={
                HTTPStatus.OK: schema.UserData,
                HTTPStatus.FORBIDDEN: dict,
            },
            tags=self.tags,
            summary="Get current user data",
        )
        def get_user(request):
            if not request.user.has_perm("killstats.basic_access"):
                return HTTPStatus.FORBIDDEN, {"error": _("Permission Denied.")}

            try:
                character_id = request.user.profile.main_character.character_id
                character_name = request.user.profile.main_character.character_name
                corporation_id = request.user.profile.main_character.corporation_id
                corporation_name = request.user.profile.main_character.corporation_name
                alliance_id = request.user.profile.main_character.alliance_id
                alliance_name = request.user.profile.main_character.alliance_name
            except AttributeError:
                character_id = 0
                character_name = ""
                corporation_id = 0
                corporation_name = ""
                alliance_id = None
                alliance_name = None

            portrait_url = (
                get_character_portrait_url(
                    character_id=character_id,
                    character_name=character_name,
                    as_html=False,
                )
                if character_id
                else None
            )

            is_admin = bool(request.user.has_perm("killstats.admin_access"))

            return schema.UserData(
                user_id=request.user.id,
                character_id=character_id,
                character_name=character_name,
                corporation_id=corporation_id,
                corporation_name=corporation_name,
                alliance_id=alliance_id,
                alliance_name=alliance_name,
                portrait=portrait_url,
                is_admin=is_admin,
            )
