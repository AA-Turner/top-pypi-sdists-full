from __future__ import annotations

from gettext import NullTranslations
from typing import Literal, NamedTuple, TYPE_CHECKING

from public import public

from flufl.i18n._translator import Translator
from flufl.i18n.types import (
    RuntimeTranslator,
    TranslationContextManager,
    TranslationStrategy,
)

# fmt: off
if TYPE_CHECKING:                       # pragma: no cover
    from types import TracebackType     # noqa: I001 Import block is un-sorted or un-formatted
# fmt: on


class _Using(TranslationContextManager):
    """Context manager for _.using()."""

    def __init__(self, application: Application, language_code: str):
        self._application = application
        self._language_code = language_code

    def __enter__(self) -> TranslationContextManager:
        self._application.push(self._language_code)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self._application.pop()
        # Do not suppress exceptions.
        return False


class _Defer(TranslationContextManager):
    """Context manager for _.defer_translation()."""

    # 2020-07-06(warsaw): Once Python 3.7 is the minimum supported version, we
    # can use `from __future__ import annotations` instead of the string type.
    def __init__(self, application: Application):
        self._application = application

    def __enter__(self) -> TranslationContextManager:
        self._application.defer()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self._application.pop()
        # Do not suppress exceptions.
        return False


class _Underscore(RuntimeTranslator):
    """The implementation of the _() function.

    This class is internal representation only and has an incestuous
    relationship with the Application class.
    """

    # 2020-07-06(warsaw): Once Python 3.7 is the minimum supported version, we
    # can use `from __future__ import annotations` instead of the string type.
    def __init__(self, application: Application):
        self._application = application

    def __call__(self, original: str, extras: dict[str, str] | None = None) -> str:
        """Translate the string into the language of the current context.

        :param original: The original string to translate.
        :param extras: Extra substitution mapping, elements of which override
            the locals and globals.
        :return: The translated string.
        """
        return self._application.current.translate(original, extras)

    def using(self, language_code: str) -> TranslationContextManager:
        """Create a context manager for temporary translation.

        While in this context manager, translations use the given language
        code.  When the with statement exits, the original language is
        restored.  These are nestable.

        :param language_code: The language code for the translation context.
        :return: The new translation context manager.
        """
        return _Using(self._application, language_code)

    def defer_translation(self) -> TranslationContextManager:
        """Push a NullTranslations onto the stack.

        This is useful for when you want to mark strings statically for
        extraction but you want to defer translation of the string until
        later.

        :return: The NULLTranslations context.
        """
        return _Defer(self._application)

    def push(self, language_code: str) -> None:
        """Push a new catalog onto the stack.

        The translation catalog associated with the language code now becomes
        the currently active translation context.

        :param language_code: The language code for the translation context.
        """
        self._application.push(language_code)

    def pop(self) -> None:
        """Pop the current catalog off the translation stack.

        No exception is raised for under-runs.  In that case, pop() just
        no-ops and the null translation becomes the current translation
        context.
        """
        self._application.pop()

    @property
    def default(self) -> str | None:
        """Return the default language code.

        :return: The default language code, or None if there is no default
            language.
        """
        return self._application.default

    @default.setter
    def default(self, language_code: str) -> None:
        """Set the default language code.

        :param language_code: The language code for the default translation
            context.
        """
        self._application.default = language_code

    @default.deleter
    def default(self) -> None:
        """Reset the default language to the null translator."""
        del self._application.default

    @property
    def code(self) -> str | None:
        """The language code currently in effect, if there is one."""
        code = self._application.code
        return self.default if code is None else code


class _StackItem(NamedTuple):
    code: str
    translator: Translator


@public
class Application:
    """Manage all the catalogs for a particular application.

    You can ask the application for a specific catalog based on the language
    code.  The Application requires a strategy for finding catalog files.

    Attributes:

    * dedent (default True) - controls whether translated strings are dedented
      or not.  This is passed through to the underlying `Translator`
      instance.
    * depth (default 2) - The number of stack frames to call sys._getframe()
      with in the underlying `Translator` instance.  Passed through to that
      class's constructor.
    """

    def __init__(self, strategy: TranslationStrategy):
        """Create an `Application`.

        Use the `dedent` attribute on this instance to control whether
        translated strings are dedented or not.  This is passed straight
        through to the `Translator` instance created in the _() method.

        :param strategy: A callable that can find catalog files for the
            application based on the language code.
        """
        self._strategy = strategy
        # A mapping from language codes to catalogs.
        self._catalogs: dict[str, NullTranslations] = {}
        self._stack: list[_StackItem] = []
        # Arguments to the Translator constructor.
        self.dedent = True
        self.depth = 2
        # By default, the baseline translator is the null translator.  Use our
        # public API so that we share code.
        self._default_language: str | None
        self._default_translator: Translator
        # This sets _default_language and _default_translator.
        del self.default

    @property
    def name(self) -> str:
        """The application name.

        :return: The application name.
        """
        return self._strategy.name

    @property
    def default(self) -> str | None:
        """The default language code, if there is one.

        :return: The default language code or None.
        """
        return self._default_language

    @default.setter
    def default(self, language_code: str) -> None:
        """Set the default language code.

        :param language_code: The language code for the default translator.
        """
        self._default_language = language_code
        catalog = self.get(language_code)
        self._default_translator = Translator(catalog, self.dedent, self.depth)

    @default.deleter
    def default(self) -> None:
        """Reset the default language to the null translator."""
        self._default_language = None
        self._default_translator = Translator(self._strategy(), self.dedent, self.depth)

    def get(self, language_code: str) -> NullTranslations:
        """Get the catalog associated with the language code.

        :param language_code: The language code.
        :return: A `gettext` catalog.
        """
        try:
            return self._catalogs[language_code]
        except KeyError:
            catalog = self._strategy(language_code)
            self._catalogs[language_code] = catalog
            return catalog

    @property
    def _(self) -> RuntimeTranslator:
        """Return a translator object, tied to the current catalog.

        :return: A translator context object for the current active catalog.
        """
        return _Underscore(self)

    def defer(self) -> None:
        """Push a deferred (i.e. null) translation context onto the stack.

        This is primarily used to support the ``_.defer_translation()``
        context manager.
        """
        self._stack.append(_StackItem('', Translator(NullTranslations(), self.dedent, self.depth)))

    def push(self, language_code: str) -> None:
        """Push a new catalog onto the stack.

        The translation catalog associated with the language code now becomes
        the currently active translation context.

        :param language_code: The language code for the translation context.
        """
        catalog = self.get(language_code)
        translator = Translator(catalog, self.dedent, self.depth)
        self._stack.append(_StackItem(language_code, translator))

    def pop(self) -> None:
        """Pop the current catalog off the translation stack.

        No exception is raised for under-runs.  In that case, pop() just
        no-ops and the null translation becomes the current translation
        context.
        """
        if len(self._stack) > 0:
            self._stack.pop()

    @property
    def current(self) -> Translator:
        """Return the current translator.

        :return: The current translator.
        """
        if len(self._stack) == 0:
            return self._default_translator
        return self._stack[-1].translator

    @property
    def code(self) -> str | None:
        """Return the current language code.

        :return: The current language code, or None if there isn't one.
        """
        if len(self._stack) == 0:
            return None
        return self._stack[-1].code
