"""
Tasks
"""

# Standard Library
from datetime import timedelta

# Third Party
import kombu
from celery import group, shared_task
from eve_sde.models import ItemType, SolarSystem

# Django
from django.utils import timezone

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce
from esi.exceptions import HTTPClientError
from esi.models import Token

# Alliance Auth AFAT
from afat import __title__
from afat.handler import esi_handler
from afat.models import Fat, FatLink, Log, Setting
from afat.providers import AppLogger, esi
from afat.utils import get_or_create_character

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)

ESI_ERROR_LIMIT = 50
ESI_TIMEOUT_ONCE_ERROR_LIMIT_REACHED = 60
ESI_MAX_RETRIES = 3
ESI_MAX_ERROR_COUNT = 3
ESI_ERROR_GRACE_TIME = 75

TASK_TIME_LIMIT = 120  # Stop after 2 minutes

# Params for all tasks
TASK_DEFAULT_KWARGS = {"time_limit": TASK_TIME_LIMIT, "max_retries": ESI_MAX_RETRIES}


@shared_task(**{**TASK_DEFAULT_KWARGS}, **{"base": QueueOnce})
def process_fats(data_list, data_source: str, fatlink_hash: str) -> None:
    """
    Process FAT link data

    :param data_list:
    :type data_list:
    :param data_source:
    :type data_source:
    :param fatlink_hash:
    :type fatlink_hash:
    :return:
    :rtype:
    """

    if data_source == "esi":
        logger.info(
            msg=(
                f'Valid fleet for FAT link hash "{fatlink_hash}" found '
                "registered via ESI, checking for new pilots"
            )
        )

        my_tasks = [
            process_character.si(
                character_id=char["character_id"],
                solar_system_id=char["solar_system_id"],
                ship_type_id=char["ship_type_id"],
                fatlink_hash=fatlink_hash,
            )
            for char in list(data_list)
        ]

        if my_tasks:
            logger.debug(
                "Creating group of tasks for %s characters and adding them to the queue",
                len(my_tasks),
            )

            try:
                group(my_tasks).delay()
            except kombu.exceptions.EncodeError:
                logger.debug(
                    msg=(
                        "No changes to the current fleet rooster, nothing to add to the queue"
                    )
                )
    else:
        logger.warning(
            msg=(
                f'Unknown data source "{data_source}" for FAT link hash "{fatlink_hash}"'
            )
        )


@shared_task
def process_character(
    character_id: int, solar_system_id: int, ship_type_id: int, fatlink_hash: str
) -> None:
    """
    Process character

    :param character_id:
    :param solar_system_id:
    :param ship_type_id:
    :param fatlink_hash:
    :return:
    """

    try:
        link = FatLink.objects.get(hash=fatlink_hash)
    except FatLink.DoesNotExist:
        logger.warning(
            f'FAT link with hash "{fatlink_hash}" does not exist, skipping character {character_id}'
        )

        return

    character = get_or_create_character(character_id=character_id)
    solar_system = SolarSystem.objects.get(id=solar_system_id)
    ship = ItemType.objects.get(id=ship_type_id)

    logger.debug(
        f"Processing character {character} in {solar_system.name} flying a {ship.name} "
        f"for FAT link with hash {fatlink_hash}"
    )

    fat, created = Fat.objects.get_or_create(
        fatlink=link,
        character=character,
        corporation_eve_id=character.corporation_id,
        alliance_eve_id=character.alliance_id,
        defaults={"system": solar_system.name, "shiptype": ship.name},
    )

    if created:
        logger.info(
            f"New Pilot: Adding {character} in {solar_system.name} flying "
            f'a {ship.name} to FAT link "{fatlink_hash}" (FAT ID {fat.pk})'
        )
    else:
        logger.debug(
            f"Pilot {character} already registered for FAT link {fatlink_hash} "
            f"with FAT ID {fat.pk}"
        )


def _close_esi_fleet(fatlink: FatLink, reason: str) -> None:
    """
    Closing ESI fleet

    :param fatlink:
    :type fatlink:
    :param reason:
    :type reason:
    :return:
    :rtype:
    """

    logger.info(
        msg=f'Closing ESI FAT link with hash "{fatlink.hash}". Reason: {reason}'
    )

    fatlink.is_registered_on_esi = False
    fatlink.save()


def _esi_fatlinks_error_handling(error_key: str, fatlink: FatLink) -> None:
    """
    ESI error handling

    :param error_key:
    :type error_key:
    :param fatlink:
    :type fatlink:
    :return:
    :rtype:
    """

    time_now = timezone.now()
    grace_period = time_now - timedelta(seconds=ESI_ERROR_GRACE_TIME)

    if (
        fatlink.last_esi_error == error_key
        and fatlink.last_esi_error_time >= grace_period
        and fatlink.esi_error_count >= ESI_MAX_ERROR_COUNT
    ):
        _close_esi_fleet(fatlink=fatlink, reason=error_key.label)

        return

    fatlink.esi_error_count = (
        fatlink.esi_error_count + 1
        if fatlink.last_esi_error == error_key
        and fatlink.last_esi_error_time >= grace_period
        else 1
    )
    fatlink.last_esi_error = error_key
    fatlink.last_esi_error_time = time_now
    fatlink.save()

    logger.info(
        msg=(
            f'FAT link "{fatlink.hash}" Error: "{error_key.label}" '
            f"({fatlink.esi_error_count} of {ESI_MAX_ERROR_COUNT})."
        )
    )


def _check_for_esi_fleet(fatlink: FatLink) -> dict | None:
    """
    Check if there is a fleet for this FAT link registered on ESI

    :param fatlink:
    :type fatlink:
    :return:
    :rtype:
    """

    required_scopes = ["esi-fleets.read_fleet.v1"]

    fleet_commander_id = fatlink.character.character_id
    esi_token = Token.get_token(character_id=fleet_commander_id, scopes=required_scopes)

    operation = esi.client.Fleets.GetCharactersCharacterIdFleet(
        character_id=fleet_commander_id, token=esi_token
    )

    try:
        fleet_from_esi = esi_handler.result(operation=operation, use_etag=False)

        logger.debug("Fleet from ESI: %s", fleet_from_esi)
        logger.debug("FAT Link ESI fleet ID: %s", fatlink.esi_fleet_id)

        if not fleet_from_esi or fatlink.esi_fleet_id != fleet_from_esi.fleet_id:
            logger.debug(
                f'Fleet ID mismatch for fleet "{fatlink.fleet}" of {fatlink.character} '
                f"(ESI ID: {fatlink.esi_fleet_id}): ESI fleet ID is {fleet_from_esi.fleet_id}."
            )

            _esi_fatlinks_error_handling(
                error_key=FatLink.EsiError.FC_WRONG_FLEET, fatlink=fatlink
            )

            return None

        return {"fleet": fleet_from_esi, "token": esi_token}
    except HTTPClientError as ex:
        logger.debug(
            f'HTTPClientError while checking fleet "{fatlink.fleet}" of {fatlink.character} '
            f"(ESI ID: {fatlink.esi_fleet_id}): {ex}"
        )

        # Handle the case where the fleet is not found
        if ex.status_code == 404:
            _esi_fatlinks_error_handling(
                error_key=FatLink.EsiError.NOT_IN_FLEET, fatlink=fatlink
            )
        else:  # 400, 401, 402, 403 ?
            _esi_fatlinks_error_handling(
                error_key=FatLink.EsiError.NO_FLEET, fatlink=fatlink
            )
    except Exception as ex:  # pylint: disable=broad-exception-caught
        logger.debug(
            f'Unexpected error while checking fleet "{fatlink.fleet}" of {fatlink.character} '
            f"(ESI ID: {fatlink.esi_fleet_id}): {ex}"
        )

        # Handle any other errors that occur
        _esi_fatlinks_error_handling(
            error_key=FatLink.EsiError.NO_FLEET, fatlink=fatlink
        )

    return None


@shared_task()
def _process_esi_fatlink(fatlink: FatLink) -> None:
    """
    Processing ESI FAT link

    :param fatlink:
    :type fatlink:
    :return:
    :rtype:
    """

    logger.info(msg=f'Processing ESI FAT link with hash "{fatlink.hash}"')

    if not fatlink.creator.profile.main_character:
        _close_esi_fleet(fatlink=fatlink, reason="No FAT link creator available.")

        return

    # Check if there is a fleet
    esi_fleet = _check_for_esi_fleet(fatlink=fatlink)

    if not esi_fleet:
        return

    # Check if we deal with the fleet boss here
    operation = esi.client.Fleets.GetFleetsFleetIdMembers(
        fleet_id=esi_fleet["fleet"].fleet_id,
        token=esi_fleet["token"],
    )

    try:
        esi_fleet_member = esi_handler.result(operation=operation, use_etag=False)
    except Exception:  # pylint: disable=broad-exception-caught
        _esi_fatlinks_error_handling(
            error_key=FatLink.EsiError.NOT_FLEETBOSS, fatlink=fatlink
        )

        return

    # Process fleet members
    logger.debug(
        msg=f'Processing fleet members for ESI FAT link with hash "{fatlink.hash}"'
    )

    process_fats.delay(
        data_list=[fleet_member.dict() for fleet_member in esi_fleet_member],
        data_source="esi",
        fatlink_hash=fatlink.hash,
    )


@shared_task(**{**TASK_DEFAULT_KWARGS, "base": QueueOnce})
def update_esi_fatlinks() -> None:
    """
    Checking ESI fat links for changes
    """

    esi_fatlinks = (
        FatLink.objects.select_related_default()
        .filter(is_esilink=True, is_registered_on_esi=True)
        .distinct()
    )

    if esi_fatlinks.exists():
        logger.debug(msg=f"Found {len(esi_fatlinks)} ESI FAT links to process")
        logger.debug("ESI FAT Links: %s", esi_fatlinks)

        for fatlink in esi_fatlinks:
            _process_esi_fatlink(fatlink=fatlink)
    else:
        logger.debug(msg="No ESI FAT links to process")


@shared_task
def logrotate():
    """
    Remove logs older than AFAT_DEFAULT_LOG_DURATION

    :return:
    :rtype:
    """

    logger.info(
        msg=f"Cleaning up logs older than {Setting.get_setting(Setting.Field.DEFAULT_LOG_DURATION)} days"
    )

    Log.objects.filter(
        log_time__lte=timezone.now()
        - timedelta(days=Setting.get_setting(Setting.Field.DEFAULT_LOG_DURATION))
    ).delete()
