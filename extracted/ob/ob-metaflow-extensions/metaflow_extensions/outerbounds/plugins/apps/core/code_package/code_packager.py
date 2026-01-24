import os
import sys
import time
import tarfile
import json
from io import BytesIO
from typing import List, Tuple, Dict, Any, Optional, Callable, Union

from metaflow.datastore.content_addressed_store import ContentAddressedStore
from metaflow.util import to_unicode
from metaflow.metaflow_config import (
    DATASTORE_SYSROOT_S3,
    DATASTORE_SYSROOT_AZURE,
    DATASTORE_SYSROOT_GS,
    DATASTORE_SYSROOT_LOCAL,
)

DEFAULT_FILE_SUFFIXES = [
    ".py",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".html",
    ".css",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".md",
    ".rst",
]
# Default prefix for code packages in content addressed store
CODE_PACKAGE_PREFIX = "apps-code-packages"


# this is os.walk(follow_symlinks=True) with cycle detection
def walk_without_cycles(top_root):
    seen = set()

    def _recurse(root):
        for parent, dirs, files in os.walk(root):
            for d in dirs:
                path = os.path.join(parent, d)
                if os.path.islink(path):
                    # Breaking loops: never follow the same symlink twice
                    #
                    # NOTE: this also means that links to sibling links are
                    # not followed. In this case:
                    #
                    #   x -> y
                    #   y -> oo
                    #   oo/real_file
                    #
                    # real_file is only included twice, not three times
                    reallink = os.path.realpath(path)
                    if reallink not in seen:
                        seen.add(reallink)
                        for x in _recurse(path):
                            yield x
            yield parent, files

    for x in _recurse(top_root):
        yield x


def symlink_friendly_walk(root, exclude_hidden=True, suffixes=None):
    if suffixes is None:
        suffixes = []
    root = to_unicode(root)  # handle files/folder with non ascii chars
    prefixlen = len("%s/" % os.path.dirname(root))
    for (
        path,
        files,
    ) in walk_without_cycles(root):
        if exclude_hidden and "/." in path:
            continue
        # path = path[2:] # strip the ./ prefix
        # if path and (path[0] == '.' or './' in path):
        #    continue
        for fname in files:
            if (fname[0] == "." and fname in suffixes) or (
                fname[0] != "." and any(fname.endswith(suffix) for suffix in suffixes)
            ):
                p = os.path.join(path, fname)
                yield p, p[prefixlen:]


class CodePackager:
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

    def __init__(
        self,
        datastore_type: str = "s3",
        datastore_root: Optional[str] = None,
        code_package_prefix: Optional[str] = None,
    ):
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
        self._datastore_type = datastore_type
        self._datastore_root = datastore_root
        self._code_package_prefix = code_package_prefix

    def store(
        self,
        package_create_fn: Optional[Callable[[], bytes]] = None,
        paths_to_include: Optional[List[str]] = None,
        file_suffixes: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, str]:
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
        # Prepare default values
        _paths_to_include = paths_to_include or []
        _file_suffixes = file_suffixes or DEFAULT_FILE_SUFFIXES
        _metadata = metadata or {}

        # If no package_create_fn provided, use default_package_create
        if package_create_fn is None:
            _package_create_fn = lambda: self.default_package_create(
                _paths_to_include, _file_suffixes, _metadata
            )
        else:
            _package_create_fn = package_create_fn

        # Create the package
        code_package = _package_create_fn()

        # Get the ContentAddressedStore for the specified datastore
        ca_store = self.get_content_addressed_store(
            datastore_type=self._datastore_type,
            datastore_root=self._datastore_root,
            prefix=(
                str(self._code_package_prefix)
                if self._code_package_prefix is not None
                else str(CODE_PACKAGE_PREFIX)
            ),
        )

        # Store the package using raw=True to ensure we can access it directly via URL
        results = ca_store.save_blobs([code_package], raw=True, len_hint=1)
        package_url, package_key = results[0].uri, results[0].key

        return package_url, package_key

    @staticmethod
    def get_content_addressed_store(
        datastore_type: str = "s3",
        datastore_root: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> ContentAddressedStore:
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
        from metaflow.plugins import DATASTORES

        datastore_impls = [i for i in DATASTORES if i.TYPE == datastore_type]
        if len(datastore_impls) == 0:
            raise ValueError(f"Unsupported datastore type: {datastore_type}")
        if len(datastore_impls) > 1:
            raise ValueError(
                f"Multiple datastore implementations found for type: {datastore_type}"
            )
        datastore_impl = datastore_impls[0]
        root = None
        # Import the storage implementation based on datastore_type
        if datastore_type == "s3":
            root = datastore_root or DATASTORE_SYSROOT_S3
        elif datastore_type == "azure":
            root = datastore_root or DATASTORE_SYSROOT_AZURE
        elif datastore_type == "gs":
            root = datastore_root or DATASTORE_SYSROOT_GS
        elif datastore_type == "local":
            root = datastore_root or DATASTORE_SYSROOT_LOCAL

        # Ensure prefix is a string
        store_prefix = str(prefix) if prefix is not None else str(CODE_PACKAGE_PREFIX)

        storage_impl = datastore_impl(root=root)
        # Create and return a ContentAddressedStore
        return ContentAddressedStore(prefix=store_prefix, storage_impl=storage_impl)

    @staticmethod
    def get_download_cmd(
        package_url: str,
        datastore_type: str,
        python_cmd: str = "python",
        target_file: str = "job.tar",
        escape_quotes: bool = True,
    ) -> str:
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
        if datastore_type == "s3":
            from metaflow.plugins.aws.aws_utils import parse_s3_full_path

            bucket, s3_object = parse_s3_full_path(package_url)
            # Simplify the script and use single quotes to avoid shell escaping issues
            script = 'import boto3, os; ep=os.getenv({quote}METAFLOW_S3_ENDPOINT_URL{quote}); boto3.client("s3", **({{"endpoint_url":ep}} if ep else {{}})).download_file({quote}{bucket}{quote}, {quote}{s3_object}{quote}, {quote}{target_file}{quote})'.format(
                quote='\\"' if escape_quotes else '"',
                bucket=bucket,
                s3_object=s3_object,
                target_file=target_file,
            )
            # Format the command with proper quoting
            return f"{python_cmd} -c '{script}'"
        elif datastore_type == "azure":
            from metaflow.plugins.azure.azure_utils import parse_azure_full_path

            container_name, blob = parse_azure_full_path(package_url)
            # remove a trailing slash, if present
            blob_endpoint = "${METAFLOW_AZURE_STORAGE_BLOB_SERVICE_ENDPOINT%/}"
            return "download-azure-blob --blob-endpoint={blob_endpoint} --container={container} --blob={blob} --output-file={target}".format(
                blob_endpoint=blob_endpoint,
                blob=blob,
                container=container_name,
                target=target_file,
            )
        elif datastore_type == "gs":
            from metaflow.plugins.gcp.gs_utils import parse_gs_full_path

            bucket_name, gs_object = parse_gs_full_path(package_url)
            return "download-gcp-object --bucket=%s --object=%s --output-file=%s" % (
                bucket_name,
                gs_object,
                target_file,
            )
        elif datastore_type == "local":
            # For local storage, simply copy the file
            return "cp %s %s" % (package_url, target_file)
        else:
            raise NotImplementedError(
                f"Download command not implemented for datastore type: {datastore_type}"
            )

    def get_package_commands(
        self,
        code_package_url: str,
        python_cmd: str = "python",
        target_file: str = "job.tar",
        working_dir: str = "metaflow",
        retries: int = 5,
        escape_quotes: bool = True,
    ) -> List[str]:
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
        # Use the datastore_type from initialization if not provided
        datastore_type = self._datastore_type

        # Helper function to create dependency installation command
        def _get_install_dependencies_cmd():
            base_cmd = "{} -m pip install -qqq --no-compile --no-cache-dir --disable-pip-version-check".format(
                python_cmd
            )

            datastore_packages = {
                "s3": ["boto3"],
                "azure": [
                    "azure-identity",
                    "azure-storage-blob",
                    "azure-keyvault-secrets",
                    "simple-azure-blob-downloader",
                ],
                "gs": [
                    "google-cloud-storage",
                    "google-auth",
                    "simple-gcp-object-downloader",
                    "google-cloud-secret-manager",
                    "packaging",
                ],
                "local": [],
            }

            if datastore_type not in datastore_packages:
                raise NotImplementedError(
                    "Unknown datastore type: {}".format(datastore_type)
                )

            if not datastore_packages[datastore_type]:
                return "# No dependencies required for local datastore"

            cmd = "{} {}".format(
                base_cmd, " ".join(datastore_packages[datastore_type] + ["requests"])
            )
            # Skip pip installs if we know packages might already be available
            return "if [ -z $METAFLOW_SKIP_INSTALL_DEPENDENCIES ]; then {}; fi".format(
                cmd
            )

        download_cmd = self.get_download_cmd(
            code_package_url, datastore_type, python_cmd, target_file, escape_quotes
        )

        # Define the log functions for bash
        bash_mflog = (
            'function mflog() { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")]" "$@"; }'
        )
        bash_flush_logs = 'function flush_mflogs() { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Flushing logs"; }'

        cmds = [
            bash_mflog,
            bash_flush_logs,
            "mflog 'Setting up task environment.'",
            _get_install_dependencies_cmd(),
            f"mkdir -p {working_dir}",
            f"cd {working_dir}",
            "mkdir -p .metaflow",  # mute local datastore creation log
            f"i=0; while [ $i -le {retries} ]; do "
            "mflog 'Downloading code package...'; "
            + download_cmd
            + " && mflog 'Code package downloaded.' && break; "
            "sleep 10; i=$((i+1)); "
            "done",
            f"if [ $i -gt {retries} ]; then "
            "mflog 'Failed to download code package from %s "
            f"after {retries+1} tries. Exiting...' && exit 1; "
            "fi" % code_package_url,
            "TAR_OPTIONS='--warning=no-timestamp' tar xf %s" % target_file,
            "mflog 'Task is starting.'",
            "flush_mflogs",
        ]

        return cmds

    @staticmethod
    def directory_walker(
        root,
        exclude_hidden=True,
        suffixes=None,
        normalized_rel_path=False,
    ) -> List[Tuple[str, str]]:
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
        normalized_rel_path : bool, default False
            Whether to normalize the relative from the root. ie if the root is /a/b/c and the file is /a/b/c/d/e.py then the relative path will be d/e.py

        Returns
        -------
        List[Tuple[str, str]]
            List of tuples (file_path, relative_arcname) where:
            - file_path is the full path to the file
            - relative_arcname is the path to use within the archive
        """
        files = []
        for file_path, rel_path in symlink_friendly_walk(
            root, exclude_hidden, suffixes
        ):
            if normalized_rel_path:
                rel_path = file_path.replace(root, "")
            files.append((file_path, rel_path))
        return files

    @staticmethod
    def default_package_create(
        paths: List[str], suffixes: List[str], metadata: Optional[Dict[str, Any]] = None
    ) -> bytes:
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
        buf = BytesIO()

        with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=3) as tar:
            # Add metadata if provided
            if metadata:
                metadata_buf = BytesIO()
                metadata_buf.write(json.dumps(metadata).encode("utf-8"))
                metadata_buf.seek(0)
                info = tarfile.TarInfo("metadata.json")
                info.size = len(metadata_buf.getvalue())
                info.mtime = 1747158696  # 13 May 2025 10:31:36 (so that we dont have a changing hash everytime we run)
                tar.addfile(info, metadata_buf)

            def no_mtime(tarinfo):
                # a modification time change should not change the hash of
                # the package. Only content modifications will.
                # Setting this default to Dec 3, 2019
                tarinfo.mtime = 1747158696  # 13 May 2025 10:31:36 (so that we dont have a changing hash everytime we run)
                return tarinfo

            # Add files from specified paths
            for path in paths:
                if os.path.isdir(path):
                    # Use directory_walker for directories to handle symlinks properly
                    for file_path, rel_path in CodePackager.directory_walker(
                        path,
                        exclude_hidden=True,
                        suffixes=suffixes,
                        normalized_rel_path=True,
                    ):
                        tar.add(
                            file_path,
                            arcname=rel_path,
                            filter=no_mtime,
                            recursive=False,
                        )
                elif os.path.isfile(path):
                    if any(path.endswith(suffix) for suffix in suffixes):
                        tar.add(path, arcname=os.path.basename(path))

        tarball = bytearray(buf.getvalue())
        tarball[4:8] = [0] * 4  # Reset 4 bytes from offset 4 to account for ts
        return tarball

    @staticmethod
    def _add_tar_file(tar, filename, buf):
        tarinfo = tarfile.TarInfo(name=filename)
        tarinfo.size = len(buf.getvalue())
        buf.seek(0)
        tarinfo.mtime = 1747158696  # 13 May 2025 10:31:36 (so that we dont have a changing hash everytime we run)
        tar.addfile(tarinfo, fileobj=buf)

    @classmethod
    def package_directory(
        cls,
        directory_path: str,
        suffixes: Optional[List[str]] = None,
        exclude_hidden: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bytes:
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
        if not os.path.isdir(directory_path):
            raise ValueError(f"The path '{directory_path}' is not a directory")

        # Use default suffixes if none provided
        if suffixes is None:
            suffixes = [".py", ".txt", ".yaml", ".yml", ".json"]

        buf = BytesIO()

        def no_mtime(tarinfo):
            # a modification time change should not change the hash of
            # the package. Only content modifications will.
            # Setting this to a fixed date so that we don't have a changing hash everytime we run
            tarinfo.mtime = 1747158696  # 13 May 2025 10:31:36
            return tarinfo

        with tarfile.open(
            fileobj=buf, mode="w:gz", compresslevel=3, dereference=True
        ) as tar:
            # Add metadata if provided
            if metadata:
                cls._add_tar_file(
                    tar, "metadata.json", BytesIO(json.dumps(metadata).encode("utf-8"))
                )

            # Walk the directory and add matching files
            for file_path, rel_path in cls.directory_walker(
                directory_path,
                exclude_hidden=exclude_hidden,
                suffixes=suffixes,
            ):
                # Remove debug print statement
                tar.add(file_path, arcname=rel_path, recursive=False, filter=no_mtime)

        tarball = bytearray(buf.getvalue())
        tarball[4:8] = [0] * 4  # Reset 4 bytes from offset 4 to account for ts
        return tarball
