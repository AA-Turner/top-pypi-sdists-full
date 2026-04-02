"""Forms for the killstats app."""

# Django
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


def get_mandatory_form_label_text(text: str) -> str:
    """Label text for mandatory form fields"""

    required_marker = "<span class='form-required-marker'>*</span>"

    return mark_safe(
        f"<span class='form-field-required'>{text} {required_marker}</span>"
    )


class SingleKillmail(forms.Form):
    """Form for Add Single Killmails."""

    killmail_id = forms.IntegerField(
        required=True,
        min_value=1,
        label=get_mandatory_form_label_text(_("Killmail ID")),
    )
