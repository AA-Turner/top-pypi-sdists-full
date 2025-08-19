import os
import re
from datetime import datetime
from typing import Iterable, Optional
from urllib.parse import unquote

from botocore.exceptions import ClientError
from loguru import logger
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ObjectTypeDef

from gable.cli.helpers.data_asset_s3.compression_handler import CompressionHandler
from gable.cli.helpers.data_asset_s3.logger import log_debug, log_error, log_trace
from gable.cli.helpers.data_asset_s3.path_pattern_manager import (
    DATETIME_DIRECTORY_TYPE,
    FULL_DATE_REGEXES,
    SUPPORTED_FILE_TYPES,
    SUPPORTED_FILE_TYPES_SET,
    PathPatternManager,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.logging import log_execution_time


@log_execution_time
def discover_patterns_from_s3_bucket(
    client: S3Client,
    bucket_name: str,
    recent_file_count: int,
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    start_date: datetime,
    end_date: Optional[datetime] = None,
    files_per_directory: int = 1000,
    ignore_timeframe_bounds: bool = False,
) -> dict[str, list[tuple[datetime, str]]]:
    """
    Discover patterns in an S3 bucket.

    Args:
        client: S3 client.
        bucket_name (str): S3 bucket.
        start_date (datetime): The furthest back in time we'll crawl to discover patterns
        end_date (datetime, optional): The most recent point in time we'll crawl to discover patterns. Defaults to None, which implies crawl to now.
        include_prefix (tuple[str], optional): list of prefixes to include
        exclude_prefix (tuple[str], optional): list of prefixes to exclude
        files_per_directory (int, optional): Number of files per directory. Defaults to 1000.

    Returns:
        list[str]: List of patterns.
    """
    logger.info("Starting pattern discovery in bucket: {}", bucket_name)
    _validate_bucket_exists(client, bucket_name)
    path_manager = PathPatternManager(recent_file_count)
    _discover_file_paths_from_s3_bucket(
        client,
        path_manager,
        bucket_name,
        "",
        include_prefix,
        exclude_prefix,
        files_per_directory,
        ignore_timeframe_bounds,
        start_date,
        end_date,
    )
    result = path_manager.get_pattern_to_actual_paths()
    if (asset_count := len(result)) > 0:
        file_count = sum([len(urls) for urls in result.values()])
        logger.info(
            f"{EMOJI.GREEN_CHECK.value} {asset_count} S3 data asset(s) found across {file_count} files"
        )
    else:
        logger.error(
            f"{EMOJI.RED_X.value} No S3 data assets discovered in bucket! You can use the --debug or --trace flags for more details.",
        )
    return result


def _discover_file_paths_from_s3_bucket(
    client: S3Client,
    path_manager: PathPatternManager,
    bucket_name: str,
    prefix: str,
    include_prefix: Optional[tuple[str, ...]],
    exclude_prefix: Optional[tuple[str, ...]],
    max_ls_results,
    ignore_timeframe_bounds: bool,
    start_date: datetime,
    end_date: Optional[datetime] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    second: Optional[int] = None,
):
    """
    Discover patterns in an S3 bucket via populating pattern_manager recursively.

    Args:
        client: S3 client.
        path_manager (PathPatternManager): Path pattern manager whose underlying structures are populated by this function
        bucket_name (str): S3 bucket.
        prefix (str): Prefix.
        include_prefix (tuple[str], optional): list of prefixes to include
        exclude_prefix (tuple[str], optional): list of prefixes to exclude
        max_ls_results (int, optional): Maximum number of results to return when listing items in a prefix. Defaults to 1000.
        ignore_timeframe_bounds (bool): Whether to ignore the start and end date bounds
        start_date (datetime): The furthest back in time we'll crawl to discover patterns
        end_date (datetime, optional): The most recent point in time we'll crawl to discover patterns. Defaults to None indicating "now".
        year (int, optional): The year if we're in a year directory. Defaults to None.
        month (int, optional): The month if we're in a month directory. Defaults to None.
        day (int, optional): The day if we're in a day directory. Defaults to None.
        hour (int, optional):  The hour if we're in an hour directory. Defaults to None.
        minute (int, optional): The minute if we're in a minute directory. Defaults to None.
        second (int, optional): The second if we're in a second directory. Defaults to None.
    """
    if (
        include_prefix
        and len(include_prefix) > 0
        and not any(
            [prefix.startswith(incl) or prefix in incl for incl in include_prefix]
        )
    ):
        log_trace_with_prefix(prefix, "Excluded by include pattern")
        return
    if (
        exclude_prefix
        and len(exclude_prefix) > 0
        and any([prefix.startswith(excl) for excl in exclude_prefix])
    ):
        # If include prefixes are passed in, then exclude prefixes should be a subset of the include prefixes to be considered
        log_trace_with_prefix(prefix, "Excluded by exclude pattern")
        return
    try:
        files = [
            obj["Key"] for obj in _list_files(client, bucket_name, max_ls_results, prefix)  # type: ignore
        ]

        # If we're in a month, day, hour, or minute folder, check for files and add them regardless of the name
        if files and any([month, day, hour, minute]):
            new_patterns = path_manager.add_filepaths(files)
            if new_patterns:
                log_trace_with_prefix(
                    prefix, f"Discovered {new_patterns} new pattern(s)"
                )
            else:
                log_trace_with_prefix(prefix, "No new pattern(s)")
        elif files:
            # Otherwise, list files and check to see if they have a datetime in them. This catches files like
            # data/shipments_2024-01-01.csv
            datetime_files = [
                f
                for f in files
                if any(map(lambda x: re.search(x, f) is not None, FULL_DATE_REGEXES))
            ]
            # For each file, extract the year, month, day, hour, minute and verify it falls within the start
            # and end date
            datetime_files_to_add = []
            for f in datetime_files:
                basename = os.path.basename(f)
                success, _year, _month, _day, _hour, _minute, _second = (
                    _get_ymdhm_from_datetime_filename(basename)
                )
                if success and (
                    ignore_timeframe_bounds
                    or _is_within_look_back_window(
                        start_date,
                        end_date,
                        _year,
                        _month,
                        _day,
                        _hour,
                        _minute,
                        _second,
                    )
                ):
                    datetime_files_to_add.append(f)
                else:
                    log_trace_with_prefix(
                        prefix, f"Files excluded by timeframe bounds: {basename}"
                    )
            new_patterns = path_manager.add_filepaths(datetime_files_to_add)
            if new_patterns:
                log_trace_with_prefix(
                    prefix, f"Discovered {new_patterns} new pattern(s)"
                )
            else:
                log_trace_with_prefix(prefix, "No new pattern(s)")

        directories = _list_directories(client, bucket_name, prefix, max_ls_results)
        grouped_datetime_directories = _group_datetime_directories_by_type(
            directories, year, month, day, hour, minute
        )
        # Split out the non-datetime directories from the datetime directories
        non_datetime_directories = grouped_datetime_directories.pop(None, [])
        filtered_non_datetime_directories = list(
            _filter_non_alpha_difference_directories(non_datetime_directories)
        )
        # Recursively traverse all of the non-datetime directories, but first, another safety check...
        if len(filtered_non_datetime_directories) > 0:

            for dir in non_datetime_directories:
                _discover_file_paths_from_s3_bucket(
                    client,
                    path_manager,
                    bucket_name,
                    os.path.join(prefix, dir) + "/",
                    ignore_timeframe_bounds=ignore_timeframe_bounds,
                    start_date=start_date,
                    end_date=end_date,
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second,
                    max_ls_results=max_ls_results,
                    include_prefix=include_prefix,
                    exclude_prefix=exclude_prefix,
                )

        elif len(non_datetime_directories) > 0:
            log_debug(
                f"Found non-datetime directories with no alphabetical difference in {bucket_name}/{prefix}, (example {non_datetime_directories[0]}) skipping further traversal",
            )
        # Now handle the datetime directories
        for (
            datetime_directory_type,
            datetime_directories,
        ) in grouped_datetime_directories.items():
            if datetime_directory_type is not None and len(datetime_directories) > 0:
                # Sort the directories in reverse order so we can break out when we hit the first
                # datetime outside of the start_date
                datetime_directories.sort(reverse=True)
                for datetime_directory in datetime_directories:
                    success, _year, _month, _day, _hour, _minute, _second = (
                        _get_ymdhm_from_datetime_directory(
                            datetime_directory_type,
                            datetime_directory,
                            year,
                            month,
                            day,
                            hour,
                            minute,
                            second,
                        )
                    )
                    if success:
                        if ignore_timeframe_bounds or _is_within_look_back_window(
                            start_date,
                            end_date,
                            _year,
                            _month,
                            _day,
                            _hour,
                            _minute,
                            _second,
                        ):
                            _discover_file_paths_from_s3_bucket(
                                client,
                                path_manager,
                                bucket_name,
                                os.path.join(prefix, datetime_directory) + "/",
                                ignore_timeframe_bounds=ignore_timeframe_bounds,
                                start_date=start_date,
                                end_date=end_date,
                                year=_year,
                                month=_month,
                                day=_day,
                                hour=_hour,
                                minute=_minute,
                                second=_second,
                                max_ls_results=max_ls_results,
                                include_prefix=include_prefix,
                                exclude_prefix=exclude_prefix,
                            )
                        else:
                            log_trace_with_prefix(
                                prefix,
                                f"Directories excluded by timeframe bounds: {datetime_directory}/",
                            )
                    else:
                        log_trace_with_prefix(
                            prefix,
                            f"Failed to parse datetime directory {datetime_directory}, skipping further traversal",
                        )
    except Exception as e:
        log_error("Failed during pattern discovery in {}: {}", bucket_name, str(e))
        raise


def _is_within_look_back_window(
    start_date: datetime,
    end_date: Optional[datetime],
    year: Optional[int],
    month: Optional[int],
    day: Optional[int],
    hour: Optional[int],
    minute: Optional[int],
    second: Optional[int],
) -> bool:
    # If we're looking at a year directory, we only need to check the year
    if year is not None and not any([month, day, hour, minute, second]):
        return year >= start_date.year
    # If we're looking at a month directory, trim the start and end dates to the month
    # for the comparison
    if year is not None and month is not None and not any([day, hour, minute, second]):
        start_date_month = datetime(start_date.year, start_date.month, 1)
        end_date_month = (
            datetime(end_date.year, end_date.month, 1) if end_date else None
        )
        return datetime(year, month, 1) >= start_date_month and (
            end_date_month is None or datetime(year, month, 1) <= end_date_month
        )
    # Otherwise we have at least year, month, day - hour and minute are filled
    # in with 0 if not present
    if year and month and day:
        f_dt = datetime(year, month, day, hour or 0, minute or 0, second or 0)
        if f_dt >= start_date and (end_date is None or f_dt <= end_date):
            return True
    return False


def _get_ymdhm_from_datetime_directory(
    datetime_directory_type: DATETIME_DIRECTORY_TYPE,
    directory: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
    second: Optional[int] = None,
) -> tuple[
    bool,
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
]:
    directory = super_unquote(directory).rstrip("/")
    # the first match group is the equals prefix, all values after that are the datetime values
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.YEAR and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.YEAR.value, directory)
    ):
        return True, int(matches.group("year")), None, None, None, None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.MONTH and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.MONTH.value, directory)
    ):
        return True, year, int(matches.group("month")), None, None, None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.DAY and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.DAY.value, directory)
    ):
        return True, year, month, int(matches.group("day")), None, None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.HOUR and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.HOUR.value, directory)
    ):
        return True, year, month, day, int(matches.group("hour")), None, None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.MINUTE and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.MINUTE.value, directory)
    ):
        return True, year, month, day, hour, int(matches.group("minute")), None
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.SECOND and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.SECOND.value, directory)
    ):
        return True, year, month, day, hour, minute, int(matches.group("second"))

    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_SECOND and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.FULL_SECOND.value, directory)
    ):
        return (
            True,
            int(matches.group("year")),
            int(matches.group("month")),
            int(matches.group("day")),
            int(matches.group("hour")),
            int(matches.group("minute")),
            int(
                matches.group("second"),
            ),
        )
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_MINUTE and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.FULL_MINUTE.value, directory)
    ):
        return (
            True,
            int(matches.group("year")),
            int(matches.group("month")),
            int(matches.group("day")),
            int(matches.group("hour")),
            int(matches.group("minute")),
            None,
        )
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_HOUR and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.FULL_HOUR.value, directory)
    ):
        return (
            True,
            int(matches.group("year")),
            int(matches.group("month")),
            int(matches.group("day")),
            int(matches.group("hour")),
            None,
            None,
        )
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_DAY and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.FULL_DAY.value, directory)
    ):
        return (
            True,
            int(matches.group("year")),
            int(matches.group("month")),
            int(matches.group("day")),
            None,
            None,
            None,
        )
    if datetime_directory_type == DATETIME_DIRECTORY_TYPE.FULL_MONTH and (
        matches := re.match(DATETIME_DIRECTORY_TYPE.FULL_MONTH.value, directory)
    ):
        return (
            True,
            int(matches.group("year")),
            int(matches.group("month")),
            None,
            None,
            None,
            None,
        )
    return False, None, None, None, None, None, None


def _get_ymdhm_from_datetime_filename(
    directory: str,
) -> tuple[
    bool,
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
]:
    directory = super_unquote(directory).rstrip("/")
    if match_results := re.match(DATETIME_DIRECTORY_TYPE.FULL_SECOND.value, directory):
        return (
            True,
            int(match_results.group("year")),
            int(match_results.group("month")),
            int(match_results.group("day")),
            int(match_results.group("hour")),
            int(match_results.group("minute")),
            int(
                match_results.group("second"),
            ),
        )
    if match_results := re.match(DATETIME_DIRECTORY_TYPE.FULL_MINUTE.value, directory):
        return (
            True,
            int(match_results.group("year")),
            int(match_results.group("month")),
            int(match_results.group("day")),
            int(match_results.group("hour")),
            int(match_results.group("minute")),
            None,
        )
    if match_results := re.match(DATETIME_DIRECTORY_TYPE.FULL_HOUR.value, directory):
        return (
            True,
            int(match_results.group("year")),
            int(match_results.group("month")),
            int(match_results.group("day")),
            int(match_results.group("hour")),
            None,
            None,
        )
    if match_results := re.match(DATETIME_DIRECTORY_TYPE.FULL_DAY.value, directory):
        return (
            True,
            int(match_results.group("year")),
            int(match_results.group("month")),
            int(match_results.group("day")),
            None,
            None,
            None,
        )
    if match_results := re.match(DATETIME_DIRECTORY_TYPE.FULL_MONTH.value, directory):
        return (
            True,
            int(match_results.group("year")),
            int(match_results.group("month")),
            None,
            None,
            None,
            None,
        )
    return False, None, None, None, None, None, None


def _filter_non_alpha_difference_directories(
    directories: list[str], filter_threshold: int = 5
) -> Iterable[str]:
    """
    Filters out groups of directories that have no alphabetical difference between them, but have a consistent pattern. This is
    used to avoid traversing directories that have a consistent pattern, but are not understood by the pattern discovery
    algorithm. This is done by removing all whitespace, non-printable characters, and replacing all consecutive digits with
    a placeholder character. If the number of directories in a group is >= than the filter_threshold, they're filtered from
    the results.

    Example:
        ["0000001", "0000002", "0000003"] would return [] (filter_threshold = 3)
        ["data_1", "data_12", "data_123", "other_dir"] would return ["other_dir"] (filter_threshold = 3)
        ["data_a_1", "data_b_1", "data_c_1"] would return ["data_a_1", "data_b_1", "data_c_1"] (filter_threshold = 3)
    Args:
        directories (list[str]): List of directories.

    Returns:
        list[str]: Filtered list of directories.
    """
    if len(directories) == 1:
        yield directories[0]
        return
    stripped_directory_groups: dict[str, list[str]] = {}
    for directory in directories:
        # Remove all non-printable characters
        stripped = "".join(
            filter(
                lambda x: x.isprintable(),
                # Remove all whitespace
                re.sub(
                    r"\s",
                    "",
                    # Replace all consecutive digits with a single very uncommon ascii character §
                    re.sub(r"\d+", "§", directory),
                ),
            )
        )

        if stripped not in stripped_directory_groups:
            stripped_directory_groups[stripped] = []
        stripped_directory_groups[stripped].append(directory)

    for _, directories in stripped_directory_groups.items():
        if len(directories) < filter_threshold:
            for d in directories:
                yield d


def _group_datetime_directories_by_type(
    directories: list[str], year=None, month=None, day=None, hour=None, minute=None
) -> dict[Optional[DATETIME_DIRECTORY_TYPE], list[str]]:
    directory_groups = {}
    for directory in directories:
        directory_type = _get_datetime_directory_type(
            directory, year, month, day, hour, minute
        )

        if directory_type not in directory_groups:
            directory_groups[directory_type] = []
        directory_groups[directory_type].append(directory)
    return directory_groups


def _get_datetime_directory_type(
    directory: str, year=None, month=None, day=None, hour=None, minute=None, second=None
) -> Optional[DATETIME_DIRECTORY_TYPE]:
    # Trim the directory to remove any trailing slashes
    directory = super_unquote(directory).rstrip("/")
    # If we're already in a second directory, don't go any deeper
    if second is not None:
        return None
    # Otherwise check if the directory matches the next logical datetime part regex
    if (
        minute is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.SECOND.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.SECOND
    if (
        hour is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.MINUTE.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.MINUTE
    if (
        day is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.HOUR.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.HOUR
    if (
        month is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.DAY.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.DAY
    if (
        year is not None
        and re.fullmatch(DATETIME_DIRECTORY_TYPE.MONTH.value, directory) is not None
    ):
        return DATETIME_DIRECTORY_TYPE.MONTH
    # At this point we're not in any sort of datetime directory, so check if it's a year directory, or a full date directory
    if re.fullmatch(DATETIME_DIRECTORY_TYPE.YEAR.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.YEAR

    if re.match(DATETIME_DIRECTORY_TYPE.FULL_SECOND.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_SECOND
    if re.match(DATETIME_DIRECTORY_TYPE.FULL_MINUTE.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_MINUTE
    if re.match(DATETIME_DIRECTORY_TYPE.FULL_HOUR.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_HOUR
    if re.match(DATETIME_DIRECTORY_TYPE.FULL_DAY.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_DAY
    if re.match(DATETIME_DIRECTORY_TYPE.FULL_MONTH.value, directory) is not None:
        return DATETIME_DIRECTORY_TYPE.FULL_MONTH
    return None


def _list_directories(
    client: S3Client, bucket_name: str, prefix: str, max_ls_results: int = 1000
) -> list[str]:
    """
    List all directories in an S3 bucket. Returns only the directory names, not the full path.

    Args:
        client: S3 client.
        bucket_name (str): S3 bucket.
        prefix (str): Prefix. This is used for recursive calls and differs from kwargs["include"] which is a configuration option.
        max_ls_results (int, optional): Maximum number of results to return when listing items in a prefix. Defaults to 1000.
    Returns:
        list[str]: List of directories.
    """
    paginator = client.get_paginator("list_objects_v2")

    pagination_result = (
        paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix,
            Delimiter="/",
            PaginationConfig={"MaxItems": max_ls_results},
        ).search("CommonPrefixes")
        or []
    )

    filtered_results = []
    for result in pagination_result:
        if result is not None and "Prefix" in result:
            filtered_results.append(result["Prefix"])

    log_trace_with_prefix(
        prefix,
        f"Completed listing directories, total directories gathered: {len(filtered_results)}",
    )
    return [item.rstrip("/").split("/")[-1] for item in filtered_results]


def _list_files(
    client: S3Client, bucket_name: str, max_files: int, prefix: str = ""
) -> list[ObjectTypeDef]:
    """
    List objects in an S3 bucket.

    Args:
        client: S3 client.
        bucket_name (str): S3 bucket.
        max_files (int): Maximum number of files to list.
        prefix (str, optional): Prefix. Defaults to None.

    Returns:
        dict[str, object]: mapping of file names to contents.
    """
    paginator = client.get_paginator("list_objects_v2")
    files: list[ObjectTypeDef] = []
    for page in paginator.paginate(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter="/",
        PaginationConfig={"MaxItems": max_files},
    ):
        for obj in page.get("Contents", []):
            if obj.get("Size", 0) == 0:
                continue
            files.append(obj)
    log_trace_with_prefix(
        prefix, f"Completed listing files, total files gathered: {len(files)}"
    )
    return files


def is_supported_file_type(file_path: str) -> bool:
    """
    Returns True if the file is a supported type (e.g. .csv, .orc),
    considering both raw and compressed file extensions.
    """
    return any(
        file_path.endswith(file_type)
        or CompressionHandler.get_original_format(file_path).extension.endswith(  # type: ignore
            file_type
        )
        for file_type in SUPPORTED_FILE_TYPES_SET
    )


def super_unquote(s: str):
    new_s, _ = super_unquote_n(s)
    return new_s


def super_unquote_n(s: str):
    if s == unquote(s):
        return s, 0
    old_s = s
    s = unquote(s)
    quote_count = 1
    while s != old_s:
        old_s = s
        s = unquote(s)
        quote_count += 1
    return s, quote_count


def _validate_bucket_exists(client, bucket_name: str) -> None:
    log_trace("Validating existence of bucket: {}", bucket_name)
    try:
        client.head_bucket(Bucket=bucket_name)
        log_trace("Bucket exists: {}", bucket_name)
    except client.exceptions.ClientError as e:
        if isinstance(e, ClientError):
            error_code = int(e.response["Error"]["Code"])  # type: ignore
            if error_code == 404:
                print(f"Bucket {bucket_name} does not exist.")
                log_error("Bucket does not exist for {}: {}", bucket_name, str(e))
            elif error_code == 403:
                print(f"Access to bucket {bucket_name} is forbidden.")
                log_error(
                    "Access to bucket is forbidden for {}: {}", bucket_name, str(e)
                )
        raise ValueError(
            f"Bucket {bucket_name} does not exist or is not accessible. Check that AWS credentials are set up correctly."
        )


def flatten(lists: list[list]):
    return list((item for sublist in lists for item in sublist))


def log_trace_with_prefix(prefix: str, message: str, *args):
    log_trace(f"(/{prefix})\t{message}", *args)
