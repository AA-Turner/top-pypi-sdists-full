# Standard Library
from typing import TYPE_CHECKING

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
from killstats.managers.killboard_manager import AttackerManager, KillmailManager
from killstats.models.general import EveEntity
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class Killmail(models.Model):
    if TYPE_CHECKING:
        attacker_killmail: models.QuerySet["Attacker"]

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(
                fields=["killmail_date"],
                name="km_date_idx",
            ),
            models.Index(
                fields=["victim_corporation_id", "-killmail_date"],
                name="km_corp_loss_idx",
            ),
            models.Index(
                fields=["victim_alliance_id", "-killmail_date"],
                name="km_ally_loss_idx",
            ),
            models.Index(
                fields=["victim_corporation_id", "-victim_total_value"],
                name="km_corp_val_idx",
            ),
            models.Index(
                fields=["victim_alliance_id", "-victim_total_value"],
                name="km_ally_val_idx",
            ),
            models.Index(fields=["-victim_total_value"], name="km_val_desc_idx"),
            models.Index(fields=["victim_solar_system_id"], name="km_system_idx"),
        ]

    objects: KillmailManager = KillmailManager()

    killmail_id = models.PositiveIntegerField(primary_key=True)
    killmail_date = models.DateTimeField(null=True, blank=True, max_length=0)
    victim = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, null=True, related_name="victim_killmail"
    )
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
    if TYPE_CHECKING:
        attacker_character: models.QuerySet["Attacker"]
        victim_killmail: models.QuerySet["Killmail"]

    objects: AttackerManager = AttackerManager()

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
        related_name="attacker_corporation",
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
        indexes = [
            # Corporation-level queries: filter by corp, group by character,
            # join to killmail for date range – all columns in one index.
            models.Index(
                fields=["corporation_id", "killmail_id"],
                name="attacker_corp_km_idx",
            ),
            # Alliance-level queries (same pattern as corp)
            models.Index(
                fields=["alliance_id", "killmail_id"],
                name="attacker_ally_km_idx",
            ),
            # Character-level queries (character killboard)
            models.Index(
                fields=["character_id", "killmail_id"],
                name="attacker_char_km_idx",
            ),
            # Hall-of-Fame: filter by corp/ally + final_blow=True
            models.Index(
                fields=["corporation_id", "final_blow"],
                name="attacker_corp_fb_idx",
            ),
            models.Index(
                fields=["alliance_id", "final_blow"],
                name="attacker_ally_fb_idx",
            ),
            models.Index(
                fields=["killmail_id", "final_blow"],
                name="att_km_final_blow_idx",
            ),
        ]
