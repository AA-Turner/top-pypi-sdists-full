import os.path
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Union, Optional

import typer

from bigeye_sdk.bigconfig_validation.big_config_reports import (
    raise_files_contain_error_exception,
    MetricSuiteReport,
    process_reports,
    ProcessStage,
    REPORTS,
)
from bigeye_sdk.bigconfig_validation.validation_context import (
    process_validation_errors,
    get_validation_error_cnt,
    get_all_validation_errors_flat,
)
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import (
    SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG,
    METRIC_APPLICATION_ERROR,
    MISMATCHED_ATTRIBUTE_ACROSS_MULTIPLE_FILES,
)
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.exceptions.exceptions import (
    FileLoadException,
    BigConfigValidationException,
    NoSourcesFoundException,
    FileNotFoundException,
)
from bigeye_sdk.functions.metric_functions import _is_table_level_metric, metric_template_has_name_without_id
from bigeye_sdk.functions.search_and_match_functions import wildcard_search
from bigeye_sdk.generated.com.bigeye.models.generated import (
    Source,
    CohortDefinition,
    MetricSuite,
    CohortAndMetricDefinition,
    CatalogEntityType,
    MetricDefinition,
    FieldType,
    NamedSchedule,
    PredefinedMetricName,
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.big_config import (
    BigConfig,
    RowCreationTimes,
    TagDeployment,
    TableDeployment,
    SavedMetricDefinitions,
    ColumnSelector,
)
from bigeye_sdk.model.protobuf_enum_facade import (
    SimplePredefinedMetricName,
    SimpleLookbackType,
)
from bigeye_sdk.model.protobuf_message_facade import (
    SimpleCollection,
    SimpleMetricDefinition,
    SimpleSLA,
    SimpleLookback, SimpleTemplateMetric,
)

from bigeye_sdk.serializable import File, BIGCONFIG_FILE

log = get_logger(__name__)


def get_fq_name_from_cohort(cohort: CohortDefinition, source_name: str = None):
    """
    Args:
        cohort: cohort for which to get fully_qualified_name
        source_name: (optional) if available will prepend source name.

    Returns: fully qualified name
    """
    if cohort.column_name_pattern:
        r = f"{cohort.schema_name_pattern}.{cohort.table_name_pattern}.{cohort.column_name_pattern}"
    else:
        r = f"{cohort.schema_name_pattern}.{cohort.table_name_pattern}"

    if not source_name:
        return r
    else:
        return f"{source_name}.{r}"


def _find_bigconfig_files(
        input_paths: List[str] = [], recursive: bool = False
) -> List[BIGCONFIG_FILE]:
    """
    Finds bigconfig files either in specified input path or in working directory
    Args:
        input_paths: specify List of input paths or working directory will be used.

    Returns: None

    """
    files: List[Path] = []
    for ip in input_paths:
        if os.path.isfile(ip):
            files.append(Path(ip))
        elif recursive:
            files.extend(list(Path(ip).rglob("*.y*ml")))
        else:
            files.extend(list(Path(ip).glob("*.y*ml")))

    if not files:
        """No YAML files were found at the given input path or current working directory, raise error for user to fix input paths."""
        raise FileNotFoundException(
            f"No YAML files for the given input paths or current working directory were found."
        )

    bigeye_files: List[BIGCONFIG_FILE] = []
    file: BIGCONFIG_FILE
    load_errs = []
    for file in files:
        try:
            """
            Loading Bigconfig YAML.  If file is not of Bigconfig type then the error will be caught and passed. If file
            is not valid YAML, then an exception will be thrown.
            """
            bigeye_files.append(File.load(str(file)))
        except FileLoadException as e:
            load_err = f"File {file} failed to load with error: {str(e.message)}"
            load_errs.append(load_err)
            log.warning(load_err)

    if len(bigeye_files) == 0:
        errors = "\n\n=========\n\n".join(load_errs)
        err = f"No conforming files found. There may be a formatting issue with the yaml.\nErrors found:\n{errors}"
        raise BigConfigValidationException(err)

    else:
        return bigeye_files


class MetricSuiteController:

    def __init__(self, client: DatawatchClient):
        self.client = client

        self.sources_by_name_ix: Dict[str, Source] = self.client.get_sources_by_name()
        self.sources_by_id_ix: Dict[int, Source] = {
            v.id: v for k, v in self.sources_by_name_ix.items()
        }
        self.bigeye_users: Optional[Dict[str, int]] = None
        self.templates_from_bigeye: Dict[str, int] = {}

        self.table_level_metrics: List[SimplePredefinedMetricName] = self._get_table_level_metric_names()

    def _get_table_level_metric_names(self):
        # Filter out values that don't exist in the SDK, if generated.py has not been updated
        raw_response = self.client.get_table_level_metrics_raw()
        metric_names = []
        for n in raw_response['metricNames']:
            try:
                metric_names.append(PredefinedMetricName.from_string(n))
            except ValueError as e:
                log.info(f"Error trying to create PredefinedMetric with {e}. Skipping to next")
        return [
            SimplePredefinedMetricName.from_datawatch_object(pmn)
            for pmn in metric_names
        ]

    def _upsert_collections(
            self, bigconfig: BigConfig, overwrite: bool, apply=False
    ) -> List[Union[SimpleSLA, SimpleCollection]]:
        """
        Currently operates as an overwrite of existing metrics.  This prevents altering in the front end.  Every time the
        config is run it will overwrite what is already there.  Does not add metrics.
        Args:
            bigconfig: Bigconfig.

        Returns: a list of upserted SLAs

        """
        existing_collections = {
            c.name: c for c in self.client.get_collections().collections
        }
        merged_or_new: SimpleCollection
        deployment_collections = []

        for collection in bigconfig.get_collections():
            if collection.name in existing_collections.keys():
                """If the collection exists, send the collection ID as part of a plan and only update for apply"""
                existing = SimpleCollection.from_datawatch_object(
                    existing_collections[collection.name]
                )
                merged_or_new = collection.merge_for_upsert(existing=existing)
                deployment_collections.append(merged_or_new)
                if apply and existing != merged_or_new:
                    self.client.update_collection(
                        collection=merged_or_new.to_datawatch_object()
                    )
            elif apply:
                """If it doesn't exist, only create it during apply"""
                c = collection.to_datawatch_object()
                c = self.client.create_collection(
                    collection_name=c.name,
                    description=c.description,
                    metric_ids=c.metric_ids,
                    notification_channels=c.notification_channels,
                    muted_until_timestamp=c.muted_until_timestamp,
                ).collection
                merged_or_new = SimpleCollection.from_datawatch_object(c)
                existing_collections[c.name] = c
                deployment_collections.append(merged_or_new)

        return deployment_collections

    def _get_matching_source_ids(
            self, column_selector: ColumnSelector, source_include_pattern: str
    ) -> List[int]:
        source_ids_to_include = [
            source.id
            for source_name, source in self.sources_by_name_ix.items()
            if source_name
               in wildcard_search(
                search_string=source_include_pattern,
                content=[source_name],
                is_raw_regex=column_selector.is_raw_regex(),
            )
        ]
        return source_ids_to_include

    def _update_metric_definition_for_deployment(self,
                                                 m: SimpleMetricDefinition,
                                                 named_schedules: List[NamedSchedule],
                                                 default_lookback: SimpleLookback,
                                                 deployment_collection: Union[SimpleSLA, SimpleCollection]
                                                 ) -> Optional[SimpleMetricDefinition]:
        if (
                deployment_collection
                and deployment_collection.id not in m.collection_ids
        ):
            m.collection_ids.append(deployment_collection.id)
        if m.metric_schedule and m.metric_schedule.named_schedule:
            try:
                m.metric_schedule.named_schedule.id = [
                    s.id
                    for s in named_schedules
                    if s.name == m.metric_schedule.named_schedule.name
                ][0]
            except IndexError:
                log.warning(
                    f"The schedule '{m.metric_schedule.named_schedule.name}' does not exist in workspace {self.client.config.workspace_id}"
                )
                log.warning("The metric will be created with no schedule.")
                log.info(
                    "Create the schedule via the CLI or the UI and the metric will be updated with the next deployment."
                )
                m.metric_schedule = None
        if isinstance(m.metric_type, SimpleTemplateMetric) and metric_template_has_name_without_id(m.metric_type):
            try:
                if not self.templates_from_bigeye.get(m.metric_type.template_name.lower()):
                    template = [
                        t for t in self.client.get_all_metric_templates(search=m.metric_type.template_name)
                        if t.name.lower() == m.metric_type.template_name.lower()
                    ][0]
                    self.templates_from_bigeye[template.name.lower()] = template.id

                m.metric_type.template_id = self.templates_from_bigeye[m.metric_type.template_name.lower()]
            except IndexError:
                log.warning(
                    f"No template found with name {m.metric_type.template_name}. Metric will not be created."
                )
                return None

        m.user_favorites = self._generate_tags_for_favorites(m.user_favorites)
        m.owner = self._get_owner_id(m.owner)

        if not m.lookback:
            m.lookback = default_lookback

        return m

    def row_creation_times_to_cohort(
            self, row_creation_times: RowCreationTimes
    ) -> Dict[int, List[CohortDefinition]]:
        r: Dict[int, List[CohortDefinition]] = {}

        for cs in row_creation_times.column_selectors:
            selector = cs.regex if cs.is_raw_regex() else cs.name
            source_pattern, schema_pattern, table_pattern, column_pattern = (
                cs.explode_to_cohort_patterns(selector)
            )
            (
                source_exclusions,
                schema_exclusions,
                table_exclusions,
                column_exclusions,
            ) = cs.explode_exclusions_to_cohort_patterns()

            matching_source_ids = self._get_matching_source_ids(
                column_selector=cs, source_include_pattern=source_pattern
            )

            if not matching_source_ids:
                "registering validation errors when the source was not matched."
                error_lines = cs.get_error_lines()
                row_creation_times.register_validation_error(
                    error_lines=error_lines,
                    error_message=SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(
                        fq_name=source_pattern
                    ),
                )

            for id in matching_source_ids:
                cd = CohortDefinition(
                    schema_name_pattern=schema_pattern,
                    table_name_pattern=table_pattern,
                    column_name_pattern=column_pattern,
                    column_type=(
                        cs.type.to_datawatch_object()
                        if cs.type
                        else FieldType.FIELD_TYPE_UNSPECIFIED
                    ),
                    schema_exclusions=schema_exclusions,
                    table_exclusions=table_exclusions,
                    column_exclusions=column_exclusions,
                    entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD,
                    use_raw_regex=cs.is_raw_regex(),
                )
                if id in r.keys():
                    r[id].append(cd)
                else:
                    r[id] = [cd]

        return r

    def table_deployment_to_row_creation_times_cohort(
            self, td: TableDeployment
    ) -> Dict[int, CohortDefinition]:
        r: Dict[int, CohortDefinition] = {}

        split: List[str] = td.explode_fq_table_name()
        source_pattern = split[0]
        schema_pattern = split[1]
        table_pattern = split[2]
        column_pattern = td.row_creation_time
        if column_pattern is None:
            return r

        matching_source_ids = [
            source.id
            for source_name, source in self.sources_by_name_ix.items()
            if source_name
               in wildcard_search(search_string=source_pattern, content=[source_name])
        ]

        if not matching_source_ids:
            "registering validation errors when the source was not matched."
            errlns = [f"fq_table_name: {td.fq_table_name}"]
            td.register_validation_error(
                error_lines=errlns,
                error_message=SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(fq_name=td),
            )

        for id in matching_source_ids:
            cd = CohortDefinition(
                schema_name_pattern=schema_pattern,
                table_name_pattern=table_pattern,
                column_name_pattern=column_pattern,
                entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD,
            )
            r[id] = cd

        return r

    def _generate_tags_for_favorites(
            self, user_favorites: List[str]
    ) -> Optional[List[str]]:
        """
        Given a list of user emails, this will build a list of strings that include the corresponding Bigeye user id.
        If no user id is found for a given email, then a warning message will be provided.
        """
        if not user_favorites:
            return None

        if not self.bigeye_users:
            # only make this request once and only if a user adds favorites
            self.bigeye_users = {u.email: u.id for u in self.client.get_users().users}

        favorite_tags: List[str] = []
        for uf in user_favorites:
            matching_user_id = self.bigeye_users.get(uf, None)
            if not matching_user_id:
                log.warning(
                    f"No user with email `{uf}` could be found. Skipping metric favorites for user. Please "
                    f"check the spelling of the email provided."
                )
            else:
                favorite_tags.append(f"favorite_user-{matching_user_id}")

        return favorite_tags

    def _get_owner_id(self, owner: Optional[str] = None) -> Optional[str]:
        """
        Given a user email, this will find the corresponding Bigeye user id. Given a user id, this will return that ID.
        If no user is found for a given email, then a warning message will be provided.
        """
        if not owner or owner.isdigit():
            return owner

        if not self.bigeye_users:
            # only make this request once and only if a user adds owner
            self.bigeye_users = {u.email: u.id for u in self.client.get_users().users}

        owner_id = self.bigeye_users.get(owner, None)

        if not owner_id:
            log.warning(
                f"No user with email `{owner}` could be found. Skipping metric ownership."
            )
            return None

        return str(owner_id)

    def tag_deployment_to_cohort_and_metric_def(
            self,
            tag_deployment: TagDeployment,
            named_schedules: List[NamedSchedule],
            default_lookback: SimpleLookback,
            deployment_collection: Union[SimpleSLA, SimpleCollection] = None,
    ) -> Dict[int, List[CohortAndMetricDefinition]]:
        """
        Builds a Cohort and MetricDefinition from a TagDeployment object.   For table level metrics
        Args:

            tag_deployment: tag deployment to convert to cohort and metric definition.
            named_schedules: a list of named schedules from the workspace
            default_lookback: the default lookback corresponding to "metric.data_time_window.default"
            deployment_collection: The collection associated with the deployment.

        Returns: Dict[source_id: int, List[CohortAndMetricDefinition]] matched based on source_id to consolidate to
        a single metric suite object.
        """

        cmds: Dict[int, List[CohortAndMetricDefinition]] = {}
        column_metrics: List[Tuple[SimpleMetricDefinition, MetricDefinition]] = []
        table_metrics: List[Tuple[SimpleMetricDefinition, MetricDefinition]] = []

        for m in tag_deployment.metrics:
            """segregate table level metrics from column level and add slas"""
            m = self._update_metric_definition_for_deployment(
                m=m,
                named_schedules=named_schedules,
                default_lookback=default_lookback,
                deployment_collection=deployment_collection
            )
            if not m:
                continue

            mdwo = m.to_datawatch_object()
            if _is_table_level_metric(
                    metric_type=m.metric_type, table_level_metrics=self.table_level_metrics
            ):
                mdwo.is_table_metric = True
                table_metrics.append((m, mdwo))
            else:
                column_metrics.append((m, mdwo))

        for cs in tag_deployment.column_selectors:
            selector = cs.regex if cs.is_raw_regex() else cs.name
            source_pattern, schema_pattern, table_pattern, column_pattern = (
                cs.explode_to_cohort_patterns(selector)
            )
            (
                source_exclusions,
                schema_exclusions,
                table_exclusions,
                column_exclusions,
            ) = cs.explode_exclusions_to_cohort_patterns()

            matching_source_ids = self._get_matching_source_ids(
                column_selector=cs, source_include_pattern=source_pattern
            )

            if not matching_source_ids:
                "registering validation errors when the source was not matched."
                tag_deployment.register_validation_error(
                    error_lines=cs.get_error_lines(),
                    error_message=SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(
                        fq_name=cs
                    ),
                )

            if column_metrics:
                """Only append cohorts if metrics actually exist."""
                columns_cohort = CohortDefinition(
                    schema_name_pattern=schema_pattern,
                    table_name_pattern=table_pattern,
                    column_name_pattern=column_pattern,
                    column_type=(
                        cs.type.to_datawatch_object()
                        if cs.type
                        else FieldType.FIELD_TYPE_UNSPECIFIED
                    ),
                    schema_exclusions=schema_exclusions,
                    table_exclusions=table_exclusions,
                    column_exclusions=column_exclusions,
                    entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD,
                    use_raw_regex=cs.is_raw_regex(),
                )
                for sid in matching_source_ids:
                    """Tag deployments support source patterns.  Each source id becomes a key in the returned dictionary
                    with the exact same cohorts and metrics."""
                    cmd = CohortAndMetricDefinition(
                        cohorts=[columns_cohort], metrics=[i[1] for i in column_metrics]
                    )
                    if sid in cmds:
                        cmds[sid].append(cmd)
                    else:
                        cmds[sid] = [cmd]

            if table_metrics:
                if (column_pattern != "*" and cs.name) or (
                        column_pattern != ".*" and cs.regex
                ):
                    for smd, md in table_metrics:
                        errmsg = (
                            f"Table level metrics can only be applied to column selectors if the column pattern is "
                            f"only a wild card.  Column Pattern: {column_pattern} -- Metric: {smd.metric_type}.  "
                            f"Table level metrics include: {', '.join([i.name for i in self.table_level_metrics])}"
                        )
                        tag_deployment.register_validation_error(
                            error_lines=smd.get_error_lines(),
                            error_context_lines=tag_deployment.get_error_lines(),
                            error_message=METRIC_APPLICATION_ERROR.format(
                                errmsg=errmsg
                            ),
                        )

                table_cohort = CohortDefinition(
                    schema_name_pattern=schema_pattern,
                    table_name_pattern=table_pattern,
                    column_name_pattern=column_pattern,
                    column_type=(
                        cs.type.to_datawatch_object()
                        if cs.type
                        else FieldType.FIELD_TYPE_UNSPECIFIED
                    ),
                    schema_exclusions=schema_exclusions,
                    table_exclusions=table_exclusions,
                    column_exclusions=column_exclusions,
                    entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_DATASET,
                    use_raw_regex=cs.is_raw_regex(),
                )

                for sid in matching_source_ids:
                    """Tag deployments support source patterns.  Each source id becomes a key in the returned dictionary
                    with the exact same cohorts and metrics."""
                    cmd = CohortAndMetricDefinition(
                        cohorts=[table_cohort], metrics=[i[1] for i in table_metrics]
                    )
                    if sid in cmds:
                        cmds[sid].append(cmd)
                    else:
                        cmds[sid] = [cmd]

        return cmds

    def table_deployment_to_cohort_and_metric_def(
            self,
            table_deployment: TableDeployment,
            named_schedules: List[NamedSchedule],
            default_lookback: SimpleLookback,
            deployment_collection: Union[SimpleSLA, SimpleCollection] = None,
    ) -> Dict[int, List[CohortAndMetricDefinition]]:
        """
        Builds a Cohort and MetricDefinition from a TableDeployment object
        Args:
            table_deployment: table deployment from which to generate cohort and metric definition
            named_schedules: a list of named schedules from the workspace
            default_lookback: the lookback corresponding to "metric.data_time_window.default"
            deployment_collection: Collection to which metrics will be added.

        Returns: Dict[warehouse_id: int, CohortAndMetricDefinition]
        """

        result: Dict[int, List[CohortAndMetricDefinition]] = {}

        fq_names_list = table_deployment.explode_fq_table_name()
        source_name = fq_names_list[0]
        schema_name = fq_names_list[1]
        table_name = fq_names_list[2]

        if source_name in self.sources_by_name_ix:
            sid = self.sources_by_name_ix[source_name].id
        else:
            "registering validation errors when the source was not matched."
            sid = 0
            error_message = SRC_NOT_EXISTS_FOR_DEPLOYMENT_ERRMSG.format(
                fq_name=table_deployment.fq_table_name
            )
            table_deployment.register_validation_error(
                error_lines=[f"fq_table_name: {table_deployment.fq_table_name}"],
                error_message=error_message,
            )

        cmds: List[CohortAndMetricDefinition] = []

        table_metrics = []
        table_cohort = CohortDefinition(
            schema_name_pattern=schema_name,
            table_name_pattern=table_name,
            entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_DATASET,
        )

        for m in table_deployment.table_metrics:
            "process table metrics and raise validation errors if column level metrics are defined."
            if not _is_table_level_metric(
                    metric_type=m.metric_type, table_level_metrics=self.table_level_metrics
            ):
                errmsg = (
                    f"Column level metrics cannot be applied at the table level.  "
                    f"Table: {table_deployment.fq_table_name}.  "
                    f"Metric: {m.metric_type} is a column level metric.  "
                    f"Table level metrics include: {', '.join([i.name for i in self.table_level_metrics])}"
                )

                table_deployment.register_validation_error(
                    error_lines=m.get_error_lines(),
                    error_context_lines=table_deployment.get_table_metrics_error_lines(),
                    error_message=METRIC_APPLICATION_ERROR.format(errmsg=errmsg),
                )
            else:
                m = self._update_metric_definition_for_deployment(
                    m=m,
                    named_schedules=named_schedules,
                    default_lookback=default_lookback,
                    deployment_collection=deployment_collection
                )
                if not m:
                    continue

                mdwo = m.to_datawatch_object()
                mdwo.is_table_metric = True
                table_metrics.append(mdwo)

        if table_metrics:
            "Only add the cohort if metrics actually exist for it."
            cmds.append(
                CohortAndMetricDefinition(cohorts=[table_cohort], metrics=table_metrics)
            )

        for c in table_deployment.columns:
            "Process Column Metrics"
            cohort = CohortDefinition(
                schema_name_pattern=schema_name,
                table_name_pattern=table_name,
                column_name_pattern=c.column_name,
                entity_type=CatalogEntityType.CATALOG_ENTITY_TYPE_FIELD,
            )
            col_metrics = []

            for m in c.metrics:
                if _is_table_level_metric(
                        metric_type=m.metric_type,
                        table_level_metrics=self.table_level_metrics,
                ):
                    errmsg = (
                        f"Table level metrics cannot be applied at the column level.  "
                        f"Table: {table_deployment.fq_table_name}.  Column: {c.column_name}.  "
                        f"Metric: {m.metric_type} is a table level metric.  "
                        f"Table level metrics include: {', '.join([i.name for i in self.table_level_metrics])}"
                    )

                    table_deployment.register_validation_error(
                        error_lines=m.get_error_lines(),
                        error_context_lines=table_deployment.get_error_lines(),
                        error_message=METRIC_APPLICATION_ERROR.format(errmsg=errmsg),
                    )
                else:
                    m = self._update_metric_definition_for_deployment(
                        m=m,
                        named_schedules=named_schedules,
                        default_lookback=default_lookback,
                        deployment_collection=deployment_collection
                    )
                    if not m:
                        continue

                    mdwo = m.to_datawatch_object()
                    col_metrics.append(mdwo)

            if col_metrics:
                "Only add the cohort if metrics actually exist for it."
                cmds.append(
                    CohortAndMetricDefinition(cohorts=[cohort], metrics=col_metrics)
                )

        result[sid] = cmds

        return result

    def bigconfig_to_metric_suites(
            self,
            bigconfig: BigConfig,
            deployment_collections: Dict[str, Union[SimpleSLA, SimpleCollection]],
    ) -> List[MetricSuite]:
        """
        Creates a MetricSuite for each source identified in a Bigconfig Table or Tag Deployment.
        Args:
            bigconfig: Bigconfig from which MetricSuites will be created.
            deployment_collections: Upserted SLAs (must contain ID)

        Returns: List[MetricSuite]
        """

        # Applying metric suites after instantiation so that validation errors early on can be located in files.
        bigconfig.apply_tags_and_saved_metrics()

        cmds: Dict[int, List[CohortAndMetricDefinition]] = {}

        rct_cohorts: Dict[int, List[CohortDefinition]] = (
            self.row_creation_times_to_cohort(bigconfig.row_creation_times)
        )
        named_schedules: List[NamedSchedule] = (
            self.client.get_named_schedule().named_schedules
        )
        default_lookback_type: bool = [
            ac.boolean_value
            for ac in self.client.get_advanced_configs()
            if ac.key == "metric.data_time_window.default"
        ][0]
        default_lookback = (
            SimpleLookback()
            if default_lookback_type
            else SimpleLookback(lookback_type=SimpleLookbackType.DATA_TIME)
        )

        for tag_d_suite in bigconfig.tag_deployments:
            for tag_d in tag_d_suite.deployments:
                """Process all tag deployments into CohortAndMetricDefinitions.  One tag deployment per CMD"""
                if tag_d_suite.collection:
                    deployment_sla = deployment_collections.get(
                        tag_d_suite.collection.name, None
                    )
                else:
                    deployment_sla = None
                r: Dict[int, List[CohortAndMetricDefinition]] = (
                    self.tag_deployment_to_cohort_and_metric_def(
                        tag_deployment=tag_d,
                        named_schedules=named_schedules,
                        default_lookback=default_lookback,
                        deployment_collection=deployment_sla,
                    )
                )
                for sid, definitions in r.items():
                    """consolidate based on source"""
                    if sid in cmds:
                        cmds[sid].extend(definitions)
                    else:
                        cmds[sid] = definitions

        for table_d_suite in bigconfig.table_deployments:
            for table_d in table_d_suite.deployments:
                "Process all table deployments into CohortAndMetricDefinitions. One table deployment per CMD"
                if table_d_suite.collection:
                    deployment_sla = deployment_collections.get(
                        table_d_suite.collection.name, None
                    )
                else:
                    deployment_sla = None
                r = self.table_deployment_to_cohort_and_metric_def(
                    table_deployment=table_d,
                    named_schedules=named_schedules,
                    default_lookback=default_lookback,
                    deployment_collection=deployment_sla,
                )
                for sid, definitions in r.items():
                    """consolidate based on sources"""
                    if sid in cmds:
                        cmds[sid].extend(definitions)
                    else:
                        cmds[sid] = definitions
                rct = self.table_deployment_to_row_creation_times_cohort(table_d)
                for sid, cohorts in rct.items():
                    if sid in rct_cohorts.keys():
                        rct_cohorts[sid].append(cohorts)
                    else:
                        rct_cohorts[sid] = [cohorts]

        deployment_metric_suites: Dict[int, MetricSuite] = {
            source_id: MetricSuite(
                source_id=source_id,
                definitions=definitions,
                auto_apply_on_indexing=bigconfig.auto_apply_on_indexing,
                namespace=bigconfig.namespace
            )
            for source_id, definitions in cmds.items()
        }

        metric_suites: List[MetricSuite] = []

        for source_id, metric_suite in deployment_metric_suites.items():
            if source_id in rct_cohorts.keys():
                metric_suite.row_creation_cohorts = rct_cohorts.pop(source_id)

            metric_suites.append(metric_suite)

        for source_id, rcts in rct_cohorts.items():
            metric_suites.append(
                MetricSuite(
                    source_id=source_id,
                    row_creation_cohorts=rcts,
                    auto_apply_on_indexing=bigconfig.auto_apply_on_indexing,
                    namespace=bigconfig.namespace
                )
            )

        return metric_suites

    def execute_purge(
            self,
            purge_source_names: List[str] = None,
            purge_all_sources: bool = False,
            output_path: str = Path.cwd(),
            apply: bool = False,
            namespace: Optional[str] = None
    ):
        """
        Executes a purge of metrics deployed by MetricSuite on named sources or for all sources.
        Args:
            purge_source_names: list of source names to purge
            purge_all_sources: if true will purge all sources.
            output_path: path to dump the reports.  If no path is given the current working directory will be used.
            apply: If true then Big Config will be applied to the workspace.  If false then a plan will be generated.
            namespace: The namespace of the bigconfig deployment
        """
        try:
            self.client.purge_metric_suites(
                source_names=purge_source_names,
                purge_all_sources=purge_all_sources,
                apply=apply,
                namespace=namespace
            )
            process_stage = ProcessStage.APPLY if apply else ProcessStage.PLAN
            return process_reports(
                output_path=output_path, strict_mode=False, process_stage=process_stage, namespace=namespace
            )
        except NoSourcesFoundException as e:
            sys.exit(e.message)

    def execute_bigconfig(
            self,
            input_path: List[str] = (Path.cwd()),
            output_path: str = Path.cwd(),
            apply: bool = False,
            recursive: bool = False,
            strict_mode: bool = False,
            auto_approve: bool = False,
            namespace: Optional[str] = None
    ):
        """
        Executes an Apply or Plan for a Big Config.
        Args:
            input_path: path of source files.  If no path is given the current working directory will be used.
            output_path: path to dump the reports.  If no path is given the current working directory will be used.
            apply: If true, then Big Config will be applied to the workspace.  If false then a plan will be generated.
            recursive: If true, search for files recursively
            strict_mode: If true errors from the API raise an exception.
            auto_approve: If true, user will not be prompted to approve deployment
            namespace: The namespace of the bigconfig deployment
        Returns: None

        """
        files: List[BIGCONFIG_FILE] = _find_bigconfig_files(
            input_paths=input_path, recursive=recursive
        )

        bigconfig: BigConfig = combine_bigconfigs(bigconfigs=files, namespace=namespace)

        if get_validation_error_cnt():
            """Processing validation errors if any exist and throw exception."""
            fixme_file_list = process_validation_errors(output_path)
            unmatched_validations_errors = get_all_validation_errors_flat(
                only_unmatched=True
            )
            raise_files_contain_error_exception(
                validation_error_cnt=get_validation_error_cnt(),
                unmatched_validations_errors=unmatched_validations_errors,
                fixme_file_list=fixme_file_list,
            )

        # Creates new SLAs only so that all ids exist when we create the metric suites.
        deployment_collections = {
            c.name: c
            for c in self._upsert_collections(
                bigconfig=bigconfig, overwrite=False, apply=apply
            )
        }

        metric_suites = self.bigconfig_to_metric_suites(
            bigconfig=bigconfig, deployment_collections=deployment_collections
        )

        if get_validation_error_cnt():
            """Processing validation errors if any exist and throw exception."""
            fixme_file_list = process_validation_errors(output_path)
            unmatched_validations_errors = get_all_validation_errors_flat(
                only_unmatched=True
            )
            raise_files_contain_error_exception(
                validation_error_cnt=get_validation_error_cnt(),
                unmatched_validations_errors=unmatched_validations_errors,
                fixme_file_list=fixme_file_list,
            )

        # Applies changes and overwrites once local validations have passed.
        if apply and not auto_approve:
            # run a plan, ask for approval, then apply
            self._process_metric_suites(
                metric_suites=metric_suites,
                output_path=output_path,
                strict_mode=strict_mode,
                apply=False,
                namespace=bigconfig.namespace
            )
            approved = typer.confirm(
                typer.style(
                    f"Please review expected results. Are you sure you want to continue?", fg="red", bold=True
                )
            )
            if approved:
                self._process_metric_suites(
                    metric_suites=metric_suites,
                    output_path=output_path,
                    strict_mode=strict_mode,
                    apply=apply,
                    namespace=bigconfig.namespace
                )
        else:
            return self._process_metric_suites(
                metric_suites=metric_suites,
                output_path=output_path,
                strict_mode=strict_mode,
                apply=apply,
                namespace=bigconfig.namespace
            )

    def _process_metric_suites(
            self,
            metric_suites: List[MetricSuite],
            output_path: str = Path.cwd(),
            strict_mode: bool = False,
            apply: bool = False,
            namespace: Optional[str] = None
    ):
        """Send metric suites to correct endpoints and process reports."""
        run_metric_on_save = False

        # if applying, clear out any plan reports that were needed for approvals.
        if apply:
            REPORTS.clear()
        else:
            try:
                run_metric_on_save = [
                    ac.boolean_value
                    for ac in self.client.get_advanced_configs()
                    if ac.key == "metric.save.run_immediately"
                ][0]
            except IndexError:
                log.warning(
                    "The configuration for 'Run metric on save' was not found in the advanced settings of Bigeye."
                )
                log.warning(
                    "The name may have changed. It is recommended to disable this setting when deploying via bigconfig."
                )

        process_stage = ProcessStage.APPLY if apply else ProcessStage.PLAN

        for metric_suite in metric_suites:
            response = self.client.post_bigconfig(metric_suite=metric_suite, apply=apply)
            MetricSuiteReport.from_datawatch_object(
                response,
                source_name=self.sources_by_id_ix[metric_suite.source_id].name,
                process_stage=process_stage,
            )

        # process reports for the current stage - even if different from user issued command
        return process_reports(
            output_path=output_path,
            strict_mode=strict_mode,
            process_stage=process_stage,
            run_metric_on_save=run_metric_on_save,
            namespace=namespace
        )


def combine_bigconfigs(bigconfigs: List[BigConfig], namespace: Optional[str] = None) -> BigConfig:
    to_return: BigConfig = BigConfig(
        type="BIGCONFIG_FILE",
        tag_definitions=[],
        row_creation_times=RowCreationTimes(),
        saved_metric_definitions=SavedMetricDefinitions(metrics=[]),
        tag_deployments=[],
        table_deployments=[],
    )
    from statistics import mode
    auto_apply_to_check: bool = mode([bc.auto_apply_on_indexing for bc in bigconfigs])
    namespace_to_check: Optional[str] = mode([bc.namespace for bc in bigconfigs])
    namespaces_match = True

    if namespace:
        for bc in bigconfigs:
            if bc.namespace != namespace and bc.namespace is not None:
                namespaces_match = False
        if not namespaces_match:
            raise BigConfigValidationException(
                f"The namespace from the CLI does not match the namespace defined in the file(s). "
                f"Remove the argument from the command line or the namespace parameter from the file(s)."
            )

        if not namespace_to_check:
            namespace_to_check = namespace

    for bc in bigconfigs:
        if auto_apply_to_check != bc.auto_apply_on_indexing:
            BigConfig.register_validation_error(
                error_lines=[f"auto_apply_on_indexing: {bc.auto_apply_on_indexing}".lower()],
                error_message=MISMATCHED_ATTRIBUTE_ACROSS_MULTIPLE_FILES.format(
                    attribute="auto_apply_on_indexing"
                ),
            )

        if namespace_to_check != bc.namespace:
            if bc.namespace is not None or namespace is None:
                BigConfig.register_validation_error(
                    error_lines=[f"namespace: {bc.namespace}"],
                    error_message=MISMATCHED_ATTRIBUTE_ACROSS_MULTIPLE_FILES.format(
                        attribute="namespace"
                    ),
                )
        to_return.auto_apply_on_indexing = auto_apply_to_check
        to_return.tag_definitions.extend(bc.tag_definitions)
        if bc.row_creation_times:
            rct = bc.row_creation_times
            to_return.row_creation_times.column_selectors.extend(rct.column_selectors)
            to_return.row_creation_times.tag_ids.extend(rct.tag_ids)
        if bc.saved_metric_definitions:
            smd = bc.saved_metric_definitions
            to_return.saved_metric_definitions.metrics.extend(smd.metrics)
        to_return.tag_deployments.extend(bc.tag_deployments)
        to_return.table_deployments.extend(bc.table_deployments)

    if namespace_to_check:
        to_return.namespace = namespace_to_check
    to_return.build_tag_ix(to_return.tag_definitions)
    to_return.build_saved_metric_ix(to_return.saved_metric_definitions)

    return to_return
