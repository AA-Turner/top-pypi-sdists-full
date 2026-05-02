import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = "Remove django_migrations table entries that no longer have a corresponding file"

    def add_arguments(self, parser):
        parser.add_argument(
            "app",
            type=str,
            help="App label (e.g. notifications) or full module path (e.g. wbcore.contrib.notifications)",
        )
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        app_config = self._resolve_app(options["app"])
        dry_run = options["dry_run"]

        db_label = app_config.label
        on_disk = self._get_migration_files(app_config)

        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM django_migrations WHERE app = %s", [db_label])
            recorded = {row[0] for row in cursor.fetchall()}

        stale = recorded - on_disk

        if not stale:
            self.stdout.write(f"[{db_label}] No stale migrations found.")
            return

        self.stdout.write(f"[{db_label}] Stale migrations to remove ({len(stale)}):")
        for name in sorted(stale):
            self.stdout.write(f"  - {name}")

        if dry_run:
            self.stdout.write("Dry run — nothing deleted.")
            return

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = %s AND name = ANY(%s)",
                [db_label, list(stale)],
            )
        self.stdout.write(self.style.SUCCESS(f"Deleted {len(stale)} stale record(s)."))

    def _resolve_app(self, identifier: str):
        # Try short label first, then fall back to matching by full module name
        try:
            return apps.get_app_config(identifier)
        except LookupError:
            pass
        matches = [cfg for cfg in apps.get_app_configs() if cfg.name == identifier]
        if not matches:
            raise CommandError(f"No app found for '{identifier}'.")
        return matches[0]

    def _get_migration_files(self, app_config) -> set[str]:
        migrations_dir = os.path.join(app_config.path, "migrations")
        if not os.path.isdir(migrations_dir):
            raise CommandError(f"No migrations directory found for '{app_config.label}'.")
        return {f[:-3] for f in os.listdir(migrations_dir) if f.endswith(".py") and not f.startswith("_")}
