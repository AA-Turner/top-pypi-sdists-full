# -*- coding: utf-8 -*-
from cleo.helpers import option

from .base_command import BaseCommand


class RefreshCommand(BaseCommand):
    name = 'migrate refresh'
    description = 'Reset and re-run all migrations.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['migrate:refresh']

    options = [
        option(
            long_name='database',
            short_name='d',
            description='The database connection to use.',
            flag=False,
            value_required=False,
        ),
        option(
            long_name='path',
            short_name='p',
            description='The path of migrations files to be executed.',
            flag=False,
            value_required=False,
        ),
        option(
            long_name='seed',
            short_name='s',
            description='Indicates if the seed task should be re-run.',
            flag=True,
            value_required=False,
        ),
        option(
            long_name='seed-path',
            short_name='sp',
            description='The path of seeds files to be executed.'
                        'Defaults to <comment>./seeders</comment>.',
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
            "<question>Are you sure you want to refresh the database?:</question> "
        ):
            return

        database = self.option("database")

        options = ' --force'

        if self.option("path"):
            options += f' --path {self.option("path")}'

        if database:
            options += f' --database {database}'

        if self._definition.has_option("config"):
            options += f' --config {self.option("config")}'

        self.call("migrate:reset", options)

        self.call("migrate", options)

        if self._needs_seeding():
            self._run_seeder(database)

    def _needs_seeding(self):
        return self.option("seed")

    def _run_seeder(self, database):
        options = f' --seeder {self.option("seeder")} --force'

        if database:
            options += f' --database {database}'

        if self._definition.has_option("config"):
            options += f' --config {self.option("config")}'

        if self.option("seed-path"):
            options += f' --path {self.option("seed-path")}'

        self.call("db:seed", options)
