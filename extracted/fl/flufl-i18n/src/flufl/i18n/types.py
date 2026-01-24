from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal, TYPE_CHECKING

from public import public

if TYPE_CHECKING:  # pragma: no cover
    from gettext import NullTranslations
    from types import TracebackType


@public
class TranslationContextManager(ABC):
    """Context manager for translations in a particular language."""

    @abstractmethod
    def __enter__(self) -> TranslationContextManager:
        pass  # pragma: nocover

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        pass  # pragma nocover


@public
class RuntimeTranslator(ABC):
    """Abstract class representing the interface for the _() function."""

    @abstractmethod
    def __call__(self, original: str, extras: dict[str, str] | None = None) -> str:
        """Translate the string into the language of the current context.

        This is the primary method for the runtime behavior or translating a
        source string.

        :param original: The original string to translate.
        :param extras: Extra substitution mapping, elements of which override
            the locals and globals.
        :return: The translated string.
        """

    @abstractmethod
    def using(self, language_code: str) -> TranslationContextManager:
        """Create a context manager for temporary translation.

        While in this context manager, translations use the given language
        code.  When the with statement exits, the original language is
        restored.  These are nestable.

        :param language_code: The language code for the translation context.
        :return: The new translation context.
        """

    @abstractmethod
    def defer_translation(self) -> TranslationContextManager:
        """Push a NullTranslations onto the stack.

        This is useful for when you want to mark strings statically for
        extraction but you want to defer translation of the string until
        later.

        :return: The NULLTranslations context.
        """

    @abstractmethod
    def push(self, language_code: str) -> None:
        """Push a new catalog onto the stack.

        The translation catalog associated with the language code now becomes
        the currently active translation context.

        :param language_code: The language code for the translation context.
        """

    @abstractmethod
    def pop(self) -> None:
        """Pop the current catalog off the translation stack.

        No exception is raised for under-runs.  In that case, pop() just
        no-ops and the null translation becomes the current translation
        context.
        """

    @property
    @abstractmethod
    def default(self) -> str | None:
        """Return the default language code.

        :return: The default language code, or None if there is no default
            language.
        """

    @default.setter
    @abstractmethod
    def default(self, language_code: str) -> None:
        """Set the default language code.

        :param language_code: The language code for the default translation
            context.
        """

    @default.deleter
    @abstractmethod
    def default(self) -> None:
        """Reset the default language to the null translator."""

    @property
    @abstractmethod
    def code(self) -> str | None:
        """The language code currently in effect, if there is one."""


@public
class TranslationStrategy(ABC):
    """Abstract class representing the interface for translation strategies."""

    @abstractmethod
    def __call__(self, language_code: str | None = None) -> NullTranslations:
        """Find the catalog for the language.

        :param language_code: The language code to find.  If None, then the
            default gettext language code lookup scheme is used.
        :return: A `gettext` catalog.
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """The application's name."""
