"""FE module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v261.Ansys.ACT.Automation.Mechanical.FE.CDB as CDB
import ansys.mechanical.stubs.v261.Ansys.ACT.Automation.Mechanical.FE.ABAQUS as ABAQUS
import ansys.mechanical.stubs.v261.Ansys.ACT.Automation.Mechanical.FE.NASTRAN as NASTRAN


class CommandsType(Enum):
    """
    
            Commands type.
            
    """

    Processed = 1
    UnProcessed = 2
    All = 3

class CommandColl(object):
    """
    
            Collection of commands.
            
    """

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the count of commands.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Common.Interop.FECommandsModel.ICommand]:
        """
        Item property.
        """
        return None

    def __init__(self, iCommandColl: Ansys.Common.Interop.FECommandsModel.ICommandColl, commandRepository: Ansys.ACT.Automation.Mechanical.FE.CommandRepository) -> None:
        """
        __init__ method.
        """
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Common.Interop.FECommandsModel.ICommand]:
        """
        GetEnumerator method.
        """
        pass


class CommandRepository(object):
    """
    
            Command repository.
            
    """

    def __init__(self, iCommandRepository: Ansys.Common.Interop.FECommandsModel.ICommandRepository) -> None:
        """
        __init__ method.
        """
        pass

    def GetCommandsByName(self, name: str) -> Ansys.ACT.Automation.Mechanical.FE.CommandColl:
        """
        Gets the commands by name.
        """
        pass

    def GetCommandByIndex(self, index: int) -> Ansys.Common.Interop.FECommandsModel.ICommand:
        """
        Gets the commands by index.
        """
        pass

    def GetCommandNamesCount(self, eCommandsType: Ansys.ACT.Automation.Mechanical.FE.CommandsType) -> int:
        """
        Gets the number of commands of a type specified by param=eCommandsType in the repository.
        """
        pass

    def GetCommandName(self, eCommandsType: Ansys.ACT.Automation.Mechanical.FE.CommandsType, index: int) -> str:
        """
        Gets the name of commands of a type specified by params eCommandsType and index in the repository.
        """
        pass

    def GetCommandNames(self, eCommandsType: Ansys.ACT.Automation.Mechanical.FE.CommandsType) -> tuple[str]:
        """
        Gets the command names of a type specified by params eCommandsType and index in the repository.
        """
        pass


class Command(object):
    """
    
            Base class for all Commands.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def FullName(self) -> typing.Optional[str]:
        """
        FullName property.
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCommand: Ansys.Common.Interop.FECommandsModel.ICommand) -> None:
        """
        __init__ method.
        """
        pass


class FEParser(object):
    """
    
            FE parser object.
            
    """

    def __init__(self) -> None:
        """
        
            Default constructor.
            
        """
        pass

    def Parse(self, filename: str, format: str) -> Ansys.ACT.Automation.Mechanical.FE.CommandRepository:
        """
        Parse method.
        """
        pass


