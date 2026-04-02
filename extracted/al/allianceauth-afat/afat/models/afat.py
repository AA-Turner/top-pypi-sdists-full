"""
The models
"""

# Standard Library
from typing import Any, ClassVar

# Third Party
from solo.models import SingletonModel

# Django
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.managers import FatLinkManager, FatManager


def get_sentinel_user() -> User:
    """
    Get user or create the sentinel user

    :return:
    """

    return User.objects.get_or_create(username="deleted")[0]


def get_hash_on_save() -> str:
    """
    Get the hash

    :return:
    """

    fatlink_hash = get_random_string(length=30)

    while FatLink.objects.filter(hash=fatlink_hash).exists():
        fatlink_hash = get_random_string(length=30)

    return fatlink_hash


class General(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        AaAfat :: Meta
        """

        managed = False
        default_permissions = ()
        permissions = (
            # can access and register his own participation to a FAT link
            ("basic_access", _("Can access the AFAT module")),
            # Can manage the FAT module
            # Has:
            #   » add_fatlink
            #   » change_fatlink
            #   » delete_fatlink
            #   » add_fat
            #   » delete_fat
            ("manage_afat", _("Can manage the AFAT module")),
            # Can add a new FAT link
            ("add_fatlink", _("Can create FAT links")),
            # Can see own corp stats
            ("stats_corporation_own", _("Can see own corporation statistics")),
            # Can see the stats of all corps
            ("stats_corporation_other", _("Can see statistics of other corporations")),
            # Can view the modules log
            ("log_view", _("Can view the modules log")),
        )
        verbose_name = _("AFAT")


class FleetType(models.Model):
    """
    FAT link fleet type

    Example:
        - CTA
        - Home Defense
        - StratOP
        - and so on …
    """

    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=254, help_text=_("Descriptive name of the fleet type")
    )

    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this fleet type is active or not"),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("Fleet type")
        verbose_name_plural = _("Fleet types")

    def __str__(self) -> str:
        """
        Return the objects string name

        :return:
        :rtype:
        """

        return str(self.name)


class FatLink(models.Model):
    """
    FAT link
    """

    class EsiError(models.TextChoices):
        """
        Choices for SRP Status
        """

        NOT_IN_FLEET = "NOT_IN_FLEET", _(
            "FC is not in the registered fleet anymore or fleet is no longer available."
        )
        NO_FLEET = "NO_FLEET", _("Registered fleet seems to be no longer available.")
        NOT_FLEETBOSS = "NOT_FLEETBOSS", _("FC is no longer the fleet boss.")
        FC_WRONG_FLEET = "FC_WRONG_FLEET", _("FC switched to another fleet.")

    created = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text=_("When was this FAT link created"),
    )

    fleet = models.CharField(
        max_length=254,
        blank=False,
        default=None,
        help_text=_("The FAT link fleet name"),
    )

    hash = models.CharField(
        max_length=254, db_index=True, unique=True, help_text=_("The FAT link hash")
    )

    creator = models.ForeignKey(
        to=User,
        related_name="+",
        on_delete=models.SET(get_sentinel_user),
        help_text=_("Who created the FAT link?"),
    )

    character = models.ForeignKey(
        to=EveCharacter,
        related_name="+",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        help_text=_("Character this FAT link has been created with"),
    )

    link_type = models.ForeignKey(
        to=FleetType,
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        help_text="Deprecated setting, will be removed in a future version …",
    )

    fleet_type = models.CharField(
        blank=True,
        default="",
        max_length=254,
        help_text=_("The FAT link fleet type, if it's set"),
    )

    doctrine = models.CharField(
        blank=True, default="", max_length=254, help_text=_("The FAT link doctrine")
    )

    is_esilink = models.BooleanField(
        default=False, help_text=_("Whether this FAT link was created via ESI or not")
    )

    is_registered_on_esi = models.BooleanField(
        default=False,
        help_text=_("Whether the fleet to this FAT link is available in ESI or not"),
    )

    esi_fleet_id = models.BigIntegerField(blank=True, null=True)

    reopened = models.BooleanField(
        default=False, help_text=_("Has this FAT link being re-opened?")
    )

    last_esi_error = models.CharField(
        max_length=15, blank=True, default="", choices=EsiError.choices
    )

    last_esi_error_time = models.DateTimeField(null=True, blank=True, default=None)

    esi_error_count = models.IntegerField(default=0)

    objects: ClassVar[FatLinkManager] = FatLinkManager()

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        ordering = ("-created",)
        verbose_name = _("FAT link")
        verbose_name_plural = _("FAT links")

    def __str__(self) -> str:
        """
        Return the objects string name

        :return:
        :rtype:
        """

        return f"{self.fleet} - {self.hash}"

    @transaction.atomic()
    def save(self, *args, **kwargs):
        """
        Add the hash on save

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """

        try:
            self.hash
        except ObjectDoesNotExist:
            self.hash = get_hash_on_save()

        super().save(*args, **kwargs)

    @property
    def number_of_fats(self):
        """
        Returns the number of registered FATs

        :return:
        :rtype:
        """

        return self.afat_fats.count()


class Duration(models.Model):
    """
    FAT link duration (expiry time in minutes)
    """

    duration = models.PositiveIntegerField()
    fleet = models.ForeignKey(
        to=FatLink, related_name="duration", on_delete=models.CASCADE
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("FAT link duration")
        verbose_name_plural = _("FAT link durations")


# AFat Model
class Fat(models.Model):
    """
    AFat
    """

    character = models.ForeignKey(
        to=EveCharacter,
        related_name="afat_fats",
        on_delete=models.CASCADE,
        help_text=_("Character who registered this FAT"),
    )

    corporation_eve_id = models.BigIntegerField(
        null=True,
        help_text=_(
            "Corporation EVE ID of the character who registered this FAT at the time of registration"
        ),
    )

    alliance_eve_id = models.BigIntegerField(
        null=True,
        help_text=_(
            "Alliance EVE ID of the character who registered this FAT at the time of registration"
        ),
    )

    fatlink = models.ForeignKey(
        to=FatLink,
        related_name="afat_fats",
        on_delete=models.CASCADE,
        help_text=_("The FAT link the character registered at"),
    )

    system = models.CharField(
        max_length=100, null=True, help_text=_("The system the character is in")
    )

    shiptype = models.CharField(
        max_length=100,
        null=True,
        db_index=True,
        help_text=_("The ship the character was flying"),
    )

    objects: ClassVar[FatManager] = FatManager()

    class Meta:  # pylint: disable=too-few-public-methods
        """
        AFat :: Meta
        """

        default_permissions = ()
        unique_together = (("character", "fatlink"),)
        verbose_name = _("FAT")
        verbose_name_plural = _("FATs")

    def __str__(self) -> str:
        """
        Return the objects string name

        :return:
        :rtype:
        """

        return f"{self.fatlink} - {self.character}"


# AFat Log Model
class Log(models.Model):
    """
    The log
    """

    class Event(models.TextChoices):
        """
        Choices for log event
        """

        CREATE_FATLINK = "CR_FAT_LINK", _("FAT link created")
        CHANGE_FATLINK = "CH_FAT_LINK", _("FAT link changed")
        DELETE_FATLINK = "RM_FAT_LINK", _("FAT link removed")
        REOPEN_FATLINK = "RO_FAT_LINK", _("FAT link re-opened")
        # CREATE_FAT = "CR_FAT", _("FAT registered")
        DELETE_FAT = "RM_FAT", _("FAT removed")
        MANUAL_FAT = "CR_FAT_MAN", _("Manual FAT added")

    log_time = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.ForeignKey(
        to=User,
        related_name="afat_log",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET(value=get_sentinel_user),
    )
    log_event = models.CharField(
        max_length=11,
        blank=False,
        choices=Event.choices,
        default=Event.CREATE_FATLINK,
    )
    log_text = models.TextField()
    fatlink_hash = models.CharField(max_length=254)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        AFatLog :: Meta
        """

        default_permissions = ()
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")


class Doctrine(models.Model):
    """
    Fleet Doctrines
    """

    # Doctrine name
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Short name to identify this doctrine"),
        verbose_name=_("Name"),
    )

    # Doctrine notes
    notes = models.TextField(
        default="",
        blank=True,
        help_text=_(
            "You can add notes about this doctrine here if you want. (optional)"
        ),
        verbose_name=_("Notes"),
    )

    # Is doctrine active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this doctrine is enabled or not."),
        verbose_name=_("Is enabled"),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        FleetDoctrine :: Meta
        """

        verbose_name = _("Doctrine")
        verbose_name_plural = _("Doctrines")
        default_permissions = ()

    def __str__(self) -> str:
        """
        String representation of the object

        :return:
        :rtype:
        """

        return str(self.name)


class Setting(SingletonModel):
    """
    Default forum settings
    """

    class Field(models.TextChoices):
        """
        Choices for Setting.Field
        """

        DEFAULT_FATLINK_EXPIRY_TIME = "default_fatlink_expiry_time", _(
            "Default FAT link expiry time"
        )
        DEFAULT_FATLINK_REOPEN_DURATION = "default_fatlink_reopen_duration", _(
            "Default FAT link reopen duration"
        )
        DEFAULT_FATLINK_REOPEN_GRACE_TIME = "default_fatlink_reopen_grace_time", _(
            "Default FAT link reopen grace time"
        )
        DEFAULT_LOG_DURATION = "default_log_duration", _("Default log duration")
        USE_DOCTRINES_FROM_FITTINGS_MODULE = "use_doctrines_from_fittings_module", _(
            "Use doctrines from fittings module"
        )

    default_fatlink_expiry_time = models.PositiveIntegerField(
        default=60,
        help_text=_(
            "Default expiry time for clickable FAT links in minutes. "
            "(Default: 60 minutes)"
        ),
        verbose_name=Field.DEFAULT_FATLINK_EXPIRY_TIME.label,  # pylint: disable=no-member
    )

    default_fatlink_reopen_grace_time = models.PositiveIntegerField(
        default=60,
        help_text=_(
            "Default time in minutes a FAT link can be re-opened after it is expired. "
            "(Default: 60 minutes)"
        ),
        verbose_name=Field.DEFAULT_FATLINK_REOPEN_GRACE_TIME.label,  # pylint: disable=no-member
    )

    default_fatlink_reopen_duration = models.PositiveIntegerField(
        default=60,
        help_text=_(
            "Default time in minutes a FAT link is re-opened for. "
            "(Default: 60 minutes)"
        ),
        verbose_name=Field.DEFAULT_FATLINK_REOPEN_DURATION.label,  # pylint: disable=no-member
    )

    default_log_duration = models.PositiveIntegerField(
        default=60,
        help_text=_("Default time in days a log entry is kept. (Default: 60 days)"),
        verbose_name=Field.DEFAULT_LOG_DURATION.label,  # pylint: disable=no-member
    )

    use_doctrines_from_fittings_module = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_(
            "Whether to use the doctrines from the Fittings modules in the doctrine "
            "dropdown. Note: The fittings module needs to be installed for this."
        ),
        verbose_name=Field.USE_DOCTRINES_FROM_FITTINGS_MODULE.label,  # pylint: disable=no-member
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Setting :: Meta
        """

        default_permissions = ()
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self) -> str:
        """
        String representation of the object

        :return:
        :rtype:
        """

        return str(_("AFAT Settings"))

    @staticmethod
    def get_setting(setting_key: str) -> Any:
        """
        Get the setting value for a given setting key

        :param setting_key: The setting key
        :type setting_key: str
        :return: The setting value
        :rtype: Any
        """

        try:
            return getattr(Setting.get_solo(), setting_key)
        except AttributeError as exc:
            raise KeyError(f"Setting key '{setting_key}' does not exist.") from exc
