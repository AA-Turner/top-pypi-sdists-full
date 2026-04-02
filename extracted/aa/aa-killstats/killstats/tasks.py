"""App Tasks"""

# Third Party
from celery import chain as Chain
from celery import shared_task

# Django
from django.db import IntegrityError

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# AA Killstats
from killstats import __title__, app_settings
from killstats.helpers.killmail import KillmailBody
from killstats.models.killboard import Killmail
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)

MAX_RETRIES_DEFAULT = 3

# Default params for all tasks.
TASK_DEFAULTS = {
    "time_limit": app_settings.KILLSTATS_TASKS_TIME_LIMIT,
    "timeout": app_settings.KILLSTATS_TASKS_TIMEOUT,
    "max_retries": MAX_RETRIES_DEFAULT,
}

# Default params for tasks that need run once only.
TASK_DEFAULTS_ONCE = {**TASK_DEFAULTS, **{"base": QueueOnce}}


@shared_task(**TASK_DEFAULTS_ONCE)
def run_zkb_r2z2():
    total_killmails = 0
    sequence_id = None

    try:
        sequence_id = KillmailBody.get_sequence_from_r2z2()
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error fetching killmail from zKB R2Z2: %s", e)
        return

    if not sequence_id:
        logger.debug("No killmail received from zKB R2Z2.")
        return

    while True:
        # Process the killmail for the current sequence ID
        killmail = KillmailBody.create_from_r2z2_sequence(sequence_id)
        if not killmail:
            logger.debug(
                "No valid killmail data received for sequence ID %s", sequence_id
            )
            break

        # Save temporary to Cache
        killmail.save()

        # Get all corporations and alliances that are tracked and run the tracker for each of them
        corps_qs = CorporationsAudit.objects.all()
        allys_qs = AlliancesAudit.objects.all()

        # Iterate over all corporations and alliances and run the tracker for each of them
        for corporation in corps_qs:
            run_tracker_corporation.delay(
                corporation_id=corporation.corporation.corporation_id,
                killmail_id=killmail.id,
            )

        # Iterate over all alliances and run the tracker for each of them
        for alliance in allys_qs:
            run_tracker_alliance.delay(
                alliance_id=alliance.alliance.alliance_id, killmail_id=killmail.id
            )

        # Increment the total killmail count and move to the next sequence ID
        total_killmails += 1
        sequence_id += 1
    logger.info(
        "Killboard runs completed. %s killmails received from zKB",
        total_killmails,
    )


@shared_task(**TASK_DEFAULTS)
def run_tracker_corporation(corporation_id: int, killmail_id: int) -> None:
    """Run the tracker for the given killmail"""
    corporation = CorporationsAudit.objects.get(
        corporation__corporation_id=corporation_id
    )
    killmail = KillmailBody.get(killmail_id)
    killmail_new = corporation.process_killmail(killmail)
    if killmail_new:
        Chain(
            store_killmail.si(killmail.id),
        ).delay()
        logger.debug(
            "%s: Start storing killmail for %s",
            killmail.id,
            corporation.corporation.corporation_name,
        )


@shared_task(**TASK_DEFAULTS)
def run_tracker_alliance(alliance_id: int, killmail_id: int) -> None:
    """Run the tracker for the given killmail"""
    alliance = AlliancesAudit.objects.get(alliance__alliance_id=alliance_id)
    killmail = KillmailBody.get(killmail_id)
    killmail_new = alliance.process_killmail(killmail)
    if killmail_new:
        Chain(
            store_killmail.si(killmail.id),
        ).delay()
        logger.debug(
            "%s: Start storing killmail for %s",
            killmail.id,
            alliance.alliance.alliance_name,
        )


@shared_task(**TASK_DEFAULTS)
def store_killmail(killmail_id: int) -> None:
    """stores killmail as EveKillmail object"""
    killmail = KillmailBody.get(killmail_id)
    try:
        Killmail.objects.create_from_killmail(killmail)
    except IntegrityError:
        logger.warning(
            "%s: Failed to store killmail, because it already exists", killmail.id
        )
    else:
        logger.debug("%s: Stored killmail", killmail.id)
