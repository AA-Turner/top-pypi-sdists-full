from __future__ import annotations

import sys
import textwrap
from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Any, Union, Optional

import yaml
from betterproto import Casing
from pydantic.v1 import Field
from pydantic_yaml import YamlStrEnum

from bigeye_sdk import DatawatchObject
from bigeye_sdk.bigconfig_validation.validation_models import ValidationError
from bigeye_sdk.exceptions.exceptions import BigConfigValidationException
from bigeye_sdk.generated.com.bigeye.models.generated import MetricSuiteResponse, CohortDefinition, \
    InvalidAssetMetricDefinitionApplication
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.protobuf_message_facade import SimpleMetricType
from bigeye_sdk.serializable import File

# TODO: Add error stats to API Execution Messages.
FAILED_API_EXECUTION_MSG = textwrap.dedent(
    """
    {namespace_heading}

    -=- REPORT -=-
    {source_reports}

    Bigconfig plan includes errors and report files have been generated.

    -=- Report files -=-
    {report_file_list}
    """
)

SUCCESSFUL_API_EXECUTION_MSG = textwrap.dedent(
    """
    {namespace_heading}

    -=- REPORT -=-                                                                                        
    {source_reports}

    Bigconfig plan successful and report files have been generated.

    -=- Report files -=-
    {report_file_list}
    """)

FIXME_FILES_LIST = """-=- FIXME files -=-
{fixme_file_list}
"""

FIXME_FILE_MESSAGE_ALL_MATCHED = """
{fixme_file_list}

"""

FIXME_FILE_MESSAGE_SOME_UNMATCHED = """
Some validation errors not matched in files:

{unmatched_validation_errors}

{fixme_file_list}

"""

FILES_CONTAIN_ERRORS_EXCEPTION_STATEMENT = """

Bigconfig file includes errors.
Number of Errors: {err_cnt}

{fixme_file_message}"""

RECOMMEND_DISABLE = """The advanced setting 'Run metric on save' is enabled. 
It is recommended to disable this setting when deploying metrics via bigconfig.
Someone from Bigeye can disable it via the UI or it can disabled by an Admin via the API using the key metric.save.run_immediately
See https://docs.bigeye.com/reference/updateconfigs"""

NAMESPACE_HEADING = """
    
-=- NAMESPACE -=-
{namespace}
"""

BIGCONFIG_REPORT = TypeVar('BIGCONFIG_REPORT', bound='BigConfigReport')
REPORTS: List[BIGCONFIG_REPORT] = []

log = get_logger(__name__)


def metric_type_not_supported(invalid: InvalidAssetMetricDefinitionApplication) -> bool:
    not_supported = True
    return not_supported in [
        True if f"Metric type {mm.predefined_metric} not supported on table {invalid.fq_asset_name}" in
                invalid.error_messages else False for mm in SimpleMetricType.get_metadata_metrics()
    ]


def all_reports() -> List[BIGCONFIG_REPORT]:
    return REPORTS


def process_reports(
        output_path: str,
        strict_mode: bool,
        process_stage: ProcessStage,
        run_metric_on_save: bool = False,
        namespace: Optional[str] = None
):
    report_files = []
    errors_reported = False

    source_reports = []
    final_report = "{message}\n{additional_info}"
    ns = ""
    rd = ""

    if run_metric_on_save:
        rd = RECOMMEND_DISABLE

    if namespace:
        ns = NAMESPACE_HEADING.format(namespace=namespace)

    for report in REPORTS:
        if process_stage == report.process_stage:
            cleansed_source_name = report.source_name.replace("/", "").replace(" ", "_")
            file_name = f'{output_path}/{cleansed_source_name}_{report.process_stage}.yml'
            report.save(output_path=file_name)
            report_files.append(file_name)
        errors_reported = errors_reported or report.has_errors()
        source_reports.append(report.get_console_report())

    if errors_reported and strict_mode:
        raise BigConfigValidationException(
            FAILED_API_EXECUTION_MSG.format(
                namespace_heading=ns,
                source_reports="\n".join(source_reports),
                report_file_list="\n".join(report_files)
            )
        )
    elif errors_reported:
        message = FAILED_API_EXECUTION_MSG.format(
            namespace_heading=ns,
            source_reports="\n".join(source_reports),
            report_file_list="\n".join(report_files)
        )

        info = f"Strict mode is OFF. There are errors reported.\n\n{rd}"
    else:
        message = SUCCESSFUL_API_EXECUTION_MSG.format(
            namespace_heading=ns,
            source_reports="\n".join(source_reports),
            report_file_list="\n".join(report_files)
        )
        info = f"{rd}"

    fr = final_report.format(message=message, additional_info=info)

    print(fr)
    return fr


class BigConfigReport(File, ABC):
    @classmethod
    @abstractmethod
    def from_datawatch_object(cls, obj: DatawatchObject, source_id: int,
                              process_stage: ProcessStage) -> BIGCONFIG_REPORT:
        pass

    @abstractmethod
    def tot_error_count(self) -> int:
        """returns a total error count for this report."""
        pass

    @abstractmethod
    def get_console_report(self) -> str:
        pass

    def has_errors(self):
        return self.tot_error_count() > 0


def raise_files_contain_error_exception(validation_error_cnt: int, unmatched_validations_errors: List[ValidationError],
                                        fixme_file_list: List[str]):
    fixme_file_list = FIXME_FILES_LIST.format(fixme_file_list=yaml.safe_dump(fixme_file_list))

    if unmatched_validations_errors:
        formatted_unmatched_validations = '\n'.join(
            ["ValidationError:\n" + yaml.safe_dump(
                umv.json(exclude_none=True, exclude_defaults=True, exclude_unset=True))
             for umv in unmatched_validations_errors])
        fixme_file_message = FIXME_FILE_MESSAGE_SOME_UNMATCHED.format(
            unmatched_validation_errors=formatted_unmatched_validations,
            fixme_file_list=fixme_file_list
        )
    else:
        fixme_file_message = FIXME_FILE_MESSAGE_ALL_MATCHED.format(
            fixme_file_list=fixme_file_list
        )

    sys.exit(FILES_CONTAIN_ERRORS_EXCEPTION_STATEMENT.format(
        err_cnt=str(validation_error_cnt),
        fixme_file_message=fixme_file_message
    ))


class ProcessStage(YamlStrEnum):
    APPLY = 'APPLY'
    PLAN = 'PLAN'


class MetricSuiteReport(BigConfigReport):
    type: str = 'BIGCONFIG_REPORT'
    _exclude_defaults = False
    process_stage: ProcessStage
    source_name: str

    row_creation_time_upserted_count: int = 0

    created_metric_count: int = 0
    updated_metric_count: int = 0
    deleted_metric_count: int = 0
    unchanged_metric_count: int = 0

    row_creation_time_upsert_failure_count: int = 0
    metric_application_error_count: int = 0
    invalid_asset_identifier_count: int = 0

    total_error_count: int = 0

    row_creation_time_report: dict = Field(default_factory=lambda: {})

    metric_application_errors: List[dict] = Field(default_factory=lambda: [])
    invalid_asset_identifier_errors: List[dict] = Field(default_factory=lambda: [])

    created_metrics: List[dict] = Field(default_factory=lambda: [])
    updated_metrics: List[dict] = Field(default_factory=lambda: [])
    deleted_metrics: List[dict] = Field(default_factory=lambda: [])
    unchanged_metrics: List[dict] = Field(default_factory=lambda: [])

    def get_console_report(self) -> str:

        source_report = f"""
-- Source Name: {self.source_name} -- 

Row Creation Upsert Count: {self.row_creation_time_upserted_count}
Created Metric Count: {self.created_metric_count}
Updated Metric Count: {self.updated_metric_count}
Deleted Metric Count: {self.deleted_metric_count}
Unchanged Metric Count: {self.unchanged_metric_count}
Row Creation Time Upsert Failure Count: {self.row_creation_time_upsert_failure_count}
Metric Application Error Count: {self.metric_application_error_count}
Invalid Asset Identifier Count: {self.invalid_asset_identifier_count}
Total Error Count: {self.tot_error_count()}"""

        # These are all available in the report and clutter the console.
        #         if self.row_creation_time_upsert_failure_count:
        #             source_report = f"""{source_report}
        #
        # Row creation Time Upsert Failures:
        # {yaml.safe_dump(self.row_creation_time_report['row_creation_time_upsert_failures'])}"""
        #
        #         if self.metric_application_errors:
        #             source_report = f"""{source_report}
        #
        # Metric Application Errors:
        # {yaml.safe_dump(self.metric_application_errors)}"""
        #
        #         if self.invalid_asset_identifier_errors:
        #             source_report = f"""{source_report}
        #
        # Invalid Asset Identifier Errors:
        # {yaml.safe_dump(self.invalid_asset_identifier_errors)}"""

        return source_report

    def tot_error_count(self) -> int:
        return self.total_error_count

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.total_error_count = self.row_creation_time_upsert_failure_count \
                                 + self.metric_application_error_count \
                                 + self.invalid_asset_identifier_count
        REPORTS.append(self)

    @classmethod
    def from_datawatch_object(cls, obj: MetricSuiteResponse, source_name: str,
                              process_stage: ProcessStage) -> MetricSuiteReport:
        row_creation_time_upserted_count = 0
        row_creation_time_upsert_failure_count = 0

        if obj.row_creation_time_response:
            row_creation_time_upserted_count = len(obj.row_creation_time_response.columns_set_as_row_creation_time)
            row_creation_time_upsert_failure_count = len(
                obj.row_creation_time_response.row_creation_time_upsert_failures
            )

        metric_application_errors = []

        def is_wildcard_search(cohort: CohortDefinition):
            return '*' in cohort.column_name_pattern or \
                '*' in cohort.table_name_pattern or \
                '*' in cohort.schema_name_pattern

        for mae in obj.metric_application_errors:
            metric_application_errors.append(mae.to_dict())

        invalid_asset_identifier_errors = [ice.to_dict() for ice in obj.invalid_cohort_errors]

        pr = MetricSuiteReport(
            process_stage=process_stage,
            source_name=source_name,
            created_metrics=[i.to_dict(casing=Casing.SNAKE) for i in obj.created_metrics],
            updated_metrics=[i.to_dict(casing=Casing.SNAKE) for i in obj.updated_metrics],
            deleted_metrics=[i.to_dict(casing=Casing.SNAKE) for i in obj.deleted_metrics],
            unchanged_metrics=[i.to_dict(casing=Casing.SNAKE) for i in obj.unchanged_metrics],
            metric_application_errors=metric_application_errors,
            invalid_asset_identifier_errors=invalid_asset_identifier_errors,
            created_metric_count=len(obj.created_metrics),
            updated_metric_count=len(obj.updated_metrics),
            deleted_metric_count=len(obj.deleted_metrics),
            unchanged_metric_count=len(obj.unchanged_metrics),
            metric_application_error_count=len(metric_application_errors),
            invalid_asset_identifier_count=len(invalid_asset_identifier_errors),
            row_creation_time_report=obj.row_creation_time_response.to_dict(casing=Casing.SNAKE),
            row_creation_time_upserted_count=row_creation_time_upserted_count,
            row_creation_time_upsert_failure_count=row_creation_time_upsert_failure_count,
        )

        return pr

    @classmethod
    def from_fast_purge(
            cls, source_name: str, process_stage: ProcessStage, deleted_metric_count: int
    ) -> MetricSuiteReport:
        return MetricSuiteReport(
            process_stage=process_stage,
            source_name=source_name,
            metric_application_errors=[],
            invalid_asset_identifier_errors=[],
            created_metric_count=0,
            updated_metric_count=0,
            deleted_metric_count=deleted_metric_count,
            unchanged_metric_count=0,
            metric_application_error_count=0,
            invalid_asset_identifier_count=0,
            row_creation_time_report={},
            row_creation_time_upserted_count=0,
            row_creation_time_upsert_failure_count=0,
        )
