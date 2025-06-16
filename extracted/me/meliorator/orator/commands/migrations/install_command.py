# -*- coding: utf-8 -*-
from cleo.helpers import option

from orator.migrations import DatabaseMigrationRepository
from .base_command import BaseCommand


class InstallCommand(BaseCommand):
    name = 'migrate install'
    description = 'Create the migration repository.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['migrate:install']

    options = [
        option(
            long_name='database',
            short_name='d',
            description='The database connection to use.',
            flag=False,
            value_required=True,
        )
    ]

    def handle(self):
        """
        Executes the command
        """
        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        repository.set_source(database)
        repository.create_repository()

        self.info("Migration table created successfully")
