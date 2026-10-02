"""Management command to check killmails and update missing solar_system_id."""

# Standard Library
import time
from http import HTTPStatus

# Third Party
import requests

# Django
from django.core.management.base import BaseCommand
from django.db import models

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import USER_AGENT_TEXT, __title__
from killstats.helpers.killmailbody import KillmailBody
from killstats.models.killboard import Killmail
from killstats.providers import AppLogger, esi

logger = AppLogger(get_extension_logger(__name__), __title__)


class Command(BaseCommand):
    help = (
        "Check killmails for missing solar_system_id, re-fetch killmail data "
        "from ESI/zKillboard, and update victim_solar_system_id and victim_region_id."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-m",
            "--missing-only",
            "--only-missing",
            action="store_true",
            dest="missing_only",
            help="Only process killmails that do not have a solar_system_id set (missing or 0).",
        )
        parser.add_argument(
            "-r",
            "--min-reserve",
            type=int,
            default=600,
            help="Minimum ESI token reserve to keep in 'esi:bucket:killmail' (default: 600).",
        )
        parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Perform a dry run without saving updates to the database.",
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            default=None,
            help="Limit the number of killmails to process.",
        )
        parser.add_argument(
            "-s",
            "--sleep",
            type=float,
            default=0.05,
            help="Sleep interval in seconds between HTTP requests (default: 0.05).",
        )

    # pylint: disable=duplicate-code
    def _fetch_solar_system_id(
        self, killmail_id: int, killmail_hash: str
    ) -> int | None:
        """Fetch solar_system_id from ESI, falling back to zKillboard if needed."""
        # 1. Direct HTTP request to ESI (fastest, no auth needed for public killmail endpoint)
        if killmail_hash:
            try:
                url = f"https://esi.evetech.net/v1/killmails/{killmail_id}/{killmail_hash}/"
                headers = {
                    "User-Agent": USER_AGENT_TEXT,
                    "Accept": "application/json",
                }
                resp = requests.get(url=url, headers=headers, timeout=10)
                if resp.status_code == HTTPStatus.OK:
                    data = resp.json()
                    system_id = data.get("solar_system_id")
                    if system_id:
                        return int(system_id)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                logger.debug(
                    "Direct ESI fetch failed for killmail %s: %s", killmail_id, exc
                )

        # 2. Try Alliance Auth ESI client if configured
        try:
            # Alliance Auth (External Libs)
            esi_op = esi.client.Killmails.GetKillmailsKillmailIdKillmailHash(
                killmail_hash=killmail_hash,
                killmail_id=killmail_id,
            )
            result = esi_op.result(use_etag=False)
            if hasattr(result, "solar_system_id") and result.solar_system_id:
                return int(result.solar_system_id)
            if isinstance(result, dict) and result.get("solar_system_id"):
                return int(result["solar_system_id"])
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.debug(
                "ESI client fetch failed for killmail %s: %s", killmail_id, exc
            )

        # 3. Fallback to zKillboard API
        try:
            url = f"https://zkillboard.com/api/killID/{killmail_id}/"
            headers = {
                "User-Agent": USER_AGENT_TEXT,
                "Accept": "application/json",
            }
            resp = requests.get(url=url, headers=headers, timeout=10)
            if resp.status_code == HTTPStatus.OK:
                data = resp.json()
                if data and isinstance(data, list):
                    item = data[0]
                    system_id = (
                        item.get("solar_system_id")
                        or item.get("esi", {}).get("solar_system_id")
                        or item.get("killmail", {}).get("solar_system_id")
                    )
                    if system_id:
                        return int(system_id)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.debug(
                "zKillboard fetch failed for killmail %s: %s", killmail_id, exc
            )

        return None

    # pylint: disable=unused-argument, too-many-locals, too-many-branches, too-many-statements
    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        limit = options.get("limit")
        sleep_interval = options.get("sleep", 0.05)
        min_reserve = options.get("min_reserve", 600)

        self.stdout.write("\nAnalyzing Killstats database for killmails...")

        self.stdout.write(
            "Mode: Checking ONLY killmails with missing solar_system_id (default). "
        )
        query = Killmail.objects.filter(
            models.Q(victim_solar_system_id__isnull=True)
            | models.Q(victim_solar_system_id=0)
        ).order_by("-killmail_id")

        total_matching = query.count()

        if total_matching == 0:
            self.stdout.write(
                "No killmails found with missing solar_system_id. All killmails are up to date!\n"
            )
            return

        if limit:
            query = query[:limit]
            self.stdout.write(
                f"Found {total_matching} killmail(s) matching criteria (limited to {limit})."
            )
        else:
            self.stdout.write(f"Found {total_matching} killmail(s) matching criteria.")

        self.stdout.write(
            f"ESI killmail bucket: {KillmailBody.get_esi_killmail_bucket_remaining()} tokens remaining (reserve: {min_reserve})."
        )

        if dry_run:
            self.stdout.write(
                f"[DRY-RUN] Would check and update {query.count()} killmail(s). No changes made.\n"
            )
            return

        self.stdout.write("Fetching killmail data and updating solar systems...\n")

        updated_count = 0
        failed_count = 0
        skipped_count = 0
        stopped_by_rate_limit = False

        total_to_process = query.count()

        for idx, km in enumerate(query.iterator(), start=1):
            remaining_tokens = KillmailBody.get_esi_killmail_bucket_remaining()
            if remaining_tokens <= min_reserve:
                self.stdout.write(
                    self.style.WARNING(
                        f"\n[RATE-LIMIT] ESI killmail bucket tokens ({remaining_tokens}) at or below reserve ({min_reserve}). "
                        f"Stopping to protect ESI bucket after updating {updated_count} killmail(s)."
                    )
                )
                logger.warning(
                    "ESI rate limit reserve threshold reached (%d tokens remaining, min %d). "
                    "Stopping killstats_update_solar_systems.",
                    remaining_tokens,
                    min_reserve,
                )
                stopped_by_rate_limit = True
                break

            solar_system_id = self._fetch_solar_system_id(km.killmail_id, km.hash)

            if solar_system_id:
                if km.victim_solar_system_id == solar_system_id and km.victim_region_id:
                    skipped_count += 1
                else:
                    region_id = KillmailBody.get_region_id(solar_system_id)
                    km.victim_solar_system_id = solar_system_id
                    km.victim_region_id = region_id
                    km.save(
                        update_fields=[
                            "victim_solar_system_id",
                            "victim_region_id",
                        ]
                    )
                    updated_count += 1
                    logger.debug(
                        "Updated killmail %s: solar_system_id=%s, region_id=%s",
                        km.killmail_id,
                        solar_system_id,
                        region_id,
                    )
            else:
                failed_count += 1
                logger.warning(
                    "Could not retrieve solar_system_id for killmail %s",
                    km.killmail_id,
                )

            if idx % 50 == 0 or idx == total_to_process:
                self.stdout.write(
                    f"Processed {idx}/{total_to_process} killmails "
                    f"({updated_count} updated, {skipped_count} skipped, {failed_count} failed)..."
                )

            if sleep_interval > 0:
                time.sleep(sleep_interval)

        total_processed = updated_count + skipped_count + failed_count
        final_tokens = KillmailBody.get_esi_killmail_bucket_remaining()
        tokens_info = (
            f" (ESI tokens remaining: {final_tokens})"
            if final_tokens is not None
            else ""
        )

        self.stdout.write(
            f"\nFinished processing {total_processed} of {total_to_process} killmail(s){tokens_info}:\n"
            f"  - Updated: {updated_count}\n"
            f"  - Skipped (already correct): {skipped_count}\n"
            f"  - Failed (could not fetch): {failed_count}\n"
            f"  - Stopped by rate limit reserve: {'Yes' if stopped_by_rate_limit else 'No'}\n"
        )
