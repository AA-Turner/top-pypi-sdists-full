# -*- coding: utf-8 -*-
from cleo.helpers import option

from orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class RollbackCommand(BaseCommand):
    name = 'migrate rollback'
    description = 'Rollback the last database migration operation.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['migrate:rollback']

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
            "<question>Are you sure you want to rollback the last migration?:</question> "
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

        migrator.rollback(path, pretend)

        for note in migrator.get_notes():
            self.line(note)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)
