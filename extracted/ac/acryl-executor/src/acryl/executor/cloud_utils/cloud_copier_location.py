import logging

from datahub.ingestion.graph.client import get_default_graph

logger = logging.getLogger(__name__)


MUTATION_QUERY = """
mutation storeExecutionRequestUploadLocation($input: StoreExecutionRequestUploadLocationInput!) {
  storeExecutionRequestUploadLocation(input: $input) {
    success
  }
}
"""


class CloudCopierLocation:
    def send_location(self, bucket: str, base_path: str, execution_id: str) -> None:
        try:
            self._send_location(bucket, base_path, execution_id)
        except Exception:
            # Adding this to avoid this failing for older server versions
            # or OSS where the endpoint is not available
            logger.warning(f"Failed to send location for execution {execution_id}")

    def _send_location(self, bucket: str, base_path: str, execution_id: str) -> None:
        graph = get_default_graph()
        execution_urn = f"urn:li:dataHubExecutionRequest:{execution_id}"
        location = f"s3://{bucket}/{base_path}/executor-logs/executor-logs.tgz"
        logger.info(f"Sending location for execution {execution_id}: {location}")
        result = graph.execute_graphql(
            MUTATION_QUERY,
            variables={
                "input": {"executionRequestUrn": execution_urn, "location": location},
            },
        )
        logger.info(f"Location sent for execution {execution_id}: {result}")
