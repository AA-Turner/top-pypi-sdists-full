"""Load class by it's Fully Qualified Class Path"""

from typing import Mapping, Any, Sequence, Optional
import importlib
import logging

LOGGER = logging.getLogger(__name__)


def get_class(klasspath: str) -> Any:
    """Get the class specified by the given str classpath"""
    klassparts = klasspath.split(".")
    modulename = ".".join(klassparts[:-1])
    klassname = klassparts[-1]
    module = importlib.import_module(modulename)
    klass = getattr(module, klassname)
    return klass


def get_instance(
    klasspath: str, *init_args: Optional[Sequence[Any]], **init_kwargs: Optional[Mapping[str, Any]]
) -> Any:
    """Get an instance of a class with the given init args"""
    klass = get_class(klasspath)
    return klass(*init_args, **init_kwargs)
