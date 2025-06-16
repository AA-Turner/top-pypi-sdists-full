import os
from typing import Iterator, Optional

from cognite.seismic._api.api import API
from cognite.seismic._api.grpc_helpers import get_single_item
from cognite.seismic._api.utility import Metadata, _get_coverage_spec, _get_identifier
from cognite.seismic.data_classes.api_types import SeismicStore
from cognite.seismic.data_classes.extents import TraceHeaderField
from cognite.seismic.data_classes.searchspec import SearchSpecBase, SearchSpecGetAll, SearchSpecSeismicStore

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import OptionalMap
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        DeleteSeismicStoreRequest,
        EditSeismicStoreRequest,
    )
    from google.protobuf.wrappers_pb2 import StringValue


class SeismicStoreAPI(API):
    def __init__(self, api_client):
        self._api_client = api_client
        super().__init__(query=api_client.seismicstub, ingestion=api_client.ingestion)

    @staticmethod
    def _verify_input(crs: Optional[str] = None, wkt: Optional[str] = None, geo_json: Optional[str] = None):
        if crs is None:
            raise Exception("CRS is required")
        if wkt is None and geo_json is None:
            raise Exception("Either `wkt` or `geo_json` needs to be specified")
        if wkt is not None and geo_json is not None:
            raise Exception("Only `wkt` or `geo_json` should be specified")

    def search(
        self,
        *,
        search_spec: SearchSpecBase,
        include_file_info: bool = False,
        include_headers: bool = False,
        include_extent: bool = False,
        extent_key: Optional[TraceHeaderField] = None,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
    ) -> Iterator[SeismicStore]:
        """Search for seismic stores.

        Can search all seismic stores included in surveys or directly search seismic stores,
        specified by id, external_id, name, or substrings of external_id or name.

        For example, to find the seismic store corresponding to a recently ingested file with id
        :code:`file_id`, run:

        .. code-block:: python

            client.seismicstore.search(search_spec=SearchSpecFile(id=file_id))

        Args:
            search_spec:
                One of :py:class:`~cognite.seismic.SearchSpecSurvey`,
                :py:class:`~cognite.seismic.SearchSpecFile`,
                :py:class:`~cognite.seismic.SearchSpecSeismicStore`, or
                :py:class:`~cognite.seismic.SearchSpecGetAll`.
                Specifies the search parameters.
            include_file_info (bool): If true, the response will include information on the source file.
            include_headers (bool): If true, the response will include headers.
            include_extent (bool):
                If true, the response will include a description of the traces contained in the seismic store
            extent_key (:py:class:`~cognite.seismic.TraceHeaderField`, optional):
                Choose which trace header field to describe the traces by (in 2D), or which to use
                as the major direction (in 3D). Implies `include_extent`.
            coverage_crs (str, optional):
                If specified, includes the coverage in the given CRS.
                Either coverage_crs or coverage_format must be specified to retrieve coverage.
            coverage_format (str, optional):
                One of "wkt", "geojson". If specified, includes the coverage as the given format.

        Returns:
            Iterator[:py:class:`~cognite.seismic.SeismicStore`]:
                A stream of matching seismic stores
        """

        req = search_spec._to_search_seismicstores_request()

        if coverage_crs is not None or coverage_format is not None:
            coverage = _get_coverage_spec(coverage_crs, coverage_format)
            req.coverage.MergeFrom(coverage)

        req.include_file_info = include_file_info
        req.include_headers = include_headers
        if extent_key is not None:
            include_extent = True
            req.extent_key = extent_key._to_proto()
        req.include_extent = include_extent

        return (SeismicStore._from_proto(s, self._api_client.traces) for s in self.query.SearchSeismicStores(req))

    def list(
        self,
        *,
        include_file_info: bool = False,
        include_extent: bool = False,
        extent_key: Optional[TraceHeaderField] = None,
    ) -> Iterator[SeismicStore]:
        """List all visible seismic stores.

        This is equivalent to calling search() with search_spec=SearchSpecGetAll().

        Args:
            include_file_info (bool, optional): If true, the response will include information on the source file.
            include_extent (bool, optional):
                If true, the response will include a description of the traces contained in the seismic store.
            extent_key (:py:class:`~cognite.seismic.TraceHeaderField`, optional):
                Choose which trace header field to describe the traces by (in 2D), or which to use
                as the major direction (in 3D). Implies `include_extent`.

        Returns:
            Iterator[:py:class:`~cognite.seismic.SeismicStore`]:
                A Stream of visible seismic stores
        """
        return self.search(
            search_spec=SearchSpecGetAll(),
            include_file_info=include_file_info,
            include_extent=include_extent,
            extent_key=extent_key,
        )

    def get(
        self,
        id: int,
        *,
        extent_key: Optional[TraceHeaderField] = None,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = "wkt",
    ) -> SeismicStore:
        """Get a seismic store by its id.

        Includes all available info.

        Args:
            id (int): The seismic store id to find
            extent_key (:py:class:`~cognite.seismic.TraceHeaderField`, optional):
                Choose which trace header field to describe the traces by (in 2D), or which to use
                as the major direction (in 3D).
            coverage_crs (str, optional):
                If specified, includes the coverage in the given CRS.
                Either coverage_crs or coverage_format must be specified to retrieve coverage.
            coverage_format (str, optional):
                Either "wkt" or "geojson". The desired file format for the coverage. Defaults to "wkt".

        Returns:
            :py:class:`~cognite.seismic.SeismicStore`
        """
        result = self.search(
            search_spec=SearchSpecSeismicStore(id=id),
            include_file_info=True,
            include_headers=True,
            include_extent=True,
            extent_key=extent_key,
            coverage_crs=coverage_crs,
            coverage_format=coverage_format,
        )
        return get_single_item(result, f"Could not find the seismic store {id}")

    def edit(
        self,
        *,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        new_name: Optional[str] = None,
        metadata: Optional[Metadata] = None,
    ) -> SeismicStore:
        """Edit a seismic store.

        Edit a seismic store, providing the seismic store id.
        The name and the metadata can be edited.

        Args:
            id (int, optional): The id of the seismic store
            new_name (str, optional): If specified, the new name. Provide an empty string to delete the existing name.
            metadata (Dict[str, str], optional): If specified, replaces the old metadata with the new one.

        Returns:
            :py:class:`~cognite.seismic.SeismicStore`:
        """
        identifier = _get_identifier(id, external_id)
        request = EditSeismicStoreRequest(seismic_store=identifier)
        if new_name is not None:
            request.name.MergeFrom(StringValue(value=new_name))
        if metadata is not None:
            request.metadata.MergeFrom(OptionalMap(data=metadata))
        return SeismicStore._from_proto(self.query.EditSeismicStore(request), self._api_client.traces)

    def delete(self, *, id: Optional[int] = None, external_id: Optional[str] = None):
        """Delete a seismic store.

        If any seismics still reference the specified seismic store, the request will fail.

        Args:
            id (int, optional): The id or the external id of the seismic store to delete
            external_id (str, optional): The id or the external id of the seismic store to delete
        """

        request = DeleteSeismicStoreRequest(seismic_store=_get_identifier(id, external_id))
        self.query.DeleteSeismicStore(request)
