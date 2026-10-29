__lazy_modules__ = ["django.utils.functional"]

from typing import TYPE_CHECKING, Literal
from uuid import uuid4

from solo.models import SingletonModel

from django.db import models
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.utils.functional import Promise


class AnalyticsIdentifier(SingletonModel):

    identifier = models.UUIDField(default=uuid4, editable=False)

    def __str__(self) -> str | Promise | Literal["Analytics Identifier"]: # pyright: ignore[reportIncompatibleMethodOverride]
        return _("Analytics Identifier")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        verbose_name = _("analytics identifier")


class AnalyticsTokens(models.Model):

    class AnalyticsType(models.TextChoices):
        GA_U = 'GA-U', _('Google Analytics Universal')
        GA_V4 = 'GA-V4', _('Google Analytics V4')

    name = models.CharField(max_length=254)
    type = models.CharField(max_length=254, choices=AnalyticsType.choices)
    token = models.CharField(max_length=254, blank=False)
    secret = models.CharField(max_length=254, blank=True)
    send_stats = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("analytics token")
        verbose_name_plural = _("analytics tokens")
