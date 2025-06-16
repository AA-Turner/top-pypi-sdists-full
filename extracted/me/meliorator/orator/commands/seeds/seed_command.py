# -*- coding: utf-8 -*-

import importlib
import inflection
import os

from cleo.helpers import option

from .base_command import BaseCommand
from ...utils import load_module


class SeedCommand(BaseCommand):
    name = 'db seed'
    description = 'Seed the database with records.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['db:seed']

    options = [
        option(
            long_name='database',
            short_name='d',
            description='The database connection to use.',
            flag=False,
            value_required=False
        ),
        option(
            long_name='path',
            short_name='p',
            description='The path to seeders files.\n'
                        'Defaults to <comment>./seeds</comment>.',
            flag=False,
            value_required=False,
        ),
        option(
            long_name='seeder',
            short_name='ds',
            description='The name of the root seeder.',
            flag=False,
            value_required=False,
            default='database_seeder',
        ),
        option(
            long_name='force',
            short_name='f',
            description='Force the operation to run.',
            flag=True,
            value_required=False
        ),
    ]

    def handle(self):
        """
        Executes the command.
        """
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to seed the database?:</question> "
        ):
            return

        self.resolver.set_default_connection(self.option("database"))

        self._get_seeder().run()

        self.info("Database seeded!")

    def _get_seeder(self):
        name = self._parse_name(self.option("seeder"))
        seeder_file = self._get_path(name)

        # Loading parent module
        load_module("seeds", self._get_path("__init__"))

        # Loading module
        mod = load_module("seeds.%s" % name, seeder_file)

        klass = getattr(mod, inflection.camelize(name))

        instance = klass()
        instance.set_command(self)
        instance.set_connection_resolver(self.resolver)

        return instance

    def _parse_name(self, name):
        if name.endswith(".py"):
            name = name.replace(".py", "", -1)

        return name

    def _get_path(self, name):
        """
        Get the destination class path.

        :param name: The name
        :type name: str

        :rtype: str
        """
        path = self.option("path")
        if path is None:
            path = self._get_seeders_path()

        return os.path.join(path, "%s.py" % name)
