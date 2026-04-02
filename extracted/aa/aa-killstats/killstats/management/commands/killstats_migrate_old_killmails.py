# Django
from django.core.management.base import BaseCommand

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.helpers.killmail import KillmailBody
from killstats.models.general import EveEntity
from killstats.models.killboard import Killmail
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class Command(BaseCommand):
    help = "Migrate old killmails to new Killstats attacker model"

    # pylint: disable=unused-argument
    def handle(self, *args, **options):
        self.stdout.write("\nMigrating Killmails this can take a while...")
        killmails = Killmail.objects.all()
        kms_count = killmails.count()
        runs = 0
        characters = 0
        corporations = 0
        alliances = 0
        for killmail in killmails:
            try:
                if killmail.victim_id:
                    _, created = EveEntity.objects.get_or_create_esi(
                        eve_id=killmail.victim_id
                    )
                    if created:
                        characters = characters + 1
                if killmail.victim_corporation_id:
                    _, created = EveEntity.objects.get_or_create_esi(
                        eve_id=killmail.victim_corporation_id
                    )
                    if created:
                        corporations = corporations + 1
                if killmail.victim_alliance_id:
                    _, created = EveEntity.objects.get_or_create_esi(
                        eve_id=killmail.victim_alliance_id
                    )
                    if created:
                        alliances = alliances + 1

                killmail_data = {
                    "killmail_id": killmail.killmail_id,
                    "zkb": {"hash": killmail.hash},
                }
                killmail_obj = KillmailBody._process_killmail_data(killmail_data)
                km = KillmailBody._create_from_dict(killmail_obj)
                km.get_or_create_attackers(killmail, km)
                runs = runs + 1
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Error processing killmail {killmail.killmail_id}: {e}")
                self.stdout.write(
                    f"Error processing killmail {killmail.killmail_id} deleting killmail..."
                )
                killmail.delete()
                continue
        self.stdout.write(f"{characters} characters created")
        self.stdout.write(f"{corporations} corporations created")
        self.stdout.write(f"{alliances} alliances created")
        self.stdout.write(f"{runs} from {kms_count} Killmails migrated")
