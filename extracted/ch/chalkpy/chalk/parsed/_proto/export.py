import collections
import os
from datetime import timedelta
from pathlib import Path
from typing import Collection, List, Optional, Sequence, Tuple

import chalk._gen.chalk.artifacts.v1.export_pb2 as export_pb
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as chart_pb
from chalk._gen.chalk.artifacts.v1.cdc_pb2 import CDCSource, CDCTableReference
from chalk._gen.chalk.artifacts.v1.cron_query_pb2 import CronQuery, RecomputeSettings
from chalk._gen.chalk.common.v1 import chalk_error_pb2
from chalk._gen.chalk.lsp.v1 import lsp_pb2
from chalk._lsp.error_builder import LSPErrorBuilder
from chalk._monitoring.Chart import Chart as _Chart
from chalk._monitoring.proto_conversion import convert_chart
from chalk._version import __version__
from chalk.client import ChalkError, ChalkException, ErrorCode, ErrorCodeCategory
from chalk.client.serialization.protos import ChalkErrorConverter
from chalk.config.project_config import ProjectSettings, load_project_config
from chalk.features import FeatureSetBase
from chalk.features.resolver import RESOLVER_REGISTRY
from chalk.importer import CHALK_IMPORTER, import_all_files
from chalk.parsed._proto.lsp import convert_lsp_gql_to_proto
from chalk.parsed._proto.utils import (
    build_failed_import,
    convert_failed_import_to_gql,
    convert_failed_import_to_proto,
    datetime_to_proto_timestamp,
)
from chalk.parsed._proto.validation import validate_artifacts
from chalk.parsed.to_proto import ToProtoConverter
from chalk.parsed.user_types_to_json import get_lsp_gql
from chalk.queries.named_query import NAMED_QUERY_REGISTRY
from chalk.queries.scheduled_query import CRON_QUERY_REGISTRY
from chalk.sql._internal.sql_source import BaseSQLSource, TableIngestMixIn
from chalk.sql._internal.sql_source_group import SQLSourceGroup
from chalk.streams import StreamSource
from chalk.utils.duration import timedelta_to_duration


def project_settings_to_proto(config: ProjectSettings) -> export_pb.ProjectSettings:
    environments: List[export_pb.EnvironmentSettings] = []
    envs = config.environments
    if envs is not None:
        environments = [
            export_pb.EnvironmentSettings(
                id=env_id,
                runtime=e.runtime,
                requirements=e.requirements,
                dockerfile=e.dockerfile,
                requires_packages=None,
                platform_version=e.platform_version,
            )
            for env_id, e in envs.items()
        ]

    validation: Optional[export_pb.ValidationSettings] = None
    if config.validation:
        feature_settings: Optional[export_pb.FeatureSettings] = None
        if config.validation.feature:
            metadata_settings = (
                [export_pb.MetadataSettings(name=m.name, missing=m.missing) for m in config.validation.feature.metadata]
                if config.validation.feature.metadata
                else None
            )
            feature_settings = export_pb.FeatureSettings(metadata=metadata_settings)

        resolver_settings: Optional[export_pb.ResolverSettings] = None
        if config.validation.resolver:
            metadata_settings = (
                [
                    export_pb.MetadataSettings(name=m.name, missing=m.missing)
                    for m in config.validation.resolver.metadata
                ]
                if config.validation.resolver.metadata
                else None
            )
            resolver_settings = export_pb.ResolverSettings(metadata=metadata_settings)

        validation = export_pb.ValidationSettings(
            feature=feature_settings,
            resolver=resolver_settings,
        )

    return export_pb.ProjectSettings(
        project=config.project,
        environments=environments,
        validation=validation,
    )


def import_files_then_export_from_registry(
    directory: Optional[str], file_allowlist: Optional[List[str]]
) -> export_pb.Export:
    """
    Packaged into a function just so that the caller can try-except this.
    """
    if directory is not None:
        os.chdir(directory)
    failed_imports_gql = import_all_files(
        file_allowlist=file_allowlist,
        project_root=None if directory is None else Path(directory),
    )
    export = export_from_registry()
    export.failed.extend([convert_failed_import_to_proto(f) for f in failed_imports_gql])

    return export


def get_lsp_proto_or_error(
    additional_failed_import_protos: Sequence[export_pb.FailedImport],
) -> Tuple[lsp_pb2.LSP, Optional[ChalkException]]:
    """
    :param additional_failed_import_protos:  Supplementary failed imports to add as lsp diagnostics
    :return: A tuple [LSP, error | None]. If generating the LSP threw an exception, return the partial LSP and a serialized form of the error for reporting.
    """
    lsp = get_lsp_gql()
    exc: Optional[ChalkException] = None
    if LSPErrorBuilder.lsp:
        failed_gql = [convert_failed_import_to_gql(f) for f in additional_failed_import_protos]
        try:
            # Modified lsp.diagnostics in-place to add info.
            # if we throw an exception due to bad state, we'll still have the errors we've collected so far
            CHALK_IMPORTER.supplement_diagnostics(failed_imports=failed_gql, diagnostics=lsp.diagnostics)
        except Exception as e:
            if len(lsp.diagnostics) == 0 and len(failed_gql) == 0:
                exc = ChalkException.from_exception(e)
    return convert_lsp_gql_to_proto(lsp), exc


def get_lsp_proto(
    additional_failed_import_protos: Sequence[export_pb.FailedImport],
) -> lsp_pb2.LSP:
    lsp, _ = get_lsp_proto_or_error(additional_failed_import_protos)
    return lsp


def export_from_registry() -> export_pb.Export:
    """
    This is separate from trying to `import_all_files` so that
    we can use this function in places where import is already
    done, like the engine.
    """
    failed_protos: List[export_pb.FailedImport] = []

    graph_res = ToProtoConverter.convert_graph(
        features_registry=FeatureSetBase.registry,
        resolver_registry=RESOLVER_REGISTRY.get_all_resolvers(),
        sql_source_registry=BaseSQLSource.registry,
        sql_source_group_registry=SQLSourceGroup.registry,
        stream_source_registry=StreamSource.registry,
        named_query_registry=NAMED_QUERY_REGISTRY,
    )

    crons: List[CronQuery] = []
    for cron in CRON_QUERY_REGISTRY.values():
        if not isinstance(cron.recompute_features, (Collection, bool)):  # pyright: ignore[reportUnnecessaryIsInstance]
            failed_protos.append(
                build_failed_import(
                    TypeError(f"Invalid `recompute_features` type '{type(cron.recompute_features).__name__}'"),
                    f"cron '{cron.name}'",
                )
            )
            continue
        crons.append(
            CronQuery(
                name=cron.name,
                cron=timedelta_to_duration(cron.cron) if isinstance(cron.cron, timedelta) else cron.cron,
                output=[str(f) for f in cron.output],
                max_samples=cron.max_samples,
                recompute=RecomputeSettings(
                    feature_fqns=list(cron.recompute_features)
                    if isinstance(cron.recompute_features, Collection)
                    else None,
                    all_features=cron.recompute_features  # pyright: ignore[reportArgumentType]
                    if isinstance(cron.recompute_features, bool)
                    else None,
                ),
                lower_bound=datetime_to_proto_timestamp(cron.lower_bound)
                if cron.lower_bound is not None
                else cron.lower_bound,
                upper_bound=datetime_to_proto_timestamp(cron.upper_bound)
                if cron.upper_bound is not None
                else cron.upper_bound,
                tags=cron.tags,
                required_resolver_tags=cron.required_resolver_tags,
                store_online=cron.store_online,
                store_offline=cron.store_offline,
                file_name=cron.filename,
                resource_group=cron.resource_group,
                planner_options=cron.planner_options,
            )
        )

    charts: List[chart_pb.Chart] = []
    for chart in _Chart.registry:
        try:
            charts.append(convert_chart(chart))
        except Exception as e:
            failed_protos.append(build_failed_import(e, f"chart ' {chart.name}'"))

    integration_name_to_tables = collections.defaultdict(list)
    for source in BaseSQLSource.registry:
        if isinstance(source, TableIngestMixIn):
            for schema_dot_table, preferences in source.ingested_tables.items():
                if preferences.cdc is True:
                    assert isinstance(source, BaseSQLSource)
                    parts = schema_dot_table.split(".")
                    if len(parts) != 2:
                        build_failed_import(
                            f"Expected {{schema}}.{{table}}, got {schema_dot_table}", f"Database source '{source.name}'"
                        )
                        continue
                    integration_name_to_tables[source.name].append(CDCTableReference(schema=parts[0], name=parts[1]))
    cdc_sources = [
        CDCSource(
            integration_name=integration_name,
            tables=tables,
        )
        for integration_name, tables in integration_name_to_tables.items()
    ]

    config = load_project_config()
    if config is not None:
        config = project_settings_to_proto(config)

    # Has side effect of populating LSPErrorBuilder
    logs = validate_artifacts(graph_res, config)

    # Get proto of currently logged LSP diagnostics
    lsp, exc = get_lsp_proto_or_error(failed_protos)
    errors: List[chalk_error_pb2.ChalkError] = []
    if exc is not None:
        err = ChalkError.create(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            category=ErrorCodeCategory.NETWORK,
            message=f"Failed to export features: {exc.message}",
            exception=exc,
        )
        errors.append(ChalkErrorConverter.chalk_error_encode(err))

    return export_pb.Export(
        graph=graph_res,
        crons=crons,
        charts=charts,
        chalkpy=export_pb.ChalkpyInfo(version=__version__),
        cdc_sources=cdc_sources,
        config=config,
        logs=logs,
        lsp=lsp,
        failed=failed_protos,
        conversion_errors=errors,
    )
