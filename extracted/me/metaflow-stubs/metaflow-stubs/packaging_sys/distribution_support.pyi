######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.36                                                                                #
# Generated on 2026-08-05T18:17:36.292093                                                            #
######################################################################################################

from __future__ import annotations

import typing
import abc
import importlib
if typing.TYPE_CHECKING:
    import importlib.metadata
    import abc
    import os


TYPE_CHECKING: bool

def modules_to_distributions() -> typing.Dict[str, typing.List[importlib.metadata.Distribution]]:
    """
    Return a mapping of top-level modules to their distributions.
    
    Returns
    -------
    Dict[str, List[metadata.Distribution]]
        A mapping of top-level modules to their distributions.
    """
    ...

class PackagedDistribution(importlib.metadata.Distribution, metaclass=type):
    """
    A Python Package packaged within a MetaflowCodeContent. This allows users to use use importlib
    as they would regularly and the packaged Python Package would be considered as a
    distribution even if it really isn't (since it is just included in the PythonPath).
    """
    def __init__(self, root: str, content: typing.Dict[str, str]):
        ...
    def read_text(self, filename: typing.Union[str, os.PathLike]) -> typing.Union[str, None]:
        """
        Attempt to load metadata file given by the name.
        
        Python distribution metadata is organized by blobs of text
        typically represented as "files" in the metadata directory
        (e.g. package-1.0.dist-info). These files include things
        like:
        
        - METADATA: The distribution metadata including fields
          like Name and Version and Description.
        - entry_points.txt: A series of entry points as defined in
          `the entry points spec <https://packaging.python.org/en/latest/specifications/entry-points/#file-format>`_.
        - RECORD: A record of files according to
          `this recording spec <https://packaging.python.org/en/latest/specifications/recording-installed-packages/#the-record-file>`_.
        
        A package may provide any set of files, including those
        not listed here or none at all.
        
        :param filename: The name of the file in the distribution info.
        :return: The text if found, otherwise None.
        """
        ...
    def locate_file(self, path: typing.Union[str, os.PathLike]):
        ...
    ...

class PackagedDistributionFinder(importlib.metadata.DistributionFinder, metaclass=abc.ABCMeta):
    def __init__(self, dist_info: typing.Dict[str, typing.Dict[str, str]]):
        ...
    def find_distributions(self, context = ...):
        ...
    ...

