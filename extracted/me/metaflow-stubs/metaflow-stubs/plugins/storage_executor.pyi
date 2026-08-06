######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.36                                                                                #
# Generated on 2026-08-05T18:17:36.305454                                                            #
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

