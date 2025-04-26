import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import nodeitems_utils

class SortedNodeCategory(nodeitems_utils.NodeCategory): ...

class CompositorNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class ShaderNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

def register(): ...
def unregister(): ...
