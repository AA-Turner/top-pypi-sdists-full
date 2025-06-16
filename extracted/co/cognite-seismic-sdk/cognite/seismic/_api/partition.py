import os
from typing import Iterator, Optional

from cognite.seismic._api.api import API
from cognite.seismic._api.grpc_helpers import get_single_item
from cognite.seismic._api.utility import _get_identifier
from cognite.seismic.data_classes.api_types import Partition
from cognite.seismic.data_classes.searchspec import SearchSpecLastModified, SearchSpecUnion

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        CreatePartitionRequest,
        DeletePartitionRequest,
        EditPartitionRequest,
        SearchPartitionsRequest,
    )


class PartitionAPI(API):
    def __init__(self, query, ingestion):
        super().__init__(query=query, ingestion=ingestion)

    def search(
        self,
        *,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        external_id_substring: Optional[str] = None,
        name: Optional[str] = None,
        name_substring: Optional[str] = None,
        last_modified: Optional[SearchSpecLastModified] = None,
        get_all: bool = False,
    ) -> Iterator[Partition]:
        """Search for partitions.

        Can search by id, external_id, name, or substrings of external_id or name.
        Only one search method should be specified. The behaviour when multiple are specified is undefined.

        Args:
            id (int, optional): Partition id
            external_id (str, optional): Partition external id
            external_id_substring (str, optional): Substring of external id to search by
            name (str, optional): Partition name
            name_substring (str, optional): Substring of name to search by
            last_modified (:py:class:`~cognite.seismic.SearchSpecLastModified`):
                Return partitions where the last modified time is within this range
            get_all (bool): Whether to instead retrieve all visible partitions. Equivalent to list().

        Returns:
            Iterator[:py:class:`~cognite.seismic.Partition`]: A stream of matching partitions
        """

        if get_all:
            req = SearchPartitionsRequest()
        elif last_modified:
            req = SearchPartitionsRequest(last_modified=last_modified.to_last_modified_filter())
        else:
            spec = SearchSpecUnion(
                id=id,
                external_id=external_id,
                external_id_substring=external_id_substring,
                name=name,
                name_substring=name_substring,
            )._to_search_spec()
            req = SearchPartitionsRequest(partitions=spec)
        return (Partition._from_proto(p) for p in self.query.SearchPartitions(req))

    def get(self, id: Optional[int] = None, external_id: Optional[str] = None) -> Partition:
        """
        Retrieve a single partition by id or external id.

        Equivalent to search() using id or external id.

        Args:
            id (int, optional): Partition id
            external_id (str, optional): Partition external id

        Returns:
            :py:class:`~cognite.seismic.Partition`
        """
        if id is None and external_id is None:
            raise TypeError("Either the id or the external_id argument must be provided")
        if id is not None and external_id is not None:
            raise TypeError("Specify only one of id and external_id")

        result = self.search(id=id, external_id=external_id)
        return get_single_item(result, "Partition not found")

    def list(self) -> Iterator[Partition]:
        """List all partitions.

        List all visible partitions. This is equivalent to calling search() with get_all=true.

        Returns:
            Iterator[:py:class:`~cognite.seismic.Partition`]: A stream of all visible partitions
        """

        return self.search(get_all=True)

    def create(self, *, external_id: str, name: str = "") -> Partition:
        """Create a new partition.

        Create a new partition, providing an external id and an optional name.

        Args:
            external_id (str): The external id of the new partition. Must be unique.
            name (str):
                The name of the new partition. If not specified, will display the
                external id wherever a name is required.

        Returns:
            :py:class:`Partition`: The newly created partition
        """
        createRequest = CreatePartitionRequest(name=name, external_id=external_id)
        return Partition._from_proto(self.query.CreatePartition(createRequest))

    def edit(self, *, new_name: str, id: Optional[int] = None, external_id: Optional[str] = None) -> Partition:
        """Edit an existing partition.

        Edit an existing partition by providing either an id or an external id.
        The only parameter that can be edited is the name.

        Args:
            id (int, optional): The id of the partition
            external_id (str, optional): The external id of the partition
            new_name (str): The new name. Set as an empty string to delete the existing name.

        Returns:
            :py:class:`Partition`: The edited partition
        """
        identifier = _get_identifier(id, external_id)
        editRequest = EditPartitionRequest(partition=identifier, new_name=new_name)
        return Partition._from_proto(self.query.EditPartition(editRequest))

    def delete(self, *, id: Optional[int] = None, external_id: Optional[str] = None):
        """Delete a partition.

        Delete a partition by providing either an id or an external id.

        Args:
            id (int, optional): The id of the partition
            external_id (str, optional): The external id of the partition
        """
        identifier = _get_identifier(id, external_id)
        deleteRequest = DeletePartitionRequest(partition=identifier)
        self.query.DeletePartition(deleteRequest)
