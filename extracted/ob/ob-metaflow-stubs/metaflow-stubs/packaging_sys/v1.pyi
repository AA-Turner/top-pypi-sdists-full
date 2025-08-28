######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-28T00:53:38.096743                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import typing
    import metaflow.packaging_sys

from ..exception import MetaflowException as MetaflowException
from ..user_decorators.user_flow_decorator import FlowMutatorMeta as FlowMutatorMeta
from ..user_decorators.user_step_decorator import UserStepDecoratorMeta as UserStepDecoratorMeta
from . import ContentType as ContentType
from . import MetaflowCodeContentV1Base as MetaflowCodeContentV1Base
from .distribution_support import modules_to_distributions as modules_to_distributions
from .utils import suffix_filter as suffix_filter
from .utils import walk as walk

EXT_EXCLUDE_SUFFIXES: list

MFCONTENT_MARKER: str

class MetaflowCodeContentV1(metaflow.packaging_sys.MetaflowCodeContentV1Base, metaclass=type):
    def __init__(self, code_dir: str = '.mf_code', other_dir: str = '.mf_meta', criteria: typing.Callable[[module], bool] = ...):
        ...
    def create_mfcontent_info(self) -> typing.Dict[str, typing.Any]:
        ...
    def get_excluded_tl_entries(self) -> typing.List[str]:
        """
        When packaging Metaflow from within an executing Metaflow flow, we need to
        exclude the files that are inserted by this content from being packaged (possibly).
        
        Use this function to return these files or top-level directories.
        
        Returns
        -------
        List[str]
            Files or directories to exclude
        """
        ...
    def content_names(self, content_types: typing.Optional[int] = None) -> typing.Generator[typing.Tuple[str, str], None, None]:
        """
        Detailed list of the content of this MetaflowCodeContent. This will list all files
        (or non files -- for the INFO or CONFIG data for example) present in the archive.
        
        Parameters
        ----------
        content_types : Optional[int]
            The type of content to get the names of. If None, all content is returned.
        
        Yields
        ------
        Generator[Tuple[str, str], None, None]
            Path on the filesystem and the name in the archive
        """
        ...
    def contents(self, content_types: typing.Optional[int] = None) -> typing.Generator[typing.Tuple[typing.Union[bytes, str], str], None, None]:
        """
        Very similar to content_names but returns the content of the non-files
        as well as bytes. For files, identical output as content_names
        
        Parameters
        ----------
        content_types : Optional[int]
            The type of content to get the content of. If None, all content is returned.
        
        Yields
        ------
        Generator[Tuple[Union[str, bytes], str], None, None]
            Content of the MF content
        """
        ...
    def show(self) -> str:
        """
        Returns a more human-readable string representation of the content of this
        MetaflowCodeContent. This will not, for example, list all files but summarize what
        is included at a more high level.
        
        Returns
        -------
        str
            A human-readable string representation of the content of this MetaflowCodeContent
        """
        ...
    def add_info(self, info: typing.Dict[str, typing.Any]):
        """
        Add the content of the INFO file to the Metaflow content
        
        Parameters
        ----------
        info: Dict[str, Any]
            The content of the INFO file
        """
        ...
    def add_config(self, config: typing.Dict[str, typing.Any]):
        """
        Add the content of the CONFIG file to the Metaflow content
        
        Parameters
        ----------
        config: Dict[str, Any]
            The content of the CONFIG file
        """
        ...
    def add_module(self, module: module):
        """
        Add a python module to the Metaflow content
        
        Parameters
        ----------
        module_path: ModuleType
            The module to add
        """
        ...
    def add_code_file(self, file_path: str, file_name: str):
        """
        Add a code file to the Metaflow content
        
        Parameters
        ----------
        file_path: str
            The path to the code file to add (on the filesystem)
        file_name: str
            The path in the archive to add the code file to
        """
        ...
    def add_other_file(self, file_path: str, file_name: str):
        """
        Add a non-python file to the Metaflow content
        
        Parameters
        ----------
        file_path: str
            The path to the file to add (on the filesystem)
        file_name: str
            The path in the archive to add the file to
        """
        ...
    ...

