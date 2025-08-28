######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-28T00:53:38.110126                                                            #
######################################################################################################

from __future__ import annotations


from ..exception import MetaflowException as MetaflowException

class StorageExecutor(object, metaclass=type):
    """
    Thin wrapper around a ProcessPoolExecutor, or a ThreadPoolExecutor where
    the former may be unsafe.
    """
    def __init__(self, use_processes = False):
        ...
    def warm_up(self):
        ...
    def submit(self, *args, **kwargs):
        ...
    ...

def handle_executor_exceptions(func):
    """
    Decorator for handling errors that come from an Executor. This decorator should
    only be used on functions where executor errors are possible. I.e. the function
    uses StorageExecutor.
    """
    ...

