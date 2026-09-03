######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39                                                                                #
# Generated on 2026-09-02T21:19:46.720209                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.packaging_sys

from ..exception import MetaflowException as MetaflowException
from ..packaging_sys import ContentType as ContentType
from ..packaging_sys.utils import suffix_filter as suffix_filter
from ..packaging_sys.utils import walk as walk
from ..user_decorators.user_flow_decorator import FlowMutator as FlowMutator

DEFAULT_PACKAGE_SUFFIXES: str

class package_sources(metaflow.user_decorators.user_flow_decorator.FlowMutator, metaclass=metaflow.user_decorators.user_flow_decorator.FlowMutatorMeta):
    """
    Include additional files or directories in a flow's code package.
    
    Relative source paths are resolved from the directory containing the flow
    file, not from the current working directory. By default, each source is
    placed in the code package under its basename.
    
    Parameters
    ----------
    sources : path-like, (path-like, path-like), or iterable of these
        A source file or directory, a ``(source, arcname)`` pair, or multiple
        source specifications. Directories are traversed recursively.
    
        A source may be absolute or relative to the flow file. The optional
        ``arcname`` in a pair specifies where that source is placed inside the
        code package.
    
        Use a list to specify exactly two sources without archive names;
        a two-item tuple is interpreted as ``(source, arcname)``.
    arcname : path-like, optional
        Destination for a single source inside the code package. It must be a
        safe relative path and cannot be absolute, ``.``, or contain ``..``.
        For multiple sources, specify archive paths with ``(source, arcname)``
        pairs instead.
    suffixes : iterable of str or comma-separated str, optional
        File suffixes to include. Leading dots are optional and matching is
        case-insensitive. The default is ``DEFAULT_PACKAGE_SUFFIXES``
        (``.py,.R,.RDS`` by default).
    
        Providing this argument replaces the default suffix set; it does not
        extend it.
    
    Raises
    ------
    MetaflowException
        If a source does not exist, an archive path is unsafe, or ``arcname``
        is used with multiple sources.
    
    Examples
    --------
    Given this project layout::
    
        project/
        ├── flows/
        │   └── train.py
        └── src/
            └── forecasting/
                └── __init__.py
    
    Package ``forecasting`` at the archive root so it remains importable as
    ``import forecasting`` during remote execution::
    
        from metaflow import FlowSpec, package_sources
    
        @package_sources("../src/forecasting")
        class TrainFlow(FlowSpec):
            ...
    
    Package multiple sources, assigning a custom archive location to one of
    them and including JSON files::
    
        @package_sources(
            [
                "../shared",
                ("../generated/client", "vendor/client"),
            ],
            suffixes=[".py", ".json"],
        )
        class TrainFlow(FlowSpec):
            ...
    """
    def init(self, sources, arcname = None, suffixes = None):
        ...
    def add_to_package(self) -> typing.Iterable[typing.Tuple[str, str, metaflow.packaging_sys.ContentType]]:
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

