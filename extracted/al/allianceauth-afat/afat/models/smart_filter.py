"""
AFAT Smart Filter
"""

# Standard Library
import datetime
from collections import defaultdict

# Third Party
from eve_sde.models import ItemType

# Django
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.models.afat import Fat, FleetType
from afat.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


def _get_threshold_date(timedelta_in_days: int) -> datetime.datetime:
    """
    Get the threshold date

    :param timedelta_in_days: The timedelta in days
    :type timedelta_in_days: int
    :return: The threshold date
    :rtype: datetime.datetime
    """

    return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        days=timedelta_in_days
    )


class BaseFilter(models.Model):
    """
    BaseFilter
    """

    name = models.CharField(
        max_length=500,
        help_text=_("The filter name that is shown to the admin."),
    )  # this is the name of the filter

    description = models.CharField(
        max_length=500,
        help_text=_("The filter description that is shown to end users."),
    )  # this is what is shown to the user

    class Meta:
        """
        Model meta definitions
        """

        abstract = True

    def __str__(self) -> str:
        """
        Model string representation

        :return: The model string representation
        :rtype: str
        """

        return f"{self.name}: {self.description}"

    def process_filter(self, user: User) -> bool:
        """
        Process the filter

        :param user: The user
        :type user: User
        :return: Return True when filter applies to the user, else False.
        :rtype: bool
        """

        raise NotImplementedError(_("Please create a filter!"))

    def audit_filter(self, users: models.QuerySet[User]) -> dict:
        """
        Return information for each given user weather they pass the filter,
        and a help message shown in the audit feature.

        :param users: The users
        :type users: models.QuerySet[User]
        :return: The audit information
        :rtype: dict
        """

        raise NotImplementedError(_("Please create an audit function!"))


class FatsInTimeFilter(BaseFilter):
    """
    FatsInTimeFilter
    """

    days = models.IntegerField(
        default=30, help_text=_("The number of days to look back for FATs.")
    )
    fats_needed = models.IntegerField(
        default=10, help_text=_("The number of FATs needed to pass the filter.")
    )
    fleet_types = models.ManyToManyField(
        to=FleetType,
        blank=True,
        help_text=_("Any of the selected fleet types are needed to pass the filter."),
    )
    ship_classes = models.ManyToManyField(
        to=ItemType,
        blank=True,
        limit_choices_to={"group__category_id": 6},
        help_text=_("Any of the selected ship classes are needed to pass the filter."),
    )

    class Meta:
        """
        Model meta definitions
        """

        verbose_name = _("Smart Filter: FATs in time period")
        verbose_name_plural = verbose_name

    def process_filter(self, user: User):
        """
        Process the filter

        :param user:
        :type user:
        :return:
        :rtype:
        """

        try:
            start_time = _get_threshold_date(timedelta_in_days=self.days)
            character_list = user.character_ownerships.all().select_related("character")
            character_ids = character_list.values_list(
                "character__character_id", flat=True
            )
            ship_classes = self.ship_classes.all().values_list("name", flat=True)
            fleet_types = self.fleet_types.all().values_list("name", flat=True)

            fats = Fat.objects.filter(
                character__character_id__in=character_ids,
                fatlink__created__gte=start_time,
            )

            if ship_classes.exists():
                fats = fats.filter(shiptype__in=ship_classes)

            if fleet_types.exists():
                fats = fats.filter(fatlink__fleet_type__in=fleet_types)

            return fats.count() >= self.fats_needed
        except CharacterOwnership.DoesNotExist:
            # If the user does not have any characters, return False
            return False

    def audit_filter(self, users):
        """
        Audit the users for the filter

        :param users:
        :type users:
        :return:
        :rtype:
        """

        character_list = CharacterOwnership.objects.filter(user__in=users)
        start_time = _get_threshold_date(timedelta_in_days=self.days)
        ship_classes = self.ship_classes.all().values_list("name", flat=True)
        fleet_types = self.fleet_types.all().values_list("name", flat=True)

        fats = Fat.objects.filter(
            character__in=character_list.values("character"),
            fatlink__created__gte=start_time,
        ).select_related("character__character_ownership__user", "character")

        if ship_classes.exists():
            fats = fats.filter(shiptype__in=ship_classes)

        if fleet_types.exists():
            fats = fats.filter(fatlink__fleet_type__in=fleet_types)

        users = defaultdict(list)
        for f in fats:
            users[f.character.character_ownership.user.pk].append(f.id)

        output = defaultdict(lambda: {"message": 0, "check": False})
        for u, fat_list in users.items():
            pass_fail = False

            if len(fat_list) >= self.fats_needed:
                pass_fail = True
            output[u] = {"message": len(fat_list), "check": pass_fail}

        return output
