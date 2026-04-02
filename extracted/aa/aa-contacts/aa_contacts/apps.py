from django.apps import AppConfig
from aa_contacts import __version__


class AAContactsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aa_contacts"
    verbose_name = f"Contacts v{__version__}"
