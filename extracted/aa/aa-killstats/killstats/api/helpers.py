"""Helper functions for killboard API endpoints."""

# Standard Library
from dataclasses import dataclass, field

# Django
from django.db.models import QuerySet

# Alliance Auth
from allianceauth.authentication.models import UserProfile
from allianceauth.eveonline.models import EveCharacter


@dataclass
class Account:
    user: UserProfile
    main_character: EveCharacter
    alts: list[EveCharacter] = field(default_factory=list)
    alt_ids: list[int] = field(default_factory=list)


class AccountManager:
    """Resolves Alliance Auth user accounts for a given EVE entity (corp or alliance).

    Can be used with or without an entity filter:

    * Without parameters → returns all registered users (legacy behaviour used
      by tests and generic helpers).
    * With ``entity_id`` / ``entity_type`` → filters to members of that entity.

    Usage::

        # All users
        manager = AccountManager()

        # Filtered to a corporation
        manager = AccountManager(entity_id=98000001, entity_type="corporation")

        accounts = manager.get_accounts_data()
    """

    def __init__(self, entity_id: int = 0, entity_type: str = ""):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.accounts = self._load_accounts()

    @property
    def get_char_ids(self) -> list[int]:
        """Return a flat list of all alt character IDs."""
        char_ids: list[int] = []
        for account in self.get_accounts_data().values():
            char_ids.extend(account.alt_ids)
        return char_ids

    def _load_accounts(self) -> QuerySet:
        """Fetch the matching UserProfile queryset for the entity.

        If no entity is configured, all UserProfiles are returned (legacy mode).
        """
        if self.entity_type == "corporation" and self.entity_id:
            return UserProfile.objects.filter(
                main_character__corporation_id=self.entity_id
            ).select_related("main_character", "user")
        if self.entity_type == "alliance" and self.entity_id:
            return UserProfile.objects.filter(
                main_character__alliance_id=self.entity_id
            ).select_related("main_character", "user")
        # No entity filter – return all (legacy / generic usage)
        return UserProfile.objects.all().select_related("main_character", "user")

    def init_accounts(self):
        """Re-initialise accounts after entity_id / entity_type were changed."""
        self.accounts = self._load_accounts()

    def get_accounts_data(self) -> dict[int, Account]:
        """Return ``{main_character_id → Account}`` for all matching members."""
        accounts: dict[int, Account] = {}

        for profile in self.accounts:
            main = profile.main_character
            alts_ids = list(
                profile.user.character_ownerships.values_list(
                    "character__character_id", flat=True
                )
            )

            if self.entity_type == "corporation" and self.entity_id:
                alts = list(
                    EveCharacter.objects.filter(
                        character_id__in=alts_ids,
                        corporation_id=self.entity_id,
                    )
                )
            elif self.entity_type == "alliance" and self.entity_id:
                alts = list(
                    EveCharacter.objects.filter(
                        character_id__in=alts_ids,
                        alliance_id=self.entity_id,
                    )
                )
            else:
                alts = list(EveCharacter.objects.filter(character_id__in=alts_ids))

            if main and main.character_id not in accounts:
                accounts[main.character_id] = Account(
                    user=profile.user,
                    main_character=main,
                    alts=alts,
                    alt_ids=alts_ids,
                )

        return accounts


def _build_main_name_map(entity_type: str, entity_id: int) -> dict[int, str]:
    """Build a {eve_character_id → main_name} mapping for the entity's members.

    Uses AccountManager which handles corp / alliance member resolution.
    Returns an empty dict if entity_type is 'character' (no alt-mapping needed).
    """
    if entity_type == "character":
        return {}

    manager = AccountManager(entity_id=entity_id, entity_type=entity_type)
    accounts = manager.get_accounts_data()

    mapping: dict[int, str] = {}
    for account in accounts.values():
        main = account.main_character
        if main:
            main_name = main.character_name
            for alt_id in account.alt_ids or []:
                mapping[alt_id] = main_name
    return mapping
