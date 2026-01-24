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
import threading
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import click
import click_completion

from bq_validator.bigquery import create_bigquery_client, validate_query
from bq_validator.utils import get_sql_files, read_file

# Initialize click-completion
click_completion.init()


class ValidationStatus(Enum):
    """Enumeration of possible validation result statuses."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"


@dataclass
class ValidationResult:
    """Represents the result of validating a single SQL file."""
    status: ValidationStatus  # SUCCESS, ERROR, or WARNING
    file_path: Optional[str] = None  # None for success cases
    details: Optional[dict] = None   # None for success cases


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
@click.option(
    "--warn-on-empty",
    is_flag=True,
    help="Show just warning(s) not to raise error(s) if the given file(s) are empty",
)
@click.option("--stats", is_flag=True, help="Show the summary of the results")
# pylint: disable=R0917
def main(
    path: str,
    quota_project: Optional[str],
    client_project: Optional[str],
    client_location: Optional[str],
    impersonate_service_account: Optional[str],
    num_parallels: Optional[int] = 1,
    verbose: Optional[bool] = False,
    warn_on_empty: Optional[bool] = False,
    stats: Optional[bool] = False,
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

    # Run validation and get results
    results = validate_queries(client, path, num_parallels, verbose, warn_on_empty)

    # Process and display results
    display_results(results, stats)


def validate_queries(
    client,
    path: str,
    num_parallels: Optional[int],
    verbose: Optional[bool],
    warn_on_empty: Optional[bool],
) -> list:
    """Validate all SQL queries in the given path"""
    sql_files = get_sql_files(path=path)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_parallels, thread_name_prefix="Worker") as executor:
        futures = {
            executor.submit(
                validate_and_collect_errors, client, sql_file, verbose, warn_on_empty, num_parallels
            )
            for sql_file in sql_files
        }
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results


def display_results(results: list, show_stats: Optional[bool]):
    """Process and display validation results"""
    # Process results
    errors = {
        result.file_path: result.details
        for result in results
        if result.status in (ValidationStatus.ERROR, ValidationStatus.WARNING)
    }

    # Show summary when requested
    if show_stats:
        status_counts = Counter(result.status for result in results)
        stats_data = {
            "summary": {
                "total": len(results),
                "success": status_counts[ValidationStatus.SUCCESS],
                "errors": status_counts[ValidationStatus.ERROR],
                "warnings": status_counts[ValidationStatus.WARNING]
            }
        }
        click.echo(json.dumps(stats_data, indent=2))

    # Show errors regardless of stats flag
    if len(errors) > 0:
        click.echo(json.dumps(errors, indent=2))

    # Exit with error code if there are actual errors (not just warnings)
    if any(result.status == ValidationStatus.ERROR for result in results):
        sys.exit(1)


def validate_and_collect_errors(
    client,
    query_file,
    verbose: Optional[bool] = False,
    warn_on_empty: Optional[bool] = False,
    total_workers: Optional[int] = 1,
):
    """Validate a query and collect errors if any"""
    worker_name = threading.current_thread().name
    # Extract worker index from thread name (e.g., "Worker_0" -> 0)
    try:
        worker_index = int(worker_name.split("_")[-1]) + 1  # Add 1 to make it 1-based
    except (ValueError, IndexError):
        worker_index = 1  # Fallback if parsing fails

    worker_prefix = f"[Worker {worker_index} / {total_workers}]"
    if verbose:
        click.echo(f"{worker_prefix} Validating {query_file}")
    try:
        query = read_file(path=query_file)
        if not query:
            if warn_on_empty:
                if verbose:
                    click.echo(f"{worker_prefix} Warning: {query_file} is empty. Skipping validation.")
                # Return warning if the query is empty and warn_on_empty is set
                return ValidationResult(
                    status=ValidationStatus.WARNING,
                    file_path=query_file,
                    details={"query": query, "warning": "Query is empty"}
                )
            # Return error if the query is empty and warn_on_empty is not set
            if verbose:
                click.echo(f"{worker_prefix} Error in {query_file}: Query is empty")
            return ValidationResult(
                status=ValidationStatus.ERROR,
                file_path=query_file,
                details={"query": query, "error": "Query is empty"}
            )

        is_valid, error_message = validate_query(client=client, query=query)
        if not is_valid:
            if verbose:
                click.echo(f"{worker_prefix} Error in {query_file}: {error_message}")
            return ValidationResult(
                status=ValidationStatus.ERROR,
                file_path=query_file,
                details={"query": query, "error": error_message}
            )
        if verbose:
            click.echo(f"{worker_prefix} Success: {query_file} is valid")
        return ValidationResult(status=ValidationStatus.SUCCESS)
    except Exception as e:  # pylint: disable=broad-except
        error_msg = str(e).strip()
        if verbose:
            click.echo(f"{worker_prefix} Error in {query_file}: {error_msg}")
        return ValidationResult(
            status=ValidationStatus.ERROR,
            file_path=query_file,
            details={"query": "", "error": error_msg}
        )
