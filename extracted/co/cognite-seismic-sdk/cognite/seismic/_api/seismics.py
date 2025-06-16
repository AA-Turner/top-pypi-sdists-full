import os
from typing import Iterator, Optional, Union

from cognite.seismic._api.api import API
from cognite.seismic._api.grpc_helpers import get_single_item
from cognite.seismic._api.utility import Metadata, _get_coverage_spec, _get_identifier
from cognite.seismic.data_classes.api_types import BinaryHeader, Seismic, TextHeader
from cognite.seismic.data_classes.extents import SeismicCutout, SeismicTraceGroupExtent, TraceHeaderField
from cognite.seismic.data_classes.searchspec import SearchSpecBase, SearchSpecGetAll, SearchSpecSeismic
from google.protobuf.wrappers_pb2 import StringValue

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import Identifier, OptionalMap
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        CreateSeismicRequest,
        DeleteSeismicRequest,
        EditSeismicRequest,
    )


class SeismicAPI(API):
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

    def create(
        self,
        *,
        external_id: str,
        partition_identifier: Union[int, str],
        seismic_store_id: int,
        name: Optional[str] = None,
        cutout: SeismicCutout,
        trace_group_cutout: Optional[SeismicTraceGroupExtent] = None,
        metadata: Optional[Metadata] = None,
        copy_metadata: bool = False,
        text_header: Optional[TextHeader] = None,
        binary_header: Optional[BinaryHeader] = None,
    ) -> Seismic:
        """Create a new Seismic.

        Args:
            external_id (str): The external id of the new Seismic
            name (str, optional): If specified, the name of the new Seismic
            partition_identifier (int | str): Either the partition id or external_id that the Seismic is part of
            seismic_store_id (int): The seismic store that the new Seismic is derived from
            cutout (:py:class:`~cognite.seismic.SeismicCutout`):
                Specifies which part of the data is included from the containing seismicstore
            trace_group_cutout (:py:class:`~cognite.seismic.SeismicTraceGroupExtent`):
                Specifies which traces are included from each prestack migrated bin from the containing seismicstore.
                Only available for prestack migrated files.
            metadata (Dict[str, str], optional): If specified, sets the metadata to the provided value.
            copy_metadata (bool): If True, ignores the `metadata` arg and copies the metadata from the seismic store.
            text_header (:py:class:`~cognite.seismic.TextHeader`, optional):
                If specified, sets the provided text header on the new seismic
            binary_header (:py:class:`~cognite.seismic.BinaryHeader`, optional):
                If specified, sets the provided binary header on the new seismic

        Returns:
            :py:class:`~cognite.seismic.Seismic`:
                The newly created Seismic with minimal data.
                Use search() or get() to retrieve all data.
        """
        if type(partition_identifier) == int:
            identifier = Identifier(id=partition_identifier)
        elif type(partition_identifier) == str:
            identifier = Identifier(external_id=partition_identifier)
        else:
            raise Exception("partition_identifier should be an int or a str.")

        request = CreateSeismicRequest(external_id=external_id, partition=identifier, seismic_store_id=seismic_store_id)
        cutout._merge_into_create_seismic_request(request)

        if trace_group_cutout is not None:
            trace_group_cutout._merge_into_create_seismic_request(request)

        if name is not None:
            request.name = name

        if metadata is not None:
            request.metadata.MergeFrom(OptionalMap(data=metadata))

        if copy_metadata:
            request.copy_metadata = True

        if text_header is not None:
            request.text_header.MergeFrom(text_header._to_proto())

        if binary_header is not None:
            request.binary_header.MergeFrom(binary_header._to_proto())

        return Seismic._from_proto(self.query.CreateSeismic(request), self._api_client.traces)

    def search(
        self,
        *,
        search_spec: SearchSpecBase,
        include_text_header: bool = False,
        include_binary_header: bool = False,
        include_extent: bool = False,
        extent_key: Optional[TraceHeaderField] = None,
        include_cutout: bool = False,
        include_seismic_store: bool = False,
        include_partition: bool = False,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
    ) -> Iterator[Seismic]:
        """Search for seismics.

        Can search all seismics included in surveys, partitions, or directly search for seismic objects,
        specified by id, external_id, name, or substrings of external_id or name.
        Only one search method should be specified.

        Args:
            search_spec: One of :py:class:`~cognite.seismic.SearchSpecSurvey`,
                :py:class:`~cognite.seismic.SearchSpecPartition`,
                :py:class:`~cognite.seismic.SearchSpecSeismic`, or
                :py:class:`~cognite.seismic.SearchSpecGetAll`.
            include_text_header (bool): If true, includes the text header in the responses
            include_binary_header (bool): If true, includes the binary header in the responses
            include_extent (bool): If true, includes a description of the traces included in the Seismic object
            extent_key (:py:class:`~cognite.seismic.TraceHeaderField`, optional):
                Choose which trace header field to describe the traces by (in 2D), or which to use
                as the major direction (in 3D). Implies `include_extent`.
            include_seismic_store (bool): If true, include the seismic store info in the responses
            include_partition (bool): If true, include the partition info in the responses
            coverage_crs (str, optional):
                If specified, includes the coverage in the given CRS.
                Either coverage_crs or coverage_format must be specified to retrieve coverage.
            coverage_format (str, optional):
                One of "wkt", "geojson". If specified, includes the coverage as the given format.

        Returns:
            Iterator[:py:class:`~cognite.seismic.Seismic`]: The list of matching Seismics
        """

        req = search_spec._to_search_seismics_request()

        if coverage_crs is not None or coverage_format is not None:
            req.coverage.MergeFrom(_get_coverage_spec(coverage_crs, coverage_format))

        req.include_text_header = include_text_header
        req.include_binary_header = include_binary_header
        if extent_key is not None:
            include_extent = True
            req.extent_key = extent_key._to_proto()
        req.include_extent = include_extent
        req.include_cutout = include_cutout
        req.include_seismic_store = include_seismic_store
        req.include_partition = include_partition

        return (Seismic._from_proto(s, self._api_client.traces) for s in self.query.SearchSeismics(req))

    def list(
        self,
        *,
        include_text_header: bool = False,
        include_binary_header: bool = False,
        include_extent: bool = False,
        extent_key: Optional[TraceHeaderField] = None,
        include_cutout: bool = False,
        include_seismic_store: bool = False,
        include_partition: bool = False,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
    ) -> Iterator[Seismic]:
        """List all visible seismics.
        This is equivalent to calling search() with search_spec=SearchSpecGetAll().

        Args:
            include_text_header (bool): If true, includes the text header in the responses
            include_binary_header (bool): If true, includes the binary header in the responses
            include_extent (bool): If true, includes a description of the traces included in the Seismic object
            include_seismic_store (bool): If true, include the seismic store info in the responses
            include_partition (bool): If true, include the partition info in the responses
            coverage_crs (str, optional):
                If specified, includes the coverage in the given CRS.
                Either coverage_crs or coverage_format must be specified to retrieve coverage.
            coverage_format (str, optional):
                One of "wkt", "geojson". If specified, includes the coverage as the given format.

        Returns:
            Iterator[:py:class:`~cognite.seismic.Seismic`]: A stream of visible seismic objects.
        """
        return self.search(
            search_spec=SearchSpecGetAll(),
            include_text_header=include_text_header,
            include_binary_header=include_binary_header,
            include_extent=include_extent,
            extent_key=extent_key,
            include_cutout=include_cutout,
            include_seismic_store=include_seismic_store,
            include_partition=include_partition,
            coverage_crs=coverage_crs,
            coverage_format=coverage_format,
        )

    def get(
        self,
        *,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        extent_key: Optional[TraceHeaderField] = None,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = "wkt",
    ) -> Seismic:
        """Get a seismic by id or external id.

        Includes all available info.

        Args:
            id (int, optional): id of seismic to get
            external_id (str, optional): external id of seismic to get
            extent_key (:py:class:`~cognite.seismic.TraceHeaderField`, optional):
                Choose which trace header field to describe the traces by (in 2D), or which to use
                as the major direction (in 3D).
            coverage_crs (str, optional): The CRS of the received coverage. Defaults to the file's CRS.
            coverage_format (str, optional):
                Either "wkt" or "geojson". The desired file format for the coverage. Defaults to "wkt".

        Returns:
            :py:class:`~cognite.seismic.Seismic`: The matching seismic
        """
        if id is not None and external_id is not None:
            raise ValueError("Only one of id and external_id can be specified.")
        if id is not None:
            search_spec = SearchSpecSeismic(id=id)
        elif external_id is not None:
            search_spec = SearchSpecSeismic(external_id=external_id)
        else:
            raise ValueError("Need to provide either the seismic id or external id")

        result = self.search(
            search_spec=search_spec,
            include_text_header=True,
            include_binary_header=True,
            include_extent=True,
            extent_key=extent_key,
            include_cutout=True,
            include_seismic_store=True,
            include_partition=True,
            coverage_crs=coverage_crs,
            coverage_format=coverage_format,
        )

        if id is not None:
            not_found_msg = f"Seismic with id '{id}'' not found"
        else:
            not_found_msg = f"Seismic with external id '{external_id}' not found"
        return get_single_item(result, not_found_msg)

    def edit(
        self,
        *,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Metadata] = None,
    ) -> Seismic:
        """Edit an existing seismic.

        Either the id or the external_id should be provided in order to
        identify the seismic. The editable fields are name and metadata.
        Providing a name or metadata field will replace the existing data with
        the new data. Providing an empty string as the name will delete the
        seismic name.

        Args:
            id (int, optional): The id of the seismic
            external_id (str, optional): The external id of the seismic
            name (str, optional): The new name of the seismic
            metadata (Dict[str, str], optional): The new metadata for the seismic

        Returns:
            :py:class:`~cognite.seismic.Seismic`:
                The edited Seismic with minimal data. Use search() to retrieve all data.
        """
        identifier = _get_identifier(id, external_id)
        request = EditSeismicRequest(seismic=identifier)
        if name is not None:
            request.name.CopyFrom(StringValue(value=name))
        if metadata is not None:
            request.metadata.MergeFrom(OptionalMap(data=metadata))

        return Seismic._from_proto(self.query.EditSeismic(request), self._api_client.traces)

    def delete(self, *, id: Optional[int] = None, external_id: Optional[str] = None):
        """Delete a seismic

        Either the id or the external id should be provided in order to identify the seismic.

        Args:
            id (int, optional): The id of the seismic
            external_id (str, optional): The external id of the seismic
        """
        identifier = _get_identifier(id, external_id)
        request = DeleteSeismicRequest(seismic=identifier)

        self.query.DeleteSeismic(request)
