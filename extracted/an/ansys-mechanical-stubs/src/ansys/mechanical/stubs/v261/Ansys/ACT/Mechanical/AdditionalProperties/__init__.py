"""AdditionalProperties module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class Control(Enum):
    """
    
            The control type for an additional property.
            
    """

    Expression = 64
    Double = 1310720
    ApplyCancel = 131072
    Options = 2097152

class ApplyCancelProperty(object):
    """
    
            Provides a way to create properties with Apply/Cancel buttons.
            
    """

    @property
    def PropertyControl(self) -> typing.Optional[Ansys.ACT.Mechanical.AdditionalProperties.Control]:
        """
        PropertyControl property.
        """
        return None

    @property
    def Type(self) -> typing.Optional[System.UInt16]:
        """
        Type property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the property.
            
        """
        return None

    @property
    def DisplayName(self) -> typing.Optional[str]:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        return None

    @DisplayName.setter
    def DisplayName(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        pass

    @property
    def GroupName(self) -> typing.Optional[str]:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        return None

    @GroupName.setter
    def GroupName(self, value: typing.Optional[str]) -> None:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        pass

    @property
    def Tooltip(self) -> typing.Optional[str]:
        """
        
            The tooltip of the property in the UI.
            
        """
        return None

    @Tooltip.setter
    def Tooltip(self, value: typing.Optional[str]) -> None:
        """
        
            The tooltip of the property in the UI.
            
        """
        pass

    @property
    def ID(self) -> typing.Optional[int]:
        """
        ID property.
        """
        return None

    @ID.setter
    def ID(self, value: typing.Optional[int]) -> None:
        """
        ID property.
        """
        pass

    @property
    def Value(self) -> typing.Optional[typing.Any]:
        """
        
            The stored value of the property.
            
        """
        return None

    @Value.setter
    def Value(self, value: typing.Optional[typing.Any]) -> None:
        """
        
            The stored value of the property.
            
        """
        pass

    @property
    def Access(self) -> typing.Optional[Ansys.Common.Interop.WBPropertyBrowsing.AnsPropertyAccess]:
        """
        Access property.
        """
        return None

    @property
    def Tag(self) -> typing.Optional[typing.Any]:
        """
        Tag property.
        """
        return None

    @Tag.setter
    def Tag(self, value: typing.Optional[typing.Any]) -> None:
        """
        Tag property.
        """
        pass

    @property
    def Owner(self) -> typing.Optional[typing.Any]:
        """
        Owner property.
        """
        return None

    @Owner.setter
    def Owner(self, value: typing.Optional[typing.Any]) -> None:
        """
        Owner property.
        """
        pass

    @property
    def ValueString(self) -> typing.Optional[str]:
        """
        
            Get the string representation of the value.
            
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is readonly.
            
        """
        return None

    @property
    def Valid(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is valid.
            
        """
        return None

    def __init__(self, name: str, groupName: str) -> None:
        """
        __init__ method.
        """
        pass

    def add_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnBeforePropertyChanged method.
        """
        pass

    def remove_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnBeforePropertyChanged method.
        """
        pass

    def add_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnAfterPropertyChanged method.
        """
        pass

    def remove_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnAfterPropertyChanged method.
        """
        pass

    def Resume(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        Resume method.
        """
        pass

    def CopyFrom(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        CopyFrom method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass


class DoubleProperty(object):
    """
    
            Provides a way to create properties that can hold double type values.
            
    """

    @property
    def ValidRange(self) -> typing.Optional[tuple]:
        """
        
            Tuple that can be used to control the upper and lower bounds of a double property.
            
        """
        return None

    @ValidRange.setter
    def ValidRange(self, value: typing.Optional[tuple]) -> None:
        """
        
            Tuple that can be used to control the upper and lower bounds of a double property.
            
        """
        pass

    @property
    def PropertyControl(self) -> typing.Optional[Ansys.ACT.Mechanical.AdditionalProperties.Control]:
        """
        PropertyControl property.
        """
        return None

    @property
    def Type(self) -> typing.Optional[System.UInt16]:
        """
        Type property.
        """
        return None

    @property
    def CanParameterize(self) -> typing.Optional[bool]:
        """
        CanParameterize property.
        """
        return None

    @CanParameterize.setter
    def CanParameterize(self, value: typing.Optional[bool]) -> None:
        """
        CanParameterize property.
        """
        pass

    @property
    def IsParameterized(self) -> typing.Optional[bool]:
        """
        IsParameterized property.
        """
        return None

    @IsParameterized.setter
    def IsParameterized(self, value: typing.Optional[bool]) -> None:
        """
        IsParameterized property.
        """
        pass

    @property
    def ParameterType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ParameterType]:
        """
        ParameterType property.
        """
        return None

    @ParameterType.setter
    def ParameterType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ParameterType]) -> None:
        """
        ParameterType property.
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the property.
            
        """
        return None

    @property
    def DisplayName(self) -> typing.Optional[str]:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        return None

    @DisplayName.setter
    def DisplayName(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        pass

    @property
    def GroupName(self) -> typing.Optional[str]:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        return None

    @GroupName.setter
    def GroupName(self, value: typing.Optional[str]) -> None:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        pass

    @property
    def Tooltip(self) -> typing.Optional[str]:
        """
        
            The tooltip of the property in the UI.
            
        """
        return None

    @Tooltip.setter
    def Tooltip(self, value: typing.Optional[str]) -> None:
        """
        
            The tooltip of the property in the UI.
            
        """
        pass

    @property
    def ID(self) -> typing.Optional[int]:
        """
        ID property.
        """
        return None

    @ID.setter
    def ID(self, value: typing.Optional[int]) -> None:
        """
        ID property.
        """
        pass

    @property
    def Value(self) -> typing.Optional[typing.Any]:
        """
        
            The stored value of the property.
            
        """
        return None

    @Value.setter
    def Value(self, value: typing.Optional[typing.Any]) -> None:
        """
        
            The stored value of the property.
            
        """
        pass

    @property
    def Access(self) -> typing.Optional[Ansys.Common.Interop.WBPropertyBrowsing.AnsPropertyAccess]:
        """
        Access property.
        """
        return None

    @property
    def Tag(self) -> typing.Optional[typing.Any]:
        """
        Tag property.
        """
        return None

    @Tag.setter
    def Tag(self, value: typing.Optional[typing.Any]) -> None:
        """
        Tag property.
        """
        pass

    @property
    def Owner(self) -> typing.Optional[typing.Any]:
        """
        Owner property.
        """
        return None

    @Owner.setter
    def Owner(self, value: typing.Optional[typing.Any]) -> None:
        """
        Owner property.
        """
        pass

    @property
    def ValueString(self) -> typing.Optional[str]:
        """
        
            Get the string representation of the value.
            
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is readonly.
            
        """
        return None

    @property
    def Valid(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is valid.
            
        """
        return None

    @typing.overload
    def __init__(self, name: str, groupName: str) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Resume(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        Resume method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def add_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnBeforePropertyChanged method.
        """
        pass

    def remove_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnBeforePropertyChanged method.
        """
        pass

    def add_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnAfterPropertyChanged method.
        """
        pass

    def remove_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnAfterPropertyChanged method.
        """
        pass

    def CopyFrom(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        CopyFrom method.
        """
        pass


class ExpressionProperty(object):
    """
    
            Provides a way to create properties that can hold expressions.
            
    """

    @property
    def PropertyControl(self) -> typing.Optional[Ansys.ACT.Mechanical.AdditionalProperties.Control]:
        """
        PropertyControl property.
        """
        return None

    @property
    def Type(self) -> typing.Optional[System.UInt16]:
        """
        Type property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the property.
            
        """
        return None

    @property
    def DisplayName(self) -> typing.Optional[str]:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        return None

    @DisplayName.setter
    def DisplayName(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        pass

    @property
    def GroupName(self) -> typing.Optional[str]:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        return None

    @GroupName.setter
    def GroupName(self, value: typing.Optional[str]) -> None:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        pass

    @property
    def Tooltip(self) -> typing.Optional[str]:
        """
        
            The tooltip of the property in the UI.
            
        """
        return None

    @Tooltip.setter
    def Tooltip(self, value: typing.Optional[str]) -> None:
        """
        
            The tooltip of the property in the UI.
            
        """
        pass

    @property
    def ID(self) -> typing.Optional[int]:
        """
        ID property.
        """
        return None

    @ID.setter
    def ID(self, value: typing.Optional[int]) -> None:
        """
        ID property.
        """
        pass

    @property
    def Value(self) -> typing.Optional[typing.Any]:
        """
        
            The stored value of the property.
            
        """
        return None

    @Value.setter
    def Value(self, value: typing.Optional[typing.Any]) -> None:
        """
        
            The stored value of the property.
            
        """
        pass

    @property
    def Access(self) -> typing.Optional[Ansys.Common.Interop.WBPropertyBrowsing.AnsPropertyAccess]:
        """
        Access property.
        """
        return None

    @property
    def Tag(self) -> typing.Optional[typing.Any]:
        """
        Tag property.
        """
        return None

    @Tag.setter
    def Tag(self, value: typing.Optional[typing.Any]) -> None:
        """
        Tag property.
        """
        pass

    @property
    def Owner(self) -> typing.Optional[typing.Any]:
        """
        Owner property.
        """
        return None

    @Owner.setter
    def Owner(self, value: typing.Optional[typing.Any]) -> None:
        """
        Owner property.
        """
        pass

    @property
    def ValueString(self) -> typing.Optional[str]:
        """
        
            Get the string representation of the value.
            
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is readonly.
            
        """
        return None

    @property
    def Valid(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is valid.
            
        """
        return None

    def __init__(self, name: str, groupName: str) -> None:
        """
        __init__ method.
        """
        pass

    def add_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnBeforePropertyChanged method.
        """
        pass

    def remove_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnBeforePropertyChanged method.
        """
        pass

    def add_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnAfterPropertyChanged method.
        """
        pass

    def remove_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnAfterPropertyChanged method.
        """
        pass

    def Resume(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        Resume method.
        """
        pass

    def CopyFrom(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        CopyFrom method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass


class OptionsProperty(object):
    """
    
            Provides a way to create properties that show up as a drop down in the UI.
            
    """

    @property
    def PropertyControl(self) -> typing.Optional[Ansys.ACT.Mechanical.AdditionalProperties.Control]:
        """
        PropertyControl property.
        """
        return None

    @property
    def Options(self) -> typing.Optional[dict[typing.Any,typing.Any]]:
        """
        
            Options shown in the drop-down, represented by a dictionary of int -> string.
            Where the int represents the option, and string represents string shown in the UI.
            When an option is selected the Value property of the property is set to to the option int.
            
        """
        return None

    @Options.setter
    def Options(self, value: typing.Optional[dict[typing.Any,typing.Any]]) -> None:
        """
        
            Options shown in the drop-down, represented by a dictionary of int -> string.
            Where the int represents the option, and string represents string shown in the UI.
            When an option is selected the Value property of the property is set to to the option int.
            
        """
        pass

    @property
    def Type(self) -> typing.Optional[System.UInt16]:
        """
        Type property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the property.
            
        """
        return None

    @property
    def DisplayName(self) -> typing.Optional[str]:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        return None

    @DisplayName.setter
    def DisplayName(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the property shown in the UI. If not set, the Name property is used.
            
        """
        pass

    @property
    def GroupName(self) -> typing.Optional[str]:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        return None

    @GroupName.setter
    def GroupName(self, value: typing.Optional[str]) -> None:
        """
        
            The group name of the property shown in the UI, and used to separate properties based on group name.
            
        """
        pass

    @property
    def Tooltip(self) -> typing.Optional[str]:
        """
        
            The tooltip of the property in the UI.
            
        """
        return None

    @Tooltip.setter
    def Tooltip(self, value: typing.Optional[str]) -> None:
        """
        
            The tooltip of the property in the UI.
            
        """
        pass

    @property
    def ID(self) -> typing.Optional[int]:
        """
        ID property.
        """
        return None

    @ID.setter
    def ID(self, value: typing.Optional[int]) -> None:
        """
        ID property.
        """
        pass

    @property
    def Value(self) -> typing.Optional[typing.Any]:
        """
        
            The stored value of the property.
            
        """
        return None

    @Value.setter
    def Value(self, value: typing.Optional[typing.Any]) -> None:
        """
        
            The stored value of the property.
            
        """
        pass

    @property
    def Access(self) -> typing.Optional[Ansys.Common.Interop.WBPropertyBrowsing.AnsPropertyAccess]:
        """
        Access property.
        """
        return None

    @property
    def Tag(self) -> typing.Optional[typing.Any]:
        """
        Tag property.
        """
        return None

    @Tag.setter
    def Tag(self, value: typing.Optional[typing.Any]) -> None:
        """
        Tag property.
        """
        pass

    @property
    def Owner(self) -> typing.Optional[typing.Any]:
        """
        Owner property.
        """
        return None

    @Owner.setter
    def Owner(self, value: typing.Optional[typing.Any]) -> None:
        """
        Owner property.
        """
        pass

    @property
    def ValueString(self) -> typing.Optional[str]:
        """
        
            Get the string representation of the value.
            
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is readonly.
            
        """
        return None

    @property
    def Valid(self) -> typing.Optional[bool]:
        """
        
            Returns whether a property is valid.
            
        """
        return None

    def __init__(self, name: str, groupName: str) -> None:
        """
        __init__ method.
        """
        pass

    def add_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnBeforePropertyChanged method.
        """
        pass

    def remove_OnBeforePropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnBeforePropertyChanged method.
        """
        pass

    def add_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        add_OnAfterPropertyChanged method.
        """
        pass

    def remove_OnAfterPropertyChanged(self, value: System.EventHandler[typing.Any]) -> None:
        """
        remove_OnAfterPropertyChanged method.
        """
        pass

    def Resume(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        Resume method.
        """
        pass

    def CopyFrom(self, property: Ansys.ACT.Mechanical.AdditionalProperties.CustomProperty) -> None:
        """
        CopyFrom method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass


