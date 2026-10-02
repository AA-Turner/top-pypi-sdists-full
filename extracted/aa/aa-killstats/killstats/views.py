"""App Views"""

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.services.hooks import get_extension_logger
from esi.decorators import token_required

# AA Killstats
from killstats import __title__, __version__
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


@login_required
@permission_required("killstats.basic_access")
def react_base(request, *args, **kwargs):  # pylint: disable=unused-argument
    """React Frontend SPA Base View."""
    context = {
        "app_name": "killstats",
        "title": "Killstats",
        "version": __version__,
    }
    return render(request, "killstats/react_killboard.html", context=context)


@login_required
@token_required(scopes=("publicData"))
@permission_required(["killstats.admin_access"])
def add_corp(request, token):
    char = get_object_or_404(EveCharacter, character_id=token.character_id)

    # Check if it is a NPC Corporation
    if not char.corporation_id or char.corporation_id < 10_000_000:
        msg = _("Cannot add NPC Corporation to Killstats")
        messages.error(request, msg)
        return redirect("killstats:react_base")

    corp = EveCorporationInfo.objects.get_or_create(
        corporation_id=char.corporation_id,
        defaults={
            "member_count": 0,
            "corporation_ticker": char.corporation_ticker,
            "corporation_name": char.corporation_name,
        },
    )[0]

    audit = CorporationsAudit.objects.update_or_create(corporation=corp, owner=char)[0]

    msg = (
        f"{audit.corporation.corporation_name} successfully added/updated to Killstats"
    )
    messages.info(request, msg)
    return redirect("killstats:corporation", entity_id=char.corporation_id)


@login_required
@token_required(scopes=("publicData"))
@permission_required(["killstats.admin_access"])
def add_alliance(request, token):
    char = get_object_or_404(EveCharacter, character_id=token.character_id)

    # Check if character belongs to an NPC Corporation
    if not char.corporation_id or char.corporation_id < 10_000_000:
        msg = _("Cannot add Alliance for a character belonging to an NPC Corporation")
        messages.error(request, msg)
        return redirect("killstats:react_base")

    # Check if character belongs to a valid player Alliance
    if not char.alliance_id or char.alliance_id < 10_000_000:
        msg = _("Character does not belong to a valid player Alliance")
        messages.error(request, msg)
        return redirect("killstats:react_base")

    try:
        alliance = EveAllianceInfo.objects.get(
            alliance_id=char.alliance_id,
        )
        audit = AlliancesAudit.objects.update_or_create(alliance=alliance, owner=char)[
            0
        ]
        msg = _("{alliance_name} successfully added/updated to Killstats").format(
            alliance_name=audit.alliance.alliance_name,
        )
    except ObjectDoesNotExist as exc:  # pylint: disable=broad-exception-caught
        msg = _("Alliance {alliance_name} could not be found in Alliance Auth").format(
            alliance_name=char.alliance_name,
        )
        messages.warning(request, msg)
        logger.error(
            "Error fetching alliance data for alliance_id %s: %s",
            char.alliance_id,
            exc,
        )
        return redirect("killstats:react_base")

    messages.info(request, msg)
    return redirect("killstats:alliance", entity_id=char.alliance_id)
