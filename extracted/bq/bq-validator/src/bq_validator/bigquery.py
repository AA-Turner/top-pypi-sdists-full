#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List, Optional, Tuple

from google import auth
from google.auth import impersonated_credentials
from google.cloud import bigquery

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform",
]


# pylint: disable=R0917
def create_bigquery_client(
    client_project_id: Optional[str] = None,
    quota_project_id: Optional[str] = None,
    location: Optional[str] = None,
    impersonate_service_account: Optional[str] = None,
    scopes: Optional[List[str]] = None,
    lifetime: Optional[int] = None,
) -> bigquery.Client:
    """Get a BigQuery client

    Args:
        client_project_id: The client project ID
        quota_project_id: The quota project ID
        location: The job location
        impersonate_service_account: The service account email
        scopes: scopes
        lifetime: impersonation lifetime

    Returns:
        bigquery.Client: client
    """
    # pylint: disable=R1705
    if impersonate_service_account is None:
        credentials = get_default_credentials(project_id=quota_project_id)
        return bigquery.Client(
            credentials=credentials, project=client_project_id, location=location
        )
    else:
        credentials = get_impersonate_credentials(
            impersonate_service_account=impersonate_service_account,
            quoted_project_id=quota_project_id,
            scopes=scopes,
            lifetime=lifetime,
        )
        return bigquery.Client(
            credentials=credentials, project=client_project_id, location=location
        )


def get_default_credentials(
    project_id: Optional[str] = None,
) -> auth.credentials.Credentials:
    """Get the default credentials"""
    if project_id is not None:
        credentials, _ = auth.default(quota_project_id=project_id)
    else:
        credentials, _ = auth.default()
    return credentials


def get_impersonate_credentials(
    impersonate_service_account: str,
    quoted_project_id: Optional[str] = None,
    scopes: Optional[List[str]] = None,
    lifetime: Optional[int] = None,
) -> impersonated_credentials.Credentials:
    """Get a impersonate credentials"""
    # Create a impersonated service account
    if scopes is None:
        scopes = DEFAULT_SCOPES
    if lifetime is None:
        # NOTE The maximum life time is 3600s. If we can't load a table within 1 hour,
        #      we have to consider alternative way.
        lifetime = 3600

    source_credentials, _ = auth.default()
    if quoted_project_id is not None:
        source_credentials, quoted_project_id = auth.default(
            quota_project_id=quoted_project_id
        )
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=impersonate_service_account,
        target_scopes=scopes,
        lifetime=lifetime,
    )
    return target_credentials


def validate_query_async(
    client: bigquery.Client, query: str
) -> Tuple[bool, Optional[str]]:
    """Validate a query asynchronously"""
    job_config = bigquery.QueryJobConfig()
    job_config.dry_run = True
    job = client.query(query=query, job_config=job_config)
    return job.dry_run


def validate_query(client: bigquery.Client, query: str) -> Tuple[bool, Optional[str]]:
    """Validate q query

    Args:
        client: The BigQuery client
        query: The validated query

    Returns:
        Tuple[bool, Optional[str]]:
    """
    # Create a job config
    job_config = bigquery.QueryJobConfig()
    job_config.dry_run = True
    # Query dry run
    try:
        client.query(query=query, job_config=job_config)
        return True, None
    # pylint: disable=W0703
    except Exception as e:
        return False, str(e).strip()
