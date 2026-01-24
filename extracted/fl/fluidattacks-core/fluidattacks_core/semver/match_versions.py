import logging
import re
from functools import lru_cache
from itertools import (
    zip_longest,
)

LOGGER = logging.getLogger(__name__)

INFINITE = "//INFINITE//"
PLATFORM_SPECIFIERS = {"macos", "darwin", "linux", "win", "mingw"}


def _simplify_pre_release(pre_release: str) -> str | None:
    if any(platform_specifier in pre_release for platform_specifier in PLATFORM_SPECIFIERS):
        return None
    return pre_release


def _normalize_version_operators(version: str) -> str:
    return re.sub(r"([><=!~^]+)\s*", r"\1", version)


def normalize(version: str) -> tuple[list[str], str | None]:
    # Split the version into parts and handle the pre-release part
    version_split = version.split("-", maxsplit=1) if version.count("-") >= 1 else [version]

    # Handle epoch in version parts (only if it looks like RPM epoch)
    version_part = version_split[0]
    if ":" in version_part and not any(op in version_part for op in ["<", ">", "="]):
        # This looks like an RPM epoch, convert it
        epoch_part, rest_version = version_part.split(":", 1)
        version_part = f"{epoch_part}.{rest_version}"

    version_parts = list(re.split(r"[\-\.]", version_part))
    pre_release = version_split[1] if len(version_split) > 1 else None
    simplified_pre_release = _simplify_pre_release(pre_release.lower()) if pre_release else None
    return version_parts, simplified_pre_release


def _aux_compare_tokens(token1: str, token2: str) -> bool | None:
    if token1.isdigit() and token2.isdigit():
        return int(token1) > int(token2)
    if token1.isdigit() or token1 == INFINITE:
        return True
    if token2.isdigit() or token2 == INFINITE:
        return False
    # Compare non-numeric qualifiers
    if token1 != token2:
        return token1 > token2
    return None


def _aux_compare_suffix(suffix1: str, suffix2: str) -> bool | None:
    if suffix1 and not suffix2:
        return True
    if suffix2 and not suffix1:
        return False
    if suffix1 != suffix2:
        return suffix1 > suffix2
    return None


def compare_tokens(token1: str, token2: str) -> bool | None:
    if "+" in token1 or "+" in token2:
        t1_parts = token1.split("+", 1)
        t2_parts = token2.split("+", 1)
        num1 = t1_parts[0]
        num2 = t2_parts[0]
        suffix1 = t1_parts[1] if len(t1_parts) > 1 else ""
        suffix2 = t2_parts[1] if len(t2_parts) > 1 else ""
        if num1.isdigit() and num2.isdigit():
            if int(num1) != int(num2):
                return int(num1) > int(num2)
        elif num1 != num2:
            return num1 > num2
        result = _aux_compare_suffix(suffix1, suffix2)
        if result is not None:
            return result

    return _aux_compare_tokens(token1, token2)


def compare_pre_releases(v1_pre_release: str | None, v2_pre_release: str | None) -> bool:
    if v1_pre_release is None and v2_pre_release is not None:
        return True
    if v1_pre_release is not None and v2_pre_release is None:
        return False
    if v1_pre_release and v2_pre_release:
        return v1_pre_release > v2_pre_release
    return False


def compare_versions(*, version1: str, version2: str, include_same: bool = False) -> bool:
    """Compare two version ranges.

    Returns True if version1 is higher or equal than version2.
    """
    version_1, v1_pre_release = normalize(version1)
    version_2, v2_pre_release = normalize(version2)

    if include_same and version_1 == version_2 and v1_pre_release == v2_pre_release:
        return True

    for part1, part2 in zip_longest(version_1, version_2, fillvalue="0"):
        if part1 != part2:
            comparison = compare_tokens(part1, part2)
            if comparison is not None:
                return comparison

    if (
        not v2_pre_release
        and all(specifier == "0" for specifier in version_2)
        and all(specifier == "0" for specifier in version_1)
    ):
        return True

    # When version parts are equal, compare pre-releases
    # Only compare pre-releases if both versions have them (e.g., RPM release numbers)
    # If only one has a pre-release, it's a semantic pre-release (alpha, beta, etc.)
    # and the version with pre-release is considered lower
    if v1_pre_release and v2_pre_release and v1_pre_release != v2_pre_release:
        return compare_pre_releases(v1_pre_release, v2_pre_release)

    if include_same:
        return compare_pre_releases(v1_pre_release, v2_pre_release)

    return False


def parse_version_range(version_range: str) -> tuple[str, ...]:
    if version_range.startswith(("<", "<=")):
        version_range = ">0 " + version_range
    if version_range.startswith((">", ">=")) and "<" not in version_range:
        version_range = version_range + f" <{INFINITE}"

    range_pattern = re.compile(r"([<>]=?)\s*([^<>=\s]+)")
    matches = range_pattern.findall(version_range)
    operators_and_values = [item for pair in matches for item in pair]
    return tuple(operators_and_values)


def _safe_parse_version_range(version_range: str) -> tuple[str, ...] | None:
    parts = parse_version_range(version_range)
    if len(parts) != 4:
        LOGGER.error("Invalid version range: %s. Values cannot be parsed.", version_range)
        return None
    return parts


def is_single_version(range_str: str) -> bool:
    operator_pattern = re.compile(r"[<>]")
    return not bool(operator_pattern.search(range_str))


def is_single_version_in_range(version: str, _range: str) -> bool:
    single_version = version.lstrip("=")
    range_parts = _safe_parse_version_range(_range)

    if range_parts is None:
        return False

    op1, min2, op2, max2 = range_parts

    include_same_1 = "=" in op1
    include_same_2 = "=" in op2
    return compare_versions(
        version1=single_version,
        version2=min2,
        include_same=include_same_1,
    ) and compare_versions(
        version1=max2,
        version2=single_version,
        include_same=include_same_2,
    )


def do_ranges_intersect(range1: str, range2: str) -> bool:
    """Compare two version ranges.

    Returns True if the input ranges intersect
    """
    is_single_version1 = is_single_version(range1)
    is_single_version2 = is_single_version(range2)
    if is_single_version1 and is_single_version2:
        return range1 == range2

    if is_single_version1:
        return is_single_version_in_range(range1, range2)

    if is_single_version2:
        return is_single_version_in_range(range2, range1)

    range1_parts = _safe_parse_version_range(range1)
    range2_parts = _safe_parse_version_range(range2)

    if range1_parts is None or range2_parts is None:
        return False

    op1_r1, lower1, op2_r1, upper1 = range1_parts
    op1_r2, lower2, op2_r2, upper2 = range2_parts

    include_same_1 = bool("=" in op1_r1 and "=" in op2_r2)
    include_same_2 = bool("=" in op1_r2 and "=" in op2_r1)

    return compare_versions(
        version1=upper2,
        version2=lower1,
        include_same=include_same_1,
    ) and compare_versions(
        version1=upper1,
        version2=lower2,
        include_same=include_same_2,
    )


def convert_asterisk_to_range(version: str) -> str:
    semver_pattern = re.compile(r"^(\d+)(\.(\*|\d+)(\.(\*|\d+))?)?$")
    match = semver_pattern.match(version)
    if match:
        major, _, minor, _, patch = match.groups()
        if patch == "*":
            return f">={major}.{minor}.0 <{major}.{minor}.{INFINITE}"
        if minor == "*":
            return f">={major}.0.0 <{major}.{INFINITE}.0"
    return version


def increment_version(version: str, position: int) -> str:
    parts = version.split(".")
    if len(parts) < 2:
        parts.extend(["0"] * (2 - len(parts)))
        position -= 1

    if position < len(parts):
        parts[position] = INFINITE
        for idx in range(position + 1, len(parts)):
            parts[idx] = "0"
    return ".".join(parts)


def simplify_final_version(version: str) -> str:
    if "+" in version:
        version = version.rsplit("+", 1)[0]
    ranges = version.lower().split(".")
    if "final" in ranges[-1]:
        return ".".join(ranges[:-1])
    return version


def convert_semver_to_range(version: str) -> str:
    version = version.replace("==", "=")
    version = version.replace(" ", "")
    if version.startswith("~"):
        version = version[1:]
        return f">={version} <{increment_version(version, 2)}"

    if version.startswith("^"):
        version = version[1:]
        return f">={version} <{increment_version(version, 1)}"

    if ".*" in version:
        return convert_asterisk_to_range(version)

    if is_single_version(version) and not version.startswith("="):
        return f"={simplify_final_version(version)}"

    return simplify_final_version(version)


def convert_to_range(version: str) -> list[str]:
    normalized_version = _normalize_version_operators(version)
    and_ranges = re.split(r"[,\s]+", normalized_version)
    return [convert_semver_to_range(and_range.strip()) for and_range in and_ranges]


def match_version_ranges(dep_version: str, vulnerable_version: str) -> bool:
    and_ranges = convert_to_range(dep_version)
    vulnerable_ranges = vulnerable_version.split("||")
    for vuln_range in vulnerable_ranges:
        vuln_range = convert_semver_to_range(vuln_range.strip())  # noqa: PLW2901
        if all(do_ranges_intersect(and_range, vuln_range) for and_range in and_ranges):
            return True
    return False


@lru_cache(maxsize=100000)
def match_vulnerable_versions(dep_version: str, advisory_range: str | None) -> bool:
    if advisory_range is None:
        return False
    dep_version = _normalize_version_operators(dep_version)
    try:
        dep_versions = dep_version.replace("||", "|").split("|")
        if any(
            match_version_ranges(dep_version.strip(), advisory_range)
            for dep_version in dep_versions
        ):
            return True
    except ValueError:
        err_msg = (
            f"Error in simple match. Dependency version: {dep_version}, "
            f"Advisory vulnerable versions: {advisory_range}, "
        )
        LOGGER.exception(err_msg)
        return False
    else:
        return False
