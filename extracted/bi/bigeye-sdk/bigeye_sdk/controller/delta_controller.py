from typing import List

from bigeye_sdk.functions.delta_functions import infer_column_mappings
from bigeye_sdk.generated.com.bigeye.models.generated import (
    TableApplicableMetricTypes,
    Table,
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.model.delta_facade import (
    SimpleTargetTableComparison,
    SimpleDeltaConfiguration,
)
from bigeye_sdk.model.protobuf_message_facade import (
    SimpleColumnMapping,
    SimpleNamedSchedule,
)

log = get_logger(__name__)


class DeltaController:
    def __init__(self, client: DatawatchClient):
        self.client = client

    def get_applicable_metric_types(self, table_id: int) -> TableApplicableMetricTypes:
        return self.client.get_delta_applicable_metric_types(
            table_id=table_id
        ).metric_types

    def create_template_delta_config(self, source_table: Table, target_tables: List[Table]) -> SimpleDeltaConfiguration:
        fq_source_name = (
            f"{source_table.warehouse_name}.{source_table.database_name}.{source_table.schema_name}.{source_table.name}"
        )
        source_metric_types = self.get_applicable_metric_types(source_table.id)

        comparisons = []
        fq_table_names = []

        for t in target_tables:
            fq_target_name = (
                f"{t.warehouse_name}.{t.database_name}.{t.schema_name}.{t.name}"
            )
            fq_table_names.append(fq_target_name)
            target_metric_types = self.get_applicable_metric_types(t.id)
            column_mappings = infer_column_mappings(
                source_metric_types=source_metric_types,
                target_metric_types=target_metric_types,
            )
            simple_mappings = [
                SimpleColumnMapping.from_datawatch_object(obj=cm) for cm in column_mappings
            ]
            comparisons.append(SimpleTargetTableComparison(
                    fq_target_table_name=fq_target_name,
                    delta_column_mapping=simple_mappings,
                    source_filters=[],
                    target_filters=[],
                    group_bys=[],
            ))

        return SimpleDeltaConfiguration(
            delta_name=f"{fq_source_name} <> {str.join(',',fq_table_names)}",
            fq_source_table_name=fq_source_name,
            target_table_comparisons=comparisons,
            tolerance=0.0,
            notification_channels=[],
            cron_schedule=SimpleNamedSchedule(
                name="Enter schedule name",
                cron="Define cron, if schedule does not exist. Otherwise just specify name.",
            )
        )
