import re
from datetime import datetime
from typing import Optional

import click
import deepdiff
from loguru import logger

from gable.cli.helpers.data_asset_s3.actions import get_s3_client
from gable.cli.helpers.data_asset_s3.native_s3_converter import NativeS3Converter
from gable.cli.helpers.data_asset_s3.path_pattern_manager import (
    DATE_PLACEHOLDER_TO_REGEX,
)
from gable.cli.helpers.data_asset_s3.pattern_discovery import (
    discover_patterns_from_s3_bucket,
)
from gable.cli.helpers.data_asset_s3.schema_detection import (
    append_s3_url_prefix,
    read_s3_files_with_schema_inference,
    strip_s3_bucket_prefix,
)
from gable.cli.option_defaults import DEFAULT_NUM_ROWS_TO_SAMPLE


def extract_date_from_pattern(pattern: str) -> Optional[str]:
    """Extract date from pattern using regex."""
    match = re.search(r"\d{4}/\d{2}/\d{2}", pattern)
    return match.group(0) if match else None


def format_deepdiff_output(deepdiff_result):
    """
    Formats the deepdiff output for CLI display.
    """
    formatted_output = []

    # Handle changed values
    values_changed = deepdiff_result.get("values_changed", {})
    if values_changed:
        formatted_output.append("\nChanged values:")
        for key, details in values_changed.items():
            parsed = parse_diff_key(key)
            formatted_output.append(
                f"  - {parsed} Changed from '{details['old_value']}' to '{details['new_value']}'"
            )
    # Handle items added
    items_added = deepdiff_result.get("iterable_item_added", {})
    if items_added:
        formatted_output.append("\nItems added:")
        for key, value in items_added.items():
            formatted_output.append(
                f"  - {key}: Added '{value['name']}' of Type '{value['type']}'"
            )

    # Handle items removed
    items_removed = deepdiff_result.get("iterable_item_removed", {})
    if items_removed:
        formatted_output.append("\nItems removed:")
        for key, value in items_removed.items():
            formatted_output.append(
                f"  - {key}: Removed '{value['name']}' of Type '{value['type']}'"
            )

    return "\n".join(formatted_output)


def extract_date_from_filepath(filepath):
    # This regex assumes the date format in the filepath is something like '2024/04/10'
    match = re.search(DATE_PLACEHOLDER_TO_REGEX["{YYYY}/{MM}/{DD}"], filepath)
    if match:
        return datetime.strptime(match.group(1), "%Y/%m/%d").date()
    return None


def parse_diff_key(key: str) -> str:
    # This regex extracts the index and the attribute being compared
    match = re.search(r"\['fields'\]\[(\d+)\]\['(\w+)'\]", key)
    if match:
        attribute = match.group(2)
        return f"{attribute.capitalize()}"
    return "Unknown field"


def get_schemas_from_files(
    pattern: str,
    files_urls: list[str],
    row_sample_count: Optional[int],
    recent_file_count: int,
) -> list[dict]:
    """Retrieve and convert data from S3 into Recap schemas."""

    s3_data = read_s3_files_with_schema_inference(
        s3_urls=files_urls,
        row_sample_count=row_sample_count or DEFAULT_NUM_ROWS_TO_SAMPLE,
        event_name=pattern,
        recent_file_count=recent_file_count,
        skip_profiling=True,
    )

    return [s3_data.schema]  # type: ignore


def compare_schemas(
    schema1: list[dict],
    schema2: list[dict],
    pattern: str,
    first_date: Optional[str],
    second_date: Optional[str],
):
    """Compare two sets of schemas and log the differences."""
    for schema_h, schema_t in zip(schema1, schema2):
        diff = deepdiff.DeepDiff(schema_h, schema_t, ignore_order=True)
        if diff:
            formatted_results = format_deepdiff_output(diff)
            logger.info(
                f"Differences detected in {pattern} between {first_date} and {second_date}: \n{formatted_results}"
            )
        else:
            logger.info(
                f"No differences detected in {pattern} between {first_date} and {second_date}"
            )


def detect_s3_data_assets_history(
    bucket_name: str,
    include_prefix: list[str],
    row_sample_count: int,
    recent_file_count: int,
):
    client = get_s3_client()
    first_pattern = include_prefix[0]
    second_pattern = include_prefix[1]
    first_date = extract_date_from_pattern(first_pattern)
    second_date = extract_date_from_pattern(second_pattern)
    first_date_files = discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket_name),
        recent_file_count,
        start_date=datetime(1970, 1, 1),
        end_date=None,
        include_prefix=(first_pattern,),
        exclude_prefix=None,
        ignore_timeframe_bounds=True,
    )
    second_date_files = discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket_name),
        recent_file_count,
        start_date=datetime(1970, 1, 1),
        end_date=None,
        include_prefix=(second_pattern,),
        exclude_prefix=None,
        ignore_timeframe_bounds=True,
    )
    all_patterns = list(set(first_date_files.keys()) | set(second_date_files.keys()))
    if not all_patterns:
        raise click.ClickException(
            "No data assets found to compare! Use the --debug or --trace flags for more details."
        )
    for pattern in all_patterns:
        # Retrieve schemas for both dates
        schema_historical = get_schemas_from_files(
            pattern,
            [
                append_s3_url_prefix(bucket_name, file_url)
                for _, file_url in first_date_files.get(pattern, [])
            ],
            row_sample_count,
            recent_file_count,
        )
        schema_today = get_schemas_from_files(
            pattern,
            [
                append_s3_url_prefix(bucket_name, file_url)
                for _, file_url in second_date_files.get(pattern, [])
            ],
            row_sample_count,
            recent_file_count,
        )
        compare_schemas(
            schema_historical, schema_today, first_pattern, first_date, second_date
        )
