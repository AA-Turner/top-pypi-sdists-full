######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.31                                                                                #
# Generated on 2026-06-01T01:50:49.556920                                                            #
######################################################################################################

from __future__ import annotations

import typing


class ClassPath_Trie(object, metaclass=type):
    def __init__(self):
        ...
    def init(self, initial_nodes: typing.Union[typing.List[typing.Tuple[str, type]], None] = None):
        ...
    def insert(self, classpath_name: str, value: type):
        ...
    def search(self, classpath_name: str) -> typing.Union[type, None]:
        ...
    def remove(self, classpath_name: str):
        ...
    def unique_prefix_value(self, classpath_name: str) -> typing.Union[type, None]:
        ...
    def unique_prefix_for_type(self, value: type) -> typing.Union[str, None]:
        ...
    def get_unique_prefixes(self) -> typing.Dict[str, type]:
        """
        Get all unique prefixes in the trie.
        
        Returns
        -------
        List[str]
            A list of unique prefixes.
        """
        ...
    ...

