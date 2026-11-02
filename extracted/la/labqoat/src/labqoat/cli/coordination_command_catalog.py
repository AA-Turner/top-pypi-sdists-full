"""The dict and queue command groups."""

import click

from labqoat.cli.commands.coordination.dict_clear_command import DictClearCommand
from labqoat.cli.commands.coordination.dict_delete_command import DictDeleteCommand
from labqoat.cli.commands.coordination.dict_get_command import DictGetCommand
from labqoat.cli.commands.coordination.dict_put_command import DictPutCommand
from labqoat.cli.commands.coordination.queue_clear_command import QueueClearCommand
from labqoat.cli.commands.coordination.queue_get_command import QueueGetCommand
from labqoat.cli.commands.coordination.queue_len_command import QueueLenCommand
from labqoat.cli.commands.coordination.queue_put_command import QueuePutCommand
from labqoat.cli.commands.coordination.store_list_command import StoreListCommand
from labqoat.cli.core_command_catalog import CoreCommandCatalog


class CoordinationCommandCatalog:
    """Assemble the commands that read and change the selected project's dicts and queues."""

    @staticmethod
    def add(root: click.Group) -> None:
        """Register both groups without network or file access."""
        root.add_command(CoordinationCommandCatalog.dicts())
        root.add_command(CoordinationCommandCatalog.queues())

    @staticmethod
    def dicts() -> click.Group:
        """Text keys and JSON or bytes values the project's runs share."""
        group = CoreCommandCatalog.group(
            "dict",
            "Read and change the project's dicts: shared key-value state of its runs, such as a stop flag or the "
            "current policy version. Runs use context.dict(name).",
        )
        for command in (StoreListCommand("dict"), DictGetCommand(), DictPutCommand(), DictDeleteCommand()):
            group.add_command(command)
        group.add_command(DictClearCommand())
        return group

    @staticmethod
    def queues() -> click.Group:
        """First in, first out values the project's runs hand each other."""
        group = CoreCommandCatalog.group(
            "queue",
            "Read and change the project's queues: values handed between runs, each taken exactly once. "
            "Runs use context.queue(name).",
        )
        for command in (StoreListCommand("queue"), QueueLenCommand(), QueuePutCommand(), QueueGetCommand()):
            group.add_command(command)
        group.add_command(QueueClearCommand("clear"))
        group.add_command(QueueClearCommand("delete"))
        return group
