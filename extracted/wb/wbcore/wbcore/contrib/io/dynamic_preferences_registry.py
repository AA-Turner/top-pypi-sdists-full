from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import IntegerPreference, StringPreference

io = Section("io")


@global_preferences_registry.register
class AdministratorMailsPreference(StringPreference):
    section = io
    name = "administrator_mails"
    default = ""

    verbose_name = "Administrator mails"
    help_text = "The mails (as comma separated string) of the person allow to send directly to the mail backend"


@global_preferences_registry.register
class ImportSourceDataRetentionPeriod(IntegerPreference):
    section = io
    name = "import_source_retention_period"
    default = 365

    verbose_name = "Import Source Retention Period"
    help_text = "The number of days to keep the data and log info until cleanup"
