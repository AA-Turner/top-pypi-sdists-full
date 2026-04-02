"""Purge data management command for Eve Universe."""

import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from eveuniverse import __title__
from eveuniverse.models.base import EveUniverseBaseModel
from eveuniverse.utils import LoggerAddTag

from . import get_input

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class Command(BaseCommand):
    help = (
        "Removes all app-related data from the database. "
        "Run this command before zero migrations, "
        "which would otherwise fail due to FK constraints."
    )

    def _purge_all_data(self):
        """updates all SDE models from ESI and provides progress output"""
        with transaction.atomic():
            for MyModel in EveUniverseBaseModel.all_models():
                self.stdout.write(
                    "Deleting {:,} objects from {}".format(
                        MyModel.objects.count(),
                        MyModel.__name__,
                    )
                )
                MyModel.objects.all().delete()

    def handle(self, *args, **options):
        self.stdout.write(
            "This command will delete all app related data in the database. "
            "This can not be undone. Note that this can disrupt other apps "
            "that relate to this data. Use with caution."
        )
        user_input = get_input("Are you sure you want to proceed? (y/N)?")
        if user_input.lower() == "y":
            self.stdout.write("Starting data purge. Please stand by.")
            self._purge_all_data()
            self.stdout.write(self.style.SUCCESS("Purge complete!"))
        else:
            self.stdout.write(self.style.WARNING("Aborted"))
