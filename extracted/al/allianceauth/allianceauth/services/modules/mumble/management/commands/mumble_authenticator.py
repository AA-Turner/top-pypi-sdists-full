__lazy_modules__ = ["argparse"]

from typing import TYPE_CHECKING

from allianceauth.services.modules.mumble import authenticator

from django.core.management.base import BaseCommand

if TYPE_CHECKING:
    from argparse import ArgumentParser


class Command(BaseCommand):
    help = 'Run the Mumble Authenticator'

    def add_arguments(self, parser: "ArgumentParser") -> None:
        parser.add_argument(
            '--server_id', action='store', default=1,
            help='Run the Mumble Authenticator for the given Server Configuration ID')

    def handle(self, *args, **options) -> None:
        authenticator.main()
