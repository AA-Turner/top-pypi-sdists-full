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
import concurrent.futures
import json
import sys
from typing import Optional

import click
import click_completion

from bq_validator.bigquery import create_bigquery_client, validate_query
from bq_validator.utils import get_sql_files, read_file

# Initialize click-completion
click_completion.init()


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--quota_project", type=str, required=False, help="BigQuery client project ID"
)
@click.option(
    "--client_project", type=str, required=False, help="BigQuery client project ID"
)
@click.option(
    "--client_location", type=str, required=False, help="BigQuery client location"
)
@click.option(
    "--impersonate_service_account",
    type=str,
    required=False,
    help="Impersonate service account email",
)
@click.option(
    "--num_parallels",
    type=int,
    required=False,
    default=1,
    help="Number of parallel query validations",
)
@click.option("--verbose", is_flag=True, help="Enable verbose output")
# pylint: disable=R0917
def main(
    path: str,
    quota_project: Optional[str],
    client_project: Optional[str],
    client_location: Optional[str],
    impersonate_service_account: Optional[str],
    num_parallels: Optional[int] = 1,
    verbose: Optional[bool] = False,
):
    """Validate BigQuery queries

    PATH is either of a SQL file path or a directory.
    When it is a directory, the command recursively validates all SQL files in the directory.
    """
    # Create a BigQuery client
    client = create_bigquery_client(
        client_project_id=client_project,
        quota_project_id=quota_project,
        location=client_location,
        impersonate_service_account=impersonate_service_account,
    )
    # Validate queries in parallel
    sql_files = get_sql_files(path=path)
    errors = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_parallels) as executor:
        futures = {
            executor.submit(validate_and_collect_errors, client, sql_file, verbose)
            for sql_file in sql_files
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                query_file, error_details = result
                errors[query_file] = error_details
    # Show errors
    if len(errors) > 0:
        click.echo(json.dumps(errors, indent=2))
        sys.exit(1)


def validate_and_collect_errors(client, query_file, verbose: Optional[bool] = False):
    """Validate a query and collect errors if any"""
    if verbose:
        click.echo(f"Validating {query_file}")
    query = read_file(path=query_file)
    is_valid, error_message = validate_query(client=client, query=query)
    if not is_valid:
        if verbose:
            click.echo(f"Error: {error_message}")
        return query_file, {"query": query, "error": error_message}
    return None
