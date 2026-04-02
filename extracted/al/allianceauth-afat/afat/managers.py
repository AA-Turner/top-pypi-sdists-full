"""
Managers for our models
"""

# Django
from django.db import models


class FatLinkManager(models.Manager):
    """
    FAT link manager
    """

    def select_related_default(self):
        """
        Apply select_related for default query optimizations.
        """

        return self.select_related(
            "creator", "character", "creator__profile__main_character"
        )


class FatManager(models.Manager):
    """
    FAT manager
    """

    def select_related_default(self):
        """
        Apply select_related for default query optimizations.
        """

        return self.select_related("fatlink", "character")
