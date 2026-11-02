"""Application module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class Progress(object):
    """
    Defines a Progress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.AnsCoreObjects.IAnsProgress]:
        """
        InternalObject property.
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    def add_OnStopped(self, value: System.EventHandler) -> None:
        """
        add_OnStopped method.
        """
        pass

    def remove_OnStopped(self, value: System.EventHandler) -> None:
        """
        remove_OnStopped method.
        """
        pass

    def SetProgress(self, uiProgress: int, uiMessage: str, uiSubProgress: int, uiSubMessage: str) -> None:
        """
        Set the current progress state
        """
        pass


class ObjectTag(object):
    """
    
            An instance of an ObjectTag.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the tag. If the tag exists in ObjectTags, attempting to set the name to a value of another tag in that collection will lead to an exception.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the tag. If the tag exists in ObjectTags, attempting to set the name to a value of another tag in that collection will lead to an exception.
            
        """
        pass

    @property
    def Objects(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        
            The list of objects which use this tag.
            
        """
        return None

    def __init__(self, name: str) -> None:
        """
        
            Creates a new tag with the given name
            
        """
        pass

    def AddObject(self, obj: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        """
        
            Add an object to this tag.
            
        """
        pass

    def RemoveObject(self, obj: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        """
        
            Remove an object from this tag.
            
        """
        pass

    def ClearObjects(self) -> None:
        """
        
            Clear all objects from this tag.
            
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class ObjectTags(object):
    """
    
            Defines the collection of Mechanical’s tags.
            
    """

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            The number of tags in the collection.
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        """
        IsReadOnly property.
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Application.ObjectTag]:
        """
        Item property.
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Application.ObjectTag]:
        """
        Item property.
        """
        return None

    @property
    def TagNames(self) -> typing.Optional[typing.List[str]]:
        """
        
            The names of the tags in the collection.
            
        """
        return None

    def __init__(self, project: Ansys.ACT.Automation.Mechanical.Project) -> None:
        """
        __init__ method.
        """
        pass

    def Add(self, tag: Ansys.Mechanical.Application.ObjectTag) -> None:
        """
        
            Adds a new tag to the collection. Throws an error if the tag already exists in the collection.
            
        """
        pass

    @typing.overload
    def Remove(self, tag: Ansys.Mechanical.Application.ObjectTag) -> bool:
        ...

    @typing.overload
    def Remove(self, tagName: str) -> bool:
        ...

    def Remove(self, *args: typing.Any) -> bool:
        """
        
            Removes a tag if it exists in the collection.
            
        """
        pass

    def GetTag(self, tagName: str) -> Ansys.Mechanical.Application.ObjectTag:
        """
        
            Returns the tag in the collection with the given name.
            
        """
        pass

    def GetEnumerator(self) -> Ansys.Mechanical.Application.TagObjects:
        """
        GetEnumerator method.
        """
        pass

    def IndexOf(self, tag: Ansys.Mechanical.Application.ObjectTag) -> int:
        """
        
            Returns the index of the given tag. If the given tag does not exist in the collection, returns -1.
            
        """
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the tag at the given index from the collection.
            
        """
        pass

    def Clear(self) -> None:
        """
        
            Clears the collection, removing all objects from the tags in the collection.
            
        """
        pass

    @typing.overload
    def Contains(self, tag: Ansys.Mechanical.Application.ObjectTag) -> bool:
        ...

    @typing.overload
    def Contains(self, tagName: str) -> bool:
        ...

    def Contains(self, *args: typing.Any) -> bool:
        """
        
            Returns whether or not the collection contains the given tag.
            
        """
        pass

    def CopyTo(self, array: Ansys.Mechanical.Application.ObjectTag, arrayIndex: int) -> None:
        """
        CopyTo method.
        """
        pass


class Message(object):
    """
    
            A message.
            
    """

    @property
    def Source(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        
            The source object of the message.
            
        """
        return None

    @Source.setter
    def Source(self, value: typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        """
        
            The source object of the message.
            
        """
        pass

    @property
    def StringID(self) -> typing.Optional[str]:
        """
        
            The string ID of the message.
            
        """
        return None

    @StringID.setter
    def StringID(self, value: typing.Optional[str]) -> None:
        """
        
            The string ID of the message.
            
        """
        pass

    @property
    def DisplayString(self) -> typing.Optional[str]:
        """
        
            The display string of the message.
            
        """
        return None

    @property
    def Location(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        
            The location of the message.
            
        """
        return None

    @property
    def TimeStamp(self) -> typing.Optional[typing.Any]:
        """
        
            The timestamp of the message.
            
        """
        return None

    @property
    def RelatedObjects(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        
            The list of objects related to the message.
            
        """
        return None

    @property
    def Severity(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MessageSeverityType]:
        """
        
            The severity of the message.
            
        """
        return None

    @Severity.setter
    def Severity(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MessageSeverityType]) -> None:
        """
        
            The severity of the message.
            
        """
        pass

    @property
    def MessageVisibility(self) -> typing.Optional[bool]:
        """
        MessageVisibility property.
        """
        return None

    def __init__(self, text: str, severity: Ansys.Mechanical.DataModel.Enums.MessageSeverityType) -> None:
        """
        
            Creates a new message with the given message and severity.
            
        """
        pass

    def Equals(self, other: Ansys.Mechanical.Application.Message) -> bool:
        """
        Equals method.
        """
        pass


class Messages(object):
    """
    
            Defines the collection of Mechanical's messages.
            
    """

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Get the number of messages.
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        """
        IsReadOnly property.
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Application.Message]:
        """
        Item property.
        """
        return None

    @property
    def AllVisibleMessages(self) -> typing.Optional[typing.List[Ansys.Mechanical.Application.Message]]:
        """
        AllVisibleMessages property.
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def add_OnAddMessage(cls, value: System.EventHandler[Ansys.Mechanical.Application.Message]) -> None:
        """
        add_OnAddMessage method.
        """
        pass

    @classmethod
    def remove_OnAddMessage(cls, value: System.EventHandler[Ansys.Mechanical.Application.Message]) -> None:
        """
        remove_OnAddMessage method.
        """
        pass

    def Add(self, item: Ansys.Mechanical.Application.Message) -> None:
        """
        
            Add a new message.
            
        """
        pass

    def Remove(self, item: Ansys.Mechanical.Application.Message) -> bool:
        """
        
            Remove a specific message in the list.
            
        """
        pass

    def Clear(self) -> None:
        """
        
            Clear the list of the messages.
            
        """
        pass

    def Contains(self, item: Ansys.Mechanical.Application.Message) -> bool:
        """
        
            Check if a message is in the current list of messages.
            
        """
        pass

    @classmethod
    def OnAddMessageFwd(cls, sender: typing.Any, args: typing.Any) -> None:
        """
        OnAddMessageFwd method.
        """
        pass

    def GetEnumerator(self) -> Ansys.Mechanical.Application.MessageList:
        """
        GetEnumerator method.
        """
        pass

    def CopyTo(self, array: Ansys.Mechanical.Application.Message, arrayIndex: int) -> None:
        """
        CopyTo method.
        """
        pass

    def ShowErrors(self) -> None:
        """
        
            Shows errors with current project.
            
        """
        pass

    def HideErrorMessages(self) -> None:
        """
        HideErrorMessages method.
        """
        pass

    def ShowErrorMessages(self) -> None:
        """
        ShowErrorMessages method.
        """
        pass

    def CountErrorMessages(self) -> int:
        """
        CountErrorMessages method.
        """
        pass

    def HideWarningMessages(self) -> None:
        """
        HideWarningMessages method.
        """
        pass

    def ShowWarningMessages(self) -> None:
        """
        ShowWarningMessages method.
        """
        pass

    def CountWarningMessages(self) -> int:
        """
        CountWarningMessages method.
        """
        pass

    def HideInfoMessages(self) -> None:
        """
        HideInfoMessages method.
        """
        pass

    def ShowInfoMessages(self) -> None:
        """
        ShowInfoMessages method.
        """
        pass

    def CountInfoMessages(self) -> int:
        """
        CountInfoMessages method.
        """
        pass

    def MergeMessages(self) -> None:
        """
        MergeMessages method.
        """
        pass

    def UnmergeMessages(self) -> None:
        """
        UnmergeMessages method.
        """
        pass

    def ShowPopUps(self) -> None:
        """
        ShowPopUps method.
        """
        pass

    def HidePopUps(self) -> None:
        """
        HidePopUps method.
        """
        pass


