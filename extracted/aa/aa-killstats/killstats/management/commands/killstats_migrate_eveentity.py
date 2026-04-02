# Django
from django.core.management.base import BaseCommand

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.models.general import EveEntity
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class Command(BaseCommand):
    help = "Migrate EveEntity data for existing killmails"

    # pylint: disable=unused-argument
    def handle(self, *args, **options):
        try:
            # Third Party
            # pylint: disable=import-outside-toplevel
            from eveuniverse.models import EveEntity as OldEveEntity
        except ImportError:
            logger.error(
                "EveUniverse is not installed. Please install it to run this command. Only required if you migrate from existing Killstats Database."
            )
            return

        self.stdout.write("\nMigrating EveEntity data for existing killmails...")
        batch_size = 1000
        old_entities = OldEveEntity.objects.exclude(
            id__in=EveEntity.objects.values_list("id", flat=True)
        ).only("id", "name", "category")
        total = old_entities.count()
        migrated = 0
        bulk_list = []

        for old_entity in old_entities.iterator(chunk_size=batch_size):
            bulk_list.append(
                EveEntity(
                    id=old_entity.id,
                    name=old_entity.name,
                    category=old_entity.category,
                )
            )

            if len(bulk_list) >= batch_size:
                created = EveEntity.objects.bulk_create(
                    bulk_list, ignore_conflicts=True, batch_size=batch_size
                )
                migrated += len(created)
                bulk_list = []

        if bulk_list:
            created = EveEntity.objects.bulk_create(
                bulk_list, ignore_conflicts=True, batch_size=batch_size
            )
            migrated += len(created)

        self.stdout.write(f"\nMigrated {migrated} EveEntity records out of {total}.")
