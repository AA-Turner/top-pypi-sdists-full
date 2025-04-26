import abc
from argparse import ArgumentParser, _SubParsersAction
from typing import List, Optional

from ..arguments import Arguments


class ArgumentRegistrar(abc.ABC):
    @abc.abstractmethod
    def register(self, parser: ArgumentParser) -> None:
        ...


class CommandRegistrar:
    arguments: List[ArgumentRegistrar]
    subcommands: List["CommandRegistrar"]

    def __init__(
        self,
        arguments: List[ArgumentRegistrar],
        subcommands: Optional[List["CommandRegistrar"]] = None,
    ) -> None:
        self.arguments = arguments
        self.subcommands = subcommands if subcommands is not None else []

    def register(
        self, subparsers: Optional[_SubParsersAction] = None
    ) -> Optional[ArgumentParser]:
        parser = self._create_parser(subparsers)
        if parser is not None:
            for argument in self.arguments:
                argument.register(parser)

        if len(self.subcommands) > 0:
            subparsers = self._create_subparsers(parser)
            if subparsers is not None:
                for subcommand in self.subcommands:
                    subcommand.register(subparsers)

        return parser

    async def execute(self, args: Arguments) -> bool:
        if self._can_execute_impl(args):
            await self._before_execute(args)
            await self._execute_impl(args)
            return True

        for subcommand in self.subcommands:
            if await subcommand.execute(args):
                return True
        return False

    def _create_parser(
        self, subparsers: Optional[_SubParsersAction]
    ) -> Optional[ArgumentParser]:
        pass

    def _create_subparsers(
        self, parser: Optional[ArgumentParser]
    ) -> Optional[_SubParsersAction]:
        pass

    def _can_execute_impl(self, args: Arguments) -> bool:
        return False

    async def _execute_impl(self, args: Arguments) -> None:
        pass

    async def _before_execute(self, args: Arguments) -> None:
        pass
