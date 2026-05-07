"""
Fat links related views
"""

# Standard Library
import re
from datetime import timedelta

# Third Party
from eve_sde.models import ItemType, SolarSystem

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

# Alliance Auth
from allianceauth.authentication.decorators import permissions_required
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger
from esi.decorators import token_required
from esi.models import Token

# Alliance Auth AFAT
from afat import __title__
from afat.constants import RegexPattern
from afat.forms import (
    AFatClickFatForm,
    AFatEsiFatForm,
    AFatManualFatForm,
    FatLinkEditForm,
    FleetSnapshot,
)
from afat.handler import esi_handler
from afat.helper.fatlinks import get_doctrines, get_esi_fleet_information_by_user
from afat.helper.time import get_time_delta
from afat.helper.views import convert_fats_to_dict
from afat.models import (
    Duration,
    Fat,
    FatLink,
    FleetType,
    Log,
    Setting,
    get_hash_on_save,
)
from afat.providers import AppLogger, esi
from afat.tasks import process_fats
from afat.utils import get_or_create_character, write_log

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@login_required()
@permission_required("afat.basic_access")
def overview(request: WSGIRequest, year: int = None) -> HttpResponse:
    """
    Fat links view

    :param request:
    :type request:
    :param year:
    :type year:
    :return:
    :rtype:
    """

    if year is None:
        year = timezone.now().year

    context = {
        "year": year,
        "year_current": timezone.now().year,
        "year_prev": int(year) - 1,
        "year_next": int(year) + 1,
    }

    logger.info(msg=f"FAT link list called by {request.user}")

    return render(
        request=request,
        template_name="afat/view/fatlinks/fatlinks-overview.html",
        context=context,
    )


@login_required()
@permissions_required(("afat.manage_afat", "afat.add_fatlink"))
def add_fatlink(request: WSGIRequest) -> HttpResponse:
    """
    Add fat link view

    :param request:
    :type request:
    :return:
    :rtype:
    """

    fleet_types = FleetType.objects.filter(is_enabled=True).order_by("name")

    context = {
        "default_expiry_time": Setting.get_setting(
            Setting.Field.DEFAULT_FATLINK_EXPIRY_TIME
        ),
        "esi_fleet": get_esi_fleet_information_by_user(request.user),
        "esi_fatlink_form": AFatEsiFatForm(),
        "manual_fatlink_form": AFatClickFatForm(),
        "doctrines": get_doctrines(),
        "fleet_types": fleet_types,
    }

    logger.info(msg=f"Add FAT link view called by {request.user}")

    return render(
        request=request,
        template_name="afat/view/fatlinks/fatlinks-add-fatlink.html",
        context=context,
    )


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def create_clickable_fatlink(request: WSGIRequest) -> HttpResponseRedirect:
    """
    Create a clickable fat link

    :param request:
    :type request:
    :return:
    :rtype:
    """

    if request.method == "POST":
        form = AFatClickFatForm(data=request.POST)

        if form.is_valid():
            fatlink_hash = get_hash_on_save()

            fatlink = FatLink()
            fatlink.fleet = form.cleaned_data["name"]
            fatlink.fleet_type = form.cleaned_data["type"]
            fatlink.doctrine = form.cleaned_data["doctrine"]
            fatlink.creator = request.user
            fatlink.hash = fatlink_hash
            fatlink.created = timezone.now()
            fatlink.save()

            dur = Duration()
            dur.fleet = FatLink.objects.get(hash=fatlink_hash)
            dur.duration = form.cleaned_data["duration"]
            dur.save()

            # Writing DB log
            fleet_type = (
                f" (Fleet type: {fatlink.fleet_type})" if fatlink.fleet_type else ""
            )

            write_log(
                request=request,
                log_event=Log.Event.CREATE_FATLINK,
                log_text=(
                    f'FAT link with name "{form.cleaned_data["name"]}"{fleet_type} and '
                    f'a duration of {form.cleaned_data["duration"]} minutes was created'
                ),
                fatlink_hash=fatlink.hash,
            )

            logger.info(
                msg=(
                    f'FAT link "{fatlink_hash}" with name '
                    f'"{form.cleaned_data["name"]}"{fleet_type} and a duration '
                    f'of {form.cleaned_data["duration"]} minutes was created '
                    f"by {request.user}"
                )
            )

            messages.success(
                request=request,
                message=mark_safe(
                    s=_(
                        "<h4>Success!</h4>"
                        "<p>Clickable FAT link created!</p>"
                        "<p>Make sure to give your fleet members the link to "
                        "click so that they get credit for this fleet.</p>"
                    )
                ),
            )

            return redirect(
                to="afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash
            )

        messages.error(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Error!</h4>"
                    "<p>Something went wrong when attempting "
                    "to submit your clickable FAT link.</p>"
                )
            ),
        )

        return redirect("afat:fatlinks_add_fatlink")

    messages.warning(
        request=request,
        message=mark_safe(
            s=_(
                "<h4>Warning!</h4>"
                '<p>You must fill out the form on the "Add FAT link" '
                "page to create a clickable FAT link</p>"
            )
        ),
    )

    return redirect(to="afat:fatlinks_add_fatlink")


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
@token_required(scopes=["esi-fleets.read_fleet.v1"])
def create_esi_fatlink_callback(  # pylint: disable=too-many-locals
    request: WSGIRequest, token, fatlink_hash: str
) -> HttpResponseRedirect:
    """
    Helper :: create ESI link (callback, used when coming back from character selection)

    :param request:
    :type request:
    :param token:
    :type token:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    # Check if there is a fleet
    operation = esi.client.Fleets.GetCharactersCharacterIdFleet(
        character_id=token.character_id, token=token
    )

    try:

        fleet_from_esi = esi_handler.result(operation=operation, use_etag=False)
    except Exception:  # pylint: disable=broad-exception-caught
        # Not in a fleet
        messages.warning(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Warning!</h4>"
                    "<p>To use the ESI function, you need to be in fleet and you need "
                    "to be the fleet boss! You can create a clickable FAT link and "
                    "share it, if you like.</p>"
                )
            ),
        )

        # Return to "Add FAT link" view
        return redirect(to="afat:fatlinks_add_fatlink")

    # check if this character already has a fleet
    creator_character = EveCharacter.objects.get(character_id=token.character_id)
    registered_fleets_for_creator = FatLink.objects.select_related_default().filter(
        is_esilink=True,
        is_registered_on_esi=True,
        character__character_name=creator_character.character_name,
    )

    fleet_already_registered = False
    character_has_registered_fleets = False
    registered_fleets_to_close = []

    if registered_fleets_for_creator.count() > 0:
        character_has_registered_fleets = True

        for registered_fleet in registered_fleets_for_creator:
            if registered_fleet.esi_fleet_id == fleet_from_esi.fleet_id:
                # Character already has a fleet
                fleet_already_registered = True
            else:
                registered_fleets_to_close.append(
                    {"registered_fleet": registered_fleet}
                )

    # If the FC already has a fleet, and it is the same as already registered,
    # just throw a warning
    if fleet_already_registered is True:
        messages.warning(
            request=request,
            message=mark_safe(
                s=format_lazy(
                    _(
                        "<h4>Warning!</h4>"
                        '<p>Fleet with ID "{fleet_id}" for your character '
                        "{creator__character_name} has already been registered and "
                        "pilots joining this fleet are automatically tracked.</p>"
                    ),
                    fleet_id=fleet_from_esi.fleet_id,
                    creator__character_name=creator_character.character_name,
                ),
            ),
        )

        # Return to "Add FAT link" view
        return redirect(to="afat:fatlinks_add_fatlink")

    # If it's a new fleet, remove all former registered fleets, if there are any
    if (
        character_has_registered_fleets is True
        and fleet_already_registered is False
        and len(registered_fleets_to_close) > 0
    ):
        for registered_fleet_to_close in registered_fleets_to_close:
            reason = (
                f"FC has opened a new fleet with the "
                f"character {creator_character.character_name}"
            )

            logger.info(
                msg=(
                    "Closing ESI FAT link with hash "
                    f'"{registered_fleet_to_close["registered_fleet"].hash}". '
                    f"Reason: {reason}"
                )
            )

            registered_fleet_to_close["registered_fleet"].is_registered_on_esi = False
            registered_fleet_to_close["registered_fleet"].save()

    # Check if we deal with the fleet boss here
    operation = esi.client.Fleets.GetFleetsFleetIdMembers(
        fleet_id=fleet_from_esi.fleet_id, token=token
    )
    try:
        esi_fleet_member = esi_handler.result(operation=operation, use_etag=False)
    except Exception:  # pylint: disable=broad-exception-caught
        messages.warning(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Warning!</h4>"
                    "<p>Not Fleet Boss! Only the fleet boss can utilize the ESI "
                    "function. You can create a clickable FAT link and share it, "
                    "if you like.</p>"
                )
            ),
        )

        # Return to "Add FAT link" view
        return redirect(to="afat:fatlinks_add_fatlink")

    creator_character = EveCharacter.objects.get(character_id=token.character_id)

    # Create the fat link
    fatlink = FatLink(
        created=timezone.now(),
        fleet=request.session["fatlink_form__name"],
        doctrine=request.session["fatlink_form__doctrine"],
        creator=request.user,
        character=creator_character,
        hash=fatlink_hash,
        is_esilink=True,
        is_registered_on_esi=True,
        esi_fleet_id=fleet_from_esi.fleet_id,
        fleet_type=request.session["fatlink_form__type"],
    )

    # Save it
    fatlink.save()

    # Writing DB log
    fleet_type = f"(Fleet type: {fatlink.fleet_type})" if fatlink.fleet_type else ""

    write_log(
        request=request,
        log_event=Log.Event.CREATE_FATLINK,
        log_text=(
            f'ESI FAT link with name "{request.session["fatlink_form__name"]}" '
            f"{fleet_type} was created by {request.user}"
        ),
        fatlink_hash=fatlink.hash,
    )

    logger.info(
        msg=(
            f'ESI FAT link "{fatlink_hash}" with name '
            f'"{request.session["fatlink_form__name"]}" {fleet_type} '
            f"was created by {request.user}"
        )
    )

    # Clear session
    del request.session["fatlink_form__name"]
    del request.session["fatlink_form__type"]

    # Process fleet members in the background
    process_fats.delay(
        data_list=[fleet_member.dict() for fleet_member in esi_fleet_member],
        data_source="esi",
        fatlink_hash=fatlink_hash,
    )

    messages.success(
        request=request,
        message=mark_safe(
            s=_(
                "<h4>Success!</h4>"
                "<p>FAT link Created!</p>"
                "<p>FATs have been queued, they may take a few minutes to show up.</p>"
                "<p>Pilots who join later will be automatically added until you "
                "close or leave the fleet in-game.</p>"
            )
        ),
    )

    return redirect(to="afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash)


@login_required()
def create_esi_fatlink(request: WSGIRequest) -> HttpResponseRedirect:
    """
    Create an ESI fat link

    :param request:
    :type request:
    :return:
    :rtype:
    """

    fatlink_form = AFatEsiFatForm(data=request.POST)

    if fatlink_form.is_valid():
        fatlink_hash = get_hash_on_save()

        request.session["fatlink_form__name"] = fatlink_form.cleaned_data["name_esi"]
        request.session["fatlink_form__doctrine"] = fatlink_form.cleaned_data[
            "doctrine_esi"
        ]
        request.session["fatlink_form__type"] = fatlink_form.cleaned_data["type_esi"]

        return redirect(
            to="afat:fatlinks_create_esi_fatlink_callback", fatlink_hash=fatlink_hash
        )

    messages.error(
        request=request,
        message=mark_safe(
            s=_(
                "<h4>Error!</h4>"
                "<p>Something went wrong when attempting to "
                "submit your ESI FAT link.</p>"
            )
        ),
    )

    return redirect(to="afat:fatlinks_add_fatlink")


@login_required()
@permission_required("afat.basic_access")
@token_required(
    scopes=[
        "esi-location.read_location.v1",
        "esi-location.read_ship_type.v1",
        "esi-location.read_online.v1",
    ]
)
def add_fat(
    request: WSGIRequest, token: Token, fatlink_hash: str
) -> HttpResponseRedirect:
    """
    Add fat to a clickable fat link

    :param request: The request object
    :type request: WSGIRequest
    :param token: The ESI token
    :type token: Token
    :param fatlink_hash: The fat link hash
    :type fatlink_hash: str
    :return: Redirect to dashboard
    :rtype: HttpResponseRedirect
    """

    try:
        fleet = FatLink.objects.get(hash=fatlink_hash, is_esilink=False)
    except FatLink.DoesNotExist:
        messages.warning(
            request,
            mark_safe(_("<h4>Warning!</h4><p>The hash provided is not valid.</p>")),
        )

        return redirect("afat:dashboard")

    if (
        timezone.now() - timedelta(minutes=Duration.objects.get(fleet=fleet).duration)
        >= fleet.created
    ):
        messages.warning(
            request,
            mark_safe(
                _(
                    "<h4>Warning!</h4>"
                    "<p>Sorry, that FAT link is expired. "
                    "If you were on that fleet, contact your FC about "
                    "having your FAT manually added.</p>"
                )
            ),
        )

        return redirect("afat:dashboard")

    character = EveCharacter.objects.get(character_id=token.character_id)
    operation = esi.client.Location.GetCharactersCharacterIdOnline(
        character_id=token.character_id, token=token
    )

    if not esi_handler.result(operation=operation, use_etag=False).online:
        messages.warning(
            request,
            mark_safe(
                format_lazy(
                    _(
                        "<h4>Warning!</h4>"
                        "<p>Cannot register the fleet participation for "
                        "{character_name}. The character needs to be online.</p>"
                    ),
                    character_name=character.character_name,
                )
            ),
        )

        return redirect("afat:dashboard")

    location = esi_handler.result(
        operation=esi.client.Location.GetCharactersCharacterIdLocation(
            character_id=token.character_id, token=token
        ),
        use_etag=False,
    )
    solar_system = SolarSystem.objects.get(id=location.solar_system_id)

    current_ship = esi_handler.result(
        operation=esi.client.Location.GetCharactersCharacterIdShip(
            character_id=token.character_id, token=token
        ),
        use_etag=False,
    )
    ship = ItemType.objects.get(id=current_ship.ship_type_id)

    logger.debug(
        f"Processing character {character} in {solar_system.name} flying a {ship.name} "
        f"for FAT link with hash {fatlink_hash}"
    )

    try:
        Fat.objects.create(
            fatlink=fleet,
            character=character,
            solar_system=solar_system,
            ship=ship,
            corporation_eve_id=character.corporation_id,
            alliance_eve_id=character.alliance_id,
        )
        messages.success(
            request,
            mark_safe(
                format_lazy(
                    _(
                        '<h4>Success!</h4><p>FAT registered for {character_name} at "{fleet_name}"</p>'
                    ),
                    character_name=character.character_name,
                    fleet_name=fleet.fleet or fleet.hash,
                )
            ),
        )
        logger.info(
            f'Participation for fleet "{fleet.fleet or fleet.hash}" registered for {character.character_name}'
        )
    except IntegrityError:
        messages.warning(
            request,
            mark_safe(
                format_lazy(
                    _(
                        "<h4>Warning!</h4><p>The selected charcter ({character_name}) is already registered for this FAT link.</p>"
                    ),
                    character_name=character.character_name,
                )
            ),
        )

    return redirect("afat:dashboard")


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def process_fatlink_name_change(
    request: WSGIRequest, fatlink_hash: str
) -> HttpResponseRedirect:
    """
    Process fat link name change form

    :param request: The request object
    :type request: WSGIRequest
    :param fatlink_hash: The fat link hash
    :type fatlink_hash: str
    :return: Redirect to fat link details view
    :rtype: HttpResponseRedirect
    """

    try:
        fatlink = FatLink.objects.get(hash=fatlink_hash)
    except FatLink.DoesNotExist:
        messages.warning(
            request,
            mark_safe(_("<h4>Warning!</h4><p>The hash provided is not valid.</p>")),
        )

        return redirect("afat:dashboard")

    if request.method == "POST":
        form = FatLinkEditForm(request.POST)

        if form.is_valid():
            logger.debug(f"Processing FAT link name change form: {form.cleaned_data}")

            fatlink.fleet = form.cleaned_data["fleet"]
            fatlink.save()

            write_log(
                request,
                Log.Event.CHANGE_FATLINK,
                f'FAT link changed. Fleet name was set to "{fatlink.fleet}"',
                fatlink.hash,
            )
            messages.success(
                request,
                mark_safe(
                    _("<h4>Success!</h4><p>Fleet name successfully changed.</p>")
                ),
            )
        else:
            messages.error(
                request, mark_safe(_("<h4>Oh No!</h4><p>Something went wrong!</p>"))
            )

    return redirect("afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def process_manual_fat(request: WSGIRequest, fatlink_hash: str) -> HttpResponseRedirect:
    """
    Process manual fat form

    :param request: The request object
    :type request: WSGIRequest
    :param fatlink_hash: The fat link hash
    :type fatlink_hash: str
    :return: Redirect to fat link details view
    :rtype: HttpResponseRedirect
    """

    try:
        fatlink = FatLink.objects.get(hash=fatlink_hash)
    except FatLink.DoesNotExist:
        messages.warning(
            request,
            mark_safe(_("<h4>Warning!</h4><p>The hash provided is not valid.</p>")),
        )

        return redirect("afat:dashboard")

    if request.method == "POST":
        form = AFatManualFatForm(request.POST)

        if form.is_valid():
            logger.debug(f"Processing manual FAT addition form: {form.cleaned_data}")

            character_name = form.cleaned_data["character"]
            system = form.cleaned_data["system"]
            ship_type = form.cleaned_data["shiptype"]
            character = get_or_create_character(name=character_name)

            if character:
                logger.debug(
                    f"Manual FAT addition for character: {character.character_name}, system: {system}, ship type: {ship_type}"
                )

                # Check SDE for system and ship type before we continue
                try:
                    solar_system = SolarSystem.objects.get(name_en=system)
                except SolarSystem.DoesNotExist:
                    messages.warning(
                        request,
                        mark_safe(
                            format_lazy(
                                _(
                                    "<h4>Warning!</h4><p>The system name you entered cannot be found: {system}</p>"
                                ),
                                system=system,
                            )
                        ),
                    )

                    return redirect(
                        "afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash
                    )

                try:
                    ship = ItemType.objects.filter(published=1).get(name_en=ship_type)
                except ItemType.DoesNotExist:
                    messages.warning(
                        request,
                        mark_safe(
                            format_lazy(
                                _(
                                    "<h4>Warning!</h4><p>The ship type you entered cannot be found: {ship_type}</p>"
                                ),
                                ship_type=ship_type,
                            )
                        ),
                    )

                    return redirect(
                        "afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash
                    )

                fat, created = (  # pylint: disable=unused-variable
                    Fat.objects.get_or_create(
                        fatlink=fatlink,
                        character=character,
                        defaults={
                            "solar_system": solar_system,
                            "ship": ship,
                            "corporation_eve_id": character.corporation_id,
                            "alliance_eve_id": character.alliance_id,
                        },
                    )
                )

                if created:
                    write_log(
                        request,
                        Log.Event.MANUAL_FAT,
                        fatlink.hash,
                        f"Pilot {character.character_name} flying a {ship_type} was manually added",
                    )
                    messages.success(
                        request,
                        mark_safe(
                            format_lazy(
                                _(
                                    "<h4>Success!</h4><p>Manual FAT processed.<br>"
                                    "{character_name} has been added flying a {shiptype} "
                                    "in {system}</p>"
                                ),
                                character_name=character.character_name,
                                shiptype=ship_type,
                                system=system,
                            )
                        ),
                    )
                else:
                    messages.info(
                        request,
                        mark_safe(
                            format_lazy(
                                _(
                                    "<h4>Information</h4>"
                                    "<p>Pilot is already registered for this FAT link.</p>"
                                    "<p>Name: {character_name}<br>System: {system}<br>Ship: {shiptype}</p>"
                                ),
                                character_name=character.character_name,
                                shiptype=ship_type,
                                system=system,
                            )
                        ),
                    )
            else:
                messages.error(
                    request,
                    mark_safe(
                        _(
                            "<h4>Oh No!</h4>"
                            "<p>Manual FAT processing failed! "
                            "The character name you entered was not found.</p>"
                        )
                    ),
                )

    return redirect("afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def process_fleetsnapshot(request, fatlink_hash) -> HttpResponseRedirect:
    """
    Processing fleet snapshot

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    try:
        fatlink = FatLink.objects.get(hash=fatlink_hash)
    except FatLink.DoesNotExist:
        messages.warning(
            request,
            mark_safe(_("<h4>Warning!</h4><p>The hash provided is not valid.</p>")),
        )

        return redirect("afat:dashboard")

    if request.method == "POST":
        form = FleetSnapshot(request.POST)

        if form.is_valid():
            logger.debug(f"Processing fleet snapshot form: {form.cleaned_data}")

            if not re.match(
                RegexPattern.FLEET_COMPOSITION.value,
                form.cleaned_data["fleet_composition"],
            ):
                messages.error(
                    request,
                    mark_safe(
                        _(
                            "<h4>Oh No!</h4><p>Something went wrong!</p>"
                            "<p>Please make sure to paste the fleet composition here.</p>"
                        )
                    ),
                )

                return redirect(
                    "afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash
                )

            fleet_composition = form.cleaned_data["fleet_composition"].splitlines()

            logger.debug(f"Fleet Composition: {fleet_composition}")

            fatlinks_to_create = []

            for line in fleet_composition:
                # Let's split the lines up by tabs, but first let's make sure to remove
                # any trailing tabs, as those would create empty list items in the
                # resulting list and thus throw off the indexing. We also want to make
                # sure to split by multiple tabs, just in case there are multiple tabs
                # between the data points.
                #
                # line[0] => Pilot Name
                # line[1] => System
                # line[2] => Ship Class
                # line[3] => Ship Type
                # line[4] => Position in Fleet
                # line[5] => Skills (FC - WC - SC)
                # line[6] => Wing Name / Squad Name
                line = re.split(r"\t+", line.rstrip("\t"))

                logger.debug(f"Processing line: {line}")

                character = get_or_create_character(name=line[0])

                if character:
                    solar_system = SolarSystem.objects.get(name_en=line[1])
                    # We need the ship class here, actually
                    ship = ItemType.objects.filter(published=1).get(name_en=line[2])

                    # Add to the list…
                    fatlinks_to_create.append(
                        Fat(
                            character=character,
                            fatlink=fatlink,
                            solar_system=solar_system,
                            ship=ship,
                            corporation_eve_id=character.corporation_id,
                            alliance_eve_id=character.alliance_id,
                        )
                    )

            logger.debug(f"FATs to create from fleet snapshot: {fatlinks_to_create}")

            Fat.objects.bulk_create(objs=fatlinks_to_create, ignore_conflicts=True)

            messages.success(
                request,
                mark_safe(
                    format_lazy(
                        ngettext_lazy(
                            "<h4>Success!</h4><p>Fleet snapshot processed: {count} FAT</p>",
                            "<h4>Success!</h4><p>Fleet snapshot processed: {count} FATs</p>",
                            len(fatlinks_to_create),
                        ),
                        count=len(fatlinks_to_create),
                    ),
                ),
            )

    return redirect("afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def details_fatlink(request: WSGIRequest, fatlink_hash: str) -> HttpResponse:
    """
    Fat link details view

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    try:
        link = FatLink.objects.select_related_default().get(hash=fatlink_hash)
    except FatLink.DoesNotExist:
        messages.warning(
            request,
            mark_safe(_("<h4>Warning!</h4><p>The hash provided is not valid.</p>")),
        )

        return redirect("afat:dashboard")

    now = timezone.now()
    link_ongoing = True
    link_can_be_reopened = False
    link_expires = None
    manual_fat_can_be_added = False

    try:
        dur = Duration.objects.get(fleet=link)
        link_expires = link.created + timedelta(minutes=dur.duration)

        if link_expires <= now:
            link_ongoing = False
            if not link.reopened and get_time_delta(
                link_expires, now, "minutes"
            ) < Setting.get_setting(Setting.Field.DEFAULT_FATLINK_REOPEN_GRACE_TIME):
                link_can_be_reopened = True

        if not link.reopened and get_time_delta(link.created, now, "hours") < 24:
            manual_fat_can_be_added = True
    except Duration.DoesNotExist:
        link_ongoing = False

    if link.is_esilink and link.is_registered_on_esi:
        link_ongoing = True

    context = {
        "link": link,
        "is_esi_link": link.is_esilink,
        "is_clickable_link": not link.is_esilink,
        "link_expires": link_expires,
        "link_ongoing": link_ongoing,
        "link_can_be_reopened": link_can_be_reopened,
        "manual_fat_can_be_added": manual_fat_can_be_added,
        "reopen_grace_time": Setting.get_setting(
            Setting.Field.DEFAULT_FATLINK_REOPEN_GRACE_TIME
        ),
        "reopen_duration": Setting.get_setting(
            Setting.Field.DEFAULT_FATLINK_REOPEN_DURATION
        ),
        "forms": {
            "manual_fat": AFatManualFatForm(),
            "fleet_snapshot": FleetSnapshot(),
        },
    }

    return render(request, "afat/view/fatlinks/fatlinks-details-fatlink.html", context)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def ajax_get_fats_by_fatlink(request: WSGIRequest, fatlink_hash) -> JsonResponse:
    """
    Ajax call :: get all FATs for a given FAT link hash

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    fats = Fat.objects.select_related_default().filter(fatlink__hash=fatlink_hash)

    fat_rows = [convert_fats_to_dict(request=request, fat=fat) for fat in fats]

    return JsonResponse(data=fat_rows, safe=False)


@login_required()
@permission_required(perm="afat.manage_afat")
def delete_fatlink(request: WSGIRequest, fatlink_hash: str) -> HttpResponseRedirect:
    """
    Delete fat link helper

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    try:
        link = FatLink.objects.get(hash=fatlink_hash)
    except FatLink.DoesNotExist:
        messages.error(
            request,
            mark_safe(
                _(
                    "<h4>Error!</h4>"
                    "<p>The FAT link hash provided is either invalid "
                    "or the FAT link has already been deleted.</p>"
                )
            ),
        )

        return redirect("afat:dashboard")

    # Delete associated FATs and the FAT link
    Fat.objects.filter(fatlink_id=link.pk).delete()
    link.delete()

    # Log the deletion
    write_log(
        request,
        log_event=Log.Event.DELETE_FATLINK,
        log_text="FAT link deleted.",
        fatlink_hash=fatlink_hash,
    )

    messages.success(
        request,
        mark_safe(
            format_lazy(
                _(
                    "<h4>Success!</h4>"
                    '<p>The FAT link "{fatlink_hash}" and all associated FATs have '
                    "been successfully deleted.</p>"
                ),
                fatlink_hash=fatlink_hash,
            )
        ),
    )

    logger.info(
        f'Fat link "{fatlink_hash}" and all associated FATs have been deleted by {request.user}'
    )

    return redirect("afat:fatlinks_overview")


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.delete_afat"))
def delete_fat(
    request: WSGIRequest, fatlink_hash: str, fat_id: int
) -> HttpResponseRedirect:
    """
    Delete fat helper

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :param fat_id:
    :type fat_id:
    :return:
    :rtype:
    """

    try:
        link = FatLink.objects.get(hash=fatlink_hash)
        fat_details = Fat.objects.get(pk=fat_id, fatlink_id=link.pk)
    except FatLink.DoesNotExist:
        messages.error(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Error!</h4>"
                    "<p>The hash provided is either invalid or has been deleted.</p>"
                )
            ),
        )

        return redirect(to="afat:dashboard")
    except Fat.DoesNotExist:
        messages.error(
            request=request,
            message=mark_safe(
                s=_("<h4>Error!</h4><p>The hash and FAT ID do not match.</p>")
            ),
        )

        return redirect(to="afat:dashboard")

    fat_details.delete()

    write_log(
        request=request,
        log_event=Log.Event.DELETE_FAT,
        log_text=f"The FAT for {fat_details.character.character_name} has been deleted",
        fatlink_hash=link.hash,
    )

    messages.success(
        request=request,
        message=mark_safe(
            s=format_lazy(
                _(
                    "<h4>Success!</h4>"
                    "<p>The FAT for {character_name} has been successfully deleted "
                    'from FAT link "{fatlink_hash}".</p>'
                ),
                character_name=fat_details.character.character_name,
                fatlink_hash=fatlink_hash,
            )
        ),
    )

    logger.info(
        msg=(
            f"The FAT for {fat_details.character.character_name} has "
            f'been deleted from FAT link "{fatlink_hash}" by {request.user}.'
        )
    )

    return redirect(to="afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def close_esi_fatlink(request: WSGIRequest, fatlink_hash: str) -> HttpResponseRedirect:
    """
    Ajax call to close an ESI fat link

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    try:
        fatlink = FatLink.objects.get(hash=fatlink_hash)
        fatlink.is_registered_on_esi = False
        fatlink.save()

        logger.info(
            msg=(
                f'Closing ESI FAT link with hash "{fatlink_hash}". '
                "Reason: Closed by manual request"
            )
        )
    except FatLink.DoesNotExist:
        logger.info(msg=f'ESI FAT link with hash "{fatlink_hash}" does not exist')

    next_view = request.GET.get("next", reverse("afat:dashboard"))

    return HttpResponseRedirect(redirect_to=next_view)


@login_required()
@permissions_required(perm=("afat.manage_afat", "afat.add_fatlink"))
def reopen_fatlink(request: WSGIRequest, fatlink_hash: str) -> HttpResponseRedirect:
    """
    Re-open fat link

    :param request:
    :type request:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    try:
        fatlink_duration = Duration.objects.get(fleet__hash=fatlink_hash)
    except Duration.DoesNotExist:
        messages.error(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Error!</h4>"
                    "<p>The hash you provided does not match with any FAT link.</p>"
                )
            ),
        )

        return redirect(to="afat:dashboard")

    if not fatlink_duration.fleet.reopened:
        created_at = fatlink_duration.fleet.created
        now = timezone.now()

        default_reopen_duration = Setting.get_setting(
            Setting.Field.DEFAULT_FATLINK_REOPEN_DURATION
        )
        time_difference_in_minutes = get_time_delta(
            then=created_at, now=now, interval="minutes"
        )
        new_duration = time_difference_in_minutes + default_reopen_duration

        fatlink_duration.duration = new_duration
        fatlink_duration.save()

        fatlink_duration.fleet.reopened = True
        fatlink_duration.fleet.save()

        # writing DB log
        write_log(
            request=request,
            log_event=Log.Event.REOPEN_FATLINK,
            log_text=f"FAT link re-opened for a duration of {default_reopen_duration} minutes",
            fatlink_hash=fatlink_duration.fleet.hash,
        )

        logger.info(
            msg=(
                f'FAT link with hash "{fatlink_hash}" re-opened by {request.user} '
                f"for a duration of {default_reopen_duration} minutes"
            )
        )

        messages.success(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Success!</h4>"
                    "<p>The FAT link has been successfully re-opened.</p>"
                )
            ),
        )
    else:
        messages.warning(
            request=request,
            message=mark_safe(
                s=_(
                    "<h4>Warning!</h4>"
                    "<p>This FAT link has already been re-opened. "
                    "FAT links can be re-opened only once!</p>"
                )
            ),
        )

    return redirect(to="afat:fatlinks_details_fatlink", fatlink_hash=fatlink_hash)
