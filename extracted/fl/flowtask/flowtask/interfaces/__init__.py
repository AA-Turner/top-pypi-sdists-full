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

# FEAT-023: Interface base classes relocated from flowtask/components/.
# Canonical homes are now flowtask/interfaces/<module_name>.py.
#
# Eager imports (lightweight, no heavy optional deps):
from .abstract import AbstractFlow
from .flow import FlowComponent
from .user import UserComponent
from .group import GroupComponent
from .base_action import BaseAction
from .base_loop import BaseLoop
from .download_from import DownloadFromBase
from .upload_to import UploadToBase
from .file_base import FileBase
from .copy_to import CopyTo
from .copy_from_base import CopyFromBase
from .copy_to_file_base import CopyToFileBase
from .t_pandas import tPandas
#
# Heavy-dep interface bases (lazy-loaded to avoid pulling in optional deps
# like google-cloud-*, sqlalchemy, azure-* at startup):
#   GoogleBase → flowtask.interfaces.google_base
#   DbClient   → flowtask.interfaces.db_client
#   TableBase  → flowtask.interfaces.table_base
#   QSBase     → flowtask.interfaces.qs_base
#   Azure      → flowtask.interfaces.azure_component

# Lazy-loaded modules and their import paths.
_LAZY_IMPORTS = {
    "DBSupport": (".databases", "DBSupport"),
    "HTTPService": (".http", "HTTPService"),
    "SeleniumService": (".selenium_service", "SeleniumService"),
    "ClientInterface": (".client", "ClientInterface"),
    "DBInterface": (".db", "DBInterface"),
    "ParrotTool": (".ParrotTool", "ParrotTool"),
    "LLMClient": (".LLMClient", "LLMClient"),
    # FEAT-023: heavy-dep interface bases (lazy-loaded):
    "GoogleBase": (".google_base", "GoogleBase"),
    "DbClient": (".db_client", "DbClient"),
    "TableBase": (".table_base", "TableBase"),
    "QSBase": (".qs_base", "QSBase"),
    "Azure": (".azure_component", "Azure"),
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
    # Support mixins (lightweight, always eager):
    "FuncSupport",
    "MaskSupport",
    "LogSupport",
    "SkipErrors",
    "ResultSupport",
    "StatSupport",
    "LocaleSupport",
    "TemplateSupport",
    "CacheSupport",
    # Service interfaces (lazy-loaded):
    "DBSupport",
    "DBInterface",
    "ClientInterface",
    "HTTPService",
    "SeleniumService",
    "ParrotTool",
    "LLMClient",
    # FEAT-023: Interface base classes (eager, lightweight):
    "AbstractFlow",
    "FlowComponent",
    "UserComponent",
    "GroupComponent",
    "BaseAction",
    "BaseLoop",
    "DownloadFromBase",
    "UploadToBase",
    "FileBase",
    "CopyTo",
    "CopyFromBase",
    "CopyToFileBase",
    "tPandas",
    # FEAT-023: Interface base classes (lazy, heavy-dep):
    "GoogleBase",
    "DbClient",
    "TableBase",
    "QSBase",
    "Azure",
)
