######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.916249                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

DATATOOLS_LOCALROOT: None

DATATOOLS_SUFFIX: str

class MetaflowLocalURLException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowLocalNotFound(metaflow.exception.MetaflowException, metaclass=type):
    ...

class LocalObject(object, metaclass=type):
    """
    This object represents a local object. It is a very thin wrapper
    to allow it to be used in the same way as the S3Object (only as needed
    in the IncludeFile use case)
    
    Get or list calls return one or more of LocalObjects.
    """
    def __init__(self, url, path):
        ...
    @property
    def exists(self):
        """
        Does this key correspond to an actual file?
        """
        ...
    @property
    def url(self):
        """
        Local location of the object; this is the path prefixed with local://
        """
        ...
    @property
    def path(self):
        """
        Path to the local file
        """
        ...
    @property
    def size(self):
        """
        Size of the local file (in bytes)
        
        Returns None if the key does not correspond to an actual object
        """
        ...
    ...

class Local(object, metaclass=type):
    """
    This class allows you to access the local filesystem in a way similar to the S3 datatools
    client. It is a stripped down version for now and only implements the functionality needed
    for this use case.
    
    In the future, we may want to allow it to be used in a way similar to the S3() client.
    """
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __init__(self):
        """
        Initialize a new context for Local file operations. This object is based used as
        a context manager for a with statement.
        """
        ...
    def __enter__(self):
        ...
    def __exit__(self, *args):
        ...
    def get(self, key = None, return_missing = False):
        ...
    def put(self, key, obj, overwrite = True):
        ...
    def info(self, key = None, return_missing = False):
        ...
    ...

