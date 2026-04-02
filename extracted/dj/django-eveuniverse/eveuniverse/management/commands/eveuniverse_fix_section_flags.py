"""Fix sections in management command for Eve Universe."""

import logging

from django.core.management.base import BaseCommand, CommandParser
from django.db.models import Count

from eveuniverse import __title__
from eveuniverse.models import EvePlanet, EveSolarSystem
from eveuniverse.utils import LoggerAddTag

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


class Command(BaseCommand):
    help = "Fixes incorrect enabled sections flags for solar systems and planets. "

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--check",
            action="store_true",
            help="Will not write changes when flag is active.",
        )

    def handle(self, *args, **options):
        my_map = [
            (EveSolarSystem, "planets", "eve_planets", 1),
            (EvePlanet, "moons", "eve_moons", 2),
        ]
        for model_class, flag_name, relation_name, value in my_map:
            objs_to_fix = (
                model_class.objects.filter(enabled_sections=value)
                .annotate(child_count=Count(relation_name))
                .filter(child_count=0)
            )
            if not options["check"]:
                affected_rows = objs_to_fix.update(enabled_sections=0)
            else:
                affected_rows = objs_to_fix.count()

            self.stdout.write(f"{model_class.__name__} {flag_name}: {affected_rows}")

        if options["check"]:
            self.stdout.write(self.style.WARNING("No changes made"))
        else:
            self.stdout.write(self.style.SUCCESS("DONE!"))
