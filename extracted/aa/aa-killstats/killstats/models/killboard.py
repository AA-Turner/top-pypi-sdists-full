# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from eve_sde.models.types import ItemType

# AA Killstats
from killstats import __title__
from killstats.managers.killboard_manager import KillmailManager
from killstats.models.general import EveEntity
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class Killmail(models.Model):
    class Meta:
        default_permissions = ()

    objects: KillmailManager = KillmailManager()

    killmail_id = models.PositiveIntegerField(primary_key=True)
    killmail_date = models.DateTimeField(null=True, blank=True, max_length=0)
    victim = models.ForeignKey(EveEntity, on_delete=models.CASCADE, null=True)
    victim_ship = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    victim_corporation_id = models.PositiveIntegerField()
    victim_alliance_id = models.PositiveIntegerField(null=True, blank=True)
    hash = models.CharField(max_length=255, unique=True)
    # Value Infos
    victim_total_value = models.PositiveBigIntegerField(null=True, blank=True)
    victim_fitted_value = models.PositiveBigIntegerField(null=True, blank=True)
    victim_destroyed_value = models.PositiveBigIntegerField(null=True, blank=True)
    victim_dropped_value = models.PositiveBigIntegerField(null=True, blank=True)
    # Location Infos
    victim_region_id = models.PositiveIntegerField(null=True, blank=True)
    victim_solar_system_id = models.PositiveIntegerField(null=True, blank=True)
    victim_position_x = models.FloatField(null=True, blank=True)
    victim_position_y = models.FloatField(null=True, blank=True)
    victim_position_z = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Killmail {self.killmail_id} - {self.killmail_date} - {self.victim} - {self.victim_ship}"

    def get_or_unknown_victim_name(self):
        """Return the victim name or Unknown."""
        return self.victim.name if self.victim else _("Unknown")

    def get_or_unknown_victim_ship_id(self):
        """Return the victim ship ID or Unknown."""
        return self.victim_ship.id if self.victim_ship else 0

    def get_or_unknown_victim_ship_name(self):
        """Return the victim ship name or Unknown."""
        return self.victim_ship.name if self.victim_ship else _("Unknown")

    def evaluate_zkb_link(self):
        try:
            zkb = f"https://zkillboard.com/character/{self.victim.id}/"
            if self.victim.category == "corporation":
                zkb = (
                    f"https://zkillboard.com/corporation/{self.victim_corporation_id}/"
                )
            if self.victim.category == "alliance":
                zkb = f"https://zkillboard.com/alliance/{self.victim_alliance_id}/"
        except ObjectDoesNotExist:
            zkb = _("Unknown")
        return zkb


class Attacker(models.Model):
    killmail = models.ForeignKey(
        Killmail, on_delete=models.CASCADE, related_name="attacker_killmail"
    )
    character = models.ForeignKey(
        EveEntity,
        on_delete=models.CASCADE,
        related_name="attacker_character",
        null=True,
        blank=True,
    )
    corporation = models.ForeignKey(
        EveEntity,
        on_delete=models.CASCADE,
        related_name="attacker_corp",
        null=True,
        blank=True,
    )
    alliance = models.ForeignKey(
        EveEntity,
        on_delete=models.CASCADE,
        related_name="attacker_alliance",
        null=True,
        blank=True,
    )
    ship = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        related_name="attacker_ship",
        null=True,
        blank=True,
    )
    damage_done = models.IntegerField(null=True, blank=True)
    final_blow = models.BooleanField(null=True, blank=True)
    weapon_type_id = models.PositiveIntegerField(null=True, blank=True)
    security_status = models.FloatField(null=True, blank=True)

    def evaluate_attacker(self) -> tuple:
        """Return the attacker ID and Name."""
        if self.character is not None:
            return self.character.id, self.character.name
        if self.corporation is not None:
            return self.corporation.id, self.corporation.name
        if self.alliance is not None:
            return self.alliance.id, self.alliance.name
        return 0, _("Unknown")

    class Meta:
        default_permissions = ()
