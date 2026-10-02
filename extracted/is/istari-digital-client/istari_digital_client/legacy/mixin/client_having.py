from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Generic, List, Optional, TypeVar

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.api.v2_api import V2Api

ClientT = TypeVar("ClientT")


class ClientHaving(Generic[ClientT]):
    """
    Generic mixin for models that require access to a client API instance.

    This class provides a `client` property (getter/setter) and ensures that the same client is
    propagated to any nested attributes listed in ``__client_fields__``. It is
    typically used in combination with other mixins that perform API operations.

    Type Parameters:
        ClientT: The type of the client API (e.g., V2Api, V3Api)

    Example:
        class PageComment(Pageable[Comment], ClientHaving[V2Api]):
            ...
    """

    _client: Optional[ClientT] = None
    __client_fields__: ClassVar[List[str]] = []

    @property
    def client(self) -> Optional[ClientT]:
        """
        Get the client instance associated with this object.

        The client is typically used to make SDK API calls.
        """

        return self._client

    @client.setter
    def client(self, value: ClientT):
        """
        Set the client instance for this object and propagate it to any nested fields.

        Fields listed in ``__client_fields__`` will also have their ``client`` attribute
        set if applicable (e.g., for nested models or lists of models).

        :param value: The client API instance to assign.
        """

        self._client = value

        for name in self.__client_fields__:
            attr = getattr(self, name, None)

            if isinstance(attr, list):
                for item in attr:
                    if hasattr(item, "client"):
                        item.client = value
            elif attr is not None and hasattr(attr, "client"):
                attr.client = value
