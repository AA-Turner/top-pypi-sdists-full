"""
Migration script to migrate fleet types from the old format to the new format.
"""

# Django
from django.core.management import BaseCommand

# Alliance Auth AFAT
from afat.models import FatLink


def get_input(text) -> str:
    """
    Wrapped input to enable import

    :param text:
    :type text:
    :return:
    :rtype:
    """

    return input(text)


class Command(BaseCommand):
    """
    Initial import of FAT data from AA FAT module
    """

    help = (
        "Migrating fleet types."
        "This command will migrate the fleet types from the old format to the new format."
    )

    def _migrate_fleet_types(self) -> None:
        """
        Start the import

        :return:
        :rtype:
        """

        # Migrate fleet types to the new format
        fatlinks = FatLink.objects.all()

        for fatlink in fatlinks:
            fatlink.fleet_type = (
                str(fatlink.link_type)
                if fatlink.link_type and fatlink.fleet_type == ""
                else fatlink.fleet_type
            )
            fatlink.save()

        self.stdout.write(msg=self.style.SUCCESS("Migration complete!"))

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        Ask before running …

        :param args:
        :type args:
        :param options:
        :type options:
        :return:
        :rtype:
        """

        self.stdout.write(
            msg=self.style.SUCCESS(
                "This command will migrate the fleet types from the old format to the new format."
            )
        )

        user_input = get_input(text="Are you sure you want to proceed? (yes/no) ")

        if user_input == "yes":
            self.stdout.write(msg="Starting import. Please stand by.")
            self._migrate_fleet_types()
        else:
            self.stdout.write(msg=self.style.WARNING("Aborted."))
