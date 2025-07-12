######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.601524                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing
    import metaflow.datastore.content_addressed_store


DATASTORE_SYSROOT_S3: None

DATASTORE_SYSROOT_AZURE: None

DATASTORE_SYSROOT_GS: None

DATASTORE_SYSROOT_LOCAL: None

DEFAULT_FILE_SUFFIXES: list

CODE_PACKAGE_PREFIX: str

def walk_without_cycles(top_root):
    ...

def symlink_friendly_walk(root, exclude_hidden = True, suffixes = None):
    ...

class CodePackager(object, metaclass=type):
    """
    A datastore-agnostic class for packaging code.
    
    This class handles creating a code package (tarball) for deployment
    and provides methods for storing and retrieving it using Metaflow's
    ContentAddressedStore directly.
    
    Usage examples:
    ```python
    packager = CodePackager(
        datastore_type: str = "s3",
        datastore_root = None,
        code_package_prefix = None,
    )
    
    package_url, package_key = packager.store(
        paths_to_include = ["./"],
        file_suffixes = [".py", ".txt", ".yaml", ".yml", ".json"],
    )
    
    package_url, package_key = packager.store(
        package_create_fn = lambda: my_custom_package_create_fn(),
    )
    ```
    """
    def __init__(self, datastore_type: str = 's3', datastore_root: typing.Optional[str] = None, code_package_prefix: typing.Optional[str] = None):
        """
        Initialize the CodePackager with datastore configuration.
        
        Parameters
        ----------
        datastore_type : str, default "s3"
            The type of datastore to use: "s3", "azure", "gs", or "local"
        datastore_root : str, optional
            Root path for the datastore. If not provided, uses the default for the datastore type.
        code_package_prefix : str, optional
            The prefix to use for storing code packages in the content addressed store.
            If not provided, uses the CODE_PACKAGE_PREFIX configuration value.
        """
        ...
    def store(self, package_create_fn: typing.Optional[typing.Callable[[], bytes]] = None, paths_to_include: typing.Optional[typing.List[str]] = None, file_suffixes: typing.Optional[typing.List[str]] = None, metadata: typing.Optional[typing.Dict[str, typing.Any]] = None) -> typing.Tuple[str, str]:
        """
        Create and store a code package using Metaflow's ContentAddressedStore.
        
        This method can be called in two ways:
        1. With paths_to_include and file_suffixes to use the default packaging
        2. With a custom package_create_fn for custom packaging logic
        
        Parameters
        ----------
        package_create_fn : Callable[[], bytes], optional
            A function that creates and returns a package as bytes.
            This allows for custom packaging logic without dependency on specific objects.
        paths_to_include : List[str], optional
            List of paths to include in the package. Used by default_package_create.
        file_suffixes : List[str], optional
            List of file suffixes to include. Used by default_package_create.
        metadata : Dict[str, Any], optional
            Metadata to include in the package when using default_package_create.
        
        Returns
        -------
        Tuple[str, str]
            A tuple containing (package_url, package_key) that identifies the location
            and content-addressed key of the stored package.
        """
        ...
    @staticmethod
    def get_content_addressed_store(datastore_type: str = 's3', datastore_root: typing.Optional[str] = None, prefix: typing.Optional[str] = None) -> metaflow.datastore.content_addressed_store.ContentAddressedStore:
        """
        Get a ContentAddressedStore instance for the specified datastore.
        
        Parameters
        ----------
        datastore_type : str, default "s3"
            Type of datastore: "s3", "azure", "gs", or "local"
        datastore_root : str, optional
            Root path for the datastore. If not provided, uses the default for the datastore type.
        prefix : str, optional
            Prefix to use when storing objects in the datastore.
            If not provided, uses the CODE_PACKAGE_PREFIX configuration value.
        
        Returns
        -------
        ContentAddressedStore
            A ContentAddressedStore instance configured for the specified datastore
        """
        ...
    @staticmethod
    def get_download_cmd(package_url: str, datastore_type: str, python_cmd: str = 'python', target_file: str = 'job.tar', escape_quotes: bool = True) -> str:
        """
        Generate a command to download the code package.
        
        Parameters
        ----------
        package_url : str
            The URL of the package to download
        datastore_type : str
            The type of datastore (s3, azure, gs, local)
        python_cmd : str, optional
            The Python command to use
        target_file : str, optional
            The target file name to save the package as
        escape_quotes : bool, optional
            Whether to escape quotes in the command
        
        Returns
        -------
        str
            A shell command string to download the package
        """
        ...
    def get_package_commands(self, code_package_url: str, python_cmd: str = 'python', target_file: str = 'job.tar', working_dir: str = 'metaflow', retries: int = 5, escape_quotes: bool = True) -> typing.List[str]:
        """
        Get a complete list of shell commands to download and extract a code package.
        
        This method generates a comprehensive set of shell commands for downloading
        and extracting a code package, similar to MetaflowEnvironment.get_package_commands.
        
        Parameters
        ----------
        code_package_url : str
            The URL of the code package to download
        python_cmd : str, optional
            The Python command to use
        target_file : str, optional
            The target file name to save the package as
        working_dir : str, optional
            The directory to create and extract the package into
        retries : int, optional
            Number of download retries to attempt
        escape_quotes : bool, optional
            Whether to escape quotes in the command
        
        Returns
        -------
        List[str]
            List of shell commands to execute
        """
        ...
    @staticmethod
    def directory_walker(root, exclude_hidden = True, suffixes = None) -> typing.List[typing.Tuple[str, str]]:
        """
        Walk a directory and yield tuples of (file_path, relative_arcname) for files
        that match the given suffix filters. It will follow symlinks, but not cycles.
        
        This function is similar to MetaflowPackage._walk and handles symlinks safely.
        
        Parameters
        ----------
        root : str
            The root directory to walk
        exclude_hidden : bool, default True
            Whether to exclude hidden files and directories (those starting with '.')
        suffixes : List[str], optional
            List of file suffixes to include (e.g. ['.py', '.txt'])
        
        Returns
        -------
        List[Tuple[str, str]]
            List of tuples (file_path, relative_arcname) where:
            - file_path is the full path to the file
            - relative_arcname is the path to use within the archive
        """
        ...
    @staticmethod
    def default_package_create(paths: typing.List[str], suffixes: typing.List[str], metadata: typing.Optional[typing.Dict[str, typing.Any]] = None) -> bytes:
        """
        Create a default tarball package from specified paths.
        
        Parameters
        ----------
        paths : List[str]
            List of paths to include in the package
        suffixes : List[str]
            List of file suffixes to include
        metadata : Dict[str, Any], optional
            Metadata to include in the package
        
        Returns
        -------
        bytes
            The binary content of the tarball
        """
        ...
    @classmethod
    def package_directory(cls, directory_path: str, suffixes: typing.Optional[typing.List[str]] = None, exclude_hidden: bool = True, metadata: typing.Optional[typing.Dict[str, typing.Any]] = None) -> bytes:
        """
        Package a directory and all of its contents that match the given suffixes.
        
        This is a convenience method that works similarly to MetaflowPackage._walk
        to package a directory for deployment. Will default follow_symlinks.
        
        Parameters
        ----------
        directory_path : str
            The directory to package
        suffixes : List[str], optional
            List of file suffixes to include (defaults to standard code extensions)
        exclude_hidden : bool, default True
            Whether to exclude hidden files and directories
        metadata : Dict[str, Any], optional
            Metadata to include in the package
        Returns
        -------
        bytes
            The binary content of the tarball
        """
        ...
    ...

