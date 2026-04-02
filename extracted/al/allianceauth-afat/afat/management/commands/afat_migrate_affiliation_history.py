"""
Migration script to fix hstats affiliation in statistics.
"""

# Django
from django.core.management import BaseCommand

# Alliance Auth AFAT
from afat.models import Fat
from afat.providers import esi


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
    Fix affiliation in statistics
    """

    def _get_character_corp_history(self, character_id: int) -> list:
        """
        Get character corporation history

        :param character_id:
        :type character_id:
        :return:
        :rtype:
        """

        self.stdout.write(
            msg=f"Querying ESI for corporation history for character with ID {character_id} …"
        )

        return esi.client.Character.GetCharactersCharacterIdCorporationhistory(
            character_id=character_id
        ).results()

    def _get_corporation_alliance_history(self, corporation_id: int) -> list:
        """
        Get corporation alliance history

        :param corporation_id:
        :type corporation_id:
        :return:
        :rtype:
        """

        self.stdout.write(
            msg=f"Querying ESI for alliance history for corporation with ID {corporation_id} …"
        )

        return esi.client.Corporation.GetCorporationsCorporationIdAlliancehistory(
            corporation_id=corporation_id
        ).results()

    def _fix_affiliation_in_statistics(self) -> None:
        """
        Fix affiliation in statistics

        :return:
        :rtype:
        """

        all_fats = Fat.objects.all().order_by("character_id")
        fats_total = all_fats.count()

        cache_character_corp_history = {}
        cache_corp_alliance_history = {}
        update_rows = []

        # Fix affiliation in statistics
        for loop_count, fat in enumerate(all_fats):
            self.stdout.write(
                msg=f"Migrating affiliation data for FAT ID {fat.pk} ({loop_count + 1}/{fats_total}) …"
            )

            if fat.character.character_id not in cache_character_corp_history:
                corp_history = self._get_character_corp_history(
                    character_id=fat.character.character_id
                )

                cache_character_corp_history[fat.character.character_id] = corp_history

            # print("cache_character_corp_history", cache_character_corp_history)

            for corp_entry in cache_character_corp_history[fat.character.character_id]:
                if fat.fatlink.created <= corp_entry.start_date:
                    continue

                affiliation_corp_id = corp_entry.corporation_id

                if affiliation_corp_id not in cache_corp_alliance_history:
                    alliance_history = self._get_corporation_alliance_history(
                        corporation_id=affiliation_corp_id
                    )

                    cache_corp_alliance_history[affiliation_corp_id] = alliance_history

                affiliation_alliance_id = next(
                    (
                        entry.alliance_id
                        for entry in cache_corp_alliance_history[affiliation_corp_id]
                        if entry.alliance_id and fat.fatlink.created > entry.start_date
                    ),
                    None,
                )

                update_rows.append(
                    {
                        "fat_id": fat.pk,
                        "corporation_eve_id": affiliation_corp_id,
                        "alliance_eve_id": affiliation_alliance_id,
                    }
                )
                break

        # Update rows
        Fat.objects.bulk_update(
            objs=[
                Fat(
                    pk=row["fat_id"],
                    corporation_eve_id=row["corporation_eve_id"],
                    alliance_eve_id=row["alliance_eve_id"],
                )
                for row in update_rows
            ],
            fields=["corporation_eve_id", "alliance_eve_id"],
            batch_size=500,
        )

        self.stdout.write(msg=self.style.SUCCESS("Migration complete!"))

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        Ask before running …

        :param args:
        :param options:
        :return:
        :rtype:
        """

        self.stdout.write(
            msg=self.style.SUCCESS(
                "This command will add the affiliation of pilots in all FATs so the "
                "statistics are correct. "
                "This might take quite a while depending on the number of pilots "
                "in your database. Please be patient."
            )
        )

        user_input = get_input(text="Are you sure you want to proceed? (yes/no) ")

        if user_input == "yes":
            self.stdout.write(msg="Starting migration. Please stand by.")
            self._fix_affiliation_in_statistics()
        else:
            self.stdout.write(msg=self.style.WARNING("Aborted."))
