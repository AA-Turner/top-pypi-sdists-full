"""
The forms we use
"""

# Standard Library
import re
from typing import Any

# Django
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth AFAT
from afat import __title__
from afat.models import Doctrine, Setting
from afat.providers import AppLogger

# Initialize a logger with a custom tag for the AA SRP application
logger = AppLogger(my_logger=get_extension_logger(__name__), prefix=__title__)


def get_mandatory_form_label_text(text):
    """
    Label text for mandatory form fields

    :param text:
    :type text:
    :return:
    :rtype:
    """

    required_text = _("This field is mandatory")
    required_marker = (
        f'<span aria-label="{required_text}" class="form-required-marker">*</span>'
    )

    return mark_safe(
        f'<span class="form-field-required">{text} {required_marker}</span>'
    )


def sanitize_cleaned_data(cleaned_data: dict[str, Any] | None) -> dict[str, Any] | None:
    """
    Sanitize all string values in cleaned_data:
    - Remove simple HTML tags
    - Remove control characters (but preserve line breaks and tabs)
    - Collapse intra-line whitespace and trim, preserving line breaks

    :param cleaned_data: The cleaned_data dictionary to sanitize.
    :type cleaned_data: dict[str, Any] | None
    :return: The sanitized cleaned_data dictionary.
    :rtype: dict[str, Any] | None
    """

    if not cleaned_data:
        return cleaned_data

    for field, value in list(cleaned_data.items()):
        if isinstance(value, str):
            # Remove simple HTML tags
            cleaned = re.sub(pattern=r"<[^>]*?>", repl="", string=value)

            # Remove control characters except tab (\x09), line feed (\x0a) and carriage return (\x0d)
            cleaned = re.sub(
                pattern=r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+", repl="", string=cleaned
            )

            # Normalize CRLF and CR to LF
            cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

            # Collapse spaces/tabs within each line but preserve line breaks
            lines = cleaned.split("\n")
            processed_lines = [
                re.sub(pattern=r"[ \t]+", repl=" ", string=line).strip()
                for line in lines
            ]
            cleaned = "\n".join(processed_lines)

            if cleaned != value:
                logger.debug(f"Sanitized field: {field}")

            cleaned_data[field] = cleaned

    return cleaned_data


class AFatEsiFatForm(forms.Form):
    """
    Fat link form
    Used to create ESI FAT links
    """

    name_esi = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Fleet name")),
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": _("Enter fleet name")}),
    )
    type_esi = forms.CharField(
        required=False,
        label=_("Fleet type (optional)"),
        widget=forms.TextInput(
            attrs={
                "data-datalist": "afat-fleet-type-list",
                "data-full-width": "true",
            }
        ),
    )
    doctrine_esi = forms.CharField(
        required=False,
        label=_("Doctrine (optional)"),
        widget=forms.TextInput(
            attrs={
                "data-datalist": "afat-fleet-doctrine-list",
                "data-full-width": "true",
            }
        ),
    )

    def clean(self):
        """
        Clean all input from HTML tags and other nefarious things.

        :return: cleaned_data
        :rtype: dict
        """

        cleaned_data = super().clean()

        return sanitize_cleaned_data(cleaned_data)


class AFatManualFatForm(forms.Form):
    """
    Manual FAT form
    """

    character = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Character Name")),
        max_length=255,
    )
    system = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("System")),
        max_length=100,
    )
    shiptype = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Ship type")),
        max_length=100,
    )

    def clean(self):
        """
        Clean all input from HTML tags and other nefarious things.

        :return: cleaned_data
        :rtype: dict
        """

        cleaned_data = super().clean()

        return sanitize_cleaned_data(cleaned_data)


class AFatClickFatForm(forms.Form):
    """
    Fat link form
    Used to create clickable FAT links
    """

    name = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Fleet name")),
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": _("Enter fleet name")}),
    )
    type = forms.CharField(
        required=False,
        label=_("Fleet type (optional)"),
        widget=forms.TextInput(
            attrs={
                "data-datalist": "afat-fleet-type-list",
                "data-full-width": "true",
            }
        ),
    )
    doctrine = forms.CharField(
        required=False,
        label=_("Doctrine (optional)"),
        widget=forms.TextInput(
            attrs={
                "data-datalist": "afat-fleet-doctrine-list",
                "data-full-width": "true",
            }
        ),
    )
    duration = forms.IntegerField(
        required=True,
        label=get_mandatory_form_label_text(text=_("FAT link expiry time in minutes")),
        min_value=1,
        initial=0,
        widget=forms.TextInput(attrs={"placeholder": _("Expiry time in minutes")}),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # This is a hack to set the initial value of the duration field,
        # which comes from the settings in the database.
        self.fields["duration"].initial = Setting.get_setting(
            Setting.Field.DEFAULT_FATLINK_EXPIRY_TIME
        )

    def clean(self):
        """
        Clean all input from HTML tags and other nefarious things.

        :return: cleaned_data
        :rtype: dict
        """

        cleaned_data = super().clean()

        return sanitize_cleaned_data(cleaned_data)


class FatLinkEditForm(forms.Form):
    """
    Fat link edit form
    Used in edit view to change the fat link name
    """

    fleet = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Fleet name")),
        max_length=255,
    )

    def clean(self):
        """
        Clean all input from HTML tags and other nefarious things.

        :return: cleaned_data
        :rtype: dict
        """

        cleaned_data = super().clean()

        return sanitize_cleaned_data(cleaned_data)


class SettingAdminForm(forms.ModelForm):
    """
    Form definitions for the FleetType form
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta
        """

        model = Setting

        fields = "__all__"

    def clean(self):
        """
        Clean all input from HTML tags and other nefarious things.

        :return: cleaned_data
        :rtype: dict
        """

        cleaned_data = super().clean()

        return sanitize_cleaned_data(cleaned_data)


class DoctrineAdminForm(forms.ModelForm):
    """
    Form definitions for the Doctrine form
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta
        """

        model = Doctrine

        fields = "__all__"

    def clean(self):
        """
        Clean all input from HTML tags and other nefarious things.

        :return: cleaned_data
        :rtype: dict
        """

        cleaned_data = super().clean()

        return sanitize_cleaned_data(cleaned_data)
