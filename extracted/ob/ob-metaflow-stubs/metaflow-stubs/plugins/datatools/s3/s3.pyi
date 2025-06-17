######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.919450                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import io
    import metaflow.exception
    import metaflow.plugins.datatools.s3.s3

from ....flowspec import FlowSpec as FlowSpec
from ....metaflow_current import current as current
from ....tuple_util import namedtuple_with_defaults as namedtuple_with_defaults
from ....exception import MetaflowException as MetaflowException
from .s3util import get_s3_client as get_s3_client
from .s3util import read_in_chunks as read_in_chunks
from .s3util import get_timestamp as get_timestamp

TYPE_CHECKING: bool

DATATOOLS_S3ROOT: None

S3_RETRY_COUNT: int

S3_TRANSIENT_RETRY_COUNT: int

S3_SERVER_SIDE_ENCRYPTION: None

S3_WORKER_COUNT: int

TEMPDIR: str

TRANSIENT_RETRY_START_LINE: str

TRANSIENT_RETRY_LINE_CONTENT: str

def check_s3_deps(func):
    """
    The decorated function checks S3 dependencies (as needed for AWS S3 storage backend).
    This includes boto3.
    """
    ...

TEST_INJECT_RETRYABLE_FAILURES: int

def ensure_unicode(x):
    ...

class S3GetObject(tuple, metaclass=type):
    """
    S3GetObject(key, offset, length)
    """
    @staticmethod
    def __new__(_cls, key: str, offset: int, length: int):
        """
        Create new instance of S3GetObject(key, offset, length)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    def __init__(self, key: str, offset: int, length: int):
        ...
    ...

class S3PutObject(tuple, metaclass=type):
    """
    S3PutObject(key, value, path, content_type, encryption, metadata)
    """
    @staticmethod
    def __new__(_cls, key: str, value: typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes, None] = None, path: typing.Optional[str] = None, content_type: typing.Optional[str] = None, encryption: typing.Optional[str] = None, metadata: typing.Optional[typing.Dict[str, str]] = None):
        """
        Create new instance of S3PutObject(key, value, path, content_type, encryption, metadata)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    def __init__(self, key: str, value: typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes, None], path: typing.Optional[str], content_type: typing.Optional[str], encryption: typing.Optional[str], metadata: typing.Optional[typing.Dict[str, str]]):
        ...
    ...

class RangeInfo(tuple, metaclass=type):
    """
    RangeInfo(total_size, request_offset, request_length)
    """
    @staticmethod
    def __new__(_cls, total_size: int, request_offset: int = 0, request_length: int = -1):
        """
        Create new instance of RangeInfo(total_size, request_offset, request_length)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    def __init__(self, total_size: int, request_offset: int, request_length: int):
        ...
    ...

class MetaflowS3InvalidObject(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowS3URLException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowS3Exception(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowS3NotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowS3AccessDenied(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowS3InvalidRange(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowS3InsufficientDiskSpace(metaflow.exception.MetaflowException, metaclass=type):
    ...

class S3Object(object, metaclass=type):
    """
    This object represents a path or an object in S3,
    with an optional local copy.
    
    `S3Object`s are not instantiated directly, but they are returned
    by many methods of the `S3` client.
    """
    def __init__(self, prefix: str, url: str, path: str, size: typing.Optional[int] = None, content_type: typing.Optional[str] = None, metadata: typing.Optional[typing.Dict[str, str]] = None, range_info: typing.Optional[metaflow.plugins.datatools.s3.s3.RangeInfo] = None, last_modified: typing.Optional[int] = None, encryption: typing.Optional[str] = None):
        ...
    @property
    def exists(self) -> bool:
        """
        Does this key correspond to an object in S3?
        
        Returns
        -------
        bool
            True if this object points at an existing object (file) in S3.
        """
        ...
    @property
    def downloaded(self) -> bool:
        """
        Has this object been downloaded?
        
        If True, the contents can be accessed through `path`, `blob`,
        and `text` properties.
        
        Returns
        -------
        bool
            True if the contents of this object have been downloaded.
        """
        ...
    @property
    def url(self) -> str:
        """
        S3 location of the object
        
        Returns
        -------
        str
            The S3 location of this object.
        """
        ...
    @property
    def prefix(self) -> str:
        """
        Prefix requested that matches this object.
        
        Returns
        -------
        str
            Requested prefix
        """
        ...
    @property
    def key(self) -> str:
        """
        Key corresponds to the key given to the get call that produced
        this object.
        
        This may be a full S3 URL or a suffix based on what
        was requested.
        
        Returns
        -------
        str
            Key requested.
        """
        ...
    @property
    def path(self) -> typing.Optional[str]:
        """
        Path to a local temporary file corresponding to the object downloaded.
        
        This file gets deleted automatically when a S3 scope exits.
        Returns None if this S3Object has not been downloaded.
        
        Returns
        -------
        str
            Local path, if the object has been downloaded.
        """
        ...
    @property
    def blob(self) -> typing.Optional[bytes]:
        """
        Contents of the object as a byte string or None if the
        object hasn't been downloaded.
        
        Returns
        -------
        bytes
            Contents of the object as bytes.
        """
        ...
    @property
    def text(self) -> typing.Optional[str]:
        """
        Contents of the object as a string or None if the
        object hasn't been downloaded.
        
        The object is assumed to contain UTF-8 encoded data.
        
        Returns
        -------
        str
            Contents of the object as text.
        """
        ...
    @property
    def size(self) -> typing.Optional[int]:
        """
        Size of the object in bytes.
        
        Returns None if the key does not correspond to an object in S3.
        
        Returns
        -------
        int
            Size of the object in bytes, if the object exists.
        """
        ...
    @property
    def has_info(self) -> bool:
        """
        Returns true if this `S3Object` contains the content-type MIME header or
        user-defined metadata.
        
        If False, this means that `content_type`, `metadata`, `range_info` and
        `last_modified` will return None.
        
        Returns
        -------
        bool
            True if additional metadata is available.
        """
        ...
    @property
    def metadata(self) -> typing.Optional[typing.Dict[str, str]]:
        """
        Returns a dictionary of user-defined metadata, or None if no metadata
        is defined.
        
        Returns
        -------
        Dict
            User-defined metadata.
        """
        ...
    @property
    def content_type(self) -> typing.Optional[str]:
        """
        Returns the content-type of the S3 object or None if it is not defined.
        
        Returns
        -------
        str
            Content type or None if the content type is undefined.
        """
        ...
    @property
    def encryption(self) -> typing.Optional[str]:
        """
        Returns the encryption type of the S3 object or None if it is not defined.
        
        Returns
        -------
        str
            Server-side-encryption type or None if parameter is not set.
        """
        ...
    @property
    def range_info(self) -> typing.Optional[metaflow.plugins.datatools.s3.s3.RangeInfo]:
        """
        If the object corresponds to a partially downloaded object, returns
        information of what was downloaded.
        
        The returned object has the following fields:
        - `total_size`: Size of the object in S3.
        - `request_offset`: The starting offset.
        - `request_length`: The number of bytes downloaded.
        
        Returns
        -------
        namedtuple
            An object containing information about the partial download. If
            the `S3Object` doesn't correspond to a partially downloaded file,
            returns None.
        """
        ...
    @property
    def last_modified(self) -> typing.Optional[int]:
        """
        Returns the last modified unix timestamp of the object.
        
        Returns
        -------
        int
            Unix timestamp corresponding to the last modified time.
        """
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class S3Client(object, metaclass=type):
    def __init__(self, s3_role_arn = None, s3_session_vars = None, s3_client_params = None):
        ...
    @property
    def client(self):
        ...
    @property
    def error(self):
        ...
    def reset_client(self):
        ...
    ...

class S3(object, metaclass=type):
    """
    The Metaflow S3 client.
    
    This object manages the connection to S3 and a temporary diretory that is used
    to download objects. Note that in most cases when the data fits in memory, no local
    disk IO is needed as operations are cached by the operating system, which makes
    operations fast as long as there is enough memory available.
    
    The easiest way is to use this object as a context manager:
    ```
    with S3() as s3:
        data = [obj.blob for obj in s3.get_many(urls)]
    print(data)
    ```
    The context manager takes care of creating and deleting a temporary directory
    automatically. Without a context manager, you must call `.close()` to delete
    the directory explicitly:
    ```
    s3 = S3()
    data = [obj.blob for obj in s3.get_many(urls)]
    s3.close()
    ```
    You can customize the location of the temporary directory with `tmproot`. It
    defaults to the current working directory.
    
    To make it easier to deal with object locations, the client can be initialized
    with an S3 path prefix. There are three ways to handle locations:
    
    1. Use a `metaflow.Run` object or `self`, e.g. `S3(run=self)` which
       initializes the prefix with the global `DATATOOLS_S3ROOT` path, combined
       with the current run ID. This mode makes it easy to version data based
       on the run ID consistently. You can use the `bucket` and `prefix` to
       override parts of `DATATOOLS_S3ROOT`.
    
    2. Specify an S3 prefix explicitly with `s3root`,
       e.g. `S3(s3root='s3://mybucket/some/path')`.
    
    3. Specify nothing, i.e. `S3()`, in which case all operations require
       a full S3 url prefixed with `s3://`.
    
    Parameters
    ----------
    tmproot : str, default: '.'
        Where to store the temporary directory.
    bucket : str, optional
        Override the bucket from `DATATOOLS_S3ROOT` when `run` is specified.
    prefix : str, optional
        Override the path from `DATATOOLS_S3ROOT` when `run` is specified.
    run : FlowSpec or Run, optional
        Derive path prefix from the current or a past run ID, e.g. S3(run=self).
    s3root : str, optional
        If `run` is not specified, use this as the S3 prefix.
    """
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __enter__(self) -> "S3":
        ...
    def __exit__(self, *args):
        ...
    def close(self):
        """
        Delete all temporary files downloaded in this context.
        """
        ...
    def list_paths(self, keys: typing.Optional[typing.Iterable[str]] = None) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        List the next level of paths in S3.
        
        If multiple keys are specified, listings are done in parallel. The returned
        S3Objects have `.exists == False` if the path refers to a prefix, not an
        existing S3 object.
        
        For instance, if the directory hierarchy is
        ```
        a/0.txt
        a/b/1.txt
        a/c/2.txt
        a/d/e/3.txt
        f/4.txt
        ```
        The `list_paths(['a', 'f'])` call returns
        ```
        a/0.txt (exists == True)
        a/b/ (exists == False)
        a/c/ (exists == False)
        a/d/ (exists == False)
        f/4.txt (exists == True)
        ```
        
        Parameters
        ----------
        keys : Iterable[str], optional, default None
            List of paths.
        
        Returns
        -------
        List[S3Object]
            S3Objects under the given paths, including prefixes (directories) that
            do not correspond to leaf objects.
        """
        ...
    def list_recursive(self, keys: typing.Optional[typing.Iterable[str]] = None) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        List all objects recursively under the given prefixes.
        
        If multiple keys are specified, listings are done in parallel. All objects
        returned have `.exists == True` as this call always returns leaf objects.
        
        For instance, if the directory hierarchy is
        ```
        a/0.txt
        a/b/1.txt
        a/c/2.txt
        a/d/e/3.txt
        f/4.txt
        ```
        The `list_paths(['a', 'f'])` call returns
        ```
        a/0.txt (exists == True)
        a/b/1.txt (exists == True)
        a/c/2.txt (exists == True)
        a/d/e/3.txt (exists == True)
        f/4.txt (exists == True)
        ```
        
        Parameters
        ----------
        keys : Iterable[str], optional, default None
            List of paths.
        
        Returns
        -------
        List[S3Object]
            S3Objects under the given paths.
        """
        ...
    def info(self, key: typing.Optional[str] = None, return_missing: bool = False) -> S3Object:
        """
        Get metadata about a single object in S3.
        
        This call makes a single `HEAD` request to S3 which can be
        much faster than downloading all data with `get`.
        
        Parameters
        ----------
        key : str, optional, default None
            Object to query. It can be an S3 url or a path suffix.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        
        Returns
        -------
        S3Object
            An S3Object corresponding to the object requested. The object
            will have `.downloaded == False`.
        """
        ...
    def info_many(self, keys: typing.Iterable[str], return_missing: bool = False) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get metadata about many objects in S3 in parallel.
        
        This call makes a single `HEAD` request to S3 which can be
        much faster than downloading all data with `get`.
        
        Parameters
        ----------
        keys : Iterable[str]
            Objects to query. Each key can be an S3 url or a path suffix.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        
        Returns
        -------
        List[S3Object]
            A list of S3Objects corresponding to the paths requested. The
            objects will have `.downloaded == False`.
        """
        ...
    def get(self, key: typing.Union[str, metaflow.plugins.datatools.s3.s3.S3GetObject, None] = None, return_missing: bool = False, return_info: bool = True) -> S3Object:
        """
        Get a single object from S3.
        
        Parameters
        ----------
        key : Union[str, S3GetObject], optional, default None
            Object to download. It can be an S3 url, a path suffix, or
            an S3GetObject that defines a range of data to download. If None, or
            not provided, gets the S3 root.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        return_info : bool, default True
            If set to True, fetch the content-type and user metadata associated
            with the object at no extra cost, included for symmetry with `get_many`
        
        Returns
        -------
        S3Object
            An S3Object corresponding to the object requested.
        """
        ...
    def get_many(self, keys: typing.Iterable[typing.Union[str, metaflow.plugins.datatools.s3.s3.S3GetObject]], return_missing: bool = False, return_info: bool = True) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get many objects from S3 in parallel.
        
        Parameters
        ----------
        keys : Iterable[Union[str, S3GetObject]]
            Objects to download. Each object can be an S3 url, a path suffix, or
            an S3GetObject that defines a range of data to download.
        return_missing : bool, default False
            If set to True, do not raise an exception for a missing key but
            return it as an `S3Object` with `.exists == False`.
        return_info : bool, default True
            If set to True, fetch the content-type and user metadata associated
            with the object at no extra cost, included for symmetry with `get_many`.
        
        Returns
        -------
        List[S3Object]
            S3Objects corresponding to the objects requested.
        """
        ...
    def get_recursive(self, keys: typing.Iterable[str], return_info: bool = False) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get many objects from S3 recursively in parallel.
        
        Parameters
        ----------
        keys : Iterable[str]
            Prefixes to download recursively. Each prefix can be an S3 url or a path suffix
            which define the root prefix under which all objects are downloaded.
        return_info : bool, default False
            If set to True, fetch the content-type and user metadata associated
            with the object.
        
        Returns
        -------
        List[S3Object]
            S3Objects stored under the given prefixes.
        """
        ...
    def get_all(self, return_info: bool = False) -> typing.List[metaflow.plugins.datatools.s3.s3.S3Object]:
        """
        Get all objects under the prefix set in the `S3` constructor.
        
        This method requires that the `S3` object is initialized either with `run` or
        `s3root`.
        
        Parameters
        ----------
        return_info : bool, default False
            If set to True, fetch the content-type and user metadata associated
            with the object.
        
        Returns
        -------
        Iterable[S3Object]
            S3Objects stored under the main prefix.
        """
        ...
    def put(self, key: typing.Union[str, metaflow.plugins.datatools.s3.s3.S3PutObject], obj: typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes], overwrite: bool = True, content_type: typing.Optional[str] = None, metadata: typing.Optional[typing.Dict[str, str]] = None) -> str:
        """
        Upload a single object to S3.
        
        Parameters
        ----------
        key : Union[str, S3PutObject]
            Object path. It can be an S3 url or a path suffix.
        obj : PutValue
            An object to store in S3. Strings are converted to UTF-8 encoding.
        overwrite : bool, default True
            Overwrite the object if it exists. If set to False, the operation
            succeeds without uploading anything if the key already exists.
        content_type : str, optional, default None
            Optional MIME type for the object.
        metadata : Dict[str, str], optional, default None
            A JSON-encodable dictionary of additional headers to be stored
            as metadata with the object.
        
        Returns
        -------
        str
            URL of the object stored.
        """
        ...
    def put_many(self, key_objs: typing.List[typing.Union[typing.Tuple[str, typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes]], metaflow.plugins.datatools.s3.s3.S3PutObject]], overwrite: bool = True) -> typing.List[typing.Tuple[str, str]]:
        """
        Upload many objects to S3.
        
        Each object to be uploaded can be specified in two ways:
        
        1. As a `(key, obj)` tuple where `key` is a string specifying
           the path and `obj` is a string or a bytes object.
        
        2. As a `S3PutObject` which contains additional metadata to be
           stored with the object.
        
        Parameters
        ----------
        key_objs : List[Union[Tuple[str, PutValue], S3PutObject]]
            List of key-object pairs to upload.
        overwrite : bool, default True
            Overwrite the object if it exists. If set to False, the operation
            succeeds without uploading anything if the key already exists.
        
        Returns
        -------
        List[Tuple[str, str]]
            List of `(key, url)` pairs corresponding to the objects uploaded.
        """
        ...
    def put_files(self, key_paths: typing.List[typing.Union[typing.Tuple[str, typing.Union[io.RawIOBase, io.BufferedIOBase, str, bytes]], metaflow.plugins.datatools.s3.s3.S3PutObject]], overwrite: bool = True) -> typing.List[typing.Tuple[str, str]]:
        """
        Upload many local files to S3.
        
        Each file to be uploaded can be specified in two ways:
        
        1. As a `(key, path)` tuple where `key` is a string specifying
           the S3 path and `path` is the path to a local file.
        
        2. As a `S3PutObject` which contains additional metadata to be
           stored with the file.
        
        Parameters
        ----------
        key_paths :  List[Union[Tuple[str, PutValue], S3PutObject]]
            List of files to upload.
        overwrite : bool, default True
            Overwrite the object if it exists. If set to False, the operation
            succeeds without uploading anything if the key already exists.
        
        Returns
        -------
        List[Tuple[str, str]]
            List of `(key, url)` pairs corresponding to the files uploaded.
        """
        ...
    ...

