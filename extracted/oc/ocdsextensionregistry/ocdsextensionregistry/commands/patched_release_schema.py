import json
import re
import sys

import requests

from ocdsextensionregistry.commands.base import BaseCommand
from ocdsextensionregistry.exceptions import CommandError
from ocdsextensionregistry.profile_builder import ProfileBuilder
from ocdsextensionregistry.util import json_dump


class Command(BaseCommand):
    name = "patched-release-schema"
    help = "Create a patched release schema from the extensions array of a release package or record package."

    def add_arguments(self):
        self.add_argument("file", help="a release package or record package")
        self.add_argument("--tag", help="the OCDS version whose release schema to extend, like 1__1__5")

    def handle(self):
        # Copy of ocdsmerge.util.get_tags().
        response = requests.get("https://standard.open-contracting.org/schema/", timeout=10)
        response.raise_for_status()
        tags = re.findall(r'"(\d+__\d+__\d+)/', response.text)

        tag = self.args.tag
        if tag is None:
            tag = tags[-1]
        elif tag not in tags:
            raise CommandError(
                f"Error: Invalid value for '--tag': '{tag}' is not one of {', '.join(map(repr, tags))}."
            )

        with open(self.args.file) as f:
            json_dump(ProfileBuilder(tag, json.load(f).get("extensions", [])).patched_release_schema(), sys.stdout)
