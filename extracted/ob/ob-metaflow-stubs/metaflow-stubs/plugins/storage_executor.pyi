######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T00:14:52.308069                                                            #
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

