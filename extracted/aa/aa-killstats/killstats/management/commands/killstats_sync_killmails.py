"""Management command to sync and backfill missing killmails from zKillboard."""

# Standard Library
import time

# Django
from django.core.management.base import BaseCommand
from django.db import IntegrityError

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.app_settings import KILLSTATS_ESI_BUCKET
from killstats.helpers.killmailbody import KillmailBody
from killstats.models.killboard import Killmail
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class Command(BaseCommand):
    help = (
        "Check and import missing killmails from zKillboard for audited corporations "
        "and/or alliances, allowing backfill of older pages."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--corporation",
            type=int,
            dest="corporation_id",
            help="Corporation ID to sync missing killmails for.",
        )
        parser.add_argument(
            "-a",
            "--alliance",
            type=int,
            dest="alliance_id",
            help="Alliance ID to sync missing killmails for.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all_entities",
            help="Sync missing killmails for all audited corporations and alliances.",
        )
        parser.add_argument(
            "-p",
            "--pages",
            type=int,
            default=10,
            help="Number of pages to fetch from zKillboard (default: 10; 200 killmails per page).",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=1.0,
            help="Delay in seconds between page requests to adhere to zKillboard rate limits (default: 1.0).",
        )

    # pylint: disable=too-many-locals, too-many-branches, unused-argument
    def handle(self, *args, **options):
        corporation_id = options.get("corporation_id")
        alliance_id = options.get("alliance_id")
        all_entities = options.get("all_entities", False)
        pages = options.get("pages", 10)
        delay = options.get("delay", 1.0)

        if not corporation_id and not alliance_id and not all_entities:
            self.stderr.write(
                "Please specify --corporation <id>, --alliance <id>, or --all to sync missing killmails."
            )
            return

        entities_to_sync: list[tuple[str, int, str]] = []

        if corporation_id:
            entities_to_sync.append(
                ("corporation", corporation_id, f"Corporation {corporation_id}")
            )

        if alliance_id:
            entities_to_sync.append(
                ("alliance", alliance_id, f"Alliance {alliance_id}")
            )

        if all_entities:
            for corp in CorporationsAudit.objects.select_related("corporation"):
                entities_to_sync.append(
                    (
                        "corporation",
                        corp.corporation.corporation_id,
                        f"Corporation {corp.corporation.corporation_name} ({corp.corporation.corporation_id})",
                    )
                )
            for ally in AlliancesAudit.objects.select_related("alliance"):
                entities_to_sync.append(
                    (
                        "alliance",
                        ally.alliance.alliance_id,
                        f"Alliance {ally.alliance.alliance_name} ({ally.alliance.alliance_id})",
                    )
                )

        self.stdout.write(
            f"Starting zKillboard sync for {len(entities_to_sync)} entity/entities (pages={pages}, delay={delay}s)..."
        )

        total_imported = 0

        for entity_type, entity_id, label in entities_to_sync:
            self.stdout.write(f"\nChecking missing killmails for {label}...")
            try:
                if entity_type == "corporation":
                    missing = Killmail.objects.check_missing_killmails(
                        corporation_id=entity_id,
                        pages=pages,
                        delay_between_pages=delay,
                    )
                else:
                    missing = Killmail.objects.check_missing_killmails(
                        alliance_id=entity_id,
                        pages=pages,
                        delay_between_pages=delay,
                    )

                self.stdout.write(
                    f"  Found {len(missing)} missing killmail(s) from zKB."
                )
                entity_imported = 0
                for km in missing:
                    esi_limit = KillmailBody.get_esi_killmail_bucket_remaining()
                    if esi_limit <= KILLSTATS_ESI_BUCKET:
                        self.stdout.write(
                            f"  ESI bucket limit reached ({esi_limit} <= {KILLSTATS_ESI_BUCKET}), slowing down..."
                        )
                        self.stdout.write(
                            "  Waiting 5 minutes for ESI bucket to replenish..."
                        )
                        time.sleep(300)  # Wait for 5 minutes before retrying
                    try:
                        Killmail.objects.create_from_killmail(km)
                        entity_imported += 1
                    except IntegrityError:
                        logger.debug(
                            "Killmail %s already exists, skipping", km.esi.killmail_id
                        )

                self.stdout.write(
                    f"  Successfully imported {entity_imported}/{len(missing)} killmail(s) for {label}."
                )
                total_imported += entity_imported

            except Exception as exc:  # pylint: disable=broad-exception-caught
                self.stderr.write(f"  Error syncing {label}: {exc}")
                logger.error(
                    "Error in killstats_sync_killmails for %s: %s",
                    label,
                    exc,
                    exc_info=True,
                )

        self.stdout.write(
            f"\nSync complete. Total killmails imported across all entities: {total_imported}."
        )
