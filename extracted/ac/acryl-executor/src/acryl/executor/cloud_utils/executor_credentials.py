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
import os
from typing import Any, Optional

import requests

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
    def __init__(self, gms_url: str, gms_token: str):
        self.gms_url = gms_url
        self.gms_token = gms_token

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
        if "errors" in response_data:
            logger.error(f"GraphQL errors: {response_data['errors']}")
            return None

        executor_configs = (
            response_data.get("data", {})
            .get("listExecutorConfigs", {})
            .get("executorConfigs", [])
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

    def get_executor_credentials(
        self, executor_pool_id: str
    ) -> Optional[dict[str, Any]]:
        """
        Fetch executor credentials from DataHub GraphQL API.

        Args:
            executor_pool_id: The executor pool ID to fetch credentials for

        Returns:
            Dictionary containing AWS credentials if found, None otherwise
        """
        try:
            request_json = {"query": LIST_EXECUTOR_CONFIGS_QUERY, "variables": {}}

            headers = {
                "Authorization": f"Bearer {self.gms_token}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                f"{self.gms_url}/api/graphql", json=request_json, headers=headers
            )
            response.raise_for_status()

            res_data = response.json()
            return self._parse_executor_configs_response(res_data, executor_pool_id)

        except Exception as e:
            logger.exception(
                f"Failed to fetch executor credentials for pool {executor_pool_id}: {e}"
            )
            return None

    @classmethod
    def from_environment(cls) -> Optional["ExecutorCredentials"]:
        """
        Create ExecutorCredentials instance from environment variables.

        Returns:
            ExecutorCredentials instance if environment variables are present, None otherwise
        """
        gms_url = os.environ.get("DATAHUB_GMS_URL")
        gms_token = os.environ.get("DATAHUB_GMS_TOKEN")

        if not gms_url or not gms_token:
            logger.debug(
                "DATAHUB_GMS_URL or DATAHUB_GMS_TOKEN not found in environment"
            )
            return None

        return cls(gms_url, gms_token)
