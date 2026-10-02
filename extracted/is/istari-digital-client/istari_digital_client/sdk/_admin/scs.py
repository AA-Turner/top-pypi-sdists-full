"""Secure Connection Service manager (IstariAdmin surface).

``Scs`` manages cross-tenant data synchronization infrastructure:
connections (receiving/sending remotes) and object stores.
"""

from __future__ import annotations

from functools import cached_property
from typing import Any

from istari_digital_client.sdk._base import Page, _Manager


class Connections(_Manager):
    """Manage cross-tenant data-sharing connections — pull (receiving) and push (sending) remotes.

    Aliases: cross-tenant sync share remote connection pull push secure-connection scs


    Connections enable cross-tenant data synchronization. Receiving remotes
    pull data from other tenants; sending remotes push data to other tenants.

    Usage::

        # List receiving connections
        for conn in admin.scs.connections.list_receiving():
            print(f"{conn.id}: {conn.label}")

        # List sending connections
        for conn in admin.scs.connections.list_sending():
            print(f"{conn.id}: {conn.label}")
    """

    def list_receiving(
        self,
        *,
        show_archived: bool | None = None,
        size: int | None = None,
    ) -> Page[Any]:
        """List receiving connections — remotes you pull data from (another tenant/organization).

        Args:
            show_archived: Include archived receiving remotes.
            size: Number of items per page (max 100).

        Returns:
            A paginated list of receiving connections.
        """
        return self._paginate(
            lambda cursor: self._call(
                self._engine.v3_api.list_receiving_remotes,
                cursor=cursor,
                size=size,
                show_archived=show_archived,
            ),
            bind=lambda dto: dto,  # Return raw DTO for now
        )

    def get_receiving(self, connection_id: str) -> Any:
        """Get a receiving remote connection by ID.

        Args:
            connection_id: The UUID of the receiving connection.

        Returns:
            The receiving connection details.
        """
        return self._call(self._engine.v3_api.get_receiving_remote, connection_id)

    def create_receiving(
        self,
        *,
        label: str,
        description: str,
        shared_id: str,
        shared_secret: str,
        object_store_id: str,
        **kwargs: Any,
    ) -> Any:
        """Create a receiving connection — a remote you pull data from (another tenant/organization).

        Mutates: true

        Args:
            label: Human-readable label for the connection.
            description: Description of the connection.
            shared_id: The shared identifier used to pair the connection.
            shared_secret: The shared secret used to authenticate the connection.
            object_store_id: The object store to use for this connection.
            **kwargs: Additional connection parameters (e.g., transformations).

        Returns:
            The created receiving connection.
        """
        from istari_digital_client.sdk._generated.v3.models.receiving_connection_create_dto import (
            ReceivingConnectionCreateDto,
        )

        dto = ReceivingConnectionCreateDto(
            label=label,
            description=description,
            shared_id=shared_id,
            shared_secret=shared_secret,
            object_store_id=object_store_id,
            **kwargs,
        )
        return self._call(self._engine.v3_api.create_receiving_remote, dto)

    def update_receiving(
        self,
        connection_id: str,
        **kwargs: Any,
    ) -> Any:
        """Update a receiving remote connection.

        Mutates: true

        Args:
            connection_id: The UUID of the connection to update.
            **kwargs: Update parameters (label, description, etc.).

        Returns:
            The updated receiving connection.
        """
        from istari_digital_client.sdk._generated.v3.models.update_receiving_connection_dto import (
            UpdateReceivingConnectionDto,
        )

        dto = UpdateReceivingConnectionDto(**kwargs)
        return self._call(
            self._engine.v3_api.update_receiving_remote, connection_id, dto
        )

    def list_sending(
        self,
        *,
        show_archived: bool | None = None,
        size: int | None = None,
    ) -> Page[Any]:
        """List sending connections — remotes you push data to (another tenant/organization).

        Args:
            show_archived: Include archived sending remotes.
            size: Number of items per page (max 100).

        Returns:
            A paginated list of sending connections.
        """
        return self._paginate(
            lambda cursor: self._call(
                self._engine.v3_api.list_sending_remotes,
                cursor=cursor,
                size=size,
                show_archived=show_archived,
            ),
            bind=lambda dto: dto,  # Return raw DTO for now
        )

    def get_sending(self, connection_id: str) -> Any:
        """Get a sending remote connection by ID.

        Args:
            connection_id: The UUID of the sending connection.

        Returns:
            The sending connection details.
        """
        return self._call(self._engine.v3_api.get_sending_remote, connection_id)

    def create_sending(
        self,
        *,
        label: str,
        description: str,
        shared_id: str,
        shared_secret: str,
        object_store_id: str,
        infosec_level_id: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Create a sending connection — a remote you push data to (another tenant/organization).

        Mutates: true

        Args:
            label: Human-readable label for the connection.
            description: Description of the connection.
            shared_id: The shared identifier used to pair the connection.
            shared_secret: The shared secret used to authenticate the connection.
            object_store_id: The object store to use for this connection.
            infosec_level_id: Optional infosec level for the connection.
            **kwargs: Additional connection parameters (e.g., transformations).

        Returns:
            The created sending connection.
        """
        from istari_digital_client.sdk._generated.v3.models.sending_connection_create_dto import (
            SendingConnectionCreateDto,
        )

        dto = SendingConnectionCreateDto(
            label=label,
            description=description,
            shared_id=shared_id,
            shared_secret=shared_secret,
            object_store_id=object_store_id,
            infosec_level_id=infosec_level_id,
            **kwargs,
        )
        return self._call(self._engine.v3_api.create_sending_remote, dto)

    def update_sending(
        self,
        connection_id: str,
        **kwargs: Any,
    ) -> Any:
        """Update a sending remote connection.

        Mutates: true

        Args:
            connection_id: The UUID of the connection to update.
            **kwargs: Update parameters (label, description, infosec_level_id, etc.).

        Returns:
            The updated sending connection.
        """
        from istari_digital_client.sdk._generated.v3.models.update_sending_connection_dto import (
            UpdateSendingConnectionDto,
        )

        dto = UpdateSendingConnectionDto(**kwargs)
        return self._call(self._engine.v3_api.update_sending_remote, connection_id, dto)


class ObjectStores(_Manager):
    """Manager for SCS object stores (read-only).

    Object stores represent external S3-compatible storage backends
    configured for the tenant.

    Usage::

        # List object stores
        for store in admin.scs.object_stores.list():
            print(f"{store.id}: {store.name}")
    """

    def list(self, *, size: int | None = None) -> Page[Any]:
        """List configured object stores.

        Args:
            size: Number of items per page (max 100).

        Returns:
            A paginated list of object stores.
        """
        return self._paginate(
            lambda cursor: self._call(
                self._engine.v3_api.list_object_stores,
                cursor=cursor,
                size=size,
            ),
            bind=lambda dto: dto,  # Return raw DTO for now
        )


class Scs(_Manager):
    """Secure Connection Service manager.

    Reached via ``admin.scs``. SCS manages cross-tenant data synchronization
    infrastructure: connections (receiving/sending remotes) and object stores.

    Usage::

        # List receiving connections
        for conn in admin.scs.connections.list_receiving():
            print(conn.label)

        # List object stores
        for store in admin.scs.object_stores.list():
            print(store.name)
    """

    @cached_property
    def connections(self) -> Connections:
        """Sub-manager for SCS connections (receiving/sending remotes)."""
        return Connections(self._engine)

    @cached_property
    def object_stores(self) -> ObjectStores:
        """Sub-manager for SCS object stores (read-only list)."""
        return ObjectStores(self._engine)
