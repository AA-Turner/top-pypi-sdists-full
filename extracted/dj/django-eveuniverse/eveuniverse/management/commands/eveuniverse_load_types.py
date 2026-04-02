"""Load types management command for Eve Universe."""

import logging

from django.core.management.base import BaseCommand

from eveuniverse import __title__, tasks
from eveuniverse.core.esitools import is_esi_online
from eveuniverse.models.base import determine_effective_sections
from eveuniverse.utils import LoggerAddTag

from . import EXPECTATION_TEXT, get_input

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class Command(BaseCommand):
    help = (
        "Loads large sets of types as specified from ESI into the local database."
        " This is a helper command meant to be called from other apps only."
    )

    def add_arguments(self, parser):
        parser.add_argument("app_name", help="Name of app this data is loaded for")
        parser.add_argument(
            "--category_id",
            action="append",
            type=int,
            help="Eve category ID to be loaded excl. dogma",
        )
        parser.add_argument(
            "--category_id_with_dogma",
            action="append",
            type=int,
            help="Eve category ID to be loaded incl. dogma",
        )
        parser.add_argument(
            "--group_id",
            action="append",
            type=int,
            help="Eve group ID to be loaded  excl. dogma",
        )
        parser.add_argument(
            "--group_id_with_dogma",
            action="append",
            type=int,
            help="Eve group ID to be loaded incl. dogma",
        )
        parser.add_argument(
            "--type_id",
            action="append",
            type=int,
            help="Eve type ID to be loaded  excl. dogma",
        )
        parser.add_argument(
            "--type_id_with_dogma",
            action="append",
            type=int,
            help="Eve type ID to be loaded  incl. dogma",
        )
        parser.add_argument(
            "--disable_esi_check",
            action="store_true",
            help="Disables checking that ESI is online",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            help="Do NOT prompt the user for input of any kind.",
        )

    def write_to_be_loaded(self, name, *items):
        items_count = sum_items(*items)
        if items_count:
            self.stdout.write(f"{name} to be loaded: {items_count}")

    def handle(self, *args, **options):
        self.stdout.write("Eve Universe - Types Loader")
        self.stdout.write("===========================")

        app_name = options["app_name"]
        category_ids = options["category_id"]
        category_ids_with_dogma = options["category_id_with_dogma"]
        group_ids = options["group_id"]
        group_ids_with_dogma = options["group_id_with_dogma"]
        type_ids = options["type_id"]
        type_ids_with_dogma = options["type_id_with_dogma"]

        if (
            not category_ids
            and not category_ids_with_dogma
            and not group_ids
            and not group_ids_with_dogma
            and not type_ids
            and not type_ids_with_dogma
        ):
            self.stdout.write(self.style.WARNING("No IDs specified. Nothing to do."))
            return

        self.stdout.write("Checking ESI...", ending="")
        if not options["disable_esi_check"] and not is_esi_online():
            self.stdout.write(
                "ESI does not appear to be online at this time. Please try again later."
            )
            self.stdout.write(self.style.WARNING("Aborted"))
            return
        self.stdout.write("ONLINE")
        self.stdout.write(
            f"This command will start loading data for the app: {app_name}."
        )
        self.write_to_be_loaded("Categories", category_ids, category_ids_with_dogma)
        self.write_to_be_loaded("Groups", group_ids, group_ids)
        self.write_to_be_loaded("Types", type_ids, type_ids_with_dogma)
        additional_objects = list(determine_effective_sections())
        if additional_objects:
            self.stdout.write(
                "It will also load the following additional entities when related to "
                "objects loaded for the app: "
                f"{','.join(additional_objects)}"
            )
        self.stdout.write(EXPECTATION_TEXT)
        if not options["noinput"]:
            user_input = get_input("Are you sure you want to proceed? (Y/n)? ")
        else:
            user_input = "y"
        if user_input.lower() != "n":
            if category_ids or group_ids or type_ids:
                tasks.load_eve_types.delay(
                    category_ids=category_ids, group_ids=group_ids, type_ids=type_ids
                )  # type: ignore
            if category_ids_with_dogma or group_ids_with_dogma or type_ids_with_dogma:
                tasks.load_eve_types.delay(
                    category_ids=category_ids_with_dogma,
                    group_ids=group_ids_with_dogma,
                    type_ids=type_ids_with_dogma,
                    force_loading_dogma=True,
                )  # type: ignore
            self.stdout.write(self.style.SUCCESS("Data load started!"))
        else:
            self.stdout.write(self.style.WARNING("Aborted"))


def sum_items(*items) -> int:
    total = 0
    for item in items:
        try:
            total += len(item)
        except TypeError:
            pass
    return total
