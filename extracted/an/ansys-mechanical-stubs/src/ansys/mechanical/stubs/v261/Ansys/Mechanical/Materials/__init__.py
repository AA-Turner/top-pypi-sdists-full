"""Materials module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ImportSettings(object):

    @property
    def Replace(self) -> typing.Optional[bool]:
        """
        
            A boolean to specify if a material exists in Mechanical that
            it should be replaced by these imported material(s).
            
        """
        return None

    @Replace.setter
    def Replace(self, value: typing.Optional[bool]) -> None:
        """
        
            A boolean to specify if a material exists in Mechanical that
            it should be replaced by these imported material(s).
            
        """
        pass

    @property
    def Filter(self) -> typing.Optional[typing.List[str]]:
        """
        
            All materials will be imported if this list of the names of
            specific materials to be imported is not specified.
            
        """
        return None

    @Filter.setter
    def Filter(self, value: typing.Optional[typing.List[str]]) -> None:
        """
        
            All materials will be imported if this list of the names of
            specific materials to be imported is not specified.
            
        """
        pass

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


