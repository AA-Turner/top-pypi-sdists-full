"""Interfaces module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class IDataModelObject(object):

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        InternalObject property.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the name of the current DataModelObject's category.
        """
        return None

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        Gets the internal id of the object.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        Gets the name of the object.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Gets the parent object.
        """
        return None

    @property
    def GroupingFolder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GroupingFolder property.
        """
        return None

    @property
    def ObjectState(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ObjectState]:
        """
        ObjectState property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IObjectTag]]:
        """
        
            Gets an IEnumerable object of the tags that 'this' is a part of.
            
        """
        return None

    def GetPath(self) -> str:
        """
        Gets the path of the object.
        """
        pass

    def Accept(self, visitor: Ansys.Mechanical.DataModel.Interfaces.IDataModelObjectVisitor) -> None:
        """
        Accept method.
        """
        pass

    def Equals(self, other: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> bool:
        """
        Equals method.
        """
        pass


class DataModelObject(IDataModelObject):
    pass
