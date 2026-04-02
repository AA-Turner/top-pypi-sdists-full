"""
The forms we use
"""

# Django
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Alliance Auth AFAT
from afat.models import Doctrine, Setting


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
