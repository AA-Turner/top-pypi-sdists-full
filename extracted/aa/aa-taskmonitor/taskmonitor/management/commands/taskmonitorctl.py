from collections import Counter
from enum import Enum

import humanize

from django.core.management.base import BaseCommand, CommandError

from taskmonitor import __title__, app_settings
from taskmonitor.core import cached_reports, celery_queues
from taskmonitor.models import TaskLog

CACHE_TIMEOUT_SECONDS = 3600


class Token(str, Enum):
    """Argument token."""

    COMMAND = "command"
    TARGET = "target"


class UserCommand(str, Enum):
    """Command for users."""

    PURGE = "purge"
    INSPECT = "inspect"


class Target(str, Enum):
    """Target of a command."""

    LOGS = "logs"
    QUEUE = "queue"
    SETTINGS = "settings"


def my_input(*args, **kwargs) -> str:
    """Helper to enable mocking of input for unit tests."""
    return input(*args, **kwargs)


class Command(BaseCommand):
    help = f"Command utility for {__title__}."

    def run_from_argv(self, *args, **kwargs) -> None:
        """Workaround to handle exceptions in missing sub commands more gracefully."""
        try:
            super().run_from_argv(*args, **kwargs)
        except CommandError as ex:
            token = __name__.split(".")
            try:
                name = token[-1:].pop()
            except IndexError:
                name = "?"
            print(f"manage.py {name}: {ex}")

    def add_arguments(self, parser) -> None:
        subparsers = parser.add_subparsers(
            dest=Token.COMMAND.value,
            required=True,
            title="commands",
            help="available commands",
        )
        # purge command
        parser_purge = subparsers.add_parser(
            UserCommand.PURGE.value, help="Purge a target"
        )
        parser_purge.add_argument(
            Token.TARGET.value,
            type=str,
            choices=[Target.QUEUE.value, Target.LOGS.value],
            help="target to purge",
        )
        purge_group = parser_purge.add_mutually_exclusive_group(required=True)
        purge_group.add_argument(
            "--all", action="store_true", help="You want to purge everything"
        )
        purge_group.add_argument(
            "--app-name", help="Limit purge to tasks from an specific app"
        )
        purge_group.add_argument(
            "--task-id", help="Limit purge to tasks with a specific ID"
        )
        purge_group.add_argument(
            "--task-name", help="Limit purge to tasks with a specific name"
        )

        # inspect command
        parser_inspect = subparsers.add_parser(
            UserCommand.INSPECT.value,
            help="Inspect a target, e.g. show information about it.",
        )
        parser_inspect.add_argument(
            Token.TARGET.value,
            type=str,
            choices=[Target.LOGS.value, Target.QUEUE.value, Target.SETTINGS.value],
            help="target to inspect",
        )
        parser_inspect.add_argument(
            "--force-calc",
            action="store_true",
            help="Fore re-calculation of values and update caches.",
        )

    def _user_confirmed(self, question_text):
        """Ask user about confirmation and exit
        when he does not reply in the affirmative.
        """
        user_input = my_input(f"{question_text} (y/N)?")
        if user_input.lower() != "y":
            self.stdout.write(self.style.WARNING("Aborted by user request."))
            exit(1)

    def _clear_line(self):
        self.stdout.write("" * 70, ending="\r")

    def purge_queue(self, options):
        num_entries = celery_queues.queue_length()
        if not num_entries:
            self.stdout.write(self.style.WARNING("Queue is empty. Aborted."))
            exit(1)
        self.stdout.write(f"Current queue size: {num_entries:,}")
        if options["task_name"]:
            task_name = options["task_name"]
            self._user_confirmed(
                f"Are you sure you purge all tasks with the TASK NAME {task_name} from the queue?"
            )
            self.stdout.write("Purged tasks from queue...", ending="\r")
            deleted_entries = celery_queues.delete_task_by_name(task_name)
            self._clear_line()
        elif options["task_id"]:
            task_id = options["task_id"]
            self._user_confirmed(
                f"Are you sure you purge all tasks with the TASK ID {task_id} from the queue?"
            )
            self.stdout.write("Purged tasks from queue...", ending="\r")
            deleted_entries = celery_queues.delete_task_by_id(task_id)
            self._clear_line()
        elif options["app_name"]:
            app_name = options["app_name"]
            self._user_confirmed(
                f"Are you sure you purge all tasks belonging to the app {app_name} from the queue?"
            )
            self.stdout.write("Purged tasks from queue...", ending="\r")
            deleted_entries = celery_queues.delete_task_by_app_name(app_name)
            self._clear_line()
        elif options["all"]:
            self._user_confirmed("Are you sure you purge ALL TASKS from the queue?")
            self.stdout.write("Purged tasks from queue...", ending="\r")
            celery_queues.clear_tasks()
            deleted_entries = num_entries
            self._clear_line()
        else:
            raise NotImplementedError("This option is not yet implemented")
        self.stdout.write(f"Purged {deleted_entries:,} tasks from queue...")
        self.stdout.write(self.style.SUCCESS("Done."))

    def purge_logs(self, options):
        all_logs = TaskLog.objects.all()
        self.stdout.write("Calculating...", ending="\r")
        num_logs = all_logs.count()
        if not num_logs:
            self.stdout.write(self.style.WARNING("No logs found. Aborted."))
            exit(1)
        self.stdout.write(f"Current task logs count: {num_logs:,}")
        if options["all"]:
            self._user_confirmed("Are you sure you purge ALL task logs?")
            self.stdout.write("Deleting task logs...")
            all_logs._raw_delete(all_logs.db)
        else:
            raise CommandError("Currently only the --all option is supported")
        cached_reports.refresh_cache()
        self.stdout.write(self.style.SUCCESS("Done."))

    def inspect_logs(self, options):
        log_count = TaskLog.objects.count()
        try:
            db_table_size = TaskLog.objects.db_table_size()
        except RuntimeError:
            table_size_str = "N/A"
            average_bytes_str = "N/A"
        else:
            table_size_str = humanize.naturalsize(db_table_size)
            average_bytes_str = (
                humanize.naturalsize(db_table_size / log_count) if log_count else "N/A"
            )
        output = {
            "Log count in DB": humanize.intword(log_count),
            "Table size in DB": table_size_str,
            "Average log size in DB": average_bytes_str,
        }
        max_length = max([len(o) for o in output.keys()])
        for label, value in output.items():
            self.stdout.write(f"{label:{max_length + 1}}: {value}")

    def inspect_queue(self, options):
        num_entries = celery_queues.queue_length()
        if not num_entries:
            self.stdout.write("Queue is empty.")
            return
        self.stdout.write(f"Current queue size: {num_entries:,}")
        if num_entries > app_settings.TASKMONITOR_QUEUED_TASKS_ADMIN_LIMIT:
            self._user_confirmed(
                "The queue is very large. Do you still want to gather statistics?"
            )
        self.stdout.write("Fetching data from queue...", ending="\r")
        self._clear_line()
        tasks = [
            (task.app_name, task.name)
            for task in celery_queues._fetch_task_from_all_queues()
        ]
        self.stdout.write("Queued tasks grouped by app counts in descending order:")
        grouped_names = (o[0] for o in tasks)
        self._render_field_counts(grouped_names)
        self.stdout.write("Queued tasks grouped by task counts in descending order:")
        grouped_names = (o[1] for o in tasks)
        self._render_field_counts(grouped_names)

    def _render_field_counts(self, grouped_names):
        field_counts = Counter(grouped_names)
        field_counts_sorted = dict(
            sorted(field_counts.items(), key=lambda item: item[1], reverse=True)
        )
        max_length = (
            max([len(o) for o in field_counts_sorted.keys()])
            if field_counts_sorted
            else 0
        )
        for app_name, count in field_counts_sorted.items():
            self.stdout.write(f"  {app_name:{max_length}}: {count:,}")

    def inspect_settings(self, options):
        settings = sorted(
            [o for o in dir(app_settings) if not o.startswith("__") and o == o.upper()]
        )
        max_length = max([len(o) for o in settings])
        for setting_name in settings:
            value = getattr(app_settings, setting_name)
            self.stdout.write(f"{setting_name:{max_length + 1}}: {value}")

    def handle(self, *args, **options):
        command = options[Token.COMMAND.value]
        target = options[Token.TARGET.value]

        method = f"{command}_{target}"
        try:
            getattr(self, method)(options)
        except AttributeError:
            raise NotImplementedError(method) from None
