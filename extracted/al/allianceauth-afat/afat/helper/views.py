"""
Views helper
"""

# Standard Library
import random
from collections import OrderedDict
from enum import Enum

# Django
from django.contrib.auth.models import Permission, User
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.framework.api.user import get_main_character_name_from_user

# Alliance Auth AFAT
from afat.helper.users import users_with_permission
from afat.models import Fat, FatLink


class AFATUI(Enum):
    """
    AFAT UI Elements
    """

    BADGE_ESI_TRACKING_ACTIVE = "badge text-bg-success afat-label ms-2"
    BADGE_ESI_TRACKING_INACTIVE = "badge text-bg-secondary afat-label ms-2"
    BADGE_ESI_TRACKING_TEXT = _("ESI")

    BUTTON_DELETE_TEXT = _("Delete")
    BUTTON_CLOSE_ESI_FLEET_TITLE = _(
        "Stop automatic tracking through ESI for this fleet and close the associated FAT link."
    )
    BUTTON_CLOSE_ESI_FLEET_CONFIRM_TEXT = _("Stop tracking")


def _generate_close_esi_fleet_action_button(  # pylint: disable=too-many-arguments, too-many-positional-arguments
    viewname: str,
    fatlink_hash: str,
    redirect_to: str,
    body_text: str,
) -> str:
    """
    Generate action button HTML

    :param viewname:
    :type viewname:
    :param fatlink_hash:
    :type fatlink_hash:
    :param redirect_to:
    :type redirect_to:
    :param body_text:
    :type body_text:
    :return:
    :rtype:
    """

    redirect_param = f"?next={redirect_to}" if redirect_to else ""

    return (
        '<a class="btn btn-afat-action btn-primary btn-sm m-1" '
        f'title="{AFATUI.BUTTON_CLOSE_ESI_FLEET_TITLE.value}" '
        'data-bs-toggle="modal" '
        'data-bs-target="#cancelEsiFleetModal" '
        'data-bs-tooltip="afat" '
        f'data-url="{reverse(viewname=viewname, args=[fatlink_hash])}{redirect_param}" '
        f'data-body-text="{body_text}" data-confirm-text="{AFATUI.BUTTON_CLOSE_ESI_FLEET_CONFIRM_TEXT.value}">'
        '<i class="fa-solid fa-times"></i></a>'
    )


def _generate_view_button(viewname: str, fatlink_hash: str) -> str:
    """
    Generate view button HTML

    :param viewname:
    :type viewname:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    return (
        f'<a class="btn btn-info btn-sm m-1" href="{reverse(viewname=viewname, args=[fatlink_hash])}">'
        '<span class="fa-solid fa-eye"></span></a>'
    )


def _get_request_cache(request: WSGIRequest) -> dict:
    """
    Get or create a per-request cache dictionary

    :param request:
    :type request:
    :return:
    :rtype:
    """

    cache = getattr(request, "_afat_cache", None)

    if cache is None:
        cache = {}
        setattr(request, "_afat_cache", cache)

    return cache


def _perm_flags(request: WSGIRequest) -> dict[str, bool]:
    """
    Get and cache permission flags for the request user

    :param request:
    :type request:
    :return:
    :rtype:
    """

    cache = getattr(request, "_afat_cache", None)

    if cache is None:
        request._afat_cache = {}
        cache = request._afat_cache

    # Return cached value if present
    if "perm_flags" in cache:
        return cache["perm_flags"]

    # Safely handle requests without a user
    user = getattr(request, "user", None)

    if user is None:
        flags = {"manage": False, "add": False}
    else:
        flags = {
            "manage": bool(user.has_perm("afat.manage_afat")),
            "add": bool(user.has_perm("afat.add_fatlink")),
        }

    cache["perm_flags"] = flags

    return flags


def _cached_main_character_name(request: WSGIRequest, user: User) -> str:
    """
    Get and cache main character name for a user in the request cache

    :param request:
    :type request:
    :param user:
    :type user:
    :return:
    :rtype:
    """

    cache = _get_request_cache(request)
    names = cache.setdefault("main_char_names", {})
    uid = getattr(user, "pk", None)

    if uid in names:
        return names[uid]

    name = get_main_character_name_from_user(user=user)
    names[uid] = name

    return name


def _generate_delete_button(
    viewname: str,
    fatlink_hash: str,
    body_text: str | Promise,
) -> str:
    """
    Generate delete button HTML

    :param viewname:
    :type viewname:
    :param fatlink_hash:
    :type fatlink_hash:
    :param confirm_text:
    :type confirm_text:
    :param body_text:
    :type body_text:
    :return:
    :rtype:
    """

    return (
        '<a class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteFatLinkModal" '
        f'data-url="{reverse(viewname=viewname, args=[fatlink_hash])}" data-confirm-text="{AFATUI.BUTTON_DELETE_TEXT.value}" '
        f'data-body-text="{body_text}">'
        '<i class="fa-solid fa-trash-can fa-fw"></i></a>'
    )


def convert_fatlinks_to_dict(
    request: WSGIRequest, fatlink: FatLink, close_esi_redirect: str = None
) -> dict:
    """
    Converts an AFatLink object into a dictionary

    :param request:
    :type request:
    :param fatlink:
    :type fatlink:
    :param close_esi_redirect:
    :type close_esi_redirect:
    :return:
    :rtype:
    """

    user = request.user
    flags = _perm_flags(request)
    has_manage = flags["manage"]
    has_add = flags["add"]

    fleet_label = fatlink.fleet or fatlink.hash
    via_esi = "Yes" if fatlink.is_esilink else "No"

    # Build ESI marker
    esi_fleet_marker = ""
    if fatlink.is_esilink:
        badge_cls = (
            AFATUI.BADGE_ESI_TRACKING_ACTIVE.value
            if fatlink.is_registered_on_esi
            else AFATUI.BADGE_ESI_TRACKING_INACTIVE.value
        )
        esi_fleet_marker = (
            f'<span class="{badge_cls}">{AFATUI.BADGE_ESI_TRACKING_TEXT.value}</span>'
        )

    actions_parts = []

    # Only compute action button when owner & esilink conditions match
    if fatlink.is_esilink and fatlink.is_registered_on_esi and fatlink.creator == user:
        actions_parts.append(
            _generate_close_esi_fleet_action_button(
                "afat:fatlinks_close_esi_fatlink",
                fatlink.hash,
                close_esi_redirect,
                _(
                    "<p>Are you sure you want to close ESI fleet with ID {esi_fleet_id} from {character_name}?</p>"
                ).format(
                    esi_fleet_id=fatlink.esi_fleet_id,
                    character_name=fatlink.character.character_name,
                ),
            )
        )

    if has_manage or has_add:
        actions_parts.append(
            _generate_view_button("afat:fatlinks_details_fatlink", fatlink.hash)
        )

    if has_manage:
        actions_parts.append(
            _generate_delete_button(
                "afat:fatlinks_delete_fatlink",
                fatlink.hash,
                _(
                    "<p>Are you sure you want to delete FAT link {fatlink_fleet}?</p>"
                ).format(fatlink_fleet=fleet_label),
            )
        )

    return {
        "pk": fatlink.pk,
        "fleet_name": fleet_label + esi_fleet_marker,
        "creator_name": _cached_main_character_name(request, fatlink.creator),
        "fleet_type": fatlink.fleet_type,
        "doctrine": fatlink.doctrine,
        "fleet_time": {
            "time": fatlink.created,
            "timestamp": fatlink.created.timestamp(),
        },
        "fats_number": fatlink.number_of_fats,
        "hash": fatlink.hash,
        "is_esilink": fatlink.is_esilink,
        "esi_fleet_id": fatlink.esi_fleet_id,
        "is_registered_on_esi": fatlink.is_registered_on_esi,
        "actions": "".join(actions_parts),
        "via_esi": via_esi,
    }


def convert_fats_to_dict(request: WSGIRequest, fat: Fat) -> dict:
    """
    Converts an AFat object into a dictionary

    :param request:
    :type request:
    :param fat:
    :type fat:
    :return:
    :rtype:
    """

    flags = _perm_flags(request)
    has_manage = flags["manage"]

    via_esi = "No"
    esi_fleet_marker = ""
    if fat.fatlink.is_esilink:
        via_esi = "Yes"
        badge_cls = (
            AFATUI.BADGE_ESI_TRACKING_ACTIVE.value
            if fat.fatlink.is_registered_on_esi
            else AFATUI.BADGE_ESI_TRACKING_INACTIVE.value
        )
        esi_fleet_marker = (
            f'<span class="{badge_cls}">{AFATUI.BADGE_ESI_TRACKING_TEXT.value}</span>'
        )

    actions_parts = []
    if has_manage:
        button_delete_fat = reverse(
            "afat:fatlinks_delete_fat", args=[fat.fatlink.hash, fat.id]
        )
        modal_body_text = _(
            "<p>Are you sure you want to remove {character_name} from this FAT link?</p>"
        ).format(character_name=fat.character.character_name)

        actions_parts.append(
            '<a class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteFatModal" '
            f'data-url="{button_delete_fat}" data-confirm-text="{AFATUI.BUTTON_DELETE_TEXT.value}" '
            f'data-body-text="{modal_body_text}">'
            '<i class="fa-solid fa-trash-can fa-fw"></i></a>'
        )

    fleet_time = fat.fatlink.created
    fleet_time_timestamp = fleet_time.timestamp()
    fleet_name = (
        fat.fatlink.fleet if fat.fatlink.fleet is not None else fat.fatlink.hash
    )

    return {
        "system": fat.system,
        "ship_type": fat.shiptype,
        "character_name": fat.character.character_name,
        "fleet_name": fleet_name + esi_fleet_marker,
        "doctrine": fat.fatlink.doctrine,
        "fleet_time": {"time": fleet_time, "timestamp": fleet_time_timestamp},
        "fleet_type": fat.fatlink.fleet_type,
        "via_esi": via_esi,
        "actions": "".join(actions_parts),
    }


def get_random_rgba_color():
    """
    Get a random RGB(a) color

    :return:
    :rtype:
    """

    red = random.randint(a=0, b=255)
    green = random.randint(a=0, b=255)
    blue = random.randint(a=0, b=255)
    alpha = 1

    return f"rgba({red}, {green}, {blue}, {alpha})"


def characters_with_permission(permission: Permission) -> models.QuerySet:
    """
    Returns queryset of characters that have the given permission
    in Auth through due to their associated user

    :param permission:
    :type permission:
    :return:
    :rtype:
    """

    # First, we need the users that have the permission
    users_qs = users_with_permission(permission=permission)

    # Now get their characters ... and sort them by userprofile and character name
    charater_qs = EveCharacter.objects.filter(
        character_ownership__user__in=users_qs
    ).order_by("-userprofile", "character_name")

    return charater_qs


def user_has_any_perms(user: User, perm_list, obj=None):
    """
    Return True if the user has each of the specified permissions. If
    an object is passed, check if the user has all required perms for it.
    """

    # Active superusers have all permissions.
    if user.is_active and user.is_superuser:
        return True

    return any(user.has_perm(perm=perm, obj=obj) for perm in perm_list)


def current_month_and_year() -> tuple[int, int]:
    """
    Return the current month and year

    :return: Month and year
    :rtype: Tuple[(int) Current Month, (int) Current Year]
    """

    current_month = timezone.now().month
    current_year = timezone.now().year

    return current_month, current_year


def get_fats_per_hour(fats) -> list:
    """
    Get the FATs per hour from the fats queryset

    :param fats:
    :type fats:
    :return:
    :rtype:
    """

    data_time = {i: fats.filter(fatlink__created__hour=i).count() for i in range(24)}

    return [
        list(data_time.keys()),
        list(data_time.values()),
        [get_random_rgba_color()],
    ]


def get_fat_per_weekday(fats) -> list:
    """
    Get the FATs per weekday from the fats queryset

    :param fats:
    :type fats:
    :return:
    :rtype:
    """

    return [
        [
            _("Monday"),
            _("Tuesday"),
            _("Wednesday"),
            _("Thursday"),
            _("Friday"),
            _("Saturday"),
            _("Sunday"),
        ],
        [fats.filter(fatlink__created__iso_week_day=i).count() for i in range(1, 8)],
        [get_random_rgba_color()],
    ]


def get_average_fats_by_corporations(
    fats: QuerySet[Fat], corporations: QuerySet[EveCorporationInfo]
) -> list:
    """
    Get the average FATs per corporation

    :param fats:
    :type fats:
    :param corporations:
    :type corporations:
    :return:
    :rtype:
    """

    data_avgs = {
        corp.corporation_name: round(
            fats.filter(corporation_eve_id=corp.corporation_id).count()
            / corp.member_count,
            2,
        )
        for corp in corporations
    }

    data_avgs = OrderedDict(sorted(data_avgs.items(), key=lambda x: x[1], reverse=True))

    return [
        list(data_avgs.keys()),
        list(data_avgs.values()),
        get_random_rgba_color(),
    ]
