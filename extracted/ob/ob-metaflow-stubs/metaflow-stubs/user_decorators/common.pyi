######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-28T00:53:38.098776                                                            #
######################################################################################################

from __future__ import annotations

import typing


class ClassPath_Trie(object, metaclass=type):
    def __init__(self):
        ...
    def init(self, initial_nodes: typing.Optional[typing.List[typing.Tuple[str, type]]] = None):
        ...
    def insert(self, classpath_name: str, value: type):
        ...
    def search(self, classpath_name: str) -> typing.Optional[type]:
        ...
    def remove(self, classpath_name: str):
        ...
    def unique_prefix_value(self, classpath_name: str) -> typing.Optional[type]:
        ...
    def unique_prefix_for_type(self, value: type) -> typing.Optional[str]:
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

