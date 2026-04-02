"""Forms for Inactivity."""

from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .models import LeaveOfAbsence


class CreateRequestForm(forms.ModelForm):
    """A form for creating a new inactivity request."""

    def __init__(self, *args, **kwargs) -> None:
        self._user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["notes"].required = True

    class Meta:
        model = LeaveOfAbsence
        fields = ["start", "end", "notes"]

    def clean(self):
        data = super().clean()
        start = data["start"] if "start" in data else None
        end = data["end"] if "end" in data else None
        today = now().date()

        if end and start and end < start:
            raise ValidationError({"end": _("End date must be after the start date.")})

        if start and start < today:
            raise ValidationError({"start": _("Start date can not be in the past.")})

        if start:
            pending = LeaveOfAbsence.objects.filter_pending().filter(user=self._user)
            overlapping = False
            if end:
                if pending.exclude(Q(end__lte=start) | Q(start__gte=end)).exists():
                    overlapping = True
            else:
                if pending.exclude(end__lte=start).exists():
                    overlapping = True

            if overlapping:
                raise ValidationError(
                    _(
                        "There already exists a pending request overlapping with "
                        "this time frame. "
                        "Please adjust the time frame or cancel the existing request."
                    )
                )

    def save(self, *args, **kwargs) -> Any:
        self.instance.user = self._user  # add current user
        return super().save(*args, **kwargs)


class RejectRequestForm(forms.Form):
    """A form for rejecting an inactivity request."""

    request = forms.CharField(
        disabled=True,
        help_text="The leave of absence request to be rejected",
        required=False,
    )
    reason = forms.CharField(
        label="Reason",
        max_length=100,
        required=True,
        help_text="Reason for rejecting this request",
    )
