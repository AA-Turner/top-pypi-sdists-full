"""Management command to delete killmails from NPC corporations not associated with any audit."""

# Django
from django.core.management.base import BaseCommand
from django.db import models, transaction

# Alliance Auth
from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.models.killboard import Attacker, Killmail
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class Command(BaseCommand):
    help = (
        "Check for killmails from NPC corporations that do not belong to any "
        "CorporationsAudit or AlliancesAudit, and optionally delete them."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="Automatically confirm deletion with 'y' without interactive prompt.",
        )
        parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Perform a dry run without actually deleting any killmails.",
        )
        parser.add_argument(
            "--all-orphans",
            action="store_true",
            help="Also include any orphaned killmails not associated with any audited corporation or alliance.",
        )

    # pylint: disable=unused-argument, too-many-locals, too-many-statements
    def handle(self, *args, **options):
        yes = options.get("yes", False)
        dry_run = options.get("dry_run", False)
        all_orphans = options.get("all_orphans", False)

        self.stdout.write("\nAnalyzing Killstats database for NPC killmails...")

        # 1. Collect valid audited corporations and alliances (player entities >= 10,000,000)
        audited_corps = set(
            CorporationsAudit.objects.filter(
                corporation__corporation_id__gte=10_000_000
            ).values_list("corporation__corporation_id", flat=True)
        )

        audited_alliances = set(
            AlliancesAudit.objects.filter(
                alliance__alliance_id__gte=10_000_000
            ).values_list("alliance__alliance_id", flat=True)
        )

        alliance_member_corps = set(
            EveCorporationInfo.objects.filter(
                alliance__alliance_id__in=audited_alliances,
                corporation_id__gte=10_000_000,
            ).values_list("corporation_id", flat=True)
        )

        all_valid_corp_ids = audited_corps.union(alliance_member_corps)
        all_valid_alliance_ids = audited_alliances

        self.stdout.write(
            f"Found {len(all_valid_corp_ids)} audited corporation(s) and "
            f"{len(all_valid_alliance_ids)} audited alliance(s)."
        )

        # 2. Check for invalid NPC Audits in CorporationsAudit / AlliancesAudit
        npc_corp_audits = CorporationsAudit.objects.filter(
            corporation__corporation_id__lt=10_000_000
        )
        npc_alliance_audits = AlliancesAudit.objects.filter(
            alliance__alliance_id__lt=10_000_000
        )
        npc_audits_count = npc_corp_audits.count() + npc_alliance_audits.count()
        if npc_audits_count > 0:
            self.stdout.write(
                f"Found {npc_corp_audits.count()} NPC corporation audit(s) and "
                f"{npc_alliance_audits.count()} NPC alliance audit(s)."
            )

        # 3. Identify all killmail IDs involving any valid audited entity (PROTECTED)
        corp_victim_km_ids = set(
            Killmail.objects.filter(
                victim_corporation_id__in=all_valid_corp_ids
            ).values_list("killmail_id", flat=True)
        )
        alliance_victim_km_ids = set(
            Killmail.objects.filter(
                victim_alliance_id__in=all_valid_alliance_ids
            ).values_list("killmail_id", flat=True)
        )
        attacker_corp_km_ids = set(
            Attacker.objects.filter(corporation_id__in=all_valid_corp_ids).values_list(
                "killmail_id", flat=True
            )
        )
        attacker_alliance_km_ids = set(
            Attacker.objects.filter(alliance_id__in=all_valid_alliance_ids).values_list(
                "killmail_id", flat=True
            )
        )

        protected_km_ids = (
            corp_victim_km_ids
            | alliance_victim_km_ids
            | attacker_corp_km_ids
            | attacker_alliance_km_ids
        )

        # 4. Identify candidate killmail IDs
        if all_orphans:
            all_km_ids = set(Killmail.objects.values_list("killmail_id", flat=True))
            candidate_km_ids = all_km_ids - protected_km_ids
        else:
            npc_victim_km_ids = set(
                Killmail.objects.filter(
                    models.Q(victim_corporation_id__lt=10_000_000)
                    | models.Q(victim_corporation_id__isnull=True)
                ).values_list("killmail_id", flat=True)
            )
            npc_attacker_km_ids = set(
                Attacker.objects.filter(
                    models.Q(corporation_id__lt=10_000_000)
                    | models.Q(corporation_id__isnull=True)
                ).values_list("killmail_id", flat=True)
            )
            npc_km_ids = npc_victim_km_ids.union(npc_attacker_km_ids)
            candidate_km_ids = npc_km_ids - protected_km_ids

        count_to_delete = len(candidate_km_ids)

        self.stdout.write(
            f"Found {count_to_delete} killmail(s) from NPC corporations "
            f"that are not associated with any audited corporation or alliance."
        )

        if count_to_delete == 0 and npc_audits_count == 0:
            self.stdout.write("No NPC killmails or NPC audits found to delete.\n")
            return

        if dry_run:
            self.stdout.write(
                f"[DRY-RUN] Would delete {count_to_delete} killmail(s) and {npc_audits_count} NPC audit(s).\n"
            )
            return

        # 5. Interactive confirmation if -y was not passed
        if not yes:
            prompt = (
                f"Do you want to delete {count_to_delete} killmail(s)"
                + (
                    f" and {npc_audits_count} NPC audit(s)"
                    if npc_audits_count > 0
                    else ""
                )
                + "? [y/N]: "
            )
            confirm = input(prompt).strip().lower()
            if confirm != "y":
                self.stdout.write("Deletion cancelled.\n")
                return

        # 6. Perform deletion in batches
        self.stdout.write("Deleting killmails...")
        km_ids_list = list(candidate_km_ids)
        batch_size = 1000
        deleted_count = 0

        for i in range(0, len(km_ids_list), batch_size):
            batch = km_ids_list[i : i + batch_size]
            with transaction.atomic():
                Killmail.objects.filter(killmail_id__in=batch).delete()
            deleted_count += len(batch)
            if len(km_ids_list) > batch_size:
                self.stdout.write(
                    f"Deleted {deleted_count}/{len(km_ids_list)} killmails..."
                )

        if npc_audits_count > 0:
            npc_corp_audits.delete()
            npc_alliance_audits.delete()
            self.stdout.write(f"Deleted {npc_audits_count} invalid NPC audit(s).")

        self.stdout.write(f"Successfully deleted {deleted_count} NPC killmail(s).\n")
