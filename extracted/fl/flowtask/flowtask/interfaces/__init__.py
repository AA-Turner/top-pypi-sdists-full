"""
Interfaces.

Services and methods covered by Flowtask.
Support interfaces for many options on Task Components.

Heavy modules (LLMClient, DBSupport, SeleniumService, etc.) are
lazy-loaded via __getattr__ to avoid importing their transitive
dependencies (parrot, google-cloud-bigquery, selenium, etc.) at
startup time.
"""
from .func import FuncSupport
from .mask import MaskSupport
from .log import LogSupport, SkipErrors
from .result import ResultSupport
from .cache import CacheSupport
from .stat import StatSupport
from .locale import LocaleSupport
from .template import TemplateSupport

# Lazy-loaded modules and their import paths.
_LAZY_IMPORTS = {
    "DBSupport": (".databases", "DBSupport"),
    "HTTPService": (".http", "HTTPService"),
    "SeleniumService": (".selenium_service", "SeleniumService"),
    "ClientInterface": (".client", "ClientInterface"),
    "DBInterface": (".db", "DBInterface"),
    "ParrotTool": (".ParrotTool", "ParrotTool"),
    "LLMClient": (".LLMClient", "LLMClient"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path, package=__name__)
        value = getattr(module, attr_name)
        # Cache in module namespace so __getattr__ is not called again.
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    "FuncSupport",
    "MaskSupport",
    "DBSupport",
    "LogSupport",
    "ResultSupport",
    "StatSupport",
    "LocaleSupport",
    "TemplateSupport",
    "SkipErrors",
    # interfaces:
    "DBInterface",
    "ClientInterface",
    "HTTPService",
    "ParrotTool",
    "LLMClient",
)
