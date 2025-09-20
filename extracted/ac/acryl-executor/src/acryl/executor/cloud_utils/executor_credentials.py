# Copyright 2021 Acryl Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Any, Optional

from datahub.ingestion.graph.client import DataHubGraph

from acryl.executor.cloud_utils.env_utils import get_executor_pool_id

logger = logging.getLogger(__name__)

LIST_EXECUTOR_CONFIGS_QUERY = """query listExecutorConfigs {
    listExecutorConfigs {
        total
        executorConfigs {
            region
            executorId
            queueUrl
            accessKeyId
            secretKeyId
            sessionToken
            expiration
        }
    }
}"""


class ExecutorCredentials:
    def __init__(self, graph: DataHubGraph):
        self.graph = graph

    def _parse_executor_configs_response(
        self, response_data: dict[str, Any], executor_pool_id: str
    ) -> Optional[dict[str, Any]]:
        """
        Parse GraphQL response to extract executor credentials.

        Args:
            response_data: Raw GraphQL response data
            executor_pool_id: The executor pool ID to find credentials for

        Returns:
            Dictionary containing AWS credentials if found, None otherwise
        """

        executor_configs = response_data.get("listExecutorConfigs", {}).get(
            "executorConfigs", []
        )

        # Find the matching executor config
        for config in executor_configs:
            if config.get("executorId") == executor_pool_id:
                logger.debug(f"Found credentials for executor pool {executor_pool_id}")
                return {
                    "region": config.get("region"),
                    "access_key_id": config.get("accessKeyId"),
                    "secret_access_key": config.get("secretKeyId"),
                    "session_token": config.get("sessionToken"),
                    "expiration": config.get("expiration"),
                }

        logger.warning(f"No credentials found for executor pool {executor_pool_id}")
        return None

    def get_executor_credentials(self) -> Optional[dict[str, Any]]:
        """
        Fetch executor credentials from DataHub GraphQL API.

        Args:

        Returns:
            Dictionary containing AWS credentials if found, None otherwise
        """
        executor_pool_id = get_executor_pool_id()
        if not executor_pool_id:
            return None

        logger.debug(f"Fetching executor credentials for pool {executor_pool_id}")
        try:
            res_data = self.graph.execute_graphql(
                query=LIST_EXECUTOR_CONFIGS_QUERY, variables={}
            )

            return self._parse_executor_configs_response(res_data, executor_pool_id)

        except Exception as e:
            logger.exception(
                f"Failed to fetch executor credentials for pool {executor_pool_id}: {e}"
            )
            return None
