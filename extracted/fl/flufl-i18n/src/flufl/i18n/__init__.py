"""A high level API for internationalizing Python libraries and applications.

initialize() is all a simple application needs: it registers a SimpleStrategy for the given
domain and returns the translation function, conventionally bound to _().  Anything more
elaborate starts from the registry, which hands out an Application per strategy.  Everything
public is re-exported here, so flufl.i18n is the only import path any consumer needs.
"""

from flufl.i18n._application import Application
from flufl.i18n._expand import expand
from flufl.i18n._registry import registry
from flufl.i18n._strategy import PackageStrategy, SimpleStrategy
from flufl.i18n._types import (
    RuntimeTranslator,
    TranslationContextManager,
    TranslationStrategy,
)


__version__ = '7.0.0'


# Most of these names are re-exports, and a type checker has no way to tell a re-export from an
# implementation detail that merely happens to be imported.  mypy under --strict, and pyright in
# its default mode, reject `from flufl.i18n import Application` for an installed package unless the
# intent is stated, and this list states it.  (pyrefly and ty accept it either way.)
#
# A literal list is what makes that work, which is why this module doesn't use @public: the
# decorator builds __all__ at runtime, where no type checker can see it.  The list is kept honest in
# both directions: ruff's F401 flags an import missing from it, and tests/test_init.py a name in it
# that nothing defines.  (ruff's F822 would catch the latter too, but outside preview it skips
# __init__.py, where an undefined name might be a submodule.)
__all__ = [
    'Application',
    'PackageStrategy',
    'RuntimeTranslator',
    'SimpleStrategy',
    'TranslationContextManager',
    'TranslationStrategy',
    'expand',
    'initialize',
    'registry',
]


def initialize(domain: str) -> RuntimeTranslator:
    """Initialize a translation context.

    :param domain: The application's name.
    :return: The translation function, typically bound to _()
    """
    strategy = SimpleStrategy(domain)
    application = registry.register(strategy)
    return application._
