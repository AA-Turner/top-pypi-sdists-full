from __future__ import annotations

import functools
from pathlib import Path
from typing import Callable, List, Union

from chalk.gitignore.gitignore_parser import parse_gitignore
from chalk.utils.paths import search_recursively_for_file


class IgnoreConfig:
    """
    A class that represents an ignore configuration.
    Can also represent a combined ignore configuration,
    i.e. a combination of a .gitignore and a .chalkignore file.
    """

    def __init__(self, ignored: Callable[[Union[Path, str]], bool], has_negation: bool):
        super().__init__()
        self.ignored = ignored
        self.has_negation = has_negation


def is_ignored(path: Path | str, ignore_functions: List[Callable[[Union[Path, str]], bool]]) -> bool:
    return any((ignored(path) for ignored in ignore_functions))


def get_default_combined_ignore_config(resolved_root: Path) -> IgnoreConfig:
    ignore_functions: List[Callable[[Path | str], bool]] = []

    gitignores_and_has_negations = (
        parse_gitignore(str(x)) for x in search_recursively_for_file(resolved_root, ".gitignore")
    )
    gitignores = (x[0] for x in gitignores_and_has_negations)
    ignore_functions.extend(gitignores)

    chalkignores_and_has_negations = (
        parse_gitignore(str(x)) for x in search_recursively_for_file(resolved_root, ".chalkignore")
    )
    chalkignores = (x[0] for x in chalkignores_and_has_negations)
    ignore_functions.extend(chalkignores)

    gitignore_negation = any(x[1] for x in gitignores_and_has_negations)
    chalkignore_negation = any(x[1] for x in chalkignores_and_has_negations)
    has_negation = gitignore_negation or chalkignore_negation

    return IgnoreConfig(
        ignored=functools.partial(is_ignored, ignore_functions=ignore_functions), has_negation=has_negation
    )
