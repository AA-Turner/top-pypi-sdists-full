"""DataModel module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class IDataModelProvider(object):

    @property
    def DataModel(self) -> typing.Optional[typing.Any]:
        """
        DataModel property.
        """
        return None


