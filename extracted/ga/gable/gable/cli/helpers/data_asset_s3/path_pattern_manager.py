import heapq
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Iterable, Optional
from urllib.parse import unquote

from gable.cli.helpers.data_asset_s3.compression_handler import CompressionHandler
from gable.cli.helpers.data_asset_s3.logger import log_debug

# backslashes are not allowed in f-strings before Python 3.12, so create an alias
_lead_zero_boundary = lambda require_leading_zero: (
    "" if require_leading_zero else "\\b"
)
_lead_zero_optional = lambda require_leading_zero: ("" if require_leading_zero else "?")

NUMBER_REGEX = r"(?P<number>\d+)"
NO_PRECEDING_DIGIT = r"(?:(?<!\d))+"  # non-capturing group to ensure that the preceding character is not a digit
YEAR_REGEX = r"(?P<year>20\d{2})"
# for month and day directories we want to allow numbers without a leading a zero (ie 1 or 01 is valid for January)
# but for date strings we want to require a leading zero (ie 2024-01-01 is valid but 2024-1-01 is not). The inner lambdas here
# allow for finer control of this when constructing the compound regexes
MONTH_REGEX = (
    lambda require_leading_zero: rf"{_lead_zero_boundary(require_leading_zero)}(?P<month>0{_lead_zero_optional(require_leading_zero)}[1-9]|1[0-2]){_lead_zero_boundary(require_leading_zero)}"
)
DAY_REGEX = (
    lambda require_leading_zero: rf"{_lead_zero_boundary(require_leading_zero)}(?P<day>0{_lead_zero_optional(require_leading_zero)}[1-9]|[12][0-9]|3[01]){_lead_zero_boundary(require_leading_zero)}"
)
HOUR_REGEX = r"(?P<hour>[01][0-9]|2[0-3])"
MINUTE_REGEX = r"(?P<minute>[0-5][0-9])"
SECOND_REGEX = r"(?P<second>[0-5][0-9])"
MICROSECOND_REGEX = r"(?P<microsecond>\d{6})"
MILLISECOND_REGEX = r"(?P<millisecond>\d{3})"
EPOCH_REGEX = r"(?P<epoch><!\d)\d{10}(?!\d)"
# Time-based
UUID_REGEX_V1 = r"(?P<uuidv1>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-1[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12})"
# Name-based using MD5 hashing
UUID_REGEX_V3 = r"(?P<uuidv3>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-3[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12})"
# Randomly generated
UUID_REGEX_V4 = r"(?P<uuidv4>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12})"
# Name-based using SHA-1 hashing
UUID_REGEX_V5 = r"(?P<uuidv5>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-5[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12})"

DATE_PART_DELIMITERS = (
    lambda num, extra_delimiters="": rf"(?P<d{num}>[-_:{extra_delimiters} ]{{0,2}})"
)

FULL_DATE_MONTH_REGEX = rf"{YEAR_REGEX}{DATE_PART_DELIMITERS(1)}{MONTH_REGEX(True)}"
FULL_DATE_DAY_REGEX = (
    rf"{FULL_DATE_MONTH_REGEX}{DATE_PART_DELIMITERS(2)}{DAY_REGEX(True)}"
)
FULL_DATE_HOUR_REGEX = rf"{FULL_DATE_DAY_REGEX}{DATE_PART_DELIMITERS(3, 'T')}{HOUR_REGEX}"  # allow T for dates like 2024-01-01T00:00:00
FULL_DATE_MINUTE_REGEX = (
    rf"{FULL_DATE_HOUR_REGEX}{DATE_PART_DELIMITERS(4)}{MINUTE_REGEX}"
)
FULL_DATE_SECOND_REGEX = (
    rf"{FULL_DATE_MINUTE_REGEX}{DATE_PART_DELIMITERS(5)}{SECOND_REGEX}"
)

# only a period or nothing is allowed to delimit seconds and microseconds/milliseconds
FULL_DATE_MICROSECOND_REGEX = rf"{FULL_DATE_SECOND_REGEX}(?P<d6>\.?){MICROSECOND_REGEX}"
FULL_DATE_MILLISECOND_REGEX = rf"{FULL_DATE_SECOND_REGEX}(?P<d6>\.?){MILLISECOND_REGEX}"
FULL_DATE_REGEXES = [
    FULL_DATE_MILLISECOND_REGEX,
    FULL_DATE_MICROSECOND_REGEX,
    FULL_DATE_SECOND_REGEX,
    FULL_DATE_MINUTE_REGEX,
    FULL_DATE_HOUR_REGEX,
    FULL_DATE_DAY_REGEX,
    FULL_DATE_MONTH_REGEX,
]

EQUALS_PREFIX_REGEX = lambda num: rf"(?P<p{num}>{NO_PRECEDING_DIGIT}[a-zA-Z-_:]*=?)"


class DATETIME_DIRECTORY_TYPE(Enum):
    YEAR = rf"{EQUALS_PREFIX_REGEX(1)}{YEAR_REGEX}"
    MONTH = rf"{EQUALS_PREFIX_REGEX(1)}{MONTH_REGEX(False)}"
    DAY = rf"{EQUALS_PREFIX_REGEX(1)}{DAY_REGEX(False)}"
    HOUR = rf"{EQUALS_PREFIX_REGEX(1)}{HOUR_REGEX}"
    MINUTE = rf"{EQUALS_PREFIX_REGEX(1)}{MINUTE_REGEX}"
    SECOND = rf"{EQUALS_PREFIX_REGEX(1)}{SECOND_REGEX}"
    # purposely do not include FULL_MICROSECOND or FULL_MILLISECOND. micro/milliseconds are too granular
    # for directory structure but are possible in file names
    FULL_SECOND = rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_SECOND_REGEX}"
    FULL_MINUTE = rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_MINUTE_REGEX}"
    FULL_HOUR = rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_HOUR_REGEX}"
    FULL_DAY = rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_DAY_REGEX}"
    FULL_MONTH = rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_MONTH_REGEX}"


DATE_PLACEHOLDER_TO_REGEX = {
    r"\g<p1>{YYYY\g<d1>MM\g<d2>DD\g<d3>HH\g<d4>mm\g<d5>ss\g<d6>SSSSSS}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_MICROSECOND_REGEX}",
    r"\g<p1>{YYYY\g<d1>MM\g<d2>DD\g<d3>HH\g<d4>mm\g<d5>ss\g<d6>SSS}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_MILLISECOND_REGEX}",
    r"\g<p1>{YYYY\g<d1>MM\g<d2>DD\g<d3>HH\g<d4>mm\g<d5>ss}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_SECOND_REGEX}",
    r"\g<p1>{YYYY}/\g<p2>{MM}/\g<p3>{DD}/\g<p4>{HH}/\g<p5>{mm}": rf"{EQUALS_PREFIX_REGEX(1)}{YEAR_REGEX}/{EQUALS_PREFIX_REGEX(2)}{MONTH_REGEX(False)}/{EQUALS_PREFIX_REGEX(3)}{DAY_REGEX(False)}/{EQUALS_PREFIX_REGEX(4)}{HOUR_REGEX}/{EQUALS_PREFIX_REGEX(5)}{MINUTE_REGEX}",
    r"\g<p1>{YYYY\g<d1>MM\g<d2>DD\g<d3>HH\g<d4>mm}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_MINUTE_REGEX}",
    r"\g<p1>{YYYY}/\g<p2>{MM}/\g<p3>{DD}/\g<p4>{HH}": rf"{EQUALS_PREFIX_REGEX(1)}{YEAR_REGEX}/{EQUALS_PREFIX_REGEX(2)}{MONTH_REGEX(False)}/{EQUALS_PREFIX_REGEX(3)}{DAY_REGEX(False)}/{EQUALS_PREFIX_REGEX(4)}{HOUR_REGEX}",
    r"\g<p1>{YYYY\g<d1>MM\g<d2>DD\g<d3>HH}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_HOUR_REGEX}",
    r"\g<p1>{YYYY}/\g<p2>{MM}/\g<p3>{DD}": rf"{EQUALS_PREFIX_REGEX(1)}{YEAR_REGEX}/{EQUALS_PREFIX_REGEX(2)}{MONTH_REGEX(False)}/{EQUALS_PREFIX_REGEX(3)}{DAY_REGEX(False)}",
    r"\g<p1>{YYYY\g<d1>MM\g<d2>DD}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_DAY_REGEX}",
    r"\g<p1>{YYYY}/\g<p2>{MM}": rf"{EQUALS_PREFIX_REGEX(1)}{YEAR_REGEX}/{EQUALS_PREFIX_REGEX(2)}{MONTH_REGEX(False)}",
    r"\g<p1>{YYYY\g<d1>MM}": rf"{EQUALS_PREFIX_REGEX(1)}{FULL_DATE_MONTH_REGEX}",
    r"\g<p1>{YYYY}": rf"{EQUALS_PREFIX_REGEX(1)}{YEAR_REGEX}",
}


EPOCH_PLACEHOLDER_TO_REGEX = {
    "{epoch}": EPOCH_REGEX,
}
NUMBER_PLACEHOLDER_TO_REGEX = {
    "{N}": NUMBER_REGEX,
}

UUID_PLACEHOLDER_TO_REGEX = {
    "{uuid}": UUID_REGEX_V4,
}


class SUPPORTED_FILE_TYPES(Enum):
    CSV = ".csv"
    JSON = ".json"
    PARQUET = ".parquet"
    ORC = ".orc"
    ORC_SNAPPY = ".orc.sz"
    AVRO = ".avro"
    TSV = ".tsv"


SUPPORTED_FILE_TYPES_SET = set({file_type.value for file_type in SUPPORTED_FILE_TYPES})


class PathPatternManager:
    """
    Manages the transformation and storage of file paths based on specified patterns.
    This class provides functionalities to add file paths after transforming them
    to a standardized format and to retrieve these paths based on matching patterns.

    Attributes:
        pattern_to_paths Dict[str, re.Pattern]: A dictionary that maps transformed
        path patterns to list of regex used to search for s3 files.
        pattern_to_actual_paths Dict[str, set[str]]: A dictionary that maps
        path patterns to the actual file paths that match the pattern.
    """

    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: tuple[str, datetime] = field(compare=False)

        def __init__(self, dt: datetime, item: tuple[str, datetime]):
            self.item = item
            self.priority = int(dt.timestamp())

    def __init__(self, n_most_recent: int = 3):
        self.pattern_to_regex_paths: Dict[str, re.Pattern] = {}
        # This is stored as a dictionary of str, heapq, where the heapq is a min heap. The heapq is used to store
        # the most recent N entries for each pattern
        self.pattern_to_actual_paths: Dict[
            str, list[PathPatternManager.PrioritizedItem]
        ] = {}
        self.n_most_recent = n_most_recent

    def substitute_if_unix_timestamp(self, path: str) -> str:
        """
        Checks if the path segment contains a UNIX timestamp and
        replaces it with a placeholder.
        """
        match = re.search(EPOCH_PLACEHOLDER_TO_REGEX["{epoch}"], path)
        if match:
            timestamp = int(match.group(0))
            try:
                date_time = datetime.fromtimestamp(timestamp)
                if datetime(2000, 1, 1) <= date_time <= datetime(2030, 12, 31):
                    path = path.replace(match.group(0), "{epoch}")
            except ValueError:
                pass
        return path

    def substitute_unknown_numbers_placeholder(self, path: str) -> str:
        """
        At this point any remaining numbers in the path are likely not dates. We can replace them with a placeholder,
        which allows us to group together paths that are similar except for the numbers.

        Example:
            2024/01/01/data.part1.csv and 2024/01/01/data.part2.csv -> 2024/01/01/data.part{N}.csv
        """
        path_only, file = self.split_path_and_file(path)
        new_file = re.sub(NUMBER_PLACEHOLDER_TO_REGEX["{N}"], "{N}", file)
        return "/".join([path_only, new_file])

    def split_path_and_file(self, path: str) -> tuple[str, str]:
        """
        Splits the path into the full directory path and the file name.
        """
        path_parts = path.split("/")
        file = path_parts[-1]
        path_only = "/".join(path_parts[:-1])
        return path_only, file

    def substitute_uuid_placeholders(self, path: str) -> str:
        """
        Replace UUIDs with {uuid}

        Example:
            2024/01/01/data.part1.csv and 2024/01/01/data.part2.csv -> 2024/01/01/data.part{N}.csv
        """

        return re.sub(UUID_PLACEHOLDER_TO_REGEX["{uuid}"], "{uuid}", path)

    def substitute_date_placeholders(self, path: str) -> tuple[str, Optional[datetime]]:
        """
        Applies regex patterns to replace date placeholders in paths with their regex equivalents.

        Args:
            path (str): The file path that may contain date patterns.

        Returns:
            str: The file path with dates standardized to placeholders.
        """
        path = self.substitute_if_unix_timestamp(path)
        # must happen before unknown numbers other numbers in uuid will be replace with {N}
        path = self.substitute_uuid_placeholders(path)
        date = None
        for placeholder, regex in DATE_PLACEHOLDER_TO_REGEX.items():
            if match := re.search(regex, path):
                path = re.sub(regex, placeholder, path)
                groups_without_delimiters = [
                    group
                    for index, group in enumerate(match.groups())
                    # even indices are either the prefix at the beginning or the delimiters
                    if index % 2 == 1
                ]
                # If date is already set, we don't want to overwrite it since we want the most specific
                # date available (order of regex patterns matters)
                if not date and len(groups_without_delimiters) >= 2:
                    # All regex patterns have year, month, day
                    date = datetime(
                        year=int(groups_without_delimiters[0]),
                        month=int(groups_without_delimiters[1]),
                        day=(
                            int(groups_without_delimiters[2])
                            if len(groups_without_delimiters) > 2
                            else 1
                        ),
                        hour=(
                            int(groups_without_delimiters[3])
                            if len(groups_without_delimiters) > 3
                            else 0
                        ),
                        minute=(
                            int(groups_without_delimiters[4])
                            if len(groups_without_delimiters) > 4
                            else 0
                        ),
                        second=(
                            int(groups_without_delimiters[5])
                            if len(groups_without_delimiters) > 5
                            else 0
                        ),
                    )
        path = self.substitute_unknown_numbers_placeholder(path)
        return path, date

    def template_to_regex(self, template) -> re.Pattern:
        """Converts a string template with placeholders into a regex pattern."""
        regex_pattern = template
        for placeholder, regex in DATE_PLACEHOLDER_TO_REGEX.items():
            regex_pattern = regex_pattern.replace(placeholder, regex)
        return re.compile(regex_pattern)

    def get_all_patterns(self) -> Iterable[str]:
        """
        Returns a list of all patterns that have been added to the manager.
        """
        return self.pattern_to_regex_paths.keys()

    def get_pattern_to_actual_paths(self) -> Dict[str, list[tuple[datetime, str]]]:
        """
        Returns a dictionary of all patterns and their corresponding file paths.
        """
        results: Dict[str, list[tuple[datetime, str]]] = {}
        for pattern, paths in self.pattern_to_actual_paths.items():
            results[pattern] = [(item.item[1], item.item[0]) for item in paths]
        return results

    def get_regex_from_pattern(self, pattern: str) -> Optional[re.Pattern]:
        """
        Returns the matching regex for pattern that has been added to the manager.
        """
        return self.pattern_to_regex_paths.get(pattern, None)

    def add_filepaths(self, filepath: list[str]) -> int:
        """
        Transforms a file path based on predefined patterns and stores the transformed
        path along with the original file path in the manager.

        Args:
            filepath (str): The file path to be added, which will be transformed and stored.
        Returns:
            int: Number of new patterns added to the manager.
        """
        unique_filepaths = set(filepath)
        new_patterns = 0

        for path in unique_filepaths:
            original_path = path
            unquoted_path = path
            try:
                while unquoted_path != (unquoted_path := unquote(unquoted_path)):
                    pass
                transformed_path, dt = self.substitute_date_placeholders(unquoted_path)
                # Only save pattern if we were able to extract a datetime from it
                if dt:
                    if transformed_path not in self.pattern_to_regex_paths:
                        regex_pattern = self.template_to_regex(transformed_path)
                        self.pattern_to_regex_paths[transformed_path] = regex_pattern
                        self.pattern_to_actual_paths[transformed_path] = []
                        new_patterns += 1

                    if (
                        len(self.pattern_to_actual_paths[transformed_path])
                        < self.n_most_recent
                    ):
                        # Add to heap if it's not full
                        heapq.heappush(
                            self.pattern_to_actual_paths[transformed_path],
                            PathPatternManager.PrioritizedItem(dt, (original_path, dt)),
                        )
                    else:
                        # If the heap is full, push the new item and pop the smallest item
                        heapq.heappushpop(
                            self.pattern_to_actual_paths[transformed_path],
                            PathPatternManager.PrioritizedItem(dt, (original_path, dt)),
                        )
            except Exception as e:
                log_debug(f"Error adding file paths '{original_path}': {e}")
        return new_patterns
