"""Utilities module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class AttributeCollection(object):
    """
    
            A collection of attributes.
            
    """

    @property
    def Item(self) -> typing.Optional[typing.Any]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[typing.Any]) -> None:
        """
        Item property.
        """
        pass

    @property
    def Keys(self) -> typing.Optional[System.Collections.Generic.ICollection[str]]:
        """
        
            The list of the available keys in the collection.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @typing.overload
    def GetValue(self, name: str, defaultValue: typing.Any) -> typing.Any:
        ...

    @typing.overload
    def GetValue(self, name: str) -> typing.Any:
        ...

    def GetValue(self, *args: typing.Any) -> typing.Any:
        """
        
            Gets an attribute value by its name.
            
        """
        pass

    def GetStringValue(self, name: str) -> str:
        """
        
            Gets an attribute value by its name.
            
        """
        pass

    def SetValue(self, name: str, value: typing.Any) -> None:
        """
        
            Set an attribute value.
            
        """
        pass

    def Remove(self, name: str) -> bool:
        """
        
            Remove an attribute. The attribute cannot be removed if it was declared as
            static attribute.
            
        """
        pass

    def Contains(self, name: str) -> bool:
        """
        
            Check if the collection contains an attribute.
            
        """
        pass

    def Clone(self) -> Ansys.ACT.Core.Utilities.AttributeCollection:
        """
        
            Create a clone of the currection collection.
            
        """
        pass

    def FillDynamicAttributes(self, other: Ansys.ACT.Core.Utilities.AttributeCollection) -> None:
        """
        
            Fill the dynamic attributes of the collection with the given 
            AttributeCollection.
            
        """
        pass

    def FillStaticAttributesFromXml(self, dataModel: Ansys.ACT.Core.XmlDataModel.Attributes) -> None:
        """
        
            Fill the static attributes of the collection with the given XmlNode.
            
        """
        pass

    def GetEnumerator(self) -> typing.Iterator[dict[str,typing.Any]]:
        """
        GetEnumerator method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def PostDeserialization(self) -> None:
        """
        PostDeserialization method.
        """
        pass


class NamedCollection(object):
    """
    
            Represents a collection of INamed objects that could be found by its Name field.
            
    """

    @property
    def Item(self) -> typing.Optional[T]:
        """
        Item property.
        """
        return None

    @property
    def Names(self) -> typing.Optional[System.Collections.ObjectModel.ReadOnlyCollection[str]]:
        """
        Names property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    @property
    def Item(self) -> typing.Optional[T]:
        """
        Item property.
        """
        return None

    def __init__(self, list: typing.List[T]) -> None:
        """
        __init__ method.
        """
        pass

    def Contains(self, value: T) -> bool:
        """
        Contains method.
        """
        pass

    def CopyTo(self, array: T, index: int) -> None:
        """
        CopyTo method.
        """
        pass

    def GetEnumerator(self) -> typing.Iterator[T]:
        """
        GetEnumerator method.
        """
        pass

    def IndexOf(self, value: T) -> int:
        """
        IndexOf method.
        """
        pass


