"""
DataDog Utility methods.
"""
import time
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries


def submit_dataframe(
    host, api_key, app_key, metric_name, dataframe, datapoint_column,
    tag_columns=[], batch_size=500
):
    """
    Submit a pandas DataFrame to DataDog.

    Args:
        host (str): The DataDog API host.
        api_key (str): Your DataDog API key.
        app_key (str): Your DataDog application key.
        metric_name (str): The name of the metric to submit.
        dataframe (pandas.DataFrame): The DataFrame containing data to submit.
        datapoint_column (str): DataFrame column containing datapoints.
        tag_columns (list, optional): List of column names to be used as tags.
          Default is an empty list.
        batch_size (int, optional): Number of rows to submit in each batch.
          Default is 500.

    Returns:
        dict: A dictionary containing any errors encountered during submission.
          Format: {"errors": ["error_message_1", "error_message_2", ...]}.
    """
    responses = {"errors": []}
    # Setup configuration
    configuration = Configuration(host=host)
    configuration.api_key['apiKeyAuth'] = api_key
    configuration.api_key['appKeyAuth'] = app_key
    # Iterate in batches by provided batch size
    for start, end in [
        (i, min(i + batch_size, dataframe.shape[0]))
        for i in range(0, dataframe.shape[0], batch_size)
    ]:
        # Submit metrics to DataDog
        with ApiClient(configuration) as api_client:
            api_instance = MetricsApi(api_client)
            response = api_instance.submit_metrics(
                body=MetricPayload([
                    MetricSeries(
                        metric=metric_name,
                        type=MetricIntakeType.COUNT,
                        points=[MetricPoint(
                            timestamp=int(time.time()),
                            value=int(row[datapoint_column]))],
                        tags=[f"{t}:{row[t]}" for t in tag_columns])
                    for index, row in dataframe.loc[start:end].iterrows()]))

            responses["errors"] += response["errors"]

    return responses
