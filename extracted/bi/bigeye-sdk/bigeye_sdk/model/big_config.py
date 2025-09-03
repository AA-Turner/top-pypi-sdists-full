from __future__ import annotations

import copy
import re

import yaml
from typing import List, Optional, Dict, Tuple, Any, Union
from pydantic.v1 import Field, PrivateAttr, validator, root_validator

from bigeye_sdk.bigconfig_validation.validation_functions import safe_split_dict_entry_lines, must_be_list_validator
from bigeye_sdk.bigconfig_validation.yaml_model_base import YamlModelWithValidatorContext
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import DUPLICATE_SAVED_METRIC_ID_EXISTS_ERRMSG, \
    DUPLICATE_TAG_EXISTS_ERRMSG, TAG_ID_NOT_EXISTS_IN_TAG_DEFINITION_ERRMSG, \
    SAVED_METRIC_ID_NOT_EXISTS_IN_SAVED_METRICS_DEFINITION_ERRMSG, FQ_COL_NOT_RESOLVES_TO_COLUMN_ERRMSG, \
    WILD_CARDS_NOT_SUPPORT_IN_FQ_TABLE_NAMES_ERRMSG, FQ_TABLE_NAME_MUST_RESOLVE_TO_TABLE_ERRMSG, \
    MUST_HAVE_COLUMN_SELECTOR_NAME_OR_TYPE, COLUMN_SELECTOR_MUST_HAVE_VALID_REGEX, \
    NAME_AND_EXCLUDE_MUST_NOT_BE_DECLARED_IF_REGEX
from bigeye_sdk.exceptions.exceptions import BigConfigValidationException
from bigeye_sdk.functions.bigconfig_functions import explode_fq_name, explode_fq_table_name
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.protobuf_enum_facade import SimpleFieldType, SimpleAutothresholdSensitivity, \
    SimpleTimeIntervalType, SimpleLookbackType
from bigeye_sdk.model.protobuf_message_facade import SimpleMetricDefinition, SimpleCollection, SimpleSLA, BucketSize, \
    SimpleMetricType, SlackNotificationChannel, EmailNotificationChannel, SimplePredefinedMetric, SimpleTemplateMetric, \
    SimpleNotificationChannel
from bigeye_sdk.serializable import BigConfigFile

log = get_logger(__name__)


class ColumnSelector(YamlModelWithValidatorContext):
    name: str = None
    type: SimpleFieldType = None
    exclude: Union[List[str], str] = None
    regex: str = None

    @validator('name', allow_reuse=True)
    def must_have_split_length_4_or_5(cls, v):
        if v and (v == '' or len(v) == 0 or len(explode_fq_name(v)) not in [4, 5]):
            error_message = FQ_COL_NOT_RESOLVES_TO_COLUMN_ERRMSG.format(fq_column_name=v)
            cls.register_validation_error(error_lines=[v], error_message=error_message)

        return v

    @validator('exclude')
    def must_be_list_of_valid_patterns(cls, v):
        # Exclude can either be a single string or a list of pattern exclusions
        list_of_excludes = v
        if not isinstance(list_of_excludes, list):
            list_of_excludes = [v]
        for v in list_of_excludes:
            if v and (v == '' or len(v) == 0 or len(explode_fq_name(v)) not in [4, 5]):
                error_message = FQ_COL_NOT_RESOLVES_TO_COLUMN_ERRMSG.format(fq_column_name=v)
                cls.register_validation_error(error_lines=[v], error_message=error_message)
        return list_of_excludes

    @validator('regex')
    def must_be_valid_regex(cls, v):
        try:
            re.compile(v)
        except (re.error, TypeError, RecursionError) as e:
            error_message = COLUMN_SELECTOR_MUST_HAVE_VALID_REGEX.format(error_message=str(e))
            cls.register_validation_error(error_lines=[v], error_message=error_message)
        return v

    @root_validator(pre=True)
    def select_all_for_just_type(cls, values):
        # If you only define a type for a ColumnSelector, explode_fq_name breaks trying to remove quotes
        # from a NoneType object. Set name as all sources, if only type is provided.
        if not values or not isinstance(values, Dict):
            return

        cs_type = values.get('type')
        cs_name = values.get('name')
        cs_regex = values.get('regex')

        if cs_type and not cs_name and not cs_regex:
            values['name'] = '*.*.*.*'

        return values

    @root_validator(pre=True)
    def type_or_name_must_be_declared_if_exclude(cls, values):
        # If no name and no type are passed in, but an exclude statement is then raise validation error.
        if not values.get('name') and not values.get('type') and values.get('exclude'):
            error_message = MUST_HAVE_COLUMN_SELECTOR_NAME_OR_TYPE.format(column_selector=values)
            raise BigConfigValidationException(error_message)
        return values

    @root_validator(pre=True)
    def name_and_exclude_must_not_be_declared_if_regex(cls, values):
        # If either name or exclude are passed in, then regex should not be used
        if (values.get('name') or values.get('exclude')) and values.get('regex'):
            error_message = NAME_AND_EXCLUDE_MUST_NOT_BE_DECLARED_IF_REGEX.format(column_selector=values)
            raise BigConfigValidationException(error_message)
        return values

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, ColumnSelector):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.name == other.name

    def is_raw_regex(self):
        if self.regex:
            return True
        else:
            return False

    def explode_exclusions_to_cohort_patterns(self) -> Union[Tuple[List[str], List[str], List[str], List[str]], Tuple[None, None, None, None]]:
        """
        Returns: Tuple(List(source_exclude_patterns), List(schema_exclude_patterns), List(table_exclude_patterns),
        List(column_exclude_pattern))
        """
        # if no exclude given, then just return none
        if not self.exclude:
            return None, None, None, None

        source_exclusions = []
        schema_exclusions = []
        table_exclusions = []
        column_exclusions = []
        for exclude in self.exclude:
            source, schema, table, column = self.explode_to_cohort_patterns(exclude)
            source_exclusions.append(source)
            schema_exclusions.append(schema)
            table_exclusions.append(table)
            column_exclusions.append(column)

        return source_exclusions, schema_exclusions, table_exclusions, column_exclusions

    def explode_to_cohort_patterns(self, selector: str) -> Union[Tuple[str, str, str, str], Tuple[None, None, None, None]]:
        """
        Returns: Tuple(source_pattern, schema_pattern, table_pattern, column_pattern)
        """
        names = explode_fq_name(selector, is_regex=self.is_raw_regex())

        if len(names) == 5:
            """Accommodates source types that have a source/instance, database, and schema in the fully 
            qualified name"""
            return names[0], '.'.join(names[1:3]), names[3], names[4]
        elif len(names) == 4:
            """Accommodates source types that have a source/instance/database and schema in the fully qualified
            name"""
            return names[0], names[1], names[2], names[3]
        else:
            return None, None, None, None


class TagDefinition(YamlModelWithValidatorContext):
    tag_id: str
    column_selectors: List[ColumnSelector]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TagDefinition, attribute_name='column_selectors', values=values)

        return values

    def __hash__(self):
        return hash((repr(self.tag_id), self.column_selectors))


class SavedMetricDefinitions(YamlModelWithValidatorContext):
    # metric_collections: SavedMetricCollection
    metrics: List[SimpleMetricDefinition]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SavedMetricDefinitions, attribute_name='metrics', values=values)

        return values


class RowCreationTimes(YamlModelWithValidatorContext):
    tag_ids: Optional[List[str]] = Field(default_factory=lambda: [])
    column_selectors: Optional[List[ColumnSelector]] = Field(default_factory=lambda: [])

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=RowCreationTimes, attribute_name='tag_ids', values=values)
        must_be_list_validator(clazz=RowCreationTimes, attribute_name='column_selectors', values=values)

        return values


class TagDeployment(YamlModelWithValidatorContext):
    column_selectors: Optional[List[ColumnSelector]] = Field(default_factory=lambda: [])
    metrics: List[SimpleMetricDefinition]
    tag_id: Optional[str] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TagDeployment, attribute_name='metrics', values=values)
        must_be_list_validator(clazz=TagDeployment, attribute_name='column_selectors', values=values)

        return values


class TagDeploymentSuite(YamlModelWithValidatorContext):
    collection: Optional[SimpleCollection] = None
    deployments: List[TagDeployment]
    sla: Optional[SimpleSLA] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TagDeploymentSuite, attribute_name='deployments', values=values)

        return values

    @validator('deployments', each_item=True)
    def validate_metric_business_rules(cls, v: TagDeployment):
        for m in v.metrics:
            m.deployment_validations(config_error_lines=v.get_error_lines())

        return v

    @root_validator(pre=True)
    def warn_and_use_collection(cls, values):
        if values.get('sla'):
            log.warning('sla class variable is deprecated and will be removed in future versions. Use collection.')
            values['collection'] = values['sla']

        return values


class ColumnMetricDeployment(YamlModelWithValidatorContext):
    column_name: str
    metrics: List[SimpleMetricDefinition]

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TableDeployment, attribute_name='metrics', values=values)

        return values


class TableDeployment(YamlModelWithValidatorContext):
    fq_table_name: str
    columns: Optional[List[ColumnMetricDeployment]] = Field(default_factory=lambda: [])
    table_metrics: Optional[List[SimpleMetricDefinition]] = Field(default_factory=lambda: [])
    row_creation_time: Optional[str] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TableDeployment, attribute_name='columns', values=values)
        must_be_list_validator(clazz=TableDeployment, attribute_name='table_metrics', values=values)

        return values

    @validator('fq_table_name')
    def fq_table_name_must_not_have_wildcards(cls, v):
        if '*' in v:
            error_message = WILD_CARDS_NOT_SUPPORT_IN_FQ_TABLE_NAMES_ERRMSG.format(fq_table_name=v)
            cls.register_validation_error(error_lines=[v], error_message=error_message)

        return v

    @validator('fq_table_name')
    def must_have_split_length_3_or_4(cls, v):
        if v == '' or len(v) == 0 or len(explode_fq_name(v)) not in [3, 4]:
            error_message = FQ_TABLE_NAME_MUST_RESOLVE_TO_TABLE_ERRMSG.format(fq_table_name=v)
            cls.register_validation_error(error_lines=[v], error_message=error_message)
        return v

    @validator('columns', each_item=True)
    def validate_metric_business_rules_for_columns(cls, v: ColumnMetricDeployment):
        """Document in deployment_validations()"""
        error_config_lines = v.get_error_lines()

        for m in v.metrics:
            m.deployment_validations(error_config_lines)

        return v

    def get_table_metrics_error_lines(self):
        return safe_split_dict_entry_lines(
            'table_metrics',
            [smd.get_error_lines() for smd in self.table_metrics])

    def explode_fq_table_name(self):
        """
        Explodes a fully qualified table name into a list of names.  Supports single and double-quoted  names
        containing periods.  Supports fully qualified names with either source.database.schema or source.schema
        conventions.  DOES NOT support wild cards.

            Example: wh."my.schema".some_table resolves to ['wh', 'my.schema', 'some_table']

        Returns: list of names from the fully qualified table name
        """

        return explode_fq_table_name(self.fq_table_name)


class TableDeploymentSuite(YamlModelWithValidatorContext):
    collection: Optional[SimpleCollection] = None
    deployments: List[TableDeployment]
    sla: Optional[SimpleSLA] = None

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=TableDeploymentSuite, attribute_name='deployments', values=values)

        return values

    @validator('deployments', each_item=True)
    def validate_metric_business_rules_for_table_metrics(cls, v: TableDeployment):
        for m in v.table_metrics:
            m.deployment_validations(config_error_lines=v.get_error_lines())
        return v

    @root_validator(pre=True)
    def warn_and_use_collection(cls, values):
        if values.get('sla'):
            log.warning('sla class variable is deprecated and will be removed in future versions. Use collection.')
            values['collection'] = values['sla']

        return values


class BigConfig(BigConfigFile, type='BIGCONFIG_FILE'):
    """
    Bigconfig is a canonical model used to collate and compile all definition and deployment files maintained by users
    into a single object that can be used to generate a metric suite.  Tag Definitions and Saved Metric Definitions
    are applied -- and validated -- during the __post_init__ phase of instantiating a Bigconfig.
    """
    auto_apply_on_indexing: bool = False
    namespace: Optional[str] = None
    tag_definitions: Optional[List[TagDefinition]] = Field(
        default_factory=lambda: [])  # only one because we must consolidate if creating Bigconfig from multiple files.
    row_creation_times: Optional[RowCreationTimes] = RowCreationTimes()
    saved_metric_definitions: Optional[
        SavedMetricDefinitions] = None  # only one b/c we must consolidate if creating Bigconfig from multiple files.
    tag_deployments: Optional[List[TagDeploymentSuite]] = Field(default_factory=lambda: [])
    table_deployments: Optional[List[TableDeploymentSuite]] = Field(default_factory=lambda: [])

    _tag_ix_: Dict[str, List[ColumnSelector]] = PrivateAttr({})  # Dict[tag_id, List[ColumnSelector]]
    _saved_metric_ix_: Dict[str, SimpleMetricDefinition] = PrivateAttr(
        {})  # Dict[saved_metric_id, SimpleMetricDefinition]
    _raw_: dict = PrivateAttr({})

    # _saved_metric_collection_ix_: Dict[str, List, str] = {}
    # Dict[saved_metric_collection_id, List[saved_metric_id]] (V1)

    @root_validator(pre=True)
    def bigconfig_validation_checks(cls, values):
        must_be_list_validator(clazz=BigConfig, attribute_name='tag_definitions', values=values)
        must_be_list_validator(clazz=BigConfig, attribute_name='tag_deployments', values=values)
        must_be_list_validator(clazz=BigConfig, attribute_name='table_deployments', values=values)

        values['_raw_'] = values
        return values

    @validator('saved_metric_definitions')
    def each_saved_metric_must_have_id(cls, v: SavedMetricDefinitions):
        """Located here to capture the full configurations lines for error.  Validators can be weird.  Could use
        root_validator in the future."""
        config_error_lines: List[str] = v.get_error_lines()
        for m in v.metrics:
            m.saved_metrics_must_have_id(config_error_lines=config_error_lines)
        return v

    def __init__(self, **data: Any):
        super().__init__(**data)

        log.info('Building Indices.')
        self.build_tag_ix(self.tag_definitions)

        self.build_saved_metric_ix(self.saved_metric_definitions)

    def build_tag_ix(self, tag_definitions: List[TagDefinition]):
        if tag_definitions:
            self._tag_ix_ = self._generate_tag_ix(tag_definitions)

    def build_saved_metric_ix(self, saved_metric_definitions: SavedMetricDefinitions):
        if saved_metric_definitions:
            self._saved_metric_ix_ = self._generate_saved_metric_def_ix(self.saved_metric_definitions)

    def apply_tags_and_saved_metrics(self):

        log.info('Applying tags and saved metrics.')

        if self._tag_ix_ or self.tag_deployments:
            apply_result = self._apply_tags(tag_ix=self._tag_ix_, tag_deps=self.tag_deployments,
                                            row_creation_times=self.row_creation_times)
            self.tag_deployments = apply_result[0]
            self.row_creation_times = apply_result[1]

        if self._saved_metric_ix_ or self.tag_deployments or self.table_deployments:
            apply_result = self._apply_saved_metrics(saved_metric_ix=self._saved_metric_ix_,
                                                     tag_deps=self.tag_deployments,
                                                     table_deps=self.table_deployments)
            self.tag_deployments = apply_result[0]
            self.table_deployments = apply_result[1]

    @classmethod
    def _generate_tag_ix(cls, tag_definitions: List[TagDefinition]) -> Dict[str, List[ColumnSelector]]:
        """
        Generates an index of Column Selectors by Tag ID and validates no duplicates exist and that column selectors
        is not empty.
        Args:
            tag_definitions: List of Tag Definitions from which an Index will be generated.

        Returns: An index of Column Selectors by Tag ID.
        """
        tix: Dict[str, List[ColumnSelector]] = {}
        for td in tag_definitions:
            if td.tag_id in tix:
                error_message = DUPLICATE_TAG_EXISTS_ERRMSG.format(tag_id=td.tag_id)
                cls.register_validation_error(error_context_lines=td.get_error_lines(),
                                              error_lines=[td.tag_id],
                                              error_message=error_message)

            tix[td.tag_id] = td.column_selectors

        return tix

    @classmethod
    def _generate_saved_metric_def_ix(cls, smd: SavedMetricDefinitions) -> Dict[str, SimpleMetricDefinition]:
        """
        Generates an index of Saved Metric Definitions by Saved Metric ID and validates no duplicates exist and that
        the Metric Definitions defined have at least a `saved_metric_id` and a `metric_type`.
        Args:
            smd: a Saved Metric Definitions object from which the Saved Metric Definitions IX will be generated.

        Returns: An index of Simple Metric Definitions keyed by `saved_metric_id`.

        """
        smdix: Dict[str, SimpleMetricDefinition] = {}
        for m in smd.metrics:
            if m.saved_metric_id in smdix:
                error_message = DUPLICATE_SAVED_METRIC_ID_EXISTS_ERRMSG.format(
                    saved_metric_id=m.saved_metric_id
                )
                test = m.get_error_lines()
                err_lines = [yaml.safe_dump({'saved_metric_id': m.saved_metric_id}, indent=True, sort_keys=False)]
                # TODO Removed the context lines because when nested bugs exist in yaml and some of them are caught as
                # TODO pre/raw bugs then we might have already fixed the issue (manipulated the values) so we could
                # TODO capture post/object bugs.  This would break the search.
                # cls.register_validation_error(error_context_lines=smd.get_error_lines(),
                #                               error_lines=err_lines,
                #                               error_message=error_message)
                cls.register_validation_error(error_lines=err_lines,
                                              error_message=error_message)

            if m.saved_metric_id:
                smdix[m.saved_metric_id] = m

        return smdix

    @classmethod
    def _saved_metric_id_exists_in_ix(cls, smd_id: str, saved_metric_ix: Dict[str, SimpleMetricDefinition]) -> bool:
        if smd_id not in saved_metric_ix.keys():
            error_message = SAVED_METRIC_ID_NOT_EXISTS_IN_SAVED_METRICS_DEFINITION_ERRMSG.format(saved_metric_id=smd_id)
            cls.register_validation_error(error_lines=[smd_id],
                                          error_message=error_message)
            return False
        else:
            return True

    @classmethod
    def _tag_id_exists_in_ix(cls, tag_id: str, tag_ix: Dict[str, List[ColumnSelector]]) -> bool:
        if tag_id not in tag_ix:
            error_message = TAG_ID_NOT_EXISTS_IN_TAG_DEFINITION_ERRMSG.format(tag_id=tag_id)
            cls.register_validation_error(error_lines=[tag_id],
                                          error_message=error_message)
            return False
        else:
            return True

    @classmethod
    def _apply_tags(cls, tag_ix: Dict[str, List[ColumnSelector]],
                    tag_deps: List[TagDeploymentSuite],
                    row_creation_times: RowCreationTimes) -> Tuple[List[TagDeploymentSuite], RowCreationTimes]:
        """
        Applies tags by tag id in all tag deployments and row creation times definitions.  Validates that all tags
        called in deployments exist in the tags definitions.  Validates that column selectors exist after application.
        Args:
            tag_ix: index of column selectors keyed by tag_id
            tag_deps: list of Tag Deployment Suites to which tags will be applied.
            row_creation_times: row creation times to which tags will be applied

        Returns: list of Tag Deployment Suites to which tags have been applied.

        """

        for td in tag_deps:
            for d in td.deployments:
                if d.tag_id and cls._tag_id_exists_in_ix(d.tag_id, tag_ix):
                    tagged_col_selectors = tag_ix.get(d.tag_id, [])
                    d.column_selectors.extend(tagged_col_selectors)
                    d.column_selectors = sorted(list(set(d.column_selectors)))

        for tag_id in row_creation_times.tag_ids:
            if cls._tag_id_exists_in_ix(tag_id, tag_ix):
                row_creation_times.column_selectors.extend(tag_ix[tag_id])

        row_creation_times.column_selectors = sorted(list(set(row_creation_times.column_selectors)))

        return tag_deps, row_creation_times

    @classmethod
    def _validate_and_apply(cls, m: SimpleMetricDefinition,
                            saved_metric_ix: Dict[str, SimpleMetricDefinition]) -> SimpleMetricDefinition:

        def _apply_overrides(saved_smd: SimpleMetricDefinition,
                             override_smd: SimpleMetricDefinition) -> SimpleMetricDefinition:
            r = SimpleMetricDefinition(**saved_smd.dict())

            for attr in override_smd.__dict__.keys():
                override_attr_value = getattr(override_smd, attr)
                if attr not in ['saved_metric_id', 'metric_type', 'sla_ids', 'collection_ids'] \
                        and not SimpleMetricDefinition.is_default_value(attr, override_attr_value):
                    setattr(r, attr, override_attr_value)

            return r

        if not m.saved_metric_id:
            return m

        if m.saved_metric_id not in saved_metric_ix.keys():
            error_message = SAVED_METRIC_ID_NOT_EXISTS_IN_SAVED_METRICS_DEFINITION_ERRMSG.format(
                saved_metric_id=m.saved_metric_id)
            cls.register_validation_error(error_lines=m.get_error_lines(),
                                          error_message=error_message)
            return m
        else:
            saved = saved_metric_ix[m.saved_metric_id]
            return _apply_overrides(saved, m)

    @classmethod
    def _apply_saved_metrics(cls, saved_metric_ix: Dict[str, SimpleMetricDefinition],
                             tag_deps: List[TagDeploymentSuite],
                             table_deps: List[TableDeploymentSuite]
                             ) -> Tuple[List[TagDeploymentSuite], List[TableDeploymentSuite]]:

        for tag_dep in tag_deps:
            for d in tag_dep.deployments:
                metrics: List[SimpleMetricDefinition] = []
                for m in d.metrics:
                    metrics.append(cls._validate_and_apply(m, saved_metric_ix))
                d.metrics = metrics

        for table_dep in table_deps:
            for d in table_dep.deployments:
                table_metrics: List[SimpleMetricDefinition] = []
                for m in d.table_metrics:
                    table_metrics.append(cls._validate_and_apply(m, saved_metric_ix))
                d.table_metrics = table_metrics

                for c in d.columns:
                    column_metrics: List[SimpleMetricDefinition] = []
                    for m in c.metrics:
                        column_metrics.append(cls._validate_and_apply(m, saved_metric_ix))
                    c.metrics = column_metrics

        return tag_deps, table_deps

    def get_collections(self) -> List[SimpleCollection]:
        collections: List[SimpleCollection] = []

        for d in self.tag_deployments:
            if d.collection:
                collections.append(d.collection)

        for d in self.table_deployments:
            if d.collection:
                collections.append(d.collection)

        return collections

    @staticmethod
    def tag_deployments_to_bigconfig(tag_deployments: List[TagDeployment],
                                     row_creation_times: RowCreationTimes = None,
                                     collection: SimpleCollection = None,
                                     dtw_is_default: bool = False) -> BigConfig:
        """
        This function accepts a list of tag deployments with single metric definitions and converts it into
        a valid Bigconfig file ready for export.
        """
        def _generate_saved_metric_definitions(simple_metrics: List[SimpleMetricDefinition]) -> SavedMetricDefinitions:
            output: List[SimpleMetricDefinition] = []
            for simple_metric in simple_metrics:
                simple_metric.saved_metric_id = _generate_saved_metric_id(simple_metric)
                simple_metric = _remove_redundant_properties(simple_metric)
                simple_metric = _remove_default_values(simple_metric)
                if simple_metric not in output:
                    output.append(simple_metric)

            return SavedMetricDefinitions(metrics=output)

        def _remove_default_values(simple_metric: SimpleMetricDefinition) -> SimpleMetricDefinition:
            simple_metric_dict = simple_metric.dict()
            metric_def_defaults = {
                'description': '',
                'group_by': [],
                'conditions': [],
                'notification_channels': [],
                'sla_ids': [],
                'collection_ids': [],
                'threshold': {
                    'type': 'AUTO',
                    'sensitivity': SimpleAutothresholdSensitivity.MEDIUM,
                    'upper_bound_only': False
                },
                'metric_schedule': {
                    'schedule_frequency': simple_metric.schedule_frequency,
                    'named_schedule': None
                },
                'schedule_frequency': {
                    'interval_type': SimpleTimeIntervalType.HOURS,
                    'interval_value': 24
                },
                'grain_seconds': 86400,
                'lookback': {
                    'lookback_window': {
                        'interval_type': SimpleTimeIntervalType.DAYS,
                        'interval_value': 2
                    },
                    'lookback_type': SimpleLookbackType.METRIC_TIME,
                    'bucket_size': BucketSize.DAY
                },
                'muted_until_epoch_seconds': 0
            }
            if not dtw_is_default:
                metric_def_defaults['lookback']['lookback_type'] = SimpleLookbackType.DATA_TIME
            if SimpleMetricType.is_freshness_volume(simple_metric.metric_type):
                metric_def_defaults['grain_seconds'] = 3600
                metric_def_defaults['lookback']['lookback_type'] = SimpleLookbackType.METRIC_TIME
                metric_def_defaults['lookback']['bucket_size'] = BucketSize.HOUR
            # Remove properties in simple metric that equal defaults to simplify bigconfig output
            for key in metric_def_defaults.keys():
                if metric_def_defaults[key] == simple_metric_dict[key]:
                    simple_metric_dict.pop(key, None)

            return SimpleMetricDefinition(**simple_metric_dict)

        def _remove_redundant_properties(simple_metric: SimpleMetricDefinition) -> SimpleMetricDefinition:
            # params should only be given for template metrics with parameters provided
            if simple_metric.parameters:
                for i, param in enumerate(simple_metric.parameters):
                    if param.key == 'arg1':
                        simple_metric.parameters.pop(i)
                    # only the necessary param type needs to be supplied
                    if not param.column_name:
                        param.column_name = None
                    if not param.string_value:
                        param.string_value = None
                    if not param.number_value:
                        param.number_value = None
                if len(simple_metric.parameters) == 0:
                    simple_metric.parameters = None
            # lookback randomly contains bucket size of 0, removing to avoid confusion
            if simple_metric.lookback and simple_metric.lookback.bucket_size == 0:
                simple_metric.lookback.bucket_size = None
            # grain seconds is not needed and copy of bucket size, bucket size is controlled in lookback
            if simple_metric.grain_seconds:
                simple_metric.grain_seconds = None
            # slack notifications contain a channel_id, removing to avoid confusion
            if simple_metric.notification_channels:
                updated = []
                for c in simple_metric.notification_channels:
                    if isinstance(c, SlackNotificationChannel):
                        updated.append({'slack': c.slack})
                    elif isinstance(c, EmailNotificationChannel):
                        updated.append({'email': c.email})
                    else:
                        updated.append(c)
                simple_metric.notification_channels = updated
            # metric schedules have an id and cron that do not need to be listed
            if simple_metric.metric_schedule and simple_metric.metric_schedule.named_schedule:
                simple_metric.metric_schedule.named_schedule.id = None
                simple_metric.metric_schedule.named_schedule.cron = None

            return simple_metric

        def _generate_saved_metric_id(simple_metric: SimpleMetricDefinition) -> Optional[str]:
            if isinstance(simple_metric.metric_type, SimplePredefinedMetric):
                return simple_metric.metric_type.predefined_metric.name
            elif isinstance(simple_metric.metric_type, SimpleTemplateMetric):
                return simple_metric.metric_type.template_name.upper().replace(" ", "_")
            else:
                log.error(f'Metric of type {type(simple_metric.metric_type)} is not currently supported '
                          f'and will be skipped.')
                return None

        def _map_column_selectors_to_metrics(simple_metric: SimpleMetricDefinition):
            # create a copy of saved metric to avoid overwriting
            saved_metric: SimpleMetricDefinition = simple_metric.copy(deep=True)
            saved_metric.saved_metric_id = _generate_saved_metric_id(saved_metric)
            # For every metric in passed tag deployments, find the matching de-duped saved metrics and add to list
            column_selectors: List[ColumnSelector] = []
            for td in tag_deployments:
                for metric in td.metrics:
                    cleaned_metric = _remove_default_values(metric)
                    if cleaned_metric == saved_metric:
                        column_selectors.extend(td.column_selectors)

            return column_selectors

        def _generate_tag_deployments(saved_metric_defs: SavedMetricDefinitions) -> List[TagDeployment]:
            deployments: List[TagDeployment] = []
            metric_ids: List[str] = []
            # for every saved metric in saved metric definitions
            for smd in saved_metric_defs.metrics:
                mid = smd.saved_metric_id
                # find the matching types for the saved metric based on saved metric id
                matching_types: List[SimpleMetricDefinition] = [
                    metric for metric in saved_metric_defs.metrics if metric.saved_metric_id == smd.saved_metric_id]
                # if more than 1 matching type, then update the saved metric id and add in conditions to
                # avoid removal on bigconfig apply
                if len(matching_types) > 1:
                    matching_types_copy = copy.deepcopy(matching_types)
                    for index, match in enumerate(matching_types):
                        mid = f'{match.saved_metric_id}_{index}'
                        match.saved_metric_id = mid
                        if mid not in metric_ids:
                            # metrics of same types can be distinguished by conditionals or group bys
                            # if neither are present on current and any other versions then add sudo conditionals
                            if not match.conditions and not match.group_by and \
                                    not any(mt.group_by for mt in matching_types_copy) and \
                                    not any(mt.conditions for mt in matching_types_copy):
                                match.conditions = [f'{index} = {index}']

                metric_ids.append(mid)
                deployments.append(TagDeployment(
                    column_selectors=_map_column_selectors_to_metrics(simple_metric=smd),
                    metrics=[SimpleMetricDefinition(saved_metric_id=smd.saved_metric_id)]
                ))

            return _dedupe_column_selectors(deployments)

        def _dedupe_column_selectors(tag_deployments: List[TagDeployment]) -> List[TagDeployment]:
            deployments: List[TagDeployment] = []
            for deployment in tag_deployments:
                # Remove any obvious passed in duplicate column selectors and sort by name
                deployment.column_selectors = list(set(deployment.column_selectors))
                deployment.column_selectors.sort(key=lambda c: c.name, reverse=True)
                # Find previous deployments with column selectors
                # If a match exists, add current deployment metrics to previous
                match = next((c for c in deployments if c.column_selectors == deployment.column_selectors), None)
                if match:
                    match.metrics.extend(deployment.metrics)
                else:
                    deployments.append(deployment)

            return deployments

        def _generate_collection() -> SimpleCollection:
            if collection.notification_channels:
                notifications: List[SimpleNotificationChannel] = []
                for channel in collection.notification_channels:
                    if isinstance(channel, SlackNotificationChannel):
                        channel.channel_id = None
                        channel.thread_ts = None
                    notifications.append(channel)
                return SimpleCollection(name=collection.name,
                                        description=collection.description,
                                        notification_channels=notifications)
            else:
                return SimpleCollection(name=collection.name,
                                        description=collection.description)

        simple_metrics: List[SimpleMetricDefinition] = []
        for tag_deployment in tag_deployments:
            for m in tag_deployment.metrics:
                simple_metrics.append(m)

        saved_metrics: SavedMetricDefinitions = _generate_saved_metric_definitions(simple_metrics=simple_metrics)
        final_deployments: List[TagDeployment] = _generate_tag_deployments(saved_metrics)
        final_collection = _generate_collection() if collection else None
        final_rcts = row_creation_times if row_creation_times and row_creation_times.column_selectors else None

        tag_deployment_suite = TagDeploymentSuite(collection=final_collection,
                                                  deployments=final_deployments)

        return BigConfig(type='BIGCONFIG_FILE',
                         row_creation_times=final_rcts,
                         saved_metric_definitions=saved_metrics,
                         tag_deployments=[tag_deployment_suite])

    @staticmethod
    def format_bigconfig_export(lines: str):
        # Creates new lines between main yaml sections and major subsections
        main_keys = re.compile(r"(\n\w+)")
        # subsections = re.compile(r"(?<!:)(\n {0,3}- )")

        def double_newline(m) -> str:
            return f"\n{m.group(1)}"

        lines, _ = re.subn(main_keys, double_newline, lines)
        # lines, _ = re.subn(subsections, double_newline, lines)
        return lines
