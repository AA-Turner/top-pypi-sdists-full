# -*- coding: utf-8 -*-
from cleo.helpers import option

from orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class ResetCommand(BaseCommand):
    name = 'migrate reset'
    description = 'Rollback all database migrations.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['migrate:reset']

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
            long_name='pretend',
            short_name='P',
            description='Dump the SQL queries that would be run.',
            flag=True,
            value_required=False,
        ),
        option(
            long_name='force',
            short_name='f',
            description='Force the operation to run.',
            flag=True,
            value_required=False,
        ),
    ]

    def handle(self):
        """
        Executes the command.
        """
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to reset all of the migrations?:</question> "
        ):
            return

        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        migrator = Migrator(repository, self.resolver)

        self._prepare_database(migrator, database)

        pretend = bool(self.option("pretend"))

        path = self.option("path")

        if path is None:
            path = self._get_migration_path()

        migrator.reset(path, pretend)

        for note in migrator.get_notes():
            self.line(note)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)
