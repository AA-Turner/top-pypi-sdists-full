from __future__ import annotations

import os
import gettext

from typing import TYPE_CHECKING

from public import public

from flufl.i18n.types import TranslationStrategy

if TYPE_CHECKING:  # pragma: no cover
    from types import ModuleType


class _BaseStrategy(TranslationStrategy):
    """Common code for strategies."""

    def __init__(self, name: str):
        """Create a catalog lookup strategy.

        :param name: The application's name.
        """
        self._name = name
        self._messages_dir: str

    def __call__(self, language_code: str | None = None) -> gettext.NullTranslations:
        """Find the catalog for the language.

        :param language_code: The language code to find.  If None, then the
            default gettext language code lookup scheme is used.
        :return: A `gettext` catalog.
        """
        # gettext.translation() requires None or a sequence.
        languages = None if language_code is None else [language_code]
        try:
            return gettext.translation(self.name, self._messages_dir, languages)
        except OSError:
            # Fall back to untranslated source language.
            return gettext.NullTranslations()

    @property
    def name(self) -> str:
        """The application's name."""
        return self._name


@public
class PackageStrategy(_BaseStrategy):
    """A strategy that finds catalogs based on package paths."""

    def __init__(self, name: str, package: ModuleType):
        """Create a catalog lookup strategy.

        :param name: The application's name.
        :param package: The package path to the message catalogs.  This
            strategy uses the __file__ (which must exist and be a string)
            of the package path as the directory containing `gettext` messages.
        """
        super().__init__(name)
        if hasattr(package, '__file__') and isinstance(package.__file__, str):
            self._messages_dir = os.path.dirname(package.__file__)
        else:
            raise ValueError('Argument `package` must have a string `__file__`')


@public
class SimpleStrategy(_BaseStrategy):
    """A simpler strategy for getting translations."""

    def __init__(self, name: str):
        """Create a catalog lookup strategy.

        :param name: The application's name.
        """
        super().__init__(name)
        self._messages_dir = os.environ.get('LOCPATH', '')
