"""Core module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v242.Ansys.ACT.Core.Math as Math
import ansys.mechanical.stubs.v242.Ansys.ACT.Core.Utilities as Utilities
import ansys.mechanical.stubs.v242.Ansys.ACT.Core.Application as Application


class ProcessUtilities(object):
    """
    
            This class exposes process-based utility methods used to run external applications.
            
    """

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @typing.overload
    def Start(self, target: str, args: str) -> int:
        ...

    @typing.overload
    def Start(self, target: str, useShell: bool, args: str) -> int:
        ...

    def Start(self, *args: typing.Any) -> int:
        """
        Start method.
        """
        pass


class ExtensionId(object):
    """
    
            Provides service to uniquely identify the extension.
            
    """

    @property
    def UniqueId(self) -> typing.Optional[str]:
        """
        
            Get the unique id of the extension.
            
        """
        return None

    def __init__(self, identifier: Ansys.ACT.Interop.IDefinitionIdentifier) -> None:
        """
        __init__ method.
        """
        pass


