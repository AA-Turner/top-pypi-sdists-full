"""NASTRAN module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class NASTRANCommand(object):

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


class GenericCommand(object):
    """
    
            Generic command.
            
    """

    @property
    def Arguments(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the arguments.
            
        """
        return None

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

    def __init__(self, iGenericCommand: Ansys.Common.Interop.FEParsePlugin_NASTRAN.INastranCommand) -> None:
        """
        __init__ method.
        """
        pass


class CaseControlCommand(object):
    """
    
            Case control command.
            
    """

    @property
    def Text(self) -> typing.Optional[str]:
        """
        
            Gets the text.
            
        """
        return None

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

    def __init__(self, iCaseControlCommand: Ansys.Common.Interop.FEParsePlugin_NASTRAN.ICaseControlCommand) -> None:
        """
        __init__ method.
        """
        pass


class NastranOption(object):
    """
    
            Option.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the option name.
            
        """
        return None

    @property
    def Value(self) -> typing.Optional[str]:
        """
        
            Gets the value.
            
        """
        return None

    def __init__(self, name: str, value: str) -> None:
        """
        __init__ method.
        """
        pass


class NastranOptionLine(object):
    """
    
            Option line.
            
    """

    @property
    def Options(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.NASTRAN.NastranOption]]:
        """
        
            Gets the options.
            
        """
        return None

    def __init__(self, options: typing.List[Ansys.ACT.Automation.Mechanical.FE.NASTRAN.NastranOption]) -> None:
        """
        __init__ method.
        """
        pass


class OptionsControlCommand(object):
    """
    
            Options control command.
            
    """

    @property
    def Arguments(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the arguments.
            
        """
        return None

    @property
    def OptionLines(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the option lines.
            
        """
        return None

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

    def __init__(self, iOptionsControlCommand: Ansys.Common.Interop.FEParsePlugin_NASTRAN.IOptionsControlCommand) -> None:
        """
        __init__ method.
        """
        pass


