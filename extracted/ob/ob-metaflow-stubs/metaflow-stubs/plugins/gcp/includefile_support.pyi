######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.920540                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import MetaflowException as MetaflowException
from ...exception import MetaflowInternalError as MetaflowInternalError

class GS(object, metaclass=type):
    @classmethod
    def get_root_from_config(cls, echo, create_on_absent = True):
        ...
    def __init__(self):
        ...
    def __enter__(self):
        ...
    def __exit__(self, *args):
        ...
    def get(self, key = None, return_missing = False):
        """
        Key MUST be a fully qualified path.  gs://<bucket_name>/b/l/o/b/n/a/m/e
        """
        ...
    def put(self, key, obj, overwrite = True):
        """
        Key MUST be a fully qualified path.  gs://<bucket_name>/b/l/o/b/n/a/m/e
        """
        ...
    def info(self, key = None, return_missing = False):
        ...
    ...

class GSObject(object, metaclass=type):
    def __init__(self, url, path, exists, size):
        ...
    @property
    def path(self):
        ...
    @property
    def url(self):
        ...
    @property
    def exists(self):
        ...
    @property
    def size(self):
        ...
    ...

