from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from esi.decorators import token_required
from esi.models import Token

from . import __version__
from .models import AllianceToken, CorporationToken
from .tasks import update_alliance_contacts, update_corporation_contacts


@login_required
def index(_: HttpRequest) -> HttpResponseRedirect:
    return redirect("aa_contacts:react_view")


@login_required
def react_view(request: HttpRequest) -> HttpResponse:
    context = {
        "version": __version__,
    }

    return render(request, "aa_contacts/react_base.html", context=context)


@login_required
@permission_required("aa_contacts.manage_alliance_contacts")
@token_required(scopes=["esi-alliances.read_contacts.v1"])
def add_alliance_token(request: HttpRequest, token: Token) -> HttpResponseRedirect:
    char = get_object_or_404(EveCharacter, character_id=token.character_id)

    if char.alliance_id is None:
        messages.error(
            request, _("You need to be in an alliance to add alliance contacts.")
        )
        return redirect("aa_contacts:index")

    try:
        alliance = char.alliance
    except EveAllianceInfo.DoesNotExist:
        alliance = EveAllianceInfo.objects.create_alliance(char.alliance_id)

    if AllianceToken.objects.filter(alliance=alliance).exists():
        messages.error(
            request, _("Alliance contacts for your alliance are already being tracked.")
        )
        return redirect("aa_contacts:index")

    AllianceToken.objects.create(alliance=alliance, token=token)
    update_alliance_contacts.delay(alliance.alliance_id)

    messages.success(request, _("Alliance contacts are now being tracked."))
    return redirect("aa_contacts:index")


@login_required
@permission_required("aa_contacts.manage_corporation_contacts")
@token_required(scopes=["esi-corporations.read_contacts.v1"])
def add_corporation_token(request: HttpRequest, token: Token) -> HttpResponseRedirect:
    char = get_object_or_404(EveCharacter, character_id=token.character_id)

    try:
        corporation = char.corporation
    except EveCorporationInfo.DoesNotExist:
        corporation = EveCorporationInfo.objects.create_corporation(char.corporation_id)

    if CorporationToken.objects.filter(corporation=corporation).exists():
        messages.error(
            request,
            _("Corporation contacts for your corporation are already being tracked."),
        )
        return redirect("aa_contacts:index")

    CorporationToken.objects.create(corporation=corporation, token=token)
    update_corporation_contacts.delay(corporation.corporation_id)

    messages.success(request, _("Corporation contacts are now being tracked."))
    return redirect("aa_contacts:index")
