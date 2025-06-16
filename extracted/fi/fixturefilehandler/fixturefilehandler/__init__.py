"""This module implements fixture file handler."""
from typing import List

from fixturefilehandler.exceptions import *  # noqa
from fixturefilehandler.factories import *  # noqa
from fixturefilehandler.file_paths import *  # noqa
from fixturefilehandler.fixture_file_handler import *  # noqa

__version__ = "1.4.0"

__all__: List[str] = []
# pylint: disable=undefined-variable
__all__ += exceptions.__all__  # type: ignore # noqa
__all__ += factories.__all__  # type: ignore # noqa
__all__ += file_paths.__all__  # type: ignore # noqa
__all__ += fixture_file_handler.__all__  # type: ignore # noqa
