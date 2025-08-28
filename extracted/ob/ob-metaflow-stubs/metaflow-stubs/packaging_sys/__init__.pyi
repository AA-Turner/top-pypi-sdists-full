######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-28T00:53:38.061406                                                            #
######################################################################################################

from __future__ import annotations

import enum
import typing
import metaflow
if typing.TYPE_CHECKING:
    import typing
    import metaflow.packaging_sys.backend
    import metaflow.extension_support.metadata
    import metaflow.packaging_sys.tar_backend
    import enum
    import metaflow.packaging_sys

from . import distribution_support as distribution_support
from .distribution_support import PackagedDistributionFinder as PackagedDistributionFinder
from . import backend as backend
from .backend import PackagingBackend as PackagingBackend
from . import tar_backend as tar_backend
from .tar_backend import TarPackagingBackend as TarPackagingBackend
from . import utils as utils
from . import v1 as v1

TYPE_CHECKING: bool

MFCONTENT_MARKER: str

class ContentType(enum.IntEnum, metaclass=enum.EnumType):
    def __new__(cls, value):
        ...
    ...

class MetaflowCodeContent(object, metaclass=type):
    """
    Base class for all Metaflow code packages (non user code).
    
    A Metaflow code package, at a minimum, contains:
      - a special INFO file (containing a bunch of metadata about the Metaflow environment)
      - a special CONFIG file (containing user configurations for the flow)
    
    Declare all other MetaflowCodeContent subclasses (versions) here to handle just the functions
    that are not implemented here. In a *separate* file, declare any other
    function for that specific version.
    
    NOTE: This file must remain as dependency-free as possible as it is loaded *very*
    early on. This is why you must decleare a *separate* class implementing what you want
    the Metaflow code package (non user) to do.
    """
    @classmethod
    def get_info(cls) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Get the content of the special INFO file on the local filesystem after
        the code package has been expanded.
        
        Returns
        -------
        Optional[Dict[str, Any]]
            The content of the INFO file -- None if there is no such file.
        """
        ...
    @classmethod
    def get_config(cls) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Get the content of the special CONFIG file on the local filesystem after
        the code package has been expanded.
        
        Returns
        -------
        Optional[Dict[str, Any]]
            The content of the CONFIG file -- None if there is no such file.
        """
        ...
    @classmethod
    def get_filename(cls, filename: str, content_type: ContentType) -> typing.Optional[str]:
        """
        Get the path to a file extracted from the archive. The filename is the filename
        passed in when creating the archive and content_type is the type of the content.
        
        This function will return the local path where the file can be found after
        the package has been extracted.
        
        Parameters
        ----------
        filename: str
            The name of the file on the filesystem.
        content_type: ContentType
        
        Returns
        -------
        str
            The path to the file on the local filesystem or None if not found.
        """
        ...
    @classmethod
    def get_env_vars_for_packaged_metaflow(cls, dest_dir: str) -> typing.Dict[str, str]:
        """
        Get the environment variables that are needed to run Metaflow when it is
        packaged. This is typically used to set the PYTHONPATH to include the
        directory where the Metaflow code package has been extracted.
        
        Returns
        -------
        Dict[str, str]
            The environment variables that are needed to run Metaflow when it is
            packaged it present.
        """
        ...
    @classmethod
    def get_archive_info(cls, archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Get the content of the special INFO file in the archive.
        
        Returns
        -------
        Optional[Dict[str, Any]]
            The content of the INFO file -- None if there is no such file.
        """
        ...
    @classmethod
    def get_archive_config(cls, archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Get the content of the special CONFIG file in the archive.
        
        Returns
        -------
        Optional[Dict[str, Any]]
            The content of the CONFIG file -- None if there is no such file.
        """
        ...
    @classmethod
    def get_archive_filename(cls, archive: typing.Any, filename: str, content_type: ContentType, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[str]:
        """
        Get the filename of the archive. This does not do any extraction but simply
        returns where, in the archive, the file is located. This is the equivalent of
        get_filename but for files not extracted yet.
        
        Parameters
        ----------
        archive: Any
            The archive to get the filename from.
        filename: str
            The name of the file in the archive.
        content_type: ContentType
            The type of the content (e.g., code, other, etc.).
        packaging_backend: Type[PackagingBackend], default TarPackagingBackend
            The packaging backend to use.
        
        Returns
        -------
        str
            The filename of the archive or None if not found.
        """
        ...
    @classmethod
    def get_archive_content_members(cls, archive: typing.Any, content_types: typing.Optional[int] = None, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.List[typing.Any]:
        ...
    @classmethod
    def get_distribution_finder(cls) -> typing.Optional["metaflow.extension_support.metadata.DistributionFinder"]:
        """
        Get the distribution finder for the Metaflow code package (if applicable).
        
        Some packages will include distribution information to "pretend" that some packages
        are actually distributions even if we just include them in the code package.
        
        Returns
        -------
        Optional["metaflow.extension_support.metadata.DistributionFinder"]
            The distribution finder for the Metaflow code package -- None if there is no
            such finder.
        """
        ...
    @classmethod
    def get_post_extract_env_vars(cls, version_id: int, dest_dir: str = '.') -> typing.Dict[str, str]:
        """
        Get the post-extract environment variables that are needed to access the content
        that has been extracted into dest_dir.
        
        This will typically involve setting PYTHONPATH.
        
        Parameters
        ----------
        version_id: int
            The version of MetaflowCodeContent for this package.
        dest_dir: str, default "."
            The directory where the content has been extracted to.
        
        Returns
        -------
        Dict[str, str]
            The post-extract environment variables that are needed to access the content
            that has been extracted into extracted_dir.
        """
        ...
    @classmethod
    def get_info_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_config_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_filename_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], filename: str, content_type: ContentType) -> typing.Optional[str]:
        ...
    @classmethod
    def get_distribution_finder_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional["metaflow.extension_support.metadata.DistributionFinder"]:
        ...
    @classmethod
    def get_archive_info_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_archive_config_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_archive_filename_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, filename: str, content_type: ContentType, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[str]:
        ...
    @classmethod
    def get_archive_content_members_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, content_types: typing.Optional[int] = None, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.List[typing.Any]:
        ...
    @classmethod
    def get_post_extract_env_vars_impl(cls, dest_dir: str) -> typing.Dict[str, str]:
        ...
    @classmethod
    def __init_subclass__(cls, version_id, **kwargs):
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
    def add_module(self, module_path: module):
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
    def get_package_version(self) -> int:
        """
        Get the version of MetaflowCodeContent for this package.
        """
        ...
    ...

class MetaflowCodeContentV0(MetaflowCodeContent, metaclass=type):
    @classmethod
    def get_info_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_config_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_filename_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], filename: str, content_type: ContentType) -> typing.Optional[str]:
        """
        For V0, the filename is simply the filename passed in.
        """
        ...
    @classmethod
    def get_distribution_finder_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional["metaflow.extension_support.metadata.DistributionFinder"]:
        ...
    @classmethod
    def get_archive_info_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_archive_config_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_archive_filename_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, filename: str, content_type: ContentType, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> str:
        ...
    @classmethod
    def get_archive_content_members_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, content_types: typing.Optional[int] = None, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.List[typing.Any]:
        """
        For V0, we use a static list of known files to classify the content
        """
        ...
    @classmethod
    def get_post_extract_env_vars_impl(cls, dest_dir: str) -> typing.Dict[str, str]:
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
    ...

class MetaflowCodeContentV1Base(MetaflowCodeContent, metaclass=type):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        ...
    def __init__(self, code_dir: str, other_dir: str):
        ...
    @classmethod
    def get_info_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_config_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_filename_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], filename: str, content_type: ContentType) -> typing.Optional[str]:
        ...
    @classmethod
    def get_distribution_finder_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]]) -> typing.Optional["metaflow.extension_support.metadata.DistributionFinder"]:
        ...
    @classmethod
    def get_archive_info_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_archive_config_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.Optional[typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def get_archive_filename_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, filename: str, content_type: ContentType, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> str:
        ...
    @classmethod
    def get_archive_content_members_impl(cls, mfcontent_info: typing.Optional[typing.Dict[str, typing.Any]], archive: typing.Any, content_types: typing.Optional[int] = None, packaging_backend: typing.Type[metaflow.packaging_sys.backend.PackagingBackend] = metaflow.packaging_sys.tar_backend.TarPackagingBackend) -> typing.List[typing.Any]:
        ...
    @classmethod
    def get_post_extract_env_vars_impl(cls, dest_dir: str) -> typing.Dict[str, str]:
        ...
    ...

