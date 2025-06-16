# -*- coding: utf-8 -*-
from cleo.helpers import option

from orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class MigrateCommand(BaseCommand):
    name = 'migrate'
    description = 'Run the database migrations.'

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
            description='The path of migrations files to be executed.',
            flag=False,
            value_required=False
        ),
        option(
            long_name='seed',
            short_name='s',
            description='Indicates if the seed task should be re-run.',
            flag=True,
            value_required=False
        ),
        option(
            long_name='seed-path',
            short_name='sp',
            description='The path of seeds files to be executed.'
                        'Defaults to <comment>./seeders</comment>.',
            flag=False,
            value_required=False
        ),
        option(
            long_name='pretend',
            short_name='P',
            description='Dump the SQL queries that would be run.',
            flag=True,
            value_required=False
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
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to proceed with the migration?</question> "
        ):
            return

        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        migrator = Migrator(repository, self.resolver)

        self._prepare_database(migrator, database)

        pretend = self.option("pretend")

        path = self.option("path")

        if path is None:
            path = self._get_migration_path()

        migrator.run(path, pretend)

        for note in migrator.get_notes():
            self.line(note)

        # If the "seed" option has been given, we will rerun the database seed task
        # to repopulate the database.
        if self.option("seed"):
            options = ''
            if self.option('force'):
                options += f' --force {self.option("force")}'

            if database:
                options += f' --database {database}'

            if self._definition.has_option("config") and self.option('config'):
                options += f' --config {self.option("config")}'

            if self.option("seed-path"):
                options += f' --path {self.option("seed-path")}'

            self.call("db:seed", options)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)

        if not migrator.repository_exists():
            options = ''

            if database:
                options += f' --database {database}'

            if self._definition.has_option("config") and self.option('config'):
                options += f' --config {self.option("config")}'

            self.call("migrate:install", options)
