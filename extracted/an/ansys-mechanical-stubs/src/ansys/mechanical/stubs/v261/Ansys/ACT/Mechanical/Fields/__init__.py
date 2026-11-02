"""Fields module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v261.Ansys.ACT.Mechanical.Fields.Adapters as Adapters


class VariableDefinitionType(Enum):
    """
    
            Defines the various ways to define the values of a variable.
            
    """

    Free = 0
    Discrete = 1
    Formula = 2

class Field(object):
    """
    
            Represents a discrete or continuous field that can be used in a component of a boundary condition from Mechanical, for instance.
            
    """

    @property
    def Inputs(self) -> typing.Optional[typing.List[Ansys.ACT.Mechanical.Fields.Variable]]:
        """
        
            Gets the input variables of this component.
            
        """
        return None

    @property
    def Output(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Variable]:
        """
        
            Gets the output variable of this component.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the name of this component.
            
        """
        return None

    @typing.overload
    def ToString(self, isForJournal: bool) -> str:
        ...

    @typing.overload
    def ToString(self) -> str:
        ...

    def ToString(self, *args: typing.Any) -> str:
        """
        ToString method.
        """
        pass


class Range(object):
    """
    
            Represents a domain for real values.
            
    """

    def Equals(self, obj: typing.Any) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class Variable(object):
    """
    
            Represents an object that is either an input or an output for a . Depending on whether it is an input or output and on the way it is defined, this object holds a series of discrete values
            or an expression that may involve other variables.
            
    """

    @property
    def Field(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        
            Gets the owner field.
            
        """
        return None

    @property
    def IsInput(self) -> typing.Optional[bool]:
        """
        
            Gets a value indicating whether this variable is an input for its container field. Otherwise, it is an output variable.
            
        """
        return None

    @property
    def IsOutput(self) -> typing.Optional[bool]:
        """
        
            Gets a value indicating whether this variable is an output for its container field. Otherwise, it is an input variable.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the index of this variable in its container field.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the variable's name.
            
        """
        return None

    @property
    def Range(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Range]:
        """
        
            Gets the domain of validity for variable's value.
            
        """
        return None

    @property
    def DefinitionType(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.VariableDefinitionType]:
        """
        
            Gets a value that indicates how this variable is defined.
            
        """
        return None

    @DefinitionType.setter
    def DefinitionType(self, value: typing.Optional[Ansys.ACT.Mechanical.Fields.VariableDefinitionType]) -> None:
        """
        
            Gets a value that indicates how this variable is defined.
            
        """
        pass

    @property
    def DiscreteValueCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of discrete values of this variable.
            
        """
        return None

    @property
    def DiscreteValues(self) -> typing.Optional[typing.List[Ansys.Core.Units.Quantity]]:
        """
        
            Gets or sets the discrete values of this variable or null if this variable represents a free degree of freedom.
            
        """
        return None

    @DiscreteValues.setter
    def DiscreteValues(self, value: typing.Optional[typing.List[Ansys.Core.Units.Quantity]]) -> None:
        """
        
            Gets or sets the discrete values of this variable or null if this variable represents a free degree of freedom.
            
        """
        pass

    @property
    def MinMaxDiscreteValues(self) -> typing.Optional[tuple[Ansys.Core.Units.Quantity,Ansys.Core.Units.Quantity]]:
        """
        
            Returns a Tuple containing the min and max values from the list of discrete values.
            
        """
        return None

    @property
    def Formula(self) -> typing.Optional[str]:
        """
        
            Gets or sets the expression that is used to defined this variable, or null if the variable is not defined by a function.
            
        """
        return None

    @Formula.setter
    def Formula(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the expression that is used to defined this variable, or null if the variable is not defined by a function.
            
        """
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        
            Gets the symbol of the unit used to express this variable's values.
            
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional[str]:
        """
        
            Gets the name of the quantity represented by this variable.
            
        """
        return None

    def GetDiscreteValue(self, index: int) -> Ansys.Core.Units.Quantity:
        """
        
            Changes a value at a given position in the tabular definition of the variable.
            
        """
        pass

    def SetDiscreteValue(self, index: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Changes a value at a given position in the tabular definition of the variable.
            
        """
        pass

    @typing.overload
    def ToString(self) -> str:
        ...

    @typing.overload
    def ToString(self, isForJournal: bool) -> str:
        ...

    def ToString(self, *args: typing.Any) -> str:
        """
        ToString method.
        """
        pass


