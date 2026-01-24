from public import public

from flufl.i18n._application import Application
from flufl.i18n.types import TranslationStrategy


@public
class Registry:
    """A registry of application translation lookup strategies."""

    def __init__(self) -> None:
        # Map application names to Application instances.
        self._registry: dict[str, Application] = {}

    def register(self, strategy: TranslationStrategy) -> Application:
        """Add an association between an application and a lookup strategy.

        :param strategy: An application translation lookup strategy.
        :type application: A callable object with a .name attribute
        :return: An application instance which can be used to access the
            language catalogs for the application.
        :rtype: `Application`
        """
        application = Application(strategy)
        self._registry[strategy.name] = application
        return application


registry: Registry  # For mypy.
public(registry=Registry())
