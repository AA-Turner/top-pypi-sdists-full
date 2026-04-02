"""
Import FAT data from alliance auth fat module
"""

# Django
from django.apps import apps
from django.core.management.base import BaseCommand

# Alliance Auth
from allianceauth.fleetactivitytracking.models import Fat, Fatlink

# Alliance Auth AFAT
from afat.models import Fat as AFat
from afat.models import FatLink as AFatLink
from afat.models import Log


def get_input(text) -> str:
    """
    Wrapped input to enable import

    :param text:
    :type text:
    :return:
    :rtype:
    """

    return input(text)


def aa_fat_installed() -> bool:
    """
    Check if native fat is installed

    :return:
    :rtype:
    """

    return apps.is_installed(app_name="allianceauth.fleetactivitytracking")


class Command(BaseCommand):
    """
    Initial import of FAT data from AA FAT module
    """

    help = "Imports FAT data from AA FAT module"

    def _import_from_aa_fat(self) -> None:
        """
        Start the import

        :return:
        :rtype:
        """

        # Check if AA FAT is active
        if aa_fat_installed():
            self.stdout.write(
                msg=self.style.SUCCESS("Alliance Auth FAT module is active, let's go!")
            )

            # First, we check if the target tables are empty ...
            current_afat_links_count = AFatLink.objects.all().count()
            current_afat_count = AFat.objects.all().count()

            if current_afat_count > 0 or current_afat_links_count > 0:
                self.stdout.write(
                    msg=self.style.WARNING(
                        "You already have FAT data with the AFAT module. "
                        "Import cannot be continued."
                    )
                )

                return

            aa_fatlinks = Fatlink.objects.all()

            for aa_fatlink in aa_fatlinks:
                self.stdout.write(
                    msg=(
                        f"Importing FAT link for fleet '{aa_fatlink.fleet}' with hash "
                        f"'{aa_fatlink.hash}'."
                    )
                )

                afat_fatlink = AFatLink()

                afat_fatlink.id = aa_fatlink.id
                afat_fatlink.created = aa_fatlink.fatdatetime
                afat_fatlink.fleet = (
                    aa_fatlink.fleet
                    if aa_fatlink.fleet is not None
                    else aa_fatlink.hash
                )
                afat_fatlink.hash = aa_fatlink.hash
                afat_fatlink.creator_id = aa_fatlink.creator_id

                afat_fatlink.save()

                # Write to log table
                log_text = (
                    f"FAT link {aa_fatlink.hash} with name {aa_fatlink.fleet} "
                    f"was created by {aa_fatlink.creator}"
                )

                afatlog = Log()
                afatlog.log_time = aa_fatlink.fatdatetime
                afatlog.log_event = Log.Event.CREATE_FATLINK
                afatlog.log_text = log_text
                afatlog.user_id = aa_fatlink.creator_id
                afatlog.save()

            aa_fats = Fat.objects.all()

            for aa_fat in aa_fats:
                self.stdout.write(msg=f"Importing FATs for FAT link ID '{aa_fat.id}'.")

                afat_fat = AFat()

                afat_fat.id = aa_fat.id
                afat_fat.system = aa_fat.system
                afat_fat.shiptype = aa_fat.shiptype
                afat_fat.character_id = aa_fat.character_id
                afat_fat.fatlink_id = aa_fat.fatlink_id

                afat_fat.save()

            self.stdout.write(
                msg=self.style.SUCCESS(
                    "Import complete! "
                    "You can now deactivate the Alliance Auth FAT "
                    "module in your local.py"
                )
            )
        else:
            self.stdout.write(
                msg=self.style.WARNING(
                    "Alliance Auth FAT module is not active. "
                    "Please make sure you have it in your "
                    "INSTALLED_APPS in your local.py!"
                )
            )

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
            msg=(
                "Importing all FAT/FAT link data from Alliance Auth's built in "
                "FAT module. This can only be done once during the very first "
                "installation. As soon as you have data collected with your AFAT "
                "module, this import will fail!"
            )
        )

        user_input = get_input(text="Are you sure you want to proceed? (yes/no) ")

        if user_input == "yes":
            self.stdout.write(msg="Starting import. Please stand by.")
            self._import_from_aa_fat()
        else:
            self.stdout.write(msg=self.style.WARNING("Aborted."))
