# Copyright 2022 Cognite AS

import os
from typing import Dict, Iterator, List, Mapping, Optional

from cognite.seismic._api.api import API
from cognite.seismic._api.grpc_helpers import get_single_item
from cognite.seismic._api.utility import _get_coverage_spec, _get_exact_match_filter, _get_identifier
from cognite.seismic.data_classes.api_types import Survey, SurveyCoverageSource, SurveyGridTransformation
from cognite.seismic.data_classes.errors import InvalidArgumentError
from cognite.seismic.data_classes.geometry import Geometry
from cognite.seismic.data_classes.searchspec import SearchSpecLastModified

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import CRS, CustomSurveyCoverage, ExternalId, GeoJson
    from cognite.seismic.protos.types_pb2 import Geometry as GeometryProto
    from cognite.seismic.protos.types_pb2 import Wkt
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import LastModifiedFilter, OptionalMap, SearchSpec
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        CreateSurveyRequest,
        DeleteSurveyRequest,
        EditSurveyRequest,
        SearchSurveysRequest,
    )
    from google.protobuf.struct_pb2 import Struct
    from google.protobuf.wrappers_pb2 import StringValue


class SurveyAPI(API):
    def __init__(self, seismic):
        super().__init__()
        self.seismic = seismic

    def list(
        self,
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
        include_grid_transformation: Optional[bool] = False,
        include_custom_coverage: Optional[bool] = False,
        coverage_source: SurveyCoverageSource = SurveyCoverageSource.UNSPECIFIED,
    ) -> Iterator[Survey]:
        """List all the surveys.
        Provide either crs or coverage_format to get surveys' coverage.

        Args:
            list_seismics (bool, optional): If true, list the seismics ids from each survey.
            list_seismic_stores (bool, optional):
                If true, list the seismic store ids from each surveys.
                Only permitted if the user is a data manager (write access to all partitions).
            include_metadata (bool, optional): true if metadata should be included in the response.
            coverage_crs (str, optional):
                The crs in which the surveys' coverage is returned, default is original survey crs
            coverage_format (str, optional):
                One of "wkt", "geojson". If specified, includes the coverage as the given format. Defaults to geojson.
            include_grid_transformation (bool, optional):
                If true, return the user-specified transformation between bin grid and projected coordinates
            include_custom_coverage (bool, optional): If true, return the customer-specified survey coverage

        Returns:
            Iterator[:py:class:`~cognite.seismic.Survey`]: the requested surveys and their files (if requested).
        """
        return self._search_internal(
            [],
            None,
            list_seismics,
            list_seismic_stores,
            include_metadata,
            coverage_crs,
            coverage_format,
            include_grid_transformation,
            include_custom_coverage,
            coverage_source,
        )

    def search(
        self,
        id: Optional[int] = None,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        name_substring: Optional[str] = None,
        external_id: Optional[str] = None,
        external_id_substring: Optional[str] = None,
        geometry: Optional[Geometry] = None,
        survey_contains_exact_metadata: Optional[Mapping[str, str]] = None,
        last_modified: Optional[SearchSpecLastModified] = None,
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
        include_grid_transformation: Optional[bool] = False,
        include_custom_coverage: Optional[bool] = False,
        coverage_source: SurveyCoverageSource = SurveyCoverageSource.UNSPECIFIED,
    ) -> Iterator[Survey]:
        """Search for subset of surveys.
        Provide either crs or coverage_format to get surveys' coverage.

        Args:
            id (int, optional): Find surveys with this id
            uuid (str, optional): Find surveys with this id in the old uuid format
            name (str, optional): Find surveys with this name
            name_substring (str): Find surveys whose name contains this substring
            external_id (str, optional): Find surveys with this external id
            external_id_substring (str, optional):
                Find surveys whose external id contains this substring
            geometry (:py:class:`~cognite.seismic.Geometry`, optional):
                Find surveys whose coverage overlaps the given geometry
            survey_contains_exact_metadata (Mapping[str, str], optional):
                Find surveys whose metadata contains an exact match of the keys and values of the provided metadata.
                It is also case-sensitive.
            last_modified (:py:class:`~cognite.seismic.SearchSpecLastModified`, optional):
                If specified, further filters the returned surveys by their last modified date.
            list_seismics (bool, optional): If true, list the seismics ids from each survey.
            list_seismic_stores (bool, optional):
                If true, list the seismic store ids from each survey.
                Only permitted if the user is a data manager (write access to all partitions).
            include_metadata (bool, optional): If true, include metadata in the response.
            coverage_crs (str, optional):
                The crs in which the surveys' coverage is returned, default is original survey crs
            coverage_format (str, optional):
                One of "wkt", "geojson". If specified, includes the coverage as the given format. Defaults to wkt.
            include_grid_transformation (bool, optional):
                If True, return the user-specified transformation between bin grid and projected coordinates
            include_custom_coverage (bool, optional): If True, return the customer-specified survey coverage
            coverage_source (SurveyCoverageSource, optional):
                If specified, attempts to return the survey coverage from the given source.
                Defaults to unspecified, where the custom coverage will be prioritized.

        Returns:
            Iterator[:py:class:`~cognite.seismic.Survey`]: The requested surveys and their files (if requested).
        """
        if (
            id is None
            and uuid is None
            and external_id is None
            and name is None
            and name_substring is None
            and external_id_substring is None
            and geometry is None
            and survey_contains_exact_metadata is None
            and last_modified is None
        ):
            raise ValueError(
                "one of id, uuid, external_id, name, name_substring, survey_external_id_substring, "
                "geometry, or survey_contains_exact_metadata must be specified"
            )

        search_specs = []
        if id is not None:
            search_specs.append(SearchSpec(id=id))
        if uuid is not None:
            search_specs.append(SearchSpec(id_string=uuid))
        if name is not None:
            search_specs.append(SearchSpec(name=name))
        if name_substring is not None:
            search_specs.append(SearchSpec(name_substring=name_substring))
        if external_id is not None:
            search_specs.append(SearchSpec(external_id=external_id))
        if external_id_substring is not None:
            search_specs.append(SearchSpec(external_id_substring=external_id_substring))
        if geometry is not None:
            search_specs.append(SearchSpec(geometry=geometry._to_proto()))
        if survey_contains_exact_metadata:
            metadata_filter = _get_exact_match_filter(survey_contains_exact_metadata)
            search_specs.append(SearchSpec(metadata=metadata_filter))

        return self._search_internal(
            search_specs,
            None if last_modified is None else last_modified.to_last_modified_filter(),
            list_seismics,
            list_seismic_stores,
            include_metadata,
            coverage_crs,
            coverage_format,
            include_grid_transformation,
            include_custom_coverage,
            coverage_source,
        )

    def get(
        self,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
        include_grid_transformation: Optional[bool] = False,
        include_custom_coverage: Optional[bool] = False,
        coverage_source: SurveyCoverageSource = SurveyCoverageSource.UNSPECIFIED,
    ) -> Survey:
        """
        Get a survey by either id, external_id, name, or the old uuid identifier.
        Provide either coverage_crs or coverage_format to get survey coverage.

        Args:
            id (int, optional): survey id.
            external_id (str, optional): survey external id.
            uuid (str, optional): survey id in the old uuid format.
            name (str, optional): survey name.
            list_seismics (bool, optional):
                If true, list the seismic ids in the survey.
            list_seismic_stores (bool, optional):
                If true, list the seismic store ids in the survey.
                Only permitted if the user is a data manager (write access to all partitions).
            include_metadata (bool, optional): If true, include the metadata in the response.
            coverage_crs (str, optional):
                The crs in which the survey coverage is returned, default is original survey crs
            coverage_format (str, optional):
                One of "wkt", "geojson". If specified, includes the coverage as the given format.
                Defaults to wkt.
            include_grid_transformation (bool, optional):
                If true, return the user-specified transformation between bin grid and projected coordinates
            include_custom_coverage (bool, optional): If true, return the customer-specified survey coverage
            coverage_source (SurveyCoverageSource, optional):
                if specified, attempts to return the survey coverage from the given source.
                Defaults to unspecified, where the custom coverage will be prioritized.

        Returns:
            :py:class:`~cognite.seismic.Survey`:
                The requested survey, its seismics, seismic stores and metadata (if requested).
        """
        if sum([id is not None, external_id is not None, uuid is not None, name is not None]) > 1:
            raise ValueError("Only one of id, external_id, name, or uuid can be specified.")

        if id is not None:
            search_spec = SearchSpec(id=id)
        elif external_id is not None:
            search_spec = SearchSpec(external_id=external_id)
        elif uuid is not None:
            search_spec = SearchSpec(id_string=uuid)
        elif name is not None:
            search_spec = SearchSpec(name=name)
        else:
            raise ValueError("At least one of id, external_id, name, or uuid should be specified.")

        result = self._search_internal(
            [search_spec],
            None,
            list_seismics,
            list_seismic_stores,
            include_metadata,
            coverage_crs,
            coverage_format,
            include_grid_transformation,
            include_custom_coverage,
            coverage_source,
        )
        return get_single_item(result, "Survey not found")

    def create(
        self,
        name: str,
        external_id: str,
        crs: str,
        metadata: Dict[str, str] = {},
        grid_transformation: Optional[SurveyGridTransformation] = None,
        custom_coverage_wkt: Optional[str] = None,
        custom_coverage_geojson: Optional[dict] = None,
    ) -> Survey:
        """Creates a survey with the provided characteristics.

        Args:
            name (str): survey name.
            metadata (Dict[str, str], optional): metadata of the survey.
            external_id (str): external id of the survey.
            crs (str): Coordinate reference system to be used by all members of this survey.
                Specified as an EPSG reference code in the format "EPSG:####".
            grid_transformation (:py:class:`~cognite.seismic.SurveyGridTransformation`, optional):
                Manually specify an affine transformation between bin grid
                coordinates and projected crs coordinates, either using an
                origin point and the azimuth of the xline axis
                (:py:class:`~cognite.seismic.P6Transformation`);
                by specifying three or more corners of the grid
                (:py:class:`~cognite.seismic.CoordList`);
                or by asking the seismic service to deduce the transformation from the traces
                in each file (:py:class:`~cognite.seismic.DeduceFromTraces`).

                This transformation must be valid for all the files in this survey.
            custom_coverage_wkt (str, optional):
                Specify a custom coverage polygon for this survey in the wkt format
            custom_coverage_geojson (dict, optional):
                Specify a custom coverage polygon for this survey in the geojson format

        Returns:
            :py:class:`~cognite.seismic.data_classes.api_types.Survey`
        """
        # Creating the custom coverage field
        if custom_coverage_wkt is not None:
            wkt = Wkt(geometry=custom_coverage_wkt)
            coverage = CustomSurveyCoverage(custom_coverage=GeometryProto(crs=CRS(crs=crs), wkt=wkt))
        elif custom_coverage_geojson is not None:
            coverage = CustomSurveyCoverage(
                custom_coverage=GeometryProto(crs=CRS(crs=crs), geo=GeoJson(json=custom_coverage_wkt))
            )
        else:
            coverage = CustomSurveyCoverage(no_custom_coverage=CustomSurveyCoverage.NoCustomCoverage())

        request = CreateSurveyRequest(
            name=name,
            metadata=metadata,
            external_id=ExternalId(external_id=external_id),
            crs=crs,
            custom_coverage=coverage,
        )
        if grid_transformation is not None:
            request.grid_transformation.MergeFrom(grid_transformation._to_proto())

        return Survey._from_proto_survey(self.seismic.CreateSurvey(request))

    def edit(
        self,
        id: Optional[int] = None,
        external_id: Optional[str] = None,
        metadata: Dict[str, str] = {},
        new_external_id: Optional[str] = None,
        crs: Optional[str] = None,
        grid_transformation: Optional[SurveyGridTransformation] = None,
        custom_coverage_wkt: Optional[str] = None,
        custom_coverage_geojson: Optional[dict] = None,
        clear_custom_coverage: Optional[bool] = False,
        name: Optional[str] = None,
    ):
        """Edit a survey
        This method replaces fields in an existing survey identified by either its id or external_id.
        Method parameters that are non-null will be used to replace the corresponding field in the survey
        object. Null (unspecified) method parameters will not affect a change to the survey object.

        Args:
            id (int, optional): integer id of the survey to edit.
            external_id (str, optional): external id of the survey to edit.
                Either id or external_id must be specified.
            metadata (dict): metadata to be used by the survey.
            new_external_id (str, optional): External id to be used by the survey.
            crs (str, optional): Coordinate reference system to be used by all members of this survey
            grid_transformation (:py:class:`~cognite.seismic.SurveyGridTransformation`, optional):
                Manually specify an affine transformation between bin grid
                coordinates and projected crs coordinates, either using an
                origin point and the azimuth of the xline axis
                (:py:class:`~cognite.seismic.P6Transformation`);
                by specifying three or more corners of the grid
                (:py:class:`~cognite.seismic.CoordList`);
                or by asking the seismic service to deduce the transformation from the traces
                in each file (:py:class:`~cognite.seismic.DeduceFromTraces`).

                This transformation must be valid for all members of this survey.
            custom_coverage_wkt (str, optional):
                Specify a custom coverage polygon for this survey in the wkt format
            custom_coverage_geojson (dict, optional):
                Specify a custom coverage polygon for this survey in the geojson format
            clear_custom_coverage (bool, optional):
                Set this to True to clear the custom coverage from this survey, so that coverage is
                computed as a union of the coverage of the data sets included in the survey.
            name (str, optional): new name for the survey.
        Returns:
            :py:class:`~cognite.seismic.Survey`: id, name and metadata of the survey.
        """

        survey = _get_identifier(id, external_id)

        if clear_custom_coverage and (custom_coverage_wkt or custom_coverage_geojson):
            raise Exception("Provide a custom_coverage or set clear_custom_coverage, but not both")
        if custom_coverage_wkt is not None:
            geometry = GeometryProto(wkt=Wkt(geometry=custom_coverage_wkt))
            if crs is not None:
                geometry.crs.MergeFrom(CRS(crs=crs))
            coverage = CustomSurveyCoverage(custom_coverage=geometry)
        elif custom_coverage_geojson is not None:
            geo_json_struct = Struct()
            geo_json_struct.update(custom_coverage_geojson)
            geometry = GeometryProto(geo=GeoJson(json=geo_json_struct))
            if crs is not None:
                geometry.crs.MergeFrom(CRS(crs=crs))
            coverage = CustomSurveyCoverage(custom_coverage=geometry)
        elif clear_custom_coverage:
            coverage = CustomSurveyCoverage(no_custom_coverage=CustomSurveyCoverage.NoCustomCoverage())
        else:
            coverage = None

        metadata_param = OptionalMap(data=metadata) if metadata else None
        new_external_id_param = ExternalId(external_id=new_external_id) if new_external_id else None
        name_param = StringValue(value=name) if name else None

        request = EditSurveyRequest(
            survey=survey,
            metadata=metadata_param,
            external_id=new_external_id_param,
            custom_coverage=coverage,
            new_name=name_param,
        )
        if grid_transformation is not None:
            request.grid_transformation.MergeFrom(grid_transformation._to_proto())
        if crs is not None:
            request.crs.MergeFrom(CRS(crs=crs))

        return Survey._from_proto_survey(self.seismic.EditSurvey(request))

    def delete(self, id: Optional[int] = None, external_id: Optional[str] = None):
        """Delete a survey

        Args:
            id (int, optional): Integer id of the survey to delete
            external_id (str, optional): External id of the survey to delete
        """
        if id is None and external_id is None:
            raise InvalidArgumentError("Must specify either id or external_id")
        self.seismic.DeleteSurvey(DeleteSurveyRequest(survey=_get_identifier(id, external_id)))

    def _search_internal(
        self,
        search_specs: List["SearchSpec"],
        last_modified: Optional["LastModifiedFilter"],
        list_seismics: bool = False,
        list_seismic_stores: bool = False,
        include_metadata: bool = False,
        coverage_crs: Optional[str] = None,
        coverage_format: Optional[str] = None,
        include_grid_transformation: Optional[bool] = False,
        include_custom_coverage: Optional[bool] = False,
        coverage_source: SurveyCoverageSource = SurveyCoverageSource.UNSPECIFIED,
    ) -> Iterator[Survey]:
        coverage_spec = None
        if coverage_crs is not None or coverage_format is not None:
            coverage_spec = _get_coverage_spec(coverage_crs, coverage_format)
        request = SearchSurveysRequest(
            surveys=search_specs,
            list_seismic_ids=list_seismics,
            list_seismic_store_ids=list_seismic_stores,
            include_metadata=include_metadata,
            coverage=coverage_spec,
            include_grid_transformation=include_grid_transformation or False,
            include_custom_coverage=include_custom_coverage or False,
            coverage_source=coverage_source.value,
            last_modified=last_modified,
        )
        return (Survey._from_proto(survey_proto) for survey_proto in self.seismic.SearchSurveys(request))
