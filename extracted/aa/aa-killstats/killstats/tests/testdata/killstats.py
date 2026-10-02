"""
Test data factories for AA Killstats models and Pydantic schemas.
Modeled after evesde_factory and aa-beltradar conventions.
"""

# Standard Library
import secrets
from datetime import datetime, timezone
from typing import Generic, TypeVar

# Third Party
import factory
import factory.fuzzy
from evesde_factory.allianceauth import (
    BaseMetaFactory,
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
    UserFactory,
)
from evesde_factory.eve_sde import ItemTypeFactory
from evesde_factory.utils import add_character_to_user
from pydantic import BaseModel

# AA Killstats
# AA Killstats Helpers / Pydantic Models
from killstats.helpers.killmailbody import (
    KillmailAttacker,
    KillmailBody,
    KillmailItems,
    KillmailPosition,
    KillmailVictim,
    esiKillmail,
    zKBKillmail,
    zKBWebKillmail,
)

# AA Killstats Models
from killstats.models import (
    AlliancesAudit,
    Attacker,
    CorporationsAudit,
    EveEntity,
    Killmail,
)

T_Model = TypeVar("T_Model")
T_Pydantic = TypeVar("T_Pydantic", bound=BaseModel)


# ==============================================================================
# Base Factories
# ==============================================================================


class BaseDjangoModelFactory(factory.django.DjangoModelFactory):
    """Base factory for Django models providing to_model / as_model helpers."""

    @classmethod
    def to_model(cls, **kwargs):
        """Generate and save the model instance."""
        return cls.create(**kwargs)

    @classmethod
    def as_model(cls, **kwargs):
        """Alias for to_model."""
        return cls.to_model(**kwargs)


class BasePydanticFactory(factory.Factory, Generic[T_Pydantic]):
    """Base factory for Pydantic models providing model instance and serialization helpers."""

    @classmethod
    def to_model(cls, **kwargs) -> T_Pydantic:
        """Generate the model and return it as a model instance."""
        return cls.build(**kwargs)

    @classmethod
    def as_model(cls, **kwargs) -> T_Pydantic:
        """Alias for to_model."""
        return cls.to_model(**kwargs)

    @classmethod
    def to_json(cls, **kwargs) -> str:
        """Generate the model and return it as a JSON string."""
        return cls.build(**kwargs).model_dump_json()

    @classmethod
    def as_json(cls, **kwargs) -> str:
        """Alias for to_json."""
        return cls.to_json(**kwargs)

    @classmethod
    def to_dict(cls, **kwargs) -> dict:
        """Generate the model and return it as a JSON-serializable dictionary."""
        return cls.build(**kwargs).model_dump(mode="json")

    @classmethod
    def as_dict(cls, **kwargs) -> dict:
        """Alias for to_dict."""
        return cls.to_dict(**kwargs)


# ==============================================================================
# User & Auth Factories
# ==============================================================================


class UserMainFactory(UserFactory):
    """Generate a User object with a main character and default permissions for Killstats."""

    permissions__ = ["killstats.basic_access"]
    scopes__ = ["publicData"]

    @factory.post_generation
    def main_character(obj, create, _, **kwargs):
        if not create:
            return
        if "character" in kwargs:
            character = kwargs["character"]
        else:
            character_name = f"{obj.first_name} {obj.last_name}"
            character = EveCharacterFactory(character_name=character_name)

        add_character_to_user(
            user=obj,
            character=character,
            is_main=True,
            scopes=obj._main_character_scopes,
        )


# ==============================================================================
# Django Model Factories
# ==============================================================================


class EveEntityFactory(BaseDjangoModelFactory, metaclass=BaseMetaFactory[EveEntity]):
    """Generate an EveEntity object (Character, Corporation, or Alliance)."""

    class Meta:
        model = EveEntity
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: 100000 + n)
    category = EveEntity.CATEGORY_CHARACTER
    name = factory.Faker("name")
    corporation = None
    alliance = None


class EveEntityCharacterFactory(EveEntityFactory):
    category = EveEntity.CATEGORY_CHARACTER
    name = factory.Faker("name")


class EveEntityCorporationFactory(EveEntityFactory):
    category = EveEntity.CATEGORY_CORPORATION
    name = factory.Faker("company")


class EveEntityAllianceFactory(EveEntityFactory):
    category = EveEntity.CATEGORY_ALLIANCE
    name = factory.Faker("company")


class KillmailFactory(BaseDjangoModelFactory, metaclass=BaseMetaFactory[Killmail]):
    """Generate a Killmail database model object with realistic defaults."""

    class Meta:
        model = Killmail
        django_get_or_create = ("killmail_id",)

    killmail_id = factory.Sequence(lambda n: 138000000 + n)
    killmail_date = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    victim = factory.SubFactory(EveEntityCharacterFactory)
    victim_ship = factory.SubFactory(ItemTypeFactory)
    victim_corporation_id = factory.Sequence(lambda n: 98000000 + n)
    victim_alliance_id = factory.Sequence(lambda n: 99000000 + n)
    hash = factory.LazyFunction(lambda: secrets.token_hex(20))

    # Value information
    victim_total_value = factory.fuzzy.FuzzyInteger(10000, 1000000000)
    victim_fitted_value = factory.fuzzy.FuzzyInteger(5000, 500000000)
    victim_destroyed_value = factory.fuzzy.FuzzyInteger(5000, 500000000)
    victim_dropped_value = 0

    # Location information
    victim_region_id = 10000002
    victim_solar_system_id = 30000142
    victim_position_x = factory.fuzzy.FuzzyFloat(-1000000.0, 1000000.0)
    victim_position_y = factory.fuzzy.FuzzyFloat(-1000000.0, 1000000.0)
    victim_position_z = factory.fuzzy.FuzzyFloat(-1000000.0, 1000000.0)


class AttackerFactory(BaseDjangoModelFactory, metaclass=BaseMetaFactory[Attacker]):
    """Generate an Attacker database model object linked to a Killmail."""

    class Meta:
        model = Attacker

    killmail = factory.SubFactory(KillmailFactory)
    character = factory.SubFactory(EveEntityCharacterFactory)
    corporation = factory.SubFactory(EveEntityCorporationFactory)
    alliance = factory.SubFactory(EveEntityAllianceFactory)
    ship = factory.SubFactory(ItemTypeFactory)
    damage_done = factory.fuzzy.FuzzyInteger(100, 10000)
    final_blow = True
    weapon_type_id = 24475
    security_status = 5.0


class CorporationsAuditFactory(
    BaseDjangoModelFactory, metaclass=BaseMetaFactory[CorporationsAudit]
):
    """Generate a CorporationsAudit object with an associated corporation and owner."""

    class Meta:
        model = CorporationsAudit
        django_get_or_create = ("corporation",)

    corporation = factory.SubFactory(EveCorporationInfoFactory)
    owner = factory.SubFactory(EveCharacterFactory)
    last_missing_check = None


class AlliancesAuditFactory(
    BaseDjangoModelFactory, metaclass=BaseMetaFactory[AlliancesAudit]
):
    """Generate an AlliancesAudit object with an associated alliance and owner."""

    class Meta:
        model = AlliancesAudit
        django_get_or_create = ("alliance",)

    alliance = factory.SubFactory(EveAllianceInfoFactory)
    owner = factory.SubFactory(EveCharacterFactory)
    last_missing_check = None


# ==============================================================================
# Pydantic Model Factories
# ==============================================================================


class KillmailPositionFactory(
    BasePydanticFactory[KillmailPosition], metaclass=BaseMetaFactory[KillmailPosition]
):
    """Generate a KillmailPosition Pydantic model."""

    class Meta:
        model = KillmailPosition

    x = factory.fuzzy.FuzzyFloat(-1000000000.0, 1000000000.0)
    y = factory.fuzzy.FuzzyFloat(-1000000000.0, 1000000000.0)
    z = factory.fuzzy.FuzzyFloat(-1000000000.0, 1000000000.0)


class KillmailItemsFactory(
    BasePydanticFactory[KillmailItems], metaclass=BaseMetaFactory[KillmailItems]
):
    """Generate a KillmailItems Pydantic model."""

    class Meta:
        model = KillmailItems

    flag = 0
    item_type_id = 33440
    items = []
    quantity_dropped = None
    quantity_destroyed = 1
    singleton = 0


class KillmailVictimFactory(
    BasePydanticFactory[KillmailVictim], metaclass=BaseMetaFactory[KillmailVictim]
):
    """Generate a KillmailVictim Pydantic model."""

    class Meta:
        model = KillmailVictim

    character_id = factory.Sequence(lambda n: 2110000000 + n)
    corporation_id = factory.Sequence(lambda n: 98000000 + n)
    alliance_id = factory.Sequence(lambda n: 99000000 + n)
    faction_id = None
    ship_type_id = 670
    items = []
    position = factory.SubFactory(KillmailPositionFactory)
    damage_taken = factory.fuzzy.FuzzyInteger(100, 100000)


class KillmailAttackerFactory(
    BasePydanticFactory[KillmailAttacker], metaclass=BaseMetaFactory[KillmailAttacker]
):
    """Generate a KillmailAttacker Pydantic model."""

    class Meta:
        model = KillmailAttacker

    character_id = factory.Sequence(lambda n: 2110000000 + n)
    corporation_id = factory.Sequence(lambda n: 98000000 + n)
    alliance_id = factory.Sequence(lambda n: 99000000 + n)
    faction_id = None
    ship_type_id = 28710
    damage_done = factory.fuzzy.FuzzyInteger(100, 50000)
    final_blow = True
    security_status = 0.0
    weapon_type_id = 28710


class esiKillmailFactory(
    BasePydanticFactory[esiKillmail], metaclass=BaseMetaFactory[esiKillmail]
):
    """Generate an esiKillmail Pydantic model."""

    class Meta:
        model = esiKillmail

    killmail_id = factory.Sequence(lambda n: 138000000 + n)
    killmail_time = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    solar_system_id = 30000142
    victim = factory.SubFactory(KillmailVictimFactory)

    @factory.lazy_attribute
    def attackers(self):
        return [KillmailAttackerFactory()]


class zKBKillmailFactory(
    BasePydanticFactory[zKBKillmail], metaclass=BaseMetaFactory[zKBKillmail]
):
    """Generate a zKBKillmail Pydantic model."""

    class Meta:
        model = zKBKillmail

    locationID = factory.Sequence(lambda n: 40000000 + n)
    hash = factory.LazyFunction(lambda: secrets.token_hex(20))
    fittedValue = 10000.0
    droppedValue = 0.0
    destroyedValue = 10000.0
    totalValue = 10000.0
    totalDroppableValue = 0.0
    points = 1
    npc = False
    solo = False
    awox = False
    labels = ["pvp", "loc:nullsec"]
    attackerCount = 1
    href = factory.LazyAttribute(
        lambda o: f"https://esi.evetech.net/killmails/{secrets.token_hex(4)}/{o.hash}/"
    )


class KillmailBodyFactory(
    BasePydanticFactory[KillmailBody], metaclass=BaseMetaFactory[KillmailBody]
):
    """Generate a KillmailBody Pydantic model."""

    class Meta:
        model = KillmailBody

    killmail_id = factory.Sequence(lambda n: 138000000 + n)
    hash = factory.LazyFunction(lambda: secrets.token_hex(20))
    esi = factory.SubFactory(esiKillmailFactory)
    zkb = factory.SubFactory(zKBKillmailFactory)

    moon_id = None
    war_id = None
    uploaded_at = None
    sequence_id = factory.Sequence(lambda n: 99000000 + n)


class zKBWebKillmailFactory(
    BasePydanticFactory[zKBWebKillmail], metaclass=BaseMetaFactory[zKBWebKillmail]
):
    """Generate a zKBWebKillmail Pydantic model for HTTP API payloads."""

    class Meta:
        model = zKBWebKillmail

    killmail_id = factory.Sequence(lambda n: 138000000 + n)
    killmail_time = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    solar_system_id = 30000142
    victim = factory.SubFactory(KillmailVictimFactory)
    zkb = factory.SubFactory(zKBKillmailFactory)

    @factory.lazy_attribute
    def attackers(self):
        return [KillmailAttackerFactory()]
