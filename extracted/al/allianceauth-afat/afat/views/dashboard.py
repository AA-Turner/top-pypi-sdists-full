"""
Dashboard related views
"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.evecharacter import get_user_from_evecharacter
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.helper.association import get_all_characters_with_fats_from_user
from afat.helper.views import convert_fatlinks_to_dict, convert_fats_to_dict
from afat.models import Fat, FatLink
from afat.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@login_required()
@permission_required(perm="afat.basic_access")
def overview(request: WSGIRequest) -> HttpResponse:
    """
    Dashboard view

    :param request:
    :type request:
    :return:
    :rtype:
    """

    characters = get_all_characters_with_fats_from_user(request.user)

    context = {"characters": characters}

    logger.info(msg=f"Module called by {request.user}")

    return render(
        request=request,
        template_name="afat/view/dashboard/dashboard.html",
        context=context,
    )


@login_required
@permission_required(perm="afat.basic_access")
def ajax_recent_get_fats_by_character(
    request: WSGIRequest, charid: int
) -> JsonResponse:
    """
    Ajax call :: get all FATs for a given character

    :param request:
    :type request:
    :param charid:
    :type charid:
    :return:
    :rtype:
    """

    character = EveCharacter.objects.get(character_id=charid)
    user_by_character = get_user_from_evecharacter(character=character)

    # Check if the user has access to the character
    if user_by_character == request.user:
        fats = (
            Fat.objects.select_related_default()
            .filter(character=character)
            .order_by("fatlink__created")
            .reverse()[:10]
        )

        character_fat_rows = [
            convert_fats_to_dict(request=request, fat=fat) for fat in fats
        ]

        return JsonResponse(data=character_fat_rows, safe=False)

    # If the user does not have access to the character
    return JsonResponse(data=[], safe=False)


@login_required
@permission_required(perm="afat.basic_access")
def ajax_get_recent_fatlinks(request: WSGIRequest) -> JsonResponse:
    """
    Ajax call :: get recent fat links for the dashboard datatable

    :param request:
    :type request:
    :return:
    :rtype:
    """

    fatlink_ids = list(
        FatLink.objects.select_related_default()
        .order_by("-created")[:10]
        .values_list("id", flat=True)
    )

    fatlinks = FatLink.objects.filter(id__in=fatlink_ids).order_by("-created")

    fatlink_rows = [
        convert_fatlinks_to_dict(
            request=request,
            fatlink=fatlink,
            close_esi_redirect=reverse(viewname="afat:dashboard"),
        )
        for fatlink in fatlinks
    ]

    return JsonResponse(data=fatlink_rows, safe=False)
