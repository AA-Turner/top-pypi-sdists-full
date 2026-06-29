import collections
import os
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Collection, Iterable, List, Optional, Sequence, Tuple

if TYPE_CHECKING:
    from chalk.features.feature_set import Features
    from chalk.ml.model_reference import ModelReference
    from chalk.queries.named_query import NamedQuery
    from chalk.queries.scheduled_aggregate_backfill import ScheduledAggregateBackfill
    from chalk.queries.scheduled_query import ScheduledQuery
    from chalk.stores.online_store_config import OnlineStoreConfig

import chalk._gen.chalk.artifacts.v1.export_pb2 as export_pb
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as chart_pb
from chalk._gen.chalk.artifacts.v1 import cron_aggregate_backfill_pb2 as cron_aggregate_backfill_pb
from chalk._gen.chalk.artifacts.v1.cdc_pb2 import CDCSource, CDCTableReference
from chalk._gen.chalk.artifacts.v1.cron_query_pb2 import CronQuery, RecomputeSettings
from chalk._gen.chalk.common.v1 import chalk_error_pb2
from chalk._gen.chalk.common.v1.offline_query_pb2 import UnloadResolverSpec
from chalk._gen.chalk.lsp.v1 import lsp_pb2
from chalk._lsp.error_builder import LSPErrorBuilder
from chalk._monitoring.Chart import Chart as _Chart
from chalk._monitoring.proto_conversion import convert_chart
from chalk._version import __version__
from chalk.client import ChalkError, ChalkException, ErrorCode, ErrorCodeCategory
from chalk.client.serialization.protos import ChalkErrorConverter
from chalk.config.project_config import ProjectSettings, load_project_config
from chalk.features import FeatureSetBase
from chalk.features.resolver import RESOLVER_REGISTRY, ResolverRegistry
from chalk.importer import CHALK_IMPORTER, import_all_files
from chalk.ml.model_reference import MODEL_REFERENCE_REGISTRY
from chalk.parsed._proto.global_variables import (
    get_function_capture_global_variable_values,
    get_global_variables_info_from_export,
)
from chalk.parsed._proto.lsp import convert_lsp_gql_to_proto
from chalk.parsed._proto.utils import (
    build_failed_import,
    convert_failed_import_to_gql,
    convert_failed_import_to_proto,
    datetime_to_proto_timestamp,
    timedelta_to_proto_duration,
)
from chalk.parsed._proto.validation import validate_artifacts
from chalk.parsed.to_proto import ToProtoConverter
from chalk.parsed.user_types_to_json import get_lsp_gql
from chalk.queries.named_query import NAMED_QUERY_REGISTRY
from chalk.queries.scheduled_aggregate_backfill import SCHEDULED_AGGREGATE_BACKFILL_REGISTRY, AggregateBackfillTarget
from chalk.queries.scheduled_query import CRON_QUERY_REGISTRY, lint_incremental_resolvers
from chalk.sql._internal.sql_source import BaseSQLSource, TableIngestMixIn
from chalk.sql._internal.sql_source_group import SQLSourceGroup
from chalk.stores.online_store_config import ONLINE_STORE_CONFIG_REGISTRY
from chalk.streams import StreamSource
from chalk.utils.duration import timedelta_to_duration

__all__ = [
    "export_from_registry",
    "get_function_capture_global_variable_values",
    "get_global_variables_info_from_export",
    "get_lsp_proto",
    "get_lsp_proto_or_error",
    "import_files_then_export_from_registry",
]


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
    directory: Optional[str],
    file_allowlist: Optional[List[str]],
    *,
    include_captured_global_values: bool = False,
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
    export = export_from_registry(include_captured_global_values=include_captured_global_values)
    export.failed.extend([convert_failed_import_to_proto(f) for f in failed_imports_gql])

    return export


def get_lsp_proto_or_error(
    additional_failed_import_protos: Sequence[export_pb.FailedImport],
) -> Tuple[lsp_pb2.LSP, Optional[ChalkException]]:
    """
    Parameters
    ----------
    additional_failed_import_protos
        Supplementary failed imports to add as LSP diagnostics.

    Returns
    -------
    Tuple[lsp_pb2.LSP, Optional[ChalkException]]
        A tuple `[LSP, error | None]`. If generating the LSP throws an exception, returns the partial
        LSP and a serialized form of the error for reporting.
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


def export_from_registry(*, include_captured_global_values: bool = False) -> export_pb.Export:
    """
    This is separate from trying to `import_all_files` so that
    we can use this function in places where import is already
    done, like the engine.
    """
    return export_from_registries(
        features_registry=FeatureSetBase.registry,
        resolver_registry=RESOLVER_REGISTRY,
        sql_source_registry=BaseSQLSource.registry,
        sql_source_group_registry=SQLSourceGroup.registry,
        stream_source_registry=StreamSource.registry,
        named_query_registry=NAMED_QUERY_REGISTRY,
        model_reference_registry=MODEL_REFERENCE_REGISTRY,
        online_store_config_registry=ONLINE_STORE_CONFIG_REGISTRY,
        cron_query_registry=CRON_QUERY_REGISTRY,
        scheduled_aggregate_backfill_registry=SCHEDULED_AGGREGATE_BACKFILL_REGISTRY,
        chart_registry=_Chart.registry,
        include_captured_global_values=include_captured_global_values,
    )


def export_from_registries(
    *,
    features_registry: "dict[str, type[Features]]",
    resolver_registry: "ResolverRegistry",
    sql_source_registry: Sequence[BaseSQLSource],
    sql_source_group_registry: Sequence[SQLSourceGroup],
    stream_source_registry: Sequence[StreamSource],
    named_query_registry: "dict[tuple[str, Optional[str]], NamedQuery]",
    model_reference_registry: "dict[tuple[str, str], ModelReference]",
    online_store_config_registry: "dict[str, OnlineStoreConfig]",
    cron_query_registry: "dict[str, ScheduledQuery]",
    scheduled_aggregate_backfill_registry: "dict[str, ScheduledAggregateBackfill]",
    chart_registry: Iterable[_Chart],
    include_captured_global_values: bool = False,
) -> export_pb.Export:
    """Build an Export proto from explicit registry inputs.

    `export_from_registry` is the production wrapper that pulls from the
    process-wide globals; this entrypoint exists so tests (and other callers
    that already have isolated registries) can drive the full export pipeline
    without inheriting whatever else is registered in the process.
    """
    failed_protos: List[export_pb.FailedImport] = []

    # This is a no-op UNLESS the project itself called `override_feature_tags`.
    # When (and only when) the customer has opted in, apply their centrally-
    # declared feature-tag overrides here, BEFORE validation and conversion;
    # otherwise code-defined tags are left exactly as written. Because the
    # registry is fully populated by this point, an opted-in project gets the
    # authoritative last word on feature tags: every code-defined tag is wiped
    # and only the declared ones are stamped on, regardless of which file defined
    # the feature or what order it was imported.
    from chalk.features.feature_tag_override import apply_feature_tag_overrides

    apply_feature_tag_overrides(features_registry)

    # Validate registries BEFORE conversion to catch errors early
    # This ensures parity with GQL validation path
    from chalk.parsed.validation_from_registries import (
        validate_all_from_registries,
        validate_scheduled_agg_backfill_from_registries,
    )

    try:
        validate_all_from_registries(
            features_registry=features_registry,
            resolver_registry=resolver_registry,
        )
    except Exception as e:
        # If validation fails, add to failed_protos but continue
        # to allow other validation to complete
        from chalk._lsp.error_builder import LSPErrorBuilder

        if not LSPErrorBuilder.promote_exception(e):
            # Not an LSP error, so log it as a failed import
            failed_protos.append(build_failed_import(e, "validation"))

    graph_res = ToProtoConverter.convert_graph(
        features_registry=features_registry,
        resolver_registry=resolver_registry.get_all_resolvers(),
        sql_source_registry=sql_source_registry,
        sql_source_group_registry=sql_source_group_registry,
        stream_source_registry=stream_source_registry,
        named_query_registry=named_query_registry,
        model_reference_registry=model_reference_registry,
        online_store_config_registry=online_store_config_registry,
    )

    crons: List[CronQuery] = []
    for cron in cron_query_registry.values():
        if cron.errors:
            failed_protos.append(
                build_failed_import(
                    "\n".join(cron.errors),
                    f"scheduled query '{cron.name}'",
                )
            )
            continue
        if not isinstance(cron.recompute_features, (Collection, bool)):  # pyright: ignore[reportUnnecessaryIsInstance]
            failed_protos.append(
                build_failed_import(
                    TypeError(f"Invalid `recompute_features` type '{type(cron.recompute_features).__name__}'"),
                    f"cron '{cron.name}'",
                )
            )
            continue

        lint_incremental_resolvers(cron, resolver_registry)

        # Build resources proto from ResourceRequests if present
        resources_proto = None
        if cron.resources is not None:
            from chalk._gen.chalk.common.v1.offline_query_pb2 import ResourceRequests as ProtoResourceRequests

            resources_proto = ProtoResourceRequests(
                cpu=cron.resources.cpu,
                memory=cron.resources.memory,
                ephemeral_storage=cron.resources.ephemeral_storage,
                ephemeral_volume_size=cron.resources.ephemeral_volume_size,
                resource_group=cron.resources.resource_group,
            )

        crons.append(
            CronQuery(
                name=cron.name,
                cron=timedelta_to_duration(cron.cron) if isinstance(cron.cron, timedelta) else cron.cron,
                output=[str(f) for f in cron.output],
                max_samples=cron.max_samples,
                recompute=RecomputeSettings(
                    feature_fqns=(
                        list(cron.recompute_features) if isinstance(cron.recompute_features, Collection) else None
                    ),
                    all_features=(
                        cron.recompute_features  # pyright: ignore[reportArgumentType]
                        if isinstance(cron.recompute_features, bool)
                        else None
                    ),
                ),
                lower_bound=(
                    datetime_to_proto_timestamp(cron.lower_bound) if cron.lower_bound is not None else cron.lower_bound
                ),
                upper_bound=(
                    datetime_to_proto_timestamp(cron.upper_bound) if cron.upper_bound is not None else cron.upper_bound
                ),
                tags=cron.tags,
                required_resolver_tags=cron.required_resolver_tags,
                store_online=cron.store_online,
                store_offline=cron.store_offline,
                file_name=cron.filename,
                resource_group=cron.resource_group,
                planner_options=cron.planner_options,
                completion_deadline=(
                    timedelta_to_proto_duration(cron.completion_deadline)
                    if cron.completion_deadline is not None
                    else cron.completion_deadline
                ),
                num_shards=cron.num_shards,
                num_workers=cron.num_workers,
                input_sql=cron.input_sql,
                unload_resolvers=[
                    UnloadResolverSpec(
                        fqn="all" if "any" in spec else spec["fqn"],
                        partition_by=[] if "any" in spec else spec.get("partition_by", []),
                    )
                    for spec in (cron.unload_resolvers or [])
                ],
                max_retries=cron.max_retries,
                resources=resources_proto,
                environment_override=cron.environment,
            )
        )

    cron_aggregate_backfills: List[cron_aggregate_backfill_pb.CronAggregateBackfill] = []
    for backfill in scheduled_aggregate_backfill_registry.values():
        if backfill.errors:
            failed_protos.append(
                build_failed_import(
                    "\n".join(backfill.errors),
                    f"scheduled aggregate backfill '{backfill.name}'",
                )
            )
            continue

        validation_errors = validate_scheduled_agg_backfill_from_registries(backfill, features_registry)
        if validation_errors:
            failed_protos.append(
                build_failed_import(
                    "\n".join(validation_errors),
                    f"scheduled aggregate backfill '{backfill.name}'",
                )
            )
            continue

        proto_target_by_storage_target = {
            AggregateBackfillTarget.ONLINE: cron_aggregate_backfill_pb.CRON_AGGREGATE_BACKFILL_TARGET_ONLINE,
            AggregateBackfillTarget.OFFLINE: cron_aggregate_backfill_pb.CRON_AGGREGATE_BACKFILL_TARGET_OFFLINE,
        }
        proto_targets = [proto_target_by_storage_target[target] for target in backfill.targets]
        cron_aggregate_backfills.append(
            cron_aggregate_backfill_pb.CronAggregateBackfill(
                name=backfill.name,
                features=backfill.features,
                schedule=(
                    timedelta_to_duration(backfill.schedule)
                    if isinstance(backfill.schedule, timedelta)
                    else backfill.schedule
                ),
                target=proto_targets[0],  # backwards-compatibility
                targets=proto_targets,
                query_tags=backfill.query_tags,
                resource_group=backfill.resource_group,
                lower_bound=(
                    datetime_to_proto_timestamp(backfill.lower_bound)
                    if backfill.lower_bound is not None
                    else backfill.lower_bound
                ),
                upper_bound=(
                    datetime_to_proto_timestamp(backfill.upper_bound)
                    if backfill.upper_bound is not None
                    else backfill.upper_bound
                ),
                allow_empty_tiles=backfill.allow_empty_tiles,
                # environment is passed only when set; the proto field is added in
                # artifacts.v1.CronAggregateBackfill (Layer 2) and None would raise on older stubs.
                **({"environment": backfill.environment} if backfill.environment is not None else {}),
            )
        )

    charts: List[chart_pb.Chart] = []
    for chart in chart_registry:
        try:
            charts.append(convert_chart(chart))
        except Exception as e:
            failed_protos.append(build_failed_import(e, f"chart ' {chart.name}'"))

    integration_name_to_tables = collections.defaultdict(list)
    for source in sql_source_registry:
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

    export = export_pb.Export(
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
        cron_aggregate_backfills=cron_aggregate_backfills,
    )
    if include_captured_global_values:
        export.captured_global_variables.CopyFrom(get_global_variables_info_from_export(export))
    return export
