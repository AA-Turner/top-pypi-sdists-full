"""
Statistics related views
"""

# Standard Library
import calendar
from collections import OrderedDict, defaultdict

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy

# Alliance Auth
from allianceauth.authentication.decorators import permissions_required
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.framework.api.evecharacter import get_main_character_from_evecharacter
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.helper.views import (
    characters_with_permission,
    current_month_and_year,
    get_average_fats_by_corporations,
    get_fat_per_weekday,
    get_fats_per_hour,
    get_random_rgba_color,
    user_has_any_perms,
)
from afat.models import Fat
from afat.providers import AppLogger
from afat.utils import get_or_create_alliance_info, get_or_create_corporation_info

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@login_required()
@permission_required(perm="afat.basic_access")
def overview(request: WSGIRequest, year: int = None) -> HttpResponse:
    """
    Statistics main view

    :param request:
    :type request:
    :param year:
    :type year:
    :return:
    :rtype:
    """

    if year is None:
        year = timezone.now().year

    logger.debug(f"Calculating statistics overview for year {year}")

    user_can_see_other_corps = False

    if user_has_any_perms(
        user=request.user,
        perm_list=["afat.stats_corporation_other", "afat.manage_afat"],
    ):
        user_can_see_other_corps = True
        basic_access_permission = Permission.objects.select_related("content_type").get(
            content_type__app_label="afat", codename="basic_access"
        )

        characters_with_access = characters_with_permission(
            permission=basic_access_permission
        )

        data = {"No Alliance": [1]}
        sanity_check = {}

        # Group corporations by alliance
        for character_with_access in list(characters_with_access):
            alliance_name = character_with_access.alliance_name or "No Alliance"
            corp_id = character_with_access.corporation_id
            corp_name = character_with_access.corporation_name

            if alliance_name not in data:
                data[alliance_name] = [character_with_access.alliance_id]

            if corp_id not in sanity_check:
                data[alliance_name].append((corp_id, corp_name))
                sanity_check[corp_id] = corp_id
    elif request.user.has_perm(perm="afat.stats_corporation_own"):
        data = [
            (
                request.user.profile.main_character.corporation_id,
                request.user.profile.main_character.corporation_name,
            )
        ]
    else:
        data = None

    months = _calculate_year_stats(request=request, year=year)

    logger.debug(f"Statistics overview data for year {year}: {months}")

    context = {
        "data": data,
        "charstats": months,
        "year": year,
        "year_current": timezone.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "user_can_see_other_corps": user_can_see_other_corps,
    }

    logger.info(msg=f"Statistics overview called by {request.user}")

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-overview.html",
        context=context,
    )


def _calculate_year_stats(request, year) -> dict:
    """
    Calculate statistics for the year

    :param request:
    :type request:
    :param year:
    :type year:
    :return:
    :rtype:
    """

    months = {"total": {}, "characters": []}

    # Get all characters for the user and order by userprofile and character name
    characters = EveCharacter.objects.filter(
        character_ownership__user=request.user
    ).order_by("-userprofile", "character_name")

    # Get all FATs for the year and group by character and month
    fats_in_year = (
        Fat.objects.filter(fatlink__created__year=year, character__in=characters)
        .values("character__character_id", "fatlink__created__month")
        .annotate(fat_count=Count("id"))
        .order_by("fatlink__created__month", "character__character_name")
    )

    # Initialize character data
    character_data = {
        char.character_id: {"name": char.character_name, "fats": {}}
        for char in characters
    }

    # Populate the months and character data
    for result in fats_in_year:
        month = int(result["fatlink__created__month"])
        char_id = int(result["character__character_id"])
        fat_count = int(result["fat_count"])

        # Update total fats per month
        if month not in months["total"]:
            months["total"][month] = 0

        months["total"][month] += fat_count

        # Update character fats per month
        character_data[char_id]["fats"][month] = fat_count

    # Sort character fats by month and add to the result,
    # excluding characters with no FATs
    for char_id, data in character_data.items():
        if data["fats"]:  # Only include characters with FATs
            sorted_fats = dict(sorted(data["fats"].items()))
            months["characters"].append((data["name"], sorted_fats, char_id))

    return months


@login_required()
@permission_required(perm="afat.basic_access")
def character(  # pylint: disable=too-many-locals
    request: WSGIRequest, charid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    Character statistics view

    :param request:
    :type request:
    :param charid:
    :type charid:
    :param year:
    :type year:
    :param month:
    :type month:
    :return:
    :rtype:
    """

    # Default to current year and month if not provided
    year = year or timezone.now().year
    month = month or timezone.now().month

    current_month, current_year = current_month_and_year()
    eve_character = EveCharacter.objects.get(character_id=charid)
    valid = [
        char.character for char in CharacterOwnership.objects.filter(user=request.user)
    ]

    can_view_character = True

    # Check if the user can view another corporation's statistics or manage AFAT
    if eve_character not in valid and not user_has_any_perms(
        user=request.user,
        perm_list=[
            "afat.stats_corporation_other",
            "afat.manage_afat",
        ],
    ):
        can_view_character = False

    # Check if the user is by any chance in the same corporation as the character
    # and can view own corporation statistics
    if (
        eve_character not in valid
        and eve_character.corporation_id
        == request.user.profile.main_character.corporation_id
        and request.user.has_perm(perm="afat.stats_corporation_own")
    ):
        can_view_character = True

    # If the user cannot view the character's statistics, send him home …
    if can_view_character is False:
        messages.warning(
            request=request,
            message=mark_safe(
                s=gettext(
                    "<h4>Warning!</h4>"
                    "<p>You do not have permission to view "
                    "statistics for this character.</p>"
                )
            ),
        )

        return redirect(to="afat:dashboard")

    fats = Fat.objects.filter(
        character__character_id=charid,
        fatlink__created__month=month,
        fatlink__created__year=year,
    )

    # Data for ship type pie chart
    data_ship_type = {}

    for fat in fats:
        if fat.ship_id in data_ship_type:
            continue

        data_ship_type[fat.ship_id] = fats.filter(ship=fat.ship).count()

    colors = []

    for _ in data_ship_type:
        bg_color_str = get_random_rgba_color()
        colors.append(bg_color_str)

    data_ship_type = [
        # Ship type can be None, so we need to convert to string here
        list(str(key) for key in data_ship_type),
        list(data_ship_type.values()),
        colors,
    ]

    # Data for by timeline Chart
    data_time = get_fats_per_hour(fats)

    context = {
        "character": eve_character,
        "month": month,
        "month_current": current_month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "month_with_year": f"{year}{month:02d}",
        "month_current_with_year": f"{current_year}{current_month:02d}",
        "month_next_with_year": f"{year}{int(month) + 1:02d}",
        "month_prev_with_year": f"{year}{int(month) - 1:02d}",
        "year": year,
        "year_current": current_year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_ship_type": data_ship_type,
        "data_time": data_time,
        "fats": fats,
    }

    month_name = calendar.month_name[int(month)]
    logger.info(
        msg=(
            f"Character statistics for {eve_character} ({month_name} {year}) "
            f"called by {request.user}"
        )
    )

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-character.html",
        context=context,
    )


@login_required()
@permissions_required(
    perm=(
        "afat.stats_corporation_other",
        "afat.stats_corporation_own",
        "afat.manage_afat",
    )
)
def ajax_get_monthly_fats_for_main_character(
    request: WSGIRequest,
    corporation_id: int,
    character_id: int,
    year: int,
    month: int,
) -> JsonResponse:
    """
    Ajax call :: Get monthly FATs for the main characters registered characters

    :param request: The request object
    :type request: WSGIRequest
    :param character_id: The main character
    :type character_id: EveCharacter
    :param year: The year
    :type year: int
    :param month: The month
    :type month: int
    :return: JSON response
    :rtype: JsonResponse
    """

    main_character = EveCharacter.objects.get(character_id=character_id)

    # Check character has permission to view other corps stats
    if int(request.user.profile.main_character.corporation_id) != int(
        main_character.corporation_id
    ) and not user_has_any_perms(
        user=request.user,
        perm_list=["afat.stats_corporation_other", "afat.manage_afat"],
    ):
        return JsonResponse(data="", safe=False)

    fats_per_character = (
        Fat.objects.filter(
            # corporation_eve_id=corporation_id,
            character__character_ownership__user=main_character.character_ownership.user,
            fatlink__created__month=month,
            fatlink__created__year=year,
        )
        .values(
            "corporation_eve_id",
            "character__character_id",
            "character__character_name",
            "character__corporation_id",
            "character__corporation_name",
        )
        .annotate(fat_count=Count("id"))
    )

    # if main_character.corporation_id != corporation_id:
    #     fats_per_character = fats_per_character.filter(
    #         character__corporation_id=corporation_id
    #     )

    info_button_text = gettext_lazy(
        "This character is in a different corporation and their FATs are "
        "not counted towards the statistics of the main corporation."
    )

    info_button = (
        "<sup>"
        f'<span class="ms-1 cursor-pointer"title="{info_button_text}" data-bs-tooltip="afat">'
        '<i class="fa-solid fa-circle-info"></i>'
        "</span>"
        "</sup>"
    )

    logger.debug("Fat per character: %s", fats_per_character)

    return JsonResponse(
        data=[
            {
                "character": item,
                "character_id": item["character__character_id"],
                "character_name": (
                    item["character__character_name"]
                    if item["corporation_eve_id"] == corporation_id
                    else f'{item["character__character_name"]} ({item["character__corporation_name"]}){info_button}'
                ),
                "fat_count": item["fat_count"],
                "show_details_button": (
                    f'<a class="btn btn-primary btn-sm" href="{reverse(viewname="afat:statistics_character", args=[item["character__character_id"], year, month])}"><i class="fa-solid fa-eye"></i></a>'
                ),
                "in_main_corp": item["corporation_eve_id"] == corporation_id,
            }
            for item in fats_per_character
        ],
        safe=False,
    )


@login_required()
@permissions_required(
    perm=(
        "afat.stats_corporation_other",
        "afat.stats_corporation_own",
        "afat.manage_afat",
    )
)
def corporation(  # pylint: disable=too-many-statements too-many-branches too-many-locals
    request: WSGIRequest, corpid: int = 0000, year: int = None, month: int = None
) -> HttpResponse:
    """
    Corp statistics view

    :param request:
    :type request:
    :param corpid:
    :type corpid:
    :param year:
    :type year:
    :param month:
    :type month:
    :return:
    :rtype:
    """

    # Default to current year if not provided
    year = year or timezone.now().year

    current_month, current_year = current_month_and_year()

    # Check character has permission to view other corps stats
    if int(request.user.profile.main_character.corporation_id) != int(
        corpid
    ) and not user_has_any_perms(
        user=request.user,
        perm_list=["afat.stats_corporation_other", "afat.manage_afat"],
    ):
        messages.warning(
            request=request,
            message=mark_safe(
                s=gettext(
                    "<h4>Warning!</h4>"
                    "<p>You do not have permission to view statistics "
                    "for that corporation.</p>"
                )
            ),
        )

        return redirect(to="afat:dashboard")

    corp = get_or_create_corporation_info(corporation_id=corpid)
    corp_name = corp.corporation_name

    if not month:
        fats_per_year = (
            Fat.objects.filter(
                corporation_eve_id=corpid,
                fatlink__created__year=year,
            )
            .values("fatlink__created__month")
            .annotate(fat_count=Count("id"))
        )

        months = []
        fats_per_year_total = 0

        for i in range(1, 13):
            corp_fats = next(
                (
                    item["fat_count"]
                    for item in fats_per_year
                    if item["fatlink__created__month"] == i
                ),
                0,
            )
            fats_per_year_total += corp_fats

            avg_fats = 0
            if corp.member_count > 0:
                avg_fats = corp_fats / corp.member_count

            if corp_fats > 0:
                months.append((i, corp_fats, round(avg_fats, 2)))

        context = {
            "corporation": corp_name,
            "months": months,
            "corpid": corpid,
            "year": year,
            "fats_per_year": fats_per_year_total,
            "year_current": current_year,
            "year_prev": int(year) - 1,
            "year_next": int(year) + 1,
            "type": 0,
        }

        return render(
            request=request,
            template_name="afat/view/statistics/statistics-corporation-year-overview.html",
            context=context,
        )

    fats = Fat.objects.filter(
        fatlink__created__month=month,
        fatlink__created__year=year,
        corporation_eve_id=corpid,
    ).select_related("character")

    # Data for Stacked Bar Graph
    # (label, color, [list of data for stack])
    data = defaultdict(lambda: defaultdict(int))
    character_ids = set()

    character_names_list = sorted(
        {fat.character.character_name for fat in fats}, key=str.lower
    )

    for fat in fats:
        data[fat.ship.name][fat.character.character_name] += 1
        character_ids.add(fat.character.character_id)

    data_stacked = [
        character_names_list,
        [
            (
                shiptype,
                get_random_rgba_color(),
                [counts[char] for char in character_names_list],
            )
            for shiptype, counts in data.items()
        ],
    ]

    # Data for By Time
    data_time = get_fats_per_hour(fats)

    # Data for By Weekday
    data_weekday = get_fat_per_weekday(fats)

    chars = {}
    main_chars = {}

    characters = EveCharacter.objects.filter(
        character_id__in=character_ids
    ).select_related("character_ownership__user")
    character_fat_counts = fats.values("character_id").annotate(fat_count=Count("id"))
    character_fat_map = {
        item["character_id"]: item["fat_count"] for item in list(character_fat_counts)
    }

    for char in characters:
        fat_c = character_fat_map.get(char.id, 0)
        chars[char.character_name] = (fat_c, char.character_id)
        main_character = get_main_character_from_evecharacter(character=char)

        if main_character and main_character.character_id not in main_chars:
            main_chars[main_character.character_id] = {
                "name": main_character.character_name,
                "id": main_character.character_id,
                "corporation_id": main_character.corporation_id,
                "corporation_name": main_character.corporation_name,
                "fats": fat_c,
            }
        elif main_character:
            main_chars[main_character.character_id]["fats"] += fat_c

    context = {
        "corp": corp,
        "corporation": corp_name,
        "month": month,
        "month_current": timezone.now().month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "month_with_year": f"{year}{month:02d}",
        "month_current_with_year": f"{current_year}{current_month:02d}",
        "month_next_with_year": f"{year}{int(month) + 1:02d}",
        "month_prev_with_year": f"{year}{int(month) - 1:02d}",
        "year": year,
        "year_current": timezone.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_stacked": data_stacked,
        "data_time": data_time,
        "data_weekday": data_weekday,
        "chars": chars,
        "main_chars": main_chars,
    }

    month_name = calendar.month_name[int(month)]

    logger.info(
        msg=(
            f"Corporation statistics for {corp_name} ({month_name} {year}) "
            f"called by {request.user}"
        )
    )

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-corporation.html",
        context=context,
    )


@login_required()
@permissions_required(perm=("afat.stats_corporation_other", "afat.manage_afat"))
def alliance(  # pylint: disable=too-many-statements too-many-branches too-many-locals
    request: WSGIRequest, allianceid: int, year: int = None, month: int = None
) -> HttpResponse:
    """
    Alliance statistics view

    :param request:
    :type request:
    :param allianceid:
    :type allianceid:
    :param year:
    :type year:
    :param month:
    :type month:
    :return:
    :rtype:
    """

    # Default to current year if not provided
    year = year or timezone.now().year

    ally = (
        get_or_create_alliance_info(alliance_id=allianceid)
        if allianceid != "000"
        else None
    )
    alliance_name = ally.alliance_name if ally else "No Alliance"

    current_month, current_year = current_month_and_year()

    if not month:
        months = []

        ally_fats_by_month = (
            Fat.objects.filter(
                alliance_eve_id=allianceid,
                fatlink__created__year=year,
            )
            .order_by("fatlink__created__month")
            .values("fatlink__created__month")
            .annotate(fat_count=Count("id"))
        )

        for entry in ally_fats_by_month:
            months.append((entry["fatlink__created__month"], entry["fat_count"]))

        context = {
            "alliance": alliance_name,
            "months": months,
            "allianceid": allianceid,
            "year": year,
            "year_current": current_year,
            "year_prev": int(year) - 1,
            "year_next": int(year) + 1,
            "type": 1,
        }

        # /fleet-activity-tracking/statistics/alliance/<alliance_id>/<year>/
        return render(
            request=request,
            template_name="afat/view/statistics/statistics-alliance-year-overview.html",
            context=context,
        )

    fats = Fat.objects.filter(
        alliance_eve_id=allianceid,
        fatlink__created__month=month,
        fatlink__created__year=year,
    )

    # Data for ship type pie chart
    data_ship_type = fats.values("shiptype").annotate(count=Count("shiptype"))
    colors = [get_random_rgba_color() for _ in data_ship_type]

    data_ship_type = [
        [str(item["shiptype"]) for item in list(data_ship_type)],
        [item["count"] for item in list(data_ship_type)],
        colors,
    ]

    # Fats by corp and ship type
    data = {}
    corps_in_fats = set()

    for fat in fats:
        shiptype = fat.ship.name
        corp_name = fat.character.corporation_name

        if shiptype not in data:
            data[shiptype] = {}

        if corp_name not in data[shiptype]:
            data[shiptype][corp_name] = 0

        data[shiptype][corp_name] += 1
        corps_in_fats.add(corp_name)

    corps_in_fats = list(corps_in_fats)

    if None in data:
        data["Unknown"] = data.pop(None)

    data_stacked = [
        (key, get_random_rgba_color(), [value.get(corp, 0) for corp in corps_in_fats])
        for key, value in data.items()
    ]

    data_stacked = [corps_in_fats, data_stacked]

    corporations_in_alliance = EveCorporationInfo.objects.filter(alliance=ally)

    # Avg fats by corp
    data_avgs = get_average_fats_by_corporations(
        fats=fats, corporations=corporations_in_alliance
    )

    # Fats by Time
    data_time = get_fats_per_hour(fats=fats)

    # Fats by weekday
    data_weekday = get_fat_per_weekday(fats=fats)

    # Corp list
    corps = {}

    for corp in corporations_in_alliance:
        c_fats = fats.filter(corporation_eve_id=corp.corporation_id).count()
        avg = c_fats / corp.member_count
        corps[corp] = (corp.corporation_id, c_fats, round(avg, 2))

    corps = OrderedDict(sorted(corps.items(), key=lambda x: x[1][2], reverse=True))

    context = {
        "alliance": alliance_name,
        "ally": ally,
        "month": month,
        "month_current": current_month,
        "month_prev": int(month) - 1,
        "month_next": int(month) + 1,
        "month_with_year": f"{year}{month:02d}",
        "month_current_with_year": f"{current_year}{current_month:02d}",
        "month_next_with_year": f"{year}{int(month) + 1:02d}",
        "month_prev_with_year": f"{year}{int(month) - 1:02d}",
        "year": year,
        "year_current": current_year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
        "data_stacked": data_stacked,
        "data_avgs": data_avgs,
        "data_time": data_time,
        "data_weekday": data_weekday,
        "corps": corps,
        "data_ship_type": data_ship_type,
    }

    month_name = calendar.month_name[int(month)]
    logger.info(
        msg=(
            f"Alliance statistics for {alliance_name} ({month_name} {year}) "
            f"called by {request.user}"
        )
    )

    return render(
        request=request,
        template_name="afat/view/statistics/statistics-alliance.html",
        context=context,
    )
