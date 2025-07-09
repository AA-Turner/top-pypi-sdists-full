from django.utils.translation import gettext as _
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import IntegerPreference, StringPreference
from dynamic_preferences.users.registries import user_preferences_registry

from wbcore.contrib.dynamic_preferences.types import ChoicePreference, LanguageChoicePreference

wbcore = Section("wbcore")


@global_preferences_registry.register
class RetentionPeriod(IntegerPreference):
    section = wbcore
    name = "retention_period"
    default = 365

    verbose_name = _("Retention Period in Days")
    help_text = _(
        "When an object cannot be deleted and is disabled instead, it gets hidden from the queryset but not deleted. For compliance reasons we enable the retention for a specific period of days (defaults to a year)"
    )


@global_preferences_registry.register
class SystemUserEmailPeriod(StringPreference):
    section = wbcore
    name = "system_user_email"

    default = "system@stainly-bench.com"

    verbose_name = _("System User Email")
    help_text = _("System User Email")


@user_preferences_registry.register
class LanguagePreference(LanguageChoicePreference):
    weight = -1
    choices = [
        ("de", "Deutsch"),
        ("fr", "Français"),
        ("en", "English"),
    ]

    section = wbcore
    name = "language"
    default = "en"

    verbose_name = _("System Language")
    help_text = _("Select the language you want the Workbench to display.")


@user_preferences_registry.register
class DateFormatPreference(ChoicePreference):
    weight = 0
    choices = [
        ("DD.MM.YYYY", "13.04.2007"),
        ("DD/MM/YYYY", "13/04/2007"),
        ("DD-MM-YYYY", "13-04-2007"),
        ("MM/DD/YYYY", "04/13/2007"),
        ("MM-DD-YYYY", "04-13-2007"),
        ("YYYY/MM/DD", "2007/04/13"),
        ("YYYY-MM-DD", "2007-04-13"),
        ("MMM DD, YYYY", "April 13, 2007"),
        ("DD MMM YYYY", "13 April 2007"),
        ("dddd, DD MMM YYYY", "Friday, 13 April 2007"),
        ("ddd, DD MMM YYYY", "Fri, 13 April 2007"),
        ("ddd Do MMMM YYYY", "Fri 13th April 2007"),
    ]

    section = wbcore
    name = "date_format"
    default = "YYYY-MM-DD"

    verbose_name = _("Date Format")
    help_text = _("Choose how you want dates to appear throughout the Workbench.")


@user_preferences_registry.register
class TimeFormatPreference(ChoicePreference):
    weight = 1
    choices = [
        ("HH:mm", "14:05"),
        ("hh:mm", "02:05"),
        ("h:mm", "2:05"),
        ("HH [h] mm", "14 h 05"),
        ("HH[h]mm", "14h05"),
        ("h:mm A", "2:05 PM"),
        ("h:mm a", "2:05 pm"),
        ("hh:mm A", "02:05 PM"),
        ("hh:mm a", "02:05 pm"),
    ]

    section = wbcore
    name = "time_format"
    default = "HH:mm"

    verbose_name = _("Time Format")
    help_text = _("Choose how you want times to appear throughout the Workbench.")


@user_preferences_registry.register
class NumberFormatPreference(ChoicePreference):
    weight = 2
    # Value is a BCP 47 language tag
    choices = [
        ("en-US", "1,234,567.89"),
        ("fr-FR", "1\u202f234\u202f567,89"),
        ("de-DE", "1.234.567,89"),
        ("de-CH", "1’234’567.89"),
    ]

    section = wbcore
    name = "number_format"
    default = "en-US"

    verbose_name = _("Number Format")
    help_text = _("Choose how you want numbers to appear throughout the Workbench.")
