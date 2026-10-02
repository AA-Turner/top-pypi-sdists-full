# Third Party
from celery import chain as Chain
from celery import shared_task

# Django
from django.db import IntegrityError, models
from django.utils import timezone

# Alliance Auth
from allianceauth.services.tasks import QueueOnce

# AA Killstats
from killstats import __title__, app_settings
from killstats.helpers.killmailbody import KillmailBody
from killstats.models.killboard import Killmail
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import esi, logger

MAX_RETRIES_DEFAULT = 3

# Default params for all tasks.
TASK_DEFAULTS = {
    "time_limit": app_settings.KILLSTATS_TASKS_TIME_LIMIT,
    "timeout": app_settings.KILLSTATS_TASKS_TIMEOUT,
    "max_retries": MAX_RETRIES_DEFAULT,
}

# Default params for tasks that need run once only.
TASK_DEFAULTS_ONCE = {**TASK_DEFAULTS, **{"base": QueueOnce}}
TASK_DEFAULTS_ONCE_GRACE = {
    **TASK_DEFAULTS,
    "base": QueueOnce,
    "once": {"graceful": True},
}


@shared_task(**TASK_DEFAULTS_ONCE)
def run_tracker_zkb():
    total_killmails = 0
    sequence_id = None

    try:
        sequence_id = KillmailBody.get_sequence()
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error fetching killmail from zKB: %s", e)
        return

    if not sequence_id:
        logger.debug("No killmail received from zKB.")
        return

    while True:
        # Process the killmail for the current sequence ID
        killmail = KillmailBody.create_from_sequence(sequence_id)
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
                killmail_id=killmail.killmail_id,
            )

        # Iterate over all alliances and run the tracker for each of them
        for alliance in allys_qs:
            run_tracker_alliance.delay(
                alliance_id=alliance.alliance.alliance_id,
                killmail_id=killmail.killmail_id,
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
    valid_killmail = corporation.is_corporation(killmail)
    if valid_killmail:
        Chain(
            store_killmail.si(killmail.killmail_id),
        ).delay()
        logger.debug(
            "%s: Start storing killmail for %s",
            killmail.killmail_id,
            corporation.corporation.corporation_name,
        )


@shared_task(**TASK_DEFAULTS)
def run_tracker_alliance(alliance_id: int, killmail_id: int) -> None:
    """Run the tracker for the given killmail"""
    alliance = AlliancesAudit.objects.get(alliance__alliance_id=alliance_id)
    killmail = KillmailBody.get(killmail_id)
    valid_killmail = alliance.is_alliance(killmail)
    if valid_killmail:
        Chain(
            store_killmail.si(killmail.killmail_id),
        ).delay()
        logger.debug(
            "%s: Start storing killmail for %s",
            killmail.killmail_id,
            alliance.alliance.alliance_name,
        )


@shared_task(**TASK_DEFAULTS)
def run_tracker_missing_data(pages: int = 3, batch_size: int = 200) -> None:
    """
    Run the tracker for missing data, including corporations, alliances, and solar systems.

    Args:
        pages (int): Number of pages to check for missing killmails.
        batch_size (int): Number of entities to process in each batch.
    """
    # 1. Process Corporation(s)
    corps_to_check = CorporationsAudit.objects.select_related("corporation").order_by(
        models.F("last_missing_check").asc(nulls_first=True)
    )[:1]

    for corp_audit in corps_to_check:
        corp_id = corp_audit.corporation.corporation_id
        corp_audit.last_missing_check = timezone.now()
        corp_audit.save(update_fields=["last_missing_check"])

        check_and_import_corporation_killmails_task.delay(
            corporation_id=corp_id, pages=pages
        )

    # 2. Process Alliance(s)
    alliances_to_check = AlliancesAudit.objects.select_related("alliance").order_by(
        models.F("last_missing_check").asc(nulls_first=True)
    )[:1]

    for alliance_audit in alliances_to_check:
        alliance_id = alliance_audit.alliance.alliance_id
        alliance_audit.last_missing_check = timezone.now()
        alliance_audit.save(update_fields=["last_missing_check"])

        check_and_import_alliance_killmails_task.delay(
            alliance_id=alliance_id, pages=pages
        )

    # 3. Update missing solar systems (batch of 100, min 600 token reserve)
    update_missing_solar_systems_task.delay(
        batch_size=batch_size, min_reserve_tokens=600
    )


@shared_task(**TASK_DEFAULTS_ONCE_GRACE)
def store_killmail(killmail_id: int) -> None:
    """stores killmail as EveKillmail object"""
    killmail_body = KillmailBody.get(killmail_id)
    try:
        Killmail.objects.create_from_killmail(killmail_body)
    except IntegrityError:
        logger.debug(
            "%s: Failed to store killmail, because it already exists",
            killmail_body.killmail_id,
        )
    else:
        logger.debug("%s: Stored killmail", killmail_body.killmail_id)


@shared_task(**TASK_DEFAULTS_ONCE)
def check_and_import_corporation_killmails_task(
    corporation_id: int, pages: int = 3
) -> None:
    """
    Checks missing killmails for a corporation from zKillboard and directly imports them from the response data.
    """
    missing_killmails = Killmail.objects.check_missing_killmails(
        corporation_id=corporation_id, pages=pages
    )

    imported_km = 0
    for killmail in missing_killmails:
        try:
            Killmail.objects.create_from_killmail(killmail)
            imported_km += 1
        except IntegrityError:
            logger.debug(
                "%s: Killmail already exists, skipping",
                killmail.esi.killmail_id,
            )

    logger.info(
        "Imported %d missing killmails for corporation %s",
        imported_km,
        corporation_id,
    )


@shared_task(**TASK_DEFAULTS_ONCE)
def check_and_import_alliance_killmails_task(alliance_id: int, pages: int = 3) -> None:
    """
    Checks missing killmails for an alliance from zKillboard and directly imports them from the response data.
    """
    missing_killmails = Killmail.objects.check_missing_killmails(
        alliance_id=alliance_id, pages=pages
    )

    imported_km = 0
    for killmail in missing_killmails:
        try:
            Killmail.objects.create_from_killmail(killmail)
            imported_km += 1
        except IntegrityError:
            logger.debug(
                "%s: Killmail already exists, skipping",
                killmail.esi.killmail_id,
            )

    logger.info(
        "Imported %d missing killmails for alliance %s",
        imported_km,
        alliance_id,
    )


@shared_task(**TASK_DEFAULTS_ONCE)
def update_missing_solar_systems_task(
    batch_size: int = 100, min_reserve_tokens: int = 600
) -> dict:
    killmails = Killmail.objects.filter(
        models.Q(victim_solar_system_id__isnull=True)
        | models.Q(victim_solar_system_id=0)
    ).order_by("-killmail_id")[:batch_size]

    total_missing = killmails.count()
    if total_missing == 0:
        logger.info("No killmails with missing solar_system_id found.")

    logger.info(
        "Processing batch of %d killmails (out of %d missing) to update solar systems.",
        len(killmails),
        total_missing,
    )

    runs = 0
    for km in killmails:
        remaining = KillmailBody.get_esi_killmail_bucket_remaining()
        if remaining <= min_reserve_tokens:
            logger.warning(
                "ESI killmail bucket tokens (%d) at or below reserve (%d). "
                "Stopping task early after updating %d killmails.",
                remaining,
                min_reserve_tokens,
                runs,
            )
            break
        fetch_solar_system_id_for_killmail.apply_async(
            args=(km.killmail_id, km.hash),
            kwargs={"min_reserve_tokens": min_reserve_tokens},
        )
        runs += 1


@shared_task(**TASK_DEFAULTS_ONCE_GRACE)
def fetch_solar_system_id_for_killmail(
    killmail_id: int, killmail_hash: str, min_reserve_tokens: int = 600
) -> int | None:
    """
    Fetch solar_system_id for a killmail from ESI, preserving token reserve in bucket.
    Falls back to zKillboard API.
    """
    # 1. Check rate limit reserve in django-esi killmail bucket
    remaining = KillmailBody.get_esi_killmail_bucket_remaining()

    # If the remaining tokens are below the minimum reserve, skip the ESI request to preserve the bucket.
    if remaining <= min_reserve_tokens:
        return None

    # 2. Attempt to fetch from ESI using the Alliance Auth ESI client
    try:
        killmail = esi.client.Killmails.GetKillmailsKillmailIdKillmailHash(
            killmail_hash=killmail_hash,
            killmail_id=killmail_id,
        ).result(use_etag=False)

        region_id = KillmailBody.get_region_id(killmail.solar_system_id)
        Killmail.objects.filter(killmail_id=killmail_id, hash=killmail_hash).update(
            victim_solar_system_id=killmail.solar_system_id,
            victim_region_id=region_id,
        )
        return int(killmail.solar_system_id)
    except Exception as exc:  # pylint: disable=broad-except
        logger.debug("ESI client fetch failed for killmail %s: %s", killmail_id, exc)
        return None
