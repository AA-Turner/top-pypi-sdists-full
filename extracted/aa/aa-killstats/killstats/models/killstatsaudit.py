"""
Killstats Audit Model
"""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.helpers.killmail import KillmailBody
from killstats.managers.killboardaudit_manager import (
    AllianceManager,
    CorporationManager,
)
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


class CorporationsAudit(models.Model):

    corporation = models.OneToOneField(
        EveCorporationInfo,
        on_delete=models.CASCADE,
    )

    last_update = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)

    objects = CorporationManager()

    def __str__(self):
        return f"{self.corporation.corporation_name}'s Killstats Data"

    def process_killmail(self, killmail: KillmailBody):
        """Process the killmail for this corporation"""
        if (
            killmail.victim.corporation_id == self.corporation.corporation_id
            or self.corporation.corporation_id
            in killmail.attackers_distinct_corporation_ids()
        ):
            return True
        return False

    class Meta:
        default_permissions = ()


class AlliancesAudit(models.Model):

    alliance = models.OneToOneField(
        EveAllianceInfo,
        on_delete=models.CASCADE,
    )

    last_update = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)

    objects = AllianceManager()

    def __str__(self):
        return f"{self.alliance.alliance_name}'s Killstats Data"

    def process_killmail(self, killmail: KillmailBody):
        """Process the killmail for this corporation"""
        if (
            killmail.victim.alliance_id == self.alliance.alliance_id
            or self.alliance.alliance_id in killmail.attackers_distinct_alliance_ids()
        ):
            return True
        return False

    class Meta:
        default_permissions = ()
