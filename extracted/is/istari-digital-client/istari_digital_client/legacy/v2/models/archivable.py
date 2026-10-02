import abc

import inflection
from pydantic import StrictStr
from typing import TYPE_CHECKING, Optional, Callable

from istari_digital_client.legacy.v2.models.archive import Archive
from istari_digital_client.legacy.v2.models.restore import Restore
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.api.v2_api import V2Api


class Archivable(abc.ABC):
    """
    Abstract mixin class for archivable and restorable resources.

    Classes that inherit from `Archivable` must have an `id` attribute and a `client` attribute
    conforming to the `V2Api` interface. This mixin provides `archive()` and `restore()`
    methods that dynamically dispatch to the appropriate client method based on the class name.

    Intended for use with models like `File`, `Artifact`, `Model`, etc.
    """

    def _require_client(self) -> "V2Api":
        """
        Internal helper to assert that a ``client`` is attached to the instance.

        :raises ValueError: If the ``client`` attribute is not set.
        """

        client = getattr(self, "client", None)
        if client is None:
            raise ValueError(
                f"`client` is not set for instance of {self.__class__.__name__}"
            )
        return client

    @property
    def _id(self) -> StrictStr:
        """
        Retrieve the ``id`` attribute of the instance.

        :raises ValueError: If the ``id`` attribute is not set.
        """

        item_id = getattr(self, "id", None)

        if item_id is None:
            raise ValueError("id is not set")

        return item_id

    @log_method
    def archive(self, archive_reason: Optional[str] = None):
        """
        Archive the current item using the client's archive method for this resource type.

        The method dynamically dispatches based on the class name (e.g., ``archive_model``, ``archive_artifact``).
        An optional archive reason can be provided and will be wrapped in an :class:`Archive` object.

        :param archive_reason: Reason for archiving the item.
        :type archive_reason: str or None
        :raises ValueError: If ``client`` is not set or archiving is not supported for this resource type.
        """

        client = self._require_client()
        reason = Archive(reason=archive_reason) if archive_reason else None
        method_name = f"archive_{inflection.underscore(self.__class__.__name__)}"
        method: Callable[[StrictStr, Optional[Archive]], object] = getattr(
            client, method_name
        )

        try:
            return method(self._id, reason)
        except ValueError:
            raise ValueError(
                f"Cannot archive {self.__class__.__name__} with id {self._id}. Ensure the client is set and the item is archivable."
            )

    @log_method
    def restore(self, restore_reason: Optional[str] = None):
        """
        Restore the current item using the client's restore method for this resource type.

        The method dynamically dispatches based on the class name (e.g., ``restore_model``, ``restore_artifact``).
        An optional restore reason can be provided and will be wrapped in a :class:`Restore` object.

        :param restore_reason: Reason for restoring the item.
        :type restore_reason: str or None
        :raises ValueError: If ``client`` is not set or restoring is not supported for this resource type.
        """

        client = self._require_client()
        reason = Restore(reason=restore_reason) if restore_reason else None
        method_name = f"restore_{inflection.underscore(self.__class__.__name__)}"
        method: Callable[[StrictStr, Optional[Restore]], object] = getattr(
            client, method_name
        )

        try:
            return method(self._id, reason)
        except ValueError:
            raise ValueError(
                f"Cannot restore {self.__class__.__name__} with id {self._id}. Ensure the client is set and the item is restorable."
            )
