# Alliance Auth
from allianceauth.authentication.models import UserProfile
from allianceauth.eveonline.models import EveCharacter


class AccountManager:
    def __init__(self):
        self.init_accounts()

    def init_accounts(self):
        self.accounts = UserProfile.objects.filter(
            main_character__isnull=False,
        ).select_related(
            "user__profile__main_character",
            "main_character__character_ownership",
            "main_character__character_ownership__user__profile",
            "main_character__character_ownership__user__profile__main_character",
        )

    def get_mains_alts(
        self,
    ) -> tuple[dict[int, dict[str, list[EveCharacter]]], list[int]]:
        """Get all members for given corporations/alliances"""
        characters = {}
        chars_list = set()

        for account in self.accounts:
            main = account.main_character
            alts_ids = account.user.character_ownerships.values_list(
                "character__character_id", flat=True
            )
            alts = EveCharacter.objects.filter(
                character_id__in=alts_ids,
            )

            if main and main.character_id not in characters:
                characters[main.character_id] = {"main": main, "alts": []}
                characters[main.character_id]["alts"].extend(alts)
                chars_list.add(main.character_id)
                chars_list.update(alts_ids)

        return characters, list(chars_list)
