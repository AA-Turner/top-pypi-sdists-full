# -*- coding: utf-8 -*-
from cleo.helpers import option

from orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class StatusCommand(BaseCommand):
    name = 'migrate status'
    description = 'Show a list of migrations up/down.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['migrate:status']

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
    ]

    def handle(self):
        """
        Executes the command.
        """
        database = self.option("database")

        self.resolver.set_default_connection(database)

        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        migrator = Migrator(repository, self.resolver)

        if not migrator.repository_exists():
            return self.error("No migrations found")

        self._prepare_database(migrator, database)

        path = self.option("path")

        if path is None:
            path = self._get_migration_path()

        ran = migrator.get_repository().get_ran()

        migrations = []
        for migration in migrator._get_migration_files(path):
            if migration in ran:
                migrations.append(["<fg=cyan>%s</>" % migration, "<info>Yes</>"])
            else:
                migrations.append(["<fg=cyan>%s</>" % migration, "<fg=red>No</>"])

        if migrations:
            table = self.table(["Migration", "Ran?"], migrations)
            table.render()
        else:
            return self.error("No migrations found")

        for note in migrator.get_notes():
            self.line(note)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)
