from typing import List

from bigeye_sdk.log import get_logger
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.functions.bigconfig_functions import build_fq_name
from bigeye_sdk.generated.com.bigeye.models.generated import MetricConfiguration, MetricCreationState, MetricInfoList
from bigeye_sdk.model.big_config import TagDeployment, RowCreationTimes, BigConfig, ColumnSelector
from bigeye_sdk.model.protobuf_message_facade import SimpleCollection, SimpleMetricDefinition

log = get_logger(__name__)


class MetricController:

    def __init__(self, client: DatawatchClient):
        self.client = client

    @staticmethod
    def delete_metrics(metrics: List[MetricConfiguration]):
        deleatable = [m for m in metrics if m.metric_creation_state != MetricCreationState.METRIC_CREATION_STATE_SUITE]

    def metric_info_to_bigconfig(self,
                                 metric_info: MetricInfoList,
                                 collection: SimpleCollection = None) -> BigConfig:
        # Loop through metrics and create list of tag deployments / row creation times
        tag_deployments: List[TagDeployment] = []
        rct_columns: List[ColumnSelector] = []
        for m in metric_info.metrics:
            meta = m.metric_metadata

            # Get the fully qualified column selector for each metric
            if m.metric_configuration.is_table_metric:
                fq_selector = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name, "*")
            elif m.metric_configuration.metric_type.template_metric.template_id != 0:
                column_name = next((p.column_name for p in m.metric_configuration.parameters if p.column_name), None)
                fq_selector = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name, column_name)
            else:
                fq_selector = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name, meta.field_name)
            tag_deployments.append(TagDeployment(
                column_selectors=[ColumnSelector(name=fq_selector)],
                metrics=[SimpleMetricDefinition.from_datawatch_object(m.metric_configuration)])
            )

            # Get the row creation time column
            if meta.dataset_time_column_name and meta.dataset_time_column_name not in ['Collected time', '']:
                rct_column = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name,
                                           meta.dataset_time_column_name)
                rct_columns.append(ColumnSelector(name=rct_column))

        row_creation_times = RowCreationTimes(column_selectors=list(set(rct_columns)))

        dtw_is_default: bool = [ac.boolean_value for ac in self.client.get_advanced_configs()
                                if ac.key == "metric.data_time_window.default"][0]

        return BigConfig.tag_deployments_to_bigconfig(tag_deployments=tag_deployments,
                                                      row_creation_times=row_creation_times,
                                                      collection=collection,
                                                      dtw_is_default=dtw_is_default)
